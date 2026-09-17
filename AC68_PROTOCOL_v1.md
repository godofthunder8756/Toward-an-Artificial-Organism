# AC68 protocol v1: the body's self-production is closed, the acquired function is open

Hashed before the final run. Fresh seed family. Engineering seeds (0–2) informed the endpoints and are
excluded.

## Claim

Over a long horizon (16,384 ticks, four times the lineage standard), the repair-active organism's body is
self-sustaining — it survives and maintains its energy, W, C and B at a steady state — while its acquired
function (the routes) lapses. This is a characterization claim: it locates the closure boundary (body
closed, function open), and is gated categorically on the two-sided pattern, not on a margin.

## The one declared change from the frozen physics (inherited from AC67)

Program-bank damage is a sticky SET (`|=`) not a toggle (`^=`); register read is single-replica
(`REGISTER_THRESHOLD=1`). This is the AC67 world, unchanged, so the repair loop is load-bearing; AC68
measures what it sustains over the long horizon.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`. No move.

## Arms

`closed` (repair enabled) only. The `no_repair` arm dies early (AC67) and is not relevant to the
long-horizon question.

## Endpoints (per individual)

`completed`, `first_dead`, `first_route_loss`, final `energy`/`material`/`fuel`, `W_live`, `C_live`,
`B_live`, `register`, `routes`, `demand`, `occupied`, `renewals` (actions 3+4), `state_hash`.

## Prespecified gates (8 individuals = 4 seeds × 2 histories)

- **G1 (body survives)** — `first_dead` is None in all 8.
- **G2 (body machinery maintained)** — `W_live ≥ 1` and `C_live ≥ 1` at the final tick in all 8.
- **G3 (function lapses)** — `occupied == 0` at the final tick in all 8.

The claim passes iff G1–G3 all pass. A single failing individual on any gate falsifies the claim;
thresholds will not be moved.

## Seeds

Finals: `2700, 2701, 2702, 2703`. Engineering seeds (0,1,2) excluded and disjoint.

## Verification

`audit_ac68.py` recomputes the gates from the saved table without simulating; `replay_ac68.py` does
sampled exact reruns; `test_ac68.py` pins the gate shape and the recorded outcomes.
