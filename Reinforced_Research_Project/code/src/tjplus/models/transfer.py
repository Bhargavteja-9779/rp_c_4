"""Calibration transfer / model updating methods and the resulting *deployed predictor*.

A deployed predictor maps raw target-domain spectra to predictions:
    mu(x) = post( f( g(x) ) ),
where g is a spectral standardisation (PDS/DS; identity otherwise), f the source model and post an
affine output correction (SBC; identity otherwise). It also exposes the T^2/Q diagnostics of g(x)
in the source model, from which the difficulty sigma(x) is computed.
"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

RCOND = 1e-2  # relative tolerance of truncated pseudo-inverse (pre-registered)

class PDS:
    """Piecewise direct standardisation mapping `from` spectra onto `to` spectra (with intercept)."""

    def __init__(self, half_window=2, rcond=RCOND):
        self.k, self.rcond = int(half_window), rcond

    def _windows(self, X):
        Xp = np.pad(X, ((0, 0), (self.k, self.k)))           # zero padding at the edges
        return sliding_window_view(Xp, 2 * self.k + 1, axis=1)  # (n, p, w)

    def fit(self, X_from, X_to):
        self.mf_, self.mt_ = X_from.mean(0), X_to.mean(0)
        Wn = self._windows(X_from - self.mf_)                 # (m, p, w)
        Wn = np.transpose(Wn, (1, 0, 2))                      # (p, m, w)
        # truncated pseudo-inverse via eigen-decomposition of the small (w x w) Gram matrices:
        # pinv(A) = V diag(1/s^2) V^T A^T over singular values s > rcond * s_max (identical to SVD pinv)
        WnT = np.transpose(Wn, (0, 2, 1))
        G = WnT @ Wn
        lam, V = np.linalg.eigh(G)
        s = np.sqrt(np.clip(lam, 0, None))
        keep = s > self.rcond * s.max(axis=1, keepdims=True)
        inv = np.where(keep, 1.0 / np.where(keep, lam, 1.0), 0.0)
        Ginv = (V * inv[:, None, :]) @ np.transpose(V, (0, 2, 1))
        Aty = (WnT @ (X_to - self.mt_).T[:, :, None])[:, :, 0]
        self.B_ = (Ginv @ Aty[:, :, None])[:, :, 0]
        return self

    def transform(self, X):
        return (self._windows(X - self.mf_) * self.B_).sum(-1) + self.mt_

class DS:
    """Direct standardisation (full-spectrum, truncated pseudo-inverse)."""

    def __init__(self, rcond=RCOND):
        self.rcond = rcond

    def fit(self, X_from, X_to):
        self.mf_, self.mt_ = X_from.mean(0), X_to.mean(0)
        self.F_ = np.linalg.pinv(X_from - self.mf_, rcond=self.rcond) @ (X_to - self.mt_)
        return self

    def transform(self, X):
        return (X - self.mf_) @ self.F_ + self.mt_

class Deployed:
    def __init__(self, source, spec_map=None, a=0.0, b=1.0):
        self.source, self.spec_map, self.a, self.b = source, spec_map, a, b

    def mapped(self, X):
        return X if self.spec_map is None else self.spec_map.transform(X)

    def predict(self, X):
        return self.a + self.b * self.source.predict(self.mapped(X))

    def diagnostics(self, X):
        return self.source.diagnostics(self.mapped(X))

    def leverage(self, X):
        return self.source.leverage(self.mapped(X))

def fit_deployed(kind, source, Xt_std, y_std=None, Xs_std=None, half_window=2):
    """kind in {'none','sbc','pds','ds'}; Xt_std: standards on target; Xs_std: same standards on source
    instrument (needed for pds/ds); y_std: reference values (needed for sbc)."""
    if kind == "none":
        return Deployed(source)
    if kind == "pds":
        return Deployed(source, PDS(half_window).fit(Xt_std, Xs_std))
    if kind == "ds":
        return Deployed(source, DS().fit(Xt_std, Xs_std))
    if kind == "sbc":
        yh = source.predict(Xt_std)
        if len(y_std) >= 3 and np.var(yh) > 1e-12:
            b, a = np.polyfit(yh, y_std, 1)
        else:
            b, a = 1.0, float(np.mean(y_std - yh))
        return Deployed(source, None, a, b)
    raise ValueError(kind)

def needs_pairs(kind):
    return kind in ("pds", "ds")

def needs_labels(kind):
    return kind == "sbc"
