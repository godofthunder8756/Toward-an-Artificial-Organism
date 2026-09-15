# AC28: six-region maintenance chemistry

2026-09-15. `ac28_regions.py`, `test_ac28.py` (15 tests), `ac28_regions_v1.json`. **Chemistry for the
scaled world's six needs. No acquisition, no register, no scaled body for the frozen constituents,
no protocol, no final seeds, nothing claimed about the organism.**

## What the AC24–AC27 sequence established, and what it implied here

The frozen world does not fail for want of signals — `ac9.observe` produces eight. It fails because
exactly one W region is active per individual (so the other region's urgency bit is never set) and
because observation bit 5 cannot be set. Two of four rule positions are structurally mute, which is
why the frozen controller is worth 1.00 effective bit rather than 4.58 (AC24), why mere co-occurrence
is not enough (AC26), and why exact pair presentations are what make an order learnable (AC27).

So the scaled world does not need new *kinds* of signal. It needs **six independently varying
maintenance needs of one kind** — six W regions, each a group of four parent sites whose occupancy
can fall toward expiry on its own schedule. Each rule position conditions on one region and acts on
it, and the order of the six positions is the acquired object: 720 orders, 9.49 bits.

## Verified in this module

| check | result |
| --- | --- |
| signal word derived from body state | `000000` healthy; `000100` after draining a site in region 2 |
| an empty region is not a need | no signal (matching the frozen rule that urgency needs `life > 0`) |
| six regions independent | draining region k sets bit k and nothing else |
| birth costs the frozen price | 4 material + 2 energy, child life 64, parent untouched |
| birth preconditions | needs a parent; needs an empty slot; a failed payment spends nothing |
| **conservation, every tick** | life-count `N + births − expiries`, energy `E − spent_e`, material `M − spent_m`, and `spent_m == 4 × births` |
| conservation under stress | 300 driven ticks with regions drained and refilled at random, and random action orders — identities never broken |
| **the criterion** | exact-pair demand schedule over six region rules → **720 classes, 9.49 bits** |
| control: one region urgent at a time | 1 class, **0.00 bits** (the AC25 singletons-only result) |
| control: the frozen shape (a program signal co-occurring with one region) | 2 classes, **1.00 bit** (reproducing AC24/AC25/AC26 in this new machinery) |
| action-space hygiene | region actions 10–15, disjoint from the frozen 0–9, so dispatch is unambiguous |

The two controls matter more than the headline. The same code that reports 720 for the new design
reports 0.00 and 1.00 for the two failure modes, on the same measurement — and the 1.00 reproduction
is the fourth independent route to the frozen world's number.

## Reused, and changed — stated plainly

**Reused verbatim:** `ac4.pay` (cost accounting), `ac4.empty_event` (ledger keys), the birth price of
4 material + 2 energy with child life 64, the expiry rule (a site at life 1 is lost), the death check
(`energy < 1`), and the *form* of the balance identity.

**Changed deliberately:** the frozen action 6 births into **all** demanding groups at once, whereas
here each region has its own maintenance action. That is the refinement six distinct rule positions
require — and it means **this chemistry is a parallel of the frozen one, not a reducible special
case**. I cannot claim bit-for-bit reducibility here and do not: the frozen world's aggregate action
has no one-action analogue in the scaled world. This is the first extension in the sequence where
the reducibility discipline does not apply, and it is recorded rather than glossed, because the
whole point of that discipline is to notice when it stops holding.

## Limits of the driven run

The driven run (22 ticks, 2 births, conservation intact) is a **smoke test**, not an organism:

- **The demand is imposed by the harness**, not emergent. It verifies that this chemistry's signal
  set *can* satisfy the AC27 criterion; making the six needs fluctuate into exact pairs from the
  world's own dynamics is a different job and is not done.
- **Only two births occurred**, because at acquisition each region has exactly one empty slot, and
  only actions 10 and 11 fired — a structural consequence of the star-shaped pair enumeration
  (AC27) combined with an identity action order. Sustained maintenance needs region growth or site
  recycling, which is the organism's business, not this module's.
- **The order is set by the harness.** Nothing here acquires, stores or retains an order; the
  acquired object is supplied as a permutation of six positions.

## Not built, plainly

- **No acquisition.** No register, no memory renewal, no retention, no re-acquisition. The
  developmental claim — that this world's order structure is *learnable* and *retainable* — is not
  tested here; only that the structure exists to be learned.
- **No scaled body for the frozen constituents.** The C = 6 declaration of AC22 covers six
  constituent needs; this module supplies six *regions*, one kind of need. Reconciling the two
  (whether regions are the six constituents, or the constituents are a different six) is an open
  design question, not a settled one.
- **No protocol and no final seeds**, and no claims. Every number is a property of synthetic demand
  words and a small body model.
- **Nothing about experience, understanding or life**, and nothing offered as evidence toward them.
- **The two endpoints the open item names** (random-fallback survival; retention of the acquired
  function) remain untouched — though the second is now visibly the next real question, since there
  is finally something worth retaining.

## The next step

Acquisition and retention in this world: a register the order can be written into, repaired when
corrupted, and re-acquired after a disruption — the AC16/AC18 shape, but over a six-position order
whose structure is now known to be real (9.49 effective bits) rather than nominal. Then a protocol
declaring the scale, the demand schedule, and the two endpoints separately, before any final seed.

## Artifacts

`ac28_regions.py`, `test_ac28.py`, `ac28_regions_v1.json`. Related: `AC27_SCHEDULE_v1.md`,
`AC26_SIGNALS_v1.md`, `AC25_CONFRONT_v1.md`, `AC24_FUNCTIONAL_v1.md`, `ac23_body.py`.
