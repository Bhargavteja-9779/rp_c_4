"""E10 (reinforcement): standards drawn from a few batches, routine samples from new batches.

Settings (real batch structure of the mango data; a batch is a population of ~40 fruit):
  season  : season shift (source seasons 1-3, fixed source model of E1), target season 4 (18 batches).
  inst_T  : instrument shift 15006 -> T (source model of E8), target batches = populations of fruit
            measured on both instruments.
Designs:
  ("random", K, n_g): K batches drawn at random from the eligible batches (size >= n_g), n_g standards
            drawn at random within each; NEW-batch test set = all fruit of the batches not drawn;
            SAME-batch test set = the remaining fruit of the drawn batches.
  ("chrono", K, n_g): batches ordered by harvest date; standards from the K earliest batches; NEW-batch
            test set = batches harvested strictly after the latest standard batch (deterministic batches,
            random members).
Primary outcome: batch-weighted coverage on the new-batch test set (mean over batches of the within-batch
coverage), which is the probability addressed by Proposition 2.
"""
import numpy as np
from ..data.loaders import load_mango_instruments
from ..data.meta import load_mango_meta, load_mango_inst_meta
from ..models.source_model import fit_source_model
from ..intervals import methods as M
from ..intervals import group as G
from .datasets import _fixed_source, _source_pool, BASE_SEED, _FIXED_CACHE
from .core import build_sigmas

SAMPLE_METHODS = ["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI", "SCP-S"]
GROUP_METHODS = ["TJ+G-N", "TJ+G", "LGO-CV+N", "Gauss-LGO"]

def _setting(setting, raw_dir):
    key = ("batch", setting)
    if key in _FIXED_CACHE:
        return _FIXED_CACHE[key]
    if setting == "season":
        F = _fixed_source("mango", {"raw_dir": raw_dir}, 0)
        meta = load_mango_meta(raw_dir)
        pool = F["pool"]
        out = dict(y=F["y"], Xt=F["Xt"], Xs=None, pool=pool, source=F["source"], sigmas=F["sigmas"],
                   e_pool=F["e_pool"], pop=meta["pop"].to_numpy(), date=meta["date"].to_numpy(),
                   target="S4", src="S1-3")
    else:
        tgt = int(setting.split("_")[1]); src_inst = 15006
        d = load_mango_instruments(raw_dir); meta = load_mango_inst_meta(raw_dir)
        srcidx = np.nonzero(d.present[src_inst] & ~d.present[tgt])[0]
        pool = np.nonzero(d.present[src_inst] & d.present[tgt])[0]
        p = np.random.default_rng(BASE_SEED + tgt).permutation(srcidx)       # identical to E8
        ncal = int(round(0.2 * len(p))); cal, tr = p[:ncal], p[ncal:]
        Xs = d.spectra[src_inst]
        source = fit_source_model(Xs[tr], d.y[tr], max_lv=25, seed=BASE_SEED)
        sigmas = build_sigmas(source)
        e_pool, _ = _source_pool(source, Xs[tr], Xs[cal], d.y[cal])
        out = dict(y=d.y, Xt=d.spectra[tgt], Xs=Xs, pool=pool, source=source, sigmas=sigmas, e_pool=e_pool,
                   pop=meta["pop"].to_numpy(), date=meta["date"].to_numpy(), target=str(tgt), src=str(src_inst))
    _FIXED_CACHE[key] = out
    return out

def draw_design(pool, pop, date, design, rng):
    """Returns (standard indices, their batch labels, new-batch test indices, same-batch test indices)."""
    kind, K, ng = design
    labels, counts = np.unique(pop[pool], return_counts=True)
    if kind == "random":
        elig = labels[counts >= ng]
        chosen = rng.choice(elig, K, replace=False)
    else:
        first = {lab: date[pool][pop[pool] == lab].min() for lab in labels}
        order = sorted([lab for lab in labels if (pop[pool] == lab).sum() >= ng], key=lambda l: (first[l], l))
        chosen = np.array(order[:K])
    std, grp = [], []
    for lab in chosen:
        members = pool[pop[pool] == lab]
        pick = rng.choice(members, ng, replace=False)
        std += list(pick); grp += [lab] * ng
    std = np.array(std); grp = np.array(grp)
    in_chosen = np.isin(pop[pool], chosen)
    same = np.setdiff1d(pool[in_chosen], std)
    if kind == "random":
        new = pool[~in_chosen]
    else:
        first = {lab: date[pool][pop[pool] == lab].min() for lab in labels}
        last = max(first[lab] for lab in chosen)
        later = np.array([first[lab] > last for lab in pop[pool]])
        new = pool[~in_chosen & later]
    return std, grp, new, same

def _icc(e, g):
    """One-way ANOVA estimator of the intra-batch correlation of errors."""
    labs = np.unique(g)
    if len(labs) < 2:
        return np.nan
    n = np.array([(g == l).sum() for l in labs]); means = np.array([e[g == l].mean() for l in labs])
    N, k = len(e), len(labs)
    msb = (n * (means - e.mean()) ** 2).sum() / (k - 1)
    msw = sum(((e[g == l] - e[g == l].mean()) ** 2).sum() for l in labs) / max(N - k, 1)
    n0 = (N - (n ** 2).sum() / N) / (k - 1)
    return float((msb - msw) / (msb + (n0 - 1) * msw))

def _cov_metrics(lo, hi, y, pop, alpha, prefix):
    lo = np.broadcast_to(lo, y.shape); hi = np.broadcast_to(hi, y.shape)
    cov = (y >= lo) & (y <= hi)
    finite = np.isfinite(lo) & np.isfinite(hi)
    labs = np.unique(pop)
    bw = float(np.mean([cov[pop == l].mean() for l in labs])) if len(labs) else np.nan
    w = hi - lo
    IS = (np.mean(w + (2 / alpha) * np.maximum(lo - y, 0) + (2 / alpha) * np.maximum(y - hi, 0))
          if finite.all() else np.inf)
    return {f"{prefix}coverage": bw, f"{prefix}coverage_fruit": float(cov.mean()),
            f"{prefix}median_width": float(np.median(w[finite])) if finite.any() else np.nan,
            f"{prefix}frac_inf": float(1 - finite.mean()), f"{prefix}interval_score": float(IS),
            f"{prefix}n_test": int(len(y)), f"{prefix}n_batches": int(len(labs))}

def run_batch_rep(rep, cfg):
    rows = []
    for setting in cfg["settings"]:
        S = _setting(setting, cfg["raw_dir"])
        y, Xt, pool, pop, date = S["y"], S["Xt"], S["pool"], S["pop"], S["date"]
        designs = list(cfg["designs"]) + (list(cfg.get("designs_inst_extra", [])) if setting.startswith("inst") else [])
        for di, design in enumerate(designs):
            design = tuple(design)
            rng = np.random.default_rng(BASE_SEED + 1000003 * rep + 7919 * di + 17)
            std, grp, new, same = draw_design(pool, pop, date, design, rng)
            if len(new) == 0:
                continue
            te = np.r_[new, same]; is_new = np.r_[np.ones(len(new), bool), np.zeros(len(same), bool)]
            for kind in cfg["kinds"][setting.split("_")[0]]:
                Xs_std = None if S["Xs"] is None else S["Xs"][std]
                tf = M.TransferFits(kind, S["source"], Xt[std], y[std], Xs_std, Xt[te], seed=BASE_SEED + rep)
                g = G.GroupTransferFits(tf, grp, Xt[std], Xt[te])
                s_tq = S["sigmas"]["tq"]
                e_new = y[new] - tf.mu_full_test[is_new]
                base = dict(dataset="mango_batch", setting=setting, source=S["src"], target=S["target"], rep=rep,
                            design=design[0], K=design[1], n_g=design[2], m=len(std), kind=kind,
                            rmsep_new=float(np.sqrt(np.mean(e_new ** 2))), icc_new=_icc(e_new, pop[new]),
                            icc_std_loo=_icc(tf.y_std - tf.mu_loo_i, grp))
                for alpha in cfg["alphas"]:
                    for name in cfg["methods"]:
                        if name == "TJ+N": lo, hi = M.tj_plus(tf, alpha, s_tq)
                        elif name == "TJ+": lo, hi = M.tj_plus(tf, alpha, None)
                        elif name == "Gauss-LOO": lo, hi = M.gauss_loo(tf, alpha)
                        elif name == "SCP-T-split-N": lo, hi = M.scp_target_split(tf, Xt[te], Xt[std], alpha, s_tq, BASE_SEED + rep)
                        elif name == "ASTM-PI": lo, hi = M.astm_pi(tf, S["source"], alpha)
                        elif name == "SCP-S": lo, hi = M.scp_source(tf, S["e_pool"], alpha)
                        elif name == "TJ+G-N": lo, hi = G.tj_plus_group(g, alpha, s_tq)
                        elif name == "TJ+G": lo, hi = G.tj_plus_group(g, alpha, None)
                        elif name == "LGO-CV+N": lo, hi = G.lgo_cv_plus(g, alpha, s_tq)
                        elif name == "Gauss-LGO": lo, hi = G.gauss_lgo(g, alpha)
                        elif name == "TJ+H-N": lo, hi = G.tj_plus_hier(g, alpha, s_tq)
                        elif name == "TJ+H": lo, hi = G.tj_plus_hier(g, alpha, None)
                        elif name == "ANOVA-PI": lo, hi = G.anova_pi(g, alpha)
                        else: raise ValueError(name)
                        lo = np.broadcast_to(lo, te.shape); hi = np.broadcast_to(hi, te.shape)
                        r = dict(base, method=name, alpha=alpha)
                        r.update(_cov_metrics(lo[is_new], hi[is_new], y[new], pop[new], alpha, "new_"))
                        r.update(_cov_metrics(lo[~is_new], hi[~is_new], y[same], pop[same], alpha, "same_"))
                        rows.append(r)
    return rows, []

# ----------------------------------------------------------------------------- E14: application case study
def run_application_rep(rep, cfg):
    """Mango harvest-maturity screening at a dry-matter threshold (default 14 % DM) after a season or instrument
    change. Decision per fruit from a two-sided (1-alpha) interval: PASS if lower >= threshold, FAIL if upper <
    threshold, otherwise REFER (re-measure / destructive check). 'Point' passes a fruit if yhat >= threshold."""
    thr, alpha = cfg["threshold"], cfg["alpha"]
    rows = []
    for setting in cfg["settings"]:
        S = _setting(setting, cfg["raw_dir"])
        y, Xt, pool, pop, date = S["y"], S["Xt"], S["pool"], S["pop"], S["date"]
        designs = list(cfg["designs"]) + (list(cfg.get("designs_inst_extra", [])) if setting.startswith("inst") else [])
        for di, design in enumerate(designs):
            design = tuple(design)
            rng = np.random.default_rng(BASE_SEED + 2000003 * rep + 7919 * di + 29)
            std, grp, new, same = draw_design(pool, pop, date, design, rng)
            yt = y[new]
            for kind in cfg["kinds"][setting.split("_")[0]]:
                Xs_std = None if S["Xs"] is None else S["Xs"][std]
                tf = M.TransferFits(kind, S["source"], Xt[std], y[std], Xs_std, Xt[new], seed=BASE_SEED + rep)
                g = G.GroupTransferFits(tf, grp, Xt[std], Xt[new])
                s_tq = S["sigmas"]["tq"]
                cand = {"Point": None, "TJ+N": M.tj_plus(tf, alpha, s_tq), "TJ+H-N": G.tj_plus_hier(g, alpha, s_tq),
                        "Gauss-LOO": M.gauss_loo(tf, alpha), "ASTM-PI": M.astm_pi(tf, S["source"], alpha)}
                for name, iv in cand.items():
                    if iv is None:
                        passed = tf.mu_full_test >= thr; failed = ~passed
                    else:
                        lo = np.broadcast_to(iv[0], yt.shape); hi = np.broadcast_to(iv[1], yt.shape)
                        passed = lo >= thr; failed = hi < thr
                    imm = yt < thr
                    rows.append(dict(setting=setting, rep=rep, design=design[0], K=design[1], n_g=design[2], m=len(std),
                                     kind=kind, method=name, n=len(yt), n_immature=int(imm.sum()),
                                     immature_passed=int((passed & imm).sum()), mature_failed=int((failed & ~imm).sum()),
                                     n_passed=int(passed.sum()), n_failed=int(failed.sum()),
                                     n_referred=int((~passed & ~failed).sum())))
    return rows, []
