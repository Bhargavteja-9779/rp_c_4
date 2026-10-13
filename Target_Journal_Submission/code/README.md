# tjplus: distribution-free prediction intervals for transferred multivariate calibrations

Code, data instructions and complete reproduction pipeline for the manuscript
*"Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards through a leave-one-standard-out jackknife+"*.

Every number, table and figure in the manuscript is produced by `run_all.py` from the public data sets below. No result is typed by hand.

## 1. Installation
```bash
python -m venv .venv && source .venv/bin/activate        # Python 3.13 tested (3.10+ should work)
pip install torch --index-url https://download.pytorch.org/whl/cpu   # or a CUDA/MPS build
pip install -r requirements.txt
# or: conda env create -f environment.yml
```
Hardware: everything runs on CPU. The study was produced on 4 CPU cores and 15 GB RAM, without a GPU. `tjplus.utils.detect_device()` selects CUDA or Apple-Silicon MPS automatically for the optional CNN, if available.

## 2. Data (downloaded automatically, SHA-256 verified)
| Data set | Source | File | SHA-256 |
|---|---|---|---|
| Corn (80 samples × NIR instruments m5, mp5, mp6; moisture, oil, protein, starch) | Eigenvector Research, https://eigenvector.com/resources/data-sets/ | `corn.mat_.zip` | `8a2d1a03…cca795` |
| IDRC Shootout 2002 tablets (655 × instruments 1, 2; weight, hardness, assay) | Eigenvector Research (same page) | `nir_shootout_2002.mat_.zip` | `04c03a43…d52125` |
| Mango DMC (11,691 spectra, seasons 1–4) | Anderson, Walsh, Subedi & Walsh, Mendeley Data, doi:10.17632/46htwnp833 | `NAnderson2020MendeleyMangoNIRData.csv` | `86159e2d…f153f` |

The files are cached in `data/raw/` on first use (`src/tjplus/data/loaders.py`; full hashes are in the code). If a download fails (for example behind a firewall), place the files in `data/raw/` manually. The checksum is still verified.

Data handling that prevents leakage:
* **Mango.** Replicate scans are averaged per fruit before any split. A fruit is identified by season, region, date, type, cultivar, population and dry matter. The 684–990 nm region is used.
* **Tablets.** Instrument 1 calibrate (155) is source training, instrument 1 validate (40) is source calibration, and instrument 2 test (460) is the target pool.
* **Corn.** Each repetition draws a random 40/10/30 split (source training / source calibration / target pool).

## 3. Reproduce the study
```bash
python -m pytest tests -q                  # unit tests incl. a coverage simulation (~5 s)
python run_all.py --mode quick             # pipeline check, few repetitions (~3 min); outputs in ../results_quick
python run_all.py --mode full --jobs 4     # full pre-registered study (~3-4 h on 4 cores); outputs below
# Long runs can be split into resumable repetition chunks, e.g.
#   python run_all.py --mode full --only E1_main_tablets --rep-start 0 --rep-end 125
# (see scripts/run_remaining.sh); finished chunks are skipped and the analysis merges chunks automatically.
```
Useful options:
* `--only E1_main_corn,E4_robust_mango` runs selected experiments only.
* `--skip-experiments` re-runs statistics, tables and figures from existing raw results.
* `--no-analysis` runs experiments only.

Outputs (full mode):
* `../results/raw/*.csv.gz`: one row per repetition × configuration × method; `*_samples.csv.gz` holds per-sample intervals for the error analysis.
* `../results/summary/summary_all.csv`: aggregates (mean coverage with bootstrap 95% CI, width, interval score, ...).
* `../results/statistics/paired_tests.csv`, `friedman.json`; `../results/metrics.json`, `statistics.json`.
* `../tables/*.csv|md`, `../figures/*.png|pdf`.
* `../results/experiment_logs/run_all_full.log`.

## 4. What is implemented (`src/tjplus`)
| Module | Content |
|---|---|
| `models/pls.py` | PLS1 (NIPALS) with coefficients for all LVs, Hotelling T², Q residual, leverage (tested against scikit-learn) |
| `models/source_model.py` | Source-only selection of preprocessing (none/SNV/SG1/SG2) and LVs (10-fold CV, 1-SE rule); out-of-fold residuals; difficulty model σ(x) = max(ε, a + b√T² + c√Q) fitted by NNLS |
| `models/transfer.py` | PDS (window 2k+1, truncated pseudo-inverse rcond 1e-2, intercept), DS, slope/bias correction (SBC), none; *deployed predictor* μ = post∘f∘g |
| `intervals/methods.py` | **TJ+ / TJ+N** (proposed), TCV+, ablations (naive jackknife, in-sample residuals, σ from T² or Q only); baselines ASTM-PI, SCP-S, WCP-S (Tibshirani et al. 2019), Gauss-LOO, SCP-T-split, Transport (regression analogue of Doula 2026), exploratory label-free LF-conv |
| `models/ridge.py`, `models/cnn.py` | Ridge and 1D-CNN source models (model-class generalisation; CNN with MC-dropout baseline) |
| `experiments/*` | Pre-registered splits (`datasets.py`), evaluation of all methods (`core.py`), parallel runner, CNN and timing experiments |
| `statistics/analysis.py` | Bootstrap CIs, under-coverage flag, paired Wilcoxon + Holm, Friedman, tables |
| `visualization/figures.py` | All figures |

Configuration: `config/experiments.json`. Seeds: base seed 20261013; repetition *r* uses deterministic offsets of the base seed (see `experiments/datasets.py`). Seeds were fixed before any result was seen.

## 5. Using TJ+ on your own data
```python
from tjplus.models.source_model import fit_source_model, DifficultyModel
from tjplus.intervals.methods import TransferFits, tj_plus
src = fit_source_model(X_master_train, y_train)                    # source model (source data only)
sig = DifficultyModel().fit(src.oof_t2, src.oof_q, abs(src.oof_resid))
tf = TransferFits("pds", src, Xt_std, y_std, Xs_std, X_new_target) # m standards: target spectra, reference values, master spectra
lower, upper = tj_plus(tf, alpha=0.1, sigma=sig)                   # 90% intervals (coverage >= 80% guaranteed, ~90% typical)
```
Requirements for the guarantee: the standards must be a **random** sample of the target population, exchangeable with future samples, and they must not be used to train the source model. Kennard–Stone-selected standards are *not* covered by the theory (see robustness experiment E4).

## 6. Licence
Code: MIT. The data sets are subject to their providers' terms (Eigenvector Research; Mendeley Data CC BY 4.0).
