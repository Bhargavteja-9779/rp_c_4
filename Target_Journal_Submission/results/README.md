# Results

- `raw/` — per-repetition results (one row per repetition × scenario × method × α), written by `code/run_all.py`. Files named `<experiment>@rAAAA-BBBB.csv.gz` are repetition chunks of one experiment (merged automatically by the analysis). `*_samples.csv.gz` contain per-sample intervals for the error analysis. `superseded_E7_lv/` holds the LV-sensitivity runs replaced after the bug fix (deviation 9); they are **not** used.
- `raw_results.csv` — index of all raw result files with row counts and SHA-256 checksums (≈4.9 million rows in total, of which ≈3.6 million per-repetition rows and the rest per-sample error-analysis rows; therefore stored as compressed chunks).
- `summary/summary_all.csv` — aggregated results per configuration (mean coverage with bootstrap CI, widths, interval scores, validity flag, conditional coverage).
- `statistics/paired_tests.csv`, `statistics/friedman.json`, `statistics.json` — statistical tests.
- `metrics.json` — key per-method metrics for the primary analysis.
- `experiment_logs/` — logs of all runs (including the first, time-limited attempt).

Regenerate everything from the raw files: `cd ../code && python run_all.py --mode full --skip-experiments`.
