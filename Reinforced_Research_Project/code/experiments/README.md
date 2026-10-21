# Experiments

All experiments are defined declaratively in `../config/experiments.json` and executed by `../run_all.py` through the modules in `../src/tjplus/experiments/`:

| ID | Purpose (research question) | Definition | Implementation |
|---|---|---|---|
| E1_main_{corn,tablets,mango} | Main evaluation, baselines, ablation, α sensitivity (RQ1–RQ3) | config `E1_main_*` | `datasets.run_corn_rep`, `datasets.run_fixed_rep`, `core.evaluate` |
| E4_robust_* | Robustness: Kennard–Stone, noise, ±1-channel drift, half source (RQ4) | config `E4_robust_*` (variants) | same, with `variant` |
| E4b_subchannel_* | Robustness: ±0.25-channel drift (review round 10) | config `E4b_subchannel_*` | same |
| E5_reverse_corn, E5_ridge_* | Generalisation: reverse direction, ridge models (RQ5) | config `E5_*` | same, with `pairs`/`model` |
| E5_cnn_mango | Generalisation: 1D-CNN + MC-dropout baseline (RQ5) | `run_all.py` | `cnn_mango.run_cnn_experiment` |
| E6_timing, E6b scaling | Computational cost (RQ6) | `run_all.py`, `scripts/run_scaling_after_e7lv.sh` | `timing.run_timing`, `timing.run_timing_scaling` |
| E7_window_*, E7_lv_* | Sensitivity: PDS window, ±2 latent variables | config `E7_*` | `half_window`, `lv_offset` |
| E8_mango_instruments | Independent instrument shift (review round 5) | config `E8_mango_instruments` | `datasets.run_mango_inst_rep` |
| E9_competitor_* | Normalised Gaussian competitor (review round 8) | config `E9_competitor_*` | `intervals.methods.gauss_loo_normalised` |

Run one experiment: `python run_all.py --mode full --only E8_mango_instruments` (add `--rep-start/--rep-end` for resumable chunks). Driver scripts used for the reported runs are in `../scripts/`.
