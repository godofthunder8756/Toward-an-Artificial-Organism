# AC111 (I1) results v1 — composition of the cognitive mechanism with AC105's reconstruction + spending

Frozen on finals 6300-6307 (8 seeds x 2 histories, 144 rows, 3 arms x 3 conditions),
`AC111_PROTOCOL_v1.md` hashed pre-run (`pre_run_snapshot.json`). Engineering seeds 0-7 informed
the endpoints/gate shapes (disclosed in the protocol) and are excluded from the sample.

## Verdict

The two mechanisms compose, but NOT cleanly. The two DIRECT interference channels the protocol
named are clean — reconstruction never overwrites the estimate bit (the `bel_off` exclusion holds),
and the allowance-42 budget never starves reacquisition — but the corruption's effect on the
CONTACT RULE (the "attention-hijack" channel) perturbs the estimate's reacquisition SCHEDULE on a
minority of final seeds, producing a named, seed-dependent, BEHAVIOURAL interference in the cut.
No survival-level interference: every corrupt-arm cell completes and holds route-1 at the horizon.

The direct channels (reconstruction overwrite, spending starvation) being clean is the load-bearing
answer to "does reconstruction interfere with the estimate": NO. The residual is the corruption
changing WHEN the organism contacts, which changes WHEN (and whether) the estimate's reacquisition
fires — a contact-schedule perturbation, not a storage/spending interaction.

## Gates (prespecified; measured, not moved)

| gate | claim | required | measured | verdict |
|------|-------|----------|----------|---------|
| G1 | est reproduces AC110 maintained byte-for-byte | 48/48 | 48/48 | PASS |
| G2 | reconstruction completes under composition (fw=0) | 48/48 | 48/48 | PASS |
| G3 | cut: estimate discriminates + holds (bel=0, relinq=0, route held) | 16/16 | 12/16 | FAIL (recorded) |
| G4 | move: estimate relinquishes the stale route | 16/16 | 16/16 | PASS |
| G5 | reacquisition untouched (bel_writes == 7 in both arms) | 16/16 | 12/16 | FAIL (recorded) |
| G6 | no-harm survival (budget never dies where unbounded survives) | 48/48 | 48/48 | PASS |

G3 and G5 are recorded as failures, not moved (AC16/17's discipline). The honest shape is given
below: the failures are two seed-dependent behavioural modes, both survival-neutral.

## G2 / G4 / G6 — the direct channels are clean

- **Reconstruction completes under composition (G2)**: every `est_corrupt_budget` cell has
  `fw_at_corrupt == 8`, `flipped_still_wrong == 0`, `recovery_tick` at 8193-8202. The estimate's
  presence does not block `reg_from_active`; the corruption IS applied (non-vacuous). The recovery
  tick is 8193 on most seeds, slightly later (8196-8202) where the allowance defers reconstruction
  — the intended budget behaviour, not a block.
- **Move discrimination survives (G4)**: every `est_corrupt_budget` move cell relinquishes >= 1.
  The estimate reads E_world and the streak->drop fires despite reconstruction. No final seed shows
  the engineering starvation (seed 5, where the UNBOUNDED arm stalled the streak and died) — the
  allowance-42 reserve funds the decision on every final priority (AC105's transfer, reproduced).
- **No-harm survival (G6)**: no cell where `est_corrupt` completed and `est_corrupt_budget` did
  not. On finals the unbounded arm dies 0/48 (the engineering seed-5 starvation did NOT recur —
  AC39 again), so this gate is non-vacuous only in the survival direction it can express.

## G3 / G5 — the named behavioural interference (the honest finding)

The corruption flips rule 0 (the contact/income rule, mask 1 -> 126), so the organism's contact
SCHEDULE changes. The estimate's reacquisition (`bel_write`) fires only on OPEN in-window contacts,
so a schedule change moves WHEN the estimate is corrected. Two final seeds expose this:

- **6306 (2 cells, both histories)**: the cut never "bites". The corrupted contact rule shifts the
  organism's contacts so no open in-window contact occurs; `machinery_cut` never fires, the estimate
  is never written (bel_writes == 0) and stays at its acquired value 1 = E_world (WRONG for the
  cut). This is HARMLESS: with the reduced contact rate the streak never reaches 6, so the organism
  holds route-1 anyway (relinq == 0, route held, survives). The estimate reads wrong, consequence-free.
- **6307 (2 cells)**: a spurious relinquishment, recovered. The corrupted schedule extends the
  estimate's acquisition latency (AC110 already measured 2-31 ticks of latency before the first
  open contact) past the streak's 6-failure threshold: six occluded-unproductive contacts accumulate
  against the stale pre-cut estimate (1 = E_world) and the organism relinquishes a still-valid route
  at t=8198. It re-binds (8201), the first open contact then corrects the estimate to E_machinery
  (8203), and the route is held to the horizon (routes=[1,1], survives).

Both modes are BEHAVIOURAL (recovered, survival-neutral), seed-dependent, and absent from the
engineering screen (seeds 0-7 were clean 16/16 on both endpoints) — AC39's lesson in the
unfavourable direction: the engineering "no interference" screen did NOT transfer to finals.

The G5 failure is the same two modes read through the write count: 6303 (bel_writes == 8 — one
extra 1-replica re-correction after an ambient flip, a second open contact) and 6306 (bel_writes
== 0 — the cut never bit). Both are the contact-schedule perturbation, not a storage/spending
interaction: `bel_write` is W-gated and the budget defers only reconstruction, so reacquisition is
never starved — it is merely scheduled differently.

## Mechanism — why the direct channels are clean

The estimate bit lives at `bel_off = 14*dead_rule_index + 10` (the dead rule's action bit 0, frozen
value 1 = E_world). AC110's build passes `build_offs = reg_offs + streak_offs + [bel_off]` as the
`reg_from_active` exclude set, so reconstruction rebuilds the program WITHOUT writing `bel_off`.
Verified two ways: (a) the reconstruction target `build_program(description)` at `bel_off` is 1
(E_world) — the value reconstruction WOULD write if the exclusion were absent — and (b) in the cut
the estimate reads E_machinery (0) at cut end while reconstruction completes on the same tick, and
`bel_writes == 7` (a single atomic 1->0 write that is never re-done). The budget defers only
`reg_from_active` (`_cap(b, budget)`); `bel_write` is gated by `_cap` (W-catalysed) alone, so the
two spending paths are disjoint by construction.

## Files

- runner: ac111.py (extends ac110's build; adds corruption + the persistent/budget maintain_fn)
- protocol: AC111_PROTOCOL_v1.md (hashed pre-run)
- frozen results: ac111_results_v1/ (rows.jsonl, results.json, pre_run_snapshot.json)
- engineering: ac111_engineering_v1/ (seeds 0-7, excluded; clean 16/16 cut — did not transfer)
- audit: audit_ac111.py (re-derives without simulating; records G3=12/16, G5=12/16)
- replay: replay_ac111.py (sampled exact reruns)
- test: test_ac111.py (mechanism pins + the exclusion-is-load-bearing fact)

## Handoff

The supported cognitive mechanism (AC107/110 one-bit cause estimate) composes with AC105's
reconstruction + spending WITHOUT storage/spending interference: the estimate bit's exclusion from
`reg_from_active` is load-bearing and verified under a live reconstruction, and the allowance-42
budget funds the decision on every final priority. The one named residual is a seed-dependent
behavioural interference from the corrupted contact rule re-scheduling the estimate's reacquisition
(6306 never-biting cut, 6307 spurious-then-recovered relinquishment) — survival-neutral, and the
natural next question is whether the estimate's decision should tolerate a re-scheduled reacquisition
(or whether the contact rule's corruption is the thing that needs its own maintenance), NOT a new
storage or spending design.
