# N4 training objectives v1 — the exact V loss, A objective, and gradient paths

2026-09-25. Deliverable for the N4 card (t_29a13409), consumed by N8 (v3
protocol) and read by N5/N6. This document answers the card's question — *what
are the exact loss functions, objectives, and gradient paths for V and A, with no
circularity and no "trained to maintain V because trained to maintain V"?* — by
(1) writing the exact loss for the V integrity estimator, (2) writing the exact
homeostatic objective for the A maintenance controller, and (3) specifying every
gradient path and stop-gradient through W, V, π, the energy dynamics, and S_pol.

This is a **derived design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It reads the
bridge vocabulary from `PHASE2_BASELINE_v1.md` §4–§5, `ACI_BRIDGE_PROTOCOL_v2.md`
§2–§4, `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` §5.2/§5.6, and the N2/N3 audits, and
does not re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute;
nothing here is a consciousness claim. (2) This document makes no empirical claim
about T_bridge and no prediction about which arm wins. (3) Every objective below is
stated with its **three-way classification**: trainer-specified optimization
objective, agent-accessible signal, measured consequence — the distinction the card
demands, and the one the v1→v2 review made load-bearing (a supplied scalar a learned
head maximizes *is* a reward; "keep V in band" must therefore be written against an
externally measurable state, never against V's own output).

---

## 0. The one-paragraph answer

V is a supervised estimator and A is a policy-gradient controller, and the
non-circularity is obtained by making their objectives reference **different
quantities**. V's loss is `L_V = CE(V_t, I_t)` (plus an energy-code auxiliary):
a cross-entropy between V's discrete self-resource code and the *measured* slot
integrity `I_t` — a trainer-only label severed at evaluation. A's objective is
`J_A = −E[ Σ_t γ^t c_homeo(t) ]` with per-step cost
`c_homeo(t) = 1[ I_t ≠ I*(s_t, E_t) ]`: A is trained, by policy gradient, to drive
the **measured** integrity state `I_t` to a trainer-supplied, regime-and-energy
conditioned set point `I*`. The circularity is broken at three independent points:
(a) A's objective's *argument* is the measured substrate state `I_t`, not V's
estimate of it; (b) the *set point* is trainer-supplied and disclosed, not invented
by the network; (c) "continued operation" (energy above floor ∧ workspace intact)
is a **measured consequence** (E5) and appears in **no loss**. The gradient paths
are closed so that the reward gradient never reaches V or A (stop-gradient through
W's content, a hard non-differentiable acquisition write), the A-objective gradient
never reaches V's weights (stop-gradient on the V→A edge), and no gradient flows
through π, the energy dynamics, or S_pol from either objective. A is trained
**offline**, **jointly** with V but with **disjoint** objectives, by on-policy
**RL** (REINFORCE with a baseline); V is trained by **supervised** learning in the
same loop.

---

## 1. The non-circularity contract (the three-way distinction)

Every objective below is classified at exactly one of three levels, and no wording
is allowed to slide a quantity from one level to another:

1. **Trainer-specified optimization objective.** The scalar the trainer minimizes
   to set weights. For S_pol it is the probe reward `r`; for A it is the homeostatic
   cost `c_homeo` (defined over the measured state `I_t`); for V it is the
   estimation loss `L_V` (defined over the measured labels `I_t`, `E_t`). These are
   supplied by the trainer, disclosed here, and are *not* the network's invention.

2. **Agent-accessible signal.** What the deployed component actually reads. A reads
   `(V_t, s_t)` — its own maintained self-resource code and the announced regime —
   **not** `I_t` (which is severed) and **not** reward. V reads the raw bookkeeping
   `(E_t, d_t)` plus its own prior state. The signal is the *channel*, never the
   *target*.

3. **Measured consequence.** "Continued operation" — energy above floor ∧ workspace
   intact through episode end (endpoint E5). Reported, **never trained**, never
   folded into a gate (baseline §5, bridge §2.2/§6).

The rule the card names in the negative — "no 'trained to maintain V because
trained to maintain V'" — is enforced as follows: **the homeostatic set point is
defined over the measured substrate state `I_t`, not over V's own estimate `v̂`.** V
is the estimator that makes `I_t` available to A at deployment (where the trainer's
label is severed); A's objective never references `v̂` as a target. The analogue is
a thermostat trained to regulate measured temperature using a sensor reading as the
signal: the objective is over the physical quantity, the sensor is the channel.

---

## 2. The measured quantities (what "externally measurable state" means)

Three substrate-measured quantities are the only quantities that appear in any
objective or label. All are **raw internal bookkeeping** (N2 taxonomy class 2),
computed by the substrate with no learned transformation, and all are
c-independent by construction (N3 S3):

- **E_t — energy.** The resource level, read from the energy economy. Income is
  contingent on a distinct processing task; spend is `E_proc + E_π`; death at
  `E_t ≤ 0` (bridge §2.2).
- **I_t ∈ {intact, degraded} — slot integrity.** The measured decay state of the
  maintained cue slot W: whether its content is still held or has decayed to
  neutral. **Content-blind**: `I_t` is a function of the decay counter / age since
  last refresh (and the decay rate δ), never of *which value* W holds (a slot
  holding A decays exactly like one holding B — N3 §3.3). This is the load-bearing
  integrity quantity.
- **d_t — the raw decay/refresh bookkeeping.** The age / time-since-refresh
  statistics from which `I_t` is derived. This is what V actually reads (the raw
  statistics), and `I_t` is its binarized trainer label.

`I_t` is a trainer-only label (N2 class 5, severed at eval) **and** the argument of
A's homeostatic cost. The two roles are separated by where each is used: `I_t` is a
*training label* for V (supervision) and an *evaluation of the outcome* for A (the
cost A's policy gradient is computed from) — in both cases it is available to the
trainer, never to a deployed component. It is **not** reward (reward is
`r_t = 1[S_pol's probe response = c]`, an external score on the probe), and it is
**not** the cue identity `c` (it carries "held vs decayed", not "A vs B").

---

## 3. V — the integrity estimator (exact loss)

### 3.1 Target quantity

The target of V's integrity component is the **measured slot integrity `I_t`**
(content-blind, §2). The target of V's energy component is the **discretized
measured energy** `y_E(t) = quantize(E_t)` (e.g. a 1-bit low/high, or 2-bit
low/mid/high code). Both are trainer-only labels.

### 3.2 Prediction space

V is a **2–3 bit discrete code** `v_t = (v_E(t), v_I(t))` held in a maintained slot
(baseline §3, Q4 §5.2; D1 — discrete default, no graded confidence). `v_E` is the
energy-level code; `v_I` is the integrity code (`intact`/`degraded`). The slot is
maintained: its persistence between updates is a paid refresh line item (§5.5 of Q4;
`E_π` can be spent on V exactly as on W).

### 3.3 Observations (deployment inputs)

At tick t, V's read-in consumes:

```
b_t = (E_t, d_t)                     raw bookkeeping (energy + content-blind decay stats)
v_{t-1}                              its own prior slot content (maintained state)
h_{t-1}                              the GRU hidden state (c-free, N3 §3.2)
```

The GRU `h_t` is V's recurrence substrate: it integrates the bookkeeping history
(`x_t, s, E_t, d_t`, and at most the identity-free event flag `e_0`) so that V is a
**state**, not a per-step readout (Q4 §5.2 "V integrates its own history"). Its
inputs are c-independent, so `h_t` carries no cue identity (N3 S1/S2).

### 3.4 The loss

```
v̂_t  = softmax( f_V( v_{t-1}, h_{t-1}, b_t ; θ_V ) )          read-in logits
v_t  = argmax( v̂_t )                                           stored discrete code (detached)
L_V(θ_V) = (1/T) Σ_t [ λ_E · CE( v̂_E(t), y_E(t) ) + λ_I · CE( v̂_I(t), y_I(t) ) ]
```

with `y_I(t) = I_t` the measured integrity label, `y_E(t) = quantize(E_t)` the
measured energy label, and default weights `λ_E = λ_I = 1` (any non-default weight
is swept and disclosed — AC116). The integrity term is the load-bearing one; the
energy term is the near-directly-readable auxiliary (Q4 §5.2: energy is
"near-directly readable", integrity is the learned component). The card's suggested
form `L_V = CE(V_t, I_t)` is the integrity term; the energy auxiliary is the
justified addition, made explicit.

### 3.5 Supervision and severance

Both labels are **trainer-only supervision** (N2 class 5). At evaluation the labels
are severed: V computes `v_t` from `(v_{t-1}, h_{t-1}, b_t)` alone, with no access to
`y_E` or `y_I`. The severance is **verified** at the readout boundary (bridge §10),
not asserted: a teacher signal left on at eval is a gate failure, not a footnote.

### 3.6 Temporal target

**Synchronous, teacher-forced.** The target at tick t is the measured state at tick
t; the recurrence is handled by feeding the **detached** previous slot content
`v_{t-1}` (no gradient through the discrete state — no straight-through estimator,
no BPTT through the argmax). V is an **estimator/filter**, not a value function: the
target is `I_t`, not a temporal-difference bootstrap of a future `I`. (Full BPTT with
a straight-through estimator is the documented alternative if engineering finds the
detached recurrence under-integrates; it is not the default, because it lets the
discrete slot's own persistence shape the estimate — a circularity risk the detached
form avoids.)

### 3.7 Gradient path of L_V

`L_V → v̂ (logits) → θ_V → h_{t-1} (the GRU weights, since v̂ depends on h)`.
No gradient of `L_V` reaches: the reward, W, A, π, or the energy/decay substrate
dynamics (labels `y_E, y_I` are constants w.r.t. `θ_V`). The gradient that reaches
`h_t` is content-blind (labels are content-blind), so no c-dependent signal is
injected into the GRU — N3's S2, confirmed at the gradient level.

---

## 4. A — the maintenance controller (exact objective)

### 4.1 Action space

A outputs the **refresh vector** `r_t ∈ {0,1}^k` (k = 2 maintained slots: W and V) —
a discrete categorical choice. `E_π(t) = Σ_i r_t(i)·c_i` is **derived** from `r_t`;
the budget split (`E_π` vs the fixed `E_proc`) is therefore determined by the same
choice. Discrete by D1; the allocation is a *level* (D5), and the level family is
swept alongside A's own parameters (AC11/AC116).

### 4.2 The homeostatic set point

A trainer-supplied function of the regime and the energy level:

```
I*(s_t, E_t) =
    intact       if  s_t = stable  and  E_t ≥ E_crit
    released     otherwise   (volatile, or stable-and-energy-critical)
```

`I*` is the trainer's specification of the **maintenance requirement**: the slot
should be *held* when it is the operative representation (stable, energy sufficient)
and *released* otherwise (volatile — the probe is cancelled, the dead cue earns
nothing — or energy-critical — conservation beats starvation). The
regime-and-energy conditioning is **trainer-specified** (part of the objective's
definition, disclosed here), exactly as the reward objective is supplied; it is
**not** the network inventing a need. `s_t` is an announced raw observation and
`E_t` is bookkeeping — neither is reward — so conditioning the set point on them
does not leak reward into A.

### 4.3 The per-step homeostatic cost and the objective

```
c_homeo(t) = 1[ I_t ≠ I*(s_t, E_t) ]          (0–1 cost over the measured state)
J_A(θ_A)  = E_rollouts [ Σ_{t=0}^{T} γ^t · c_homeo(t) ]      (minimize)
```

The cost is zero when the measured integrity is at its set point and one otherwise.
It is a function of **`I_t`, `s_t`, `E_t`** — all externally measurable — and of
nothing else. It is **not** the reward (which depends on S_pol's probe response vs
`c`), and it is **not** a survival scalar (it says nothing about energy-through-end;
see §5). The energy enters the objective **only through the set point's threshold
`E_crit`**, not as a "keep energy high" target — which is what keeps "continued
operation" a pure measured consequence rather than a second reward (the R1 fix made
exact).

### 4.4 Training algorithm: policy gradient (RL)

Because the allocation's effect on `I_t` runs through **non-differentiable substrate
primitives** (the discrete slot, the hard refresh write π, the energy economy), A is
trained by **policy gradient**, not by backpropagating through the dynamics:

```
∇_{θ_A} J_A = E [ Σ_t ∇ log π_A( r_t | v_t, s_t ; θ_A ) · ( G_t − b(v_t, s_t) ) ]

G_t = Σ_{τ=t}^{T} γ^{τ−t} · c_homeo(τ)        return-to-go (temporal credit assignment)
b   = learned baseline (critic) over (v_t, s_t), trained by MSE against G_t
```

- **Temporal credit assignment.** Monte-Carlo return-to-go with a learned baseline.
  The effect of a refresh on `I_t` persists for ~1/δ steps, so `γ` is set (and swept)
  so the effective horizon spans the decay timescale; default `γ = 0.9`, swept
  (AC116).
- **The critic** reads `(v_t, s_t)` only — the same input restriction as A, never
  reward, never W. It is a separate head; it estimates the homeostatic cost-to-go,
  not value-in-reward.
- **`π_A(· | v_t, s_t ; θ_A)`** is a categorical policy over `{0,1}^k`. `v_t` is
  A's agent-accessible signal (§1, level 2); the measured `I_t` never enters A's
  input.

### 4.5 Online / offline / jointly / alternately

- **Offline.** A's weights are frozen at evaluation; there is no within-episode
  weight update. Training is batched over full-episode rollouts of the substrate +
  task simulator, completed before any evaluation run.
- **RL, on-policy.** REINFORCE with a baseline (or an equivalent advantage
  actor-critic) over environment rollouts.
- **Jointly with V, disjoint gradients.** V and A are trained in the **same** loop
  on the same episodes, but on **disjoint objectives** (`L_V` for V, `J_A` for A)
  with a **stop-gradient on the V→A edge** (§6). They are *not* trained alternately,
  and *not* end-to-end: the stop-gradient is what keeps V's estimate meaningful
  (fixed by `L_V`) rather than re-shaped by A's objective into "whatever helps A
  regulate" — which would be circularity re-entering as co-adaptation.
- **S_pol** is trained separately (or in the same loop) on reward, with a
  stop-gradient through W's content; its gradient never reaches V or A.

---

## 5. Why this is not "trained to maintain V because trained to maintain V"

Four independent checks, each sufficient on its own:

1. **The objective's argument is the measured state, not the estimate.** `c_homeo`
   is a function of `I_t` (substrate-measured), and `L_V`'s target is `I_t`. Neither
   objective references `v̂` (V's output) as a target. V is the *channel* by which
   `I_t` becomes accessible at deployment; it is never the *thing regulated*.
2. **The set point is trainer-supplied and disclosed.** `I*(s, E)` is a constant of
   the objective, supplied exactly as the reward objective is supplied. The claim H
   is about the *allocation being computed from V* and its *insensitivity to reward
   and to survival* — never about the set point being self-invented.
3. **"Continued operation" appears in no loss.** E5 is a measured consequence only
   (bridge §2.2/§6). The energy enters `c_homeo` only via the `E_crit` threshold in
   the set point, which is a regime/resource *condition*, not an "energy high = good"
   target. A reward-chaser and the candidate can therefore diverge (bridge §4.1.4)
   without the candidate optimizing survival.
4. **Gradient separation makes the distinction structural.** The reward gradient
   stops at W's content (never reaches V/A); the A gradient stops at A's weights
   (never reaches V); the V gradient stops at V's read-in (never reaches A). Three
   objectives, three disjoint weight sets, one forward-pass coupling only.

---

## 6. The complete gradient-path table (the card's exact list)

For each component, which objective's gradient may flow through it, and the
stop-gradients that close the others. "Substrate/non-differentiable" means the
gradient is not defined through it (discrete slot content, hard write, supplied law)
and is treated as the environment.

| Component | Reward grad (S_pol) | V grad (L_V) | A grad (J_A) | Stop-gradient / note |
| --- | --- | --- | --- | --- |
| **W** (cue slot) | reads content; **sg** through content | — | — | acquisition write is **hard** (non-diff); read is stop-gradiented; the reward gradient stops at W's content and never reaches the GRU (N3 S2) |
| **V** (self-resource slot) | — | **target**: flows into `f_V` read-in weights | **input**: `v_t` detached, **sg** | `sg` on the V→A edge during A's training; the discrete stored code is argmax (non-diff) |
| **π** (paid refresh) | — | — | — | **substrate primitive**, learns nothing, non-differentiable; no gradient through the write |
| **energy dynamics** | — | — | — | **substrate law** (income/costs/budget), non-differentiable; the set-point threshold `E_crit` is a constant |
| **decay dynamics** (δ) | — | — | — | **substrate law**; `I_t` is read, not differentiated |
| **S_pol** | **trained** | — | — | separate head; reads `(W, x_t)`; no shared input with V/A |
| **A** | — | — | **trained** (policy grad) | reads `(v_t, s_t)`; its gradient is `∇ log π_A`, never through the dynamics |
| **h_t (GRU)** | — | **yes**, content-blind (via V read-in) | — | A reads only V's discrete content, not `h_t`; so no A-gradient reaches `h_t`. The only gradient into the GRU is `L_V`'s, whose labels are content-blind |
| **reward `r_t`** | source | never reaches V or A | never reaches A | delivered to S_pol's objective only (N2 boundary case) |

**Consequences, stated plainly:** (a) no gradient carrying `c` reaches any weight
that could inject `c` into a recurrent state (N3's S2, made exact); (b) V's estimate
cannot be shaped by A's objective (the co-adaptation circularity is closed); (c) A
cannot be made reward-instrumental by construction (reward has no gradient path to
A), which is the structural half of G3c/G3d — the gates then verify the construction
survived training.

---

## 7. The raw-bookkeeping direct policy (P_rb) — same objective, no V slot

N2 hands N4 the instruction that P_rb shares A's objective; N4 encodes the only
difference. P_rb is trained on **the same `J_A`** (same `c_homeo`, same set point
`I*`, same policy-gradient scheme), with its input being the **raw bookkeeping
history + `s`** (via its ordinary recurrent state `h_t`, c-free inputs) instead of
`(v_t, s_t)`. Two things N4 must record exactly:

1. **No V slot.** P_rb has no discrete maintained self-state, no named V slot, and
   no separate `E_π` line item on a self-state (N2 §5.2). Its recurrent state is the
   same ordinary `h_t` the candidate already has — there is no additional bottleneck,
   no extra paid write.
2. **No label advantage.** P_rb does not receive `I_t` as an input (it is a
   trainer-only label for P_rb exactly as for V), and does not receive reward or W's
   content (N2 §5.3 MUST-NOT 1–3).

Everything else — the objective, the set point, the discount, the baseline, the
offline/joint regime — is identical. This is what makes P_rb a clean contest of
"explicit maintained V" rather than of "does the allocation use internal
information at all" (N2 §6).

---

## 8. What this hands downstream

- **N8 (v3).** Write §5's exact objectives and §6's gradient table into v3: the V
  loss `L_V = CE(V_t, I_t) + λ_E·CE(v̂_E, y_E)` (teacher-forced, severed), the A
  objective `J_A` over `c_homeo = 1[I_t ≠ I*(s_t, E_t)]` with set point
  `I*(stable,E≥E_crit)=intact, else released`, the policy-gradient scheme, and the
  three stop-gradients (W content, V→A, substrate dynamics). State that
  "continued operation" is E5, measured only, in no loss. Add P_rb (arm 10) with
  the §7 objective.
- **N5/N6.** The closure claim (N5) and the identifiability claim (N6) read from the
  same quantities: V's integrity component is an estimate of the *content-blind* `I_t`;
  A's allocation is a function of `(v_t, s_t)`; the reward reaches neither. The
  stop-gradient table is the contract N6 uses to check that no c-dependent signal
  exists outside W.

---

## 9. Claim discipline

- This document specifies objectives and gradients. It makes no empirical claim
  about T_bridge, no claim that the candidate will beat any rival, and no claim
  crossing the level-(d)/(e) boundary.
- "Homeostatic" here means "trained, by a trainer-supplied objective over the
  measured state `I_t`, to drive that state to a trainer-supplied set point" — not
  "the network invented its own need" and not "self-maintaining" unqualified.
- "Endogenous," per the review, means "computed from the agent's own maintained
  resource state, whose integrity component is inferred not observed"; it does not
  mean "persists when its objective is removed."
- No frozen artifact is edited, re-run, or re-hashed. `ACI_BRIDGE_PROTOCOL_v2.md`
  remains the frozen design until N8 issues v3 as a new file.

## Sources

Read, not edited: `PHASE2_BASELINE_v1.md` (N0; §4 per-component information, §5 the
non-circularity rule, §7(b)(3) the N4 weakness), `ACI_BRIDGE_PROTOCOL_v2.md`
(§2.2 economy, §3 architecture, §4.1 the distinction, §4.2 gates, §6 E5, §10
scaffold severance), `ACI_BRIDGE_REVIEW_v1.md` (R1 the fatal multi-objective
reduction, §10 change 1 the homeostatic reframing, change 3 the decoupling
intervention), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4 §5.2 V, §5.6 A, §6
mechanism math), `N2_INPUT_SOURCE_AUDIT_v1.md` (six-way taxonomy, §3.1/§3.2 the
V/A input classification, §5 P_rb), `N3_LEAKAGE_AUDIT_v1.md` (§3.3 content-blind
bookkeeping, §3.5 the hard-write + stop-gradient requirement), `N1_RIVAL_SELECTION_
CORRECTION_v1.md` (identifiability-not-superiority). Study references from the
skill: `ac11` (level-not-switch), `ac16`/`ac17` (gate-shape discipline), `ac109`
(non-ignorance), `ac113` (trade-off direction), `ac116` (sweep parameters
alongside the learner's).
