# AC3: maintained energy conversion inside the controller–catalyst loop

2026-09-14. New engineering protocol before results. AC2 was verified progress;
the broad autonomy goal remains active. This version implements the C stage,
not the spatial boundary or autonomous learning of new dependencies.

## Claim and causal change

Replace direct collection of usable energy with collection of fuel. Fuel can
be converted to usable energy only by decaying converter constituents C. The
vulnerable acquired controller P chooses production of C; local W catalysts
enable that production; C supplies energy used to maintain both P and W.

A positive result must show paid C turnover, loss under production ablation,
rescue by C supply and by usable-energy supply, and continued W dependence when
energy is clamped. This is a designed reaction model and demonstrated policy,
not spontaneous metabolism, full autopoiesis or a novel learning mechanism.

## Representation and supplied policy

Four banks each hold512 bits with7 replicas. Banks0–1 encode256 four-bit policy
rows; banks2–3 hold1024 arbitrary payload bits. This larger representation
accommodates another observation and action; it is not a matched comparison to
AC2. The family still has only24 demonstrated priority permutations.

Observation bits: low fuel (<=8); low precursor (<=64); four bank-damage flags
(>=4 minority copies summed over a bank); low W (any bank has<2); low C (<2).
Demonstrations prioritize fuel, precursor, W synthesis, C synthesis, damaged-bank
repair by a history-specific permutation, then rest. Actions0=collect fuel,
1=collect precursor,2–5=repair banks,6=produce W,7=produce C,8=rest. Unused9–15
also rest. Every context is demonstrated once. No subsequent teacher feedback.

## Reaction laws and finite state

- W: four slots per bank, initial lifetimes32/48/64/0, maximum64. Each permits
  eight writes/action, cap32. Producing one W costs4 precursor+2 usable energy,
  needs local parent W, and is attempted once per bank by action6.
- C: four global converter slots, initial lifetimes64/96/128/0, maximum128.
  Action7 produces one C in an empty slot, needs W in bank0, and costs4 precursor
  plus4 usable energy. C is produced through W, not spontaneously by fuel.
- Each surviving C converts at most one fuel unit per tick, yielding8 usable
  energy. Conversion is bounded by fuel and available product capacity:
  min(C_count,F,floor((128−E)/8)). Product inhibition and transport to the shared
  energy store are supplied generic laws, explicitly not produced components.
- Action0 imports32 fuel (capacity64), not energy. Initial fuel32, energy64,
  precursor128; energy/precursor capacities128/256. Precursor import64.
- Living/decision cost1 energy. Each effective trace replacement costs1 energy
  and1 precursor; the displaced site becomes1 waste unit. Each W or C binds4
  material units; expiration releases4 units to exported waste. Fuel mass and
  fuel conversion waste are a separately conserved account.
- Tick: corruption; W/C age and expiry; declared rescues/clamps; autonomous
  conversion; if no usable energy then stop; otherwise choose and execute one
  action. A zero-energy body with fuel and C can restart computation through
  conversion before the next decision. Do not kill it prematurely merely for
  ending a previous action with E=0.

Live state: trace bits, W/C lifetime arrays, bounded fuel/energy/precursor and
termination. No target arrays, cached decoded policy, acquisition seed, or
observer histories enter the live step. Complete erasure resets ALL of this.
Generic code, memory addressing, sensing, molecular recipes and enclosure are
supplied. There is no spatially produced boundary yet.

## Arms

| Arm | Intervention |
| --- | --- |
| self | Vulnerable policy and all production/repair reactions |
| no_C | Block C production, free ineffective attempts |
| no_C_rescue | Block C production; external C additions keep count>=3, inventoried |
| no_C_energy | Block C production; externally replenish usable energy to128 each tick |
| no_W | Block W production, free ineffective attempts |
| self_energy | Replenish usable energy only; all production intact |
| no_W_energy | Block W production with same energy clamp |
| no_policy_write | Policy-bank trace replacements blocked and free |
| protected | Explicit protected acquired policy, identical reaction machinery |

## Pre-run sample and analysis

Seeds0–7, 4,096 ticks, p=0.0001/0.0002/0.0004 per copy per tick; all nine arms.
The rates target roughly1.4/2.9/5.7 expected copy flips per tick in the larger
representation. They are chosen before any run; no matched superiority claim
over AC2's smaller state. No pulse. Retain all216 rows. Independent acquisition
and corruption streams; identical corruption for paired arms, no random action
draws influencing physics. Snapshot source/test/protocol dependencies pre-run.

Report activity per planned tick, completion, raw and survival-weighted policy/
payload accuracy, internal W/C production, expiry and external additions,
fuel conversion, all resource ledgers, bank writes and periodic full-state
digests. Terminated runs freeze at their stop state; their raw information
score does not count as functioning. Completion means executing the planned
horizon, not a guarantee of future survival.

Descriptive paired95% bootstrap intervals,10,000 draws, seed20260914:
self−no_C activity; no_C_rescue−no_C activity; no_C_energy−no_C activity;
self−no_policy_write activity; self_energy−no_W_energy policy accuracy.
No multiplicity-corrected or confirmatory claim; all rates reported.

Engineering criteria per rate: self/protected/C-rescue/C-energy mean activity
>=0.9; self−no_C activity>=0.2; energy-clamped W-dependent policy accuracy
difference>=0.2; every self individual produces>120 W and>30 C, converts fuel,
and writes every bank; all technical tests/audits pass. Failures stay failures.

## Required discriminating tests

1. Fuel collection deposits zero usable energy directly.
2. No C means no conversion despite fuel; C+fuel can restore E from zero.
3. C production requires W,4M,4E and a free slot; no hidden converter births.
4. Acquired policy intervention can block C production without changing physics.
5. Without production all initial C expires by128, all W by64.
6. Material account includes free precursor, bound W/C, imports, waste and
   external constituents. Fuel account includes stores, imports, conversion
   waste and overflow. Energy account includes8×converted fuel, external
   clamps, living, writes, synthesis, final reserve; no energy created from M.
7. Erasure and protected-template rejection cover the expanded live state.
8. Exact sampled replays, rectangular seed coverage, paired environments, all
   row ledgers and recomputed means/intervals before interpretation.

## What remains outside this test

Produced boundary, spatial transport/retention, learned rather than demonstrated
priorities, developmental acquisition of dependencies, viable relinquishment and
independent review remain open. A positive C stage does not substitute for them.
