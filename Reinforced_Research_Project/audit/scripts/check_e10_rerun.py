"""Deviation R3 check: after the ANOVA-PI correction, every other E10 method must reproduce the superseded run exactly
(same seeds). Writes audit/data/e10_rerun_check.json."""
import glob, json, os
import numpy as np, pandas as pd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "results", "raw")
keys = ["setting", "kind", "design", "K", "n_g", "rep", "alpha", "method"]
new = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(RAW, "E10_batch@*.csv.gz")))])
old = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(RAW, "superseded_E10_anova_loo", "E10_batch@*.csv.gz")))])
m = new.merge(old, on=keys, suffixes=("", "_old"))
cols = ["new_coverage", "new_median_width", "same_coverage"]
out = {"rows_new": len(new), "rows_old": len(old), "rows_matched": len(m)}
for meth, g in m.groupby("method"):
    diff = max(float(np.nanmax(np.abs(g[c] - g[c + "_old"]))) for c in cols)
    out[meth] = diff
json.dump(out, open(os.path.join(ROOT, "audit", "data", "e10_rerun_check.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
