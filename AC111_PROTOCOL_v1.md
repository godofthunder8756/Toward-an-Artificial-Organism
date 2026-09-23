# AC111 protocol v1 — composition of the cognitive mechanism with AC105's reconstruction + spending

## Question (I1)

What is needed to compose the supported cognitive mechanism (the AC107 one-bit cause estimate e
in the C2 gated world, frozen by AC110) with AC105's reconstruction + spending architecture, and
does composition introduce interference between the two mechanisms — or is any failure a
standalone failure of one mechanism acting alone?

## The two mechanisms (unchanged, inherited frozen)

- **Cognitive mechanism** (AC110, finals 6200-6207): the one-bit cause estimate
  e in {E_world=1, E_machinery=0}, stored in the dead-rule action bit (traces[0, bel_off], 7
  replicas, majority read, acquired value 1 = E_world). Correctness is carried entirely by
  REACQUISITION (`bel_write` at open in-window contacts); storage (AC109) and repair (AC110) are
  inert. The two causes land at t=8192: `move` (channel-1 mapping flips; correct response =
  relinquish, e should read 1) and `cut` (route-1 read suppressed for [8192, 8288); correct
  response = hold, e should read 0). The C2 gate occludes `used_held` on a Bernoulli(q=0.5)
  fraction of channel-1 contacts, so the stored estimate carries the decision at occluded contacts.

- **AC105 body** (frozen): reconstruction = `reg_from_active`, which rebuilds the 126-bit program
  from the 130-bit description under a persistent trigger (`fire = reg_trigger or program_incomplete`)
  and, in the candidate, the allowance-42 budget rule `budget = max(0, material - 42)` reserving
  material for the relinquishment decision. Corruption = 8 program bits (rule 0, the contact/income
  rule) majority-flipped at t=8192.

## The composition

The estimate bit is EXCLUDED from `reg_from_active` BY CONSTRUCTION: AC110's build passes
`build_offs = reg_offs + streak_offs + [bel_off]` as the reconstruction exclude set, so
reconstruction does not overwrite the estimate. This exclusion is UNTESTED in AC110 (corrupt=False
there, so `reg_from_active` never fires). The composition is the first run where reconstruction
fires while the estimate is live. The two open interference channels are measured, not assumed:
(a) attention-hijack — the corrupted contact rule (mask 1 -> 126) preempts other rules on the
corruption observation; (b) spending — the budget defers reconstruction while `bel_write` is
W-gated (not budget-gated), so the two spending paths are expected to be independent.

All three challenges CO-OCCUR at t=8192 (CORRUPT_TICK == MOVE_TICK == CUT_TICK): corruption
(reconstruction), route change (move), and access impairment (cut).

## Arms

| arm | corrupt | reconstruction | spending | meaning |
|-----|---------|----------------|----------|---------|
| est | no | (none) | (none) | cognitive mechanism alone (reproduces AC110 `maintained`) |
| est_corrupt | yes | persistent trigger, unbounded | none | estimate + AC105's no-budget CONTROL |
| est_corrupt_budget | yes | persistent trigger | allowance-42 | estimate + AC105 CANDIDATE (the full composition) |

Conditions: `no_cause`, `move`, `cut` (from AC110). Both `est_corrupt` arms flip the same 8 bits
at the same tick; the ONLY difference between them is the budget rule.

## Prediction

No interference. The estimate's reacquisition (`bel_write`) and AC105's reconstruction
(`reg_from_active`) act on disjoint bit sets (the estimate is excluded from the reconstruction
target; reconstruction never writes `bel_off`), and their spending is gated by disjoint resources
(W-gated reacquisition vs material-budgeted reconstruction). So:

- the estimate discriminates correctly under corruption (cut -> E_machinery, hold; move -> E_world,
  relinquish), exactly as in AC110;
- reconstruction completes (fw == 0) regardless of the estimate;
- the only failures are the STANDALONE failures already documented: the unbounded arm starves the
  decision (AC104) and the no-corruption arm suffers the route-move collapse (AC107).

## Gates (prespecified; measured, not moved)

G1 (single-change license): `est` reproduces AC110 `maintained` byte-for-byte (`state_hash`),
    every final seed x history x condition. 48/48.

G2 (reconstruction completes under composition): every `est_corrupt_budget` cell has
    `fw_at_corrupt == 8`, `flipped_still_wrong == 0`, `recovery_tick is not None`. Non-vacuous
    (the corruption IS applied) and seed-independent.

G3 (cut: estimate discrimination survives reconstruction): every `est_corrupt_budget` cut cell has
    `bel_at_cut_end == 0` (E_machinery), `relinquishments == 0`, and route-1 bound at the horizon
    (the still-valid route is held through the cut despite reconstruction firing on the same tick).

G4 (move: estimate discrimination survives reconstruction): every `est_corrupt_budget` move cell has
    `relinquishments >= 1` (E_world -> streak -> drop; an E_machinery read would hold indefinitely,
    so relinquishments == 0 would be the discrimination failure).

G5 (reacquisition untouched): every `est_corrupt_budget` cut cell has `bel_writes == 7` AND the
    `est` cut cell has `bel_writes == 7` (the estimate is written exactly once and stays correct;
    a reconstruction reset would force a second write).

G6 (no-harm survival): no cell where `est_corrupt` completed and `est_corrupt_budget` did not
    (the budget never introduces a survival penalty relative to the unbounded arm).

## Reported, NOT gated (standalone failures, bimodality-aware lower bounds)

- `est_corrupt` (unbounded) move deaths: the AC104 starvation mode (relinquishments == 0, the
  reconstruction drains material below the allowance so the drop never fires). Reported per cell.
- `est` (no corruption) move deaths: the AC107 route-move collapse. Reported per cell.
- Survival is reported as a bimodality-aware lower bound; no universal-survival gate.

## Discipline

Engineering first (seeds 0-7, informed the endpoint/gate shapes, disclosed here), then a hashed
protocol, then disjoint final seeds (6300-6307). No gate is moved after seeing the result. The
verification tools (audit/replay/test) are NOT in the frozen source set (AC16/17's drift rule).

## Unit of analysis

Rows are arm-runs (N seeds x 2 histories x 3 conditions x 3 arms). The findings — "estimate holds
through the cut", "budget fixes the starvation", "est collapses" — are properties of matched
(seed, history, condition) cells, one per pairing. The comparison denominator is N x 2 cells per
condition (16 per condition for 8 seeds), never the raw row count.

SOURCES (declared): ac111.py ac110.py ac107.py ac106.py ac104.py ac103.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC111_PROTOCOL_v1.md
