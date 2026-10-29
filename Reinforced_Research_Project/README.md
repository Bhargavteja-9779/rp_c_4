# Reinforced research project: trustworthy prediction intervals after calibration transfer

This folder is the second, more demanding research cycle on the project in `../Target_Journal_Submission/`. That earlier package is left untouched as the record of the first submission version, and its raw results are reused here, with checksums re-verified.

**Revised title:** *Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season: how many reference samples, and from how many batches?*

**Target journal:** *Analytica Chimica Acta*, retained after reinforcement. See `audit/journal_fit_assessment.md`.

## Contents

| Path | What it contains |
|---|---|
| `submission_readiness_report.md` | Final report and decision |
| `audit/project_integrity_report.md` | Phase 1 forensics: every component verified, status per component |
| `audit/rejection_risk_register.md` | Rejection board (10 roles) and risk register R01–R16 |
| `audit/novelty_reassessment.md` | Independent assessment (Phase 2) and novelty stress test (Phase 4) |
| `audit/journal_fit_assessment.md` | Refreshed timing measurements and journal decision |
| `audit/scripts/`, `audit/data/` | PubMed and Crossref timing scripts with raw data; consistency-check script and output |
| `literature/updated_literature_matrix.csv`, `literature/competing_work_analysis.md` | Verified competing work, including the hierarchical jackknife+ prior art |
| `research_design/reinforcement_plan.md` | Weaknesses → changes, with the 12-field specification |
| `research_design/revised_experimental_protocol.md` | Protocol of E10–E14, written before the results, with deviation log R1–R2 |
| `code/` | Full code (original plus reinforcement modules), `run_all.py`, `run_reinforcement.py`, `config/`, `tests/` (18 tests), `README.md` |
| `results/raw/` | Per-repetition raw results of E10, E11 and E14 (26 files, about 1.0 M rows) |
| `results/raw_results.csv` | Index of the raw files with SHA-256 hashes |
| `results/summary/`, `results/statistics/`, `results/tables/` | Aggregates, tests and generated tables |
| `results/statistics.json`, `results/metrics.json` | Key numbers, machine-readable |
| `results/experiment_logs/` | Run logs, test output, software versions |
| `figures/` | New figures plus copies of the original figures used; `figures/README.md` gives provenance; `figures/submission/` holds files named by manuscript number |
| `tables/` | Generated tables used in the revised manuscript |
| `manuscript/` | `Revised_Manuscript.docx/.pdf`, `Revised_Cover_Letter.docx/.pdf`, `Highlights.txt`; sources in `src/`; build scripts in `build/` |
| `supplementary/` | `Supplementary_Material.docx/.pdf` (Tables S1–S14, Figs S1–S10) |
| `review/reinforcement_review.md` | Which hypotheses held and which did not |
| `review/second_adversarial_review.md` | Second review round on the revised manuscript, with resolutions |
| `review/final_consistency_audit.md` | Reproducibility and manuscript-consistency report |

## Reproduce

```bash
cd code
pip install -r requirements.txt
python -m pytest tests -q                                    # 18 tests
python run_reinforcement.py --skip-experiments               # re-analyse committed raw results (≈1 min)
python run_reinforcement.py --mode full                      # re-run E10–E14 (≈3–4 h on 4 cores)
cd ../manuscript/build
python values_reinforced.py && python build_revised.py && python build_supplementary_revised.py
python ../../audit/scripts/consistency_checks.py
```

The original experiments (E1–E9) are reproduced with `code/run_all.py`. Their committed raw results live in `../Target_Journal_Submission/results/`.
