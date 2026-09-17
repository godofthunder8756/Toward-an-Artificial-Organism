# AC79 engineering v1: description maintenance — the turnover does not need a hidden pristine backup

2026-09-17. `ac79_engineering.py`. **No protocol, no final seeds, no claim.** Engineering only.

This is a re-scope of the "description maintenance" task. That task was premised on the priority
being **self-produced**; AC78 falsified that premise (the production signal is a locked,
path-dependent fixed point). The task's core survives the falsification because it is independent
of where the priority's *content* comes from: AC76's frozen turnover stores the 8-bit priority in
dead bank 1, where the damage stream never reaches it and no action repairs it — a **hidden
pristine backup**, which the goal explicitly rules out as evidence of endogenous reconstruction.
That gap is AC76's own listed caveat ("the description's own maintenance … is unscoped").

## The question, re-scoped to what is live

Can the 8-bit priority description be stored in the vulnerable substrate, **put in the damage
stream**, and maintained through the organism's own paid vulnerable machinery — so the
compressed-description turnover does not rely on a hidden pristine backup?

This does **not** require the priority to be self-produced. It requires the *reference* for
turnover to be as vulnerable and as paid-maintained as the program it re-instantiates.

## The mechanism (single declared change from AC76)

1. The description (`traces[1,:8]`, 8 bits × 7 replicas) receives the same **sticky** 1e-4 damage
   as the program, from an independent stream.
2. When the program's own corruption observation (obs bit 2) fires, the re-instantiation step first
   repairs the description's minority replicas to its 7-replica majority (paid, same primitive,
   same per-action cap), then re-instantiates the program from the repaired description.

The description maintenance therefore *rides* the program's corruption-triggered re-instantiation.
This is conservative, not arbitrary: the program is 16× larger than the description, so it degrades
16× faster and its corruption signal fires long before the description could approach a majority
flip (see the boundary below).

## Arms

| arm | description in damage stream | description repaired | program re-instantiation |
| --- | --- | --- | --- |
| `maintained` | yes | yes (paid) | yes |
| `pristine` | no (= AC76 as-is) | — | yes |
| `unmaintained` | yes | **no** | yes |
| `no_repair` | yes | no | loop cut (AC76 load-bearing control) |

Intervention: at t=8192, flip the majority of program bits 0–7 (the AC76 intervention). 16,384
ticks, engineering seeds 0–7 × 2 histories. `pristine` is AC76's `regen` arm exactly (frozen
`reg_from_priority`, no description damage), so its recovery is a built-in reproduction of AC76.

## Measured result

Viability scan (no corruption): 12/16 individuals alive at t=8192 — the 4 pre-corruption deaths
are the known AC68 W/C bimodality on engineering seeds, bucketed separately per the repo rule.

Among individuals alive at the corruption tick:

| arm | recover (flipWrong = 0) | description intact (decoded = original priority) | survive to horizon |
| --- | --- | --- | --- |
| `maintained` | **12/12** | **12/12** | 12/12 |
| `pristine` | 12/12 (2 die later at 11275, natural) | 14/14 | 12/14 |
| `unmaintained` | **0/12** | 0/12 (descValid = 0) | 0/12 (deaths 8327–8423) |
| `no_repair` | — (dead before t=8192) | — | 0/16 |

The contrast is clean and not bimodal-noise-dependent:

- **`maintained` recovers exactly as well as `pristine`.** The program's 8 corrupted bits are
  re-instantiated to correct in 12/12 (identical to the AC76 re-instantiation from a pristine
  description), and the description itself stays correct (decoded priority = original in 12/12).
  The description maintenance is **sufficient** — the turnover does not need the hidden backup.
- **`unmaintained` fails 12/12.** Under sticky 1e-4 damage the 56 description replicas degrade
  (~80% flipped by mid-horizon), the decoded priority is no longer a valid permutation (descValid
  = 0), re-instantiation silently refuses (the `sorted(priority) != range(4)` guard), the frozen
  majority-restore cements the t=8192 corruption, and every individual dies 8327–8423 — the AC76
  `baseline` death signature. The description maintenance is **necessary (load-bearing)**.

## The boundary: the description is the terminal, non-regenerable reference

Description maintenance is majority-restore of an 8-bit value — the same preventive primitive as
the program's repair, which AC61 showed **cements** a flipped majority. So the description has no
turnover of its own: corrupting its majority past 4-of-7 would be cemented, because there is no
more-internal description to re-derive it from. The description is the *smallest self-encoding*,
so its corruption is the "catastrophic destruction" the goal already scopes out — not a hidden
backup.

Under natural damage this boundary is never reached: the description's 56 replicas accumulate
~0.006 flips/tick, and re-instantiation fires every ~45 ticks (the program's corruption signal),
so the probability that any single description bit reaches a 4-of-7 majority flip before a repair
is ~2e-5 over the horizon. The description is vulnerable and maintained, yet its majority stays
correct — which is exactly what "maintained through paid vulnerable machinery, not a hidden
pristine backup" requires.

## The one economic caveat

Description maintenance is a real paid write (energy + material per repaired replica). The cost is
small (~0.006 writes/tick vs the program's ~0.09 and a 64/tick material income), but it slightly
shifts the AC68 bimodal collapse: `maintained` shows 4 pre-corruption deaths where `pristine`
shows 2, and the collapse tick of a borderline seed moves (4518 vs 5040 in the 3-seed pass). This
is the documented "stochastic stress decides which" cliff sensitivity, not a systematic survival
cost — in the no-corruption control `maintained` (12/16) actually completes marginally more often
than `pristine` (10/16). A frozen study should gate on recovery and description integrity (the
clean endpoints), and report survival as a bimodality-aware lower bound, not an exact count.

## The answer

**Yes, and it is a positive re-scope, not an archive.** The compressed-description turnover does
not require a hidden pristine backup: the description can be put in the same damage stream as the
program and maintained through the organism's own paid vulnerable machinery, recovering the
program as well as the pristine-reference version (12/12) while the unmaintained control degrades
and dies 12/12. This closes AC76's last unscoped caveat for the turnover mechanism itself — with
the correct, honest boundary that the description is the terminal reference whose own
past-majority corruption is unrecoverable (the "complete destruction" analog).

## What this does not establish

Nothing here bears on content self-production (AC78: still blocked — the priority's content remains
externally supplied). It establishes only that the *storage and maintenance* of the description is
endogenous. Autopoiesis/consciousness/life claims are out of scope.

## Bounds

Engineering prerequisite. No protocol, no final seeds, nothing frozen. Measured quantities: program
recovery (`flipped_still_wrong`), description integrity (decoded-vs-original priority), and
survival, in the AC76 world (PORTS=4, YIELD 64/64, sticky 1e-4 damage, t=8192 majority-flip of
program bits 0–7), engineering seeds 0–7, disjoint from every frozen family (1000–3400, 5100–5507,
3000–3003) and from AC78's 8500–8799. The frozen AC76 study re-audits clean (all 5 gates, no hash
drift) as of this session.

## Artifacts

`ac79_engineering.py`. Related: `AC76_RESULTS_v1.md` (the turnover whose caveat this closes),
`AC76_ENGINEERING_v1.md`, `DEPENDENCY_AUDIT_v1.md` (the internal-template causal-dependency
requirement), `AC78_ENGINEERING_v1.md` (the falsified self-production premise this re-scopes away).
