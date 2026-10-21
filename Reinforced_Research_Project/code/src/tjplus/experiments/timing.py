"""E6: computational cost of the interval methods (wall-clock, single core) and memory."""
import os, time, tracemalloc
import numpy as np, pandas as pd
from ..data.loaders import load_corn, load_tablets, load_mango
from ..models.source_model import fit_source_model
from ..models.transfer import fit_deployed
from ..intervals import methods as M
from .core import build_sigmas
from .datasets import BASE_SEED, _source_pool

def _cases(raw_dir):
    c = load_corn(raw_dir); rng = np.random.default_rng(BASE_SEED); perm = rng.permutation(80)
    tr, cal, pool = perm[:40], perm[40:50], perm[50:]
    y = c.Y[:, 0]
    yield "corn", "pds", c.spectra["m5"], c.spectra["mp5"], y, tr, cal, pool, 20
    t = load_tablets(raw_dir); y = t.Y[:, 2]
    yield ("tablets", "pds", t.spectra["1"], t.spectra["2"], y, np.nonzero(t.split == "calibrate")[0],
           np.nonzero(t.split == "validate")[0], np.nonzero(t.split == "test")[0], 50)
    mg = load_mango(raw_dir); src = np.nonzero(mg.season <= 3)[0]; p = np.random.default_rng(BASE_SEED).permutation(src)
    ncal = int(round(0.2 * len(p)))
    yield "mango", "sbc", mg.X, mg.X, mg.y, p[ncal:], p[:ncal], np.nonzero(mg.season == 4)[0], 50

def run_timing(raw_dir, out_dir, n_repeat=20, log=None, alpha=0.1):
    rows = []
    for name, kind, Xs, Xt, y, tr, cal, pool, m in _cases(raw_dir):
        t0 = time.perf_counter(); source = fit_source_model(Xs[tr], y[tr], max_lv=25 if name == "mango" else 15, seed=BASE_SEED)
        t_source = time.perf_counter() - t0
        sig = build_sigmas(source)["tq"]
        e_pool, Xs_pool = _source_pool(source, Xs[tr], Xs[cal], y[cal])
        std, te = pool[:m], pool[m:]
        Xs_std = Xs[std] if kind == "pds" else None
        def full_only():
            d = fit_deployed(kind, source, Xt[std], y[std], Xs_std); d.predict(Xt[te]); return d
        def tjplus():
            tf = M.TransferFits(kind, source, Xt[std], y[std], Xs_std, Xt[te]); return M.tj_plus(tf, alpha, sig)
        def split():
            d = fit_deployed(kind, source, Xt[std[: m // 2]], y[std[: m // 2]], None if Xs_std is None else Xs_std[: m // 2])
            d.predict(Xt[std[m // 2:]]); d.predict(Xt[te])
        funcs = {"point prediction only (1 transfer fit)": full_only, "SCP-T-split (1 fit)": split,
                 "TJ+N incl. m LOO + 5 CV fits": tjplus}
        for label, fn in funcs.items():
            fn()  # warm-up
            ts = []
            for _ in range(n_repeat):
                t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
            tracemalloc.start(); fn(); _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
            rows.append(dict(dataset=name, kind=kind, m=m, n_test=len(te), n_channels=Xt.shape[1], step=label,
                             median_s=float(np.median(ts)), p90_s=float(np.quantile(ts, 0.9)), peak_mem_MB=peak / 2**20,
                             source_model_fit_s=t_source))
        if log: log.info(f"[E6_timing] {name} done")
    df = pd.DataFrame(rows); os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, "E6_timing.csv"), index=False)
    return df

def run_timing_scaling(raw_dir, out_dir, m_values=(10, 20, 30, 50), n_repeat=10, log=None, alpha=0.1):
    """E6b (review round 6): wall-clock time of TJ+N and of a single transfer fit as a function of m (single core)."""
    rows = []
    for name, kind, Xs, Xt, y, tr, cal, pool, _ in _cases(raw_dir):
        source = fit_source_model(Xs[tr], y[tr], max_lv=25 if name == "mango" else 15, seed=BASE_SEED)
        sig = build_sigmas(source)["tq"]
        for m in m_values:
            if m >= len(pool) - 5:
                continue
            std, te = pool[:m], pool[m:]
            Xs_std = Xs[std] if kind == "pds" else None
            def one():
                d = fit_deployed(kind, source, Xt[std], y[std], Xs_std); d.predict(Xt[te])
            def tj():
                tf = M.TransferFits(kind, source, Xt[std], y[std], Xs_std, Xt[te]); M.tj_plus(tf, alpha, sig)
            for label, fn in (("single transfer fit + prediction", one), ("TJ+N (m LOO + 5 CV fits)", tj)):
                fn(); ts = []
                for _ in range(n_repeat):
                    t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
                rows.append(dict(dataset=name, kind=kind, m=m, n_test=len(te), step=label, median_s=float(np.median(ts))))
        if log: log.info(f"[E6b_scaling] {name} done")
    df = pd.DataFrame(rows); df.to_csv(os.path.join(out_dir, "E6b_timing_scaling.csv"), index=False)
    return df
