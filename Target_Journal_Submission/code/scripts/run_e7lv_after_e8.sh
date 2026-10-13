#!/usr/bin/env bash
cd "$(dirname "$0")/.."
until grep -q "E8_DONE" /tmp/claude-0/e8.log; do sleep 10; done
python3 run_all.py --mode full --no-analysis --jobs 4 --skip-cnn-timing --only E7_lv_corn,E7_lv_tablets,E7_lv_mango
echo "E7LV_DONE"
