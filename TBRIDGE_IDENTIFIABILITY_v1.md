# T_bridge identifiability v1 — the integrity state is observable, so there is no latent to infer and a compact sufficient statistic collapses the architecture

2026-09-25. Deliverable for the N6 card (t_bd5a5cb6), consumed by N7 (power/resolution
plan) and read by N8 (v3 protocol). This document answers the card's question — *is
T_bridge analytically identifiable: are there two histories with the same current
observable tuple but different optimal maintenance actions because of different latent
representation integrity?* — by writing T_bridge out as a decision problem (state,
observable, latent, sufficient statistic), deriving the optimal allocation and its oracle,
and testing whether the compact statistic (time-since-acquisition, time-since-refresh,
energy, regime, probe-distance) collapses the architecture.

This is a **derived analysis document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It reads the bridge vocabulary from
`PHASE2_BASELINE_v1.md` §3–§4, `ACI_BRIDGE_PROTOCOL_v2.md` §2–§4, and the N1–N5
corrections, and does not re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); nothing here is a consciousness claim. (2) This document
makes no empirical claim about T_bridge and no prediction about which arm wins.
(3) "Identifiable" carries N1 §3.3's meaning — *the permitted observation/history separates
the integrity states* — never "the candidate wins" and never "the mechanism is load-bearing."
(4) "Necessary" carries N2 §6's meaning — *the no-V rival provably fails to reproduce the
candidate* — and is never inferred from the weaker "internal information matters."

---

## 0. The one-paragraph answer

**No.** T_bridge, as specified, is **not** identifiable as a latent-integrity problem: there
are **no two histories with the same current observable tuple but different optimal
maintenance actions**, because the "latent" representation integrity `I_t` is a deterministic
function of an **observable** — the decay age `d_t` (time since the cue slot was last
refreshed), which the substrate hands every arm as raw content-blind maintenance bookkeeping
(N3 S3). The maintenance decision is therefore a **fully observed MDP** over the state
`(regime s_t, energy E_t, decay age d_t)`; its oracle is a threshold policy on `d_t` gated by
`s_t` and `E_t`, and its optimal action is a memoryless function of those three observables.
The consequences, all established below: (i) **explicit V is unnecessary for this task** — its
"inferred, not observed" integrity component (H clause (c)(i)) is, in T_bridge, *observed*
(via `d_t`), not inferred; (ii) a **compact sufficient statistic exists** and is even smaller
than the card's proposed tuple — `(s_t, E_t, d_t)`, with "time-since-acquisition" and
"probe-distance" both redundant — and it must be **included as the strongest rival** (a
memoryless state machine, the collapse of P_rb and the upgrade of arm 9); (iii) the reduction
to a simple state machine is **not hidden** — it is stated here as the bound a pass maximally
demonstrates. This is a *prerequisite* finding (N5 Tier 0), not evidence: it says the task's
integrity state is distinguishable from nothing, because it is already in the observation. If
the program wants to test *inferred* integrity, the integrity must be made genuinely latent
(a corruption stream whose flips the substrate does not reveal) — that is T7/T6 territory, a
different task (§8).

---

## 1. The question and what N6 owns

### 1.1 The exact question

N1 replaced the bridge's "genuinely beatable" engineering gate with an **identifiability
test**: construct matched situations — resource level matched, regime matched, reward matched,
clock/probe-distance matched — that differ only in the **actual integrity** of the maintained
cue slot, and ask whether the permitted observation/history distinguishes them (N1 §3.3).
N6's card is the *analytic* form of that test, specialized to T_bridge:

> Are there two histories with the same current observable tuple but different optimal
> maintenance actions, where the difference traces to different latent representation
> integrity?

The two "matched situations" of N1 §3.3 are exactly the "two histories" of this question. N6
answers it by construction from the frozen design, before any neural realization exists.

### 1.2 What N6 does and does not decide

- N6 decides **whether the integrity state is a latent that must be inferred** (in which case
  V's integrity estimate does real work, and the design proceeds with it load-bearing) or an
  **observable that is merely re-encoded** (in which case explicit V is unnecessary and the
  sufficient-statistic rival expresses the same allocation).
- N6 does **not** decide whether the candidate *wins* against any rival — that is N7/N8's
  final-run question, and N1 already ruled it out of engineering's remit. The rivals must
  remain capable of defeating H at finals regardless of this finding.
- N6's finding is a **Tier-0 prerequisite** (N5 §2.1): it determines whether the central
  contrast is *well-posed*, not whether it will pass. A "not identifiable" verdict is a
  pre-protocol stop or redesign signal (N1 §3.3, N5 §8.8), never a recorded falsification.

---

## 2. The decision problem, written out

The allocation decision under test is A's: at each tick t, choose the refresh vector
`r_t ∈ {0,1}^k` (k = 2 maintained slots, W and V in the bridge), with `E_π(t) = Σ r_t(i)·c_i`.
The load-bearing slot is W (the cue); V's own maintenance is a second-order detail that drops
out of the identifiability analysis (it is a re-encoding of the same observables, §5). The
decision problem is therefore: **refresh W or not, each tick.**

### 2.1 State variables (the true state the decision depends on)

| Variable | Meaning | Range | Where it lives |
| --- | --- | --- | --- |
| `c` | the latent cue | {A, B} | the environment; supplied to W only at t=0 |
| `s_t` | regime | {stable, volatile} | the environment; **announced** at t=m (observable) |
| `E_t` | energy level | 0…E_max | the energy economy (substrate bookkeeping, observable) |
| `W_t` | the cue slot's content | {A, B, neutral} | the maintained slot (the thing being maintained) |
| `I_t` | slot **integrity** (W held vs decayed) | {intact, degraded} | derived from W's decay state |
| `d_t` | decay **age** (time since W was last refreshed) | 0, 1, 2, … | the maintenance bookkeeping (substrate counter, observable) |
| `V_t` | self-resource state (energy code + integrity estimate) | 2–3 bits | the candidate's maintained slot (the contested component) |

### 2.2 Observable variables (the current observable tuple, common to every arm)

At tick t every arm — candidate and every rival — receives (N2 §5.3, N3 §2.2):

1. `x_t` — the distractor stream (i.i.d., independent of c; N3 §1.3);
2. `s_t` — the announced regime (raw environmental observation);
3. `E_t` — the energy reading (raw internal bookkeeping);
4. `d_t` — the decay age / time-since-refresh (raw maintenance bookkeeping, **content-blind**:
   a slot holding A decays at the same δ as one holding B — N3 S3);
5. its own action history — the refresh choices it made, which jointly determine `d_t` and
   `E_t` through the supplied substrate laws.

Item 4 is the load-bearing one. `d_t` is **not** the integrity estimate and **not** V's
output; it is the *raw* statistic the substrate maintains and hands over directly, from which
`I_t` is derived (`I_t` is `d_t`'s binarized trainer label — N4 §2). Every arm gets it,
including the sufficient-statistic rival (N2 §5.3 MUST-receive 1).

### 2.3 Latent variables (hypothesized to require inference)

Two quantities are, or could be, "latent" — not directly in the observable tuple:

- **The cue content `c` after t=0.** Genuinely latent (observable only at t=0; N3 S1 keeps it
  out of every recurrent state; W is its only carrier). But `c` is **irrelevant to the
  maintenance decision**: A's objective is content-blind (N3 S3, N4 §2), and the set point
  `I*` never references which value W holds, only whether it is held. `c` is latent but idle
  for A; it is S_pol's business, not A's.
- **The representation integrity `I_t`.** The quantity the card asks about. The claim under
  test (H clause (c)(i)) is that V infers `I_t` from bookkeeping — i.e., that `I_t` is
  **not observed**. The analysis of §3–§5 shows this is false: `I_t` is a deterministic
  function of the observable `d_t` (the age), so it is **observed**, not inferred. This is the
  whole finding.

---

## 3. The optimal action per relevant state (the oracle and DP)

The decision problem is an MDP, not a POMDP, because its state is fully observed. Write the
state as `q_t = (s_t, E_t, d_t)`.

### 3.1 The objective and the set point (N4 §4.2–4.3)

A minimizes the discounted homeostatic cost

```
J_A = E_rollouts [ Σ_{t=0}^{T} γ^t · c_homeo(t) ],   c_homeo(t) = 1[ I_t ≠ I*(s_t, E_t) ]
```

with the trainer-supplied set point

```
I*(s_t, E_t) = intact     if  s_t = stable  and  E_t ≥ E_crit
               released   otherwise   (volatile, or stable-and-energy-critical)
```

Two facts fix the policy's shape. First, the cost is **per-step and myopic**: it penalizes
`I_t ≠ I*` at *this* tick, and the only cross-tick coupling is through `E_t` — which is
already a state variable. There is no "hold until the probe" term; the probe reward reaches
S_pol, never A (N4 §6), so `probe-distance` cannot enter A's decision. Second, `I_t` is a
function of `d_t` alone (content-blind, uniform δ-decay), so "is W intact" is read off `d_t`.

### 3.2 The optimal policy (threshold on age, gated by regime and energy)

Under deterministic countdown decay (W flips to neutral after a lifetime `L = 1/δ` since the
last refresh):

```
r_W(t) = 1   iff   s_t = stable  and  E_t ≥ E_crit  and  d_t ≥ L − 1
r_W(t) = 0   otherwise
```

That is: refresh exactly when W would otherwise decay, and only when the regime makes the cue
worth holding and energy makes holding affordable; otherwise let it decay (the "released" set
point is already satisfied by a decayed slot). Under a geometric per-step hazard δ the shape
is the same up to a small dynamic program over `E_t` (balancing refresh spend against the
energy threshold `E_crit`) — still Markov in `(s_t, E_t, d_t)`, still a function of the same
three observables, still no latent.

### 3.3 The oracle

The oracle (arm 6) reads the ground-truth `(s_t, E_t, d_t)` and applies the threshold rule of
§3.2. It attains (near-)zero discounted homeostatic cost. The important structural point for
identifiability: **the oracle needs no privileged access to `I_t` beyond `d_t`**, because
`I_t = f(d_t)`. The oracle is not "reads the true integrity"; it is "reads the true age," and
the age is already in every arm's observation. This is the exact sense in which there is no
latent to infer: the privileged controller and the sufficient-statistic rival differ only in
*which function of the same observable* they apply, not in *which hidden state* they see.

---

## 4. Is memory actually required?

The bridge conflates two questions that must be kept apart, and they have opposite answers:

- **Memory for the *content* (T2 / N1): YES.** The cue is observable only at t=0 and absent
  through the delay; a memoryless readout of the current `x_t` is at chance at the probe *by
  construction* (bridge §2.3, T2 §3.2). W — the paid-maintained slot — is required to hold
  `c` across the delay. This is the "active paid persistence" half of the claim, and it is
  unaffected by this finding.

- **Memory for the *maintenance decision* (T4 / N3): NO.** The allocation is a function of
  `(s_t, E_t, d_t)`, all *current* observables. `d_t` is a substrate-maintained counter that
  summarizes the only relevant history (when W was last refreshed); no integration of
  history by the agent is needed. The decision is memoryless **in the agent's own recurrent
  state**: it does not require V, does not require the GRU to integrate anything, and does not
  require the agent to remember its own refresh history beyond reading the counter the
  substrate already maintains.

This is the AC109 lesson in its cleanest form: **storage is inert where the current
observation is decisive.** For the allocation, the current observation tuple `(s_t, E_t, d_t)`
is decisive, so the maintained self-state V is inert there — exactly as N2 §6's distinction
anticipates ("internal information matters" without "an explicit maintained self-state is
necessary").

---

## 5. Is integrity inference actually required? (the crux)

**No.** The chain, each link stated by the frozen design:

1. `I_t ∈ {intact, degraded}` is **content-blind**: it records whether W is held or has
   decayed to neutral, never which value it holds (N3 S3, N4 §2).
2. `I_t` is a **function of the decay counter** `d_t` (age since last refresh) and the decay
   rate δ — "a slot holding A decays at the same δ as one holding B" (N3 §3.3), and N4 §2
   states `I_t` is "a function of the decay counter / age since last refresh ... never of
   which value W holds."
3. `d_t` is **raw internal bookkeeping, directly readable** (N2 §3.1 class 2), handed to every
   arm including the sufficient-statistic rival (N2 §5.3 MUST-receive 1).

Therefore `I_t` is observable via `d_t`. V's "integrity estimate" — a learned transformation
of `d_t` (N2 §3.1, N4 §3) — **re-encodes an observable; it infers nothing hidden.** The
phrase in H clause (c)(i), "whose integrity component is inferred, not observed," does not
describe T_bridge as specified: the integrity is *observed* (as the age), and the only thing
V adds is a learned, discrete, paid-maintained re-encoding of that age.

Two framings give the same verdict, so the conclusion is robust to an implementation choice:

- **Substrate hands over `d_t`** (the specified reading): `I_t` is directly observable; no
  inference.
- **Substrate withholds `d_t`, agent tracks its own refresh history**: the age is still a
  deterministic function of the agent's own action history (refresh actions + the supplied
  decay law), so a policy reading its own history recovers `d_t`; still no latent, and even
  the "richer" recourse collapses to a counter — the AC77 fixed-point lesson (a life is one
  sample; the belief over a uniform-decay slot is a counter, not an integration).

In neither framing does the bridge require the agent to *estimate* integrity from indirect
evidence. What would require it is stated in §8.

---

## 6. The identifiability verdict (the two-histories question)

The matched-situations construction of N1 §3.3 asks: hold `(energy, regime, reward, clock,
probe-distance)` fixed, vary the actual integrity, and ask whether the observation separates
the states. Unpacked for T_bridge:

- If the "observable tuple" **includes** the decay bookkeeping `d_t` — which it does, per N2
  §5.3 and N3 §2.2 — then "same observable tuple" implies "same `d_t`," which implies "same
  `I_t`" (`I_t = f(d_t)`), which implies "same optimal action" (§3.2 is a function of `d_t`
  and nothing latent). **No two such histories exist.**
- If the matched-situations construction instead matches on `(energy, regime, reward, clock)`
  but *not* on `d_t`, then two histories can differ in integrity — but they differ in
  integrity **only through `d_t`**, which is itself observable. The observation distinguishes
  the integrity states **by reading the age**, not by inferring a hidden state. There is no
  residual latent; the "estimate" is a read.

Either way the answer is the same and is **negative**: there are **no two histories with the
same current observable tuple but different optimal maintenance actions due to different
latent integrity.** The optimal action is a deterministic function of the observable tuple;
the integrity is one of the observables. Consequently, per the card's own directive, **explicit
V is unnecessary for this task**, and the "inferred integrity" component of H clause (c)(i) is
not supported by T_bridge as specified — it must be either re-scoped (N8) or the task must be
changed to make integrity genuinely latent (§8).

The one-sided caveat, stated to avoid over-reach: the answer is about the **integrity** latent,
not the **regime** latent or the **cue-content** latent. The regime is announced (observable)
by design — regime *inference* is T1 and is deliberately not confounded here (bridge §2.1).
The cue content `c` is genuinely latent after t=0 but is idle for A (§2.3). Those two facts are
by construction and are not what this finding contests. What this finding contests is only the
claim that the *integrity* component of V is inferred rather than observed.

---

## 7. The sufficient-statistic test (does the architecture collapse?)

### 7.1 The proposed tuple, tested term by term

The card proposes `(time-since-acquisition, time-since-refresh, energy, regime,
probe-distance)` as a candidate sufficient statistic. Test each term against §3.2:

| Term | Needed for the optimal action? | Why |
| --- | --- | --- |
| **regime `s_t`** | **YES** | selects the set point `I*` (stable→hold, volatile→release) |
| **energy `E_t`** | **YES** | selects the set point (`E_t ≥ E_crit` gate) and the affordability of a refresh |
| **time-since-refresh `d_t`** | **YES** | determines `I_t = f(d_t)`, hence whether a refresh is needed *now* |
| time-since-acquisition `t` | **NO (redundant)** | its only roles — which regime, how long since the cue entered — are already carried by `s_t` (announced) and `d_t` (age); the set point is myopic |
| probe-distance `D − t` | **NO (redundant)** | A is reward-blind and the cost is per-step; the probe reward reaches S_pol only (N4 §6), so A's decision cannot depend on how far the probe is |

### 7.2 The compact sufficient statistic (the collapse, stated not hidden)

**`(s_t, E_t, d_t)` — regime, energy, decay age — is a sufficient statistic for the optimal
maintenance action.** It is:

- **Observable** (regime announced, energy bookkeeping, age bookkeeping — all raw, all
  c-independent);
- **Sufficient** (the oracle of §3.3 is a deterministic function of it; §3.2 is the threshold
  policy);
- **Compact** (a 1-bit regime, a small energy code, and an integer counter — no maintained
  state, no history integration, no learned estimate);
- **Memoryless** (it is the *current* tuple; the counter `d_t` already summarizes the only
  history that matters).

The corresponding rival is a **memoryless state machine**:

```
allocate( s, E, d ) =
    refresh W   if  s = stable  and  E ≥ E_crit  and  d ≥ L − 1
    release     otherwise
```

This is, in the arm taxonomy (N2 §5.4, N5 §3.2):

- the **collapse of P_rb (arm 10)** — P_rb's full recurrent history is unnecessary, because
  the raw bookkeeping's current value `d_t` already carries the information; and
- the **upgrade of the sufficient-statistic rival (arm 9)** — arm 9 conditions on
  `(energy, regime)` *only* and omits the bookkeeping read; adding the age `d_t` (the one raw
  maintenance statistic it lacks) makes it sufficient.

Per N2 §5.4 and N6's own instruction, this state machine is the **strongest** form of the
no-explicit-V rival and is **included**, never hidden. N8 should add it (or upgrade arm 9 to
read the age) so the final run's falsifying-rival set contains a rival that expresses the
optimal allocation by construction. Its presence is what makes any candidate advantage trace
to *something other than* "read the observable age" — and given §6, no such something exists
in T_bridge as specified.

### 7.3 What this does and does not say about arm 9 as written

Arm 9 as written ("duty cycle a function of the observable (energy, regime), no maintained
integrity estimate") is **not** sufficient: it misses `d_t`, so it cannot tell a fresh slot
from one about to decay and would be suboptimal in the stable regime. This is *not* evidence
that the integrity estimate does work — it is evidence that arm 9 was under-specified. The
honest reading is: arm 9, upgraded with the age read (which the card's own "raw maintenance
bookkeeping" already grants every arm), reaches the oracle. The candidate's V adds a
re-encoding of that same age; it does not add information.

---

## 8. Boundary conditions (when the answer flips to YES)

The "no" of §6 is a property of T_bridge *as specified*, and it flips under any one of three
modifications. These are named so N8 can decide whether to re-scope or re-design, and so the
"explicit V unnecessary" conclusion is not read as universal:

1. **Unobservable integrity decay.** If W's content is flipped by a **corruption/damage
   stream** (not the uniform, age-determined δ-decay) and the substrate does **not** reveal
   the flips — so the agent must infer "is W still correct" from downstream consequences
   (prediction error, agreement signals, maintenance-machinery bookkeeping) — then integrity
   becomes genuinely latent, and V's estimate would be an inference over an unobservable.
   This is **T7 (response to corruption)** / the AC67–AC71 damage line, a *different task*,
   not the bridge's memory decay.

2. **A non-myopic set point.** If A's objective were "hold W intact *until the probe*" with a
   terminal cost rather than a per-step `c_homeo`, then `probe-distance` would enter the
   optimal action and a forward-looking (partially latent, if the flip time is unknown) belief
   would be needed. N4's set point is explicitly myopic (`I*(s_t, E_t)` over the *current*
   regime and energy), so this does not obtain — but it is the single change that would make
   the card's "probe-distance" term non-redundant.

3. **Maintained self-state in the loop (N5-in-full).** If the integrity *bookkeeping itself*
   were a vulnerable, paid-maintained state that must be re-held (the maintainer's own state
   in the loop), then a maintained V would not be a gratuitous re-encoding — it would be the
   substrate of the closure. That is N5-in-full, explicitly deferred by the bridge (bridge §1,
   baseline §1), and is **not** what this finding is about. "Explicit V unnecessary" is scoped
   to the bridge's N3 claim; it says nothing about N5-in-full.

The constructive reading for N8: **either** re-scope H clause (c)(i) to what the task can
honestly support (the allocation is computed from the agent's own *observed* resource
state — energy and decay age — not from an inferred latent), **or** move the "inferred
integrity" claim to a task whose integrity is genuinely latent (T7/T6). Keeping the phrase
"inferred, not observed" over a δ-decay slot with a readable age counter is the exact
over-statement this card exists to catch.

---

## 9. What this hands downstream

- **N8 (v3 protocol).**
  1. Re-scope H clause (c)(i): in T_bridge the integrity is observed (the decay age `d_t`),
     not inferred; do not let the protocol claim "inferred, not observed" for a readable age
     counter, or state it as a re-design target (§8).
  2. Add the compact sufficient-statistic rival as the **strongest** no-explicit-V rival: the
     memoryless state machine `(s_t, E_t, d_t) → allocation` of §7.2. Carry it as the upgrade
     of arm 9 (add the age read) and the collapse of arm 10 (drop the history; `d_t` suffices).
     Do not require it to lose at engineering (N1 §3.2); it must remain capable of defeating H
     at finals (N1 §3.4).
  3. Record the identifiability outcome as a **Tier-0 prerequisite result** (N5 §2.1), not as
     evidence: the integrity state is separable from nothing because it is already observed.
  4. If the "inferred integrity" claim is retained, N8 must either modify the task (§8) or STOP
     (its own completion condition, N5 §8.8) — the central contrast as written cannot answer
     the question.
- **N7 (power/resolution plan).** The primary discriminating contrast is now the
  same-information contrast against the `(s, E, d)` state machine, not a test of integrity
  inference. N7's power analysis must grade the candidate against a rival that reaches the
  oracle by construction — which means, under N1/AC16/AC17, the graded quantity cannot be
  strict dominance or a mean margin over it (both were ruled out); the honest question N7
  faces is whether *any* candidate advantage survives, and on what residual it could rest.

---

## 10. Claim discipline

- This is a **level-(b)/(c) representational** analysis (N1 §3.3's "identifiable" is a property
  of the task + permitted information): it establishes that T_bridge's integrity state is
  *observed, not latent*, nothing more. It makes no level-(d) claim, no claim that the
  candidate will or will not beat any rival, and no claim crossing the level-(d)/(e) boundary.
- "Identifiable = NO" means "the permitted observation already contains the integrity state
  (as `d_t`), so no two matched histories differ in optimal action" — not "the candidate
  fails" and not "the mechanism is inert." The memory (W) required for the *content* is
  untouched; only the *allocation's* dependence on an *inferred* integrity is denied.
- "Explicit V is unnecessary for this task" is scoped to the bridge's N3 claim (§8.3) and is a
  statement about T_bridge's observables, not a claim that maintained self-states are
  unnecessary everywhere in the program.
- No frozen artifact is edited, re-run, or re-hashed. This is a design note consumed by
  N7/N8; `ACI_BRIDGE_PROTOCOL_v2.md` remains the frozen design until N8 issues v3 as a new
  file.

---

## Sources

Read, not edited: `PHASE2_BASELINE_v1.md` (N0; §3 architecture, §4 per-component information,
§5 objectives, §6 arms), `ACI_BRIDGE_PROTOCOL_v2.md` (§2.1 task, §2.2 economy, §3 architecture,
§4.2 gates, §5 arms, §6 endpoints, §7.2 failure table), `N1_RIVAL_SELECTION_CORRECTION_v1.md`
(§3.3 the identifiability test, §5 the hand-off to N6), `N2_INPUT_SOURCE_AUDIT_v1.md` (§3.1 V's
inputs, §5 the raw-bookkeeping direct policy P_rb, §6 the maintained-self-state-vs-internal-
information distinction), `N3_LEAKAGE_AUDIT_v1.md` (§3.3 content-blind bookkeeping, §1.3 the
task precondition N6 verifies), `N4_TRAINING_OBJECTIVES_v1.md` (§2 the measured quantities,
§4.2 the set point, §4.3 the homeostatic cost, §6 the gradient table), `N5_EVIDENCE_HIERARCHY_
v1.md` (§2 the three-tier hierarchy, §3.2 the rival classes), `ACI_MINIMAL_NEURAL_ARCHITECTURE_
v1.md` (Q4 §5.2 V, §5.5 π, §5.6 A — the full architecture the bridge narrows),
`ACI_PHASE2_BENCHMARKS_v1.md` (T2/T4/T5 — the tasks the bridge fuses), `TASK_IDENTIFIABILITY_
v1.md` (K4 — the analytic-identifiability form this card lifts to T_bridge),
`DEFINITIONS_CHARTER_v1.md` (§2 levels). Study references from the skill: `ac11`
(level-not-switch), `ac15` (asymmetric intervention), `ac16`/`ac17` (gate-shape discipline),
`ac77` (the fixed-point / counter collapse), `ac109` (storage inert where the current
observation is decisive; non-ignorant rivals), `ac113` (trade-off direction).
