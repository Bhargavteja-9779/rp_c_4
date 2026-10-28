"""Reinforcement experiments of the second research cycle (E10 batch-structured standards, E11 classical
competitors + E12 error-shape statistics), followed by their analysis.

    python run_reinforcement.py --mode quick        # pipeline check (minutes)
    python run_reinforcement.py --mode full         # all reinforcement experiments (~3-4 h on 4 cores)
    python run_reinforcement.py --skip-experiments  # re-analyse existing raw results

The original study (E1-E9) is reproduced with run_all.py; its raw results are read from
../../Target_Journal_Submission/results by the analysis.
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
from tjplus.utils import get_logger, set_seed
from tjplus.experiments.runner import run_experiment

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=max(1, os.cpu_count() or 1))
    ap.add_argument("--skip-experiments", action="store_true")
    ap.add_argument("--no-analysis", action="store_true")
    ap.add_argument("--rep-start", type=int, default=0)
    ap.add_argument("--rep-end", type=int, default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results"))
    a = ap.parse_args()
    out = os.path.abspath(a.out if a.mode == "full" else a.out + "_quick")
    raw_dir = os.path.join(HERE, "data", "raw")
    log = get_logger(logfile=os.path.join(out, "experiment_logs", f"run_reinforcement_{a.mode}.log"))
    set_seed(20261021)
    cfg = json.load(open(os.path.join(HERE, "config", "reinforcement.json")))
    only = set(filter(None, a.only.split(",")))
    t0 = time.time()
    if not a.skip_experiments:
        from tjplus.data.loaders import prefetch_all, load_mango_instruments
        from tjplus.data.meta import load_mango_meta, load_mango_inst_meta
        prefetch_all(raw_dir); load_mango_instruments(raw_dir); load_mango_meta(raw_dir); load_mango_inst_meta(raw_dir)
        for name, spec in cfg["experiments"].items():
            if only and name not in only:
                continue
            c = {k: v for k, v in spec.items() if k not in ("reps_full", "reps_quick", "dataset")}
            c["raw_dir"] = raw_dir
            c.setdefault("alphas", cfg["alphas"])
            c.setdefault("methods", cfg["classical_methods"])
            if a.mode == "quick":
                if "m_values" in c: c["m_values"] = c["m_values"][:2]
                if "designs" in c: c["designs"] = c["designs"][:2]
            reps = spec["reps_full"] if a.mode == "full" else spec["reps_quick"]
            run_experiment(name, spec["dataset"], c, reps, os.path.join(out, "raw"), a.jobs, log, a.rep_start, a.rep_end)
    if a.no_analysis:
        log.info(f"experiments finished in {time.time() - t0:.0f}s (analysis skipped)"); return
    from tjplus.statistics.reinforcement import analyse_reinforcement
    analyse_reinforcement(out, os.path.join(HERE, "..", "..", "Target_Journal_Submission", "results"), cfg, log)
    from tjplus.visualization.reinforcement_figures import make_reinforcement_figures
    make_reinforcement_figures(out, os.path.join(HERE, "..", "figures") if a.mode == "full" else os.path.join(out, "figures"))
    log.info(f"finished in {time.time() - t0:.0f}s; outputs in {out}")

if __name__ == "__main__":
    main()
