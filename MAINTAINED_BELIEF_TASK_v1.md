# Maintained-belief task v1 — a two-cause, partially-observed task and its discriminating predictions

2026-09-22. **Design document, not a study.** No experiment run, no seeds, no protocol, no
freeze. This is C1's deliverable: a task specification and discriminating predictions, before
implementation. It stands on the R3 chosen mechanism (`CONSCIOUSNESS_ROADMAP_v1.md` §4) and the
A1 ledger (`DEPENDENCY_AUDIT_v2.md`), and it hands to C2 the separability requirement (estimate
causal role vs resource cost / sensor damage / motor impairment / memory capacity).

The task is not yet discriminating unless it is falsifiable by the named rivals — and this
document states the rival that is most likely to falsify it, and the measurement that would
catch it. If a rival reproduces the estimate's behaviour, that result is reported and the
question refined; it is not concealed (the card's falsification rule).

---

## 1. The research question, made computational

Can a minimally sufficient partially-observed task be designed in which **two distinct causes
produce the same immediate failure** — (i) *environmental change* (the world moved) and
(ii) *impaired access machinery* (the stored content is still correct but the organism cannot
read it) — and in which **distinguishing them requires an internally maintained estimate**, not
an externally supplied diagnosis and not a raw failure counter?

The target organism is the AC105 body (the frozen reference architecture, `DEPENDENCY_AUDIT_v2.md`
§1). Its first-order content-bearing state is the **route memory** (component C7): acquired
key→port entries bound from productive contact outcomes, stored in damageable state, read by
majority, maintained by paid renewal. The estimate under test is a **second-order state about
why that first-order state is failing** — the R3 mechanism e ∈ {E_world, E_machinery}.

---

## 2. The two causes (both expressible in the frozen world)

The failure in both cases is identical: **a contact attempt on channel 1 fails to yield
income**. The causes differ only in *what is wrong*.

**E_world — the world moved.** At a scheduled tick T (post-development, T > DEV), the channel-1
mapping flips (the frozen AC100/AC105 `MOVE`, `mapping[1] -> 1 - mapping[1]`). The route-1 entry
is **intact and self-consistent** — it still reads the port that was correct *before* the move.
Contacts on channel 1 fail because the stored value is now obsolete. Nothing is damaged.

**E_machinery — the access machinery is impaired.** At the same tick T, the organism's *read* of
the route-1 entry is suppressed for a declared window W (a machinery cut: `memory.read(1)`
forced to return `None` during [T, T+W), so the contact falls back to blind search —
`selected is None -> port = coin`). The entry's replicas are **untouched and its content is
still correct**; the organism simply cannot access it during the window. Contacts on channel 1
fail at the blind rate (1/PORTS) during the window, then resume succeeding **without any
re-binding** once the read is restored, because the entry was valid all along.

The read cut is the same *kind* of intervention the frozen arc already sanctions as
machinery-suppression, not a conservation-law patch: `ac9.step`'s `blocked` parameter suppresses
renewal, and AC91/AC92's W-birth block / W-cut suppress the write machinery. A read cut
suppresses the read machinery. It changes only which port the contact uses; the `ac4.balance`
identities (material/energy/fuel, in-step asserts) hold unchanged. **With the cut disabled
(W = 0), the world is byte-identical to the frozen one** — the single-change license that a
later study will have to re-derive as a `state_hash` equality, exactly as AC12/AC75/AC89 did.

---

## 3. The organism receives observations, not a diagnosis

The organism's observation is the frozen nine-bit `ac9.observe` (substrate, charter §5) plus the
contact outcome (`productive`), and nothing else. It is **not** told which cause is active.

Crucially, **no single observation bit separates the two causes** at the moment of failure:

- **obs bit 2 (corruption)** is computed over the *program* bank (`traces[0,:126]` minority ≥ 4,
  `ac9.observe` line 55-56). Neither a route move nor a route-read cut touches the program bank,
  so obs bit 2 behaves identically (ambient only) in both causes. This is deliberate: obs bit 2
  is the AC67/71 repair reflex's input, and the R3 roadmap (its §3) explicitly says the mechanism
  under test is *not* that reflex. If obs bit 2 separated the causes, the task would be a
  relabelled reflex and this document would say so.
- **obs bits 3-4 (renewal-urgent)** reflect the memory bank's *aging* (`life ≤ 16`) and
  *replica mismatch* (`bits != decoded majority`). In E_world the entry is intact (no mismatch;
  urgent reflects only aging). In E_machinery the entry is also intact (the cut does not flip any
  replica), so urgent again reflects only aging. The two causes are indistinguishable on these
  bits too.

The causes are therefore **not distinguishable by any passive single-tick observation**. They are
distinguishable only by an *intervention* whose outcome is contingent and must be remembered —
which is what the estimate is for (§5).

---

## 4. The available actions permit informative intervention

The frozen action space already contains everything the task needs (no new actions):

- **Retry** — contact channel 1 again (action 0/1), observing whether the outcome is productive.
- **Probe / repair** — renew the route entry (action 3/4), a paid write that refreshes the
  entry's replicas and life; this is the "is the access path fixable" probe.
- **Abandon / relinquish** — the Gray-streak `_drop` (erase the entry, set the register bit),
  the frozen erase-on-relinquishment path (AC75).
- **Re-bind** — the deposit path (`mem.deposit`), which binds a fresh key/port from a productive
  contact outcome (gated on `grow` in the frozen world; see §8 on the declared gate).

The informative intervention is the **hold-and-observe probe**: withhold relinquishment, keep
contacting channel 1 across the window, and read the *resumption of productivity* as the verdict.
Productivity resuming **without re-binding** is the signature of E_machinery (the entry was
valid); productivity *never* resuming is the signature of E_world (the entry is stale). A second,
complementary probe is **re-bind-and-compare**: a re-bind that yields a *different* port than the
one previously held signals E_world; the *same* port signals E_machinery. This second probe
requires remembering the previously held port — again, a maintained state.

---

## 5. The internally maintained estimate

**Content.** A one-bit register e ∈ {E_world, E_machinery} (the R3 mechanism), plus the window
timing its update rule needs (either folded into the existing maintained W-funded timer, C6, or
a second maintained bit — C2's implementation choice, but the timing state must be vulnerable
and paid-maintained, not a host field).

**Storage.** Vulnerable, paid-maintained state in the existing substrate: a spare region of
`traces` — either bank 0 beyond the 126 program bits or bank 1 beyond the
description/pointer/CTRL offsets (both are "legacy, damageable, not read by the interpreter"
space per `DEPENDENCY_AUDIT_v2.md` §1). Damaged by the ambient sticky-SET stream, read by the
same majority-of-7 convention as every other vulnerable read, repaired by a paid majority-restore,
and **excluded from `reg_from_active`** (decision state, not program content) — exactly the
AC12 register / AC96 streak treatment. The initial value is chosen so the acquired organism is
byte-identical to the frozen one (invert the semantics, the AC12 pattern: 0 = the acquired value).

**Update rule (from the organism's own observations only).** On a contact-1 failure the estimate
enters "hold" and the organism continues to contact channel 1 across a declared window W:
- if a productive contact-1 outcome occurs within W (productivity resumed without re-binding) →
  e = E_machinery, streak reset;
- if no productive contact-1 outcome occurs in the whole window → e = E_world → relinquish.

The correctness of e is a property of this rule against the organism's own realized outcomes. **No
externally supplied diagnosis**: nothing tells the organism "the world moved" or "your read is
cut". The cut itself is an environmental intervention the organism experiences only as failed
contacts.

**Two distinct consumptions (the content is flexibly consumed, not a reflex).**

1. **e = E_world → relinquish.** Erase the stale entry and re-bind (or, if re-binding is gated
   off, stop spending on the dead route). The same bit selects a *different* downstream behaviour
   than (2).
2. **e = E_machinery → maintain.** Withhold relinquishment **and direct spend to renewal** so the
   still-valid entry survives the read-outage window (proactive renewal, ahead of the
   renewal-urgent bit). This second consumption is *active* — it is a maintenance commitment made
   *because* the failure is attributed to the access path, not a passive "not yet relinquished".

The two branches are observably different (relinquish + re-bind vs renew-and-hold) and
economically different (relinquishment spend vs maintenance spend), which is the R3 requirement
and the level-(c) "flexibly consumed" bar (`DEFINITIONS_CHARTER_v1.md` §2).

**Costs, accounted for (requirement 6).**

| cost | what it is |
| --- | --- |
| storage | 1-2 bits × 7 replicas in vulnerable space, damaged by the ambient stream |
| update | a paid, W-gated, atomic write on each cause resolution (≤ 7 replicas per bit; the AC96 `streak_write` pattern) |
| sensing | free — the update reads the organism's own `productive` outcome and the tick clock |
| maintenance | the estimate is damaged by the program stream and repaired by the paid bank-0 majority-restore (action 2), like the register and streak |

The estimate is thus a **component** in the charter's sense only if it is read as *state* (C1
existence, damageable finite state); it is *not* claimed to be produced/replaced (C2), so it is a
level-(c) representational mechanism, not a level-(a) closure claim.

---

## 6. Distinguishability, argued before implementation

The causes are distinguishable from the organism's own action-observation history, by the
temporal structure of the failure:

- **E_world** produces a **permanent** failure: the stored port is wrong for the rest of life;
  productivity resumes only after the stale entry is replaced (re-bind to the new port). Holding
  the route forever never recovers productivity.
- **E_machinery** produces a **transient** failure: productivity resumes on its own at T+W
  (the read is restored, the entry was correct throughout). Holding the route through the window
  recovers productivity without any re-bind.

This is a real, frozen-code-grounded asymmetry (`ac9.step` line 86: a stale entry fails forever;
a read-cut entry resumes once the cut is lifted, because its bits never changed). An organism
that can **hold and observe** can separate the causes; an organism that cannot hold (a reflex) or
cannot observe the resumption (a raw counter that relinquishes at a fixed failure count) cannot.

**The signal is not in any single observation bit.** It is the *contingent outcome of the
organism's own hold-and-observe intervention*, which is a fact about a past tick's action-outcome
pair. The estimate is the state that carries that fact across ticks. This is the precise sense in
which a *maintained* estimate is required rather than a per-tick reflex.

**What must still be verified in engineering (disclosed, not assumed).** The exact obs-bit-2 and
renewal-urgent trajectories over the window, the blind-failure streak behaviour under PORTS=4,
and the economic magnitudes (renewal cost vs re-bind cost vs income during the outage) are to be
measured on the frozen runner before any protocol — the AC15 economy rule: do not assume the
trade-off exists, measure the capability's payoff against its maintenance cost first.

---

## 7. The rivals (specified, each with its failure mode)

**R1 — reactive rival.** Action = f(obs(t)), a pure function of the current observation, no
memory. The natural form is "relinquish iff (failing) and (obs bit 2 == 0)" — read the corruption
bit to decide. **Predicted to fail** because no observation bit at the failure tick separates the
causes (§3): obs bit 2 is not elevated by either cause here, so the reactive rival has no
discriminating signal and collapses to a fixed policy.

**R2 — simple history-based rival (raw failure counter).** The frozen Gray-coded streak:
relinquish after STREAK_N = 6 consecutive unproductive contacts, with no cause attribution. This
is *already in the organism* (component C8). **Predicted to fail in E_machinery**: during the
read-outage the blind contacts fail consecutively (PORTS = 4 → blind success 1/4, so 6 consecutive
failures is reached with high probability within a W ≈ 20+ tick window), and the streak fires and
relinquishes a route that is in fact valid. Because re-binding is gated off post-development in
the frozen world (the deposit gate `grow = t < DEV`, AC16's finding), that relinquishment is a
**permanent, self-inflicted loss of a valid route** — an observable, economically costly error the
estimate does not make.

**R3 — state-blind rival.** A fixed duty cycle (relinquish/renew on a fixed schedule). **Predicted
to fail** by being wrong in at least one world (it cannot be simultaneously right to relinquish in
E_world and to hold in E_machinery).

**The rival that most threatens the task — stated, not hidden.** A raw counter *with a longer
threshold* ("relinquish after N' ≫ 6 failures") would also survive a short outage by not firing.
This is the sharpest version of the card's falsification risk. The estimate is distinguished from
"a bigger threshold" only if its E_machinery branch does something the counter's passive hold does
not: **active, cause-directed renewal spend** during the window (§5 consumption 2). The
discriminating measurement is therefore the *renewal-write timing and entry-life trajectory
during the outage window*, not merely the relinquishment count. If, in engineering, the estimate's
renewal behaviour turns out to be indistinguishable from the frozen renewal-urgent-triggered
renewal (i.e. the estimate adds nothing over the counter), **the task is not discriminating and
that result is reported and the question refined** — this document anticipates that outcome
rather than papering over it.

---

## 8. Discriminating predictions (the gates C2 will prespecify)

The claim is categorical, so the predictions are **per-individual dominance**, not a mean margin
(AC16/AC17's gate-shape lesson).

**P1 (E_machinery).** On every individual, in the E_machinery world, the candidate (with the
maintained estimate) **holds route-1** (fewer relinquishments than R2; renewal spend directed at
the entry through the window; route-1 still bound and productive at the horizon), while **R2
relinquishes route-1** during the outage and, with the deposit gate closed post-development, loses
it permanently. The candidate's post-outage income and survival dominate R2's.

**P2 (E_world).** On every individual, in the E_world world, the candidate **relinquishes the
stale route** (it does not hold a dead route), matching or exceeding R2's relinquishment, with no
survival harm (relinquishment is the correct response here; the estimate earns nothing extra in
E_world — the content only matters where the causes diverge, and this asymmetry is itself part of
the prediction).

**P3 (no-move / no-cut control).** With neither cause present, the candidate is byte-identical
(`state_hash`) to the frozen organism — the estimate is inert by construction, like the AC12
register. This is the single-change license: the estimate adds behaviour only where a cause is
present.

**P4 (falsification — scramble/cut).** Scrambling the estimate's bits, or cutting its maintenance
(leaving the host observation and the rest of the organism untouched), changes relinquishment
timing, route-holding, and/or survival in at least one world. If behaviour is **unchanged**, the
organism was relying on the host observation, not on its own maintained estimate, and the
mechanism does not exist as claimed (the R3 falsification, stated computationally).

---

## 9. Economy check (to be run before any protocol)

Per the AC15 rule carried in this repo's skill: before designing an allocation/relinquishment
study, measure whether the trade-off exists in the frozen economy. The C1 task must verify, in
engineering, that **both** responses remain *affordable* and *distinguishable* in the declared
world (AC11/12/13's shared wall — an intervention that zeroes the organism's income fixes the
outcome by starvation and erases the decision):

1. In E_world, both "hold the stale route" (wasted renewal spend) and "relinquish" (saved spend)
   must be affordable, so the decision is about the *value of the information*, not survival.
2. In E_machinery, both "hold through the outage" and "relinquish" must be affordable, so the
   estimate's hold is a real economic choice, not forced by starvation.
3. The window W and PORTS must be chosen so R2's streak actually fires during the outage (P1 is
   non-vacuous) while the entry survives holding (the estimate's hold is rewarded) — measured on
   engineering seeds, not assumed.

If (3) cannot be met for any W (the streak never fires, or holding never pays), the task's
discriminator is vacuous and must be re-designed — reported, not hidden.

---

## 10. Controls and confounds (handed to C2)

The estimate's causal role must later be separable from: resource cost (does the estimate just
spend more?), sensor damage (is the read cut affecting the estimate's own read?), motor
impairment (is the contact failing because the action isn't chosen, not because the read is cut?),
and memory capacity (does a bigger failure counter reproduce it?). Each is a distinct C2 control
arm; this document only fixes the task and predictions. The oracle/scaffold controls (a protected
copy of the estimate, or an externally supplied correct cause label) are to be labelled EXTERNAL
and never counted as autonomous.

---

## 11. Claim discipline and boundary

- This is a **level-(c) cognitive-representation** test (a maintained, flexibly-consumed state),
  a prerequisite the R3 roadmap names for the **level-(d)** HOT-2 "metacognitive monitoring"
  indicator. This document makes no level-(d) claim and no level-(e) claim. The strongest wording
  a positive result will ever earn is "meets candidate indicator HOT-2 at degree Y", and that
  grading is a later card, not this one.
- The distinction "meets a candidate indicator" vs "is conscious" is not crossed anywhere here.
- No autopoiesis claim. The estimate is a vulnerable maintained state (C1 existence); its
  production/replacement (C2) is not claimed and is not needed for this task.
- Seeds are the replication unit; the freeze, engineering-before-protocol, disjoint-seed-family,
  and hashed-source discipline all apply unchanged when this task is implemented (C2).

---

## 12. What this hands to C2

A concrete task (two causes, the read-cut primitive, the observation/action space, the estimate
and its two consumptions, the rivals, the four predictions), plus the separability requirement
(§10) and the three engineering measurements that must precede any protocol (§9). C2 implements
the runner as a new `acN.py` (never editing a frozen study), resolves the estimate's storage
offsets once at acquisition (the AC12 rule), and re-derives the frozen-world byte-identity before
freezing a protocol on disjoint final seeds.
