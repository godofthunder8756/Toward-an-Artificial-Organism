# T_bridge identifiability v2 — Path B (corruption-stream integrity) is still unidentifiable, and the paid refresh has no correct content to write: documented STOP

2026-09-26. Deliverable for the N6b card (t_1b31220c): *does a re-designed T_bridge —
where W's content is flipped by an unrevealed corruption stream rather than
age-determined decay — have an identifiable latent integrity state (two histories with the
same observable tuple but different optimal maintenance actions due to different latent
integrity)?* This is a **new file**; it supersedes `TBRIDGE_IDENTIFIABILITY_v1.md` in the
reading order but does not edit it. It carries the operator's Path B decision (2026-09-25)
to make integrity genuinely latent, re-specifies the design per v1 §8.1, and re-runs the
identifiability test of N1 §3.3 / N6 on the re-designed problem.

This is a **derived analysis document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It reads the bridge vocabulary from
`ACI_BRIDGE_PROTOCOL_v2.md` §2–§4, `ACI_BRIDGE_PROTOCOL_v3.md` §10, the N1–N3 corrections,
and the AC67–AC71 damage line, and does not re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); nothing here is a consciousness claim. (2) This document
makes no empirical claim and no prediction about which arm wins. (3) "Identifiable" carries
N1 §3.3's meaning — *the permitted observation/history separates the integrity states* —
never "the candidate wins." (4) "Necessary" carries N2 §6's meaning — *the no-V rival
provably fails to reproduce the candidate* — never the weaker "internal information matters."

---

## 0. The one-paragraph answer

**No — and the failure is more fundamental than v1's.** v1's verdict was that integrity is
*observed, not latent* (`I_t = f(d_t)`, the age counter is handed to every arm). Path B
replaces the readable age counter with an unrevealed corruption stream, and the re-verified
verdict is that this does **not** produce an identifiable latent-integrity problem — for a
reason v1 did not need to state: **under the bridge's own isolation constraints, W's
correctness has no observable correlate at all during the delay, so an unrevealed
corruption of W is unobservable in principle, not merely unrevealed.** There is no
downstream consequence to infer from, and — a second, independent blocker — **the paid
refresh π has no correct content to write** (c is unobservable after t=0 and a pristine copy
is forbidden by N3 §3.6), so "maintain-or-drop" is not a decision the substrate can even
execute. Making corruption *inferable* requires relaxing exactly the constraints that
define the bridge as a deferred-cue task — and the relaxed task is T1/T7, whose "response to
corruption" treats the damage signal as **observable** (a minority/disagreement count
computed from the system's own state, AC71) and whose load-bearing question is *who enacts
the repair*, not *whether integrity is inferred*. The "inferred, not observed" integrity
(clause (c)(i)) is therefore unsupported not only by T_bridge but by the corruption regime
it points to. **Documented STOP**: N7b is not unblocked; the central claim needs a task that
does not exist in either regime, not a re-design of this one.

---

## 1. The question and what N6b owns

### 1.1 The exact question

N1 §3.3 replaced the bridge's "genuinely beatable" engineering gate with an
identifiability test: construct matched situations that differ only in the **actual
integrity** of the maintained cue slot, and ask whether the permitted observation/history
distinguishes them. N6 answered analytically for T_bridge: **no** — integrity is a
deterministic function of the observable decay age `d_t`. The operator's Path B decision
then directed that integrity be made genuinely latent (v3 §10): replace uniform δ-decay with
a corruption stream whose flips the substrate does not reveal, and re-verify. N6b's question
is the same test, run on the re-designed problem:

> Are there two histories with the same current observable tuple but different optimal
> maintenance actions, where the difference traces to different latent integrity?

### 1.2 What N6b does and does not decide

- N6b decides **whether the corruption-stream re-design makes integrity a latent that must
  be inferred** (identifiable → N7b proceeds) or **whether the re-design is itself
  unidentifiable or ill-posed** (not → documented STOP, per the card's own "do not loop").
- N6b does **not** decide whether the candidate wins, does **not** pick Path A vs Path B
  (the operator picked B), and does **not** authorize a further redesign cycle. Its verdict
  is a **Tier-0 prerequisite** (N5 §2.1), a pre-protocol stop signal, never a recorded
  falsification.

### 1.3 The re-design is a *specification* here, not a run

The card names the re-design but does not fully specify it. Two load-bearing details are
left open by "flipped by an unrevealed corruption stream" and must be fixed before any
identifiability claim can be made: **(i) what the paid refresh writes** (the content problem,
§4), and **(ii) what observable, if any, carries information about correctness during the
delay** (the consequence problem, §6). This document fixes both against the frozen bridge
vocabulary, then tests identifiability. It is an analysis of the re-designed *decision
problem*, not an executed simulation.

---

## 2. The re-design spec (Path B)

Replacing v1 §8.1's hand-wave with a spec that the frozen constraints actually permit. The
change is confined to the **decay law** and its **bookkeeping**; everything else — the cue
presented once at t=0, the delay 1…D, the distractor stream, the announced regime, the
energy economy, the paid refresh line item E_π, the arms, the leakage controls, the
identifiability test — is carried unchanged (the card's "keep" list).

### 2.1 What changes

| Frozen element (v2/v3) | Re-design (Path B) |
| --- | --- |
| Decay law: W relaxes toward neutral at rate δ (erase, not overwrite) | Corruption law: W's content is **flipped** (A↔B) by a stochastic stream at rate ρ per step; a flip is **sticky** (persists until a repair writes over it) |
| Bookkeeping: substrate hands every arm the decay age `d_t` | Bookkeeping: the substrate does **not** reveal the flips; no age/corruption counter is handed over |
| Integrity `I_t = f(d_t)` (observed) | Integrity `I_t = 1[W_t = c]` (claimed latent) |
| Refresh π = re-energize (reset the age counter; content already correct) | Refresh π = **undefined until specified** (§4) |

The sticky-|= model is the AC67–AC71 primitive lifted to the bridge: a flip that stays
flipped until a paid repair overwrites it. The intended consequence (the card's words): the
agent must infer "is W still correct" from *downstream consequences* — prediction error,
agreement signals, maintenance-machinery bookkeeping — not from a readable age counter.

### 2.2 The three candidate signal channels, named

The card names three downstream consequences. All three are examined in §6:

1. **Prediction error** — W is used continuously to predict/act, and errors reveal W≠c.
2. **Agreement signals** — k redundant replicas of W; disagreement reveals corruption.
3. **Maintenance-machinery bookkeeping** — the repair process's own accounting.

Each is tested against the bridge's isolation constraints (N3 S1–S4) in §6. The finding is
that none of the three survives those constraints as a *content-blind, c-independent*
signal of integrity — which is exactly what N3 requires any V input to be.

---

## 3. The new decision problem, written out

### 3.1 State variables

| Variable | Meaning | Where it lives |
| --- | --- | --- |
| `c` | latent cue ∈ {A, B} | environment; supplied to W only at t=0 (N3 S1) |
| `s_t` | regime {stable, volatile} | environment; **announced** at t=m (observable) |
| `E_t` | energy | substrate bookkeeping (observable) |
| `W_t` | cue slot content ∈ {A, B} (possibly corrupted) | the maintained slot (the thing being maintained) |
| `I_t` | integrity = `1[W_t = c]` | **the claimed latent** |
| `h_t` | GRU hidden state | the agent; fed only c-independent inputs (N3 S2) |

Under Path B there is **no** `d_t` (the age counter is removed). The corruption state — which
replicas/values have flipped and when — is hidden. `W_t`'s *value* is readable by the agent
(it is its own memory); `W_t`'s *correctness* is not.

### 3.2 Observable variables (the tuple common to every arm)

At tick t every arm receives (N2 §5.3, N3 §2.2, minus the removed age counter):

1. `x_t` — distractor stream (i.i.d., independent of c; N3 §1.3);
2. `s_t` — announced regime;
3. `E_t` — energy reading;
4. its own action history — refresh choices, which determine E_t through the economy.

**Nothing in this tuple depends on W's correctness during the delay.** Item 4 is the only
history the agent has, and it is a record of the agent's *own actions*, not of the
corruption stream. This single observation — stated here, established in §6 — is the whole
verdict: the re-design removes the one quantity (`d_t`) that made integrity observable,
without supplying any replacement that is observable under N3.

### 3.3 Latent variables

- **The corruption stream** (which flips happened when) — genuinely hidden; the substrate
  does not reveal it.
- **The integrity `I_t`** — the quantity the card asks about. The claim under test
  (H clause (c)(i)) is that V infers `I_t` from downstream consequences. §6 shows there are
  no downstream consequences to infer from, so `I_t` is not "inferred but unavailable" — it
  is **absent from the observation**, and the inference has no evidence.

---

## 4. The refresh-content blocker (π is undefined under corruption)

The card's "keep" list includes the paid refresh π. But under corruption π has **no correct
content to write**, and this is independent of any identifiability question. It is a
specification failure that must be closed before the decision problem is even well-posed.

Under δ-decay, W relaxes toward *neutral* — content is **erased, not overwritten** — so
"re-energize" (reset the age counter) restores persistence without needing to re-observe c:
the correct content is still sitting in the slot, merely fading. Under corruption, W's
content is **flipped** — the wrong value is *written over* the right one — so "re-energize"
preserves the wrong value. Restoring correctness requires writing c, and there are exactly
three sources of c, each blocked:

| Refresh semantics | Source of the written value | Blocked by |
| --- | --- | --- |
| rewrite c from a pristine copy | a hidden backup of c | N3 §3.6 "no pristine copy"; v2 §3 standing rule 1 (the reference copy lives in the vulnerable substrate) |
| re-acquire c from the environment | re-presentation of c | "cue observable only at t=0" (T2's defining fact; v2 §2.1) |
| majority-restore across k replicas | the majority value (assumed correct) | AC67: repair cements a flipped majority; and requires k replicas, a different architecture (§6.2) |

Consequence, stated once: **under the bridge's constraints, "maintain-or-drop" is not a
decision the substrate can execute.** The refresh either writes the wrong content (re-energize
a flipped slot), needs a forbidden pristine copy, needs an unavailable re-observation, or
silently changes the architecture to a redundant majority-restore. A decision problem whose
action ("refresh") has no defined effect is not identifiable — it is ill-posed. This is a
*separate* failure from the identifiability verdict of §6 and would block the re-design even
if a signal channel existed.

(For completeness: the redundancy escape — k replicas, π = majority-restore — *is* a
well-defined refresh, and it is the AC-consistent Path B. It is analyzed in §6.2; it does
not rescue identifiability.)

---

## 5. The oracle and DP (degenerate where faithful)

### 5.1 The faithful re-design has a degenerate oracle

Recall v1 §3.2: under δ-decay the optimal policy is `refresh iff s=stable ∧ E≥E_crit ∧
d_t≥L−1` — a non-trivial threshold because refresh *causally preserves* c. Under corruption
that causal link is severed. The agent's refresh cannot prevent a flip (corruption is a
random event independent of refresh) and cannot undo one (refresh writes W's current value,
not c). So **the maintenance action has zero causal effect on the probe outcome**: probe
success depends on whether the corruption stream happened to spare W, which no policy
controls.

Formally, the value of any refresh policy is

```
V^π = E[ reward | π ] = P(W_D = c) · P(correct readout | held) + …,
```

and `P(W_D = c)` is set entirely by the corruption stream, not by π. Every policy — refresh
always, refresh never, any schedule — attains the same value. The optimal allocation is the
**constant** policy, and the homeostatic cost `1[I_t ≠ I*(s_t,E_t)]` is minimized by doing
nothing (a refresh spend that buys nothing is dominated by not spending). The DP is
degenerate: there is no state-dependent allocation to discover.

This is the corruption analogue of AC109 ("storage is inert where the current observation
is decisive") and the AC113 trade-off check, pushed to the limit: **there is no trade-off
to allocate across, because maintenance buys nothing.** A re-designed T_bridge with an
unrevealed corruption stream and no downstream consequence is not merely unidentifiable —
its maintenance decision is vacuous (F5, in the pre-protocol sense).

### 5.2 The tractable relaxation (the only case with a non-degenerate DP)

The DP becomes non-degenerate exactly when a downstream consequence makes `W_t`'s
correctness informative — i.e., when the stream depends on c and W is used continuously.
That is T1/T7, not T_bridge; its belief structure is given in §6.1/§6.2 so the boundary is
named rather than asserted.

---

## 6. The identifiability re-verification (the two-histories question, three channels)

The matched-situations construction of N1 §3.3: hold `(energy, regime, reward, clock)` fixed,
vary the actual integrity, ask whether the permitted observation separates the states. Run it
for each signal channel.

### 6.1 Channel 1 — prediction error (the task stops being T_bridge)

For prediction error to reveal `W ≠ c`, the agent must use W to predict an observable that
depends on c. But the bridge's distractor stream is declared **i.i.d. and independent of c**
(N3 §1.3, v2 §2.3) — that independence is *what makes the cue only in W* and is a
precondition the whole leakage audit rests on. Making the stream depend on c so that
prediction errors reveal corruption does three things at once:

1. **It breaks N3 S1.** If `x_t` carries information about c, then c enters the GRU's
   input stream, the GRU can recover c from `x_t` for free, and the free-recurrent-memory
   channel N3 closes is reopened. The "cue is only in W" claim — the load-bearing premise of
   N1/E1 — is false.
2. **It changes the task.** "Hold a cue observable only at t=0 across a delay" (T2) becomes
   "maintain a belief about a latent cause from a weakly-informative stream" (T1) or "detect
   and repair damage via its consequences" (T7). Both are *different benchmarks* with their
   own claim ceilings (v3 §10 already recorded Path B as "T7 / a different task"; this
   confirms it).
3. **It re-collapses to a compact statistic.** In T1 the observable is a two-cause HMM, and
   the belief `P(c | x_{1:t})` has a **scalar sufficient statistic** (the log-odds, updated
   recursively). T1's own "simplest sufficient policy" is "a maintained discrete accumulator
   — a 1–2 bit belief updated by an evidence-weighting rule" (the AC116 integer counter);
   "a graded posterior buys nothing here (D1)". So even where integrity *is* inferable, the
   strongest rival is a maintained **counter**, and the discrete paid-maintained self-state V
   is a lossy re-encoding of it — the v1 collapse, one level up, not its negation.

**Two-histories verdict for channel 1:** YES in the "same current observation, different
accumulated history" sense (the POMDP belief differs), **but only after the task is T1/T7,
not T_bridge**, and the sufficient statistic is a scalar, so the bridge's specific claim —
a discrete maintained self-state is the load-bearing integrity mechanism — is still
unsupported (N2 §6: "internal information matters" ≠ "an explicit maintained self-state is
necessary").

### 6.2 Channel 2 — agreement signals (reveals drift, not correctness)

Redundant replicas (`k` copies of c) give an observable **disagreement count** `m_t =
min(#A, #B)`. This is the AC-consistent, refresh-defined variant (§4), so it is the one
case worth the full two-histories test.

The obstruction is the **missing baseline**. Disagreement tells the agent *that replicas
differ*; it does not tell it *which value is correct*, because c is unretained (N3 S1: c
enters no recurrent state; W is its only record). Reading W gives the values, and the
question "is the majority still c" is a question about the values *relative to c*, which the
agent cannot answer. Two consequences:

- **A symmetric flip is information-theoretically invisible.** "All replicas read A" is
  consistent with "c=A, no corruption" and with "c=B, total corruption"; the posterior over
  integrity is the prior. With disagreement (`m_t > 0`), the agent knows there is drift but
  not which side is the drift. The only thing that breaks the symmetry is *remembering the
  initial value* — which is retaining c in the recurrent state, exactly the leak N3 S1/S2
  close (and N3 §3.8's "forgetting" path: decodable at t=1 is the failure signature).
- **There is a forced dilemma.** Either (i) the agent retains the initial content — then
  integrity is **observable** (compare current majority to retained c), back to v1's
  collapse; or (ii) it does not (N3 honored) — then integrity is **unidentifiable** (the
  baseline is lost). **There is no configuration in which integrity is both genuinely latent
  and inferable within the bridge's content-isolation constraints.** The symmetry of "flip
  A↔B" is what makes this unavoidable: the only reference for "correct" is the very content
  whose retention the isolation principles forbid.

The sticky-|= (asymmetric, set-to-1) variant does not escape this. Set-to-1 is *detectable*
only when c differs from the set value (an AC67-encoded damage bit is visible because it
differs from the program's majority), and that detectability is itself c-dependent — for a
1-bit cue, corruption of c=A is visible while corruption of c=B is a no-op, so the signal
is exactly as informative as the content it was supposed to hide. And in the AC line the
question "is the majority still correct" is never *inferred* — it is **assumed** by the
majority-restore, and AC67's cementing failure is the recorded proof that the assumption
can be violated. Detected damage ≠ inferred integrity.

**Two-histories verdict for channel 2:** NO, and not for v1's reason. Integrity is not a
function of the observable tuple — it is *absent* from it. Two histories can share the same
observable tuple and differ in integrity, but no policy can tell them apart, so there is no
pair of histories with different *optimal* actions that differ *because of* the latent. The
latent is idle, not load-bearing.

### 6.3 Channel 3 — maintenance-machinery bookkeeping (the collapse, re-branded)

If the "bookkeeping" the agent reads is a substrate counter of the repair process (a
damage/minority count, a refresh tally), then integrity is again a deterministic function
of an observable counter — the v1 `d_t` result with the counter renamed. The sufficient
statistic is `(s_t, E_t, m_t)`, the oracle is a threshold on `m_t`, and the strongest rival
is the memoryless state machine `refresh iff s=stable ∧ E≥E_crit ∧ m_t≥τ`. Collapse, exactly
as v1 §7.2. If instead the bookkeeping is *itself* in the corruption stream (so it cannot be
a reliable signal), then it carries no information and channel 3 reduces to §5.1's vacuity.
Either way, no latent.

---

## 7. The sufficient-statistic collapse re-test

The card asks whether "a compact sufficient statistic (e.g. observable prediction-error
history) collapses the architecture." The answer, stated across the three channels:

| Channel | Is integrity latent? | Compact sufficient statistic | Does it collapse the architecture? |
| --- | --- | --- | --- |
| 1 — prediction error (requires T1/T7) | YES (inferred from history) | **scalar log-odds / maintained counter** | Collapses to a **counter** — the discrete V is a lossy re-encoding (T1's "simplest sufficient policy"); the bridge's discrete-self-state claim is unsupported |
| 2 — agreement signals | NO (absent; or observable iff baseline retained) | disagreement count `m_t` (if observable) | Collapses to a **memoryless threshold on `m_t`** (v1's collapse, renamed) — or is vacuous (no baseline) |
| 3 — maintenance bookkeeping | NO | `m_t` / refresh tally | Collapses to the `(s, E, m)` state machine |

The pattern is the same as v1's, at one level of abstraction higher: **wherever the
integrity state is made inferable, the inference has a compact, observable-or-scalar
sufficient statistic that a simple rival maintains; wherever it is made genuinely latent,
the inference has no evidence and the maintenance action is vacuous.** There is no middle
regime in which integrity is latent, inferable, *and* a discrete paid-maintained self-state
is the load-bearing mechanism. This is the AC77 fixed-point lesson ("a life is one sample;
the belief collapses to a counter") and AC109 ("storage is inert where the current
observation is decisive") generalizing together: the corruption re-design does not create a
latent that needs a self-state; it creates either an observable count or a vacuity.

---

## 8. Boundary conditions (when the answer would flip — and why that is a different task)

Named so the "no" is not read as universal and so N7b knows what, if anything, could unblock
it:

1. **A c-dependent stream with continuous use of W (T1).** Integrity becomes inferable from
   the prediction-error history — but the sufficient statistic is a maintained scalar
   (counter), the simplest rival is that counter, and the claim ceiling is T1's: **N1+N2
   (active persistence + content load-bearing)**, never endogenous allocation (T4) and never
   "inferred self-state integrity" (clause (c)(i)). This unblocks *a* task, not *the
   bridge's* claim.
2. **An observable damage signal with internalized repair (T7).** The corruption regime the
   AC67–AC71 line actually implements: the damage signal is **observed** (a minority count
   computed from the system's own state), and the load-bearing question is **who enacts the
   repair** (system vs host watchdog — the observer-discard test, AC95-D4), not whether
   integrity is inferred. T7's spec is explicit that the rival "sees the same damage signal;
   the contrast is *who* computes and enacts the repair, not whether the damage is visible."
   This is a real, answerable experiment — and it **does not require latent integrity**.
3. **A retained baseline (relaxing N3 S1).** If the agent is permitted to retain the initial
   content separately, integrity becomes observable (compare to the retained value) and the
   v1 collapse returns. Relaxing the isolation to make integrity latent defeats the purpose;
   relaxing it to make integrity observable undoes the re-design.

The constructive reading: the program's actual "inferred integrity" ambition, wherever it is
honestly testable, is **T1 (maintained hidden-state inference over a cause)** or **T7
(internalized repair of observed damage)**. Neither is the bridge. The bridge's clause
(c)(i) — "whose integrity component is inferred, not observed" — has no faithful realization:
the δ-decay slot makes integrity observed, and the corruption slot makes it absent or
observed-as-damage.

---

## 9. Go/no-go verdict and what this hands downstream

**NO-GO. Documented STOP.** The re-designed T_bridge (Path B) is not identifiable, for two
independent reasons, and the second survives even a fix to the first:

1. **No signal (identifiability).** Under the bridge's isolation constraints (cue observable
   only at t=0; distractor i.i.d. independent of c; W the only record of c), W's correctness
   has no observable correlate during the delay. The corruption is unobservable in
   principle, the two-histories contrast has no pair with different *optimal* actions
   attributable to the latent, and the maintenance DP is degenerate (§5.1).
2. **No action (well-posedness).** The paid refresh has no correct content to write: c is
   unobservable after t=0 and a pristine copy is forbidden. "Maintain-or-drop" is not
   executable by the substrate as specified (§4).

Because both are **structural facts of the task + the permitted information**, not wording
or under-powering, they are a pre-protocol stop (N1 §3.3, N5 §8.8), never a run-time
falsification and never a gate to move. Per the card's directive, this document stops here
and does not loop into a further redesign.

**What this hands N7b (and the operator):**

1. **Do not proceed with N7b on a corruption-stream T_bridge.** There is no power analysis
   to write: the contrast has no well-posed action and no latent to grade. N7b should be
   re-parented or re-scoped rather than executed against this design.
2. **The honest successors are named, not the bridge.** If the program wants "inferred
   integrity," it is T1 (claim ceiling N1+N2, sufficient statistic a scalar counter); if it
   wants "internalized response to corruption," it is T7 (damage observable, load-bearing
   question = who enacts repair). Both are answerable; both are different experiments; both
   must be authorized as new cards, not as "N6b fixed the bridge."
3. **Carry forward the general rule**, which is this document's durable output: **a
   representation's integrity can be (i) observed (age counter / damage count), (ii) inferred
   from consequences (requires the content to be in continuous use against a content-dependent
   stream — and the inference's sufficient statistic is a scalar/counter), or (iii) absent
   (content held in isolation from any observable consequence). There is no fourth case in
   which a *discrete paid-maintained self-state* is the load-bearing inference mechanism.**
   Any future "inferred self-state" claim must first locate itself in case (ii) and then
   beat the scalar-integrator rival — a hurdle the AC67–AC71 line never cleared either (its
   repair is threshold-on-count, not belief-over-latent).

---

## 10. Claim discipline

- This is a **level-(b)/(c) representational** analysis in N1 §3.3's sense: it establishes
  that the re-designed integrity state is *absent from the permitted observation, and the
  maintenance action ill-defined*, nothing more. It makes no level-(d) claim, no claim that
  the candidate would lose, and no claim crossing the level-(d)/(e) boundary.
- "Unidentifiable = NO" here means *two things at once and they must be kept distinct*:
  (a) no two matched histories differ in optimal action *because of* the latent (the latent
  is idle — no signal); and (b) the refresh primitive is undefined (no action). Neither is a
  verdict that the mechanism is inert in general; both are verdicts about **this design**.
  Memory for the *content* (W, N1) is untouched — what is denied is only the *allocation's*
  dependence on an *inferred* integrity and, further, the executability of that allocation
  under a corruption stream.
- "The corruption regime does not require inferred integrity" is a statement about the
  AC67–AC71/T7 design (damage observed, repair internalized, correctness assumed), not a
  claim that no conceivable system infers integrity from consequences. T1 is that system's
  home, with its own ceiling.
- No frozen artifact is edited, re-run, or re-hashed. `ACI_BRIDGE_PROTOCOL_v3.md` remains
  the last issued protocol (a STOP); this document is a design note consumed by the operator
  and N7b.

---

## Sources

Read, not edited: `TBRIDGE_IDENTIFIABILITY_v1.md` (N6; §6 the two-histories verdict, §7 the
sufficient statistic, §8.1 the corruption boundary), `ACI_BRIDGE_PROTOCOL_v3.md` (§10 Path B,
§9.2 the audit), `ACI_BRIDGE_PROTOCOL_v2.md` (§2.1 task, §2.2 economy, §2.3 free-permanence,
§3 architecture), `N1_RIVAL_SELECTION_CORRECTION_v1.md` (§3.3 the identifiability test),
`N2_INPUT_SOURCE_AUDIT_v1.md` (§5.3 the non-handicapping clauses, §6 the
maintained-self-state-vs-internal-information distinction), `N3_LEAKAGE_AUDIT_v1.md`
(§2.3 S1–S4, §3.6 no pristine copy, §3.8 the forgetting path), `PHASE2_BASELINE_v1.md`
(§3 architecture, §4 per-component information), `ACI_PHASE2_BENCHMARKS_v1.md` (§3.1 T1,
§3.2 T2, §3.7 T7), `DEFINITIONS_CHARTER_v1.md` (§2 levels), `TASK_IDENTIFIABILITY_v1.md`
(K4; the action-observation identifiability form). Study references from the skill: `ac67`
(sticky-|=, repair cements a flipped majority), `ac71` (read/repair threshold), `ac77`
(fixed-point / counter collapse), `ac109` (storage inert where the current observation is
decisive), `ac113` (trade-off direction), `ac95-d4` (observer-discard equivalence),
`ac110` (in-window vs post-window repair).
