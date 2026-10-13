# Review round 4 — Reviewer #4 (ML methodology, implementation correctness, reproducibility)

I inspected the code (`code/src/tjplus`) against every methodological statement in the manuscript. My concerns differ from Reviewers #1–3.

## Code–manuscript cross-check
| Statement in manuscript | Code location | Status |
|---|---|---|
| σ(x) = max(ε, c₀ + c₁√T² + c₂√Q), NNLS on \|OOF residuals\|, ε = 5% of median | `models/source_model.py::DifficultyModel` | Consistent |
| T² = Σ t²/s², Q = squared X-residual | `models/pls.py::diagnostics` | Consistent; **Q is computed in the preprocessed spectral space** (not stated) |
| PDS window 5, truncated pseudo-inverse rcond 0.01, intercept | `models/transfer.py::PDS` | Consistent; **edge channels use zero-padded (effectively shorter) windows** (not stated) |
| SBC: least-squares slope and bias on standards | `fit_deployed('sbc')` | Consistent |
| TJ+N: σ evaluated on the fold-specific transferred spectrum | `intervals/methods.py::TransferFits`, `tj_plus` | Consistent |
| Jackknife+ ranks ⌈(1−α)(m+1)⌉ and ⌊α(m+1)⌋, unbounded otherwise | `jackknife_plus` | Consistent; unit-tested |
| WCP-S: logistic domain classifier on PLS scores; target spectra unlabelled (incl. test spectra) | `wcp_source` | Consistent; **transductive use of the test spectra should be stated** |
| ASTM-PI: t(n−A−1)·SEC·√(1+h) | `astm_pi` | Consistent for PLS. For ridge models, SEC uses n − A − 1 with A from the companion PLS model (approximation; not stated) |
| MC-dropout: 100 passes, sd = \|b\|·√(var + s²_cal), SBC on the MC mean | `cnn_mango.py` | Consistent |
| CNN architecture and training | `models/cnn.py` | **Hyperparameters missing from manuscript** (SNV + standardisation input, Conv1d(16, k=7) → Conv1d(32, k=7, stride 2), dense 64, dropout 0.2, Adam lr 1e-3, weight decay 1e-5, batch 128, ≤150 epochs, early stopping patience 20) |
| LV sensitivity (±2 LVs) | `experiments/datasets.py` | **INCONSISTENT — see M1** |

## MAJOR
**M1 (implementation error, LV sensitivity).** The LV offset was applied after `fit_source_model`, so the deployed predictions used A±2 LVs while σ(x), the out-of-fold residual pool and the SEC were computed at the originally selected A. The source-calibrated baselines in Table S3 were therefore calibrated on residuals of a different model. TJ+N validity is unaffected in principle (σ is still a fixed function, independent of the target data), but the reported sensitivity numbers are not internally consistent.
*Fix:* move the offset inside model selection and re-run E7_lv. *(Done; see deviation log #9.)*

## MODERATE
- Add the CNN hyperparameters (above) to §3.2 or the Supplementary Material.
- State that Q is computed in the preprocessed space, that PDS edge channels use truncated windows, and that WCP-S uses the unlabelled target spectra transductively.
- State the ASTM-PI approximation for ridge.

## MINOR
- The timing for TJ+N includes the five CV+ refits computed in the same routine. This is stated in §4.10; keep it.
- `requirements.txt` pins versions. `run_all.py --mode full` reproduces the study, but on a 4-core machine it may need the chunked driver (`scripts/run_remaining.sh`) because of runtime. Mention this in the README.

## Reproducibility check (performed)
- `python -m pytest tests -q` → 11 passed.
- `python run_all.py --mode quick` → completes; quick outputs are isolated in `results_quick/`.
- Seeds are deterministic: identical repetition seeds give identical standards across methods. Confirmed by the paired structure of the raw files (one row per repetition × method with identical `n_test`).
