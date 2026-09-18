# AC93 results v1: coordinator transitions enacted by produced machinery — write_ctrl becomes W-gated

2026-09-18. Final seeds `4400, 4401, 4402, 4403` (4 seeds × 2 histories = 8 individuals per condition,
88 rows), hashed protocol `AC93_PROTOCOL_v1.md`, 16,384 ticks, `transition='none'`, forced succession at
t=2400, W production cut from the same tick, machinery-only rescue at t=2490. **All eight prespecified
gates pass.** Audit passed (88 rows, 14 source hashes no drift, arm invariants, W-dependence contrast,
generic-decode link, gates recomputed without simulating); replay 6/6 exact; 21 AC93 tests; full 666-test
AC suite green.

## The question

AC92 established the W repair catalyst (finite-lived, produced, autocatalytic) gates every content write on
the reconstruction/coordination path, and pinned that the coordinator's own transition write `write_ctrl` is
W-INDEPENDENT (energy + material alone, AC88's distinct-resource model). AC93 revokes that declaration on a
NEW architecture: `write_ctrl`'s MODE field (the coordinator's state transition) becomes W-gated (atomic under
`_cap = min(32, 8·available_W, energy, material)`), so coordinator state transitions become a service the
produced machinery performs. The LAST field (rate-limit timestamp) keeps its distinct budget (E2: bookkeeping,
not a transition). The frozen AC88/AC92 rows are never edited; they are the comparator.

## A correction of D3's attribution (carried into the claim)

D3's engineering observed a succession stall mid-cycle at W=0 and attributed it to the gated `write_ctrl`
refusing the COPY→VERIFY transition. **That attribution was wrong, and D4 corrects it.** The direct rival
added for this study (`W_block_ungated` — the ungated architecture under the same W cut) stalls IDENTICALLY:
every measured field is equal to `W_block` (copy_progress, phase, window writes, death tick, W, C). The reason
is structural: in `advance()`, the COPY→VERIFY mode transition is attempted only when the slot copy is complete,
and the slot copy (`write_toward_slot`) is itself W-gated — so at W=0 the copy never completes, the COPY→VERIFY
transition is never attempted, and the `write_ctrl` gate is never exercised. The stall is the pre-existing
W-dependence of the slot copy, not the new gate.

## The measured arms (damage on, corruption off for the interruption arms)

| arm | forced start | first_W_empty | phase at W_empty | copy at W_empty | phase_changes | window succ/ctrl/reg | completes | outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `W_block` | 2400 (8/8) | 2415–2416 | COPY (8/8) | 776–781/910 | **0** | **0 / 0 / 0** | 0/8 | dies 2610–2650, W=0 C=0, desc 130 at death |
| `W_rescue` | 2400 (8/8) | 2415–2416 | COPY (8/8) | 776–781/910 | **0** | **0 / 0 / 0** | **1/1** tick 2550–2551 | survives, W=3 C=2 |
| `W_block_ungated` | 2400 (8/8) | 2415–2416 | COPY (8/8) | 776–781/910 | **0** | **0 / 0 / 0** | 0/8 | dies 2610–2650, W=0 C=0, desc 130 at death |

`copy_progress` at death is 761–770 (vs 776–781 at W_empty): the ambient sticky damage stream, not
`write_toward_slot` (which wrote 0 over the stall window). `W_block` and `W_block_ungated` are field-for-field
identical — the gate toggle changes nothing in the interrupted world.

## The causal links (the gates, all categorical per individual)

**G1 — the gated architecture reconstructs.** Every `gated` (damage=T, corrupt=T) individual completes with
`flipped_still_wrong == 0` and `description_correct == 130`: the W-gated architecture still reconstructs the
corrupted program and survives (the gate does not break reconstruction at W=3).

**G2 — the comparator reconstructs.** Every `ungated` (damage=T, corrupt=T) individual completes with
`flipped_still_wrong == 0`. Runner correctness is the separate pre-final equivalence check: `ungated`
reproduces frozen AC92 `intact` byte-for-byte — **32/32 state_hash** on AC92's final family 4300–4303.

**G3 — the gate is inert at the healthy fixed point (near-equivalence, not byte-identity).** On every
(damage, corrupt) condition, `gated` and `ungated` agree per individual on `completed`, `flipped_still_wrong`,
and `description_correct`, and `successions` differs by at most 1. The state_hash divergence (reported, not
gated) is 4/8 individuals (damage=T, corrupt=T), 6/8 (damage=T, corrupt=F), 8/8 (damage=F) — traced to the
W=2 SWITCH→REMOVE transition (21 replicas > 8·W=16), a 1-2 tick delay, never a structural change (E3). This is
the gate's organism-level signature: it binds gradedly in W (W=0 all transitions, W=1 >8-replica, W=2 the
>16-replica SWITCH→REMOVE, W=3 none), which the unit test `test_gate_binds_gradedly_in_W` pins.

**G4 — the interruption stalls the succession (the COPY) while alive.** Every `W_block` individual forces the
succession at 2400, W empties mid-COPY (2415–2416, `phase_at_W_empty == COPY`, `copy_progress` 776–781/910),
the slot copy and coordinator writes both stop (`window_succ_writes == 0`, `window_ctrl_writes == 0`), the
phase freezes (`phase_changes_during_stall == 0` — the COPY→VERIFY transition is never attempted because the
copy precondition fails), the succession never completes, and the organism dies with the description intact
(`description_correct_at_death == 130`, W=0, C=0).

**G5 — the stall is the copy, NOT the gate.** Every `W_block_ungated` individual has the SAME stall signature
(in fact every measured field equals `W_block`). Removing the gate does not change the stall: the gate is not
the causal mechanism; the copy's pre-existing W-dependence is.

**G6 — the rescue resumes the succession.** Every `W_rescue` individual was stalled at COPY with W == 0 before
the rescue (`phase_at_rescue == COPY`, `W_at_rescue == 0`, `copy_progress` frozen 773–779, `window_succ_writes
== 0`, `phase_changes_during_stall == 0`), then — after the machinery-only re-seed at t=2490 — the succession
completes (2550–2551) and the organism survives (W=3, C=2). The restoration touches only `life[:4]`/`pos[:4]`
(unit-tested), so no controller content is supplied by construction.

**G7 — controls clean.** Every `gated`/`ungated` (damage=F, corrupt ∈ {T,F}) individual completes with
`flipped_still_wrong == 0` (no damage → no succession fires; corruption, when present, is reconstructed).

**G8 — completeness + determinism.** 88 rows == seeds × 2 × 11; the first row's exact rerun is byte-identical
(`state_hash`).

## The single-step gate (unit tests — the W=0 refusal lives here, not at the organism level)

With W == 0, gated `write_ctrl` MODE refuses the whole transition (writes 0), while ungated writes on energy +
material alone. The gate is graded in W: at W=2 the 21-replica SWITCH→REMOVE transition exceeds `8·W=16` and is
refused; at W=3 it proceeds. These facts are pinned by `test_ac93.py` (`test_gated_mode_refuses_with_W_zero`,
`test_ungated_mode_writes_with_W_zero`, `test_gate_binds_gradedly_in_W`, `test_gated_mode_atomic_under_cap`).
The W=0 refusal is NOT observed at the organism level, because at W=0 no MODE transition is ever attempted
during a succession (the copy stalls first) — this is exactly what G5 establishes.

## What this establishes, and its limits

Supported:

- **The coordinator transition write is now W-gated** — pinned at the single-step level (refuses at W=0, graded
  binding in W) and visible at the organism level as the graded near-equivalence (G3: the transition is
  occasionally delayed when W dips to 2). The gate is real, not a no-op, and inert when the machinery is healthy
  (W=3).
- **A succession interrupted mid-cycle stalls and resumes live** (G4, G6): cutting W production during an actual
  succession freezes the COPY phase while the organism is alive, and a machinery-only restoration resumes and
  completes it. This closes AC92's scope note — the succession function was not observed mid-cycle there; here it
  is, and the stall is the copy.
- **The stall is the pre-existing copy dependence, not the new gate** (G5): the ungated architecture stalls
  identically. This is the honest causal attribution the D3 engineering got wrong, and it is now pinned by the
  direct rival arm.

Not established, and not claimed:

- **The write_ctrl gate does not produce a categorical organism-level stall.** Its organism-level effect is the
  graded near-equivalence (a 1-2 tick delay at W=2), because every succession phase transition except VERIFY→SWITCH
  is gated behind a W-gated content-write precondition, so at W=0 the copy stalls before `write_ctrl` is ever
  exercised. "Coordinator transitions become a produced-machinery service" is therefore established at the
  single-step level and as a graded dependency, not as a categorical organism-level interruption.
- **Full autopoiesis is still not claimed.** `advance()` and `prog.choose` remain supplied format-level machinery;
  what is shown W-gated is the write that enacts the supplied machine's transitions. The rescue is EXTERNAL (AC91
  established endogenous production separately).
- **Survival is a bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent): the 8/8
  `gated`/`ungated`/`W_rescue` survival is the observed count, not a per-seed-family guarantee.
- **The final priorities** `[0,1,3,2]`, `[1,0,3,2]`, `[2,3,1,0]`, `[2,3,1,0]` do not include AC83's adversarial
  `[3,0,2,1]` (bank-1 renewal last); the mechanism is priority-independent (the succession copies rule words
  verbatim), recorded as a scope note.

## Verification

- `audit_ac93.py` re-derives coverage (88 rows), arm invariants (`first_W_empty ≤ FORCE_TICK + 63`, mid-COPY
  stall, description intact at death, rescue-from-COPY), the W-dependence contrast (`window_succ_writes == 0` and
  `window_ctrl_writes == 0` in all three interrupted arms), the generic-decode link, source hashes (14 files, no
  drift) and all eight gates — without simulating.
- `replay_ac93.py`: 6/6 sampled conditions reproduce exactly (`state_hash` and endpoint fields).
- `test_ac93.py` (21 tests): the arm config (incl. the W_block_ungated rival), the write_ctrl gate (W=0 refusal,
  atomic-under-cap, graded binding, LAST W-independence), the low-bit-first partial-write fact, the D3
  intervention (force_succession, restore_W machinery-only, make_birth bank-0-only), final-seed disjointness, the
  categorical gate shapes, and the recorded freeze.
- Full AC suite: 666 tests green (56 core AC1–9 + the AC79–93 line, incl. 21 AC93).
- Equivalence (pre-final): `ac93.ungated` reproduces frozen AC92 `intact` byte-for-byte, 32/32 state_hash.

## Files

`ac93.py` (runner, sha256 `d9fda66da8d9e17a493069d7616d6c95ea395fbc43771c157e9b4167e409d514`),
`AC93_PROTOCOL_v1.md` (hashed protocol, sha256
`2bb9c07cbf175df81431ab4124f5fc08ea8f2f385ddb1d19f25af0f12c82aa47`), `test_ac93.py`, `audit_ac93.py`
(split audit), `replay_ac93.py` (sampled exact reruns), `ac93_results_v1/` (frozen rows, pre-run snapshot,
results), `ac93_engineering_v1/` (D2 engineering, seeds 0-7; the E1 clean-control failure),
`ac93_d3_engineering_v1/` (D3 engineering, seeds 0-7), `ac93_engineering_v1_partial_timeout/` (first D2 run,
timed out at seed 5, preserved), `AC93_DESIGN_v1.md` (design + errata E1-E3), `AC93_ENGINEERING_v1.md` (D2
engineering report), `AC93_D3_ENGINEERING.md` (D3 engineering report, attribution corrected here).
