"""Command-line tool.

  python -m tjplus.cli interval --standards ref.csv --new routine.csv [--batch-column lot] [--alpha 0.1]
                                [--rule jackknife+|gauss] [--threshold 14] [--out result.csv]
      ref.csv:     columns 'prediction' (original-calibration prediction), 'reference' (reference value),
                   optional batch column
      routine.csv: column 'prediction'
  python -m tjplus.cli plan --standards 20 --batches 2 [--rho 0.5] [--alpha 0.1]
"""
import argparse, sys
import numpy as np
import pandas as pd
from .api import SBCIntervals, plan

def main(argv=None):
    ap = argparse.ArgumentParser(prog="tjplus", description="Prediction intervals after calibration transfer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("interval", help="slope/bias correction with prediction intervals")
    a.add_argument("--standards", required=True); a.add_argument("--new", required=True)
    a.add_argument("--batch-column", default=None); a.add_argument("--alpha", type=float, default=0.1)
    a.add_argument("--rule", default="jackknife+", choices=["jackknife+", "gauss", "anova"])
    a.add_argument("--threshold", type=float, default=None); a.add_argument("--out", default=None)
    p = sub.add_parser("plan", help="expected coverage for new batches for a sampling design")
    p.add_argument("--standards", type=int, required=True); p.add_argument("--batches", type=int, required=True)
    p.add_argument("--rho", type=float, default=0.5); p.add_argument("--alpha", type=float, default=0.1)
    args = ap.parse_args(argv)
    if args.cmd == "plan":
        res = plan(args.standards, args.batches, args.rho, args.alpha)
        print(f"{args.standards} standards from {args.batches} batches, intra-batch correlation {args.rho}, "
              f"nominal coverage {1 - args.alpha:.2f}")
        names = {"gauss_loo": "Gaussian, leave one sample out", "tj_plus": "jackknife+, leave one sample out",
                 "tj_b": "jackknife+, leave one batch out", "gauss_lgo": "Gaussian, leave one batch out"}
        for k, lab in names.items():
            r = res[k]
            txt = "no finite interval (too few batches)" if r["frac_inf"] > 0.5 else f"expected coverage {r['coverage']:.3f}"
            print(f"  {lab:34s} {txt}")
        return 0
    std = pd.read_csv(args.standards); new = pd.read_csv(args.new)
    unit = "batch" if args.batch_column else "sample"
    iv = SBCIntervals(alpha=args.alpha, unit=unit, rule=args.rule).fit(
        std["prediction"], std["reference"], None if unit == "sample" else std[args.batch_column])
    yhat, lo, hi = iv.predict(new["prediction"])
    out = new.copy(); out["corrected"] = yhat; out["lower"] = lo; out["upper"] = hi
    if args.threshold is not None:
        out["decision"] = iv.decide(new["prediction"], args.threshold)
    if args.out:
        out.to_csv(args.out, index=False)
    else:
        out.to_csv(sys.stdout, index=False)
    n_inf = int((~np.isfinite(hi)).sum())
    if n_inf:
        print(f"warning: {n_inf} unbounded intervals (too few {'batches' if unit == 'batch' else 'standards'} "
              f"for alpha = {args.alpha})", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
