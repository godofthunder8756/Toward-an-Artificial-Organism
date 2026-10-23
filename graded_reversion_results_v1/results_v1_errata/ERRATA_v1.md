# Errata v1

Additive notes for the graded joint recurrent reversion phase B report. No existing file is modified. No label, measured value, or claim text is changed. No network was trained for this note.

The corrected reading is `../PHASE_B_RESULTS_v2.md`. The original report remains `../PHASE_B_RESULTS.md`.

## E-B1. Freeze commit recorded as HEAD

`PHASE_B_RESULTS.md` line 7 and the `freeze_commit` field in `phase_b_results.json` record `9808759ffd4dfd417014b22c6b63512c22a61c9f`. That commit is the phase A results commit. The frozen protocol commit is `018f2a773e4d5fb897230e9ca1d6904c32c9fd78`. The runner recorded HEAD at run time. All 13 manifest hashes match at `70080264d40969bfba06480849d64c0fc4628f5c`, so no value is affected.

## E-B2. Secondary-block summary bullets omit the block letter

The three secondary summary bullets do not name r, z, or n. From `phase_b_results.json`, they read as follows. All three are criterion not met.

- r 0/10 (D 7, M 0)
- z 0/10 (D 5, M 0)
- n 5/10 (D 7, M 8; seeds 202-205, 209)

Joint passes for block n are seeds 202, 203, 204, 205, and 209. The per-seed secondary table in the original report already names the blocks. Those rows are unchanged.
