"""Submission->acceptance intervals from publisher-deposited Crossref 'assertion' history dates (received,
accepted), for journals whose publishers do not deposit history dates in PubMed (e.g. Wiley, RSC, SAGE).
Elsevier does not deposit these assertions in Crossref (checked), so Elsevier journals are measured via PubMed.

Usage: python crossref_timing.py out_dir
"""
import csv, json, os, random, statistics, sys, time, urllib.parse, urllib.request
from datetime import date

JOURNALS = {  # name -> ISSN (electronic)
    "J Chemometrics (Wiley)": "1099-128X",
    "Analyst (RSC)": "1364-5528",
    "Analytical Methods (RSC)": "1759-9679",
    "Applied Spectroscopy (SAGE)": "1943-3530",
    "J Near Infrared Spectrosc (SAGE)": "1751-6552",
    "Journal of Raman Spectroscopy (Wiley)": "1097-4555",
}
FROM, UNTIL = "2025-10-01", "2026-10-20"

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "journal-timing-audit/1.0 (mailto:research-audit@example.org)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(2 ** (i + 1))
    raise RuntimeError(url)

def d(s):
    try:
        y, m, dd = map(int, s[:10].split("-")); return date(y, m, dd)
    except Exception:
        return None

def measure(issn, n_max=500):
    days, cursor, seen = [], "*", 0
    while seen < 2000 and len(days) < n_max:
        q = urllib.parse.urlencode({"filter": f"from-pub-date:{FROM},until-pub-date:{UNTIL},type:journal-article",
                                    "rows": 200, "cursor": cursor, "select": "DOI,assertion,title"})
        m = get(f"https://api.crossref.org/journals/{issn}/works?{q}")["message"]
        items = m["items"]
        if not items:
            break
        for it in items:
            seen += 1
            a = {x.get("name"): x.get("value") for x in it.get("assertion", []) if isinstance(x.get("value"), str)}
            r, acc = d(a.get("received", "")), d(a.get("accepted", ""))
            if r and acc and acc >= r:
                days.append((acc - r).days)
        cursor = m.get("next-cursor")
        time.sleep(0.5)
    return seen, days[:n_max]

def boot(dd, B=2000, seed=1):
    rr = random.Random(seed); n = len(dd); v = []
    for _ in range(B):
        s = [dd[rr.randrange(n)] for _ in range(n)]
        v.append(100 * sum(x <= 72 for x in s) / n)
    v.sort(); return round(v[int(.025 * B)], 1), round(v[int(.975 * B)], 1)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    rows, raw = [], {}
    for name, issn in JOURNALS.items():
        try:
            seen, dd = measure(issn)
        except Exception as e:
            print(name, "failed", e); continue
        raw[name] = dd
        row = dict(journal=name, records_scanned=seen, n_with_dates=len(dd))
        if len(dd) >= 20:
            qs = statistics.quantiles(dd, n=4); lo, hi = boot(dd)
            row.update(median_days=statistics.median(dd), q1=qs[0], q3=qs[2],
                       pct_le72=round(100 * sum(x <= 72 for x in dd) / len(dd), 1), pct_le72_ci=f"{lo}-{hi}")
        print(row, flush=True); rows.append(row)
    keys = ["journal", "records_scanned", "n_with_dates", "median_days", "q1", "q3", "pct_le72", "pct_le72_ci"]
    with open(os.path.join(out, "crossref_timing.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    json.dump({"window": [FROM, UNTIL], "days": raw}, open(os.path.join(out, "crossref_timing_raw.json"), "w"))
