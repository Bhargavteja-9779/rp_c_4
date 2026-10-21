"""E5 (model class): 1D-CNN trained once on mango seasons 1-3; intervals on season 4 after SBC.
Deviation from the PLS protocol (logged in deviations.md): sigma(x) and the source residual pool use
source-calibration residuals (no 10-fold OOF re-training of the CNN)."""
import os, time
import numpy as np, pandas as pd
from scipy import stats
from ..data.loaders import load_mango
from ..models.source_model import fit_source_model, DifficultyModel
from ..models.cnn import CNNRegressor
from ..utils import detect_device, set_seed
from .core import evaluate
from .datasets import BASE_SEED
from ..evaluation.metrics import interval_metrics, tertile_coverage

KEY = ["TJ+N", "TJ+", "SCP-T-split-N", "SCP-T-split", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"]

class CNNSource:
    def __init__(self, cnn, pls, Xcal, ycal):
        self.cnn, self._pls = cnn, pls
        self.prep, self.model, self.A = pls.prep, pls.model, pls.A
        r = ycal - cnn.predict(Xcal)
        self.oof_resid = r
        self.oof_t2, self.oof_q = pls.diagnostics(Xcal)
        self.sec = float(np.sqrt(np.mean(r ** 2)))
    def transform(self, X): return self._pls.transform(X)
    def predict(self, X):
        return self.cnn.predict(X)  # no caching: address-keyed caches can return stale results
    def diagnostics(self, X): return self._pls.diagnostics(X)
    def leverage(self, X): return self._pls.leverage(X)

def run_cnn_experiment(raw_dir, out_dir, reps=200, log=None, epochs=None, m_values=(10, 20, 30, 50), alpha=0.1):
    set_seed(BASE_SEED)
    d = load_mango(raw_dir)
    srcidx = np.nonzero(d.season <= 3)[0]; pool = np.nonzero(d.season == 4)[0]
    p = np.random.default_rng(BASE_SEED).permutation(srcidx)
    ncal = int(round(0.2 * len(p))); cal, tr = p[:ncal], p[ncal:]
    # early-stopping split inside source training only
    pe = np.random.default_rng(BASE_SEED + 1).permutation(tr); nval = len(pe) // 10
    t0 = time.time()
    cnn = CNNRegressor(epochs=epochs or 150, seed=BASE_SEED % 10000, device=detect_device()).fit(
        d.X[pe[nval:]], d.y[pe[nval:]], d.X[pe[:nval]], d.y[pe[:nval]])
    t_train = time.time() - t0
    pls = fit_source_model(d.X[tr], d.y[tr], max_lv=25, seed=BASE_SEED)
    src = CNNSource(cnn, pls, d.X[cal], d.y[cal])
    sig = DifficultyModel(("t2", "q")).fit(src.oof_t2, src.oof_q, np.abs(src.oof_resid))
    sigmas = {"tq": sig, "t2": sig, "q": sig}
    e_pool, Xs_pool = src.oof_resid, d.X[cal]
    mc_mean, mc_var = cnn.predict_mc(d.X[pool], T=100, seed=BASE_SEED)
    s2_cal = float(np.mean(src.oof_resid ** 2))
    rows = []
    for rep in range(reps):
        for m in m_values:
            rng = np.random.default_rng(BASE_SEED + 104729 * rep + m)
            perm = rng.permutation(len(pool)); std, te = pool[perm[:m]], pool[perm[m:]]
            r, _ = evaluate(src, sigmas, e_pool, Xs_pool, "sbc", d.X[std], d.y[std], None, d.X[te], d.y[te],
                            d.X[pool], [alpha], seed=BASE_SEED + rep, methods=KEY)
            # MC-dropout baseline (+ SBC fitted on the standards' MC means)
            mm_std, mm_te = mc_mean[perm[:m]], mc_mean[perm[m:]]
            b, a = np.polyfit(mm_std, d.y[std], 1)
            sd = abs(b) * np.sqrt(mc_var[perm[m:]] + s2_cal)
            z = stats.norm.ppf(1 - alpha / 2)
            lo, hi = a + b * mm_te - z * sd, a + b * mm_te + z * sd
            x = dict(method="MC-dropout", alpha=alpha, kind="sbc", m=m, rmsep=float(np.sqrt(np.mean((a + b * mm_te - d.y[te]) ** 2))),
                     t_method=np.nan, t_transfer_fits=np.nan)
            x.update(interval_metrics(lo, hi, d.y[te], alpha)); x.update(tertile_coverage(lo, hi, d.y[te], sig(*src.diagnostics(d.X[te])), "cov_sig"))
            x.update(tertile_coverage(lo, hi, d.y[te], d.y[te], "cov_y"))
            r.append(x)
            meta = dict(dataset="mango", property="dry_matter", source="S1-3", target="S4", rep=rep, prep="cnn", A=pls.A)
            rows += [{**meta, **xx} for xx in r]
        if log and (rep + 1) % max(1, reps // 5) == 0:
            log.info(f"[E5_cnn_mango] {rep + 1}/{reps}")
    df = pd.DataFrame(rows)
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, "E5_cnn_mango.csv.gz"), index=False)
    pd.DataFrame(cnn.history_, columns=["epoch", "train_mse_std", "val_mse_std"]).to_csv(os.path.join(out_dir, "E5_cnn_training_history.csv"), index=False)
    info = dict(n_params=cnn.n_params(), train_seconds=t_train, epochs_run=len(cnn.history_), device=detect_device(),
                source_cal_rmse=float(np.sqrt(s2_cal)))
    pd.Series(info).to_json(os.path.join(out_dir, "E5_cnn_info.json"))
    if log: log.info(f"[E5_cnn_mango] done {info}")
    return df
