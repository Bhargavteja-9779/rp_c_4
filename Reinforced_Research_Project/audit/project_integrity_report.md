# Project integrity report (Phase 1: takeover forensics)

**Scope.** This report covers the complete original project in `Target_Journal_Submission/`, at commit 8363f05 on branch `claude/zen-ptolemy-3bpyvn`, inspected on 2026-10-21. Every check below was executed in this session. The original tree was not modified: a value-regeneration run rewrote one generated file, and its content was byte-identical.

**Status codes.**

| Code | Meaning |
|---|---|
| VERIFIED | Checked directly, result as claimed |
| PARTIALLY VERIFIED | Main claim checked, part of it could not be |
| UNVERIFIED | Could not be checked |
| FAILED | Checked and found wrong |
| NOT AVAILABLE | Artifact does not exist |

| Component | Available artifacts | Verification method (this session) | Status | Deficiencies identified | Scientific importance | Required action |
|---|---|---|---|---|---|---|
| Final manuscript | `manuscript/Final_Manuscript.docx/.pdf` (44 pp., 9,138 words in DOCX body), sources `manuscript/src/*.md`, filled `build/manuscript_filled.md` | Read in full; placeholder scan of the DOCX; page count via `pdfinfo` | VERIFIED (exists, complete) | Placeholders remain only for authors and affiliations (intended). The text claims "never under-covered" as a headline, although under the study's own random-standards design this is guaranteed by theory (see novelty reassessment). No experiment addresses batch-structured standards. | High | Rebuild around the strongest defensible contribution (Phase 9) |
| Earlier manuscript versions | git history (commits 7a451ba → 8363f05) | `git log` | VERIFIED | — | Low | None |
| Journal selection | `journal_selection/*.md`, PubMed CSVs, script | Script re-run with a fresh window (2025-10-01 to 2026-10-20, n = 500 per journal): `audit/data/journal_timing_refresh.csv` | VERIFIED (timing) / UNVERIFIED (JIF, quartile) | ACA: median 59 d, 67.8% ≤ 72 d (95% CI 63.6–72.0). The original 70.3% (n = 300) is consistent. JIF/quartile still come from aggregators: JCR is not reachable. The official guide for authors returns HTTP 403. | Medium | Re-assess in `journal_fit_assessment.md` |
| Literature review / novelty map | `literature/literature_matrix.md`, `references_verified.json`, `abstracts.json` | New targeted prior-art search (Crossref/arXiv-verified) | PARTIALLY VERIFIED | **Missed prior art:** (i) hierarchical jackknife+ (Lee, Barber & Willett 2026), directly relevant to batch-structured standards; (ii) Duma et al. is now published in CILS 2026 (the manuscript cites the arXiv version); (iii) the Sun, Cui & Qiao 2026 SSRN preprint on CV+ for NIR; (iv) the Haggam et al. 2026 CILS review naming "uncertainty-aware validation schemes" as a gap; (v) the Khairbek 2026 empirical conformal coverage loss under spectral shift; (vi) Chiappini et al. 2025 ACA bootstrap uncertainty; (vii) training-conditional results (Bian & Barber 2023; Liang & Barber 2025); (viii) β-expectation tolerance intervals = prediction intervals (Rozet et al. 2012; Mee 1984). No paper was found that provides coverage-valid regression intervals after calibration transfer. | High | Updated matrix and competing-work analysis |
| Research gap | Manuscript §1, matrix | Re-derived independently | PARTIALLY VERIFIED | The gap (interval validity after transfer) is real per the search. The **method** gap is thin: jackknife+ applied to a symmetric algorithm. | High | Reformulate the contribution (Path A + B) |
| Pre-registration / protocol | `research_design/preregistration.md`, `deviations.md` (12 entries) | Read; compared with config | VERIFIED | Post-hoc experiments (E8, E9, E4b) are labelled as such | Medium | Continue the deviation log |
| Source code | `code/src/tjplus` (≈1,900 lines), `run_all.py` | Line-by-line reading of `datasets.py`, `methods.py`, `core.py`, `transfer.py`, `source_model.py`, `loaders.py` | VERIFIED | No defect found in the interval constructions: jackknife+ ranks are correct; the LOO fits use only the other standards. Minor: WCP-S uses the unlabelled target pool including test spectra (transductive; disclosed). | High | Reuse, extended |
| Leakage audit | Code + data | Checked: (1) corn train/cal/pool from disjoint index ranges of one permutation; (2) tablets source = calibrate/validate sets (instrument 1), target = test set (instrument 2); (3) mango season: source seasons 1–3, target season 4, with replicate scans averaged per fruit (key includes DM); (4) E8 source fruit restricted to fruit **not** measured on the target instrument (`present[src] & ~present[tgt]`); (5) σ, preprocessing and LV number fitted on source training data only (`fit_source_model`, `build_sigmas`); (6) standards never in the test set (`_std_test` returns complementary permutation slices). New unit tests for the batch designs. | VERIFIED: **no leakage found** | A *structural* issue was found instead: standards and test samples are drawn at random from the same pool, so exchangeability holds by construction. Batches, lots and harvest dates are ignored, although the mango data contain them (18 season-4 populations; 29–49 populations per instrument pair). | **Critical** (external validity) | New experiment E10 |
| Configuration files | `code/config/experiments.json` | Read | VERIFIED | — | — | — |
| Dataset documentation | Manuscript §3.1, `results/README.md`, SHA-pinned sources in `loaders.py` | Re-loaded mango and metadata; checked fruit counts (4,677; season 4: 725) | VERIFIED | Batch metadata (population, date) not documented or used | Medium | Document in revised protocol |
| Raw outputs | `results/raw/` (64 files), `raw_results.csv` index with SHA-256 | **Recomputed all 64 SHA-256 hashes** | VERIFIED (64/64 match) | — | High | — |
| Processed results / statistics | `results/summary`, `statistics/`, `metrics.json`, `statistics.json` | Indirect: value regeneration (next row) | VERIFIED | The under-coverage flag is an absence-of-evidence criterion; there is no positive (non-inferiority) evidence; scenario dependence is handled only descriptively | Medium | E13 re-analysis |
| Manuscript numbers | `manuscript/build/values.json` (175 values), `compute_values.py` | **Re-ran `compute_values.py` on the committed raw results: 175/175 values identical** | VERIFIED | — | High | Same mechanism in the revised build |
| Training logs | `results/experiment_logs/`, `E5_cnn_training_history.csv` | Listed | VERIFIED (exist) | — | Low | — |
| Predictions | `*_samples.csv.gz` (per-sample intervals, first 100 reps) | Listed in the index; hashes match | VERIFIED | — | Low | — |
| Figures | `figures/` (26 in `submission/`) | Generated by `visualization/figures.py` from results | PARTIALLY VERIFIED (generation path read; not re-rendered) | — | Medium | Regenerated in the reinforced package |
| Tables | `tables/` | Generated from CSV | VERIFIED via value regeneration | — | Medium | — |
| Supplementary material | `supplementary/Supplementary_Material.docx/.pdf` | Exists | VERIFIED (exists) | — | Low | Update |
| Existing reviewer reports | `REVIEW/review_01–10.md`, `final_audit.md`, `rejection_risk_report.md` | Read | VERIFIED (exist) | The ten rounds were simulated by the same agent. They found and fixed real errors (LV bug, wrong claims), but **none questioned the random-standards design**, which is the main external-validity weakness. | Medium | Independent board (this cycle) |
| Reproducibility documentation | `code/README.md`, `run_all.py`, fresh-clone audit | Tests re-run: the original 11 pass. A quick-mode run was not repeated, but the same pipeline ran in quick mode for the reinforcement code. | VERIFIED (tests) / PARTIALLY VERIFIED (end-to-end) | Full re-execution (≈4–5 CPU-h) was not repeated in this session | Medium | Document honestly |
| Cover letter | `manuscript/cover_letter.docx/.pdf` | Read source | VERIFIED | Claims "to our knowledge … not been studied systematically before": consistent with the new search, but it must cite the closest adjacent work | Low | Rewrite |
| Journal author guidelines | Only a secondary "indexed snapshot" in `selected_journal.md` | Official Elsevier guide page: HTTP 403 (twice) | UNVERIFIED | Abstract/highlight limits cannot be re-confirmed from the primary source | Medium | Must be re-checked by the authors at submission |

## Summary of the forensics

1. **Integrity is good.** Results are checksum-verified, the manuscript numbers regenerate exactly, the code is correct as far as inspected, and no data leakage was found.
2. **The decisive weaknesses are scientific, not technical:**
   - **(a)** The headline result ("never under-covers") is a theorem-guaranteed consequence of the evaluation design, in which standards and test samples are exchangeable by construction.
   - **(b)** The realistic deployment condition was never tested: standards from a few lots, routine samples from new lots, although the data contain this structure.
   - **(c)** Classical competitors that an analytical chemist would use were missing: the OLS prediction interval for SBC, bootstrap intervals, and random-effects (multi-batch) intervals.
   - **(d)** A closely related statistical construction (hierarchical jackknife+) was not cited.
3. These are addressed by experiments E10–E13 (`research_design/revised_experimental_protocol.md`).
