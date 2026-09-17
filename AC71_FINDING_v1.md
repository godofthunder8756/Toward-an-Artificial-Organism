# AC71 finding v1: the threshold mismatch was the single root cause — read-at-4 reconciles all three gaps

2026-09-16. The breakthrough this session has been moving toward.

## The result

With the register read at **majority (4)** — aligned with the repair trigger, and the same convention
the rest of the program bank uses — the AC67 closed arm, at the long horizon (16,384 ticks) across 6
seeds, shows all three gaps of `CLOSURE_BOUNDARY_v1.md` closed at once:

| seed | death | routes | demand | W | C | energy |
| --- | --- | --- | --- | --- | --- | --- |
| 0–5 | none (6/6) | both held | `[42,0]` | 3 | 2 | 118–125 |

- **Gap (a) — function lapse — closed.** Both acquired routes are held for the whole horizon
  (`demand=[42,0]`), instead of lapsing by ~t=891.
- **Gap (b) — body bimodality — closed.** No seed collapses at ~7,500; energy, W and C are stable
  throughout (no W/C decay cascade).
- **Gap (c) — register degradation — closed.** The register never reads "relinquished" (a lone damaged
  replica cannot flip a majority read).

## Why one change closes all three

The cascade of `CASCADE_FINDING_v1.md` was downstream of a single point of failure: the single-replica
register read (`REGISTER_THRESHOLD=1`). One sticky-damaged replica flipped the read to "relinquished",
the renewal stopped, the entry lapsed, contacts failed, `_drop` degraded the register, and the whole
organism cascaded into the W/C collapse. Reading the register by majority — the same convention the
program bank's rules already use — makes the decision state robust to single-replica noise, so the
renewal never stops, the routes never lapse, and the cascade never starts.

## The repair is still load-bearing (the closure survives)

At read-at-4 the `no_repair` arm still dies (deaths 382–539 across damage rates 1e-4–1e-3), but now by
the **observation-hijack** path: without repair the sticky damage sets the bank-0 corruption bit
permanently, the program loops on a cut repair action and neglects everything. The load-bearing role has
shifted from the decision register (read-at-1, AC67) to the **self-monitoring observation** (read-at-4).
So the organism still has a closure-of-constraints — the paid repair of its own program is causally
necessary — but the constraint it maintains is now the program's own corruption signal rather than its
decision state.

## What this establishes and what it does not

Establishes (engineering, 6 seeds, seed-0 no_repair): the three closure gaps share one root cause — a
read/repair threshold mismatch — and reading the decision state by majority closes all three while the
repair loop remains load-bearing through the self-monitoring path. This is the reconciled configuration
the line has been missing: a *robust* decision state and a *load-bearing* self-monitoring loop.

Does not establish: a frozen multi-seed study (the engineering seeds here are 0–5, and the no_repair
death is seed-0 only); autopoiesis; consciousness. Those are the next study's job.

## Artifacts

Diagnostics only. Next: `ac71.py` — read-at-4, the full protocol/audit/replay/test discipline, fresh
seeds, gates on (i) routes held at 16,384, (ii) no bimodality, (iii) no_repair death by hijack.
