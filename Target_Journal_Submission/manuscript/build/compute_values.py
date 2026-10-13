"""Compute every number quoted in the manuscript from machine-generated result files -> values.json.
No number in the manuscript is typed by hand: placeholders {{key}} are filled from this file."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "results")
sys.path.insert(0, os.path.join(ROOT, "code", "src"))
CFG = json.load(open(os.path.join(ROOT, "code", "config", "experiments.json")))
PK = CFG["primary_kind"]
SRC_METHODS = ["ASTM-PI", "SCP-S", "WCP-S"]

def f3(x): return f"{x:.3f}"
def f2(x): return f"{x:.2f}"
def pct(x): return f"{100 * x:.0f}%"

def md_table(df, caption, label):
    """Pipe table with caption (pandoc 'Table:' syntax)."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join([":--"] + ["--:"] * (len(cols) - 1)) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines) + f"\n\nTable: {caption}\n"

def main():
    S = pd.read_csv(os.path.join(RES, "summary", "summary_all.csv"))
    S["source"] = S["source"].astype(str); S["target"] = S["target"].astype(str)
    a = CFG["primary_alpha"]
    E1 = S[S["experiment"].str.startswith("E1_main")]
    P = E1[(E1["alpha"] == a) & E1.apply(lambda r: r["kind"] == PK[r["dataset"]], axis=1)]
    V = {}
    scen = P[P["method"] == "TJ+N"]
    V["n_scen_main"] = len(scen)
    V["n_scen_corn"] = int((scen["dataset"] == "corn").sum()); V["n_scen_tablets"] = int((scen["dataset"] == "tablets").sum())
    V["n_scen_mango"] = int((scen["dataset"] == "mango").sum())
    src = P[P["method"].isin(SRC_METHODS)]
    V["min_cov_source"] = f2(src["coverage_mean"].min())
    V["n_under_source"] = int(src["under_covering"].sum()); V["n_source_cells"] = len(src)
    for ds in ("corn", "tablets", "mango"):
        d = src[src["dataset"] == ds]
        V[f"src_cov_range_{ds}"] = f"{d['coverage_mean'].min():.2f}–{d['coverage_mean'].max():.2f}"
        V[f"src_under_{ds}"] = f"{int(d['under_covering'].sum())}/{len(d)}"
    t = P[P["method"] == "TJ+N"]
    V["tjn_cov_main"] = f"{t['coverage_mean'].mean():.3f} (range {t['coverage_mean'].min():.3f}–{t['coverage_mean'].max():.3f})"
    V["tjn_cov_mean"] = f3(t["coverage_mean"].mean())
    V["tjn_n_under"] = int(t["under_covering"].sum())
    # smallest m from which TJ+N never under-covers (per data set, then overall statement)
    msg = []
    worst = 0
    for ds in ("corn", "tablets", "mango"):
        d = t[t["dataset"] == ds]
        ok_from = None
        for mm in sorted(d["m"].unique()):
            if not d[d["m"] >= mm]["under_covering"].any():
                ok_from = mm; break
        msg.append(f"{ds} {ok_from}")
        worst = max(worst, ok_from if ok_from is not None else 999)
    V["tjn_valid_m"] = worst if worst < 999 else "none"
    V["tjn_valid_m_by_ds"] = ", ".join(msg)
    sp = P[P["method"] == "SCP-T-split-N"]
    inf_small = sp[sp["frac_reps_any_inf"] > 0.5]
    V["split_inf_text"] = (f"the split-standards intervals were unbounded in {len(inf_small)} of {len(sp)} scenarios, all with m ≤ "
                           f"{int(inf_small['m'].max()) if len(inf_small) else 0}")
    for k, v in V.items():
        print(k, "=", v)
    json.dump({k: (int(v) if isinstance(v, (np.integer,)) else v) for k, v in V.items()}, open(os.path.join(HERE, "values.json"), "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
