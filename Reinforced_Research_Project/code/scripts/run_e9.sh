#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 run_all.py --mode full --no-analysis --jobs 4 --skip-cnn-timing --only E9_competitor_corn,E9_competitor_tablets,E9_competitor_mango,E9_competitor_mango_inst
echo "E9_DONE"
