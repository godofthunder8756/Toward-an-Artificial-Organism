# AC74 engineering v1: the reconciled closure is fixed-world — a route move exposes a material→W→re-acquisition cascade

2026-09-17. `ac74_engineering.py`, `ac74_diagnostic.py`. **No protocol, no final seeds, no claim.**
Prerequisite measurement for the "world-accommodating architecture" question the AC71 fixed-world closure
leaves open.

## The question

AC71 froze the closure (majority-read register + load-bearing self-monitoring repair + 65,536-tick steady
state) in a **fixed** world: `MOVE=10^9`, so the route mapping never changes and re-acquisition is never
needed. Does the reconciled architecture *accommodate* a post-development world change — survive a route
move, keep its body/register, and re-acquire the moved route? Three configurations, in the AC71 world
(full yields, sticky damage, majority read, 16,384 ticks, move of channel 1 at t=8192):

| variant | re-acquisition machinery | result (6 individuals) |
| --- | --- | --- |
| A | AC71 as-is (`grow=t<512`, `activation=[t<DEV]*2`, one-way drop) | re-acquire **0/6**, die **4/6** (t≈8446) |
| B | deposit open (`grow=True`, `activation=[T,T]`), one-way | re-acquire **2/6**, die **4/6** |
| C | B + restore rule (AC16's two-way `AllocRestore`) | re-acquire **4/6**, die **2/6** |

Every gate AC16 opened helps, and each step is measured: A→B opens the deposit path (2 re-acquire), B→C
adds the restore rule (4 re-acquire). So the closure *can* be made world-accommodating — but not robustly:
2/6 (seed 2) still dies even at C.

## The residual failure, and its mechanism

Seed 2 dies at t=8446 with W=0, C=0, no routes, register `[F,T,F,F]` (the moved slot relinquished at
t=8229). The diagnostic trace shows the sequence:

1. **Move (8192)** → channel 1's correct port flips 1→0, the stored route (port 1) goes stale.
2. **Drop (8229)** — after the 6-failure streak, the organism relinquishes the moved slot (a paid
   7-replica write), material falls to ~54.
3. **Material-low trap.** Material ≤ 64 sets observation bit 1, which the program answers with **action 1
   (contact channel 1 for material)** — and this rule precedes the W-birth rule (action 6) in the stored
   priority. But the stale entry is *relinquished, not erased*: it persists for its 64-tick life, so
   `read(1)` still returns the stale port and the contacts **fail** for that whole window. Material does
   not recover; the program keeps choosing the failing contact.
4. **W extinction.** While the program loops on the failing contact, no action-6 birth fires; the core W
   sites age out (3→2→1→0 over ~7 ticks, t=8234–8241).
5. **No recovery path.** With W=0 there is no live W parent, so both W birth (needs a parent in bank 0)
   and the deposit path (`if len(parents):` in the frozen step) are closed. The organism cannot re-acquire,
   cannot rebuild W, and dies at 8446.

Seed 1 survives because its W dip bottoms at 1 (not 0) and action 6 fires again at t=8292 before the
stale entry's window starves it — the same cascade, narrowly escaped. Seed 0's economics never dip it
below the threshold.

## What this establishes and what it does not

**Establishes (engineering):** the AC71 closure is a fixed-world property. World-accommodation requires
joining the re-acquisition line (AC16's deposit activation + restore rule), and even then a named,
measured failure mode remains: **the stale-route persistence window** — relinquishment stops renewal but
does not erase the entry, so the material-low contact loop fails for the entry's full remaining life,
starving W to extinction and closing the deposit path (which needs a live W parent).

**Does not establish:** any claim, anything frozen, autopoiesis/consciousness/life. The precise fix
(e.g. erase the entry on relinquishment so the next contact is blind, or remove the deposit path's W-parent
dependency, or reprioritize W-birth above the material contact) is a design decision for the next study,
not decided here.

## Bounds

Engineering prerequisite. The measured quantities are survival, route correctness, W/C/B counts, register
state and per-tick action, in a declared world with a declared move.

## Artifacts

`ac74_engineering.py`, `ac74_diagnostic.py`. Related: `AC71_RESULTS_v1.md` (the fixed-world closure),
`AC16_RESULTS_v1.md` / `ac16.py` (the re-acquisition machinery joined here), `AC68_RESULTS_v1.md` (the
W/C decay cascade family this failure belongs to).
