"""Planning transfer standards: expected coverage of prediction intervals for samples from NEW batches.

Model (one-way random effects for the errors of the source model on the target domain, after scaling to unit
total variance):  e_kj = b_k + w_kj,  b_k ~ N(0, rho),  w_kj ~ N(0, 1 - rho),  rho = intra-batch correlation.
A bias (intercept) correction is fitted on the standards, as in slope/bias correction with a fixed slope.
K batches x n standards per batch are drawn; the routine sample comes from a new batch, so its error is N(0, 1)
and independent of the standards. For an interval [L, U] on the error scale, its coverage is Phi(U) - Phi(L);
the expected coverage is the Monte Carlo mean over draws of the standards.

Interval rules (as in the paper):
  gauss_loo : centre = mean of all standards, +/- t_{N-1} * RMSE of leave-one-STANDARD-out residuals
  tj_plus   : jackknife+ with leave-one-standard-out centres (sample-level TJ+)
  tj_b      : hierarchical jackknife+ with leave-one-BATCH-out centres, weights 1/((K+1) n)  (TJ+B)
  gauss_lgo : centre = mean, +/- t_{K-1} * RMS of leave-one-batch-out residuals

Closed-form intuition (Gaussian rules): the leave-one-standard-out scale estimates
  E[r^2] = N/(N-1) (1-rho) + (N/(N-1))^2 (1 - 1/K) rho,
whereas a new-batch error (relative to the fitted bias) has variance
  V    = (1 + 1/N)(1 - rho) + (1 + 1/K) rho.
The ratio kappa = E[r^2]/V < 1 whenever n > 1 and rho > 0; the interval is then too narrow by the factor sqrt(kappa).
"""
import numpy as np
from scipy import stats

def kappa(K, n, rho):
    N = K * n
    er2 = N / (N - 1) * (1 - rho) + (N / (N - 1)) ** 2 * (1 - 1 / K) * rho
    v = (1 + 1 / N) * (1 - rho) + (1 + 1 / K) * rho
    return er2 / v

def _jk_bounds(centres, radii, alpha, weights=None, K=None):
    """jackknife+ bounds over rows (sims x m); weights None -> equal weights with mass 1/(m+1) at infinity."""
    up = centres + radii; lo = centres - radii
    if weights is None:
        m = centres.shape[1]
        ku = int(np.ceil((1 - alpha) * (m + 1) - 1e-12)); kl = int(np.floor(alpha * (m + 1) + 1e-12))
        U = np.sort(up, 1)[:, ku - 1] if ku <= m else np.full(len(up), np.inf)
        L = np.sort(lo, 1)[:, kl - 1] if kl >= 1 else np.full(len(lo), -np.inf)
        return L, U
    # equal batch sizes: weight per member 1/((K+1) n); cumulative weight of the j-th smallest = j/((K+1) n)
    m = centres.shape[1]; n = m // K
    ku = int(np.ceil((1 - alpha) * (K + 1) * n - 1e-9))
    kl = m + 1 - ku
    U = np.sort(up, 1)[:, ku - 1] if ku <= m else np.full(len(up), np.inf)
    L = np.sort(lo, 1)[:, kl - 1] if kl >= 1 else np.full(len(lo), -np.inf)
    return L, U

def expected_coverage(K, n, rho, alpha=0.1, rules=("gauss_loo", "tj_plus", "tj_b", "gauss_lgo"), sims=20000, seed=0):
    """Expected coverage (and share of unbounded intervals) of each rule for a sample from a new batch."""
    rng = np.random.default_rng(seed)
    N = K * n
    b = rng.normal(0, np.sqrt(rho), (sims, K))
    e = np.repeat(b, n, axis=1) + rng.normal(0, np.sqrt(1 - rho), (sims, N))
    tot = e.sum(1, keepdims=True)
    mean = tot / N
    loo_c = (tot - e) / (N - 1)                       # leave-one-standard-out centre
    r = e - loo_c
    g = e.reshape(sims, K, n)
    gsum = g.sum(2)                                    # (sims, K)
    lbo_c = np.repeat((tot - gsum) / (N - n), n, axis=1) if K > 1 else np.full_like(e, np.nan)
    rb = e - lbo_c
    out = {}
    for rule in rules:
        if rule == "gauss_loo":
            half = stats.t.ppf(1 - alpha / 2, N - 1) * np.sqrt((r ** 2).mean(1))
            L, U = mean[:, 0] - half, mean[:, 0] + half
        elif rule == "tj_plus":
            L, U = _jk_bounds(loo_c, np.abs(r), alpha)
        elif rule == "tj_b":
            if K < 2:
                L, U = np.full(sims, -np.inf), np.full(sims, np.inf)
            else:
                L, U = _jk_bounds(lbo_c, np.abs(rb), alpha, weights=True, K=K)
        elif rule == "gauss_lgo":
            half = stats.t.ppf(1 - alpha / 2, max(K - 1, 1)) * np.sqrt((rb ** 2).mean(1)) if K > 1 else np.full(sims, np.inf)
            L, U = mean[:, 0] - half, mean[:, 0] + half
        else:
            raise ValueError(rule)
        cov = stats.norm.cdf(U) - stats.norm.cdf(L)
        out[rule] = dict(coverage=float(np.mean(cov)), frac_inf=float(np.mean(~np.isfinite(U))),
                         p05=float(np.quantile(cov, 0.05)))
    return out

def min_batches(n_total, rho, alpha=0.1, target=None, rule="tj_plus", max_k=None):
    """Smallest number of batches K (with n_total/K standards each, K dividing n_total) whose expected
    coverage for new batches reaches `target` (default: nominal minus 0.01)."""
    target = 1 - alpha - 0.01 if target is None else target
    for K in range(2, (max_k or n_total) + 1):
        if n_total % K:
            continue
        c = expected_coverage(K, n_total // K, rho, alpha, rules=(rule,), sims=8000)[rule]
        if c["frac_inf"] < 0.5 and c["coverage"] >= target:
            return K
    return None
