#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 run_all.py --mode full --no-analysis --jobs 4 --skip-cnn-timing --only E4b_subchannel_corn,E4b_subchannel_tablets,E4b_subchannel_mango
echo "E4B_DONE"
