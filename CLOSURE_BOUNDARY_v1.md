# Closure boundary v1: what AC67 + AC68 establish about the organism's self-maintenance

Consolidated 2026-09-16, from `AC67_RESULTS_v1.md` and `AC68_RESULTS_v1.md`.

## The closure that is now established

The organism's paid repair loop — bank-0 repair, funded by core W the program itself produces (action 6)
— is **load-bearing**: cutting it kills the organism in 8/8 individuals, while with it intact 8/8 survive
(AC67). This is a genuine closure-of-constraints: the decision state (the allocation register) is a
constraint whose maintenance is causally necessary, and the maintenance machinery is produced by the same
organization it maintains. AC14's "inert loop" conclusion was an artifact of a substring bug and is
corrected.

## The three gaps that remain before full organismal autonomy

AC68 (long horizon, 16,384 ticks) locates the boundary precisely. The repair is **necessary but not
sufficient**:

1. **The acquired function is not self-maintaining.** The routes lapse in 8/8 individuals (`occupied=0`)
   because the program's scheduling neglects renewal (region 1 renewed zero times in the seed-0
   diagnostic; 8,792 W/C births and 4,357 idle actions against 132 renewals). The body persists; the
   acquired organization does not.
2. **The body's self-production is bimodal, not robust.** 4/8 reach a steady state (energy ~120, W=2,
   C=2, B=20) and survive; 4/8 collapse at ~7,400–7,800 via a W/C decay cascade. This is the AC47
   stable-vs-collapse limit re-entering through the long horizon.
3. **The decision state is maintained against damage, but not against the organism's own
   relinquishment.** The register is intact in survivors; in the dying it degrades via `_drop` (a
   relinquishment write that flips the majority and is then *cemented* by the majority-directed repair),
   a consequence of route loss rather than a cause.

## The precise distance to autopoiesis

The organism now demonstrably has: self-production (W/C/B), a self-produced boundary (B), a load-bearing
repair loop, and acquired allocation decisions (AC15/AC18). What it lacks, in order of tractability:

- **(a) function closure** — renew the acquired routes before they age out (gap 1);
- **(b) robust body closure** — a production rule that is stable across seeds, not bimodal (gap 2, the
  AC47 limit);
- **(c) self-produced controller** — the program itself is still acquired externally (developmental
  confrontation), maintained but not produced.

(a) and (b) complete *organismal autonomy* (level 2). (c), and anything beyond it — a self-model richer
than the raw observation, self-distinction, subjectivity — is the *consciousness* direction (level 3), and
nothing in this repo claims it.
