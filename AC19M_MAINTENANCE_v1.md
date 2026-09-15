# AC19-M: the maintenance half, diagnosed — the route is the register's occupancy, not corruption

2026-09-15. `ac19_maintenance.py`, `ac19_ledger.py`, `test_ac19_m.py`. Diagnostic. **No protocol, no
final seeds, no claim, nothing frozen.** This closes the open item AC19 left: *both register-cut arms
died by an unidentified route.*

## The recorded next measurement, and its result

AC19's record named the next step exactly: **register-cut vs register-cut with flip events suppressed.**

| arm | corruption on | register damage rate 0 |
| --- | ---: | ---: |
| `two_way` | 4/4 alive | 4/4 alive |
| `two_way_protected` | 4/4 alive | 4/4 alive |
| `two_way_no_repair` | **0/4** | **0/4** |
| `two_way_protected_no_repair` | **0/4** | **0/4** |

**The corruption is excluded.** With the register damage rate set to zero — no flip events at all — the
cut arms still die, 0/4, exactly as before. The route is structural to the repair cut, not caused by
damage. The hypothesis AC19's record leaned toward is dead, and it took ten seconds to kill.

## Naming the route

The ledgers separate the two arms cleanly (4 seeds, 4096 ticks each, totals):

| ledger entry | live `two_way` | cut `two_way_no_repair` |
| --- | ---: | ---: |
| `active` (ticks the organism acted) | **16384** (= every tick) | **6156** |
| `memory_writes` | 10346 | 4147 |
| `deposits` | 92 | 17 |
| `W_birth` | 1488 | 557 |
| `C_birth` | 252 | 114 |
| `converted` (particles → energy) | 4450 | 1938 |
| `particle_export` | 0 | **148** |
| `spent_e` / `spent_m` | 35367 / 21959 | 15760 / 10718 |
| demand at the end | `[[21,0],[42,0],[42,0],[21,0]]` | **`[[0,0],[0,0],[0,0],[0,0]]`** |

The live arm acts on **every** tick. The cut arm acts on 38% of them, and its register ends **empty** —
demand all zeros, bindings and expirations equal, writes roughly halved — while its sites are exported
(`particle_export` 148 against 0).

**The route: without the repair action the register empties, an empty register stops driving activity,
and the organism winds down — fewer conversions, fewer births, less spent — until it dies.** Repair is
load-bearing not for the *bits* but for the *activity*.

## What this means for AC14's "arithmetically inert" finding

AC14 concluded that the frozen world's repair loop was structurally present but arithmetically inert:
seven-fold replication plus self-reversing XOR damage meant the decision state was never at risk. That
finding was about the state's **integrity**, and it stands.

AC19-M shows the two halves are not in tension — they are about different things. With corruption
present, integrity is indeed never at risk. But the repair *action* is what keeps the register
**occupied**, and occupancy is what drives the organism's activity; remove the action and the organism
stops running whether or not anything is corrupt. So the closure question "is the decision state a
maintained constraint inside the loop?" has a sharper answer than either study alone: **the state's
integrity is not load-bearing, but its occupancy is.**

## What this does and does not establish

- **Establishes**: the death route of AC19's cut arms (activity collapse from an emptying register), the
  exclusion of corruption as the cause, and the reason AC14's inertness result and AC19's mortality
  result can both be true.
- **Does not establish** any new claim about the organism, and it is not offered as one. This is a
  diagnosis of an existing exploratory result, on four seeds, with the exploratory module unchanged.
- **Not autopoiesis, not closure, not life.** "Load-bearing" here means: removing an action changes
  whether the machinery keeps running. Nothing about experience or understanding, and nothing that
  upgrades AC19 from exploratory status.
- **Nothing is frozen.** No protocol, no declared seeds, no results directory.

## Next

The maintenance half's remaining question is whether the *occupancy* finding can be made into a
pre-registered claim rather than a diagnosis — most naturally: does a register whose occupancy is
maintained by repair keep the organism active longer than one whose occupancy is not, **with corruption
absent** so the integrity channel is switched off by construction? That has a clean control (the
corruption-off condition used here), a measurable endpoint (active ticks, or time to death), and no
dependence on the damage model that AC19 spent its effort on.

## Artifacts

`ac19_maintenance.py`, `ac19_ledger.py`, `test_ac19_m.py`, `/tmp/ac19_maintenance.json`,
`/tmp/ac19_ledger.json`. Related: `AC19_ENGINEERING_v1.md` (the open item), `AC14_CLOSURE_v1.md` (the
inertness finding this complements), `ac19.py` (unchanged).
