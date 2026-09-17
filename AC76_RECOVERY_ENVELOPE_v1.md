# AC76 recovery-envelope probe: the catastrophic-corruption boundary and what (if anything) moves it

2026-09-17. Engineering diagnostic. **No protocol, no final seeds, no claim.** Follows the AC76
freeze, which established that ≥16-bit sudden corruption is economically unrecoverable (the corruption
idles the program while the paid re-instantiation starves). This probe asks the optional question the
freeze left open: does a **starvation buffer**, **staged regeneration**, or a **cheaper write** extend
that recovery envelope?

## Method

Three single-declared-change variants of the frozen `ac76.reg_from_priority` (re-instantiate the
126-bit program from the stored 4-bank priority description, paid per replica under the frozen
per-action cap, register bits excluded), each measured across a corruption-size sweep (8, 16, 32, 64
bits). The corruption is the AC76 intervention: at t=8192, flip the majority (4 of 7 replicas) of the
first N program bits to the wrong value.

| variant | change from frozen |
| --- | --- |
| `full` | none — the frozen re-instantiation (rewrite EVERY disagreeing replica, 4 per corrupted bit) |
| `majority` | cheaper write: rewrite only the minimum replicas needed to flip the majority back (1 per 4-of-7 flip, 4× cheaper); minority replicas left wrong |
| `staged` | full re-instantiation but sites ordered income-first: material rule (rule 1) then fuel rule (rule 0) before non-income rules |
| `buffer` | `full` plus extra material injected at the corruption tick (diagnostic: is material stock the binding constraint?) |

16,384 ticks, 1e-4 sticky-SET program-bank damage, the AC71 world. Endpoint is **recover-content**:
the individual completes the horizon AND the corrupted bits' majority reads correct at the end.

## A confound caught first (and corrected)

The first sweep used engineering seeds 0–3 and gave a misleading "4/8 recover at n=8" — because seed
2 (and many seeds in 0–23) die **naturally at t≈450–5000, before the corruption tick**, of the AC68
W/C bimodality, not of the corruption. Corrupting an already-dead body makes `still_wrong=nbits`
without exercising the recovery at all. The envelope below is re-measured on a **viability-clean
family** (7 seeds whose individuals all survive to t=8192, 14 individuals), and pre-corruption deaths
are reported separately, never folded into "failed recovery".

## Result (clean family, 14 individuals)

| variant | n=8 | n=16 | n=32 | n=64 |
| --- | --- | --- | --- | --- |
| `full` (frozen) | 12/14 | 4/14 | **0/14** | 0/14 |
| `full` + buffer 128 | — | 6/14 | 2/14 | — |
| `full` + buffer 256 | — | 10/14 | 2/14 | — |
| `majority` (cheaper) | 12/12 | 12/12 | **12/12** | 6/12 |
| `staged` (income-first) | 10/10 | 10/10 | 6/10 | 0/10 |

(`majority` has 2/14 and `staged` 4/14 pre-corruption deaths — see "two costs" below — so their
denominators are 12 and 10, not 14. `full` has 0/14 pre-corruption deaths.)

## Three answers, each measured not assumed

**1. A starvation buffer does not move the boundary.** Extra material at the corruption tick lifts
n=16 (4→10/14 at 256) but leaves n=32 at 2/14. The binding constraint at ≥32 bits is **not material
stock** — it is income collapse. The corrupted bits are the fuel- and material-acquisition rules
(bits 0–27), so the program earns nothing while it is corrupted; a buffer only delays the same
starvation. The frozen trace at n=32 shows why: the organism holds ~69 material at t=8191, and full
re-instantiation of 32 bits costs 128 writes, draining material to 0 in two ticks (t=8192–8193) with
no income to refill it. No feasible buffer (material cap is 256) covers 128 writes while metabolism
runs in parallel.

**2. The cheaper write is the mechanism that actually extends the envelope.** `majority` recovers 32
bits 12/12 and 64 bits 6/12 where `full` recovers 0/14. The cause is measured, not guessed: a
majority flip needs only **one** replica written per bit (4-of-7 → write 1 → 4 correct), so 32 bits
cost 32 writes, not 128, which fits inside the idle organism's ~68 material. The trace shows material
recovering (44→100) and income resuming (in_m=64 at t=8193) instead of hitting 0.

**3. Staged (income-first) regeneration does not help — and actively harms in the natural regime.**
`staged` recovers 32 bits only 6/10 and 64 bits 0/10, no better than `full`, and it introduces 4/14
pre-corruption deaths where `full` has none. Those deaths are **body collapse, not program failure**:
at death all 9 rules read correct (0 wrong-majority), but the write ordering shifts the action stream
into the AC68 bimodality branch (W/C decay, energy→0). Reordering the writes changes the program's
own action choices tick-by-tick, which changes the body trajectory — a real but not favourable
effect.

## Two costs of the cheaper write (reported, not hidden)

1. **It is majority-restore, not full re-instantiation.** `majority` leaves the minority replicas
   (3 per corrupted bit) wrong; the bank is majority-correct but not pristine. `full` rewrites all 4
   and returns 7/7. The decoded program — what the interpreter reads — is correct in both, but only
   `full` restores full replication.
2. **It loses the drift-prevention property.** `full` re-instantiation also prevents the gradual
   sticky-SET drift AC76 reported (holding 125–126/126 where the baseline drifts to 102–106), because
   it rewrites every disagreeing replica whenever the corruption observation fires. `majority` only
   writes a bit whose majority is already wrong, so sub-majority drift accumulates untouched: 2/14
   individuals die pre-corruption, where `full` has 0/14.

## Bottom line

The frozen AC76 boundary (≥16 bits economically unrecoverable) is real and is an **income** limit,
not a material-stock limit — that is why a starvation buffer cannot buy it back. The one thing that
extends the envelope is **making the write cheaper** (majority-only, 4× fewer writes), which pushes
recovery from ~16 to 32–64 bits. But it does so by trading two properties `full` re-instantiation
has: full replication (7/7) and drift prevention. So the honest statement of the limit stands with
one refinement: recovery past the self-repair threshold is bounded by the *cost per corrupted bit*,
and the cheap end of that cost (majority restore) reaches further than the faithful end (full
re-instantiation) at the price of leaving minority corruption and drift unaddressed. Recovery from
complete destruction remains out of scope, exactly as the goal says.

## Artifacts

`ac76_recovery_probe.py` (the three variants + sweep), `ac76_envelope_probe.py` (resource trace),
`ac76_viability_scan.py` / `ac76_envelope_clean.py` (the confound and its correction),
`ac76_cost_confirm.py` (write-cost causal trace), `ac76_staged_diag.py` / `ac76_staged_trace.py`
(the staged-death mechanism). Outputs in the matching `*.out` files.
