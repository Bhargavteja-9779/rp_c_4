#!/usr/bin/env bash
# E8 external validation (resumable chunks)
cd "$(dirname "$0")/.."
for s in 0 100; do python3 run_all.py --mode full --no-analysis --jobs 4 --skip-cnn-timing --only E8_mango_instruments --rep-start $s --rep-end $((s+100)); done
echo "E8_DONE"
