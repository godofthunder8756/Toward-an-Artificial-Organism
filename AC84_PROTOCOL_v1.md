# AC84 protocol v1: component turnover reported unconditionally

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering record
(`AC84_ENGINEERING_v1.md`, `ac84_eng_probe.py`, `ac84_eng_verify.py`, `ac84_eng_scan.py`,
`ac84_eng_broad.py`). Final seeds declared below, disjoint from every engineering seed and prior
frozen family.

SOURCES (declared): ac84.py ac80.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC84_PROTOCOL_v1.md

## Claim

The organism's physical components — the W catalysts, C energy-converters and B boundary — are
**constructed, used, and replaced across multiple turnover cycles**, driven by the internally
retained, maintained production recipe (AC80's 78-bit description). Unlike AC81, this claim is
reported **unconditionally**: turnover (births), use (repair writes, energy conversion) and
replacement (births >= the slot complement) are scored on **every individual in the cohort, dead or
alive** — no `completed` filter. The t=8192 kill intervention is dropped entirely; the components
turn over continuously with no intervention, and the horizon (4096 ticks) sits inside the pre-
collapse window, so the AC68 W/C collapse does not dominate the cohort. If it still kills some
individuals, that is reported as a finding about the body's fragility, not used as a licence to
gate.

This is a component-level claim, not an autopoiesis/consciousness claim. Content self-production is
untouched (AC78): the recipe's content is inherited at acquisition; this study shows the inherited,
maintained recipe drives multi-cycle replacement of the physical components.

## The mechanism (no new primitives — reuses AC80 unchanged)

- The description (`traces[1,:78]`, 7 replicas/bit) stores the five rule words (5x14=70 bits)
  including the three production rules — W-birth `(1,64,6)`, C-birth `(1,128,7)`, B-birth
  `(1,256,8)` — plus the 8-bit permutation.
- During life the 126-bit program is re-instantiated from this description by the generic decode
  `rebuild` (AC80); `prog.program` survives only in the observer.
- The production rules fire on the observation bits (W-low=6, C-low=7, B-low=8), paying the frozen
  prices to birth replacements when a component dies (W life 64, C 128, B 256). This is the turnover
  loop: component dies -> observation bit -> production rule -> replacement born.
- The description is maintained against the sticky damage stream by its own trigger
  (`DESC_TRIGGER=2`, AC80): the re-instantiation fires on (obs bit 2) OR (description minority
  count >= 2), first majority-restoring the description (paid), then rebuilding the program.

The claim "replacement uses internally retained information" rests on three links (all testable):
(a) the production rules are the description's words 3-5 (unit test: `rebuild` copies them);
(b) the description is maintained (internalized keeps 78/78, unmaintained degrades);
(c) the maintenance is load-bearing (unmaintained degrades and its turnover is not sustained;
no_repair dies).

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=4096`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick, sticky description damage (`|=`) at 1e-4
per replica per tick from an independent stream (`rng1 = default_rng([seed,1609])`). No route move,
no kill intervention, no program corruption. `DESC_TRIGGER=2`.

Horizon rationale (engineering, `ac84_eng_probe.py`): at 4096 ticks the internalized arm's turnover
is ~20x the complement in survivors and ~5x in the earliest-collapse individual, while the collapse
kills 8/64 engineering individuals (vs 24/64 at 16384, the AC68-dominated regime). The horizon is
therefore inside the pre-collapse window, and the residual collapses are reported as fragility.

## Arms

| arm | description in damage stream | description repaired | decode |
| --- | --- | --- | --- |
| `internalized` | yes | yes (paid, own trigger) | generic |
| `unmaintained` | yes | **no** | generic |
| `no_repair` | yes | no | loop cut (AC80 load-bearing control) |

`pristine` (AC80's hidden-backup arm) is deliberately dropped: its description is never damaged, so
it is not a test of the maintained recipe, and in engineering its early W/C collapses (t=439-673)
make its turnover non-unconditional, muddying the contrast.

## Endpoints (per individual)

`completed`, `first_dead`, turnover (`W_birth`, `C_birth`, `B_birth` totals over the horizon), use
(`writes` repair, `converted` energy), `particle_export`, component populations at end (`W_live`,
`C_live`, `B_live`), `routes` (endpoint), `first_acquire` (per-key tick first bound),
`first_route_loss` (tick a held route first lapsed), `demand`, `description_correct` (of 78),
`description_same` (decoded permutation == original priority), `energy`, `material`, `fuel`,
`state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Turnover and use are scored on **every individual** — no `completed` filter. The only
survivor-scoped gate is G5 (description integrity), because the paid description maintenance stops
at death (AC79's post-mortem degradation); that is a fact about the description, not the turnover.

- **G1 (turnover, unconditional)** — every `internalized` individual (dead or alive) has
  `W_birth >= 16`, `C_birth >= 4`, `B_birth >= 20`: each component class is fully replaced at least
  once over its complement (16 W slots, 4 C slots, 20 B sites). Multiple turnover cycles (the
  stronger form) is reported per individual as `births / complement` — healthy individuals ~20x,
  the earliest collapse ~1.3-1.9x — and is descriptive, not gated.
- **G2 (use, unconditional)** — every `internalized` individual has `writes > 0` (W repaired),
  `converted > 0` (C converted), and both routes bound during development (`first_acquire[0]` and
  `first_acquire[1]` non-None): the acquired organization is built and the components are used.
- **G3 (loop load-bearing)** — every `no_repair` individual dies (`completed` False): the
  re-instantiation loop is load-bearing (AC80 control).
- **G4 (recipe degrades without maintenance)** — every `unmaintained` individual has
  `description_correct < 78`: the recipe content degrades when unmaintained.
- **G5 (recipe maintained in survivors)** — every `internalized` completer has
  `description_correct == 78`: the production recipe is retained. (Survivor-scoped; see above.)
- **G6 (completeness and determinism)** — 4 seeds x 2 histories x 3 arms (24 rows) all present;
  re-running the first individual reproduces it exactly (`state_hash` included).

The claim passes iff G1-G6 all pass. Thresholds are not moved; this protocol may not be edited
after the first final seed. Reported but not gated: internalized survival (bimodality-aware lower
bound — the AC68 collapse kills some individuals even at 4096), unmaintained survival, and B
retention (routes, `particle_export`, `first_route_loss`), which lapses in collapsing individuals.

## Boundary (stated up front)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down). Content self-production is not claimed (AC78). The
study shows the inherited, maintained recipe drives replacement of the physical components; it does
not show the organism invents the recipe, and it does not test recovery from destruction of every
usable copy (catastrophic analog, out of scope). The bank rules are still synthesized by the
architectural convention (AC80's residual).

## Seeds

Finals: `4020, 4021, 4022, 4023` (4 seeds x 2 histories = 8 individuals per condition). Disjoint
from every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4019) and from
engineering families 0-127 and 8500-8799. Engineering seeds are excluded.

## Anti-drift rules

- The runner creates `ac84_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac84.py`, `audit_ac84.py`, `replay_ac84.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac84_results_v1/pre_run_snapshot.json at freeze time)
