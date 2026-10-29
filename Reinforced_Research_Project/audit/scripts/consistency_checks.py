"""Automated manuscript/result consistency checks for the reinforced package (Phase 11).
Usage: python consistency_checks.py  -> prints a Markdown report and writes audit/data/consistency_checks.json"""
import csv, glob, hashlib, json, os, re, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
B = os.path.join(ROOT, "manuscript", "build")

def pdftext(p):
    return subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout

def main():
    out = {}
    md = open(os.path.join(B, "manuscript_filled.md"), encoding="utf-8").read()
    out["unfilled_placeholders"] = len(re.findall(r"\{\{\w+\}\}|\[\[\w+\]\]", md))
    figs = re.findall(r"\]\((figures/[^)]+)\)", md)
    out["figures_referenced"] = len(figs)
    out["figures_missing"] = [f for f in figs if not os.path.exists(os.path.join(ROOT, f))]
    cites = set(re.findall(r"@([A-Za-z0-9_]+)", md))
    bib = {r["id"] for r in json.load(open(os.path.join(B, "references.json")))}
    out["citations_missing_in_bib"] = sorted(c for c in cites if c not in bib)
    out["bib_entries_uncited"] = sorted(bib - cites)
    s_tabs = sorted({int(x) for x in re.findall(r"Supplementary Table S(\d+)", md)})
    supp = open(os.path.join(B, "supplementary_filled.md"), encoding="utf-8").read()
    have_tabs = sorted({int(x) for x in re.findall(r"# Table S(\d+)\.", supp)})
    out["supp_tables_cited"] = s_tabs; out["supp_tables_present"] = have_tabs
    out["supp_tables_cited_but_missing"] = [t for t in s_tabs if t not in have_tabs]
    tabs = re.findall(r"Table: \*\*Table (\d+)\.\*\*", md)
    out["main_tables"] = len(tabs)
    out["main_table_refs_out_of_range"] = sorted({int(x) for x in re.findall(r"\bTable (\d+)\b", md) if int(x) > len(tabs)})
    nfig = len(re.findall(r"!\[\*\*Fig\. \d+\.", md))
    out["main_figures"] = nfig
    out["main_fig_refs_out_of_range"] = sorted({int(x) for x in re.findall(r"\bFig\. (\d+)\b", md) if int(x) > nfig})
    for name in ("Revised_Manuscript.pdf", "Revised_Cover_Letter.pdf"):
        t = pdftext(os.path.join(ROOT, "manuscript", name))
        out[f"broken_glyphs_{name}"] = t.count("¿")
    t = pdftext(os.path.join(ROOT, "supplementary", "Supplementary_Material.pdf"))
    out["broken_glyphs_supplement"] = t.count("¿")
    a = md[md.index("**Background:**"): md.index("**Keywords:**")]
    out["abstract_words"] = len(re.sub(r"\*\*", "", a).split())
    hl = open(os.path.join(ROOT, "manuscript", "Highlights.txt"), encoding="utf-8").read().strip().splitlines()
    out["highlights"] = len(hl); out["highlight_max_chars"] = max(len(h.lstrip("- ").strip()) for h in hl)
    bad = 0; n = 0
    for r in csv.DictReader(open(os.path.join(ROOT, "results", "raw_results.csv"))):
        n += 1
        if hashlib.sha256(open(os.path.join(ROOT, "results", r["file"]), "rb").read()).hexdigest() != r["sha256"]:
            bad += 1
    out["raw_files_checked"] = n; out["raw_hash_mismatches"] = bad
    body = md[md.index("# 1. Introduction"): md.index("# Declarations")]
    out["main_text_words"] = len(body.split())
    json.dump(out, open(os.path.join(ROOT, "audit", "data", "consistency_checks.json"), "w"), indent=1)
    for k, v in out.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()
