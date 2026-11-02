#!/bin/bash
# Third round: E15 confirmatory study and E14b guard bands (resumable chunks).
cd "$(dirname "$0")/.."
for S in 0 50 100 150 200 250; do
  python3 run_reinforcement.py --mode full --only E15_confirm --rep-start $S --rep-end $((S+50)) --no-analysis --jobs 4
done
for S in 0 50 100 150; do
  python3 run_reinforcement.py --mode full --only E14b_guard --rep-start $S --rep-end $((S+50)) --no-analysis --jobs 4
done
echo DONE > ../results/experiment_logs/round3.done
