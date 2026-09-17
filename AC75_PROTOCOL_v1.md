# AC75 protocol v1: erase-on-relinquish makes the reconciled closure world-accommodating

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering diagnostic
(`AC75_ENGINEERING_v1.md`, seeds 0–2). Final seeds are declared below and are disjoint from every
engineering seed and every prior frozen family.

SOURCES (declared): ac75.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC75_PROTOCOL_v1.md

## Claim

With the AC71 reconciled architecture (majority-read register, sticky program-bank damage, load-bearing
self-monitoring repair) joined to AC16's re-acquisition machinery, **erasing the relinquished entry when
the organism drops it** makes the closure world-accommodating: the organism survives, re-acquires the
moved route, and holds **both** routes with an intact register through permanent and temporary
post-development route changes, while the repair loop stays load-bearing — and the same architecture
*without* the erase fails under change.

Two-sided, like AC71: (a) the erase arm meets the accommodation gates, and (b) the no-erase rival and the
no-repair arm fail in their declared ways.

## The one declared change from AC74's variant C

Variant C is `AllocRestore` (drop on failure streak + restore on productive contact) with the deposit
path open (`grow=True`, `activation=[True,True]`). The change is in the drop only: after writing the
relinquished register bit, the drop **erases the entry** (clears the slot's `life` and `bits`, booked as
`memory_expiry`, consistent with the frozen decay law). Nothing else differs; the conservation identities
of `ac4.balance` are untouched.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick. Route move: channel 1 flips (`1 - base_map[1]`).

## Arms and transitions

| arm | allocation | repair |
| --- | --- | --- |
| `erase` | drop+erase+restore, deposit open | on |
| `restore` | drop+restore (no erase), deposit open | on |
| `erase_no_repair` | drop+erase+restore, deposit open | cut (frozen `no_policy_write`) |
| `restore_no_repair` | drop+restore (no erase), deposit open | cut |

Transitions: `perm` (channel 1 flips at t=8192, stays), `temp` (flips at 8192, flips back at 12288),
`none` (no change). Each individual = one (seed, history) = 4 seeds × 2 histories = 8 per condition.

## Endpoints (per individual)

`completed`, `first_dead`, `first_relinquish`, `first_restore`, `energy`, `material`, `fuel`, `W_live`,
`C_live`, `B_live`, `register`, `routes`, `demand`, `occupied`, `relinquishments`, `restorations`,
`contacts`, `productive`, `state_hash`.

## Prespecified gates (8 individuals per condition)

- **G1 (survive permanent move)** — `erase`/`perm` `first_dead is None` in all 8.
- **G2 (survive temporary outage)** — `erase`/`temp` `first_dead is None` in all 8.
- **G3 (re-acquire and hold)** — `erase`/`perm` `routes[1] == 1 - base_map[1]` and `demand == [42,0]` in all 8.
- **G4 (register intact)** — `erase` register `[F,F,F,F]` in all 8 under `perm` **and** all 8 under `temp`.
- **G5 (erase is load-bearing for accommodation)** — `restore`/`temp` has `first_dead` not None in **at least one** of 8 (the no-erase rival fails under change).
- **G6 (repair stays load-bearing)** — `erase_no_repair`/`perm` `first_dead` not None in all 8.
- **G7 (inert without change)** — `erase`/`none` has 0 relinquishments and `demand == [42,0]` in all 8, and `erase`/`none` reproduces `restore`/`none` exactly (`state_hash`).
- **G8 (completeness and determinism)** — every declared condition has 8 rows; re-running the first two individuals reproduces them exactly.

The claim passes iff G1–G8 all pass. A single failing individual on G1–G4, G6, G7 falsifies it; G5 needs
at least one failing individual. Thresholds are not moved; this study is not re-run with a better bar.

## Seeds

Finals: `2900, 2901, 2902, 2903`. Engineering seeds (0–2) and every prior frozen family are excluded and
disjoint.

## Anti-drift rules

- The runner creates `ac75_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight (AC32/AC33's rule, enforced in code):** the runner parses the `SOURCES (declared):` line
  above and asserts it equals the set of files it hashes, before the first final seed.
- `test_ac75.py`, `audit_ac75.py`, `replay_ac75.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails; this protocol may not be edited after the first final seed.

## Source hashes (computed before the first final seed)

    (recorded in ac75_results_v1/pre_run_snapshot.json at freeze time)
