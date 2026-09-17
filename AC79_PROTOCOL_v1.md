# AC79 protocol v1: description maintenance through paid vulnerable machinery (no hidden pristine backup)

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering result
(`AC79_ENGINEERING_v1.md`, `ac79_engineering.py`). Final seeds declared below, disjoint from every
engineering seed and prior frozen family.

SOURCES (declared): ac79.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC79_PROTOCOL_v1.md

## Claim

Under the AC76 bounded-corruption intervention (t=8192 majority-flip of program bits 0-7), an
organism whose 8-bit priority description lives **in** the sticky 1e-4 damage stream and is
maintained by a paid majority-restore (folded into the corruption-triggered re-instantiation)
recovers the program and survives as well as the pristine-description AC76 arm, while the
unmaintained-description control degrades and dies. The compressed-description turnover therefore
does **not** rely on a hidden pristine backup.

This does **not** claim content self-production (AC78: the priority's content is still externally
supplied). It establishes only that the description's *storage and maintenance* is endogenous — the
reference for turnover is as vulnerable and as paid-maintained as the program it re-instantiates.

## The mechanism (single declared change from AC76)

1. The description (`traces[1,:8]`, 8 bits x 7 replicas) receives the same sticky 1e-4 damage as the
   program, from an independent stream (`rng1 = default_rng([seed,1609])`).
2. When the program's own corruption observation (obs bit 2) fires, the re-instantiation step first
   repairs the description's minority replicas to its 7-replica majority (paid, same primitive, same
   per-action cap), then re-instantiates the program from the repaired description, exactly as AC76
   does (`reg_maintained`, verbatim from `ac79_engineering.py`).

The description maintenance *rides* the program's corruption-triggered re-instantiation. This is
conservative: the program is 16x larger than the description, so it degrades 16x faster and its
corruption signal fires long before the description could approach a majority flip.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick, sticky description damage (`|=`) at 1e-4 per
replica per tick from an independent stream. No route move.

## Arms

| arm | description in damage stream | description repaired | program re-instantiation |
| --- | --- | --- | --- |
| `maintained` | yes | yes (paid) | yes |
| `pristine` | no (= AC76 regen as-is) | — | yes |
| `unmaintained` | yes | **no** | yes |
| `no_repair` | yes | no | loop cut (AC76 load-bearing control) |

Intervention: at t=8192, flip the majority (4 of 7 replicas) of program bits 0-7 to the opposite of
the correct value, leaving 3 replicas intact. `pristine` is AC76's `regen` arm exactly (frozen
`reg_from_priority`, no description damage), so its recovery is a built-in reproduction of AC76.

## Endpoints (per individual)

`completed`, `first_dead`, `alive_at_corruption` (alive at t=8192), `program_correct`,
`flipped_still_wrong` (of the 8 flipped bits, how many still wrong at end), `description_correct`,
`description_valid` (decoded priority is a permutation), `description_same` (decoded priority ==
original priority), `W`, `C`, `energy`, `material`, `fuel`, `routes`, `demand`, `register`,
`state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Gates G1, G2 and G5 are on clean endpoints (recovery + description integrity), not on survival
counts. Recovery and description integrity are gated on **survivors** (`completed`) only: the paid
description maintenance stops at death, and the AC68 W/C collapse kills `maintained` and `pristine`
alike, leaving a dying organism unable to fund the re-instantiation — so a surviving organism's
recovery is the clean endpoint, and a dying organism's degradation is a consequence of death, not a
mechanism failure. Survival is reported as a bimodality-aware lower bound (AC68 W/C bimodality; the
description-repair spend slightly shifts the cliff) and is not gated to an exact count.

- **G1 (maintained recovers)** — every `maintained` individual that **completes the horizon**
  (`completed`) has `flipped_still_wrong == 0` **and** `description_same == 1` (decoded description
  == original priority): the program's 8 corrupted bits are re-instantiated to correct and the
  description is intact, i.e. the description maintenance is sufficient. (Non-vacuous by G3's
  at-least-one-survivor clause.)
- **G2 (unmaintained fails)** — every alive-at-t=8192 `unmaintained` individual has
  `flipped_still_wrong > 0` **and** `description_valid == 0` (decoded priority is not a permutation):
  the damaged, unmaintained description cannot re-instantiate, so the corruption stays cemented, i.e.
  the description maintenance is necessary.
- **G3 (maintenance load-bearing)** — every alive-at-t=8192 `unmaintained` individual dies after
  t=8192 (`first_dead` not None; the AC76 baseline death signature ~8-9k), **and** at least one
  alive-at-t=8192 `maintained` individual completes the horizon. The maintained survival count is
  reported as a lower bound, not gated to an exact number.
- **G4 (no_repair dies)** — every `no_repair` individual dies (`completed` False): the loop cut is
  load-bearing (AC76 control).
- **G5 (control clean)** — with no corruption, every `maintained` and `pristine` individual has
  `flipped_still_wrong == 0`; every `pristine` individual has `description_same == 1` (its
  description is never damaged); and every `maintained` individual that **completes the horizon**
  (`completed`) has `description_same == 1`. The mechanism is inert and introduces no spurious
  change. Description integrity is gated on survivors only: the description repair is paid, so a
  death (the AC68 W/C bimodality) stops it and the description then degrades post-mortem exactly as
  the program bank does — a consequence of death, not a mechanism failure.
- **G6 (completeness and determinism)** — 4 seeds x 2 histories x 4 arms x 2 corruption conditions
  (64 rows) all present; re-running the first individual reproduces it exactly (`state_hash`
  included).

The claim passes iff G1-G6 all pass. Thresholds are not moved; this protocol may not be edited after
the first final seed.

## Boundary (stated up front)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down) — the "catastrophic destruction" analog already out of
scope — not a hidden backup. There is no more-internal description to re-derive it from.

## Seeds

Finals: `4004, 4005, 4006, 4007` (4 seeds x 2 histories = 8 individuals per condition). Disjoint from
every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003) and from engineering families 0-7 and
8500-8799. Engineering seeds (0-7) are excluded.

**Gate-shape corrections recorded before the frozen finals.** Two endpoint-population corrections
were made after deviating runs exposed them, both population-filter changes only (the simulation is
unchanged) and recorded here rather than applied silently:

1. **G5** was first specified on individuals *alive at t=8192*; a deviating run (seeds 4000-4003,
   preserved at `ac79_deviation_seeds4000_v1/`) showed a maintained individual can be alive at t=8192
   and then die of the AC68 W/C collapse, after which the paid description repair stops and the
   description degrades post-mortem. G5 is corrected to gate description integrity on *survivors*
   (`completed`).
2. **G1** had the same flaw in the corruption arm: a maintained individual can be alive at t=8192 yet
   already in the terminal W/C collapse (its W has collapsed, so `8*interior_W` repair capacity is
   zero and the re-instantiation cannot run), and `pristine` fails *identically* on such individuals —
   the corruption is not recovered because the organism is dying, not because the description
   maintenance failed. G1 is therefore corrected to gate recovery + description integrity on
   *survivors* (`completed`), with non-vacuity carried by G3's at-least-one-survivor clause.

The G1 correction was found on the first 4004-4007 run (corrected G5, still-unfixed G1), which failed
for the G1 reason above. Because both corrections are population-filter changes only, that run's rows
are byte-identical to the frozen run and it is superseded by `ac79_results_v1/` rather than preserved
separately. The frozen finals are seeds 4004-4007, disjoint from the deviating 4000-4003.

## Anti-drift rules

- The runner creates `ac79_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac79.py`, `audit_ac79.py`, `replay_ac79.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac79_results_v1/pre_run_snapshot.json at freeze time)
