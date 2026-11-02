"""E15 (confirmatory): standards from batches on handheld instruments and seasons not used before.

For each target setting (instrument x season with at least 12 consignments, instrument not used in E8/E10), the
source model is a PLS model of master unit 15006, trained on all 15006 fruit EXCEPT fruit of the target setting's
consignments and fruit measured on the target instrument. The transfer is slope/bias correction (SBC), the usual
correction for handheld fruit meters; it needs only target spectra and reference values. Designs, methods and
outcomes as in E10; OLS-PI is added because the pipeline is SBC.
"""
import numpy as np
from ..data.meta import load_mango_v6_settings
from ..models.source_model import fit_source_model
from ..intervals import methods as M
from ..intervals import group as G
from ..intervals import classical as CL
from .batch import draw_design, _cov_metrics, _icc
from .datasets import BASE_SEED, _FIXED_CACHE
from .core import build_sigmas

SRC_INST = 15006

def _setting(setting, raw_dir):
    key = ("confirm", setting)
    if key in _FIXED_CACHE:
        return _FIXED_CACHE[key]
    inst, season = (int(v) for v in setting.split("_"))
    meta, X = load_mango_v6_settings(raw_dir)
    tgt = np.nonzero((meta["instrument"].to_numpy() == inst) & (meta["season"].to_numpy() == season))[0]
    tgt_pops = set(meta["pop"].to_numpy()[tgt])
    tgt_keys = set(meta["key"].to_numpy()[meta["instrument"].to_numpy() == inst])
    src = np.nonzero((meta["instrument"].to_numpy() == SRC_INST)
                     & ~meta["pop"].isin(tgt_pops).to_numpy()
                     & ~meta["key"].isin(tgt_keys).to_numpy())[0]
    y = meta["y"].to_numpy(float)
    source = fit_source_model(X[src], y[src], max_lv=25, seed=BASE_SEED)
    out = dict(X=X, y=y, pool=tgt, pop=meta["pop"].to_numpy().astype(str),
               date=meta["date"].to_numpy(), source=source, sigmas=build_sigmas(source), n_source=len(src))
    _FIXED_CACHE[key] = out
    return out

def run_confirm_rep(rep, cfg):
    rows = []
    for si, setting in enumerate(cfg["settings"]):
        S = _setting(setting, cfg["raw_dir"])
        X, y, pool, pop, date = S["X"], S["y"], S["pool"], S["pop"], S["date"]
        n_pops = len(set(pop[pool]))
        designs = [tuple(d) for d in cfg["designs"]] + \
                  [tuple(d) for d in cfg.get("designs_large", []) if n_pops >= d[1] + cfg.get("min_new_batches", 3)]
        for di, design in enumerate(designs):
            rng = np.random.default_rng(BASE_SEED + 3000017 * rep + 104729 * si + 7919 * di + 41)
            std, grp, new, same = draw_design(pool, pop, date, design, rng)
            if len(new) == 0:
                continue
            tf = M.TransferFits("sbc", S["source"], X[std], y[std], None, X[new], seed=BASE_SEED + rep)
            g = G.GroupTransferFits(tf, grp, X[std], X[new])
            s_tq = S["sigmas"]["tq"]
            e_new = y[new] - tf.mu_full_test
            base = dict(dataset="mango_confirm", setting=setting, rep=rep, design=design[0], K=design[1],
                        n_g=design[2], m=len(std), kind="sbc", n_source=S["n_source"], n_batches_setting=n_pops,
                        rmsep_new=float(np.sqrt(np.mean(e_new ** 2))), icc_new=_icc(e_new, pop[new]))
            for alpha in cfg["alphas"]:
                for name in cfg["methods"]:
                    if name == "TJ+N": lo, hi = M.tj_plus(tf, alpha, s_tq)
                    elif name == "Gauss-LOO": lo, hi = M.gauss_loo(tf, alpha)
                    elif name == "OLS-PI": lo, hi = CL.ols_pi_sbc(tf, S["source"], X[std], X[new], alpha)
                    elif name == "ASTM-PI": lo, hi = M.astm_pi(tf, S["source"], alpha)
                    elif name == "TJ+H-N": lo, hi = G.tj_plus_hier(g, alpha, s_tq)
                    elif name == "Gauss-LGO": lo, hi = G.gauss_lgo(g, alpha)
                    elif name == "ANOVA-PI": lo, hi = G.anova_pi(g, alpha)
                    else: raise ValueError(name)
                    r = dict(base, method=name, alpha=alpha)
                    r.update(_cov_metrics(np.broadcast_to(lo, new.shape), np.broadcast_to(hi, new.shape),
                                          y[new], pop[new], alpha, "new_"))
                    rows.append(r)
    return rows, []
