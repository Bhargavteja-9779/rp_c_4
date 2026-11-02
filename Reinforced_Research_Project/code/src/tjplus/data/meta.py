"""Batch (population) and harvest-date metadata for the mango data, aligned row-by-row with the
fruit-level arrays returned by `loaders.load_mango` and `loaders.load_mango_instruments`.

A *population* in the mango data is a consignment of about 40 fruit of one cultivar, region, maturity
stage and harvest date (data providers' definition). It is used here as the batch unit."""
import functools
import numpy as np
import pandas as pd
from .loaders import fetch, MANGO_FRUIT_KEY

@functools.lru_cache(maxsize=None)
def load_mango_meta(raw_dir):
    """Per-fruit metadata in the order of `load_mango` (groupby on MANGO_FRUIT_KEY, sorted)."""
    d = pd.read_csv(fetch("mango", raw_dir), usecols=MANGO_FRUIT_KEY)
    idx = d.groupby(MANGO_FRUIT_KEY, sort=True).size().index.to_frame(index=False)
    idx["date"] = pd.to_datetime(idx["Date"], format="%d/%m/%Y")
    return pd.DataFrame({"season": idx["Season"].to_numpy(int), "pop": idx["Pop"].astype(str).to_numpy(),
                         "date": idx["date"].to_numpy(), "dm": idx["DM"].to_numpy(float),
                         "cultivar": idx["Cultivar"].to_numpy(), "region": idx["Region"].to_numpy()})

@functools.lru_cache(maxsize=None)
def load_mango_inst_meta(raw_dir, instruments=(15006, 15016, 15014, 15029)):
    """Per-fruit metadata in the order of `load_mango_instruments` (sorted season_reference keys)."""
    d = pd.read_csv(fetch("mango_v4", raw_dir),
                    usecols=["outlier_flag_1", "season", "reference_no", "instrument", "population", "date"],
                    dtype=str, low_memory=False)
    d = d[(d["outlier_flag_1"].astype(float) == 0) & d["instrument"].astype(float).astype(int).isin(instruments)]
    d["key"] = d["season"].astype(float).astype(int).astype(str) + "_" + d["reference_no"].astype(str)
    g = d.groupby("key").agg(pop=("population", "first"), npop=("population", "nunique"), date=("date", "min"))
    keys = sorted(d["key"].unique())
    g = g.reindex(keys)
    if (g["npop"] > 1).any():
        raise ValueError("fruit key mapped to several populations")
    return pd.DataFrame({"key": keys, "pop": g["pop"].astype(str).to_numpy(),
                         "date": pd.to_datetime(g["date"]).to_numpy()})

@functools.lru_cache(maxsize=None)
def load_mango_v6_settings(raw_dir, wl_min=684, wl_max=990):
    """All fruit x instrument spectra of the providers' extended mango file (record version 6), outlier-flagged
    spectra removed, replicate spectra averaged per fruit (season + reference number) and instrument.
    Returns a long DataFrame of metadata and an aligned spectra array. Cached as npz + csv next to the raw file."""
    import os
    path = fetch("mango_v4", raw_dir)
    cache_x = os.path.join(raw_dir, "mango_v6_all_instruments_X.npy")
    cache_m = os.path.join(raw_dir, "mango_v6_all_instruments_meta.csv")
    if os.path.exists(cache_x) and os.path.exists(cache_m):
        return pd.read_csv(cache_m, dtype={"key": str, "pop": str}), np.load(cache_x)
    head = pd.read_csv(path, nrows=0).columns
    wl_cols = [c for c in head if c.replace(".", "", 1).isdigit() and wl_min <= float(c) <= wl_max]
    d = pd.read_csv(path, usecols=["outlier_flag_1", "season", "reference_no", "dry_matter", "instrument",
                                   "population", "date"] + wl_cols, dtype={"reference_no": str, "population": str,
                                   "date": str}, low_memory=False)
    d = d[d["outlier_flag_1"] == 0]
    d["key"] = d["season"].astype(int).astype(str) + "_" + d["reference_no"].astype(str)
    g = d.groupby(["key", "instrument"])
    X = g[wl_cols].mean()
    meta = g.agg(season=("season", "first"), pop=("population", "first"), date=("date", "min"),
                 y=("dry_matter", "mean")).reindex(X.index).reset_index()
    np.save(cache_x, X.to_numpy(float)); meta.to_csv(cache_m, index=False)
    return meta, X.to_numpy(float)
