"""Source-only model selection: preprocessing choice + number of LVs by 10-fold CV (1-SE rule),
out-of-fold residuals and diagnostics (used by the difficulty model and source-based baselines).
No target-domain data are touched here."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import nnls
from ..preprocessing.spectra import preprocess
from .pls import PLS1

@dataclass
class SourceModel:
    prep: str
    model: PLS1
    A: int
    oof_resid: np.ndarray      # out-of-fold residuals on source training (y - yhat)
    oof_t2: np.ndarray
    oof_q: np.ndarray
    sec: float                 # standard error of calibration
    cv_table: dict

    def transform(self, X):
        return preprocess(self.prep, X)

    def predict(self, X_raw):
        return self.model.predict(self.transform(X_raw), self.A)

    def diagnostics(self, X_raw):
        return self.model.diagnostics(self.transform(X_raw), self.A)

    def leverage(self, X_raw):
        return self.model.leverage(self.transform(X_raw), self.A)

def _kfold(n, k, rng):
    idx = rng.permutation(n)
    return [idx[i::k] for i in range(k)]

def fit_source_model(X, y, max_lv=15, preps=("none", "snv", "sg1", "sg2"), k=10, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y)
    folds = _kfold(n, k, rng)
    best = None; table = {}
    for prep in preps:
        Xp = preprocess(prep, X)
        A = min(max_lv, n - n // k - 2)
        pred = np.zeros((n, A)); t2s = {}; qs = {}
        fold_mse = np.zeros((k, A))
        for fi, te in enumerate(folds):
            tr = np.setdiff1d(np.arange(n), te)
            m = PLS1(A).fit(Xp[tr], y[tr])
            P = m.predict_all(Xp[te])
            if P.shape[1] < A:  # pad if fewer comps were possible
                P = np.hstack([P, np.repeat(P[:, -1:], A - P.shape[1], 1)])
            pred[te] = P
            fold_mse[fi] = ((P - y[te, None]) ** 2).mean(0)
            t2s[fi] = (te, m, tr)
        mse = ((pred - y[:, None]) ** 2).mean(0)
        se = fold_mse.std(0, ddof=1) / np.sqrt(k)
        amin = int(np.argmin(mse))
        a_1se = int(np.nonzero(mse <= mse[amin] + se[amin])[0][0]) + 1
        table[prep] = dict(rmsecv=np.sqrt(mse).tolist(), a_min=amin + 1, a_1se=a_1se)
        if best is None or mse[amin] < best[0]:
            best = (mse[amin], prep, a_1se, pred, t2s, Xp)
    _, prep, A, pred, folds_info, Xp = best
    oof_t2 = np.zeros(n); oof_q = np.zeros(n)
    for te, m, tr in folds_info.values():
        a = min(A, m.A_)
        t2, q = m.diagnostics(Xp[te], a); oof_t2[te] = t2; oof_q[te] = q
    oof_resid = y - pred[:, A - 1]
    model = PLS1(A).fit(Xp, y); model.n_use = A
    fit_res = y - model.predict(Xp, A)
    sec = float(np.sqrt((fit_res ** 2).sum() / max(n - A - 1, 1)))
    return SourceModel(prep, model, A, oof_resid, oof_t2, oof_q, sec, table)

class DifficultyModel:
    """sigma(x) = max(eps, a + b*sqrt(T2) + c*sqrt(Q)), fitted by NNLS to |OOF residuals| on source data.
    `features` selects ('t2','q') or a subset for the ablation."""

    def __init__(self, features=("t2", "q")):
        self.features = tuple(features)

    def _design(self, t2, q):
        cols = [np.ones_like(t2)]
        if "t2" in self.features: cols.append(np.sqrt(t2))
        if "q" in self.features: cols.append(np.sqrt(q))
        return np.column_stack(cols)

    def fit(self, t2, q, abs_resid):
        # scale features for numerical stability
        D = self._design(t2, q)
        self.scale_ = D.max(0) + 1e-300
        coef, _ = nnls(D / self.scale_, abs_resid)
        self.coef_ = coef / self.scale_
        self.eps_ = max(0.05 * float(np.median(abs_resid)), 1e-12)
        return self

    def __call__(self, t2, q):
        return np.maximum(self._design(t2, q) @ self.coef_, self.eps_)
