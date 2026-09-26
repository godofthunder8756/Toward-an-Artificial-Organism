# ACI research constitution v1 — the ten questions every future card must answer

2026-09-25. Deliverable for the Q11 card (t_b93a8fef): *what document governs
future research-agent behavior so every future card is tied to the ACI goal?*
Category F — **governance; do not execute.**

This is the **terminal governance document** of the Q-series. It runs nothing,
trains nothing, freezes nothing, and edits no frozen artifact (runner, protocol,
results dir, hash, or ledger). It is not hashed into any study's
`pre_run_snapshot.json`. It governs *behavior*: which cards may enter active
research, and what each of them must establish before it does.

It binds every future research-agent session that touches this board. The
questions below are not optional metadata; an answer to each of the ten is the
**admission requirement** for any experiment card (engineering, frozen, or
review). A card that cannot answer all ten does not enter active research.

---

## 0. The one-paragraph answer

A single document — this one — governs every future card. It does so by making
**the ACO goal the only admissible destination** and by requiring each card to
locate itself against it through **ten questions**, each of which has a known
correct *shape* of answer and a known failure mode. The ten questions are the
gate. Behind them stand three standing rules that make the gate binding rather
than ritual: (1) the **claim ceiling** — no card's claim may cross the level-(d)/(e)
boundary, and the strongest wording any realized phase earns is "meets the ACO
definition (N1–N5, at the stated degree)"; (2) the **rival discipline** — a claim
is credited only if the strongest simpler mechanism that omits it provably fails,
with that rival's parameter family swept alongside the learner's; (3) the
**collapse record** — any mechanism that reduces to a simpler policy has failed,
regardless of how elaborate the implementation looks. A card that cannot name the
ACO property it tests, the hypothesis it tests against, and the result that would
kill that hypothesis is not a research card; it is a hope, and it is returned.

---

## 1. What this constitution governs and where it sits

The constitution is the terminal card of the strategic F-series (Q0–Q11). It
does not re-derive anything the earlier cards fixed. It **reads**:

- `ACI_TARGET_CONSTRUCT_v1.md` (Q1) — the ACO: five necessary properties N1–N5,
  four optional O1–O4, exclusions X1–X6, interventions I1–I5, failure table F1–F5,
  and the central hypothesis ("recurrent cognitive organization of the form
  N1–N5 … is the smallest organization a neural architecture must realize before a
  theory-specific consciousness question is well-posed").
- `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2) — principles P1–P7 and demotions D1–D8.
- `ACI_MASTER_RESEARCH_TREE_v1.md` (Q10) — the seven phases (I–VII), the dependency
  DAG, the per-phase hypothesis / decisive experiment / rival / falsification /
  compute / claim-ceiling fields, and the card decomposition each phase implies.
- `DEFINITIONS_CHARTER_v1.md` — the five claim levels (a)–(e), and the absolute
  (d)/(e) boundary.

The constitution's **jurisdiction** is every card created on the ACI board from
now on: run cards, protocol-freeze cards, engineering-screen cards, audit and
replay cards, and review cards. It is enforced by the agent that writes the card
and by the reviewer that admits it — not by an external process.

---

## 2. The claim ceiling, stated once and for every card

The ACO is a **specification**, not a consciousness result. No card in the
program — from a single engineering seed to the terminal Phase VII conjunction —
may claim, or be written so that a reader could infer:

- **consciousness, phenomenal experience, "an artificial conscious being", or any
  subjective-experience claim** (level (e)); the level-(d)/(e) boundary is
  absolute;
- **autopoiesis unqualified** or **"alive"** for the organism line (level (a));
- **"wants", "needs", "has a self", "is self-aware"** for any decision state
  (levels (b)–(d)).

The strongest wording the whole program can ever earn is:

> **meets the ACO definition (N1–N5, at the stated degree)** — and, for a
> theory-specific piece, **meets candidate indicator X at degree Y**.

Every card states its own ceiling in its claim field, and the ceiling must be
narrower than this program ceiling. A card whose claim field cannot be stated
without touching the forbidden wording is out of scope for this board (it belongs
to philosophy, not to a falsifiable experiment).

---

## 3. The ten questions — the gate

Every future experiment card must answer all ten. Each question is stated with
(i) what it is asking, (ii) the *shape* of an admissible answer, and (iii) the
failure mode that voids the card. The ten are the operative content of this
constitution; §4–§6 are the standing rules that make the answers binding.

**Q1. What ultimate ACI question does this address?**

The card names the terminal goal this work advances. The ultimate question is the
central hypothesis of `ACI_TARGET_CONSTRUCT_v1.md` §9: does a recurrent cognitive
organization of the form N1–N5 exist that a neural architecture can realize, and
is that organization what must be built before any theory-specific
consciousness-relevant question is well-posed? A card locates itself against this
by naming which ACO property (N1–N5) or optional property (O1–O4) it moves.

*Admissible:* names a specific property (e.g. "tests N1, active persistence").
*Void if:* the answer is "consciousness", "general intelligence", or any goal
outside the ACO vocabulary.

**Q2. Which architectural hypothesis does it test?**

One bounded, falsifiable claim, stated in the ACO property vocabulary. Exactly
one hypothesis per card; anything else measured is reported, not claimed.

*Admissible:* "a recurrent agent acquires an endogenous maintenance allocation
that is required for later performance, load-bearing beyond every state-blind
schedule, and a function of its own resource state" (the bridge's H).
*Void if:* the hypothesis is a list, a slogan, or unfalsifiable.

**Q3. What result would falsify the hypothesis?**

A concrete, observable signature, prespecified and pinned before any result is
seen. Drawn from the named failure tables (the bridge's F1–F7, the construct's
F1–F5, the benchmark's per-task falsification) or stated new in the same shape.

*Admissible:* "a fixed duty-cycle level matches/beats the candidate on the
decision endpoint" (AC11's signature).
*Void if:* no result is named that would change the program's mind; a card that
cannot lose is not a test.

**Q4. What is the strongest simpler explanation?**

The candidate's own mechanism with the contested piece removed — never a
strawman, never an unrelated weaker system. Its parameter family is swept
alongside the learner's, and the claim is credited only if this rival provably
fails.

*Admissible:* the state-blind fixed schedule, the reactive/memoryless reflex, the
sufficient-statistic rival, the finite-state/direct-control rival, the
reward-only rival.
*Void if:* the rival is weaker than the candidate for reasons unrelated to the
contested piece, or the rival's parameters are not swept.

**Q5. What existing evidence makes this experiment necessary?**

The card cites the frozen record that motivates it — a positive result it
extends, a negative it resolves, or a composition it assembles — from the
Q-series documents or the frozen organism studies. "Necessary" means: the answer
is not already implicit, and would not be settled by re-running what exists.

*Admissible:* "Phase II is the first neural realization of the paid-maintenance
principle (P1/P2) the organism line repeatedly established."
*Void if:* the necessity is asserted against a result already recorded (the
mission audit's §2.3 "pursued too far" cases are the cautionary examples), or no
prior artifact is cited.

**Q6. What would we do differently if it succeeds?**

The concrete downstream consequence, named in the vocabulary of the tree: which
phase, gate, or design decision the positive result releases or changes. A
result with no downstream consequence is not a result.

**Q7. What would we do differently if it fails?**

The concrete negative consequence: which phase is blocked, which principle is
demoted, which rival is promoted. Both Q6 and Q7 are required; a card that only
anticipates success is not doing science.

**Q8. Does this need an organism simulation, a neural model, an analytic proof,
or no experiment at all?**

The card states the minimum apparatus the question requires, and refuses the
rest. The organism line is exited (Q7); a neural-phase card runs the minimal
architecture, a design-only card is a document, and a question that is already
settled analytically (e.g. the graded-posterior-is-an-integer-counter result,
R2) needs no simulation at all.

*Void if:* the apparatus is chosen for continuity or ambition rather than by what
the hypothesis requires; or a frozen organism study is proposed to answer a
neural question.

**Q9. Are we testing a consciousness-relevant mechanism, or merely improving
robustness?**

The card states which, honestly. Robustness work (a repair that does not change
which property is realized; a faster or cheaper encoding of an established
state) is legitimate but is **labelled** as such and is not credited as an ACO
property. The mission audit's §2.3 records where robustness re-tests were
mistaken for new ceilings; a card must not re-commit that.

**Q10. What is the claim ceiling?**

The strongest wording this card's result may earn, stated negatively and
narrower than the program ceiling of §2. This field is as load-bearing as the
hypothesis.

*Admissible:* "earns at most 'meets ACO property N1 and N3(a)(b)(c) at the stated
degree'; no N4, no O1, no consciousness claim."
*Void if:* the ceiling is omitted, or stated so loosely that a positive result
could be read as a consciousness claim.

**The admission rule.** All ten must be answered, each in its admissible shape.
If they cannot be answered, the card **does not enter active research** — it is
returned to its author (or to the parent that spawned it) with the missing or
voided question named, and no dispatcher, no engineering seed, no frozen
protocol is created for it. A card is not a research card by virtue of being on
the board; it is a research card by virtue of answering these ten.

---

## 4. Standing rule I — the rival discipline (P6)

A positive claim is credited only against a rival that provably fails. Concretely,
every experiment card must:

1. implement the strongest simpler mechanism that omits the contested piece, as
   the candidate's own mechanism with one piece removed (not a strawman);
2. sweep the rival's parameter family and the learner's own parameters together —
   if any state-blind fixed policy matches or beats the learner's best
   configuration, no acquired mechanism has been demonstrated (AC11);
3. label oracle/scaffold/protected-copy arms EXTERNAL and never count them as
   autonomous results;
4. match the gate shape to the claim shape — categorical claims gate on dominance
   or separation-of-minima, never a mean margin; check satisfiability against the
   score bounds before freezing (AC16/AC17).

---

## 5. Standing rule II — the collapse record is the standing falsification set

A mechanism that *looks* cognitively interesting but reduces to a simpler policy
has **failed** — however elaborate the implementation. The recorded collapses
(`ACI_MISSION_AUDIT_v1.md` §2.6) are the standing falsification set; a card whose
mechanism reproduces one of them must name the collapse it risks and the contrast
that would distinguish it:

- the self-repair loop → a watchdog timer (AC67/AC71);
- the graded posterior → an integer counter (C4/R2);
- the weighted two-counter → no advantage over one (AC113);
- maintained storage → weakly dominant only (AC116);
- the "monitor" → a directional-repair controller, control-yes/prediction-no
  (AC117);
- the adaptive allocation arm → beaten by a state-blind duty cycle (AC11);
- the self-directed learner → blocked by a locked, path-dependent fixed point
  (AC78).

The anti-checkmark rule follows: a card's deliverable is a **discrimination**,
not a per-family tally of satisfied indicators. Adding a mechanism that fails its
contrast is not progress; it is a recorded collapse, and it should be recorded
rather than re-architected.

---

## 6. Standing rule III — inherited discipline (P7, byte-identity, seeds)

Three methodological invariants bind every card, carried from the organism line:

1. **Byte-identity is the composition license.** Prove a change inert
   (`state_hash` equality) at the intact boundary before attributing any
   difference to it. Composition is never licensed by prose.
2. **Seeds are the replication unit; survival is a bimodality-aware lower bound.**
   N seeds × 2 histories = N independent units. Engineering and final seed
   families are disjoint; a body-survival claim needs the long horizon and no
   upper bound on survivors (AC39/AC68).
3. **Frozen-version discipline.** Any changed experiment gets a new versioned
   protocol and a new results dir; an old freeze, hash, ledger, or result is
   never edited to make something pass; gates are prespecified and never moved
   after a result (AC16).

---

## 7. Amendment and precedence

This document is v1. It may be amended only by a future governance card that
(a) states which rule it changes, (b) states the recorded failure that motivates
the change, and (c) does not relax the claim ceiling of §2 or the admission rule
of §3 — those two are the constitution's non-negotiable content and cannot be
amended except by a successor document that says, explicitly, that it supersedes
this one.

Where a later document conflicts with this one on a specific card, this
constitution governs unless the later document is itself a governance document
amending it under §7. On a conflict between a card and this constitution, the
constitution wins; the card is reworked or returned.

---

## 8. What this hands the board

- The **ten-question admission gate** (§3) — the operative rule every future card
  obeys.
- The **claim ceiling** (§2) — the wording no card may cross.
- Three **standing rules** (§4–§6) — rival discipline, the collapse record, and
  the inherited methodology — that make "tied to the ACI goal" mean something
  checkable rather than aspirational.
- A **precedence clause** (§7) that keeps the gate itself stable while the
  program evolves.

The next cards after this one are the first *executable* neural cards of
Phase II (the bridge engineering screen, then the frozen realization) — the first
cards that must pass this gate. Everything downstream inherits it.

---

## Sources

Read, not re-derived or edited: `ACI_TARGET_CONSTRUCT_v1.md` (Q1; N1–N5, O1–O4,
X1–X6, I1–I5, F1–F5, central hypothesis §9), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md`
(Q2; P1–P7, D1–D8), `ACI_MASTER_RESEARCH_TREE_v1.md` (Q10; seven phases, DAG,
per-phase fields, card decomposition, §10 cross-cutting discipline),
`DEFINITIONS_CHARTER_v1.md` (claim levels (a)–(e), the absolute (d)/(e)
boundary), `ACI_MISSION_AUDIT_v1.md` (Q0; collapse record §2.6, negative ledger
§3, "pursued too far" §2.3), `ACI_ORGANISM_EXIT_CRITERIA_v1.md` (Q7),
`ACI_BRIDGE_PROTOCOL_v2.md` (Q8/Q9; arms, gates G3a–G3d, failure table F1–F7).
Frozen study references read from the skill's `references/` dir where named
(`ac11`, `ac16`, `ac17`, `ac113`, `ac116`, `m6-harness-result.md`). This document
is derived and is not hashed into any study's `pre_run_snapshot.json`.
