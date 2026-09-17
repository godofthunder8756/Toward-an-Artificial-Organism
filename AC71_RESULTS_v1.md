# AC71 results v1: majority register read closes all three closure gaps, repair stays load-bearing

2026-09-16. Final seeds 2800–2803 (4 seeds × 2 histories = 8 individuals per arm), hashed protocol
`AC71_PROTOCOL_v1.md`, 16,384 ticks. Engineering seeds excluded.

## Gate outcomes (prespecified)

| gate | statement | result |
| --- | --- | --- |
| G1 | `closed` survives the horizon in all 8 | **PASS** (8/8) |
| G2 | `closed` routes held (`occupied > 0`) in all 8 | **PASS** (8/8, `demand=[42,0]`) |
| G3 | `closed` body stable (W≥1, C≥1) in all 8 | **PASS** (8/8, W=3, C=2) |
| G4 | `closed` register intact in all 8 | **PASS** (8/8, `[F,F,F,F]`) |
| G5 | `no_repair` dies in all 8 | **PASS** (8/8, deaths 402–860) |

All five gates pass. The claim holds.

## What the result is

The single declared change from AC67 — reading the decision-state register by **majority (4)** instead of
single-replica (1) — closes all three closure gaps of `CLOSURE_BOUNDARY_v1.md` at once, at four times the
standard horizon:

1. **The acquired function is now self-maintaining.** Both routes are held for the full 16,384 ticks
   (`demand=[42,0]`), where they previously lapsed by ~t=891.
2. **The body is no longer bimodal.** All 8 individuals survive with W=3, C=2, energy 118–125 stable —
   the W/C decay cascade of AC68 is gone, because the cascade's single point of failure (a
   single-replica register flip stopping the renewal) is removed.
3. **The register no longer degrades.** A lone damaged replica cannot flip a majority read, so the
   self-relinquishment (`_drop`) path never starts.

And the repair loop remains **load-bearing**: cutting it still kills 8/8 (deaths 402–860), now by the
observation-hijack path (the bank-0 corruption bit stays set, the program loops on the cut repair). The
load-bearing constraint has shifted from the decision register (AC67) to the self-monitoring observation.

## The reconciled architecture

The organism now has a **robust decision state** (majority-read register, so single-replica noise cannot
relinquish a route) and a **load-bearing self-monitoring loop** (the paid repair of its own corruption
signal, whose failure kills it). This is the configuration the line had been missing: the two demands that
looked irreconcilable in AC70 — vulnerable-to-damage and robust-to-noise — are separated across two
mechanisms (the register is robust; the observation loop is vulnerable), rather than forced onto one
threshold.

## What this establishes and what it does not

Establishes: the three closure gaps had one root cause (a read/repair threshold mismatch), and reading the
decision state by majority closes all three while the repair stays causally necessary. This is a genuine
step toward organismal autonomy: the acquired function is self-maintaining, the body is stable, and the
self-maintenance loop is load-bearing.

Does not establish: autopoiesis (the controller is still acquired, not self-produced), consciousness,
optimality, or generality beyond the two-route, four-region world.

## Verification

`audit_ac71.py` passes (five gates recomputed from the table without simulating); `replay_ac71.py` 5/5
exact; `test_ac71.py` 6 tests green.

## Artifacts

`ac71.py`, `ac71_results_v1/`, `AC71_PROTOCOL_v1.md`, `AC71_FINDING_v1.md`, plus the diagnostic trail
`AC69_FINDING_v1.md`, `AC70_FINDING_v1.md`.
