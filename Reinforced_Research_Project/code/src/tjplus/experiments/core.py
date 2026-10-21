"""Evaluation of all interval methods for one (source model, standards, test set) configuration."""
import time
import numpy as np
from ..intervals import methods as M
from ..evaluation.metrics import interval_metrics, tertile_coverage
from ..models.source_model import DifficultyModel
from ..models.transfer import needs_pairs
from ..intervals import classical as CL

ALL_METHODS = ["TJ+N", "TJ+", "TCV+N", "TJ-naive-N", "TJ-insample-N", "TJ+N[T2]", "TJ+N[Q]",
               "SCP-T-split-N", "SCP-T-split", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"]

def build_sigmas(source):
    """Difficulty models fitted on |OOF residuals| of source training only."""
    out = {}
    for name, feats in (("tq", ("t2", "q")), ("t2", ("t2",)), ("q", ("q",))):
        out[name] = DifficultyModel(feats).fit(source.oof_t2, source.oof_q, np.abs(source.oof_resid))
    return out

def evaluate(source, sigmas, e_pool, Xs_pool, kind, Xt_std, y_std, Xs_std, X_test, y_test,
             X_target_unlab, alphas, seed, half_window=2, methods=ALL_METHODS, keep_samples=False,
             error_stats=False, boot_B=200):
    rows, samples = [], []
    t0 = time.perf_counter()
    tf = M.TransferFits(kind, source, Xt_std, y_std, Xs_std, X_test, half_window, seed=seed)
    t_fits = time.perf_counter() - t0
    rmsep = float(np.sqrt(np.mean((tf.mu_full_test - y_test) ** 2)))
    s_tq = sigmas["tq"]
    sig_test = s_tq(*tf.diag_full_test)
    paired = needs_pairs(kind)
    boot = None
    extra = {}
    if error_stats:
        # shape of the deployed predictor's test errors (reinforcement E12: why Gaussian intervals fail)
        from scipy import stats as _st
        e = y_test - tf.mu_full_test
        z = e / max(np.sqrt(np.mean(e ** 2)), 1e-300)
        rmse_loo = float(np.sqrt(np.mean(tf.r_loo ** 2)))
        extra = dict(err_skew=float(_st.skew(z)), err_exkurt=float(_st.kurtosis(z)),
                     err_bias_rel=float(np.mean(e) / max(np.std(e), 1e-300)),
                     rmsep_over_rmseloo=rmsep / max(rmse_loo, 1e-300),
                     loo_exkurt=float(_st.kurtosis(tf.r_loo * np.sign(tf.y_std - tf.mu_loo_i))) if tf.m > 3 else np.nan,
                     spearman_abs_err_sigma=float(_st.spearmanr(np.abs(e), sig_test)[0]))
    for alpha in alphas:
        for name in methods:
            if name in ("Transport", "LF-conv") and not paired:
                continue
            t1 = time.perf_counter()
            if name == "TJ+N": lo, hi = M.tj_plus(tf, alpha, s_tq)
            elif name == "TJ+": lo, hi = M.tj_plus(tf, alpha, None)
            elif name == "TCV+N": lo, hi = M.tcv_plus(tf, alpha, s_tq)
            elif name == "TJ-naive-N": lo, hi = M.tj_naive(tf, alpha, s_tq)
            elif name == "TJ-insample-N": lo, hi = M.tj_insample(tf, alpha, s_tq)
            elif name == "TJ+N[T2]": lo, hi = M.tj_plus(tf, alpha, sigmas["t2"])
            elif name == "TJ+N[Q]": lo, hi = M.tj_plus(tf, alpha, sigmas["q"])
            elif name == "SCP-T-split-N": lo, hi = M.scp_target_split(tf, X_test, Xt_std, alpha, s_tq, seed)
            elif name == "SCP-T-split": lo, hi = M.scp_target_split(tf, X_test, Xt_std, alpha, None, seed)
            elif name == "Gauss-LOO": lo, hi = M.gauss_loo(tf, alpha)
            elif name == "Gauss-LOO-N": lo, hi = M.gauss_loo_normalised(tf, alpha, s_tq)
            elif name == "ASTM-PI": lo, hi = M.astm_pi(tf, source, alpha)
            elif name == "SCP-S": lo, hi = M.scp_source(tf, e_pool, alpha)
            elif name == "WCP-S": lo, hi = M.wcp_source(tf, source, e_pool, Xs_pool, X_target_unlab, X_test, alpha)
            elif name == "Transport": lo, hi = M.transport(tf, source, e_pool, Xs_pool, Xt_std, Xs_std, alpha, half_window)
            elif name == "LF-conv": lo, hi = M.label_free_conv(tf, source, e_pool, Xt_std, Xs_std, alpha)
            elif name == "ASTM-T": lo, hi = CL.astm_target(tf, alpha)
            elif name == "OLS-PI":
                if kind != "sbc":
                    continue
                lo, hi = CL.ols_pi_sbc(tf, source, Xt_std, X_test, alpha)
            elif name == "Boot-T":
                if boot is None:
                    boot = CL.BootTransfer(tf, X_test, Xt_std, kind, B=boot_B, seed=seed + 31)
                lo, hi = boot.interval(alpha)
            else: raise ValueError(name)
            dt = time.perf_counter() - t1
            r = dict(method=name, alpha=alpha, kind=kind, m=len(y_std), rmsep=rmsep, t_method=dt, t_transfer_fits=t_fits)
            r.update(extra)
            r.update(interval_metrics(lo, hi, y_test, alpha))
            r.update(tertile_coverage(lo, hi, y_test, sig_test, "cov_sig"))
            r.update(tertile_coverage(lo, hi, y_test, y_test, "cov_y"))
            rows.append(r)
            if keep_samples and alpha == 0.1 and name in ("TJ+N", "TJ+", "ASTM-PI", "SCP-S", "Gauss-LOO", "SCP-T-split-N"):
                t2, q = tf.diag_full_test
                lo_b = np.broadcast_to(lo, y_test.shape); hi_b = np.broadcast_to(hi, y_test.shape)
                for j in range(len(y_test)):
                    samples.append(dict(method=name, j=j, y=y_test[j], yhat=tf.mu_full_test[j], lo=lo_b[j], hi=hi_b[j],
                                        t2=t2[j], q=q[j], sigma=sig_test[j]))
    return rows, samples
