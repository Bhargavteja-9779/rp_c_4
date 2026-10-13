"""Interval evaluation metrics."""
import numpy as np

def interval_metrics(lo, hi, y, alpha):
    lo = np.broadcast_to(lo, y.shape); hi = np.broadcast_to(hi, y.shape)
    cov = (y >= lo) & (y <= hi)
    finite = np.isfinite(lo) & np.isfinite(hi)
    width = hi - lo
    if finite.all():
        IS = np.mean(width + (2 / alpha) * np.maximum(lo - y, 0) + (2 / alpha) * np.maximum(y - hi, 0))
    else:
        IS = np.inf
    return dict(coverage=float(cov.mean()),
                width=float(width[finite].mean()) if finite.any() else np.nan,
                median_width=float(np.median(width[finite])) if finite.any() else np.nan,
                frac_inf=float(1 - finite.mean()), interval_score=float(IS),
                miss_lo=float((y < lo).mean()), miss_hi=float((y > hi).mean()), n_test=int(len(y)))

def tertile_coverage(lo, hi, y, z, prefix):
    """Coverage within tertiles of z (computed on the test set)."""
    lo = np.broadcast_to(lo, y.shape); hi = np.broadcast_to(hi, y.shape)
    cov = (y >= lo) & (y <= hi)
    edges = np.quantile(z, [1 / 3, 2 / 3])
    b = np.digitize(z, edges)
    return {f"{prefix}{k + 1}": float(cov[b == k].mean()) if (b == k).any() else np.nan for k in range(3)}
