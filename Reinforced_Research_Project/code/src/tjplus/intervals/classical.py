"""Additional classical competitors (reinforcement experiment E11).

ASTM-T : ASTM E1655-type interval re-estimated on the target standards:
         mu(x) +/- t_{m-1} * RMSE_LOO * sqrt(1 + h(x)), h = source-model leverage of the transferred spectrum.
OLS-PI : for slope/bias correction only. SBC is an ordinary least-squares regression of y on the source
         prediction f, so the textbook regression prediction interval applies:
         yhat +/- t_{m-2} * s * sqrt(1 + 1/m + (f - fbar)^2 / S_ff). Exact under Gaussian homoscedastic errors.
Boot-T : bootstrap prediction interval (pairs bootstrap of the standards for the transfer variability,
         plus resampled centred in-sample residuals of the full transfer fit, scaled by sqrt(m/(m-p)) with
         p = 2 for SBC and p = 0 otherwise). Prediction errors delta* = mu*_b(x) - mu(x) - e_j over all
         b, j; interval [mu(x) - q_{1-a/2}(delta*), mu(x) - q_{a/2}(delta*)] (Davison & Hinkley 1997, Alg. 6.4,
         pairs version).
"""
import numpy as np
from scipy import stats

def astm_target(tf, alpha):
    rmse = np.sqrt(np.mean(tf.r_loo ** 2))
    t = stats.t.ppf(1 - alpha / 2, max(tf.m - 1, 1))
    half = t * rmse * np.sqrt(1 + tf.lev_full_test)
    return tf.mu_full_test - half, tf.mu_full_test + half

def ols_pi_sbc(tf, source, Xt_std, X_test, alpha):
    f_i = source.predict(Xt_std); f_x = source.predict(X_test)
    m = len(f_i)
    b, a = np.polyfit(f_i, tf.y_std, 1)
    res = tf.y_std - (a + b * f_i)
    s = np.sqrt((res ** 2).sum() / max(m - 2, 1))
    sff = ((f_i - f_i.mean()) ** 2).sum()
    t = stats.t.ppf(1 - alpha / 2, max(m - 2, 1))
    half = t * s * np.sqrt(1 + 1 / m + (f_x - f_i.mean()) ** 2 / max(sff, 1e-300))
    yhat = a + b * f_x
    return yhat - half, yhat + half

class BootTransfer:
    """Pre-computes B pairs-bootstrap refits of the transfer step (shared across alpha levels)."""

    def __init__(self, tf, X_test, Xt_std, kind, B=200, seed=0):
        rng = np.random.default_rng(seed)
        m = tf.m
        self.delta = np.empty((B, len(X_test)))
        for b in range(B):
            while True:
                idx = rng.integers(0, m, m)
                if len(np.unique(idx)) >= 3:
                    break
            d = tf._fit(idx)
            self.delta[b] = d.predict(X_test) - tf.mu_full_test
        p = 2 if kind == "sbc" else 0
        e = tf.y_std - tf.mu_full_std
        self.e = (e - e.mean()) * np.sqrt(m / max(m - p, 1))
        self.mu = tf.mu_full_test

    def interval(self, alpha, chunk=64):
        lo = np.empty(len(self.mu)); hi = np.empty(len(self.mu))
        for s in range(0, len(self.mu), chunk):
            D = (self.delta[:, s:s + chunk, None] - self.e[None, None, :])   # (B, c, m)
            D = np.moveaxis(D, 1, 0).reshape(D.shape[1], -1)
            q_lo, q_hi = np.quantile(D, [alpha / 2, 1 - alpha / 2], axis=1)
            lo[s:s + chunk] = self.mu[s:s + chunk] - q_hi
            hi[s:s + chunk] = self.mu[s:s + chunk] - q_lo
        return lo, hi
