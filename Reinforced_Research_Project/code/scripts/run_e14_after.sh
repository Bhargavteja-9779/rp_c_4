#!/bin/bash
# Runs E14 after the main reinforcement driver has finished (avoids CPU contention).
cd "$(dirname "$0")/.."
while pgrep -f run_reinforcement_full.sh > /dev/null; do sleep 30; done
for S in 0 50 100 150; do
  python3 run_reinforcement.py --mode full --only E14_application --rep-start $S --rep-end $((S+50)) --no-analysis --jobs 4
done
echo DONE > ../results/experiment_logs/e14.done
