#!/bin/bash
# Detached, resumable driver for the reinforcement experiments (chunks of 50 repetitions; existing chunks are skipped).
cd "$(dirname "$0")/.."
for EXP in E10_batch E11_classical_mango E11_classical_mango_inst E11_classical_corn E11_classical_tablets; do
  REPS=$( [ "$EXP" = "E10_batch" ] && echo 300 || echo 200 )
  for S in $(seq 0 50 $((REPS-50))); do
    python3 run_reinforcement.py --mode full --only $EXP --rep-start $S --rep-end $((S+50)) --no-analysis --jobs 4
  done
done
echo ALLDONE > ../results/experiment_logs/reinforcement_full.done
