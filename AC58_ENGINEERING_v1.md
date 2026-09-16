# AC58 engineering: repair retains the acquired order — but corruption is abrupt, not gradual

2026-09-15. `ac58_engineering.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**

## The question

AC43 froze the maintenance line with corruption ABSENT (`reg_rate = 0` — AC14's integrity channel off by
construction). AC57 froze the developmental line. AC58 turns the integrity channel ON: the acquired order
sits in a replica-encoded register that is corrupted over the run, and asks whether paying to repair it
retains the acquired function.

## What was measured

AC57's scaled body (regime B, concentrated head + graded tail), order read back from a 10-bit × 7-replica
majority-4 register each tick. Arms: protected (no damage), repaired (damage + repair each tick at 1
energy), unrepaired (damage only). Damage rate swept.

| damage rate / tick | repaired − unrepaired p | median | dead |
| --- | --- | --- | --- |
| 0.0005 | 1.0 | 0 | 0 |
| 0.001 | 0.50 | 0 | 2 |
| 0.002 | 0.031 | 12 | 3 |
| 0.003 | 0.0010 | 14,932 | 5 |
| 0.005 | 0.0005 | 18,295 | 5 |

Two findings:

1. **Repair retains the order exactly.** repaired == protected (median difference 0): continuous repair
   restores every flipped replica, so the read-back order is always the acquired one. The repair cost is
   invisible only because the world's energy is abundant here (production ≫ drain + repair).
2. **Corruption is abrupt, not gradual.** Below rate ~0.001 nothing happens; above ~0.003 the unrepaired
   register corrupts catastrophically and the organism collapses (up to 5/12 dead). There is no stable
   "partial value loss" regime.

## Why corruption is abrupt (a real, worth-keeping observation)

The register's structure makes degradation non-local: a stored bit flips when 4 of its 7 replicas turn
(an abrupt majority flip), and the 10-bit Lehmer code is positional — a single flipped bit maps the
stored code to a *different permutation*, often one that moves the critical region (value 100) to the
back. Under concentrated value, neglecting the critical region crashes production, and energy falls below
drain, so the organism dies. Degradation is therefore a threshold crossing into collapse, not a smooth
loss.

## Consequence for the claim

The repair claim is a **survival/integrity** claim, not a maintenance claim: repair retains the order and
thereby prevents corruption-induced collapse, rather than preventing a gradual loss. That is the honest
shape of AC14's integrity channel, and it is freezeable as such — endpoint production (with death as
collapse), arms {repaired, unrepaired, protected}, gates resolvability + effect + retention
(repaired ≈ protected) + repaired-arm stability (0 dead), with the unrepaired arm's death count reported
descriptively. A gradual (0-dead) maintenance variant would need either a non-positional encoding or a
moderate value spread, both left untested.

## Bounds

No claim. Engineering prerequisite. Not autopoiesis, closure, or life.

## Artifacts

`ac58_engineering.py`. Related: `AC57_RESULTS_v1.md` (the acquired order), `AC43_RESULTS_v1.md` (the
maintenance line, corruption absent), `ac29_register.py` (the register).
