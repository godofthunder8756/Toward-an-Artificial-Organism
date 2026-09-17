# AC81 protocol v1: replacement across generations of components

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering result
(`AC81_ENGINEERING_v1.md`, `ac81_engineering.py`). Final seeds declared below, disjoint from every
engineering seed and prior frozen family.

SOURCES (declared): ac81.py ac80.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC81_PROTOCOL_v1.md

## Claim

The organism's physical components — the W catalysts, C energy-converters and B boundary — are
**constructed, used, and replaced across multiple turnover cycles**, and this replacement is driven
by the **internally retained production recipe** (the 78-bit description internalized in AC80). A
**partial loss** (one killed converter and five killed boundary sites, not every copy) is rebuilt by
the organism's own production rules, the components are **used** (W repairs, C converts fuel to
energy, B retains the acquired routes), and the recipe is **maintained** against damage — so that
the maintained organism keeps constructing components and survives, while the organism whose recipe
is not maintained (unmaintained description) degrades and dies.

This is a component-level claim, not an autopoiesis/consciousness claim, and it is **not** a claim
of recovery from catastrophic destruction (destroying every usable copy of a component, the analog
already out of scope). Content self-production is untouched (AC78): the recipe's content is
inherited at acquisition; this study shows the inherited recipe drives multi-cycle replacement.

## The mechanism (no new primitives — reuses AC80 unchanged)

- The description (`traces[1,:78]`, 7 replicas/bit) stores the five rule words (5×14=70 bits)
  including the three production rules — W-birth `(1,64,6)`, C-birth `(1,128,7)`, B-birth
  `(1,256,8)` — plus the 8-bit permutation.
- During life the 126-bit program is re-instantiated from this description by the generic decode
  `rebuild` (AC80), which copies the five words verbatim and derives the four bank rules from the
  permutation. `prog.program` is retained only in the observer.
- The program's production rules fire on the observation bits (W-low=6, C-low=7, B-low=8), paying
  the frozen prices to birth replacements when a component dies (W life 64, C 128, B 256). This is
  the turnover loop: component dies -> observation bit -> production rule -> replacement born.
- The description is maintained against the sticky damage stream by its own trigger
  (`DESC_TRIGGER=2`, AC80): the re-instantiation fires on (obs bit 2) OR (description minority
  count >= 2), first majority-restoring the description (paid), then rebuilding the program.

The claim "replacement uses internally retained information" rests on three links, each testable:
(a) the production rules are the description's words 3–5 (unit test: `rebuild` copies them);
(b) the description is maintained (internalized keeps 78/78, unmaintained degrades);
(c) the maintenance is load-bearing (unmaintained and no_repair die).

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick, sticky description damage (`|=`) at 1e-4
per replica per tick from an independent stream (`rng1 = default_rng([seed,1609])`). No route move.
`DESC_TRIGGER=2`. `LOSS_TICK=8192`.

## Arms

| arm | description in damage stream | description repaired | decode |
| --- | --- | --- | --- |
| `internalized` | yes | yes (paid, own trigger) | generic |
| `pristine` | no (hidden backup) | — | generic |
| `unmaintained` | yes | **no** | generic |
| `no_repair` | yes | no | loop cut (AC80 load-bearing control) |

Intervention (partial loss, `loss=True`): at t=8192, kill one C converter (`life[16]=0`) and five B
boundary sites (`boundary[0:5]=0`). Not every copy — the catastrophic-destruction analog is out of
scope. The killed C and B must be rebuilt by the organism's production rules. W is left intact so
the loss is survivable (killing W powers down the repair and is not the claim). The `loss=False`
condition is the control: identical world, no intervention.

## Endpoints (per individual)

`completed`, `first_dead`, `alive_at_loss` (alive at t=8192), turnover (`W_birth`, `C_birth`,
`B_birth` totals over the horizon), `C_birth_post`/`B_birth_post` (births after t=8192), use
(`writes` repair, `converted` energy, `routes`), component populations at end (`W_live`, `C_live`,
`B_live`), `description_correct` (of 78), `description_same` (decoded permutation == original
priority), `energy`, `material`, `demand`, `state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Recovery and description endpoints are gated on **survivors** (`completed`): the paid description
maintenance stops at death, and the AC68 W/C collapse kills individuals in the stable arms alike
(AC79/AC80). Survival is reported as a bimodality-aware lower bound, not gated to an exact count.

- **G1 (turnover: constructed + replaced)** — every `internalized` individual that completes the
  horizon has `W_birth >= 100`, `C_birth >= 20`, `B_birth >= 100`: each component class is born
  many times over the horizon (W ~95x its 16 slots, C ~64x its 4 slots, B ~84x its 20 sites),
  i.e. multiple turnover cycles, not a held steady state.
- **G2 (use)** — every `internalized` completer has `writes > 0`, `converted > 0`, and both
  `routes` non-None: the components are used (W repairs, C converts, B retains).
- **G3 (partial-loss recovery: replaced)** — every `internalized` completer has `C_birth_post >= 1`
  and `B_birth_post >= 5` and `C_live >= 2` and `B_live == 20`: the killed converter and boundary
  sites are rebuilt and the populations restored.
- **G4 (recipe maintained)** — every `internalized` completer has `description_correct == 78`, and
  every `unmaintained` individual has `description_correct < 78`: the production recipe is retained
  in the maintained arm and degrades in the unmaintained arm.
- **G5 (maintenance load-bearing)** — every `unmaintained` individual dies (`completed` False), and
  at least one `internalized` individual completes. The internalized survival count is a lower
  bound, not gated.
- **G6 (loop cut dies)** — every `no_repair` individual dies: the re-instantiation loop is
  load-bearing (AC80 control).
- **G7 (control clean)** — in the `loss=False` condition, every `internalized` and `pristine`
  completer has `description_correct == 78` and `W_birth >= 100`: the mechanism is inert and
  turnover proceeds without the intervention.
- **G8 (completeness and determinism)** — 4 seeds x 2 histories x 4 arms x 2 loss conditions
  (64 rows) all present; re-running the first individual reproduces it exactly (`state_hash`
  included).

Two deterministic **unit tests** (not run gates) pin the internalized-information links: (1)
`rebuild(o)` copies the production words — the program's production rules equal the description's
bits 28–69 — for every acquisition priority; (2) `rebuild(o) == prog.program(priority)`
bit-for-bit. The claim passes iff G1–G8 all pass. Thresholds are not moved; this protocol may not
be edited after the first final seed.

## Boundary (stated up front)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down). Content self-production is not claimed (AC78). The
study shows the inherited recipe drives multi-cycle replacement of the physical components; it does
not show the organism invents the recipe, and it does not test recovery from destruction of every
usable copy (catastrophic analog, out of scope).

## Seeds

Finals: `4012, 4013, 4014, 4015` (4 seeds x 2 histories = 8 individuals per condition). Disjoint
from every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4011) and from
engineering families 0-23 and 8500-8799. Engineering seeds (0-7) are excluded.

## Anti-drift rules

- The runner creates `ac81_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac81.py`, `audit_ac81.py`, `replay_ac81.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac81_results_v1/pre_run_snapshot.json at freeze time)
