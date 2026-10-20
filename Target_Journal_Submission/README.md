# Submission package: transfer jackknife+ for transferred NIR calibrations

**Title:** Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+

**Target journal:** *Analytica Chimica Acta* (Elsevier; Research Paper). The journal was chosen from primary PubMed history dates: median submission→acceptance 58 days (IQR 43–77), with 70.3% of accepted papers within 72 days (n = 300). The JIF of about 6.1 comes from secondary sources, because JCR could not be accessed directly. See `journal_selection/`.

## Manifest

| Path | Content |
|---|---|
| `journal_selection/` | `selected_journal.md`, `journal_comparison.md`, `journal_verification.md`, PubMed timing data and script |
| `research_design/` | Topic selection, pre-registration, deviation log (12 entries) |
| `literature/` | Verified references, abstracts, literature matrix and novelty map |
| `manuscript/` | `Final_Manuscript.docx/.pdf`, `cover_letter.docx/.pdf`, `Highlights.txt`; sources in `src/` and `src_cover/`; build scripts in `build/` |
| `supplementary/` | `Supplementary_Material.docx/.pdf` (Tables S1–S10, Figs S1–S3) |
| `figures/` | All generated figures; `submission/` holds the files named by manuscript number (Fig1–Fig9, FigS1–FigS3, GraphicalAbstract) |
| `tables/` | Generated tables (CSV/Markdown) |
| `code/` | Package `src/tjplus`, `run_all.py --mode quick\|full`, `config/`, `experiments/`, `scripts/`, `tests/`, `requirements.txt`, `environment.yml`, `README.md` |
| `results/` | `raw/` (per-repetition results), `raw_results.csv` (index with SHA-256), `metrics.json`, `statistics.json`, `summary/`, `statistics/`, `experiment_logs/` |
| `REVIEW/` | `review_01.md`–`review_10.md`, `final_audit.md`, `rejection_risk_report.md` |

## Reproduction

```bash
cd code
pip install -r requirements.txt
pytest tests                                   # 11 tests
python run_all.py --mode quick                 # about 5 min, downloads and verifies the data
python run_all.py --mode full --skip-experiments   # rebuild statistics, tables and figures from committed raw results
python ../manuscript/build/compute_values.py && python ../manuscript/build/build_manuscript.py
```

A full re-run of all experiments takes about 4–5 CPU-hours on 4 cores and can be run in resumable chunks with `--rep-start/--rep-end`.

## Main findings (all generated from `results/`)

- **Problem.** After transfer, source-calibrated intervals (ASTM-PI, split conformal, weighted conformal) under-covered in 72/72 corn, 12/12 mango and 11/36 tablet scenarios, with coverage as low as 0.03 for nominal 0.90.
- **Method.** TJ+N had a mean coverage of 0.922 and was never flagged as under-covering:
  - 40 primary scenarios;
  - 152 pipeline × scenario combinations;
  - 528 cells over all α levels;
  - the independent handheld-instrument test (E8, 0/72);
  - PLS, ridge and 1D-CNN models (0/22).
- **Efficiency.** Splitting the standards gave unbounded intervals in 20 of 40 scenarios (all with m ≤ 15). Where both methods were bounded, TJ+N was narrower in 20/20.
- **Honest limits.**
  - At 90% the Gaussian LOO interval is as efficient (Friedman rank 2.17 vs 2.52, p = 0.11), but it under-covers at 95% (14/40).
  - The normalised Gaussian is about 3% narrower but under-covers in 14/192 scenarios.
  - Spectral drift after standardisation defeats all methods. Even at ±0.25 channel, TJ+N under-covered in 4/12 scenarios.
  - The label-free variant is unreliable (20/36 under-covering).
- **Novelty.** The inference engine is jackknife+ (Barber et al. 2021). The contribution is its instantiation for the transfer step, together with the validated chemometric benchmark and practical rules. This is stated explicitly in the manuscript.

## Final decision (Phase 42)

**READY FOR SUBMISSION**, once the authors complete the items that cannot be generated:

1. Author names, affiliations, corresponding-author details, CRediT roles and funding (placeholders in the title page and cover letter).
2. A public repository URL or archive DOI (e.g. Zenodo) for the code and results, inserted in the data-availability statement.
3. A review of the generative-AI declaration, the date and the suggested reviewers in the cover letter.
4. A check of the current ACA guide for authors at submission time (word limits, figure formats).

Residual risks are listed in `REVIEW/rejection_risk_report.md`. The dominant ones are perceived novelty and the 72-day acceptance target: about 30% of accepted ACA papers take longer, and a major revision would very likely exceed 72 days.
