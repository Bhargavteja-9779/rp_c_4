"""Compact raw result files for archiving (GitHub file-size limits):
- per-repetition files: rewritten with 6 significant digits (far below any reported precision);
- per-sample files (error analysis): only the m used by the error-analysis figure is kept
  (corn m=15, tablets m=20, mango m=20), 6 significant digits.
Idempotent. Usage: python scripts/compact_raw.py ../results/raw"""
import glob, os, sys
import pandas as pd
KEEP_M = {"corn": 15, "tablets": 20, "mango": 20}
raw = sys.argv[1]
for f in sorted(glob.glob(os.path.join(raw, "E*.csv.gz"))):
    d = pd.read_csv(f)
    before = os.path.getsize(f)
    if f.endswith("_samples.csv.gz"):
        ds = d["dataset"].iloc[0]
        d = d[d["m"] == KEEP_M[ds]]
    tmp = f + ".tmp.gz"
    d.to_csv(tmp, index=False, float_format="%.6g", compression="gzip")
    os.replace(tmp, f)
    print(f"{os.path.basename(f)}: {before/1e6:.1f} MB -> {os.path.getsize(f)/1e6:.1f} MB")
