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
