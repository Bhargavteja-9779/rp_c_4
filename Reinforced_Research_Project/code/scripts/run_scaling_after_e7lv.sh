#!/usr/bin/env bash
cd "$(dirname "$0")/.."
until grep -q "E7LV_DONE" /tmp/claude-0/e7lv.log; do sleep 10; done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src python3 -c "
from tjplus.experiments.timing import run_timing_scaling
print(run_timing_scaling('data/raw', '../results/raw').to_string())"
echo "SCALING_DONE"
