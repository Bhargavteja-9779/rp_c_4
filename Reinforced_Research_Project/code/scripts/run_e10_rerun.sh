#!/bin/bash
# Re-run of E10 after the ANOVA-PI correction (deviation R3). Seeds are unchanged, so every other method must
# reproduce the superseded results exactly (checked by the analysis).
cd "$(dirname "$0")/.."
for S in 0 50 100 150 200 250; do
  python3 run_reinforcement.py --mode full --only E10_batch --rep-start $S --rep-end $((S+50)) --no-analysis --jobs 4
done
echo DONE > ../results/experiment_logs/e10_rerun.done
