"""Prediction-interval methods for transferred calibrations.

All methods return (lower, upper) arrays for the target test spectra. Infinite bounds are returned
as +/-inf when the finite-sample quantile index exceeds the calibration size (honest behaviour).

Proposed
--------
TJ+  / TJ+N : transfer jackknife+. For each standard i the *transfer step* is re-fitted on the other
              m-1 standards (mu_{-i}); R_i = |y_i - mu_{-i}(x_i)| / sigma_{-i}(x_i);
              C(x) = [ q^-_a{ mu_{-i}(x) - sigma_{-i}(x) R_i },  q^+_a{ mu_{-i}(x) + sigma_{-i}(x) R_i } ].
              Coverage >= 1 - 2a for exchangeable standards/test samples (Barber et al., 2021, Thm 1,
              applied to the symmetric transfer algorithm with the fixed source model).
"""
import math
import numpy as np
from scipy import stats
from ..models.transfer import fit_deployed, PDS, needs_pairs

# ----------------------------------------------------------------------------- quantile helpers
def conformal_upper_index(n, alpha):
    """1-based rank k = ceil((1-alpha)(n+1)); returns None when k > n (infinite bound)."""
    k = math.ceil((1 - alpha) * (n + 1) - 1e-12)
    return None if k > n else k

def conformal_lower_index(n, alpha):
    k = math.floor(alpha * (n + 1) + 1e-12)
    return None if k < 1 else k

def jackknife_plus(L, U, alpha):
    """L, U: (m, n_test) lower/upper candidate endpoints. Returns jackknife+ bounds."""
    m = L.shape[0]
    ku, kl = conformal_upper_index(m, alpha), conformal_lower_index(m, alpha)
    upper = np.full(L.shape[1], np.inf) if ku is None else np.sort(U, 0)[ku - 1]
    lower = np.full(L.shape[1], -np.inf) if kl is None else np.sort(L, 0)[kl - 1]
    return lower, upper

def split_quantile(scores, alpha):
    k = conformal_upper_index(len(scores), alpha)
    return np.inf if k is None else np.sort(scores)[k - 1]

def weighted_quantile_inf(scores, w_cal, w_test, alpha):
    """Weighted conformal quantile (Tibshirani et al. 2019) with point mass at +inf for the test point.
    scores: (n,), w_cal: (n,), w_test: (n_test,). Returns (n_test,) quantiles."""
    order = np.argsort(scores); s = scores[order]; w = w_cal[order]
    cw = np.cumsum(w)
    tot = cw[-1] + w_test                                   # (n_test,)
    # smallest s_j such that cw_j / tot >= 1 - alpha
    thresh = (1 - alpha) * tot
    idx = np.searchsorted(cw, thresh, side="left")
    q = np.full(len(w_test), np.inf)
    ok = idx < len(s)
    q[ok] = s[idx[ok]]
    return q

# ----------------------------------------------------------------------------- shared LOO computations
class TransferFits:
    """Pre-computes the full-standard fit and all leave-one-standard-out fits of the transfer step,
    with predictions and T^2/Q diagnostics on the test spectra and the held-out standards."""

    def __init__(self, kind, source, Xt_std, y_std, Xs_std, X_test, half_window=2, kfold=5, seed=0):
        self.kind, self.m = kind, len(y_std)
        self.y_std = y_std
        fit = lambda idx: fit_deployed(kind, source, Xt_std[idx], y_std[idx],
                                       None if Xs_std is None else Xs_std[idx], half_window)
        allidx = np.arange(self.m)
        self.full = fit(allidx)
        self.mu_full_test = self.full.predict(X_test)
        self.diag_full_test = self.full.diagnostics(X_test)
        self.mu_full_std = self.full.predict(Xt_std)
        self.diag_full_std = self.full.diagnostics(Xt_std)
        self.lev_full_test = self.full.leverage(X_test)
        # leave-one-out
        self.mu_loo_test = np.empty((self.m, len(X_test)))
        self.t2_loo_test = np.empty_like(self.mu_loo_test); self.q_loo_test = np.empty_like(self.mu_loo_test)
        self.mu_loo_i = np.empty(self.m); self.t2_loo_i = np.empty(self.m); self.q_loo_i = np.empty(self.m)
        self.mu_loo_i_source = None
        for i in range(self.m):
            d = fit(np.delete(allidx, i))
            self.mu_loo_test[i] = d.predict(X_test)
            self.t2_loo_test[i], self.q_loo_test[i] = d.diagnostics(X_test)
            self.mu_loo_i[i] = d.predict(Xt_std[i:i + 1])[0]
            t2, q = d.diagnostics(Xt_std[i:i + 1]); self.t2_loo_i[i], self.q_loo_i[i] = t2[0], q[0]
        # K-fold (CV+) fits
        rng = np.random.default_rng(seed)
        perm = rng.permutation(self.m); K = min(kfold, self.m)
        self.cv_fold_of = np.empty(self.m, int)
        self.mu_cv_test = np.empty((K, len(X_test))); self.t2_cv_test = np.empty_like(self.mu_cv_test)
        self.q_cv_test = np.empty_like(self.mu_cv_test)
        self.mu_cv_i = np.empty(self.m); self.t2_cv_i = np.empty(self.m); self.q_cv_i = np.empty(self.m)
        for k in range(K):
            te = perm[k::K]; tr = np.setdiff1d(allidx, te)
            d = fit(tr)
            self.cv_fold_of[te] = k
            self.mu_cv_test[k] = d.predict(X_test)
            self.t2_cv_test[k], self.q_cv_test[k] = d.diagnostics(X_test)
            self.mu_cv_i[te] = d.predict(Xt_std[te])
            t2, q = d.diagnostics(Xt_std[te]); self.t2_cv_i[te], self.q_cv_i[te] = t2, q
        self._fit = fit
        self.r_loo = np.abs(y_std - self.mu_loo_i)

# ----------------------------------------------------------------------------- proposed methods
def tj_plus(tf, alpha, sigma=None):
    """Transfer jackknife+; sigma=None -> unnormalised TJ+, else TJ+N with difficulty model `sigma`."""
    if sigma is None:
        R = tf.r_loo[:, None]
        L, U = tf.mu_loo_test - R, tf.mu_loo_test + R
    else:
        s_i = sigma(tf.t2_loo_i, tf.q_loo_i)
        R = (tf.r_loo / s_i)[:, None]
        s_test = sigma(tf.t2_loo_test.ravel(), tf.q_loo_test.ravel()).reshape(tf.t2_loo_test.shape)
        L, U = tf.mu_loo_test - s_test * R, tf.mu_loo_test + s_test * R
    return jackknife_plus(L, U, alpha)

def tcv_plus(tf, alpha, sigma=None):
    """K-fold CV+ version of the transfer jackknife+ (ablation / cheaper alternative)."""
    r = np.abs(tf.y_std - tf.mu_cv_i)
    mu = tf.mu_cv_test[tf.cv_fold_of]                                   # (m, n_test)
    if sigma is None:
        R = r[:, None]; s_test = 1.0
    else:
        R = (r / sigma(tf.t2_cv_i, tf.q_cv_i))[:, None]
        t2 = tf.t2_cv_test[tf.cv_fold_of]; q = tf.q_cv_test[tf.cv_fold_of]
        s_test = sigma(t2.ravel(), q.ravel()).reshape(t2.shape)
    return jackknife_plus(mu - s_test * R, mu + s_test * R, alpha)

def tj_naive(tf, alpha, sigma=None):
    """Ablation: jackknife without '+': full-fit centre, LOO residual quantile."""
    if sigma is None:
        q = split_quantile(tf.r_loo, alpha); s = 1.0
    else:
        q = split_quantile(tf.r_loo / sigma(tf.t2_loo_i, tf.q_loo_i), alpha); s = sigma(*tf.diag_full_test)
    return tf.mu_full_test - q * s, tf.mu_full_test + q * s

def tj_insample(tf, alpha, sigma=None):
    """Ablation: residuals of the transfer fitted on all standards (no leave-one-out)."""
    r = np.abs(tf.y_std - tf.mu_full_std)
    if sigma is None:
        q = split_quantile(r, alpha); s = 1.0
    else:
        q = split_quantile(r / sigma(*tf.diag_full_std), alpha); s = sigma(*tf.diag_full_test)
    return tf.mu_full_test - q * s, tf.mu_full_test + q * s

# ----------------------------------------------------------------------------- baselines
def scp_target_split(tf, X_test, Xt_std, alpha, sigma=None, seed=0):
    """Valid baseline: half of the standards fit the transfer, the other half calibrate split conformal."""
    m = tf.m
    h = m // 2
    perm = np.random.default_rng(seed).permutation(m)
    a, b = perm[:h], perm[h:]
    d = tf._fit(a)
    r = np.abs(tf.y_std[b] - d.predict(Xt_std[b]))
    mu = d.predict(X_test)
    if sigma is None:
        q = split_quantile(r, alpha); s = 1.0
    else:
        q = split_quantile(r / sigma(*d.diagnostics(Xt_std[b])), alpha); s = sigma(*d.diagnostics(X_test))
    return mu - q * s, mu + q * s

def gauss_loo(tf, alpha):
    """Common practice: yhat +/- t * RMSE of leave-one-standard-out residuals."""
    rmse = np.sqrt(np.mean(tf.r_loo ** 2))
    t = stats.t.ppf(1 - alpha / 2, max(tf.m - 1, 1))
    return tf.mu_full_test - t * rmse, tf.mu_full_test + t * rmse

def astm_pi(tf, source, alpha):
    """Classical parametric PLS prediction interval (ASTM E1655-style): t * SEC * sqrt(1 + h)."""
    n, A = source.model.n_train_, source.A
    t = stats.t.ppf(1 - alpha / 2, max(n - A - 1, 1))
    half = t * source.sec * np.sqrt(1 + tf.lev_full_test)
    return tf.mu_full_test - half, tf.mu_full_test + half

def scp_source(tf, e_pool, alpha):
    """Split conformal with source residual pool (assumes no shift)."""
    q = split_quantile(np.abs(e_pool), alpha)
    return tf.mu_full_test - q, tf.mu_full_test + q

def wcp_source(tf, source, e_pool, Xs_pool, X_target_unlab, X_test, alpha, C=1.0):
    """Weighted conformal under covariate shift (Tibshirani et al., 2019); likelihood ratio from a
    logistic domain classifier on source-model PLS scores (target spectra after transfer)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    def scores(Xraw, mapped):
        Z = source.transform(tf.full.mapped(Xraw) if mapped else Xraw)
        return (Z - source.model.x_mean_) @ source.model.R_[:, :source.A]
    Ss, St, Sx = scores(Xs_pool, False), scores(X_target_unlab, True), scores(X_test, True)
    Z = np.vstack([Ss, St]); lab = np.r_[np.zeros(len(Ss)), np.ones(len(St))]
    sc = StandardScaler().fit(Z)
    clf = LogisticRegression(C=C, max_iter=2000).fit(sc.transform(Z), lab)
    def lr(S):
        p = np.clip(clf.predict_proba(sc.transform(S))[:, 1], 1e-6, 1 - 1e-6)
        return p / (1 - p) * (len(Ss) / len(St))
    q = weighted_quantile_inf(np.abs(e_pool), lr(Ss), lr(Sx), alpha)
    return tf.mu_full_test - q, tf.mu_full_test + q

def transport(tf, source, e_pool, Xs_pool, Xt_std, Xs_std, alpha, half_window=2):
    """Regression analogue of transported conformal calibration (Doula, 2026): source calibration
    spectra are mapped into the target space (master->slave PDS fitted on the paired standards),
    passed through the deployed pipeline; residual = e_j + [f(x_j) - mu(h(x_j))]."""
    h = PDS(half_window).fit(Xs_std, Xt_std)
    shift = source.predict(Xs_pool) - tf.full.predict(h.transform(Xs_pool))
    q = split_quantile(np.abs(e_pool + shift), alpha)
    return tf.mu_full_test - q, tf.mu_full_test + q

def label_free_conv(tf, source, e_pool, Xt_std, Xs_std, alpha):
    """Exploratory label-free variant: target error ~ e_source - d, d = LOO transfer discrepancy on
    paired unlabelled standards. Empirical quantiles of all pairwise differences (no guarantee)."""
    d = tf.mu_loo_i - source.predict(Xs_std)
    diffs = (e_pool[:, None] - d[None, :]).ravel()
    lo, hi = np.quantile(diffs, [alpha / 2, 1 - alpha / 2])
    return tf.mu_full_test + lo, tf.mu_full_test + hi
