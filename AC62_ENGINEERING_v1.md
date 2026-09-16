# AC62 engineering: the repair/re-acquisition complementarity is architecturally real but dynamically inert

2026-09-15. `ac62_engineering.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**

## The question

AC61 established that register repair is preventive, not curative — so repair (AC58) and re-acquisition
(AC57) are complementary mechanisms. AC62 asked whether that complementarity has a freezeable dynamic
consequence: under corruption that crosses the register's majority threshold (which repair cannot undo),
does an organism that also re-acquires retain more value than one that only repairs?

## What was measured

Two corruption designs, both on AC57's scaled body with the acquired order in the register:

1. **Continuous corruption + intermittent repair** (repair every K ticks, so the threshold can be crossed
   between repairs). Swept damage rate 0.005–0.02 and interval 25–100. The contrast (re-acquire vs
   repair-only) never resolved cleanly: p between 0.12 and 1.0, because a bit flip reorders the Lehmer
   code *non-locally*, so whether it harms the critical region is per-seed luck — some seeds catastrophic
   (up to 6 dead), most harmless.
2. **Single disruption** (a corruption event at mid-run flipping half the replicas, then freeze). This
   isolates the mechanism cleanly: repair-only freezes a *random* order, re-acquire restores the optimal
   order. Result: re-acquire == protected (67,930), repair-only only 65,453 / 68,386 — a 0–4% gap, p = 1.0.

## Why the contrast is inert

Corruption produces a *random* permutation, and the critical region (value 100) is the highest-stress
region — it is urgent almost every tick, so it is repaired regardless of its position in the order. A
random order therefore keeps the critical region alive nearly as well as the optimal one. The order's
value effect lives in the *rare-urgent* (low-stress) regions, which are low-value. This is the same
structural reason AC56 found the re-acquisition benefit negligible: the deadline-scheduling balance makes
a stale or corrupted order "good enough" because the thing worth protecting is exactly the thing that
protects itself by being urgent.

## What this does and does not establish

- **Establishes (negatively)**: the repair/re-acquisition complementarity, though architecturally real
  (AC61), is dynamically inert in this world — corruption causes too little value loss to make the
  recovery benefit resolvable. The complementarity would need a world where the critical region is
  *rare-urgent* (so a random order genuinely risks it), which is not the AC57 configuration.
- **Establishes (method)**: the single-disruption design cleanly isolates repair-freeze vs re-search, and
  is the right shape to reuse if a world where corruption is costly is ever built.
- **Does not establish**: any claim about the complementarity's behavioural effect; autopoiesis, closure,
  life.

## Bounds

No claim. Engineering prerequisite. The finding closes the question cleanly: the complementarity is real
but not freezable here, for a named reason.

## Artifacts

`ac62_engineering.py`. Related: `AC61_ENGINEERING_v1.md` (the complementarity), `AC58_RESULTS_v1.md`
(repair), `AC57_RESULTS_v1.md` (re-acquisition), `AC56_ENGINEERING_v1.md` (the same structural inertness
in the re-acquisition benefit).
