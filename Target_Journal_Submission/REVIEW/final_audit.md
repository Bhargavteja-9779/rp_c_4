# Final audit (Phases 22, 23, 34, 35)

## 1. Claim → evidence map (Phase 22)
| Claim (where) | Evidence (value) | Experiment | Table/Figure | Citation |
|---|---|---|---|---|
| Source-calibrated intervals under-cover after transfer; coverage as low as 0.03 (Abstract, §4.2) | ASTM-PI/SCP-S/WCP-S under-covering in 72 of 72 (corn), 12 of 12 (mango), 11 of 36 (tablets) cells | E1 | Table 3, Fig. 3 | — |
| The failure is not due to the in-sample SEC (§4.2) | SCP-S (out-of-fold residuals) corn coverage 0.03–0.74 | E1 | Table 3 | — |
| TJ+N mean coverage 0.922, never flagged in the primary scenarios (Abstract, §4.3) | 40 scenarios; CI half-widths corn ±0.008, mango ±0.007, tablets ±0.005 | E1 | Table 3, Fig. 3 | — |
| …at α = 0.05/0.10/0.20 and for four pipelines (Abstract) | 0 of 152 under-covering pipeline × scenario combinations at α = 0.10; 0 over three α (primary); all E1 cells 0 of 528 | E1 | Table 4, Table S2 | — |
| …with PLS, ridge, 1D-CNN, independent instruments (Abstract, §4.6) | 0/22 (E5); E8 0/72 | E5, E8 | Tables 6, 7 | — |
| Splitting standards gives unbounded intervals for m ≤ 15 (Abstract, §4.3) | 20 of 40 scenarios, all with m ≤ 15 | E1 | Table 3 | — |
| TJ+N beats the split baseline where both are bounded (§4.3) | 20/20 scenarios, rank-biserial -0.52 | E1 | Table S5 | Holm 1979 |
| Gauss-LOO similarly efficient at 90% (Abstract, §4.3) | Friedman ranks Gauss 2.17, TJ+N 2.52; Holm p = 0.11 | E1 | Fig. S2 | Demšar 2006 |
| Gauss-LOO under-covers at 95% (Abstract) | 14 of 40 scenarios | E1 | Table 4 | — |
| Normalised Gaussian is ≈3% more efficient but invalid in some scenarios (§4.3) | Gauss-LOO-N 14/192 vs TJ+N 0/192 | E9 | Table S8 | — |
| Leave-one-out re-fitting is essential (§4.4) | TJ-insample-N under-covering 14 (primary), 199 of 528 (all cells) | E1, E8 | Table 5, Fig. 5 | — |
| Normalisation improves efficiency and conditional coverage in most scenarios (§4.4) | Better/worse than TJ+ in 24/5; high-σ tertile coverage 0.878 → 0.933 | E1 | Table 5, Fig. 6 | Papadopoulos 2011 |
| Kennard–Stone standards → conservative (§4.5) | TJ+N 0.93–0.96 | E4 | Fig. 7, Table S9 | Kennard & Stone 1969 |
| Drift after standardisation defeats all methods, even ¼ channel (Abstract, §4.5) | ±1 channel: TJ+N tablets 0.04–0.07; ±0.25: TJ+N corn 0.84–0.96, tablets 0.59–0.62, mango 0.86–0.96 (4/12 under) | E4, E4b | Fig. 7, Tables S9, S10 | — |
| Label-free variant unreliable (§4.7) | 20/36 under-covering | E1 | Table 3 | Doula 2026 |
| Cost: seconds or less (Abstract, §4.10) | 0.15 s, 2.79 s, 0.06 s; scaling corn: 0.10 s at m = 10 to 0.15 s at m = 20; tablets: 0.80 s at m = 10 to 2.56 s at m = 50; mango: 0.02 s at m = 10 to 0.06 s at m = 50 | E6, E6b | Fig. S3, Tables S4, S7 | — |
| Coverage ≥ 1−2α under exchangeability (Prop. 1) | Proof (Appendix A); unit-test Monte Carlo | — | — | Barber et al. 2021 |

Claims that were weakened or rewritten during the reviews:
- "whenever the transfer added error" → "when … substantial error";
- "under-coverage mainly for assay" → split into the assay at m = 10 and marginal under-coverage for weight;
- "normalisation helped only partly" → quantified (24 better / 5 worse);
- E8 "source intervals under-covered in every scenario" → WCP-S unbounded under SBC;
- "ASTM-PI fell to 0.78" removed after the LV bug fix;
- "valid whenever its assumptions held" retained (all failures occurred under drift, which violates the assumptions);
- the abstract no longer claims validity for m ≥ 10 (which was vacuous).

## 2. Citation audit (Phase 23)
- Every journal reference was verified against Crossref (authors, title, year, venue, DOI).
- The datasets were verified against DataCite (Mendeley v1 and v6 DOIs).
- Conference papers were verified on their official proceedings pages (NeurIPS 2019 ×2, ICML 2016 PMLR, NeurIPS 2022 JAWS via arXiv/conference).
- JMLR (Demšar 2006) was verified on jmlr.org, Holm (1979) via the JSTOR/DOI record, and the arXiv preprints via the arXiv API.
- An HTML entity in one venue name was fixed. No reference is cited without verification.
- Statements attributed to papers were limited to what their retrieved abstracts or well-established content support (`literature/abstracts.json`).
- Missing competitors identified during review and added: JAWS (Prinster et al. 2022), Zhivkov & Fidanova (2026), Papadopoulos et al. (2011).

## 3. Consistency audit (Phase 34)
- **Numbers.** Every result number in the manuscript, cover letter and review records is a double-brace placeholder filled from `values.json`, which is computed from `results/` (`manuscript/build/compute_values.py`, `values_secondary.py`). A scan of the sources found no remaining hand-typed result numbers; the last two ("40", "3%") were converted. Remaining literal numbers are design constants (α levels, splits, hyperparameters) or mathematical consequences (m ≥ 9 / 19 / 99).
- **Tables.** All are generated from CSV results; numbered 1–7 in order of first citation. Supplementary S1–S10 are generated from results.
- **Figures.** All are generated from result files by `visualization/figures.py` (Fig. 1 and the graphical abstract are schematic). Numbered 1–9 in order; S1–S3 in the supplement.
- **Equations ↔ code.** Eq. (1) ↔ `transfer.Deployed`; Eq. (2) ↔ `DifficultyModel`; Eq. (3)–(4) ↔ `TransferFits`/`tj_plus`/`jackknife_plus` (ranks unit-tested).
- **Experiments mentioned ↔ existing results.** E1, E4, E4b, E5 (reverse, ridge, CNN), E6, E6b, E7, E8 and E9 are all present in `results/raw` and listed in `results/raw_results.csv`.

## 4. Reproducibility audit (Phase 35, performed as a stranger)
1. Fresh `git clone` of the branch → `pytest`: 11 passed.
2. Fresh clone, empty `data/raw` → `python run_all.py --mode quick`.
   - **First attempt failed:** a race between parallel downloads, then a network IncompleteRead.
   - **Fixed:** atomic, retried downloads plus prefetch (deviation 12).
   - **Second attempt:** completed in 5 min with no errors. All four data files were downloaded and checksum-verified, and statistics, tables and figures were produced.
3. Fresh clone → `python run_all.py --mode full --skip-experiments` on the committed raw results, then `compute_values.py`: **175 of 175 manuscript values identical** to those used to build the submitted manuscript.
4. Full re-execution of all experiments takes ≈4–5 CPU-hours on 4 cores and is supported in resumable chunks (`--rep-start/--rep-end`). It was executed once to produce the reported results; it was not repeated in full in the fresh clone.
