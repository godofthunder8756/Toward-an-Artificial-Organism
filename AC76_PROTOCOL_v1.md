# AC76 protocol v1: controller turnover via a compressed internal description

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering probes
(`AC76_ENGINEERING_v1.md`). Final seeds declared below, disjoint from every engineering seed and prior
frozen family.

SOURCES (declared): ac76.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC76_PROTOCOL_v1.md

## Claim

Under bounded program corruption — flipping the **majority** of the first 8 program bits (rule 0's
enabled bit and mask), which the single-bank majority-restore architecture **cements** (AC61) — an
organism that maintains its program by **re-instantiation from an internal priority description**
regenerates the correct program and survives, where the baseline (repair-only) architecture leaves the
flipped bits wrong.

This is the §3 turnover claim: the controller's content is re-derived from a description (the 4-bank
priority, stored redundantly in the organism's own substrate), not restored to its own corrupted
majority. It does **not** claim content self-production (the priority is still externally supplied), and
it does **not** claim recovery from catastrophic (whole-program) corruption, which the engineering found
economically unrecoverable.

## The mechanism (single declared change from the AC71 baseline)

The program's acquired content is the 4-bank priority. It is stored as 8 bits × 7 replicas in the dead
legacy bank 1. When the organism's own corruption observation (obs bit 2) fires, the program is
re-instantiated from `priority + fixed rules` (a decode) as a **paid** write, under the frozen per-action
cap, **excluding the 4 register bits** (dynamic decision state, not program content). Nothing else
differs from the AC71 architecture.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick. No route move.

## Arms

| arm | re-instantiation from description | bank repair |
| --- | --- | --- |
| `regen` | on | on |
| `baseline` | off | on (AC71 — cements) |
| `no_repair` | off | off (loop cut) |

Intervention: at t=8192, flip the majority (4 of 7 replicas) of program bits 0–7 to the opposite of the
correct value, leaving 3 replicas intact.

## Endpoints (per individual)

`completed`, `first_dead`, `program_correct` (decoded bits matching the priority-derived program),
`flipped_still_wrong` (of the 8 flipped bits, how many still wrong at end), `W`, `C`, `energy`,
`material`, `fuel`, `routes`, `demand`, `register`, `state_hash`.

## Prespecified gates (8 individuals = 4 seeds × 2 histories)

- **G1 (regen recovers)** — `regen` completes the horizon **and** `flipped_still_wrong == 0` (the 8
  corrupted bits' majority is restored to correct) in all 8.
- **G2 (baseline cements)** — `baseline` `flipped_still_wrong > 0` in all 8 (the corruption is cemented,
  not repaired).
- **G3 (regeneration load-bearing)** — `no_repair` dies (`first_dead` not None) in all 8.
- **G4 (control clean)** — with no corruption, `regen` and `baseline` both complete with
  `flipped_still_wrong == 0` in all 8 (the mechanism introduces no spurious change).
- **G5 (completeness and determinism)** — 4 seeds × 2 histories × 3 arms × 2 corruption conditions rows
  all present; re-running the first individual reproduces it exactly.

**Gate-shape correction recorded before finals:** G1 was originally stated as `program_correct == 126`.
Engineering seed 2 recovered all 8 corrupted bits (`flipped_still_wrong == 0`) yet scored 125/126 because
a *non*-corrupted bit carried natural damage at the final tick — so "whole program exactly correct" is
confounded by natural damage on bits the claim is not about. G1 was therefore corrected to
`flipped_still_wrong == 0` (the claim is about the corrupted bits), and the correction is recorded here
rather than applied silently after the fact.

The claim passes iff G1–G5 all pass. Thresholds are not moved; this protocol may not be edited after the
first final seed.

## Seeds

Finals: `3000, 3001, 3002, 3003`. Engineering seeds (0–2) and every prior frozen family (2600–2903) are
excluded and disjoint.

## Anti-drift rules

- The runner creates `ac76_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed set,
  before the first final seed.
- `test_ac76.py`, `audit_ac76.py`, `replay_ac76.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac76_results_v1/pre_run_snapshot.json at freeze time)
