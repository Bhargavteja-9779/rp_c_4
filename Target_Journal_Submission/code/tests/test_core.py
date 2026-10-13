"""Unit tests for the statistical core. Run: python -m pytest tests -q"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from tjplus.models.pls import PLS1
from tjplus.models.transfer import PDS, DS, fit_deployed
from tjplus.intervals.methods import (conformal_upper_index, conformal_lower_index, jackknife_plus,
                                      split_quantile, weighted_quantile_inf, TransferFits, tj_plus)
from tjplus.evaluation.metrics import interval_metrics

def test_pls_matches_sklearn():
    from sklearn.cross_decomposition import PLSRegression
    rng = np.random.default_rng(0)
    X = rng.normal(size=(50, 30)); y = X[:, :3] @ [1.0, -2.0, 0.5] + rng.normal(0, .1, 50)
    a = PLS1(5).fit(X, y).predict(X[:10], 5)
    b = PLSRegression(5, scale=False).fit(X, y).predict(X[:10]).ravel()
    assert np.allclose(a, b, atol=1e-10)

def test_quantile_indices():
    assert conformal_upper_index(9, 0.1) == 9      # ceil(0.9*10)=9
    assert conformal_upper_index(8, 0.1) is None   # ceil(0.9*9)=9 > 8 -> infinite
    assert conformal_lower_index(9, 0.1) == 1
    assert conformal_lower_index(8, 0.1) is None
    assert np.isinf(split_quantile(np.arange(5.0), 0.1))

def test_pds_recovers_linear_instrument_response():
    rng = np.random.default_rng(1)
    Xm = rng.normal(size=(25, 60)).cumsum(1)
    Xs = 0.9 * Xm + 0.2                             # slave = affine distortion of master
    pds = PDS(2).fit(Xs, Xm)
    Xnew = rng.normal(size=(5, 60)).cumsum(1)
    assert np.allclose(pds.transform(0.9 * Xnew + 0.2), Xnew, atol=1e-6)
    ds = DS().fit(Xs, Xm)
    assert ds.transform(Xs).shape == Xm.shape

def test_weighted_quantile_reduces_to_split_with_equal_weights():
    s = np.arange(1.0, 20.0)
    q = weighted_quantile_inf(s, np.ones_like(s), np.ones(3), 0.1)
    assert np.allclose(q, split_quantile(s, 0.1))

class _LinSource:
    """Minimal source model y = x @ beta used for the coverage simulation."""
    def __init__(self, beta): self.beta = beta
    def predict(self, X): return X @ self.beta
    def diagnostics(self, X): return np.ones(len(X)), np.ones(len(X))
    def leverage(self, X): return np.zeros(len(X))

def test_tj_plus_coverage_simulation():
    """Exchangeable target standards/test points, SBC transfer refitted in every LOO fold:
    empirical coverage must be >= 1 - 2*alpha (theory) and close to 1 - alpha in practice."""
    rng = np.random.default_rng(2)
    beta = rng.normal(size=5); src = _LinSource(beta)
    alpha, covs = 0.1, []
    for r in range(300):
        X = rng.normal(size=(60, 5)); y = 1.5 * X @ beta + 0.7 + rng.standard_t(3, 60)  # shifted target
        tf = TransferFits("sbc", src, X[:20], y[:20], None, X[20:])
        lo, hi = tj_plus(tf, alpha, None)
        covs.append(interval_metrics(lo, hi, y[20:], alpha)["coverage"])
    c = np.mean(covs)
    assert c >= 1 - 2 * alpha
    assert c >= 1 - alpha - 0.03

def test_insample_undercovers_relative_to_loo():
    """Sanity: in-sample residuals of a refitted transfer are optimistic."""
    rng = np.random.default_rng(3)
    beta = rng.normal(size=5); src = _LinSource(beta)
    from tjplus.intervals.methods import tj_insample
    c_loo, c_in = [], []
    for r in range(300):
        X = rng.normal(size=(40, 5)); y = 1.3 * X @ beta - 0.4 + rng.normal(0, 1, 40)
        tf = TransferFits("sbc", src, X[:8], y[:8], None, X[8:])
        c_loo.append(interval_metrics(*tj_plus(tf, 0.2, None), y[8:], 0.2)["coverage"])
        c_in.append(interval_metrics(*tj_insample(tf, 0.2, None), y[8:], 0.2)["coverage"])
    assert np.mean(c_loo) > np.mean(c_in)
