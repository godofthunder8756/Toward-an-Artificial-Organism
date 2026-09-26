# ACI bridge review v1 — does the bridge protocol survive adversarial reduction?

2026-09-25. Deliverable for the Q9 card (t_8bfdd2a0): *does the bridge protocol
survive adversarial reduction?* Category E — **adversarial review of a design-only
artifact.** This document attacks `ACI_BRIDGE_PROTOCOL_v1.md` (the Q8 deliverable),
tries to reduce its candidate mechanism to each of the card's named categories,
states what survives and what does not, and — because one clause does not survive —
invokes the card's **single authorized redesign cycle** and delivers the revision as
`ACI_BRIDGE_PROTOCOL_v2.md`.

Nothing here runs, trains, freezes, or edits any frozen artifact. Reading
discipline of the program applies throughout: the level-(d)/(e) boundary is
absolute (`DEFINITIONS_CHARTER_v1.md` §2), seeds are the replication unit, and no
gate is moved after a result.

---

## 0. Verdict (read this first)

**The bridge survives as a test of N1 (active, paid persistence — no free
permanence) and of *self-computed-vs-exogenous* allocation (N3's clause (a)/(b)).**
Its arm set, its no-free-permanence gate, and its level-sweep gate are the right
shape and inherit the program's hardest-won lessons correctly (AC11, AC15, AC109,
AC113).

**The bridge does NOT survive its headline clause N3(c)** — "the allocation is not
reducible to learning an action that maximizes reward" — as written. The reason is
precise and is not a matter of degree:

> The protocol makes **"continued operation" a supplied scalar training
> objective** (§2.2 "This is what the allocation readout A is trained to maximize";
> §4.1 point 2 "trained against continued operation"). A supplied scalar that a
> learned head is trained to maximize **is a reward** by any definition the field
> uses. The candidate therefore optimizes **two** rewards (probe reward for S_pol,
> survival reward for A). "Two objectives, two consumers" (§4.1) is multi-objective
> RL — it is not a distinction between reward and non-reward.

This is the card's own redesign condition, listed twice by the protocol itself:
**F2** ("self-maintenance is reward optimization"), and **F7** ("reward and
continued operation cannot be decoupled → the distinction is not experimentally
identifiable"). Both fire. The fix is a *reframing*, not a new architecture: A is
re-trained from "maximize survival" to "regulate the agent's own resource state"
(homeostasis), survival becomes a *measured consequence* (reported, never trained),
and a decoupling causal intervention is added as the test the card demands. That
revision is §6 and the v2 protocol.

---

## 1. The attack surface

Per the card, I attempted to reduce the candidate mechanism to each of:

ordinary RL · reward shaping · a sufficient statistic · a trivial recurrent state ·
an externally encoded task clock · privileged observation access · larger parameter
count · extra compute · easier optimization · train/test leakage.

I then asked the card's second question — *is "self-maintenance" anything more than
optimizing expected reward?* — and required a meaningful causal intervention.

The protocol's own pre-emptions (§8) map each reduction to a defensive arm or gate.
I checked each mapping. One is load-bearing and fails; several others are
under-specified rather than wrong. Findings R1–R7 below; R1 is the fatal one.

---

## 2. R1 (fatal) — the candidate reduces to multi-objective RL

**The claim.** H clause (c): the allocation is "not reducible to learning an action
that maximizes reward."

**The reduction.** §2.2 defines two quantities: reward r_t (a score on the probe)
and "continued operation" (energy above floor ∧ workspace intact). §2.2 then states
A is "trained to maximize" continued operation; §4.1 point 2 states the two are
"distinct *by the objective they optimize*." But "distinct by the objective they
optimize" **is the reduction**. Two objectives, each a scalar supplied to the
trainer, each optimized by a learned head, is ordinary multi-objective RL. The
candidate is a two-head recurrent net trained on (probe reward, survival reward).
Nothing in the protocol makes "continued operation" anything other than a second,
sparser reward.

**Why G3c does not save it.** G3c ("reward-invariance") zeroes the *probe* reward
and predicts E_π is invariant. But it never zeroes — or even perturbs — the
*survival* reward. So the strongest thing G3c can show is "E_π is not driven by the
probe reward," which leaves the entire reduction intact: E_π is driven by the
survival reward. A reward-invariance gate that only removes one of the two rewards
does not test reward-invariance; it tests probe-reward-invariance. F2 fires.

**Why arm 7 does not save it.** Arm 7 is the single-reward null (trained on probe
reward only, no A/V/π). It falsifies "the architecture is needed to hold the cue."
It does **not** falsify "the allocation is reward optimization," because the
candidate's own allocation is driven by a *different* reward (survival) that arm 7
is not given. The correct multi-objective rival — a two-head net trained on (probe
reward, survival reward) — is **absent from the arm set**. That is the rival the
card's "critically distinguish" clause requires, and it is missing.

**Consequence.** As written, a pass of G3a/G3b/G3c would establish "the agent has a
state-dependent allocation that beats fixed schedules and is insensitive to the
probe reward" — a real and worth-reporting finding — but it would **not** establish
"the allocation is not reward optimization." The headline N3(c) is unidentifiable,
and the protocol's own §4.4 says that is the trigger for revision. It is triggered.

---

## 3. R2 — free permanence is under-specified (trivial recurrent state)

E1 and arm 2 test "no free permanence": cut π, the cue decays at rate δ, the probe
fails. But the protocol never constrains **δ against D against the GRU's own memory
capacity**. A GRU hidden state is itself a decaying-but-recurrent memory; if D is
short relative to the GRU's effective time constant, the cue survives in h_t with
**no paid write at all**, and arm 2 (cut π, but the GRU still runs) would pass the
probe — falsifying N1 by the protocol's own logic. Two related holes:

- Arm 2 cuts π but keeps the recurrent cell; the protocol does not say whether the
  cue can leak into h_t and be reconstructed at the probe. The "cut π" must be shown
  to actually remove the only channel carrying the cue, or arm 2 is not a clean cut.
- Arm 7 (a plain recurrent net with matching capacity) gets the *strongest* test of
  this: if it holds the cue for free, the entire "paid write is required" premise
  collapses. The protocol assumes the outcome instead of gating on it.

**Fix (in v2).** Add an explicit **free-permanence constraint**: δ and D are chosen
so that without the paid refresh the cue is unrecoverable at the probe *and* a
GRU-only control (arm 2 variant: recurrent cell present, π cut, W read-in disabled)
is at chance. This becomes an engineering gate (§9), not a hope.

---

## 4. R3 — missing sufficient-statistic rival

The "sufficient statistic" pre-emption maps to arm 5 (reactive reflex). Arm 5 is too
weak: it is a memoryless reflex with no maintained state. The genuine sufficient
statistic of this task is **(energy level, announced regime, time since
announcement)** — all of which are *observable*. The candidate's V is "energy
low/mid/high" (directly readable, §3) plus a learned integrity estimate. So the
candidate's conservation behavior at low energy may be nothing more than
"condition on the observable energy gauge," which **any** rival is allowed to do
(AC109: every arm sees the energy reading). The arm set has no rival that conditions
on (energy, regime) but lacks the learned integrity estimate. Without it, G3a can
pass trivially: E_π co-varies with V because V ≈ the observable energy gauge, and a
state-blind-but-energy-conditioned rival would do the same.

**Fix (in v2).** Add the **sufficient-statistic rival**: a reactive level whose duty
cycle is a function of the observable (energy, regime) but has no maintained
integrity estimate and no content attribution. The candidate must beat it, which is
only possible if V's *learned integrity* component — not the energy gauge — is doing
the work. This is what makes G3a a test of self-state rather than of observation.

---

## 5. R4 — "regime-tracking" (E4) is not discriminating, and the critical-economy
### is unspecified (F5/F6 risk)

Two separate problems, both about the economy.

**(a) E4 is vacuous as stated.** The regime s is *announced* (§2.1: "part of the
observation, not a hidden state to infer"). So "the split tracks the regime" (E4) is
achievable by reading an observation — every arm can do it. E4 is not a
discriminating endpoint and should not be gated; the discriminating N3 endpoint is
the **conservation divergence** (forgo the deferred reward to survive at low
energy), which the protocol correctly identifies in §2.2 but does not promote to a
gate.

**(b) The energy-critical state has no defined cause.** §2.2 asserts "when energy
is critically low, reward-seeking and continued-operation diverge," but the economy
has a *fixed drip* and no mechanism that makes energy fall. With a fixed drip and
fixed costs, energy is critical only if the agent overspends — and "continued
operation" is then trivially satisfiable by staying in budget, which is not a
divergence from reward-seeking at all. The protocol has left the load-bearing design
point of its own crux **unspecified**. This is exactly the vacuous-economy failure
the protocol itself names (F5: "no regime where maintenance is worth it") and the
trade-off-direction failure (F6/AC113): the economy check in §9 is told to find a
trade-off but is not told where one could come from.

**Fix (in v2).** Make energy income **contingent on a distinct processing task**
(the distractor stream is a continuous "metabolic" task that pays energy for correct
processing), while the probe reward remains a separate score on the deferred cue.
Then in the volatile regime the probe is cancelled, the dead cue earns nothing, and
every unit of E_π spent maintaining it is budget *not* spent on the processing that
earns energy — a reward-chaser that keeps maintaining the dead cue starves, a
conserver drops it and survives. The divergence is real and its direction is
measurable (AC113). Reward and energy are still distinct quantities (energy = a
resource paid by a different task than the reward's probe), so G3c stays clean.

---

## 6. R5 — "endogenous" partly collapses to reading an observation

The protocol's V is "read from the energy bookkeeping (directly readable)" (§3).
Energy is observable and is delivered to every arm (§5). So the "self-resource
state" the allocation is computed from is, in its energy component, an *observation*
— and the AC109 non-ignorance rule means every rival sees it. "Endogenous" then
cannot mean "computed from information the rival lacks." The only genuinely
endogenous content in V is the **learned integrity estimate** (the agent's estimate
of its own slot's decay state), which is *not* directly observable. The revision
must make the integrity estimate — not the energy gauge — the load-bearing component
of V, and state plainly that "endogenous" means "computed from the agent's own
maintained resource state, whose integrity component is inferred, not observed." R3's
sufficient-statistic rival is what forces this to be true.

---

## 7. R6 — the task-clock check is partial

§4.3's clock-invariance check shuffles the regime-announcement tick m and the
energy-dip tick, but holds the delay D (and the probe tick) fixed. A policy that
times its drop to "D − t" (time-to-probe) is a legitimate clock that the check does
not disturb. If the allocation is timed to the probe rather than to (V, s), G3a
would still pass (E_π co-varies with V only if V happens to track the clock). The
check should also sweep D itself (or randomize the probe tick within a band) so that
"time-to-probe" is decorrelated from the allocation. Minor, but the card names it
explicitly.

---

## 8. R7 — arm 7's capacity accounting must be declared, and the trainer scaffold is
### a leakage edge

- **Arm 7 gets the full recurrent capacity on one objective**, while the candidate
  must split its capacity across S_pol and A. That is the *right* direction (never
  handicap a rival), but §10 says only "matched in total recurrent capacity" without
  noting that this hands arm 7 *more per-task* capacity. Declare it, or a reader
  will misread a candidate win as an expressivity artifact.
- **Scaffold leakage.** §10 discloses W's belief labels and V's integrity labels to
  the trainer only, with "no ground truth at eval." This is the right statement, but
  it must be enforced at the *readout boundary*: if V's integrity labels (or W's
  content) reach the deployed readouts through a residual path (e.g., a teacher
  signal left on during eval), the candidate gains privileged information. The v2
  protocol makes the eval-time severance an explicit gate.

---

## 9. What survives (do not discard these)

The following parts of the protocol are correct and are carried unchanged into v2:

- **The task shape (T_bridge = T2+T4+T5).** Deferred once-presented cue, paid
  refresh, shared budget, conditional value. This is the right composition and the
  right size (D2: smallest content that makes a belief differ from a readout).
- **The arm taxonomy and the AC11/AC15 discipline.** Level family *and* learner
  parameters both swept (G3b); asymmetric intervention so the two state-blind
  extremes are wrong in opposite directions; per-slot scoring; the fixed schedule
  named as the honest simplest-sufficient policy of T2.
- **The falsification table F1–F7**, including the pre-protocol economy check (F5)
  and trade-off-direction check (F6), and the recorded-not-moved rule (AC16).
- **The non-ignorance rule (AC109)** applied to every arm, and the byte-identity
  reproduction control (AC83/P7) before attributing anything to an intervention.
- **The seed discipline** (engineering vs final, disjoint families, N seeds × 2
  histories = N units, survival as a bimodality-aware lower bound — AC39/AC68).
- **The claim ceiling** (§11): "meets N1 and N3 at the stated degree," nothing
  stronger, no consciousness/self-maintenance-unqualified claim. This is correct and
  is *strengthened*, not relaxed, by the revision.

---

## 10. The one authorized revision

The card authorizes exactly one major redesign cycle. It is triggered (F2/F7), and
it is issued once, now, as `ACI_BRIDGE_PROTOCOL_v2.md`. The revision is a
**reframing plus specification**, not a new architecture — the GRU + W + V + π +
S_pol + A + budget skeleton is unchanged. Five changes:

1. **A's objective becomes homeostatic regulation of V, not survival maximization.**
   A is trained to keep the agent's own resource state V within a viable band
   (reduce the rate of integrity degradation / keep V at a set point), using only
   internal signals. "Continued operation" (energy above floor ∧ workspace intact)
   is demoted to a **measured consequence**, reported as E5, **never a training
   signal**. This removes the second external reward and makes the two consumers
   genuinely different in kind: S_pol optimizes an *external score* (reward); A
   regulates an *internal state* (homeostasis).

2. **The claim is reframed to what is actually identifiable.** H clause (c) is
   replaced by the strongest honest formulation: the allocation is (i) insensitive
   to the task reward (G3c, plus a structural guarantee that A's inputs are
   restricted to (V, s) so it cannot read reward-relevant content W), and (ii) not
   instrumental to survival (the new decoupling intervention, below). The residual
   philosophical point — a trained policy always optimizes some objective — is
   conceded in the protocol, not hidden.

3. **A decoupling causal intervention is added (the "meaningful causal intervention"
   the card demands).** A condition in which survival is made irrelevant (energy
   cannot deplete) *and* the probe reward is zeroed. Prediction: the candidate's A
   keeps regulating V (homeostasis is not instrumental to either reward); arm 7's
   "maintenance" collapses to zero (it was instrumental to reward/survival). This is
   the causal signature of "regulating one's own state" vs "optimizing an external
   score," and it is the only test that separates them.

4. **The economy is specified** so the divergence is real: energy income is
   contingent on a distinct processing task (R4b), reward and energy remain distinct
   quantities (R4b), and the free-permanence constraint (δ vs D vs GRU capacity) is
   declared (R2).

5. **Two rivals and one gate are added**: the multi-objective RL rival (the
   two-head (probe, survival) net — the correct form of R1), and the
   sufficient-statistic rival (energy/regime-conditioned reactive level, R3); plus
   the eval-time scaffold-severance gate (R7) and the D-swept clock check (R6).

The v2 protocol carries the full revised arm set, gate set, falsification table,
economy, and claim ceiling. The review's finding is that **this** version survives
the reduction attempt: every named reduction now has a rival or gate that would
expose it, and the headline claim is one the experiment can actually falsify.

---

## 11. Attribution and claim discipline (what this review does not say)

- The v1 protocol is a competent, well-disciplined design; its failure is the same
  one the program's own Q4 §5.3 made (S_reg "trained to maximize continued
  operation"), inherited faithfully and foregrounded. This review attributes the
  flaw to the *inherited specification*, not to carelessness on Q8's part.
- No claim here is made that the revised experiment will pass. It is a *design that
  can now be falsified cleanly*, which is what the bridge is for.
- The revision does not touch, re-hash, or re-run any frozen organism artifact.
- "Endogenous," in the revised claim, means "computed from the agent's own
  maintained resource state, whose integrity component is inferred not observed" —
  it does not mean "persists when its objective is removed" (no trained policy does),
  and it does not mean "conscious" or "self-maintaining" unqualified.

---

## Sources

Read, not edited or re-hashed: `ACI_BRIDGE_PROTOCOL_v1.md` (Q8, the attack target),
`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4 §5.2 V, §5.3 S_reg "trained to maximize
continued operation," §2 the reward/energy distinction),
`ACI_PHASE2_BENCHMARKS_v1.md` (Q6 T2 §3.2, T4 §3.4, T5 §3.5, joint-demand §7),
`DEFINITIONS_CHARTER_v1.md` (§2 levels, §4 scaffolding, §5 supplied substrate).
Study references read from the skill: `ac11` (level-not-switch), `ac15` (asymmetric
intervention, per-slot scoring, vacuous pass), `ac109` (non-ignorance),
`ac113` (trade-off direction), `ac116` (economically invisible), `ac95-d4`
(observer-discard equivalence).
