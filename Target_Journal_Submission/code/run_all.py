"""Reproduce every experiment, statistic, table and figure of the study.

    python run_all.py --mode quick   # pipeline check (few repetitions, minutes)
    python run_all.py --mode full    # complete pre-registered study (~2-3 h on 4 CPU cores)

Optional: --only E1_main_corn,E4_robust_mango   --jobs 4   --skip-experiments (re-analyse existing raw results)
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
from tjplus.utils import get_logger, set_seed, detect_device
from tjplus.experiments.runner import run_experiment
from tjplus.experiments.core import ALL_METHODS

def expand(name, spec, cfg_all, mode, raw_dir):
    """Expand variant/window/lv lists into individual runs."""
    base = {k: v for k, v in spec.items() if k not in ("variants", "half_windows", "lv_offsets", "reps_full", "reps_quick", "dataset")}
    base["raw_dir"] = raw_dir
    base.setdefault("alphas", cfg_all["alphas"])
    base["methods"] = ALL_METHODS if spec["methods"] == "ALL" else cfg_all["key_methods"]
    if mode == "quick":
        base["m_values"] = base["m_values"][:2]
    runs = []
    if "variants" in spec:
        for v in spec["variants"]:
            c = dict(base, variant=v)
            if v == "half_source" and spec["dataset"] == "corn":
                c["corn_n_train"] = 20
            runs.append((f"{name}__{v}", c))
    elif "half_windows" in spec:
        runs = [(f"{name}__hw{h}", dict(base, half_window=h)) for h in spec["half_windows"]]
    elif "lv_offsets" in spec:
        runs = [(f"{name}__lv{o:+d}", dict(base, lv_offset=o)) for o in spec["lv_offsets"]]
    else:
        runs = [(name, base)]
    return runs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=max(1, os.cpu_count() or 1))
    ap.add_argument("--skip-experiments", action="store_true")
    ap.add_argument("--no-analysis", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results"))
    a = ap.parse_args()
    out = os.path.abspath(a.out if a.mode == "full" else a.out + "_quick")
    raw_dir = os.path.join(HERE, "data", "raw")
    log = get_logger(logfile=os.path.join(out, "experiment_logs", f"run_all_{a.mode}.log"))
    set_seed(20261013)
    log.info(f"mode={a.mode} jobs={a.jobs} device={detect_device()} (all computations are CPU/numpy; device only used by the optional CNN)")
    cfg = json.load(open(os.path.join(HERE, "config", "experiments.json")))
    only = set(filter(None, a.only.split(",")))
    t0 = time.time()
    if not a.skip_experiments:
        for name, spec in cfg["experiments"].items():
            if only and name not in only:
                continue
            reps = spec["reps_full"] if a.mode == "full" else spec["reps_quick"]
            for rname, c in expand(name, spec, cfg, a.mode, raw_dir):
                run_experiment(rname, spec["dataset"], c, reps, os.path.join(out, "raw"), a.jobs, log)
        if not only or "E5_cnn_mango" in only:
            from tjplus.experiments.cnn_mango import run_cnn_experiment
            run_cnn_experiment(raw_dir, os.path.join(out, "raw"), reps=200 if a.mode == "full" else 3, log=log,
                               epochs=None if a.mode == "full" else 5)
        if not only or "E6_timing" in only:
            from tjplus.experiments.timing import run_timing
            run_timing(raw_dir, os.path.join(out, "raw"), n_repeat=20 if a.mode == "full" else 2, log=log)
    if a.no_analysis:
        log.info(f"experiments finished in {time.time() - t0:.0f}s (analysis skipped)"); return
    from tjplus.statistics.analysis import analyse_all
    analyse_all(out, cfg, log)
    from tjplus.visualization.figures import make_all_figures
    make_all_figures(out, cfg, log)
    log.info(f"finished in {time.time() - t0:.0f}s; outputs in {out}")

if __name__ == "__main__":
    main()
