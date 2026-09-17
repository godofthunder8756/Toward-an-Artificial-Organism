# AC71 protocol v1: majority register read closes all three closure gaps, repair stays load-bearing

Hashed before the final run. Fresh seed family. Engineering seeds (0–2 and the 0–5 diagnostic) informed
the endpoints and are excluded.

## Claim

With the decision-state register read at majority (4, the same convention the program bank's rules use)
under non-self-reversing damage, the repair-active organism holds its acquired routes, keeps its body
stable, and keeps the register intact over the long horizon, while the repair link remains load-bearing
(cutting it kills the organism).

This is a two-sided claim: (a) the three closure gaps of `CLOSURE_BOUNDARY_v1.md` are closed in the
`closed` arm, and (b) the repair remains necessary (the `no_repair` arm dies).

## The one declared change from AC67

`REGISTER_THRESHOLD` from 1 (single-replica) to **4 (majority)**. Everything else — sticky program-bank
damage, the register's location, the paid bank-0 repair, the frozen conservation laws — is unchanged.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`. No move.

## Arms

`closed` (repair enabled), `no_repair` (program-bank repair cut via the frozen `no_policy_write` guard).

## Endpoints (per individual)

`completed`, `first_dead`, `energy`, `W_live`, `C_live`, `B_live`, `register`, `routes`, `demand`,
`occupied`, `state_hash`.

## Prespecified gates (8 individuals = 4 seeds × 2 histories, per arm)

- **G1 (closed survives)** — `first_dead` is None in all 8.
- **G2 (routes held)** — `occupied > 0` at the final tick in all 8 (the acquired function persists).
- **G3 (body stable)** — `W_live ≥ 1` and `C_live ≥ 1` at the final tick in all 8 (no bimodality).
- **G4 (register intact)** — `register == [F,F,F,F]` in all 8.
- **G5 (repair necessary)** — `no_repair` `first_dead` is not None in all 8.

The claim passes iff G1–G5 all pass. A single failing individual on any gate falsifies it; thresholds are
not moved.

## Seeds

Finals: `2800, 2801, 2802, 2803`. Engineering/diagnostic seeds excluded and disjoint.

## Verification

`audit_ac71.py` recomputes the gates from the saved table without simulating; `replay_ac71.py` does
sampled exact reruns; `test_ac71.py` pins the gate shape and recorded outcomes.
