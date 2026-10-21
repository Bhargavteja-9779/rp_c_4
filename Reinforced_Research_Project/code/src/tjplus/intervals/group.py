"""Batch-level (group) transfer jackknife+ for standards that come in batches.

Setting. The target population consists of batches (production lots, harvest consignments). The m
standards come from K batches (n_g standards each); a routine sample comes from a batch that may be
*new*. Sample-level exchangeability between standards and a sample from a new batch then fails,
because errors within a batch are correlated.

TJ+G (proposed, Proposition 2). The unit of exchangeability is the batch. For each batch k, the
transfer is re-fitted without all standards of batch k (mu_{-k}, sigma_{-k}); the batch score is the
largest normalised residual of its members,
    S_k = max_{i in batch k} |y_i - mu_{-k}(x_i)| / sigma_{-k}(x_i),
and the interval is the jackknife+ over the K batches,
    C(x) = [ q^-_a{ mu_{-k}(x) - sigma_{-k}(x) S_k },  q^+_a{ mu_{-k}(x) + sigma_{-k}(x) S_k } ]
with ranks ceil((1-a)(K+1)) and floor(a(K+1)). If the K+1 batches are exchangeable and the n_g
members of each batch (standards, or hypothetical draws for the new batch) are drawn at random
within the batch, coverage for a sample from the new batch is >= 1 - 2a (max-score argument: the
test sample's score cannot exceed its batch's max score). With n_g = 1 this is ordinary TJ+.

Comparators implemented here (no guarantee for new batches):
  LGO-CV+N : CV+ with the batches as folds, pooled member-level scores (what a practitioner would
             naturally do; exchangeability at sample level is not satisfied).
  Gauss-LGO: mu(x) +/- t_{K-1} * RMSE of leave-batch-out residuals.
"""
import numpy as np
from scipy import stats
from .methods import jackknife_plus

class GroupTransferFits:
    def __init__(self, tf, groups, Xt_std, X_test):
        """tf: methods.TransferFits for the same standards (provides the fit function and full fit);
        groups: (m,) batch labels of the standards."""
        self.tf = tf
        self.groups = np.asarray(groups)
        self.labels = np.unique(self.groups)
        K, m = len(self.labels), len(self.groups)
        self.K = K
        self.mu_test = np.empty((K, len(X_test)))
        self.t2_test = np.empty_like(self.mu_test); self.q_test = np.empty_like(self.mu_test)
        self.mu_i = np.empty(m); self.t2_i = np.empty(m); self.q_i = np.empty(m)
        self.g_index = np.empty(m, int)
        allidx = np.arange(m)
        for k, lab in enumerate(self.labels):
            out = np.nonzero(self.groups == lab)[0]
            d = tf._fit(np.setdiff1d(allidx, out))
            self.mu_test[k] = d.predict(X_test)
            self.t2_test[k], self.q_test[k] = d.diagnostics(X_test)
            self.mu_i[out] = d.predict(Xt_std[out])
            t2, q = d.diagnostics(Xt_std[out]); self.t2_i[out], self.q_i[out] = t2, q
            self.g_index[out] = k
        self.r = np.abs(tf.y_std - self.mu_i)

    def _scales(self, sigma):
        if sigma is None:
            return np.ones_like(self.r), np.ones_like(self.mu_test)
        s_i = sigma(self.t2_i, self.q_i)
        s_t = sigma(self.t2_test.ravel(), self.q_test.ravel()).reshape(self.t2_test.shape)
        return s_i, s_t

def tj_plus_group(g, alpha, sigma=None):
    """TJ+G (sigma=None) / TJ+G-N: batch-level jackknife+ with max-member scores."""
    s_i, s_t = g._scales(sigma)
    R = g.r / s_i
    S = np.array([R[g.g_index == k].max() for k in range(g.K)])[:, None]
    return jackknife_plus(g.mu_test - s_t * S, g.mu_test + s_t * S, alpha)

def lgo_cv_plus(g, alpha, sigma=None):
    """CV+ with batches as folds and pooled member scores (no guarantee for new batches)."""
    s_i, s_t = g._scales(sigma)
    R = (g.r / s_i)[:, None]
    mu = g.mu_test[g.g_index]; st = s_t[g.g_index]
    return jackknife_plus(mu - st * R, mu + st * R, alpha)

def gauss_lgo(g, alpha):
    """Gaussian interval from leave-batch-out residuals, t with K-1 degrees of freedom."""
    rmse = np.sqrt(np.mean(g.r ** 2))
    t = stats.t.ppf(1 - alpha / 2, max(g.K - 1, 1))
    return g.tf.mu_full_test - t * rmse, g.tf.mu_full_test + t * rmse
