# Software for laboratories

The software has three parts:

1. **`tjplus` Python package** (`../code/src/tjplus`). Install it with `pip install -r ../code/requirements.txt` and add `code/src` to your path.
   - `tjplus.api.SBCIntervals`: slope/bias correction with transfer jackknife+ intervals, leaving out one sample or one batch at a time, or the Gaussian alternative. It works from the original calibration's predictions and the reference values of the standards.
   - `tjplus.api.transfer_jackknife`: the same interval for any transfer method, given as a fitting function (for example PDS on spectra).
   - `tjplus.api.plan` / `tjplus.planning`: the planning model. It gives the expected coverage, for samples from new batches, of each interval rule for a design of K batches × n standards and an intra-batch correlation ρ.

2. **Command-line program:**
   ```bash
   cd code/src
   python -m tjplus.cli plan --standards 20 --batches 2 --rho 0.5
   python -m tjplus.cli interval --standards ref.csv --new routine.csv --batch-column lot --threshold 14 --out result.csv
   ```
   - `ref.csv` has the columns `prediction`, `reference` and a batch column.
   - `routine.csv` has the column `prediction`.

3. **Browser tool:** `transfer_interval_tool.html`, a single file that needs no installation and sends no data anywhere.
   - *Planner:* expected coverage for a design.
   - *Calculator:* corrected values, intervals and pass/fail/re-measure decisions from pasted data.

Tests (`code/tests/test_reinforcement.py`) check that the package reproduces the research implementation exactly. The browser tool's numerics (t quantiles, planner, jackknife+) were checked against the package.
