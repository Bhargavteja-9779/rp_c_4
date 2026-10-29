# Second adversarial review of the reinforced manuscript (Phase 10)

**How it was run.** An independent reviewer agent read the revised manuscript (filled Markdown), the result files and the code. It had no access to the author's reasoning. It was asked for ten separate passes, each looking for new issues:

1. novelty;
2. significance;
3. literature;
4. design;
5. statistics;
6. baseline fairness;
7. generalisation;
8. reproducibility;
9. journal fit and writing;
10. overall risk.

It spot-checked 34 numbers against the result files: 31 matched, and three were mislabelled ranges, all corrected below.

**Verdict on the version it read:** major revision, bordering on reject (rejection risk about 50%). Its three main demands were:

1. a fair 95% comparison;
2. correctly built and fairly reported batch-aware baselines;
3. more modest application and generalisation claims.

The review is preserved verbatim in the session record. The issues and what was done about them are listed below. Every correction was re-validated by rebuilding the manuscript from the result files and running `audit/scripts/consistency_checks.py`.

| ID | Severity | Issue (short) | Fixable? | Action taken | Re-validation | Status |
|---|---|---|---|---|---|---|
| C1 | CRITICAL | 95% comparison not like-for-like: TJ+N unbounded in 20/40 main and 45/100 E11 scenarios; competitors' shortfalls small; recipe step 4 overstated | Yes | §4.2 rewritten. 95% counts are now restricted to m ≥ 20 (TJ+N 0/55, Gauss-LOO 16/55, ASTM-T 12/55, OLS-PI 11/29). Unbounded counts and non-inferiority counts are reported for all methods (Gauss-LOO 77/100, OLS-PI 40/52). The shortfall is quantified as 1–2 points. Step 4 softened; abstract says simple intervals were "almost as good at 90% but fell slightly short at 95%". | Values generated from `E11_summary.csv` and `summary_all.csv` | Resolved |
| C2 | CRITICAL | Gauss-LGO (leave-one-batch-out *t*-interval) valid in all random designs; "too wide to be useful" true only at K = 2 | Yes | §4.3 now credits Gauss-LGO as a simple batch-aware option (0 of the random-design combinations too narrow). Width ratios to TJ+N are given per design. Conclusions, cover letter and procedure rewritten: the key is leaving out whole consignments; the formula matters less. | Values from the re-run `E10_summary.csv` | Resolved |
| C3 | CRITICAL | ANOVA-PI built from leave-one-*standard*-out residuals (unfair to the classical method) | Yes | Corrected to signed leave-one-*batch*-out residuals with moment estimators and Satterthwaite df (deviation R3). E10 re-run with unchanged seeds; old files kept in `results/raw/superseded_E10_anova_loo/`. | All other methods reproduced exactly (`audit/data/e10_rerun_check.json`). New ANOVA-PI results reported in §4.3 and Table 4. | Resolved |
| M1 | MAJOR | Wrong mechanism: TJ+N uses symmetric absolute scores, so it does not adapt to skewness | Yes | §4.2 now says TJ+N uses the empirical distribution of absolute errors (no normal tail shape) and is conservative at 95% by its rank rule | Text check | Resolved |
| M2 | MAJOR | Application: bare point-rule comparator; TJ+N ≈ Gauss-LOO; PDS cells unusable; E14 timing not disclosed | Yes | Headline restricted to SBC (RMSEP 1.1–1.2% DM); PDS moved to Table S14. Text states that TJ+N and Gauss-LOO were identical, so the case study shows the sampling effect (3.1× more immature fruit passed with two consignments) and not a formula advantage. Guard-band rules discussed. E14 timing disclosed in §3.2, §4.4 and §4.9. | Values from `E14_summary.csv` | Resolved (guard-band trade-off curves not computed: stated as discussion only) |
| M3 | MAJOR | Unreported pre-registered results (H10d, LGO-CV+N); causal language | Yes | H10d reported as not supported (ρ and p, Fig. S6); LGO-CV+N in Table 4, Fig. 4 and text; mechanism presented as "a plausible reason" | Text check | Resolved |
| M4 | MAJOR | Transport valid on the handheld pairs, omitted from the "source-based intervals fail" statement | Yes | §4.1 now reports Transport covering 0.95–0.99 there, with intervals more than twice as wide | Values from `summary_all.csv` | Resolved |
| M5 | MAJOR | 15 × 1 design uses m = 15; 20 × 1 only for instrument pairs | Partly | Text separates 20 × 1 (m = 20, instrument pairs) from 15 × 1 (m = 15, inflated by the rank rule) and explains why the season shift cannot have 20 × 1 (18 consignments) | Text check | Resolved (design itself not changed) |
| M6 | MAJOR | One product; dependent cells; extension to other products not supported | Partly | §4.3 and §4.9 state that the 8 combinations are closer to 2 independent settings; the extension to pharmaceutical lots and grain is labelled a conjecture; the no-transfer combination is identified | Text check | Resolved as a limitation (no further data available) |
| M7 | MAJOR | CIs conditional on available consignments; chronological design a single configuration; counts pooled over α | Yes | Per-α counts for TJ+B; conditionality and single configuration stated in §3.2, §4.3 and §4.9 | Text check | Resolved (bootstrap over consignments not implemented; stated) |
| M8 | MAJOR | Boot-T weaker than necessary (in-sample residuals, B = 200) | Partly | Result labelled as specific to the implementation; better bootstrap variants named as untested (§4.2, §4.9) | Text check | Accepted limitation (re-run with B ≥ 1000 not done: about 15 CPU-h) |
| M9 | MAJOR | Novelty thin; simple formulas about as good at 90% | Partly | Abstract and conclusions now state the 90% result. The contribution is framed as a benchmark and design study with the batch-sampling finding as headline, and no new statistics is claimed. | Text check | Residual risk (irreducible) |
| Mo1 | MODERATE | Naming TJ+B / TJ+H / TJ+H-N; TJ+G identical to TJ+B in all designs | Yes | §2.4 defines TJ+B as the scaled hierarchical jackknife+ and states that TJ+G gave identical intervals | Text check | Resolved |
| Mo2 | MODERATE | 7 vs 8 combinations | Yes | §3.2 and §4.3 list the 8 combinations; Table 5 caption states that it covers SBC only | Text check | Resolved |
| Mo3 | MODERATE | Abstract "6 of 8 settings" wording | Yes | Now "instrument and season combinations", with coverage over all eight | Text check | Resolved |
| Mo4 | MODERATE | Training-conditional description ("next few hundred samples") | Yes | Reworded: test sets of 10–700 samples; small test sets add their own randomness | Text check | Resolved |
| Mo5 | MODERATE | Supplementary tables and figures not cited | Yes | All S1–S14 cited; Fig. S6 cited | `consistency_checks.py` | Resolved |
| Mo6 | MODERATE | Dangling cross-reference (§2.3 → §4.2) | Yes | Now points to Supplementary Table S3 | Text check | Resolved |
| Mo7 | MODERATE | "Planned in advance" too strong | Yes | §1 now distinguishes the pre-specified main experiments from the second-round additions, with the dated deviation log | Text check | Resolved |
| Mi1 | MINOR | Intra-consignment correlation range | Yes | Now the mean per combination (random designs) | Values | Resolved |
| Mi2 | MINOR | "Ridge and CNN (0 of 22)" mislabelled | Yes | Now "ridge and 1D-CNN models and the reverse transfer direction (0 of 22)" | Text check | Resolved |
| Mi3 | MINOR | "Halved" compared different designs | Yes | Both numbers now refer to the 10 × 2 design, SBC only | Values | Resolved |
| Mi4 | MINOR | Fig. 6 caption omits ±0.25 | Yes | Caption refers to Table S8 | Text check | Resolved |
| Mi5 | MINOR | Missing citations (Sun et al. CV+, Rozet 2012) | Partly | Sun et al. 2026 added (Crossref-verified). Rozet 2012 not added: the record found is a reply letter whose content could not be verified. | Bibliography check | Resolved / partly |
| Mi6 | MINOR | Placeholders (authors, funding, repository) | No (author action) | Listed in the readiness report | — | Open (author action) |
| Mi7 | MINOR | Formulaic phrases ("honest", "The reason is simple", personification, repeated drift warning, bullet lists in Results) | Yes | Removed or rewritten; Results lists converted to prose; drift warning kept once (§4.5), with the procedure referring to it | grep check | Resolved |
| Mi8 | MINOR | Title long and "Trustworthy" vague; abstract should define "valid", name the method and explain "no extra cost" | Partly | Abstract now names the jackknife+ and says "without extra reference analyses". The title was kept, because the corresponding author asked for a title that students can follow; the more technical alternative is offered in the readiness report. | — | Author decision |

## New risks found in this round and how they were checked

- **Equation rendering.** Visual inspection of the PDF showed that LibreOffice rendered Eq. (3) and two appendix formulas as "¿". The same defect existed in the original submission PDF. The math was rewritten (`\lbrack`/`\rbrack`, superscript `\text{+}`), and the PDF text was re-checked: 0 broken glyphs.
- **Unverified venue.** "Accepted at ICML 2026" for Doula 2026 was checked against the arXiv author comment and confirmed.
- **Re-run identity.** All E10 methods other than ANOVA-PI must reproduce the superseded run exactly; see `audit/data/e10_rerun_check.json`.
