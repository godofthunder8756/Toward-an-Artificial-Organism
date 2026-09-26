# N3 leakage audit v1 — closing the free recurrent-memory channel

2026-09-25. Deliverable for the N3 card (t_80ce37f4), consumed by N8 (v3 protocol)
and read by N6 (analytic identifiability). This document answers the card's two
questions — *can cue identity survive through an unpriced recurrent pathway, and how
is that channel closed structurally?* — by (1) enumerating every pathway through
which cue identity could reach the probe without passing through the paid maintained
slot W, (2) specifying the structural closure that makes those pathways carry no cue
by construction, and (3) defining the six leakage tests that verify the closure.

This is a **derived design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It reads the
bridge vocabulary from `PHASE2_BASELINE_v1.md` §3–§5 and `ACI_BRIDGE_PROTOCOL_v2.md`
§2–§4 and does not re-derive them. Its six tests are **specified**, not executed:
there is no bridge realization yet, and the tests become executable only when N8
issues v3 and the realization runs.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); nothing here is a consciousness claim. (2) Seeds
are the replication unit; probe/leakage measurements use disjoint train/test seed
families and are never read off a single seed (AC39). (3) This document makes no
empirical claim about T_bridge and no prediction about which arm wins — it specifies
*what must be true* of the architecture and *how to verify it*.

---

## 0. The one-paragraph answer

Cue identity must not — and in T_bridge need not — survive through an unpriced
recurrent pathway, and the channel is closed **structurally**, not by choosing D long
enough that the GRU forgets. The cue's only consumer is S_pol, and it reads W; no
recurrent state (the GRU hidden state h_t, the self-resource state V, or the
homeostatic readout A) needs c, and each is fed only c-independent inputs by
construction. The closure has three structural parts: (1) **W is non-recurrent** — a
discrete 1-bit maintained slot written once by a *supplied, hard* acquisition write,
so its content is reachable only by S_pol and its persistence is the paid refresh's
job (P1); (2) **forward-pass isolation** — h_t, V, and A receive only c-independent
inputs (distractor x_t, regime s, energy E_t, *content-blind* decay bookkeeping, and
at most an identity-free acquisition-event flag); (3) **gradient isolation** — W's
write and read are non-differentiable with respect to h_t, so no reward gradient
carrying c can reach the GRU weights. The six tests verify the closure: disable W's
content, sever W's readout, cut π, and probe h_t / V / A / auxiliary activations for
decodable cue identity at multiple delay ticks. The bar is chance-level decodability
at **every** probed tick: a probe that decodes c at t=1 but not at t=D reveals
*forgetting*, not structural prevention, and is rejected in favour of the structural
fix. If any state genuinely must carry c for optimization, it becomes a second
priced-and-decayed maintained slot — never a free channel.

---

## 1. The question and what N3 owns

### 1.1 The question

The baseline (N0 §7(b)(2)) records the open weakness: "whether cue identity can
survive through an unpriced recurrent pathway (the GRU's h_t, or an auxiliary
activation acting as a pristine copy) is not yet structurally closed." The bridge
protocol already gestures at it — §2.3's "free-permanence constraint" and §9.3's
free-permanence engineering gate, plus arm 2's "GRU-only variant" and F3 ("the cue
survives arm 2's cut, or the GRU-only variant passes") — but none of them specifies
*which* recurrent states are candidate carriers, *which* isolation guarantees close
them, or *how many* tests must pass before the channel is declared closed. N3 owns
that specification.

The question has an exact form: **is there any pathway by which the cue identity c
reaches S_pol's probe response (or is otherwise recoverable to solve the probe)
without passing through the paid maintained slot W?** If yes, N1 (active paid
persistence) is not identified, because the representation's persistence was free —
the F3 "free permanence" failure. Closing the channel is therefore a precondition of
E1's and G3c/G3d's clean interpretation, not a side concern.

### 1.2 Scope: the candidate, not the rivals

The audit is about **the candidate's** architecture (arm 1). The rivals are the
contrast, not the subject: arm 7 (reward-only) is *expected* to hold the cue in its
recurrent state — that is its mechanism, and it is exactly why arm 7 must collapse
under G3c/G3d. The leakage tests below are run on the candidate (and on any rival
that shares its structure where the test is meaningful, e.g. arm 2's GRU-only
variant as the control for test 3). What the audit forbids is the candidate having a
free cue-carrier *in addition to* the priced W.

### 1.3 One task-construction precondition the audit assumes, not establishes

The distractor stream x_t is declared i.i.d. and independent of c (bridge §2.3: "the
information genuinely is not there"). If that independence fails, the GRU could
recover c from x_t — a *task* leak, not an *architectural* leak, and outside this
card. N3 assumes it as the precondition the whole audit rests on and flags it to N6
(whose identifiability analysis must confirm it). This document audits only the
architectural channels: the states and activations *inside* the agent that could
carry c for free.

---

## 2. The leakage audit: every unpriced pathway, enumerated and classified

### 2.1 The preferred topology (the target the audit protects)

```
  cue c (env, one-shot, t=0)
        │  acquisition write (SUPPLIED, hard)
        ▼
   ┌─────────┐   refresh π (paid)      ┌──────────┐
   │   W     │◀────────────────────────│    π     │
   │ (1-bit, │                         │ (substrate│
   │  non-   │                         │  write)  │
   │recurrent)│                        └────▲─────┘
   └────┬────┘                              │ allocation (E_π, r_t)
        │ W                                 │
        ▼                                  │
   ┌─────────┐                        ┌────┴─────┐
   │  S_pol  │── probe response       │    A     │◀── (V, s)
   └─────────┘                        └────▲─────┘
      ▲                                    │ V
      │ x_t (distractor)             ┌─────┴──────┐
      │                              │     V      │◀── energy E_t (c-free)
      │                              │ (2–3 bits) │◀── decay bookkeeping (c-free)
      │                              └────────────┘
      └──────────── GRU h_t (recurrence) ◀── x_t, s, E_t, decay bk, [event flag e_0]
                     — NO c enters h_t
```

The topology asserts three facts the audit then verifies: (a) c reaches exactly one
state, W, through one supplied write; (b) W's only consumer is S_pol; (c) every
other state's inputs are functions of c-independent quantities only.

### 2.2 The channel inventory

Every stateful or persistent quantity in the candidate is one potential free
carrier. The inventory lists each, its declared inputs, whether c can enter it in
the forward pass, whether a gradient can inject c, and which test closes it.

| # | Carrier | Declared inputs | Forward-pass c-entry? | Gradient c-entry? | Closed by | Test |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | GRU hidden state h_t | x_t, s, E_t, decay bk, [event flag e_0] | only if c is in the input stream (it is not, by topology) | only if a c-carrying gradient reaches the GRU weights (blocked by hard write) | S1+S2 | 1, 3, 4 |
| C2 | GRU gates/candidate (z_t, r_t, h̃_t, pre-activations) | as h_t | same as C1; transient, not persistent | same | S1+S2 | 6 |
| C3 | W (the priced slot) | acquisition write (c); refresh π | **yes — by design** | read by S_pol; gradient stops at W's content | (this is the *legitimate* carrier) | — (the control) |
| C4 | V (self-resource state) | energy E_t, decay bookkeeping | only if the bookkeeping encodes W's *value* rather than its *age* | same | S3 | 5 |
| C5 | A (homeostatic readout) | (V, s) | only via V or s (both c-free) | only via V | S1 | 5 |
| C6 | S_pol's inputs beyond W | declared (W, x_t); must **not** read h_t, V, A | only if S_pol is mis-wired to read a c-carrier | — | S4 | 2, 6 |
| C7 | Acquisition-write internals (any buffer/register holding c during the write) | c | yes, transiently | — | cleared at t=0; nothing persists it | 6 |
| C8 | Weight-encoded copy (a "copy gate" learned into the weights) | — | no (weights are not per-episode state) | yes, if gradients route c around W | S2 | 6 (via activations) + pristine-backup rival |
| C9 | Optimizer state / replay buffer (training only) | — | training-only | — | scaffold severance (§10) | (severance gate) |

C3 (W) is the one legitimate carrier; it is priced (paid refresh) and decayed (δ),
so it is not free. Every other channel must carry no c, and the tests below are the
proof.

### 2.3 The four isolation principles

**S1 — forward-pass isolation.** The cue identity c is an input to **no** component
except the acquisition write into W. Concretely: at t=0 the environment delivers the
distractor x_0 (c-independent) and, if the acquisition write is a learned behaviour,
an **identity-free event flag** e_0 ∈ {0,1} ("a cue was presented", identical for
c=A and c=B); the identity itself is consumed only by the supplied acquisition write.
The regime s, energy E_t, and decay bookkeeping are c-independent by the task
construction (§1.3).

**S2 — gradient isolation.** No gradient that depends on c reaches any weight that
could inject c into a recurrent state. This holds iff W's write and read are
**non-differentiable with respect to h_t**: W is a discrete slot whose content is
set by a hard write (a substrate primitive, like π's write — Q4 §5.5) and read with
a stop-gradient through its content. Then S_pol's reward gradient reaches W's
content and stops there; it cannot continue into h_t, so the GRU weights receive no
signal that distinguishes c=A from c=B and cannot learn to reconstruct c from
c-independent inputs. (N4 makes the exact gradient paths and stop-gradients
precise; N3 fixes the *requirement*.)

**S3 — content-blind integrity bookkeeping.** V's integrity estimate is read from
the slot's *age* (decay counter / time-since-refresh), never from its *value*. Age
is c-independent (a slot holding A decays at the same δ as one holding B), so the
integrity component carries no identity. This is the fix that keeps the V channel
closed without letting c ride through V (§3.3).

**S4 — readout isolation.** S_pol reads (W, x_t) only — not h_t, V, A, or any
auxiliary activation. This is what makes the only c-carrier S_pol can read the
priced W, so disabling W (test 1) or severing its readout (test 2) leaves S_pol with
no source of c (§3.4).

These four principles together are what make the closure **structural**: with S1–S4,
h_t contains no information about c at **any** tick — not t=1, not t=D — because
neither its inputs nor its training ever carried c. The contrast with the rejected
alternative is the point of §3.8. "No pristine copy" (§3.6) is a *consequence* of
S1–S4 plus the pristine-backup rival, not a fifth principle.

---

## 3. The structural closure (how the channel is closed by construction)

### 3.1 W is not recurrent

W is a discrete 1-bit maintained slot with exactly two dynamics: decay toward
neutral at rate δ (absent refresh) and re-energization by π (refresh). It has **no**
self-dynamics that integrate any other quantity — it is not a function of h_t, not a
readout of the GRU, and not itself a recurrent cell. Its persistence is therefore the
paid refresh's job by construction (P1), and its content is reachable by no recurrent
path. This is the Q4 §5.1/§5.5 split made exact: W is the *content*, π is the *paid
process* that sustains it, and the GRU is neither.

### 3.2 h_t is fed only c-independent inputs

The GRU's input at every tick is drawn from {x_t (distractor), s (regime), E_t
(energy), decay bookkeeping (content-blind, §3.3), e_0 (identity-free event flag,
optional)}. None depends on c (§1.3, §2.2). Therefore h_t carries no c at any tick —
**not by forgetting, but because it was never there.**

### 3.3 V reads content-blind bookkeeping (the sharp fix for the V channel)

V's integrity component is a learned estimate of *slot integrity*. The trap the audit
must close: if "integrity" were computed by reading W's **value** (to check "is it
still A?"), V would receive c and test 5 would fail by construction. The fix is that
integrity is read from the **content-blind** maintenance bookkeeping — the decay
counter / age of the slot / time-since-last-refresh, which is a function of *whether
and when* the slot was refreshed, not of *what value* it holds. A slot holding A
decays at the same δ as a slot holding B, so age carries no identity. V's energy
component reads E_t (c-independent). V therefore carries no c, and the content-blind
bookkeeping clause is a hard requirement, not an implementation preference: it is what
makes G3a's "integrity component" load-bearing without letting c ride through V.

### 3.4 S_pol reads (W, x_t) only

S_pol's declared inputs are W's content and the current distractor x_t. It must **not**
read h_t, V, A, or any auxiliary activation. This is the forward-pass guarantee that
the only c-carrying state S_pol can read is W — so if W is disabled (test 1) or its
readout severed (test 2), S_pol has no source of c and must be at chance.

### 3.5 Gradient isolation (the hard-write + stop-gradient requirement)

W's content is set by a hard acquisition write (a substrate primitive, non-
differentiable) and read by S_pol with a stop-gradient through its value. Consequence:
no reward gradient reaches the GRU weights with c-dependent information, and the GRU
cannot learn to reconstruct c from c-independent inputs (S2). This is the neural form
of the organism's discipline that "correctness rides the acquisition write, not
continuous repair" (D3) plus P1's "no hidden pristine weight matrix."

### 3.6 No pristine copy

Every state that could hold c is either (a) the priced slot W, or (b) structurally
unable to hold c (S1+S2, §3.2–§3.4). There is no weight matrix, buffer, gate,
readout pre-activation, or residual that holds a copy of c the decay stream never
reaches and no process refreshes (P1's pristine-backup rival). Test 6 is the
catch-all that searches for any such copy; the pristine-backup rival (arm-level) is
the standing detector for any copy the inventory missed.

### 3.7 The acquisition-event flag is permitted, and is identity-free

The card permits the controller to "receive a cue-acquisition EVENT." That flag —
e_0 ∈ {0,1}, "a cue was presented at t=0" — is c-independent (identical for A and B)
and may enter h_t; it carries timing ("acquisition happened"), not identity. Two
notes keep it honest: (a) if the acquisition write is a *supplied* primitive (§3.1),
the flag is not needed in the GRU at all, and the cleanest realization omits it; (b)
if it is kept, the audit must confirm the flag is literally a single constant bit —
any identity-dependent "flag" is a leak and test 6 must catch it.

### 3.8 The rejected alternative, stated so it cannot re-enter silently

The fragile path the card forbids: let c enter h_t at t=0 and "choose D long enough
that the GRU forgets" (τ < D). It passes test 3 by construction but fails the sharp
form of test 4 — c is decodable from h_1 even though not from h_D. It is fragile for
two reasons: it depends on a hyperparameter (D) that the clock-invariance check
(§4.3) sweeps, so it breaks under the sweep; and it leaves the architecture with a
free cue-carrier that happens to decay, rather than no free cue-carrier at all. The
**fallback** for a genuine need: if engineering shows some recurrent state must carry
c for optimization (which the audit does not expect — §1.2), then isolate c into a
**second dedicated maintained slot** with its own δ and its own π refresh cost, so the
pathway is priced and decayed *equivalently* to W, and cutting π kills it exactly as
it kills W. That is "isolate + price/decay the pathway equivalently"; it is not
structural prevention, and it must be disclosed as the fallback it is.

---

## 4. The six leakage tests (specified)

Each test is stated as: the intervention (what is disabled), what remains intact, the
procedure, and the pass/fail criterion. Tests 1–3 are **behavioural** (does the probe
get solved without the priced path?); tests 4–6 are **probes** (is c decodable from a
state that should be c-free?). All are run on the trained, frozen candidate on
engineering seeds, disjoint from the final sample (AC39).

### Test 1 — W disabled, recurrent controller intact

- **Intervention.** W's content is disabled: either the acquisition write is withheld
  (c never enters W) or W is zeroed immediately after t=0. The GRU h_t, V, A, π, and
  the readouts run exactly as trained; S_pol reads the neutral W.
- **Intact.** Every recurrent/stateful component except W's content.
- **Procedure.** Run episodes across the delay; record probe accuracy in the stable
  regime (where a held cue would answer the probe).
- **Pass.** Probe accuracy at chance (within CI). **Fail.** Above chance — then S_pol
  recovered c through a path other than W (h_t, V, A, or a pristine copy), i.e. a
  free channel exists. This is the behavioural form of "the cue is only in W."

### Test 2 — W readout disabled, controller intact

- **Intervention.** W is written and maintained exactly as trained (so its content is
  present and correct), but S_pol's read of W is severed (S_pol sees a neutral W; or
  the W→S_pol edge is cut). Everything else — h_t, V, A, π — runs.
- **Intact.** W's content and maintenance; the full recurrent controller.
- **Procedure.** Same as test 1.
- **Pass.** At chance. **Fail.** Above chance — S_pol has a non-W source of c. This
  is the sharp test of §3.4 (S_pol reads only W): it distinguishes "W holds the cue"
  from "W is one of several carriers," and it is what makes the "content selector"
  role of W load-bearing (Q4 §5.1 I2).

### Test 3 — π disabled, all else intact

- **Intervention.** Cut the paid refresh (r_t ≡ 0). W's initial write at t=0, the
  GRU, V, A, and S_pol all run unchanged.
- **Intact.** Everything except the refresh process.
- **Procedure.** Run the delay; record W's decay time-course and probe accuracy in
  the stable regime.
- **Pass.** W decays on the supplied time constant 1/δ and probe accuracy is at
  chance (the cue is unrecoverable at the probe without the paid refresh). **Fail.**
  The cue survives the cut — probe above chance, or W's content stable absent refresh
  — free permanence (F3). This is the formalization of bridge §9.3 and E1's
  "free-permanence check" and of arm 2's GRU-only variant: the persistence is paid,
  not free.

### Test 4 — decode cue identity from h_t across the delay

- **Target.** The GRU hidden state h_t.
- **Procedure.** Probe h_t at multiple delay ticks T_probe = {t=1, t=m, t=D} (and,
  for the time-course, every tick) using the probe instrument (§4.1).
- **Pass.** c not decodable above chance at **any** probed tick — including t=1,
  immediately after acquisition. **Fail.** Decodable at any tick. The t=1 reading is
  the load-bearing one: decodable at t=1 but not at t=D is *forgetting* (§3.8), which
  fails the test and demands the structural fix, not a longer D.

### Test 5 — decode cue identity from V and A state

- **Targets.** V's content and A's readout/pre-activation.
- **Procedure.** Probe V's discrete code and A's activations at T_probe, using the
  probe instrument.
- **Pass.** c not decodable above chance from either. **Fail.** Decodable from V — the
  content-blind bookkeeping clause (§3.3) was violated (V read W's value, not its
  age), or c reached V another way; decodable from A — c reached the homeostatic
  pathway that must be content-blind (§4.1.3). A fail here also breaks G3c's
  "A is insensitive to reward/content by construction" claim.

### Test 6 — probe all auxiliary activations for pristine copies

- **Targets.** Every activation that could act as a copy: the GRU gates z_t, r_t and
  candidate h̃_t (and their pre-activations); S_pol's readout pre-activation; A's
  pre-activation; any acquisition-write buffer/register; any residual or skip
  connection state; any other tensor in the forward pass that persists across ≥1
  tick. (The inventory is §2.2's C2, C6, C7, C8.)
- **Procedure.** Probe each at T_probe. A pristine copy is specifically one the
  decay/refresh stream never reaches and no process refreshes — so the probe is run
  **with π cut and W disabled**, to expose any copy that survives when the priced
  store does not.
- **Pass.** No target decodes c above chance. **Fail.** Any target does — a pristine
  copy exists; the pristine-backup rival (P1) is the arm-level detector for exactly
  this, and a fail here is its firing.

### 4.1 The probe instrument (for tests 4–6)

One instrument, used identically by all three probe tests, so the results are
comparable and no test can be tuned into passing:

- **Detached measurement.** The candidate's weights are frozen; the probe never
  influences the agent and no gradient flows back into it. The probe is a measurement
  of "is c present in this state," not a mechanism.
- **Data.** M ≥ 100 balanced episodes (c ∈ {A,B} equiprobable), across n ≥ 8
  disjoint seed families; the probe's train and test splits are disjoint families
  (AC39), never a within-family split.
- **Primary instrument.** A **linear** probe (ℓ2-regularized logistic regression,
  regularization swept and cross-validated). For a 1-bit cue this is sufficient to
  detect linear separability, and its low capacity cannot fabricate information.
- **Secondary instrument.** A **bounded MLP** (1–2 hidden layers, capacity
  cross-validated against the train split to prevent memorization), to catch
  nonlinear encoding the linear probe would miss. Reported alongside the linear
  result; a discrepancy is itself a finding, not a tie-break.
- **Baseline and CI.** Chance = 0.5. Report accuracy with an exact binomial 95% CI
  around 0.5 computed on the held-out test episodes. **Pass = accuracy within the
  CI at every probed tick.**
- **Severity reading.** At chance at all ticks → channel closed (structural). Above
  chance at t=1 only → *forgetting*, not structural prevention; treated as a fail
  (§3.8). Above chance at t=D, or at probe-solving accuracy → leak; N1 not identified
  (F3 risk).

---

## 5. How this composes with the frozen protocol

The six tests do not add a new science gate; they make the already-frozen free-
permanence machinery precise, and they do it in the vocabulary the protocol already
uses:

- **Test 3 ≡ the sharpening of §9.3 and E1's free-permanence check.** §9.3 says
  "choose δ and D so that without the paid refresh the cue is unrecoverable at the
  probe, and the GRU-only variant is at chance." Test 3 is that check stated as an
  executable test; tests 1, 2, 4, 5, 6 are the *audit* that says *why* the GRU-only
  variant is at chance (structural isolation), rather than merely *that* it is.
- **Tests 1–2 ≡ the behavioural half of arm 2's role.** Arm 2 (cut π; GRU-only
  variant with W read-in disabled) is the arm-level null. Tests 1 and 2 are the
  candidate-level interventions that the arm-level null summarizes.
- **F3 is the failure these tests pre-empt.** "The cue survives arm 2's cut, or the
  GRU-only variant passes" is exactly a fail of test 3 (survives the cut) or tests
  1/2/4 (a free carrier exists). The six tests are how F3 is *detected before the
  final run*, on engineering seeds, instead of discovered as a run-time failure.
- **Test 5 protects G3c's clean-by-construction claim.** G3c ("A is insensitive to
  reward because it has no access to it") is clean only if A's pathway is also
  content-blind; test 5 verifies that.
- **Severity of a fail.** A fail of any of the six is a **pre-protocol stop**
  (like F5/F6), resolved by the structural fix of §3 before any final seed runs —
  not a run-time falsification to be recorded. A leak that survives to the final run
  and passes F3's threshold is then a recorded F3 falsification, never amended away.

---

## 6. What this hands downstream

- **N8 (v3 protocol).** (1) Fold the six tests of §4 into v3 — concretely, extend
  §9.3 into a **leakage-closure engineering gate** with the six tests as its
  sub-checks, and sharpen E1's free-permanence check to reference test 3. (2) Write
  the structural constraints of §3 into the architecture spec (§3): W non-recurrent
  (§3.1), h_t/V/A input isolation (§3.2–§3.4), content-blind decay bookkeeping
  (§3.3), the hard-write + stop-gradient requirement (§3.5), no pristine copy
  (§3.6), the identity-free event flag (§3.7). (3) Record the fallback (§3.8) as the
  disclosed escape hatch, never as the default. (4) Do not let any wording claim
  "the cue is only in W" off a result that skipped tests 1, 2, 4, 5, or 6.
- **N4 (training objectives / gradient paths).** N3 fixes the *requirement*; N4 makes
  it exact: the specific stop-gradients and non-differentiable write that realize
  §3.5, and confirmation that no reward gradient reaches the GRU or V weights with
  c-dependent information. N4 should read §3.5 as its contract for the gradient-path
  section.
- **N6 (analytic identifiability).** N3 closes the *architectural* channel; N6
  verifies the *task* precondition it rests on (§1.3): that x_t is c-independent and
  that the cue's information genuinely is not present outside W. The two together
  are the "the cue is only in W" claim — N3 the mechanism, N6 the task fact.

---

## 7. Claim discipline

- This document makes no empirical claim about T_bridge and no prediction about
  which arm wins. "The channel is closed" is a claim about the *specified
  architecture*, to be **verified by the six tests at realization**, never asserted
  as achieved here.
- "Structural prevention" means c is absent from h_t at every tick by construction
  (S1+S2), not that the GRU forgets c over a long delay. The two are distinguished by
  test 4's t=1 reading, and only the former is accepted.
- "Content-blind" is a property of the integrity bookkeeping (§3.3): it encodes
  *age*, not *value*. A bookkeeping read that encodes W's value is a leak, however
  innocuous, and test 5 catches it.
- No frozen artifact is edited, re-run, or re-hashed. This is a design note consumed
  by N8/N4/N6; `ACI_BRIDGE_PROTOCOL_v2.md` remains the frozen design until N8 issues
  v3 as a new file.

## Sources

Read, not edited: `PHASE2_BASELINE_v1.md` (N0; §3 architecture, §4 per-component
information, §7(b)(2) the free-recurrent-memory weakness), `ACI_BRIDGE_PROTOCOL_v2.md`
(§2.3 free-permanence constraint, §3 architecture, §4.1.3 A's input restriction,
§5 arm 2 GRU-only variant, §6 E1 free-permanence check, §7.2 F3, §9.3 engineering
gate, §10 scaffold severance), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; §4
substrate, §5.1 W, §5.2 V, §5.5 π, §5.6 A, §5.4 workspace), `N1_RIVAL_SELECTION_
CORRECTION_v1.md` (N1; identifiability-not-superiority), `N2_INPUT_SOURCE_AUDIT_v1.md`
(N2; six-way source taxonomy, the content-blind boundary cases), `ACI_ARCHITECTURAL_
PRINCIPLES_v1.md` (P1 pristine-backup rival and free-permanence, D3 correctness-rides-
acquisition), `ACI_NEURALIZATION_MAP_v1.md` (P1's "reference copy in the vulnerable
substrate"). Study references from the skill: `ac11` (level-not-switch), `ac39`
(disjoint seed families), `ac109` (non-ignorance), `ac113` (trade-off direction).
