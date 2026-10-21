"""Refresh of submission->acceptance times (PubMed publisher-deposited history dates) for journals
whose scope fits a chemometric uncertainty paper. Re-uses the measurement function of the original
office's script but (i) uses the most recent window, (ii) samples up to 500 articles, (iii) stores the
per-article intervals so that bootstrap confidence intervals of the share accepted within 72 days can
be computed.

Usage: python journal_timing_refresh.py out_dir
"""
import csv, json, os, random, statistics, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "Target_Journal_Submission",
                                "journal_selection", "scripts"))
import pubmed_acceptance_times as P

P.WINDOW = "2025/10/01:2026/10/20[dp]"
JOURNALS = {
    "Analytica Chimica Acta (Elsevier)": '"Anal Chim Acta"[ta]',
    "Talanta (Elsevier)": '"Talanta"[ta]',
    "Analytical Chemistry (ACS)": '"Anal Chem"[ta]',
    "Analyst (RSC)": '"Analyst"[ta]',
    "Analytical Methods (RSC)": '"Anal Methods"[ta]',
    "Anal Bioanal Chem (Springer)": '"Anal Bioanal Chem"[ta]',
    "Spectrochim Acta A (Elsevier)": '"Spectrochim Acta A Mol Biomol Spectrosc"[ta]',
    "Food Chemistry (Elsevier)": '"Food Chem"[ta]',
    "Food Research International (Elsevier)": '"Food Res Int"[ta]',
    "J Pharm Biomed Anal (Elsevier)": '"J Pharm Biomed Anal"[ta]',
    "Applied Spectroscopy (SAGE)": '"Appl Spectrosc"[ta]',
    "Postharvest Biol Technol (Elsevier)": '"Postharvest Biol Technol"[ta]',
    "Food Chemistry X (Elsevier)": '"Food Chem X"[ta]',
    "Microchemical Journal (Elsevier)": '"Microchem J"[ta]',
    "J Chemometrics (Wiley)": '"J Chemom"[ta]',
    "Chemometr Intell Lab Syst (Elsevier)": '"Chemometr Intell Lab Syst"[ta]',
}

def boot_ci(d, B=2000, seed=1):
    r = random.Random(seed); n = len(d); vals = []
    for _ in range(B):
        s = [d[r.randrange(n)] for _ in range(n)]
        vals.append(100 * sum(v <= 72 for v in s) / n)
    vals.sort(); return round(vals[int(0.025 * B)], 1), round(vals[int(0.975 * B)], 1)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    rows, raw = [], {}
    for name, q in JOURNALS.items():
        n_ids, d = P.measure(q, retmax=500)
        raw[name] = d
        row = dict(journal=name, sampled=n_ids, n_with_dates=len(d))
        if len(d) >= 20:
            qs = statistics.quantiles(d, n=4)
            lo, hi = boot_ci(d)
            row.update(median_days=statistics.median(d), q1=qs[0], q3=qs[2],
                       pct_le72=round(100 * sum(v <= 72 for v in d) / len(d), 1), pct_le72_ci=f"{lo}-{hi}",
                       p90_days=statistics.quantiles(d, n=10)[8])
        print(row, flush=True); rows.append(row)
    keys = ["journal", "sampled", "n_with_dates", "median_days", "q1", "q3", "pct_le72", "pct_le72_ci", "p90_days"]
    with open(os.path.join(out, "journal_timing_refresh.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    json.dump({"window": P.WINDOW, "days": raw}, open(os.path.join(out, "journal_timing_refresh_raw.json"), "w"))
