"""Practical interface for laboratories: prediction intervals for a transferred calibration.

Two entry points:

* ``SBCIntervals`` works on the *predictions* of the original calibration, which is what most instruments
  (including handheld fruit meters) export. It fits slope/bias correction on the reference samples and returns,
  for every new prediction, the corrected value and a prediction interval:
    - ``unit="sample"``: transfer jackknife+ with leave-one-sample-out refits (valid when the reference samples
      are a random sample of the routine samples, or come from different, randomly chosen batches);
    - ``unit="batch"``: leave-one-batch-out (hierarchical) jackknife+, valid for samples from new batches if the
      batches were chosen at random (needs >= 9 batches at 90 %); ``rule="gauss"`` gives the simpler t-interval.
* ``transfer_jackknife`` wraps any transfer method given as a fitting function (e.g. PDS on spectra).

``plan`` predicts the coverage of each rule for a sampling design (see ``tjplus.planning``).

Example
-------
>>> iv = SBCIntervals(alpha=0.1, unit="batch").fit(f_std, y_std, batch=lot_std)
>>> yhat, lower, upper = iv.predict(f_new)
>>> decision = iv.decide(f_new, threshold=14.0)      # 'pass' / 'fail' / 'refer'
"""
import numpy as np
from scipy import stats
from .planning import expected_coverage, kappa

def _ranks(m, alpha):
    ku = int(np.ceil((1 - alpha) * (m + 1) - 1e-12))
    kl = int(np.floor(alpha * (m + 1) + 1e-12))
    return ku, kl

def _jackknife_plus(centres, radii, alpha, weights=None, n_units=None):
    """centres, radii: (m, n_new). Unweighted: ordinary jackknife+; weights: per-row weights summing to K/(K+1)."""
    up, lo = centres + radii, centres - radii
    m = centres.shape[0]
    if weights is None:
        ku, kl = _ranks(m, alpha)
        U = np.sort(up, 0)[ku - 1] if ku <= m else np.full(up.shape[1], np.inf)
        L = np.sort(lo, 0)[kl - 1] if kl >= 1 else np.full(lo.shape[1], -np.inf)
        return L, U
    def wq(V):
        order = np.argsort(V, 0); Vs = np.take_along_axis(V, order, 0)
        cw = np.cumsum(weights[order], 0); hit = cw >= (1 - alpha) - 1e-12
        out = np.full(V.shape[1], np.inf); ok = hit.any(0); idx = np.argmax(hit, 0)
        out[ok] = Vs[idx[ok], np.nonzero(ok)[0]]
        return out
    return -wq(-lo), wq(up)

def _sbc_fit(f, y):
    if len(np.unique(f)) < 2:
        return 1.0, float(np.mean(y - f))
    b, a = np.polyfit(f, y, 1)
    return float(b), float(a)

class SBCIntervals:
    """Slope/bias correction with prediction intervals from the reference samples themselves."""

    def __init__(self, alpha=0.1, unit="sample", rule="jackknife+", slope=True):
        if unit not in ("sample", "batch"):
            raise ValueError("unit must be 'sample' or 'batch'")
        if rule not in ("jackknife+", "gauss", "anova"):
            raise ValueError("rule must be 'jackknife+', 'gauss' or 'anova'")
        if rule == "anova" and unit != "batch":
            raise ValueError("rule='anova' (random-effects interval for a new batch) needs unit='batch'")
        self.alpha, self.unit, self.rule, self.slope = alpha, unit, rule, slope

    def _fit_one(self, f, y):
        return _sbc_fit(f, y) if self.slope else (1.0, float(np.mean(y - f)))

    def fit(self, f_std, y_std, batch=None):
        f = np.asarray(f_std, float); y = np.asarray(y_std, float)
        if len(f) != len(y) or len(f) < 3:
            raise ValueError("need at least three reference samples with predictions and reference values")
        if self.unit == "batch":
            if batch is None:
                raise ValueError("unit='batch' needs a batch label for every reference sample")
            groups = np.asarray(batch)
        else:
            groups = np.arange(len(f))
        self.labels_ = np.unique(groups)
        self.K_ = len(self.labels_)
        self.full_ = self._fit_one(f, y)
        self.loo_ = []; res = np.empty(len(f)); unit_of = np.empty(len(f), int)
        for k, lab in enumerate(self.labels_):
            out = groups == lab
            if (~out).sum() < 2:
                raise ValueError("each leave-out fit needs at least two remaining reference samples")
            b, a = self._fit_one(f[~out], y[~out])
            self.loo_.append((b, a))
            res[out] = y[out] - (a + b * f[out]); unit_of[out] = k
        self.residuals_ = res; self.unit_of_ = unit_of
        self.n_ = len(f)
        return self

    def predict(self, f_new):
        f = np.atleast_1d(np.asarray(f_new, float))
        b, a = self.full_
        yhat = a + b * f
        if self.rule == "anova":
            e = self.residuals_; labs = self.unit_of_; K = self.K_; N = len(e)
            n = np.bincount(labs, minlength=K); nbar = float(np.mean(n))
            means = np.array([e[labs == k].mean() for k in range(K)])
            if K < 2 or nbar <= 1:
                V = np.var(e, ddof=1) * (1 + 1 / N); df = N - 1
            else:
                msb = (n * (means - e.mean()) ** 2).sum() / (K - 1)
                msw = sum(((e[labs == k] - means[k]) ** 2).sum() for k in range(K)) / max(N - K, 1)
                sb2 = max((msb - msw) / nbar, 0.0)
                V = sb2 * (1 + 1 / K) + msw * (1 + 1 / N)
                a_, c_ = (1 + 1 / K) / nbar, (1 + 1 / N) - (1 + 1 / K) / nbar
                df = V ** 2 / ((a_ * msb) ** 2 / (K - 1) + (c_ * msw) ** 2 / max(N - K, 1)) if sb2 > 0 else N - 1
            half = stats.t.ppf(1 - self.alpha / 2, max(df, 1)) * np.sqrt(V)
            centre = yhat + e.mean()
            return centre, centre - half, centre + half
        if self.rule == "gauss":
            df = (self.K_ - 1) if self.unit == "batch" else (self.n_ - 1)
            half = stats.t.ppf(1 - self.alpha / 2, max(df, 1)) * np.sqrt(np.mean(self.residuals_ ** 2))
            return yhat, yhat - half, yhat + half
        centres = np.array([self.loo_[k][1] + self.loo_[k][0] * f for k in self.unit_of_])   # (n, n_new)
        radii = np.abs(self.residuals_)[:, None] * np.ones_like(centres)
        if self.unit == "batch":
            n_k = np.bincount(self.unit_of_)[self.unit_of_]
            L, U = _jackknife_plus(centres, radii, self.alpha, weights=1.0 / ((self.K_ + 1) * n_k))
        else:
            L, U = _jackknife_plus(centres, radii, self.alpha)
        return yhat, L, U

    def decide(self, f_new, threshold, above_is_pass=True):
        """'pass' if the whole interval is on the acceptable side of the threshold, 'fail' if it is entirely on
        the other side, 'refer' (re-measure) otherwise."""
        _, L, U = self.predict(f_new)
        if above_is_pass:
            return np.where(L >= threshold, "pass", np.where(U < threshold, "fail", "refer"))
        return np.where(U <= threshold, "pass", np.where(L > threshold, "fail", "refer"))

def transfer_jackknife(fit, predict, standards, new, alpha=0.1, groups=None):
    """Transfer jackknife+ for any transfer method.

    fit(indices) -> fitted transfer object (uses the reference samples `standards[indices]`);
    predict(obj, which) -> predictions of the deployed predictor for `which` ('new' -> new samples, or an index array
    of reference samples). `standards` must provide the reference values as standards['y'].
    groups: optional batch labels -> leave-one-batch-out (hierarchical) jackknife+."""
    y = np.asarray(standards["y"], float); m = len(y)
    groups = np.arange(m) if groups is None else np.asarray(groups)
    labels = np.unique(groups); K = len(labels); allidx = np.arange(m)
    centres = []; radii = []; n_k = []
    for lab in labels:
        out = np.nonzero(groups == lab)[0]
        obj = fit(np.setdiff1d(allidx, out))
        mu_new = np.asarray(predict(obj, "new"), float)
        r = np.abs(y[out] - np.asarray(predict(obj, out), float))
        for ri in r:
            centres.append(mu_new); radii.append(np.full_like(mu_new, ri)); n_k.append(len(out))
    centres = np.array(centres); radii = np.array(radii)
    w = None if K == m else 1.0 / ((K + 1) * np.array(n_k, float))
    return _jackknife_plus(centres, radii, alpha, weights=w)

def plan(n_standards, n_batches, rho=0.5, alpha=0.1, sims=20000):
    """Expected coverage for samples from new batches when n_standards are taken from n_batches batches."""
    if n_standards % n_batches:
        raise ValueError("n_standards must be a multiple of n_batches")
    n = n_standards // n_batches
    out = expected_coverage(n_batches, n, rho, alpha, sims=sims)
    out["kappa"] = float(kappa(n_batches, n, rho))
    return out
