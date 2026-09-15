# AC31 engineering: re-acquisition design FALSIFIED before any final seed

2026-09-15. `ac31_reacquire.py` (no runner, no protocol, no finals), engineering seeds 0–3.
**No protocol was frozen. No final seed was run. No claim is made or withdrawn — the study's premise
failed its own engineering controls, exactly as AC11's did.**

## What the design claimed

After the environment's stress regime changes so a different order is best, an organism that can both
release its stored order and search again performs at the level the new regime permits, while an
organism unable to release or search does not. Gate shape: **separation of minima** (this line's
standing lesson for "cannot hold" claims).

## Prerequisites passed

| regime | optimum | rating | median | worst |
| --- | --- | ---: | ---: | ---: |
| A (rates descending) | `(4,3,1,5,0,2)` | 13.67 | 11.33 | 8.67 |
| B (rates reversed) | `(0,1,2,3,5,4)` | 13.67 | 11.33 | 9.33 |

- the optima **differ**, as required;
- the old optimum rated under the new regime: **11.00** against the new optimum's 13.67 — a margin of
  **2.67 sites**, well above AC13's "there is nothing here" situation (its mean saving was −9.3%).

So the signal exists in aggregate: the world ranks orders with a 4.33-site spread under regime B.

## What the arms actually did (4 individuals each, no finals)

| arm | per-individual post-switch scores | min | mean |
| --- | --- | ---: | ---: |
| `learner_both` (releases and re-acquires) | 11.67, 11.00, 11.67, 13.00 | **11.00** | 11.83 |
| `no_release` (cannot overwrite) | 11.00, 10.00, 10.67, 10.00 | 10.00 | 10.42 |
| `no_search` (never searches) | 12.00, 12.00, 11.67, 12.33 | 11.67 | 12.00 |
| `preserve` (state-blind control) | 12.00, 12.00, 11.67, 12.33 | 11.67 | 12.00 |
| `oracle_b` (handed the optimum — SCAFFOLD) | 12.33, 12.00, 12.00, 13.00 | 12.00 | 12.33 |

**The capable arm does not beat the arms it is supposed to beat.** `learner_both`'s mean (11.83) is
*below* `no_search` and `preserve` (12.00) and below the oracle (12.33). Only `no_release` behaves as
predicted, and it is the arm that is supposed to be worst — which it is, on both min and mean.

## Diagnosis

Two measured causes, neither of which is a threshold in disguise:

1. **Seed noise is comparable to the margin.** The oracle's *individual-level* rating is 12.0–13.0
   (mean 12.33) while the same order rates 13.67 on the sweep's seed set (0,1,2). A single order's
   rating moves by ~1 site depending on which seeds it is scored on, and the arms are compared
   **unpaired** — each individual uses its own seeds. The comparison is therefore swamped by scoring
   variance rather than by the mechanism.
2. **A random order is already close to optimal.** `no_search` and `preserve` act on a uniformly
   random initial order and score 12.00 — about **88% of the 13.67 the optimum achieves**. The
   ranking is real in aggregate (4.33 spread) but its *per-individual* learning margin is small
   relative to noise, so an 80-evaluation hill-climb with 3-seed scoring cannot be distinguished from
   not searching at all.

## What this does and does not mean

- It **does not** say re-acquisition is impossible. It says *this design cannot detect it*, and the
  design failed for two identified, fixable reasons.
- It is **not** a reason to change the bar. The standing rule is that a gate threshold is never moved
  to turn a failure into a pass, and the AC16 rule ("do not re-run with a better-chosen threshold")
  applies here in advance.
- The candidate fixes are **design** changes and must be re-engineered and re-declared before any
  final seed:
  1. **Pair the comparison**: score every arm on the *same* seed set, so the shared variance cancels
     — the standard fix for exactly this failure.
  2. **Raise replication**: more individuals and more scoring seeds per individual, since the
     per-individual noise (~1 site) is half the margin (~2.67).
  3. Optionally, sharpen the world: make a random order worse (currently 88% of optimal), so the
     available margin is larger than the noise. That is a *world* change and must be made and
     re-measured **before** the protocol, never after seeing results.

## Status, plainly

- `ac31_reacquire.py` has **no runner**: its `__main__` refuses and points here.
- **No `AC31_PROTOCOL_v1.md` exists**, because the study never reached the protocol stage. Seeding in
  the module's docstring that a protocol "will" be written is accurate only if the design is
  re-engineered and passes engineering first.
- No final seeds, no frozen directory, no claims, nothing withdrawn. The two open endpoints are
  untouched: this study was aimed at neither survival nor retention.
- Nothing here bears on experience, understanding or life.

## Artifacts

`ac31_reacquire.py`, `test_ac31.py`, `/tmp/ac31_engineering.json` (engineering rows, not a frozen
artifact). Related: `AC30_ACQUIRE_v1.md` (whose single-seed noise diagnosis this study inherited and
did not fix), `AC18_PROTOCOL_v1.md` (the gate shape this study intended to use), `AC11_DESIGN_
CONTROLS_v2.md` (the precedent: a study stopped by its own engineering controls).
