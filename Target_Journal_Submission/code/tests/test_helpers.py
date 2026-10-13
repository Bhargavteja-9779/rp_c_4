import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from tjplus.evaluation.metrics import interval_metrics, tertile_coverage
from tjplus.experiments.datasets import kennard_stone
from tjplus.intervals.methods import jackknife_plus

def test_interval_metrics_winkler():
    y = np.array([0.0, 1.0, 5.0]); lo = np.array([-1.0, -1.0, -1.0]); hi = np.array([1.0, 1.0, 1.0])
    m = interval_metrics(lo, hi, y, 0.1)
    assert np.isclose(m["coverage"], 2 / 3)
    assert np.isclose(m["interval_score"], 2 + (2 / 0.1) * 4 / 3)   # width 2 + penalty 20*4 averaged over 3
    assert m["miss_hi"] > 0 and m["miss_lo"] == 0

def test_infinite_intervals_flagged():
    y = np.zeros(4)
    m = interval_metrics(np.full(4, -np.inf), np.full(4, np.inf), y, 0.1)
    assert m["frac_inf"] == 1 and np.isinf(m["interval_score"]) and m["coverage"] == 1

def test_jackknife_plus_infinite_when_m_too_small():
    L = np.zeros((5, 3)); U = np.ones((5, 3))
    lo, hi = jackknife_plus(L, U, 0.1)       # ceil(0.9*6)=6 > 5 -> unbounded
    assert np.all(np.isinf(hi)) and np.all(np.isinf(lo))

def test_kennard_stone_picks_extremes_first():
    X = np.array([[0.0], [1.0], [10.0], [5.0], [4.9]])
    sel = kennard_stone(X, 3)
    assert set(sel[:2]) == {0, 2} and sel[2] in (3, 4)

def test_tertile_coverage_keys():
    y = np.arange(9.0); r = tertile_coverage(y - 1, y + 1, y, y, "c")
    assert set(r) == {"c1", "c2", "c3"} and all(v == 1 for v in r.values())
