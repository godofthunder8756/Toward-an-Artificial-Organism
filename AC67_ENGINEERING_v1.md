# AC67 engineering v1: the repair loop IS load-bearing — and AC14's "inert loop" was an artifact

`ac67.py --engineering` (seeds 0,1,2, two histories each, 4096 ticks).

## The bug that invalidates AC14's conclusion

AC14 concluded the closure loop was "structurally present but arithmetically inert" because its
`no_repair` arm behaved identically to `closed`. That identity was **by construction**, not a finding:

`arm_parts` matched `'_no_repair' in arm`, but the arm is named `'no_repair'` — no leading underscore —
so the substring test never matched. The `no_repair` arm therefore ran with the repair **enabled**,
i.e. it *was* the `closed` arm. Only `protected_no_repair` (which does contain the underscore) actually
cut the repair, and it died — which AC14 recorded as an "unexplained anomaly".

With `'no_repair' in arm`, the cut is applied to the intended arm, and the loop is exercised for the
first time.

## The one declared change, and why it is enough

AC14's option 2 was a **non-self-reversing damage model** — "the faithful way to model a constraint that
is maintained rather than merely perturbed, and the more interesting option because it makes repair
load-bearing by construction." AC67 makes exactly that change and nothing else: the program-bank damage
line becomes a sticky SET (`b.traces[0,:126] |= core_flips`) instead of a toggle (`^=`), so a damaged
replica stays damaged until the paid bank-0 repair rewrites it to the decoded majority. The register read
convention is single-replica (`REGISTER_THRESHOLD=1`), so the decision state is genuinely at risk the
moment one replica is set.

## Result (3 engineering seeds × 2 histories = 6 individuals per arm)

| arm | register (final) | first register flip | first death | alive | activity |
| --- | --- | --- | --- | --- | --- |
| `closed` | [0,0,0,0] | 174/798/216 | never | 6/6 | 1.000 |
| `no_repair` | [0,0,1,1] / [0,1,0,0] / [1,0,1,1] | 77/30/216 | 539/554/2842 | 0/6 | 0.13–0.69 |
| `protected_closed` | [0,0,0,0] | 174/798/216 | never | 6/6 | 1.000 |
| `protected_no_repair` | [0,0,1,1] / [0,1,0,0] / [1,0,0,1] | 77/30/216 | 539/554/1381 | 0/6 | 0.13–0.34 |

Cutting the repair link:
1. **degrades the decision state** — the register reads "relinquished" in every `no_repair` individual
   and stays degraded to the end;
2. **propagates to the routes** — the allowance stops renewing the flagged slots, the 64-tick entries
   lapse, occupancy falls;
3. **kills the organism** — 0/6 survive, deaths 539–2842, activity collapses.

With the repair link intact, the register stays `[0,0,0,0]` in every individual, the routes are held,
and 6/6 survive. The causal order is right in every individual: `first_register_flip` (30–216) precedes
`first_death` (539–2842).

## The mechanism, measured

`program_bits_damaged` (majority-decode difference) is 0 in most `no_repair` individuals and 2 in one:
the **program** is protected by 7-replica majority redundancy and does not flip, while the **decision
state** (single-replica read) is sensitive to the first set replica. The loop's load is borne precisely
by the vulnerable decision state, not by the replicated program. This is the closure of constraints the
line has been reaching for since AC12: the decision state is a maintained constraint whose maintenance
(the paid bank-0 repair, funded by core W the program itself produces) is causally necessary for the
organism's continued functioning.

## What this does and does not establish

Establishes (engineering): cutting the repair link degrades the decision state and kills the organism
under sticky damage; the repair maintains it. The loop is load-bearing, not inert.

Does not establish: anything beyond this single declared mechanism change. No autopoiesis, no
consciousness, no optimality. The protected arms have a subtle semantics (their shadow register is not
in bank 0, so the paid repair cannot reach it — it degrades by the organism's own relinquishment writes
rather than by damage) and are scaffold controls only, not part of the primary claim.

## Next

`AC67_PROTOCOL_v1.md`, then final seeds on a fresh family (2600–2603), with the gates prespecified.
