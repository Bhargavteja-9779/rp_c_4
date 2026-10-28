"""Assemble the revised manuscript and cover letter: Markdown parts + values.json -> DOCX (pandoc, Word equations,
Elsevier numeric references) -> PDF (LibreOffice). Fails if any {{placeholder}} has no value.

Usage: python values_reinforced.py && python build_revised.py
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "..", "src")
OUT = os.path.join(ROOT, "manuscript")
sys.path.insert(0, HERE)

def fill(text, vals):
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", text)) - set(vals))
    if missing:
        sys.exit(f"Missing values for placeholders: {missing}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(vals[m.group(1)]), text)

def loosen_lists(text):
    out = []
    for ln in text.split("\n"):
        if re.match(r"^(\s*)(- |\d+\. )", ln) and out and out[-1].strip() != "":
            out.append("")
        out.append(ln)
    return "\n".join(out)

def to_pdf(docx):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(docx), docx],
                   check=True, capture_output=True)

def main():
    vals = json.load(open(os.path.join(HERE, "values.json")))
    parts = sorted(f for f in os.listdir(SRC) if f.startswith("part") and f.endswith(".md"))
    text = fill("\n\n".join(open(os.path.join(SRC, f), encoding="utf-8").read() for f in parts), vals)
    k = [0]
    def _num(m):
        k[0] += 1
        return f"Table: **Table {k[0]}.** "
    text = re.sub(r"^Table: ", _num, text, flags=re.M)
    text = loosen_lists(text)
    md = os.path.join(HERE, "manuscript_filled.md"); open(md, "w", encoding="utf-8").write(text)
    docx = os.path.join(OUT, "Revised_Manuscript.docx")
    subprocess.run(["pandoc", md, "-o", docx, "--citeproc", "--bibliography", os.path.join(HERE, "references.json"),
                    "--csl", os.path.join(HERE, "elsevier-with-titles.csl"), "--reference-doc", os.path.join(HERE, "reference.docx"),
                    "--resource-path", ROOT, "-M", "link-citations=false", "-M", "reference-section-title=References"],
                   check=True, cwd=ROOT)
    from postprocess_docx import postprocess
    postprocess(docx); to_pdf(docx)
    print("built", docx)
    cl = loosen_lists(fill(open(os.path.join(HERE, "..", "src_cover", "cover_letter.md"), encoding="utf-8").read(), vals))
    clmd = os.path.join(HERE, "cover_letter_filled.md"); open(clmd, "w", encoding="utf-8").write(cl)
    cl_docx = os.path.join(OUT, "Revised_Cover_Letter.docx")
    subprocess.run(["pandoc", clmd, "-o", cl_docx, "--reference-doc", os.path.join(HERE, "reference_letter.docx")], check=True)
    to_pdf(cl_docx)
    print("built", cl_docx)
    hl = os.path.join(HERE, "..", "src_cover", "highlights.md")
    if os.path.exists(hl):
        h = fill(open(hl, encoding="utf-8").read(), vals)
        open(os.path.join(OUT, "Highlights.txt"), "w", encoding="utf-8").write(h)
        for line in h.strip().splitlines():
            if len(line.lstrip("- ").strip()) > 85:
                sys.exit(f"Highlight longer than 85 characters: {line}")
    figs = {"Fig1": "fig1_overview", "Fig2": "fig2_datasets", "Fig3": "fig3_coverage_vs_m", "Fig4": "fig_batch_coverage",
            "Fig5": "fig_application", "Fig6": "fig6_robustness", "GraphicalAbstract": "graphical_abstract_revised"}
    sub = os.path.join(ROOT, "figures", "submission"); os.makedirs(sub, exist_ok=True)
    for new, old in figs.items():
        for ext in (".png", ".pdf"):
            p = os.path.join(ROOT, "figures", old + ext)
            if os.path.exists(p):
                shutil.copyfile(p, os.path.join(sub, new + ext))
    print("submission figures written")

if __name__ == "__main__":
    main()
