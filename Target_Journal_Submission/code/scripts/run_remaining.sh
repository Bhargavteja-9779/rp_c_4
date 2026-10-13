#!/usr/bin/env bash
# Resumable driver: runs the full study in repetition chunks (each chunk saved on completion; finished chunks are skipped).
set -u
cd "$(dirname "$0")/.."
J=${JOBS:-4}
run() { python3 run_all.py --mode full --no-analysis --jobs "$J" --skip-cnn-timing "$@"; }
for s in 0 125 250 375; do run --only E1_main_tablets --rep-start $s --rep-end $((s+125)); done
for s in 0 150; do run --only E1_main_mango --rep-start $s --rep-end $((s+150)); done
run --only E4_robust_corn,E4_robust_tablets,E4_robust_mango
run --only E5_reverse_corn,E5_ridge_corn,E5_ridge_tablets,E5_ridge_mango
run --only E7_window_corn,E7_window_tablets,E7_lv_corn,E7_lv_tablets,E7_lv_mango
python3 run_all.py --mode full --no-analysis --jobs "$J" --only E5_cnn_mango,E6_timing
echo "ALL_REMAINING_DONE"
