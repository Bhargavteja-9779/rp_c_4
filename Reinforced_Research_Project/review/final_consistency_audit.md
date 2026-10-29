# Final reproducibility and manuscript-consistency audit (Phase 11)

Every item below was executed in this session on the final state of the branch. The machine-readable outputs are in `audit/data/consistency_checks.json` and `audit/data/e10_rerun_check.json`.

| Check | How | Result |
|---|---|---|
| Code executes | `python -m pytest tests -q` | 18 passed (`results/experiment_logs/pytest_final.txt`) |
| Pipeline runs end to end | `run_reinforcement.py --mode quick` | Completed |
| Pipeline runs in full | `run_reinforcement.py --mode full` (E10, E11, E14) | Completed, ≈3.5 h on 4 cores |
| Analyses regenerate from committed raw results | `run_reinforcement.py --skip-experiments` | Completed (≈1 min) |
| Re-run identity (deviation R3) | E10 re-run with unchanged seeds after the ANOVA-PI correction | All 12 other methods reproduced exactly (maximum absolute difference 0 on coverage, width and same-batch coverage, 538,200 rows); only ANOVA-PI changed |
| Raw-file integrity | SHA-256 of all raw files against `results/raw_results.csv` | 32 files (26 current, 6 superseded), 0 mismatches |
| Original study integrity | SHA-256 of 64 original raw files; regeneration of the 175 original manuscript values | 0 mismatches; 175/175 identical (see `audit/project_integrity_report.md`) |
| Every manuscript number generated | `values_reinforced.py` → `values.json`; build fails on any unfilled placeholder | 0 unfilled placeholders. A scan of the sources for literal numbers found only design constants, section and equation numbers, and data-set descriptors; result-like literals found earlier were replaced by generated values |
| Tables match results | Tables 1–5 and S1–S14 are generated from CSV/JSON results | Generated; Table 3–5 cells spot-checked against `E11_validity_by_dataset.csv`, `E10_summary.csv` and `E14_summary.csv` by an independent reviewer |
| Figures match results | Figs 3–6 and S1–S10 generated from result files; Fig. 1 and the graphical abstract are schematics (the graphical abstract plots E10 summary values) | Generated; provenance in `figures/README.md` |
| Figures referenced exist | Consistency script | 6 of 6 present |
| Table and figure numbering | Consistency script | 5 main tables and 6 main figures; no out-of-range references; all S1–S14 cited and present |
| Citations | Every cited key in the bibliography; new references fetched from DOI content negotiation (Crossref) or verified on arXiv | 0 missing. New items verified: Lee et al. 2026, Dunn et al. 2023, Bian & Barber 2023, Liang & Barber 2025, Mee 1984, Hubert et al. 2004, Haggam et al. 2026, Khairbek 2026, Duma et al. 2026, Chiappini et al. 2025, Davison & Hinkley 1997, Sun et al. 2026 (SSRN), Ainsworth 2016 (Hort Innovation report, ISBN checked on the PDF). "Accepted at ICML 2026" for Doula 2026 confirmed by the arXiv author comment. |
| Equations match code | Eq. (1) ↔ `transfer.Deployed`; Eq. (2)–(3) ↔ `methods.TransferFits`, `tj_plus`; Eq. (4) ↔ `DifficultyModel`; TJ+B ↔ `group.tj_plus_hier` (weights 1/((K+1)n_k), mass at ±∞); TJ+G ↔ `group.tj_plus_group`; ANOVA-PI ↔ `group.anova_pi` | Matched; unit tests cover ranks, singleton equivalence, unbounded behaviour and Monte Carlo validity |
| PDF rendering | `pdftotext` scan for broken glyphs; visual inspection of rendered pages | 0 broken glyphs in manuscript, cover letter and supplement. An equation-rendering defect present in the original submission PDF was found and fixed. |
| Journal formalities | Abstract ≤ 250 words, 3–5 highlights ≤ 85 characters, keywords, declarations (CRediT, competing interests, generative AI, data availability, funding) | Abstract 247 words; 5 highlights, maximum 81 characters; declarations present. Author names, affiliations, funding and repository URL are placeholders (author action). |
| Placeholders left intentionally | Scan of the DOCX | `[Author 1]`, `[Author 2]`, `[Affiliation…]`, e-mail, CRediT completion, funding, repository URL/DOI, suggested reviewers. No unintended placeholders. |
| Additional experiments documented | `research_design/revised_experimental_protocol.md` (E10–E14, deviations R1–R3); `code/config/reinforcement.json` | Present; the protocol was committed before the full runs (commit ac18a18) |
| Changes traceable | Git history of branch `claude/zen-ptolemy-3bpyvn` | Each step is a separate commit; the original package is untouched |
| Software versions | `results/experiment_logs/software_versions.txt` | Python 3.13.16, NumPy 2.5.3, SciPy 1.18.1, scikit-learn 1.9.1, pandas 3.0.5, Matplotlib 3.11.2 |

## Not re-executed in this cycle

- **Original experiments E1–E9.** The full re-execution takes ≈4–5 CPU-h and was not repeated. Their raw results were verified by hash, and all values derived from them were regenerated identically.
- **Bootstrap competitor with B ≥ 1000.** It was not run (≈15 CPU-h). The limitation is stated in the manuscript.
