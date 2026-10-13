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
              "86159e2df9244fa52f821856ea003f562ef7f6a031dd08794e3cd4458f0f153f", "NAnderson2020MendeleyMangoNIRData.csv"),
}

def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch(name, raw_dir):
    url, sha, fname = SOURCES[name]
    os.makedirs(raw_dir, exist_ok=True)
    path = os.path.join(raw_dir, fname)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tjplus reproducibility)"})
        with urllib.request.urlopen(req, timeout=300) as r, open(path, "wb") as f:
            f.write(r.read())
    got = _sha256(path)
    if got != sha:
        raise RuntimeError(f"Checksum mismatch for {path}: {got} != {sha}. Delete the file and retry.")
    return path

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
