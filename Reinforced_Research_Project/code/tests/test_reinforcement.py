"""Tests of the reinforcement code: batch-level jackknife+ (Proposition 2), classical competitors and the
batch design sampler (leakage checks). Run: python -m pytest tests -q"""
import os, sys
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from tjplus.intervals.methods import TransferFits, tj_plus
from tjplus.intervals import group as G
from tjplus.intervals import classical as CL
from tjplus.experiments.batch import draw_design, _icc

class _LinSource:
    def __init__(self, beta): self.beta = beta
    def predict(self, X): return X @ self.beta
    def diagnostics(self, X): return np.ones(len(X)), np.ones(len(X))
    def leverage(self, X): return np.zeros(len(X))

def _batches(rng, beta, n_batches, n_per, sd_batch=1.0, sd_within=0.5):
    """Target data with a random additive bias per batch (errors correlated within batch)."""
    X = rng.normal(size=(n_batches * n_per, len(beta)))
    g = np.repeat(np.arange(n_batches), n_per)
    y = 1.2 * X @ beta + 0.5 + rng.normal(0, sd_batch, n_batches)[g] + rng.normal(0, sd_within, len(g))
    return X, y, g

def _cover(lo, hi, y):
    return float(np.mean((y >= lo) & (y <= hi)))

def test_batch_effects_break_sample_level_tj_but_not_group_tj():
    """Standards from K=2 batches (10 each), test samples from new batches: sample-level TJ+ under-covers
    strongly; with K=12 batches (1 standard each) ordinary TJ+ is valid, and TJ+G is valid for K=12 x 2."""
    rng = np.random.default_rng(5)
    beta = rng.normal(size=4); src = _LinSource(beta); alpha = 0.1
    cov_few, cov_one, cov_g, cov_h, cov_a = [], [], [], [], []
    for r in range(400):
        X, y, g = _batches(rng, beta, 40, 10)
        # (a) 2 batches x 10 standards
        std = np.nonzero(g < 2)[0]; te = np.nonzero(g >= 14)[0]
        tf = TransferFits("sbc", src, X[std], y[std], None, X[te])
        cov_few.append(_cover(*tj_plus(tf, alpha), y[te]))
        # (b) 12 batches x 1 standard: ordinary TJ+ (each standard is its own batch)
        std = np.array([10 * b for b in range(2, 14)])
        tf = TransferFits("sbc", src, X[std], y[std], None, X[te])
        cov_one.append(_cover(*tj_plus(tf, alpha), y[te]))
        # (c) TJ+G with 12 batches x 2 standards
        std = np.array([10 * b + j for b in range(2, 14) for j in range(2)])
        tf = TransferFits("sbc", src, X[std], y[std], None, X[te])
        gt = G.GroupTransferFits(tf, g[std], X[std], X[te])
        cov_g.append(_cover(*G.tj_plus_group(gt, alpha), y[te]))
        cov_h.append(_cover(*G.tj_plus_hier(gt, alpha), y[te]))
        cov_a.append(_cover(*G.anova_pi(gt, alpha), y[te]))
    assert np.mean(cov_few) < 0.75                 # failure of sample-level exchangeability
    assert np.mean(cov_one) >= 1 - 2 * alpha and np.mean(cov_one) > 0.86
    assert np.mean(cov_g) >= 1 - 2 * alpha and np.mean(cov_g) > 0.86
    assert np.mean(cov_h) >= 1 - 2 * alpha and np.mean(cov_h) > 0.86
    assert abs(np.mean(cov_a) - 0.9) < 0.04          # Gaussian random-effects model is correct here

def test_group_jackknife_reduces_to_tj_plus_with_singleton_batches():
    rng = np.random.default_rng(1)
    beta = rng.normal(size=3); src = _LinSource(beta)
    X = rng.normal(size=(40, 3)); y = X @ beta + rng.normal(0, 1, 40)
    tf = TransferFits("sbc", src, X[:15], y[:15], None, X[15:])
    gt = G.GroupTransferFits(tf, np.arange(15), X[:15], X[15:])
    a = tj_plus(tf, 0.1); b = G.tj_plus_group(gt, 0.1); h = G.tj_plus_hier(gt, 0.1)
    assert np.allclose(a[0], b[0]) and np.allclose(a[1], b[1])
    assert np.allclose(a[0], h[0]) and np.allclose(a[1], h[1])

def test_group_bounds_infinite_with_few_batches():
    rng = np.random.default_rng(2)
    beta = rng.normal(size=3); src = _LinSource(beta)
    X = rng.normal(size=(40, 3)); y = X @ beta + rng.normal(0, 1, 40)
    tf = TransferFits("sbc", src, X[:20], y[:20], None, X[20:])
    gt = G.GroupTransferFits(tf, np.repeat([0, 1, 2, 3, 4], 4), X[:20], X[20:])
    lo, hi = G.tj_plus_group(gt, 0.1)               # K=5 < 9 -> unbounded at alpha = 0.1
    assert np.all(np.isinf(hi)) and np.all(np.isinf(lo))

def test_ols_pi_matches_textbook_formula_and_covers():
    rng = np.random.default_rng(3)
    beta = rng.normal(size=3); src = _LinSource(beta)
    covs = []
    for r in range(500):
        X = rng.normal(size=(60, 3)); y = 0.8 * X @ beta + 1.0 + rng.normal(0, 0.7, 60)
        tf = TransferFits("sbc", src, X[:10], y[:10], None, X[10:])
        lo, hi = CL.ols_pi_sbc(tf, src, X[:10], X[10:], 0.1)
        covs.append(_cover(lo, hi, y[10:]))
    assert abs(np.mean(covs) - 0.9) < 0.015          # exact under Gaussian homoscedastic errors

def test_boot_transfer_shapes_and_order():
    rng = np.random.default_rng(4)
    beta = rng.normal(size=3); src = _LinSource(beta)
    X = rng.normal(size=(50, 3)); y = X @ beta + rng.normal(0, 1, 50)
    tf = TransferFits("sbc", src, X[:15], y[:15], None, X[15:])
    bt = CL.BootTransfer(tf, X[15:], X[:15], "sbc", B=50, seed=0)
    lo, hi = bt.interval(0.1)
    assert lo.shape == (35,) and np.all(hi > lo)
    lo2, hi2 = bt.interval(0.05)
    assert np.all(hi2 >= hi - 1e-12) and np.all(lo2 <= lo + 1e-12)

def test_draw_design_is_disjoint_and_respects_batches():
    rng = np.random.default_rng(0)
    pop = np.repeat(np.array([f"p{i}" for i in range(12)]), 30)
    date = np.repeat(np.arange(12), 30).astype("datetime64[D]")
    pool = np.arange(len(pop))
    for design in [("random", 2, 10), ("random", 10, 1), ("chrono", 3, 4)]:
        std, grp, new, same = draw_design(pool, pop, date, design, rng)
        assert len(std) == design[1] * design[2] and len(np.unique(std)) == len(std)
        assert not set(std) & set(new) and not set(std) & set(same) and not set(new) & set(same)
        assert not set(pop[new]) & set(pop[std])       # new-batch test set contains no standard batch
        assert set(pop[same]) <= set(pop[std])
        assert len(np.unique(grp)) == design[1]
        if design[0] == "chrono":
            assert date[new].min() > date[std].max()

def test_icc_estimator():
    rng = np.random.default_rng(6)
    g = np.repeat(np.arange(200), 10)
    e = rng.normal(0, 1, 200)[g] + rng.normal(0, 1, len(g))     # true ICC = 0.5
    assert abs(_icc(e, g) - 0.5) < 0.08
