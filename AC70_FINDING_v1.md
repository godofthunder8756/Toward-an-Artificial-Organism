# AC70 finding v1: vulnerable-vs-reliable is a real tension — the resolution is aligned thresholds + sufficient damage

2026-09-16. Follows `AC69_FINDING_v1.md`.

## The two fix directions, both measured

1. **Register read at majority (4).** Aligns the read with the repair trigger. Routes held for the full
   4,096 ticks (`demand=[42,0]`, both entries alive). But this is AC14's configuration: the register is
   protected by 7-replica redundancy, so the repair loop is arithmetically inert.
2. **Repair trigger at 1.** Keeps the single-replica read (vulnerable) but makes the paid repair fire on
   the same event. Routes held to ~2,048, but route 1 still lapses by ~3,072 — this time by **repair
   thrashing**: the program spends its action budget repairing single damaged replicas and under-serves
   the renewal, so the entry ages out while the register itself stays intact (`[F,F,F,F]`).

Neither single-threshold change closes gap (a) *and* keeps the repair load-bearing.

## The tension, stated

The decision state (register) is simultaneously asked to be (i) **vulnerable** — so that its repair is a
causally load-bearing constraint, the AC67 closure — and (ii) **reliable** — so that single-replica noise
does not silently relinquish an entry, the gap (a) failure. A 7-replica majority read makes it robust but
inert; a single-replica read makes it sensitive but unreliable; and making the repair as sensitive as the
read makes the program thrash. No single read threshold satisfies both.

## The resolution direction

Decouple the two demands: keep the **majority read** (robust — a lone damaged replica does not relinquish
a route), and make the damage **persistent and frequent enough** that even a majority read eventually
flips, so the paid repair is still causally necessary rather than inert. Concretely: read threshold 4 +
non-self-reversing damage at a rate where ≥4 replicas of a register bit accumulate within the horizon —
the register is then robust to single-replica noise (routes held) *and* genuinely at risk from sustained
corruption (repair load-bearing). The two parameters (read threshold, damage rate) must be chosen
together and declared, exactly as AC14's option-1 requirement said, but now with the threshold mismatch
of AC69 explicitly resolved.

## What this establishes and what it does not

Establishes: gap (a)'s root cause is a read/repair threshold mismatch; the two single-threshold fixes
each fail in a measured way; the reconciliation is a two-parameter design (majority read + sufficient
sustained damage), not a one-constant fix.

Does not establish: the reconciled configuration end-to-end (the next study); autopoiesis; consciousness.

## Artifacts

Diagnostics only. Next: the two-parameter study — read at 4, damage rate swept to find where the register
flips under repair vs not, with routes held throughout.
