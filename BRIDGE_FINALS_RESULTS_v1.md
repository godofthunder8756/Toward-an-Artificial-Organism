# N11 — Final experiment results (δ-decay scaffold, frozen statistical plan)

2026-09-26. Deliverable of the N11 card (t_21622dd7): *what do the frozen final
runs show on the primary + secondary endpoints?*

This is a **results document**. It reads the frozen run's saved artifacts —
`bridge/finals_v1/pre_run_snapshot.json` (source + config hashes),
`bridge/finals_v1/rows.jsonl` (192 per-seed rows, 16 arms × 12 seeds), and
`bridge/finals_v1/results.json` (gates + controls + tradeoff) — and reports what
the untouched final experiment measured. No gate was moved after results began;
the gate constants were frozen in `bridge/run_finals.py` before the run.

**Scaffold STOP, restated once and binding.** The bridge's central question —
does a maintained, *inferred* integrity estimate do causal work — is
unidentifiable in this design (N6/N6b; v3/v4 STOP). The scaffold realizes the
δ-decay design, whose integrity `I_t = f(d_t)` is **observed** (a readable age
counter), not inferred. This document therefore evaluates N1 paid persistence,
N3a internal-state dependence, N3b nontrivial allocation, and N3c same-
information architectural contribution **in the observed-integrity world**, and
claims nothing about inferred integrity. Where the direct rival matches the
candidate, the conclusion is "explicit maintained V was unnecessary in this
task" — never a relabeling of the rival as part of the candidate.

---

## 0. Verdict (read this first)

**N1 paid persistence is confirmed at the test's resolution floor; the
allocation half of the claim is not.**

- **N1 (active paid persistence) — CONFIRMED, p = 2/2^12 = 0.00049 (floor).**
  The candidate holds the cue slot through the probe (stable slot survival
  0.978, probe accuracy 0.989) while no-maintenance and free-memory both lose it
  exactly (0.000). All 12/12 seeds positive; the effect is ceiling − chance, the
  one load-bearing claim the frozen plan grades as primary. The cue is
  recoverable only through the actively-maintained, costly W.
- **N3a (internal-state dependence) — present, but it is a re-encoding of the
  observable.** The candidate's allocator A does depend causally on V's discrete
  code (mean |ΔP(refresh)| = 0.19 on the integrity bit, 0.15 on the energy
  code). But V's integrity bit is a learned re-encoding of the readable age
  `d_t`, and the `(s,E,d)` state machine reproduces the same allocation from
  that same observable. Internal-state dependence exists; *inferred*-integrity
  dependence is not shown.
- **N3b (beats the state-blind family) — NOT strict dominance.** The candidate's
  operation score (0.895) beats every fixed level (all 0.5) in 10/12 seeds, but
  ties in 2/12 — two seeds (2000, 2004) collapsed to over-refresh (refresh rate
  0.65/0.82) and died. The allocation is regime-dependent beyond every
  state-blind schedule, but not robustly (bimodal, AC39/AC68).
- **N3c (same-information architectural contribution) — NOT DEMONSTRATED.**
  The strongest raw-bookkeeping direct policy (P_rb, arm 10) **matches** the
  candidate: mean op 0.823 vs 0.895, sign-flip p = 0.64 (5 positive / 7 negative
  seeds), no significant difference. And the sufficient-statistic state machine
  (arm 9 with the age read) attains the oracle (op 1.0), *above* the candidate.
  **The direct rival matches → explicit maintained V was unnecessary in this
  task.** This is the N6/N7 collapse, confirmed empirically rather than assumed.

**The one honest headline** is N1: the architecture realizes active paid
persistence — future-task information depends on a representation whose
retention is paid for, per tick, out of a limited budget. The "explicit
maintained V is causally load-bearing for the *allocation*" claim is not
supported: the same-information rival reaches the ceiling, the candidate does
not beat it, and V is a re-encoding of an observable.

---

## 1. What was run

The full 10-arm protocol set (v3 §4) plus the free-memory control, on the
12 final seeds 2000–2011 (N=12, disjoint from engineering 0–2 per AC39):

| # | Arm | Mechanism | Trained? |
| --- | --- | --- | --- |
| 1 | candidate | GRU → V → A homeostatic allocator | yes (frozen config) |
| 2 | no_maintenance | π cut, W decays | no |
| — | free_memory | W read-in disabled (GRU-only) | no |
| 3 | fixed family | state-blind duty cycle, periods {1,2,4,8,16,32,64} swept | no |
| 6 | oracle | threshold on (s, E, d) — EXTERNAL bound | no |
| 7 | reward-only | same capacity, probe-reward RL | yes |
| 8 | multi-objective | two-head (probe reward + survival) RL | yes |
| 9 | sufficient-statistic | (s,E) [arm9_nod] vs (s,E,d) [arm9_d = oracle] | no |
| 10 | P_rb | raw-bookkeeping direct policy, no V slot | yes |

Arms 7/8/10 are new rivals built on the frozen harness
(`bridge/final_arms.py`); arm 9's two forms and the mechanical arms reuse the
frozen action rules. The exact sign-flip test and exact binomial (Clopper–
Pearson) CI are in `bridge/exact_stats.py`.

Every trained arm was checkpointed (`bridge/finals_v1/checkpoints/`); a spot
re-check (reload seed-2000 candidate → re-eval) reproduced the saved rows
field-for-field.

---

## 2. G-N1 — active paid persistence (PRIMARY)

Endpoint: stable probe accuracy + slot survival (E1 read). Candidate vs
no_maintenance, plus the free-memory (W read-in disabled) free-permanence arm.

| Quantity | Value |
| --- | --- |
| candidate stable slot survival | 0.978 |
| no_maintenance stable slot survival | 0.000 |
| candidate stable probe accuracy | 0.989 |
| free_memory stable slot survival | 0.000 |
| fraction of seeds candidate > no_maintenance | 12/12 |
| exact sign-flip p (N_eff=12, 0 ties) | **0.000488 = 2/2^12 (floor)** |
| effect size (mean paired diff) | +0.978 |

Free-permanence: with paid W cut (no_maintenance) or W read-in disabled
(free_memory), the cue is unrecoverable at the probe in every seed — no
auxiliary recurrent state carries it. The causal read is the W-intervention
(§5): force-hold → probe accuracy 1.0, force-drop → ~0.5 (chance).

**Gate verdict: PASS at the floor.** This is the strongest wording the data
earns: "future-task information depends on actively-maintained, costly W."

---

## 3. G3b — candidate vs the swept state-blind family

Operation score (hold in stable, release in volatile) per seed.

| Quantity | Value |
| --- | --- |
| candidate op score (mean) | 0.895 |
| every fixed level (periods 1–64) op score | 0.500 |
| seeds candidate > best level | 10/12 |
| seeds candidate ties level (collapsed) | 2/12 (seeds 2000, 2004) |
| exact sign-flip vs best level (N_eff=10, 2 ties) | p = 0.00195 |

The two collapsed seeds are the AC39/AC68 lesson in the unfavorable direction:
the candidate's REINFORCE policy over-refreshed (stable refresh 0.65 and 0.82)
and died (survival ≈ 0.009, 0.000), landing its op score at the state-blind
baseline of 0.5. The mechanism is regime-dependent beyond every fixed level in
10/12 seeds; the "strictly better in every seed" dominance claim **fails**.
Reported as a bimodality-aware result: the optimum level of maintenance is
intermediate, and two final seeds overshot it into death.

---

## 4. `d_t`-read necessity (arm 9: without vs with the age read)

| Quantity | Value |
| --- | --- |
| arm9_d (s,E,d) op score | 1.000 |
| arm9_nod (s,E) op score | 1.000 (phase 0) |
| paired effect | 0.000 (12/12 ties) |

The frozen arm9_nod used a phase-0 fixed clock (`t % 16 == 0`), which coincides
with the deterministic countdown deadline (lifetime 16, probe at t=32), so it
holds the slot exactly as the oracle does. A disclosed post-hoc phase sweep
shows this is knife-edge: phases 1, 4, 8, 15 all collapse to op 0.5 (the slot
decays before the misaligned refresh). The honest reading: the age read's
necessity here is fragile — a phase-aligned fixed clock reproduces it, and any
misalignment fails — which is itself the N6 point that `d_t` is a readable
counter, not a latent. **No inference claim hangs on this contrast.**

---

## 5. N3c — same-information architectural contribution (candidate vs P_rb)

The CRITICAL contrast: does the candidate exceed the strongest raw-bookkeeping
direct policy, the recurrent no-V-slot rival trained on the same homeostatic
objective?

| Quantity | Value |
| --- | --- |
| candidate op score (mean) | 0.895 |
| P_rb op score (mean) | 0.823 |
| candidate stable slot survival | 0.978 |
| P_rb stable slot survival | 0.826 |
| fraction of seeds candidate > P_rb | 5/12 |
| exact sign-flip p (N_eff=12) | **0.64** |

The direct rival **matches** the candidate — no significant difference, and the
per-seed differences split both ways. The sufficient-statistic state machine
(arm 9, with the age read) attains the oracle (op 1.0), above both. Per the
card's own instruction, the conclusion is recorded as:

> **Explicit maintained V was unnecessary in this task.** The allocation is
> reproduced by a rival that reads the same raw bookkeeping `(E_t, d_t)` and
> regime through ordinary recurrence, with no discrete, paid-maintained
> self-state. V is a re-encoding of an observable, and its architectural
> contribution over the direct rival is not demonstrated.

This is the empirical confirmation of the N6/N7 identifiability collapse
(`ACI_BRIDGE_PROTOCOL_v3.md` §9.2, `TBRIDGE_IDENTIFIABILITY_v1.md` §7.2), not a
new finding.

---

## 6. Mechanistic controls (all pass)

| Control | Check | Result |
| --- | --- | --- |
| G3c reward-removal | reward/probe/L_V/critic losses add zero gradient to A's policy head | PASS (3/3 seeds, g_joint == g_alone) |
| G3d survival-decoupling | c_homeo invariant to the alive mask | PASS (3/3 seeds) |
| V-intervention (N3a) | A's P(refresh) depends on V's integrity code | mean \|ΔP\| = 0.19 (integrity), 0.15 (energy) |
| W-intervention | force-hold vs force-drop | hold → probe 1.0, slot 1.0; drop → probe ≈ 0.47–0.56, slot 0.0 |
| free-permanence | W read-in disabled → at chance | PASS (0.000 slot survival) |
| clock/generalization | announce ±8, delay 48, horizon 80 | stable slot survival 0.97–1.00 across all shifts |

The reward-removal and survival-decoupling controls verify the architecture was
realized as specified (A structurally cannot read reward; the homeostatic cost
is a function of (regime, E, age) only) — their passing is a prerequisite, not
evidence of endogeneity (N5 §2.2).

---

## 7. Utility / resource tradeoff (reported, not gated)

| Arm | stable probe | stable slot | stable refresh | stable survival | op score |
| --- | --- | --- | --- | --- | --- |
| candidate | 0.989 | 0.978 | 0.220 | 0.815 | 0.895 |
| no_maintenance | 0.000 | 0.000 | 0.000 | 1.000 | 0.500 |
| oracle | 1.000 | 1.000 | 0.062 | 1.000 | 1.000 |
| arm9_d (state machine) | 1.000 | 1.000 | 0.062 | 1.000 | 1.000 |
| arm10 P_rb | 0.519 | 0.826 | 0.245 | 0.833 | 0.823 |
| arm7 reward-only | 1.000 | 1.000 | 0.505 | 0.048 | 0.500 |
| arm8 multi-objective | 0.941 | 0.887 | 0.177 | 0.853 | 0.520 |

Reading: the candidate over-spends on maintenance relative to the oracle
(0.22 vs 0.062 refresh rate — ~3.5× — to hold the same cue), and its survival
is bimodal (0.815 mean, dragged down by the two collapsed seeds; the other ten
survive ≈ 0.96–1.0). The reward-only rival (arm 7) chases the probe reward to
the point of death (refresh 0.5, survival 0.05) — reward optimization is not
self-maintenance. The multi-objective rival (arm 8) survives but over-holds in
volatile (op 0.52). The oracle's conservation discipline — refresh at
0.062 in stable, 0.000 in volatile — is what the candidate and P_rb both
approximate but do not attain.

---

## 8. What this hands N12 (independent audit + adversarial reduction)

- Saved artifacts: `bridge/finals_v1/{pre_run_snapshot.json, rows.jsonl,
  results.json, checkpoints/}`. Source hashes of every frozen dependency plus
  the three new runner files are in the snapshot; the runner reproduces its own
  rows from the checkpoints.
- The one positive result to attack is **N1** (candidate 0.978 vs
  no-maintenance 0.000, p at floor). The reductions N12 should attempt:
  ordinary RL (arm 7 — dies, does NOT reproduce the candidate's conservation),
  supervised integrity prediction (V is re-encoding `d_t`; arm 9/10 reproduce
  it), the direct control policy (arm 9_d reaches the oracle, above the
  candidate), a sufficient statistic (arm 9_d = oracle), a fixed schedule (all
  levels 0.5, candidate 0.895), hidden recurrent memory (free-memory at chance),
  parameter-count advantage (arms 7/8/10 matched capacity), optimization
  advantage (same optimizer budget and objective family), reward shaping and
  task-clock exploitation (clock/generalization control).
- The N3c conclusion — "explicit maintained V was unnecessary" — is the
  documented result the audit should verify, not a claim to be defended.

---

## 9. Claim ceiling

- Confirmed: **active paid persistence (N1)** — future-task information depends
  on a representation whose retention is paid per tick from a limited budget;
  the allocation is regime-dependent beyond every state-blind schedule in the
  majority of seeds (10/12).
- Not confirmed: endogeneity from an *inferred* integrity state; any candidate
  advantage over the strongest same-information rival (P_rb matches, the state
  machine exceeds). No autopoiesis / subjectivity / consciousness claim is made
  or implied; this is a level-(b)/(c) representational result.
