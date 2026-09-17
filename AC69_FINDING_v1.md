# AC69 finding v1: the route lapse is a threshold mismatch, not capacity or timing

2026-09-16. This pins the open question left by `CASCADE_FINDING_v1.md` (renewal-timing failure).

## The mechanism, measured

Instrumenting `renew_alloc` in the AC67 closed arm showed the renewal is *not* starved of budget and is
*not* too late — it is **switched off**. From ~t=850 the renewal's `allowed` mask flips from
`[True, True]` to `[False, True]`: slot 0 is relinquished, so `renew_alloc` skips it and its entry ages
out (`life → 0`, bits cleared, unrecoverable).

Why slot 0 is relinquished: the register read is single-replica (`REGISTER_THRESHOLD=1`), so **one**
sticky-damaged replica of the register bit reads as "relinquished" and stops the renewal. But the repair
that would reset that replica is triggered by observation bit 2, which fires only at **≥ 4** minority
replicas (`ac9.observe`: `min(ones, 7-ones).sum() >= 4`). So there is a window — from the first damaged
replica (flips the read) until four accumulate (fires the repair) — in which the register is
"relinquished", the renewal is stopped, and the entry lapses. The two thresholds are **misaligned**.

## The fix, and the verified direction

Raising the register read to majority (`REGISTER_THRESHOLD=4`) aligns it with the repair trigger, and the
routes then stay held for the whole 4,096 ticks: `demand=[42,0]` (both entries alive), register
`[F,F,F,F]`, routes `[0,0]` throughout. This is the closure of gap (a) — the acquired function becomes
self-maintaining.

The other direction (lower the repair trigger to 1 so it resets single-replica damage immediately) would
also align them and keeps the register vulnerable rather than redundant — the choice between the two is a
design decision, not a correctness question.

## The tension this exposes

The two directions trade off the two goals the line has held separately:

- **Read at 1, repair at 4** (the AC67 configuration): the register is *vulnerable* — the repair loop is
  load-bearing (AC67's result) — but the same vulnerability makes a single damaged replica silently
  relinquish a route (gap (a)).
- **Read at 4, repair at 4** (the frozen majority): the register is *redundant* — routes are reliably
  held — but the repair loop is arithmetically inert (AC14's original finding).

There is no single threshold that is both vulnerable-to-damage and robust-to-noise. The reconciliation is
to make the *repair* as sensitive as the *read* (both at 1): the register still flips on one damaged
replica, but the paid repair now fires on the same event and resets it within a tick, so the renewal
resumes and the route is held. That keeps the loop load-bearing (the register is genuinely at risk) and
the function self-maintaining (the repair wins the race). This is the declared change for AC70.

## What this establishes and what it does not

Establishes: the route lapse is a **threshold mismatch** between the register read (1) and the repair
trigger (4), not a capacity or scheduling failure; aligning them holds the routes. This closes the
diagnosis of gap (a) with a measured mechanism and a verified fix direction.

Does not establish: the reconciled configuration (repair-at-1) end-to-end, which is AC70's test; any claim
about autopoiesis or consciousness.

## Artifacts

Diagnostics only (`renew_alloc` instrumentation, threshold sweep). No frozen study. Next: `ac70.py`
(repair-trigger = 1) with the full protocol/audit/replay/test discipline.
