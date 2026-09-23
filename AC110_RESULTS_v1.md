# AC110 (C3) results v1 — repair is not load-bearing for the acquired estimate's correctness/use

Frozen on finals 6200-6207 (8 seeds x 2 histories, 96 rows, 2 arms x 3 conditions),
`AC110_PROTOCOL_v1.md` hashed pre-run (`pre_run_snapshot.json`). Engineering seeds 0-7 informed
the endpoints/gate shapes (disclosed in the protocol) and are excluded from the sample.

## Verdict

FALSIFICATION of the support hypothesis. Cutting the estimate's ONLY repair path (`no_repair`
excludes the estimate bit from action 2's bank-0 majority-restore, leaving reacquisition intact)
does NOT degrade the estimate's correctness or use during the decision-relevant window. Its
correctness is maintained entirely by REACQUISITION (`bel_write` at open in-window contacts). The
repair path's only measured effect is a seed-dependent, decision-irrelevant drift of the estimate's
storage after the cause has passed.

## Gates (prespecified; measured, not moved)

| gate | claim | required | measured | verdict |
|------|-------|----------|----------|---------|
| G1 | clean control (no_repair == maintained, no_cause + move) | 32/32 | 32/32 | PASS |
| G2 | accuracy independence in cut (window accuracy equal, both correct) | 16/16 | 16/16 | PASS |
| G3 | use independence in cut (relinquishments + routes equal) | 16/16 | 16/16 | PASS |
| G4 | storage dependence in cut (maintained bel=0 AND no_repair bel=1) | 16/16 | 8/16 | FAIL |
| G5 | viability identity (completed + first_dead equal, all conditions) | 48/48 | 48/48 | PASS |

G1, G2, G3, G5 pass and falsify the support claim. G4 FAILS as prespecified and is recorded, not
moved (see below).

## G2 / G3 — the falsification (robust)

In the cut, the estimate is written to 0 (E_machinery) by `bel_write` at the first open in-window
contact and re-written at every subsequent open contact; at occluded contacts (the C2 gate, q=0.5)
the stored estimate carries the decision. Cutting repair changes nothing on the decision surface:

- G2 accuracy: `bel_wrong_in_window` is IDENTICAL across arms in all 16 individuals (2-31 ticks of
  acquisition latency before the first open contact), and `bel_at_cut_end == 0` (correct) for both
  arms in all 16. The estimate reads the correct cause through the whole window with or without repair.
- G3 use: `relinquishments` (0 in all 16) and `routes` (held in all 16) are IDENTICAL across arms.

The correctness/use of the acquired representation depends on REACQUISITION, not repair.

## G4 — storage dependence is real but seed-dependent (recorded failure)

Cutting repair does have ONE effect: the estimate's storage drifts after the cut window. The
maintained arm holds the estimate at 0 in 16/16 (action 2 restores the minority flips the ambient
sticky-SET stream keeps introducing). The no_repair arm drifts to a majority read of 1 in only 8/16;
the other 8/16 stay at minority (ones = 2-3) within the horizon.

The mechanism is a Binomial coin flip, not a tuning miss: after the cut the estimate latches at 0
(no `bel_write` rule fires on post-window productive held contacts), and the ambient 1e-4 sticky-SET
stream flips each of the 7 replicas independently with probability ~0.55 over the remaining ~8000
ticks, so the number of flipped replicas is Binomial(7, ~0.55) with mean ~3.9 — ~half the individuals
cross the 4-of-7 majority threshold, ~half do not. Measured final ones counts (no_repair): 2 (x2),
3 (x6), 4 (x6), 6 (x2); maintained: 0 (x16). The direction is clean (maintained never drifts,
no_repair drifts in ~half), but the per-individual "no_repair == 1" count is stochastic.

G4 was prespecified as "16/16" and measured "8/16" — this is the AC45 gate-shape error re-entering
(do not gate a seed-dependent fraction on an exact per-individual count). It is recorded as a
FAILURE, not moved; the honest shape is a lower-bound separation (maintained holds 16/16, no_repair
holds 8/16).

This drift is decision-irrelevant in this world: it happens after the cut window has passed, on a
latched conclusion that no second cause re-reads. It would matter only if a later cause needed the
estimate again — out of scope for this single-intervention study.

## G5 — viability identity

`completed` and `first_dead` are IDENTICAL across arms in all 48 cells. The only deaths are seed
6206 in the move condition (both histories, both arms collapse at t=8424 identically) — the AC107
route-move collapse, shared by both arms, not a repair effect.

## Expenditure (resource accounting)

The repair cut is essentially free and saves essentially nothing: `bel_writes == 7` in BOTH arms in
every cell (reacquisition is untouched by construction), and `reg_writes` differs by at most 10
writes across the whole run (the estimate's minority flips that action 2 would otherwise restore).
The estimate rides the program's bank-0 repair, so its repair is bundled into the program's
maintenance at negligible marginal cost.

## Mechanism — why repair cannot fire during the decision window

Action 2 (bank-0 majority-restore) is triggered by observation bit 2, computed as
`min(ones, 7-ones).sum() >= 4` over ALL 126 bits of bank 0. A single estimate bit contributes at
most 3 minority replicas (a 4-of-7 flip reads as majority, minority = 3), so the estimate's own
damage can NEVER trigger its own repair, and the ambient program damage is too slow to trigger it
within the 96-tick window. A per-tick diagnostic confirmed action 2 fires 0 times in the cut window
in both arms. The estimate's repair is therefore structurally unreachable during the only period the
estimate is decision-relevant — AC107 Q3's "ongoing repair is not exercised", now explained, plus
AC76's single-bit-trigger rule.

## Scope notes

- No elevated damage was used: the frozen ambient 1e-4 sticky-SET stream is sufficient to exercise
  the repair cut (post-window drift) without degrading the organism. This is the smallest justified
  regime.
- An external-restoration arm was deemed unnecessary: the mechanism is identified by the
  storage-vs-accuracy split (repair is exercised post-window and decision-irrelevant; reacquisition
  carries the window), so no external mechanism identifier is required.
- The storage drift (G4) is a lower-bound finding, not a per-individual invariant; a
  longer-horizon or second-cause world would make it decision-relevant, which is the natural next
  target, not this study.

## Files

- runner: ac110.py (extends ac107; the repair cut is source surgery on ac4.react, skip_est flag)
- protocol: AC110_PROTOCOL_v1.md (hashed pre-run)
- frozen results: ac110_results_v1/ (rows.jsonl, results.json, pre_run_snapshot.json)
- engineering: ac110_engineering_v1/ (seeds 0-7, excluded from the sample)
