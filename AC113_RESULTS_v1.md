# AC113 (P6) results v1 — heterogeneous weighting is NOT load-bearing at the organism scale (F1)

Frozen on finals 6400–6407 (8 seeds × 2 histories = 16 individuals), both regimes
(ε = 0.08 primary, ε = 0.02 secondary), `AC113_PROTOCOL_v1.md` hashed pre-run
(`pre_run_snapshot.json`). Engineering seeds 0–7 selected the fixed comparison parameters
(disclosed in the protocol) and are excluded from the sample. 736 rows per regime.

## Verdict

**F1 (equivalence).** At high occlusion (q = 0.9), the maintained two-counter weighted
estimate does **not** beat the strongest single-counter rival on post-cause income, in either
tested regime. At their respective optima the two arms TIE (identical combined income), and
the per-individual paired differences are small and mixed-sign (exact sign-flip p = 0.38 /
0.30, both ≫ 0.05). Heterogeneous weighting is **not** load-bearing at the organism scale:
the P2 conclusion — a maintained integer counter suffices — survives the heterogeneous
likelihood ratio.

This is the falsification the study was built to detect and record, not a support claim. The
P4 decision-theoretic prediction (+0.03 … +0.32 min-mean regret at q = 0.9) does **not**
transfer to the organism scale.

## Gates (prespecified; measured, not moved)

| gate | claim | required | measured (ε=0.08 / ε=0.02) | verdict |
|------|-------|----------|---------------------------|---------|
| V1 | clean control: no_cause 0 relinquish, all complete | 64/64 | 64/64 / 64/64 | PASS |
| V2 | causal role: accumulator's read content matters (θ=0.6) | (a) or (b) | (b) both; (a) 14/16 only ε=0.02 | PASS |
| V3 | observer-discard: per-tick byte-identity under swap | 16/16 | 16/16 / 16/16 | PASS |
| G-COMPARE | graded income comparison (fixed params, paired sign-flip) | verdict | F1 / F1 | F1 (recorded) |

## The fixed comparison (G-COMPARE) — the scientific question

Fixed parameters (engineering-selected, disclosed): ε=0.08 → θ* = 0.5 vs (w,N)* = (−6, 4);
ε=0.02 → θ* = 0.5 vs (w,N)* = (−6, 1). Per-individual paired combined-income difference
(post-cause income, move + cut), two_counter − single_counter:

- ε = 0.08: mean **−2336**, observed sum −37376, exact sign-flip **p = 0.375**. Differences:
  `[−18816, −18816, −192, −192, −64, −64, −64, −64, +64, +64, +64, +64, +128, +128, +192, +192]`.
- ε = 0.02: mean **−2344**, observed sum −37504, exact sign-flip **p = 0.305**. Differences:
  `[−18752, −18752, −128, −128, 0, 0, 0, 0, 0, 0, 0, 0, +64, +64, +64, +64]`.

The mean is slightly NEGATIVE (the two-counter is marginally worse) and not significant —
F1 (equivalence), exactly as the prespecified decision rule maps it (mean < 0 but p > 0.05).
The two large negative differences are a seed-dependent collapse tail, reported next.

## The collapse tail (AC39's lesson, in the unfavourable direction)

The two `−18816` / `−18752` differences are **deaths**: on 2/16 finals individuals the
two-counter at the aggressive θ* = 0.5 collapses under the cut (its accumulated weak-M
evidence fires a false relinquishment, the route lapses, and the organism dies — income ≈ 0
post-cause). The single counter at (w,N)* holds and survives. Measured survival (completed &
alive):

| arm | ε=0.08 move / cut | ε=0.02 move / cut |
|-----|--------------------|-------------------|
| two_counter (θ*) | 16/16 / **14/16** | 14/16 / 14/16 |
| single_counter ((w,N)*) | 16/16 / 16/16 | 16/16 / 14/16 |
| scramble (θ*=0.5) | 16/16 / 14/16 | 16/16 / 14/16 |
| immediate | 8/16 / 16/16 | 10/16 / 16/16 |

The engineering screen (seeds 0–7) showed **no** collapse at θ* = 0.5 — the collapse is
seed-dependent and lands on the finals, not the engineering seeds. This is AC39's
engineering-vs-finals transfer failure, here in the unfavourable direction: the aggressive
threshold the engineering screen endorsed is fragile on fresh seeds.

The in-sample sweep on the finals confirms it: the finals' own income-maximising two-counter
θ is **0.60** (not 0.5), and the finals' best single-counter is **(−2, 4)** — and at those
finals-selected optima the two arms again **TIE** (both 611,840 combined income at ε=0.08).
So the equivalence is robust to where the optima are selected; only the aggressive θ*=0.5 is
fragile, and that fragility is shared by the aggressive end of both families, not a
two-counter defect.

## The causal role (V2) — information carried + causally effective, but not useful

At θ = 0.6 (where the read-forced (0,0) scramble does not degenerate), under the cut the
two-counter **false-relinquishes in 4/16** while the scramble holds in **0/16** — the
accumulated content causally drives the decision. Under move the contrast is weaker and
seed-dependent: the scramble drops in 16/16 (ε=0.08) / 14/16 (ε=0.02), so the "content drops
the stale route earlier" advantage is present on only 2/16 individuals (ε=0.02) and absent on
the ε=0.08 finals. The accumulator's content is **informative and causally effective**, but
its measured effect at the aggressive threshold is a false relinquishment (harmful), not an
early correct drop (helpful). "Causally effective" is established; "useful" is not.

## Expenditure (resource accounting)

The functional-capability-vs-cost ladder is as P4/P5 declared: the two-counter holds 7 bits,
the single-counter 3, the immediate 0. Measured mean writes (cut, ε=0.08):
counter_writes 77.4 (two_counter) vs 40.2 (single_counter) — the two-counter pays roughly
2× the decision-state write cost for **no** graded income gain. reg_writes (the shared program
maintenance) are essentially equal (~2170) — the decision-state maintenance rides the program
repair, as in AC110.

## What this establishes (and does not)

- **Established.** In the informative-heterogeneous regime (ε ≤ 0.125, q = 0.9), a maintained
  single integer counter matches a maintained two-counter weighted estimate on every
  decision-relevant endpoint at the organism scale. The two-dimensional non-integer weighting
  is not load-bearing; gradedness remains unrequired (P4's F1 outcome, now measured at
  organism scale). The immediate (no-state) rival still dies under move (8/16 ε=0.08, 10/16
  ε=0.02), so a maintained decision state remains necessary — it just need not be a
  two-dimensional weighted one.
- **Not established.** No support for heterogeneous weighting being load-bearing; no
  survival advantage for the candidate; no maintenance-dependence claim (the repair-dependence
  of the decision state was explicitly out of scope — AC110's question, not this one).

## Files

- runner: `ac113.py` (imports `ac112.py`; income accumulator verified byte-identical to
  `ac112.run`, `state_hash` included, before the freeze)
- protocol: `AC113_PROTOCOL_v1.md` (hashed pre-run; sha256 `a86cdc37…`)
- frozen results: `ac113_results_v1/` (ε=0.08), `ac113_results_v1_eps002/` (ε=0.02) —
  each `pre_run_snapshot.json` + `rows.jsonl` (736 rows) + `results.json`
- audit: `audit_ac113.py` (re-derives coverage, ledgers, arm invariants, V2, and the verdict
  from the saved table WITHOUT simulating) — PASS both regimes
- replay: `replay_ac113.py` (sampled exact reruns, byte-identical `state_hash`) — PASS 12 rows
  each regime
- tests: `test_ac113.py` (9 tests: mechanics, ac113≡ac112 byte-identity, recorded gates pinned
  as F1) — PASS
- engineering (disclosed, excluded): seeds 0–7 (`_income_q09*.py` screens); no frozen artifact
  edited, re-run, or re-hashed.
