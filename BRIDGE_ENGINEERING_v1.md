# Bridge engineering validation v1 — N10

2026-09-26. Deliverable of the N10 card (t_17e7175e): *does the implementation
pass engineering validation, and is it frozen?*

This is a **results / engineering document**. It is not hashed into the study's
`pre_run_snapshot.json` (only the frozen sources are), and it may be edited. The
frozen artifacts are `bridge/engineering_v1/pre_run_snapshot.json` and
`bridge/engineering_v1/results.json`.

---

## 0. Verdict

**Engineering validation PASSED, with one vacuous-economics fix and one training
tune — and the scaffold is frozen with an explicit STOP on the bridge's central
claim.**

The scaffold (N9's six neural modules + substrate + trainer) is mechanically
sound **after** two changes, both made under the N10 card's permitted "vacuous
economics" and "tune training hyperparameters" clauses:

1. **Decay-law fix.** The substrate's decay was a *stochastic, irreversible
   erase* (slot zeroed with probability δ per unrefreshed tick, refresh unable to
   restore it). This made the economy **vacuous** — measured: the oracle held the
   cue at the probe only 3.8% of the time vs 3.1% for no-maintenance, a 0.7-point
   margin (maintenance bought nothing), because preserving the cue required
   refreshing nearly every tick and that was unaffordable (refresh-every-tick
   died 8/8). Fixed to the **deterministic countdown** the protocol actually
   specifies (N6 §3.2: "W flips to neutral after a lifetime L since the last
   refresh; refresh re-energizes"). After the fix: oracle 1.000 vs no-maintenance
   0.000 slot survival — maintenance genuinely pays.
2. **Training tune.** REINFORCE collapsed to a "never refresh" local optimum
   (the Bernoulli policy stopped sampling the high-cost-avoiding action). Fixed
   with a Bernoulli entropy bonus (`a_entropy_weight=0.1`) and a higher A-policy
   learning rate (`lr_a_policy=1e-2`), under the declared finite search budget
   (§4). After the tune the candidate learns locally-rational maintenance
   (holds in stable, drops in volatile).

**STOP, stated once and carried verbatim into the freeze.** The bridge's central
question — does a maintained, *inferred* integrity estimate do causal work — is
**unidentifiable** in this design (N6, N6b; `ACI_BRIDGE_PROTOCOL_v3.md` §10,
`v4.md` §11). The scaffold realizes the **δ-decay** design, whose integrity
`I_t = f(d_t)` is **observed** (a readable age counter), not inferred. This
validation verifies the scaffold's *mechanics* — economy, arms, controls,
information paths — and freezes them for N11. It does **not** freeze or present
an inferred-integrity claim; none is made.

---

## 1. What N10 verified (the six items)

All six measured on **engineering seeds only** (0, 1, 2), disjoint from N11's
final sample (2000–2011, N=12).

| # | Item | Result |
| --- | --- | --- |
| 1 | learning converges | PASS — L_V, J_A_critic, probe all decrease; V's integrity code reaches ~0.95 accuracy |
| 2 | economy non-vacuous | PASS — oracle slot survival 1.000 vs no-maintenance 0.000 at the probe |
| 3 | maintenance/dropping locally rational | PASS — oracle refreshes in stable (0.062/tick) and never in volatile; the candidate learns the same (stable 0.12 vs volatile ~0.002) |
| 4 | candidate/rivals/interventions function | PASS — five arms + free-memory run and produce distinct, correct endpoints; forced refresh/hold is causal (unit test) |
| 5 | free-memory removes cue persistence | PASS — W read-in disabled → readout neutral (slot survival 0.000); the cue has no path to the probe except W |
| 6 | information paths match protocol | PASS — gradient paths (L_V→{f_V,GRU}, J_A_policy→{A_policy}, J_A_critic→{A_critic}, probe→{S_pol}) and cue leakage (cue only in slot + probe) verified |

---

## 2. The decay-law fix (vacuous economics)

Measured **before** the fix (fixed policies, engineering seed 0):

| policy | slot survival at probe | survival |
| --- | --- | --- |
| never refresh | 0.031 | 1.0 |
| oracle (threshold) | 0.038 | 1.0 |
| refresh every tick | 1.000 | 0.0 (dies) |

The oracle — the N6 §3.2 threshold rule that should hold the cue — held it only
3.8% of the time. Cause: the substrate's `decay_slot` zeroed the slot with
probability δ=0.1 per unrefreshed tick, **irreversibly** (refresh resets the age
counter but cannot restore a zeroed slot). Preserving the cue therefore required
refreshing nearly every tick, which the economy cannot fund (income 0.18/tick vs
refresh cost 1.0/tick). Maintenance bought ~0.7 points. That is the AC11/AC15
"no trade-off exists" failure in the strongest form.

The protocol's model is the **deterministic countdown** (N6 §3.2): the slot's
readout flips to neutral once the age reaches `lifetime` since the last refresh,
and a paid refresh (age reset) restores the readout. The stored value is a
register that persists; only the readout gates. This makes `I_t = 1[age <
lifetime]` the literal, observed integrity, and refresh genuinely causal.

Changes: `substrate.py` `decay_slot` (stochastic erase → age-gated readout),
`agent.py` forward (slot value preserved; per-tick readout recorded),
`config.py` `DecayConfig` (`delta` removed; `lifetime` is the deadline), plus the
affected docstrings/tests. `bridge/tests` (41 tests) green before and after.

---

## 3. The training tune (REINFORCE collapse)

With the default hyperparameters the candidate's policy collapsed toward "never
refresh": both stable and volatile refresh rates fell together, and the policy
never separated the regimes (a classic REINFORCE premature-convergence trap —
once the policy is near-deterministic it stops sampling the action that would
reveal the cost saving).

Fix: a Bernoulli entropy bonus on `J_A` (`-w·H`, so minimizing the total
maximizes action entropy) plus a higher A-policy learning rate. The bonus keeps
the policy exploring long enough to discover that refreshing *in stable* avoids
cost while refreshing *in volatile* incurs it.

**Declared finite search budget** (engineering seed 0, recorded here because the
card requires it): entropy weight ∈ {0.0, 0.05, 0.1}, A-policy LR ∈ {1e-3, 5e-3,
1e-2}, steps ∈ {1000, 2000}, then the chosen config re-checked on seeds 1, 2.
No task parameter (architecture, economy, decay, arm set, seeds) was selected by
this sweep.

Chosen: `a_entropy_weight=0.1`, `lr_a_policy=1e-2`, 1000 steps × 64. Candidate
behavior on engineering seeds 0/1/2: stable slot survival 0.98/0.97/0.98,
volatile slot survival 0.01/0.03/0.03, stable refresh 0.120/0.114/0.115,
volatile refresh 0.002/0.004/0.004, stable survival 0.95/0.98/1.00. (lr=5e-3 was
rejected: it collapsed on seed 2 — refresh 0.675/0.649 and 0/1 survival. steps=
2000 was also viable but offered no material gain over 1000.)

---

## 4. Arm endpoints (frozen in `results.json`)

Fixed-policy arms are deterministic under the seeded substrate; the candidate is
the trained learned allocator. `stable_slot_surv` / `volatile_slot_surv` are the
probability the cue slot's readout is intact at the probe in each regime.

| arm | stable slot | volatile slot | stable refresh | volatile refresh | stable survival |
| --- | --- | --- | --- | --- | --- |
| candidate | 0.977 | 0.025 | 0.116 | 0.003 | 0.977 |
| no_maintenance | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| oracle | 1.000 | 0.000 | 0.062 | 0.000 | 1.000 |
| always | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| fixed_p16 | 1.000 | 1.000 | 0.062 | 0.062 | 1.000 |
| fixed_p4 | 1.000 | 1.000 | 0.250 | 0.250 | 0.752 |
| free_memory | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |

Reading: the oracle is locally rational (holds stable, drops volatile, survives);
`always` and `fixed_p4` over-spend and die; `fixed_p16` holds both regimes but
wastes energy refreshing in volatile; the candidate converges onto the oracle's
shape. The two state-blind extremes are wrong in opposite directions (AC15 rule
1): `always`/`fixed_p4` die by over-maintenance, `no_maintenance` loses the cue.

---

## 5. What this hands N11

- The frozen scaffold + arm harness (`bridge/arms.py`) + validation driver
  (`bridge/validate_engineering.py`) + config, with the freeze in
  `bridge/engineering_v1/pre_run_snapshot.json`.
- N11 (run the untouched final experiment) builds the **full rival set** (arms
  7 reward-only, 8 multi-objective RL, 9 sufficient-statistic, 10 raw-bookkeeping
  direct policy P_rb) on top of this harness. The mechanical arms here
  (no-maintenance, fixed family, oracle, free-memory) are the engineering screen;
  the falsifying-rival arms are N11's extension.
- **What N11 must not claim:** any inferred-integrity result. The δ-decay
  scaffold's integrity is observed (`I_t = f(d_t)`); the strongest same-information
  rival (the `(s,E,d)` memoryless state machine) *is* the oracle by construction
  (N6 §7.2), so the candidate is bounded above by it on every seed — the
  "explicit maintained V is necessary" claim is unsupported here (N2 §6). N11
  evaluates N1 paid persistence, N3a-c, and the controls *in the observed-integrity
  δ-decay world*, not an inferred-integrity world.

---

## 6. Provenance

Read, not edited: `ACI_BRIDGE_PROTOCOL_v3.md` (δ-decay STOP; §4 arms, §5
engineering gates, §6 architecture, §7 objectives), `ACI_BRIDGE_PROTOCOL_v4.md`
(Path B STOP), `TBRIDGE_IDENTIFIABILITY_v1.md` (N6; §3.2 deterministic countdown,
§7.2 the sufficient statistic), `TBRIDGE_IDENTIFIABILITY_v2.md` (N6b),
`TBRIDGE_STATISTICAL_PLAN_v1.md` (N7, the δ-decay N=12 sign-flip plan),
`TBRIDGE_STATISTICAL_PLAN_v2.md` (N7b, no plan for Path B), `N4_TRAINING_OBJECTIVES_v1.md`,
`N3_LEAKAGE_AUDIT_v1.md`.

Study references from the skill: `ac11`/`ac15` (no-trade-off / asymmetric
intervention), `ac16`/`ac17` (gate-shape discipline), `ac39` (disjoint seed
families), `ac109` (storage inert where the current observation is decisive),
`ac113` (trade-off direction), `ac67`/`ac71` (sticky damage; read/repair threshold).
