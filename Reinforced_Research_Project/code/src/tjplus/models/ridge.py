"""Ridge-regression source model (model-class generalisation check). Preprocessing is chosen with the
same source-only PLS procedure; T^2/Q diagnostics for the difficulty model come from that PLS model."""
import numpy as np
from sklearn.linear_model import Ridge
from .source_model import fit_source_model, _kfold

class RidgeSource:
    def __init__(self, pls_source, ridge, oof_resid, sec):
        self.prep, self.model, self.A = pls_source.prep, pls_source.model, pls_source.A
        self.ridge, self.oof_resid, self.sec = ridge, oof_resid, sec
        self.oof_t2, self.oof_q = pls_source.oof_t2, pls_source.oof_q
        self._pls = pls_source

    def transform(self, X): return self._pls.transform(X)
    def predict(self, X): return self.ridge.predict(self.transform(X))
    def diagnostics(self, X): return self._pls.diagnostics(X)
    def leverage(self, X): return self._pls.leverage(X)

def fit_source_ridge(X, y, max_lv=15, seed=0, k=10):
    pls = fit_source_model(X, y, max_lv=max_lv, seed=seed)
    Xp = pls.transform(X)
    scale = np.trace(np.cov(Xp, rowvar=False))
    alphas = scale * np.logspace(-6, 1, 15)
    rng = np.random.default_rng(seed); folds = _kfold(len(y), k, rng)
    cv = np.zeros((len(alphas), len(y)))
    for te in folds:
        tr = np.setdiff1d(np.arange(len(y)), te)
        for ai, a in enumerate(alphas):
            cv[ai, te] = Ridge(alpha=a).fit(Xp[tr], y[tr]).predict(Xp[te])
    best = int(np.argmin(((cv - y) ** 2).mean(1)))
    ridge = Ridge(alpha=alphas[best]).fit(Xp, y)
    res = y - ridge.predict(Xp)
    sec = float(np.sqrt((res ** 2).sum() / max(len(y) - pls.A - 1, 1)))
    return RidgeSource(pls, ridge, y - cv[best], sec)
