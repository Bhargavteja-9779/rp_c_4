"""Parallel execution of experiment configurations -> raw CSV results."""
import os, time
from multiprocessing import get_context
import pandas as pd

def _init():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[v] = "1"
    try:
        from threadpoolctl import threadpool_limits
        threadpool_limits(1)
    except Exception:
        pass

def _work(args):
    dataset, rep, cfg = args
    from .datasets import run_corn_rep, run_fixed_rep, run_mango_inst_rep
    if dataset == "corn":
        return run_corn_rep(rep, cfg)
    if dataset == "mango_inst":
        return run_mango_inst_rep(rep, cfg)
    if dataset == "mango_batch":
        from .batch import run_batch_rep
        return run_batch_rep(rep, cfg)
    return run_fixed_rep(dataset, rep, cfg)

def run_experiment(name, dataset, cfg, reps, out_dir, n_jobs, log=None, rep_start=0, rep_end=None):
    """Runs repetitions [rep_start, rep_end) (default: all). A partial range is written as
    <name>@r<start>-<end>.csv.gz; the analysis merges chunks (seeds depend only on the repetition index)."""
    os.makedirs(out_dir, exist_ok=True)
    rep_end = reps if rep_end is None else min(rep_end, reps)
    tag = "" if (rep_start == 0 and rep_end == reps) else f"@r{rep_start:04d}-{rep_end:04d}"
    out = os.path.join(out_dir, f"{name}{tag}.csv.gz")
    if rep_start >= rep_end:
        return None
    if os.path.exists(out):
        if log: log.info(f"[{name}{tag}] exists, skipped")
        return None
    t0 = time.time()
    tasks = [(dataset, r, cfg) for r in range(rep_start, rep_end)]
    reps = len(tasks)
    rows, samples = [], []
    if n_jobs > 1:
        with get_context("fork").Pool(n_jobs, initializer=_init) as pool:
            for i, (r, s) in enumerate(pool.imap_unordered(_work, tasks, chunksize=1)):
                rows += r; samples += s
                if log and (i + 1) % max(1, reps // 10) == 0:
                    log.info(f"[{name}] {i + 1}/{reps} reps ({time.time() - t0:.0f}s)")
    else:
        for t in tasks:
            r, s = _work(t); rows += r; samples += s
    df = pd.DataFrame(rows)
    df = df.sort_values([c for c in ["rep", "setting", "property", "target", "design", "K", "m", "kind", "alpha", "method"]
                         if c in df.columns], kind="stable")
    df.to_csv(out, index=False, float_format="%.6g")
    if samples:
        pd.DataFrame(samples).to_csv(os.path.join(out_dir, f"{name}{tag}_samples.csv.gz"), index=False)
    if log:
        log.info(f"[{name}] done: {len(df)} rows in {time.time() - t0:.0f}s -> {out}")
    return df
