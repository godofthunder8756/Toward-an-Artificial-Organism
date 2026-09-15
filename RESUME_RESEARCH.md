# Resume guide: Toward an Artificial Organism

## Current stopping point

The latest completed study is **AC10, the integrated constituent ablations**
(`AC10_RESULTS_v1.md`, `ac10_results_v1/results.json`, 72 rows, seeds 1300–1303).
It closes the requirement that stood open since AC1–AC4: every produced
constituent is now ablated **inside** the integrated AC9 body, and the enclosure's
function is separated from its matter.

Main results, all nine prespecified gates passing:

- Removing **W production** leaves no entry ever allocated (0/8) and kills all
  eight individuals at 248–252.
- Removing **C production** confines conversion to the inherited endowment (zero
  assay conversion) and kills all eight at 200–232.
- Removing **B production** exports constituents in 8/8 and loses both routes at
  195–279; activity still reaches 0.355 by random fallback, so survival is not a
  proxy for organization.
- **Forced retention with zero enclosure matter** (`no_B_retention`) and
  **external B supply** (`B_rescue`) both hold routes 8/8, completion 8/8 and
  zero export. The enclosure's causal contribution is retention, not mass.
- Suppressing W or B production only **after** development still destroys the
  acquired routes (599–609 and 647–857): the requirement is continuous
  maintenance, not a one-time acquisition.

Before it, the frozen baseline is **AC9 controls v3** (`AC9_CONTROLS_RESULTS_v3.md`):
acquired functional organization is maintenance-dependent where it is physically
located, with relocation, inert-burden, protected-copy and oracle controls all
run. AC9 v1 is preserved as a negative result and v2 as the first-stage pass.

## Exact resume commands

Any Python 3.12 with NumPy suffices. On this host the project has its own venv
(3.12.3 / NumPy 2.5.3); the default system `python3` has no NumPy:

```bash
cd ~/projects/Toward-an-Artificial-Organism
export OPENBLAS_NUM_THREADS=1

# AC10: tests, frozen-table audit, sampled exact replays, and a 14 s full rerun
.venv/bin/python -B -m unittest test_ac10
.venv/bin/python -B audit_ac10.py        # uses the frozen table, does not rerun
.venv/bin/python -B replay_ac10.py       # 11 sampled conditions, exact
.venv/bin/python -B ac10.py              # refuses to overwrite ac10_results_v1

# AC9 controls v3 remains frozen and audited
.venv/bin/python -B audit_ac9_controls_v3.py
```

Every runner uses `mkdir(exist_ok=False)`, so a re-run raises rather than
overwriting frozen results. Changed experiments need a new versioned protocol and
a new results directory; the v3 and AC10 directories are frozen.

Regression suite before extending anything:

```bash
.venv/bin/python -B -m unittest test_ac1 test_ac2 test_ac3 test_ac4 \
  test_ac4_transport test_ac5 test_ac5_program test_ac6 test_ac7 test_ac8 \
  test_ac9 test_ac9_memory test_ac10      # 77 tests, about 6 s
```

The docs' original commands (`py -3.12-arm64 -B ...`, `C:\Users\ahern\...`) are
the author's Windows machine, not this host.

## What to do next

1. **The next target, and the strongest remaining claim**: test whether the
   controller can *acquire* the need to allocate or relinquish maintenance
   resources under an intervention chosen **after** development, with no
   protected copy and no externally fixed correct state. This is the requirement
   the status table still records as NOT ESTABLISHED. Keep the constituents of
   AC10 intact and make a fixed schedule matched for spending, plus
   random/reactive allocation on the same observation stream, competent rivals.
2. Add a broader developmental function than the present four routing classes and
   two unknown bits, keeping random-fallback survival and acquired-function
   retention as separate endpoints.
3. Preserve exact replays, source hashes, ledgers and negative controls. Any
   successful result must survive protected-memory, relocation, inert-burden and
   read-disabled comparisons.

Useful standing facts: activity is a poor proxy for organization (AC10 shows
three arms acting long after route loss); `policy_accuracy` of the program bank
does not discriminate at the current horizon and flip rate; eight independent
individuals per study is the working sample size.

Do not resume the stopped E3 v0.11 experiment or reinterpret the current results
as proof of full autopoiesis. The next breakthrough must show that the system's
own maintained organization changes its maintenance decisions under
counterfactual damage or scarcity, with no protected copy or externally fixed
correct state.
