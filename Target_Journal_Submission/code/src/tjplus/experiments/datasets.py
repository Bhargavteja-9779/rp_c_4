"""Dataset-specific repetition generators (splits exactly as pre-registered)."""
import numpy as np
from ..data.loaders import load_corn, load_tablets, load_mango
from ..models.source_model import fit_source_model
from .core import evaluate, build_sigmas

BASE_SEED = 20261013

def kennard_stone(X, k):
    X = np.asarray(X, float)
    D = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    i, j = np.unravel_index(np.argmax(D), D.shape)
    sel = [i, j]
    mind = np.minimum(D[i], D[j])
    while len(sel) < k:
        mind[sel] = -1
        nxt = int(np.argmax(mind)); sel.append(nxt); mind = np.minimum(mind, D[nxt])
    return np.array(sel[:k])

def _source_pool(source, X_tr, X_cal, y_cal):
    e_cal = y_cal - source.predict(X_cal)
    return np.r_[source.oof_resid, e_cal], np.vstack([X_tr, X_cal])

def _perturb(variant, X, rng, ref_sd):
    if variant.startswith("noise"):
        snr = float(variant.split("_")[1])
        return X + rng.normal(0, 1, X.shape) * (ref_sd / snr)
    return X

def _shift(X, s):
    Y = np.roll(X, s, axis=1)
    if s > 0: Y[:, :s] = X[:, :1]
    elif s < 0: Y[:, s:] = X[:, -1:]
    return Y

def _std_test(pool, m, rng, variant, X_pool_target):
    perm = rng.permutation(len(pool))
    if variant == "ks":
        cand = perm[: max(int(0.5 * len(pool)), m + 1)]
        sel = cand[kennard_stone(X_pool_target[cand], m)]
        rest = np.setdiff1d(np.arange(len(pool)), sel)
        return pool[sel], pool[rest]
    return pool[perm[:m]], pool[perm[m:]]

def run_corn_rep(rep, cfg):
    data = load_corn(cfg["raw_dir"])
    rng = np.random.default_rng(BASE_SEED + rep)
    perm = rng.permutation(80)
    n_tr = cfg.get("corn_n_train", 40)
    tr, cal, pool = perm[:n_tr], perm[40:50], perm[50:]
    rows, samples = [], []
    for pi in cfg["properties"]:
        y = data.Y[:, pi]
        for (src, tgt) in cfg["pairs"]:
            Xs, Xt = data.spectra[src], data.spectra[tgt]
            if cfg.get("model", "pls") == "ridge":
                from ..models.ridge import fit_source_ridge
                source = fit_source_ridge(Xs[tr], y[tr], max_lv=15, seed=BASE_SEED + rep)
            else:
                source = fit_source_model(Xs[tr], y[tr], max_lv=15, seed=BASE_SEED + rep, lv_offset=cfg.get("lv_offset", 0))
            sigmas = build_sigmas(source)
            e_pool, Xs_pool = _source_pool(source, Xs[tr], Xs[cal], y[cal])
            vr = np.random.default_rng(BASE_SEED + 7919 * rep + pi)
            Xt_all = _perturb(cfg.get("variant", ""), Xt, vr, Xt[pool].std(0).mean())
            for m in cfg["m_values"]:
                std, te = _std_test(pool, m, np.random.default_rng(BASE_SEED + 104729 * rep + m), cfg.get("variant", ""), Xt_all[pool])
                X_test = Xt_all[te]
                if cfg.get("variant", "").startswith("shift"):
                    X_test = _shift(X_test, int(cfg["variant"].split("_")[1]))
                for kind in cfg["kinds"]:
                    r, s = evaluate(source, sigmas, e_pool, Xs_pool, kind, Xt_all[std], y[std], Xs[std], X_test, y[te],
                                    Xt_all[pool], cfg["alphas"], seed=BASE_SEED + rep, half_window=cfg.get("half_window", 2),
                                    methods=cfg["methods"], keep_samples=cfg.get("keep_samples", False) and rep < 100 and kind == cfg["kinds"][0])
                    meta = dict(dataset="corn", property=data.properties[pi], source=src, target=tgt, rep=rep, prep=source.prep, A=source.A)
                    rows += [{**meta, **x} for x in r]
                    samples += [{**meta, "m": m, "sample": int(te[x["j"]]), **x} for x in s]
    return rows, samples

_FIXED_CACHE = {}

def _fixed_source(dataset, cfg, pi):
    """Tablets/mango: the source split and source model are fixed (seeded once) across repetitions."""
    key = (dataset, pi, cfg.get("variant", ""), cfg.get("lv_offset", 0), cfg.get("model", "pls"))
    if key in _FIXED_CACHE:
        return _FIXED_CACHE[key]
    if dataset == "tablets":
        d = load_tablets(cfg["raw_dir"])
        src, tgt = "1", "2"
        tr = np.nonzero(d.split == "calibrate")[0]; cal = np.nonzero(d.split == "validate")[0]
        pool = np.nonzero(d.split == "test")[0]
        if cfg.get("variant") == "half_source":
            tr = np.random.default_rng(BASE_SEED).permutation(tr)[: len(tr) // 2]
        y = d.Y[:, pi]; Xs, Xt = d.spectra[src], d.spectra[tgt]; maxlv = 15; prop = d.properties[pi]
    else:
        d = load_mango(cfg["raw_dir"])
        srcidx = np.nonzero(d.season <= 3)[0]; pool = np.nonzero(d.season == 4)[0]
        p = np.random.default_rng(BASE_SEED).permutation(srcidx)
        ncal = int(round(0.2 * len(p))); cal, tr = p[:ncal], p[ncal:]
        if cfg.get("variant") == "half_source":
            tr = tr[: len(tr) // 2]
        y = d.y; Xs = Xt = d.X; maxlv = 25; prop = "dry_matter"
    if cfg.get("model", "pls") == "pls":
        source = fit_source_model(Xs[tr], y[tr], max_lv=maxlv, seed=BASE_SEED, lv_offset=cfg.get("lv_offset", 0))
    else:
        from ..models.ridge import fit_source_ridge
        source = fit_source_ridge(Xs[tr], y[tr], max_lv=maxlv, seed=BASE_SEED)
    sigmas = build_sigmas(source)
    e_pool, Xs_pool = _source_pool(source, Xs[tr], Xs[cal], y[cal])
    out = dict(y=y, Xs=Xs, Xt=Xt, pool=pool, source=source, sigmas=sigmas, e_pool=e_pool, Xs_pool=Xs_pool, prop=prop)
    _FIXED_CACHE[key] = out
    return out

def run_fixed_rep(dataset, rep, cfg):
    rows, samples = [], []
    for pi in cfg["properties"]:
        F = _fixed_source(dataset, cfg, pi)
        y, Xs, pool, source = F["y"], F["Xs"], F["pool"], F["source"]
        vr = np.random.default_rng(BASE_SEED + 7919 * rep + pi)
        Xt_all = _perturb(cfg.get("variant", ""), F["Xt"], vr, F["Xt"][pool].std(0).mean())
        for m in cfg["m_values"]:
            std, te = _std_test(pool, m, np.random.default_rng(BASE_SEED + 104729 * rep + m), cfg.get("variant", ""), Xt_all[pool])
            X_test = Xt_all[te]
            if cfg.get("variant", "").startswith("shift"):
                X_test = _shift(X_test, int(cfg["variant"].split("_")[1]))
            for kind in cfg["kinds"]:
                r, s = evaluate(source, F["sigmas"], F["e_pool"], F["Xs_pool"], kind, Xt_all[std], y[std],
                                Xs[std] if dataset == "tablets" else None, X_test, y[te], Xt_all[pool], cfg["alphas"],
                                seed=BASE_SEED + rep, half_window=cfg.get("half_window", 2), methods=cfg["methods"],
                                keep_samples=cfg.get("keep_samples", False) and rep < 100 and kind == cfg["kinds"][0])
                meta = dict(dataset=dataset, property=F["prop"], source="1" if dataset == "tablets" else "S1-3",
                            target="2" if dataset == "tablets" else "S4", rep=rep, prep=source.prep, A=source.A)
                rows += [{**meta, **x} for x in r]
                samples += [{**meta, "m": m, "sample": int(te[x["j"]]), **x} for x in s]
    return rows, samples

def run_mango_inst_rep(rep, cfg):
    """E8 (review-driven external validation): mango instrument shift with paired spectra.
    Source = instrument 15006 fruit NOT measured on the target instrument (80/20 train/cal, fixed seed);
    target pool = fruit measured on both instruments (target spectrum + paired master spectrum)."""
    from ..data.loaders import load_mango_instruments
    d = load_mango_instruments(cfg["raw_dir"])
    src_inst = 15006
    rows = []
    for pi in cfg["properties"]:
        tgt = cfg["targets"][pi]
        key = ("mango_inst", tgt, cfg.get("model", "pls"))
        if key not in _FIXED_CACHE:
            srcidx = np.nonzero(d.present[src_inst] & ~d.present[tgt])[0]
            pool = np.nonzero(d.present[src_inst] & d.present[tgt])[0]
            p = np.random.default_rng(BASE_SEED + tgt).permutation(srcidx)
            ncal = int(round(0.2 * len(p))); cal, tr = p[:ncal], p[ncal:]
            Xs = d.spectra[src_inst]
            source = fit_source_model(Xs[tr], d.y[tr], max_lv=25, seed=BASE_SEED)
            sigmas = build_sigmas(source)
            e_pool, Xs_pool = _source_pool(source, Xs[tr], Xs[cal], d.y[cal])
            _FIXED_CACHE[key] = (pool, source, sigmas, e_pool, Xs_pool)
        pool, source, sigmas, e_pool, Xs_pool = _FIXED_CACHE[key]
        Xs, Xt, y = d.spectra[src_inst], d.spectra[tgt], d.y
        for m in cfg["m_values"]:
            std, te = _std_test(pool, m, np.random.default_rng(BASE_SEED + 104729 * rep + m), "", Xt[pool])
            for kind in cfg["kinds"]:
                r, _ = evaluate(source, sigmas, e_pool, Xs_pool, kind, Xt[std], y[std], Xs[std], Xt[te], y[te], Xt[pool],
                                cfg["alphas"], seed=BASE_SEED + rep, methods=cfg["methods"])
                meta = dict(dataset="mango_inst", property="dry_matter", source=str(src_inst), target=str(tgt), rep=rep,
                            prep=source.prep, A=source.A)
                rows += [{**meta, **x} for x in r]
    return rows, []
