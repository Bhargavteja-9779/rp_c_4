"""End-to-end check of the browser tool against the Python package: loads the page in Chromium, enters a fixed
data set, runs every interval rule and compares the table with tjplus.api.SBCIntervals.
Usage: python check_tool_e2e.py   (needs playwright and a Chromium build)"""
import os, sys
import numpy as np
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code", "src"))
from tjplus.api import SBCIntervals

def main():
    rng = np.random.default_rng(1)
    f = np.round(rng.normal(15, 2, 20), 2); y = np.round(f + 0.4 + np.repeat(rng.normal(0, .6, 10), 2) + rng.normal(0, .4, 20), 2)
    g = np.repeat(np.arange(10), 2); fn = np.array([13.0, 15.0, 17.0])
    std = "prediction,reference,batch\n" + "\n".join(f"{a},{b},B{c}" for a, b, c in zip(f, y, g))
    new = "prediction\n" + "\n".join(str(v) for v in fn)
    html = open(os.path.join(HERE, "transfer_interval_tool.html")).read()
    page_html = "<!doctype html><html><head><meta charset='utf-8'></head><body>" + html + "</body></html>"
    worst = 0.0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium") if os.path.exists("/opt/pw-browsers/chromium") else None)
        page = b.new_page(); page.set_content(page_html)
        for unit, rule, js_rule in (("sample", "jackknife+", "jk"), ("batch", "jackknife+", "jk"), ("sample", "gauss", "gauss"),
                                    ("batch", "gauss", "gauss"), ("batch", "anova", "anova")):
            page.fill("#std", std); page.fill("#new", new); page.fill("#thr", "")
            page.select_option("#unit", unit); page.select_option("#rule", js_rule); page.select_option("#ca", "0.1")
            page.click("#run")
            rows = page.eval_on_selector_all("#ctab tbody tr", "rs => rs.map(r => [...r.children].map(c => c.textContent))")
            yh, lo, hi = SBCIntervals(0.1, unit, rule).fit(f, y, batch=g if unit == "batch" else None).predict(fn)
            for r, a_, b_, c_ in zip(rows, yh, lo, hi):
                d = max(abs(float(r[2]) - a_), abs(float(r[3]) - b_), abs(float(r[4]) - c_))
                worst = max(worst, d)
            print(f"{unit:6s} {rule:10s} max abs difference {max(abs(float(r[3]) - l) for r, l in zip(rows, lo)):.3f}")
        b.close()
    print(f"worst difference over all rules: {worst:.3f} (table shows 2 decimals)")
    assert worst <= 0.006

if __name__ == "__main__":
    main()
