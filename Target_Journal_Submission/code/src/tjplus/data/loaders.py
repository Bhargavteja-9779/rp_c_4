"""Download (with SHA-256 verification), cache and parse the three public NIR data sets.

Data sets
---------
corn     : Eigenvector Research corn data (80 samples x 3 NIR instruments m5, mp5, mp6; 4 properties).
tablets  : IDRC Shootout 2002 pharmaceutical tablets (655 tablets x 2 instruments; weight, hardness, assay).
mango    : Anderson et al. (2020) mango dry-matter NIR data, Mendeley Data doi:10.17632/46htwnp833.
"""
import hashlib, io, os, urllib.request, zipfile
from dataclasses import dataclass, field
import functools
import numpy as np

SOURCES = {
    "corn": ("https://eigenvector.com/wp-content/uploads/2019/06/corn.mat_.zip",
             "8a2d1a03648b6ad334caaafa5d8377bf945ba1477a5082c4963d705d07cca795", "corn.mat_.zip"),
    "tablets": ("https://eigenvector.com/wp-content/uploads/2019/06/nir_shootout_2002.mat_.zip",
                "04c03a4314ab8e8f63e0ecc788b657b5d1b5450791ce465ad41ad90cb5d52125", "nir_shootout_2002.mat_.zip"),
    "mango": ("https://data.mendeley.com/public-files/datasets/46htwnp833/files/62760987-c0a4-48c7-86cd-eb9d60f77e48/file_downloaded",
              "86159e2df9244fa52f821856ea003f562ef7f6a031dd08794e3cd4458f0f153f", "NAnderson2020MendeleyMangoNIRData.csv"),  # record version 1
    "mango_v4": ("https://data.mendeley.com/public-files/datasets/46htwnp833/files/747b2613-4d0a-4628-8aaf-8fc5547d286e/file_downloaded",
                 "367c377255c350f322387236ed121629807055baa3f02aeaf5a76fe9ada518b6", "MangoDMC_NIR_Data_v4.csv"),  # record version 6
}

def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch(name, raw_dir, retries=5):
    """Download (streamed, with retries) into a temporary file, verify SHA-256, then rename atomically.
    Partial downloads never leave a file under the final name."""
    import time
    url, sha, fname = SOURCES[name]
    os.makedirs(raw_dir, exist_ok=True)
    path = os.path.join(raw_dir, fname)
    if not os.path.exists(path):
        tmp = path + f".part{os.getpid()}"
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tjplus reproducibility)"})
                with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        f.write(chunk)
                if _sha256(tmp) != sha:
                    raise IOError("checksum mismatch after download")
                os.replace(tmp, path)
                break
            except Exception as e:
                if os.path.exists(tmp):
                    os.remove(tmp)
                if attempt == retries - 1:
                    raise RuntimeError(f"Download of {name} failed after {retries} attempts: {e}. "
                                       f"Download {url} manually into {raw_dir}/{fname}.")
                time.sleep(2 ** (attempt + 1))
    got = _sha256(path)
    if got != sha:
        raise RuntimeError(f"Checksum mismatch for {path}: {got} != {sha}. Delete the file and retry.")
    return path

def prefetch_all(raw_dir):
    """Fetch every data set once (called in the main process before parallel workers start)."""
    return {k: fetch(k, raw_dir) for k in SOURCES}

def _ds(mobj):
    """Extract the .data field of a PLS_Toolbox DataSet object read by scipy."""
    return np.asarray(mobj[0, 0]["data"], dtype=float)

def _mat_from_zip(path):
    import scipy.io as sio
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".mat") and not n.startswith("__MACOSX")][0]
        return sio.loadmat(io.BytesIO(z.read(name)))

@dataclass
class MultiInstrumentData:
    """Spectra of the same physical samples on several instruments."""
    name: str
    spectra: dict            # instrument -> (n, p) array
    Y: np.ndarray            # (n, k)
    properties: list
    wavelengths: np.ndarray
    split: np.ndarray = None # optional predefined split labels per sample
    meta: dict = field(default_factory=dict)

@functools.lru_cache(maxsize=None)
def load_corn(raw_dir):
    m = _mat_from_zip(fetch("corn", raw_dir))
    spectra = {k: _ds(m[k + "spec"]) for k in ("m5", "mp5", "mp6")}
    Y = _ds(m["propvals"])
    return MultiInstrumentData("corn", spectra, Y, ["moisture", "oil", "protein", "starch"],
                               np.arange(1100, 2500, 2, dtype=float))

@functools.lru_cache(maxsize=None)
def load_tablets(raw_dir):
    m = _mat_from_zip(fetch("tablets", raw_dir))
    parts = ["calibrate", "validate", "test"]
    spectra = {inst: np.vstack([_ds(m[f"{p}_{inst}"]) for p in parts]) for inst in ("1", "2")}
    Y = np.vstack([_ds(m[f"{p}_Y"]) for p in parts])
    split = np.concatenate([[p] * _ds(m[f"{p}_Y"]).shape[0] for p in parts])
    wl = np.asarray(m["calibrate_1"][0, 0]["axisscale"][1, 0], dtype=float).ravel()
    return MultiInstrumentData("tablets", spectra, Y, ["weight", "hardness", "assay"], wl, split)

@dataclass
class SeasonData:
    name: str
    X: np.ndarray        # fruit-averaged spectra (n_fruit, p)
    y: np.ndarray        # dry matter content (%)
    season: np.ndarray   # 1..4
    wavelengths: np.ndarray
    n_scans: np.ndarray  # number of scans averaged per fruit

MANGO_META = ["Set", "Season", "Region", "Date", "Type", "Cultivar", "Pop", "Temp", "DM"]
MANGO_FRUIT_KEY = ["Season", "Region", "Date", "Type", "Cultivar", "Pop", "DM"]

@functools.lru_cache(maxsize=None)
def load_mango(raw_dir, wl_min=684, wl_max=990):
    """Average replicate scans per fruit (fruit identified by the metadata key + DM value) to
    prevent replicate leakage; restrict to the 684-990 nm region used by Anderson et al. (2020)."""
    import pandas as pd
    d = pd.read_csv(fetch("mango", raw_dir))
    wl_cols = [c for c in d.columns if c not in MANGO_META]
    wl = np.array([float(c) for c in wl_cols])
    keep = [c for c, w in zip(wl_cols, wl) if wl_min <= w <= wl_max]
    g = d.groupby(MANGO_FRUIT_KEY, sort=True)
    Xf = g[keep].mean()
    n_scans = g.size().loc[Xf.index].to_numpy()
    idx = Xf.index.to_frame(index=False)
    return SeasonData("mango", Xf.to_numpy(float), idx["DM"].to_numpy(float), idx["Season"].to_numpy(int),
                      np.array([float(c) for c in keep]), n_scans)


@dataclass
class PairedInstrumentData:
    name: str
    spectra: dict        # instrument -> (n_fruit, p) fruit-mean spectra (NaN rows where not measured)
    y: np.ndarray
    present: dict        # instrument -> bool mask of fruit measured on it
    wavelengths: np.ndarray

@functools.lru_cache(maxsize=None)
def load_mango_instruments(raw_dir, instruments=(15006, 15016, 15014, 15029), wl_min=684, wl_max=990):
    """Mango multi-instrument data (Mendeley record version 6, file MangoDMC_NIR_Data_v4.csv): spectra flagged as
    outliers by the providers (outlier_flag_1 != 0) are excluded; replicate spectra are averaged per fruit
    (season + reference number) and instrument. A processed cache is written next to the raw file."""
    import pandas as pd
    path = fetch("mango_v4", raw_dir)
    cache = os.path.join(raw_dir, "mango_instruments_" + "_".join(map(str, instruments)) + ".npz")
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=False)
        inst = [int(i) for i in z["instruments"]]
        return PairedInstrumentData("mango_inst", {i: z[f"X_{i}"] for i in inst}, z["y"],
                                    {i: z[f"P_{i}"] for i in inst}, z["wl"])
    head = pd.read_csv(path, nrows=0).columns
    wl_cols = [c for c in head if c.replace(".", "", 1).isdigit()]
    keep = [c for c in wl_cols if wl_min <= float(c) <= wl_max]
    d = pd.read_csv(path, usecols=["outlier_flag_1", "season", "reference_no", "dry_matter", "instrument"] + keep,
                    dtype={"reference_no": str})
    d = d[(d["outlier_flag_1"] == 0) & d["instrument"].isin(instruments)]
    d["key"] = d["season"].astype(str) + "_" + d["reference_no"].astype(str)
    g = d.groupby(["key", "instrument"])[keep].mean()
    keys = sorted(d["key"].unique())
    y = d.groupby("key")["dry_matter"].mean().reindex(keys).to_numpy(float)
    spectra, present = {}, {}
    for i in instruments:
        X = np.full((len(keys), len(keep)), np.nan)
        gi = g.xs(i, level="instrument")
        idx = pd.Index(keys).get_indexer(gi.index)
        X[idx] = gi.to_numpy(float)
        spectra[i], present[i] = X, ~np.isnan(X).any(1)
    wl = np.array([float(c) for c in keep])
    np.savez_compressed(cache, instruments=np.array(instruments), y=y, wl=wl,
                        **{f"X_{i}": spectra[i] for i in instruments}, **{f"P_{i}": present[i] for i in instruments})
    return PairedInstrumentData("mango_inst", spectra, y, present, wl)
