# Consciousness roadmap v1 — one active roadmap, one chosen mechanism

2026-09-22. Active roadmap / decision note. Not a frozen study: no experiment run, no
seeds, no protocol. It supersedes the two historical consciousness documents and is now
the single active consciousness-related roadmap. It fixes the vocabulary, removes two
false stops, and names one mechanism to build. The actual task design is C1's job; this
document only makes the roadmap concrete and hands a falsifiable mechanism over.

## 1. Supersession — what is replaced, what is preserved

This roadmap **supersedes**:

- `CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md` (the goal-§7 scheduling archive, which gated
  consciousness work on content self-production);
- `CONSCIOUSNESS_MECHANISM_SPEC_v1.md` (the "no concrete mechanism is currently
  testable" closure).

Both are **preserved unchanged** as the historical record of how the track reached its
current position. They are no longer active: future workers read this roadmap, not
either of them, for what to build next. The correct reading of those two documents from
now on is "superseded by `CONSCIOUSNESS_ROADMAP_v1.md`".

## 2. What this roadmap removes, and why

**2.1 The content self-production gate (AC78) is removed as a prerequisite.** The
blocks disposition archived the consciousness task because its `ao-content-self-production`
gate failed. That gating is a project *scheduling* decision, not evidence that a
consciousness-relevant mechanism requires successful priority learning
(`AC79_ERRATA_v1.md` §5). Autopoiesis is not an established prerequisite in the
indicator-based framework (Butlin et al. 2023), and the definitions charter makes the
same point at the definition level: content self-production is an *additional research
ambition*, explicitly **not required** even for the autopoiesis claim itself
(`DEFINITIONS_CHARTER_v1.md` §6, §10). A theory-specific consciousness investigation may
proceed on the mechanism it needs without waiting for the AC78 fixed point to be broken.

**2.2 The "no single experiment can establish consciousness, therefore unwarranted" stop
is removed.** The mechanism spec's §3 closed by observing that a positive result is
capped at "meets a candidate indicator" and therefore not worth building. That
observation is correct about the *wording* ceiling; it is wrong as a *stop*. The
level-(d)/(e) boundary is a claim discipline ("meets candidate indicator X at degree Y",
never "conscious"), not a reason to avoid the experiment. A bounded, theory-specific
claim is the only honest progress the discipline permits on the subjectivity track; the
correct response to "this cannot establish consciousness" is to **do it anyway and say
exactly what it does establish**, not to decline to run it. The framework's own authors
deny the inference from indicator satisfaction to phenomenal consciousness — which means
the inference is forbidden, not that the indicator is worthless.

## 3. What this roadmap retains and does NOT relabel

The AC67/71 finding stands, unchanged: **the self-monitoring loop is homeostatic
infrastructure, not a consciousness indicator.**

The loop is a repair reflex, read from frozen code: `ac9.observe` recomputes observation
bit 2 each tick as a host-side scalar over the program bank's minority-replica count, and
the frozen bank-0 rule answers that single threshold bit with one paid repair action.
It is (i) external scaffolding — the organism neither stores nor maintains nor produces
the monitoring state, it reads it; (ii) not a representation — one bit driving one fixed
action, with no content flexibly consumed; (iii) not acquired — the bit→action mapping is
a frozen rule word. No theory in Butlin et al. lists "pays to repair its own corruption"
as an indicator. This is a watchdog timer, the kind of sub-conscious infrastructure every
theory treats as outside the framework.

**This roadmap does not relabel that reflex.** It does not call the loop a
consciousness indicator, and it does not build its chosen mechanism on top of the loop.
The chosen mechanism (§4) differs from the reflex on exactly the properties the reflex
lacks — stored, maintained, flexibly consumed — which is what makes it a candidate
indicator rather than infrastructure.

## 4. The single chosen mechanism

**Name:** an *internally maintained cause-attribution estimate* — a vulnerable,
paid-maintained second-order state about why a first-order representation is failing.

**First-order representation (what the estimate is about).** The route memory entry —
the acquired key→port binding in `mem.Memory`, bound from productive contact outcomes,
stored in damageable state, maintained by paid renewal (charter component C7). This is
the organism's only content-bearing state: it is interoceptive/route-level, not
perceptual, but it *is* content — acquired within life, damageable, maintained, and its
content selects the organism's contact actions. This roadmap **adopts the position that
interoceptive route-level content is representational** (charter contested judgment J5,
decided in the affirmative here rather than assumed away; see §5). It is *not* assumed
that a simple, inherited, or interoceptive state cannot represent anything.

**The estimate.** A new vulnerable, paid-maintained register (the AC12 dead-rule
free-bit pattern, or a maintained word in the recipe bank) holding a low-bit-width value
e ∈ {E_world, E_machinery}: the estimate that a route-contact failure is caused either by
*environmental change* (the channel moved; the stored route content is now obsolete) or
by *impaired access machinery* (the stored route is still correct; the read/repair path is
degraded). Two causes, one identical immediate failure.

**Update rule (from the organism's own observations only).** e is updated within the
lifetime from signals the organism already receives — the contact-outcome sequence, the
corruption observation (obs bit 2), and renewal/repair outcomes — by a rule that the
organism's own paid machinery executes. **No externally supplied diagnosis.** The
organism receives observations, not the correct answer; the correctness of the estimate
is a property of its update rule against those observations, and the rule is the thing
under test.

**Flexible consumption (the content is used in at least two behaviourally distinct
ways).** The same estimate selects between two policies that allocate resources
differently:

1. If e = E_world → **relinquish**: erase the stale entry and re-bind (the
   AC75 erase-on-relinquish path), freeing the organism to re-acquire the moved route.
2. If e = E_machinery → **maintain**: withhold relinquishment and direct spend to
   repair/renewal, because the route content is still valid and the failure is in the
   access path, not the content.

These two policies are observably different (rebind attempts vs repair/renewal spend) and
economically different (relinquishment spend vs maintenance spend). A one-bit threshold
that always drives one fixed action would fail this requirement; the estimate is defined
by its *two* downstream uses.

**Falsification (stated in computational terms).** The mechanism is falsified if, in a
task where both causes occur, **scrambling or cutting the maintenance of the estimate —
while leaving the host observation and the rest of the organism untouched — leaves
behaviour unchanged** (relinquishment timing, survival, route-holding). Unchanged
behaviour means the organism was relying on the host observation, not on its own
maintained estimate, and the mechanism does not exist as claimed. The estimate must also
produce behaviour that a **state-blind fixed-policy rival** (a fixed duty cycle) and a
**simple history-based rival** (a raw failure counter with no cause attribution) cannot
reproduce; if either rival reproduces it, the estimate carries no content and the
roadmap's mechanism is falsified. These rival requirements are handed to C1 unchanged.

## 5. Theory mapping

**Primary mapping: HOT-2 — metacognitive monitoring** (Butlin et al. 2023, Table 1:
"metacognitive monitoring distinguishing reliable perceptual representations from
noise"). The estimate is a second-order state about the reliability of a first-order
representation: E_world is the judgement "this representation is now noise (obsolete)",
E_machinery is "this representation is reliable but my access to it is degraded".
Distinguishing those two, from observations alone, *is* the metacognitive-monitoring
function — a monitor that grades the reliability of the organism's own content rather
than the content itself.

**Adaptation, flagged not hidden.** HOT-2's canonical domain is *perceptual*
representations, and the organism has no perceptual content. The mapping therefore
extends HOT-2's monitor to the organism's only available content — interoceptive,
route-level. This is a **theory-specific adaptation**, exactly the move §4 makes on
charter J5 ("can a host-computed-observation system represent anything"), and it is a
**modeling judgment, not a settled finding**. The roadmap adopts it as its stated
position and records that a reviewer may contest it; if contested, the verdict falls to
"unresolved" on this point rather than silently assuming interoceptive content is
representational. What is *not* at stake is whether the mechanism is worth building: the
falsification in §4 is testable either way.

**Adjacency, not the mapping.** The estimate is also adjacent to PP-1 (predictive
coding): it is updated from signals that function as prediction errors (expected contact
success vs observed failure). But PP-1's canonical content is input-module predictive
coding over perceptual content, and the *source-attribution* structure of the estimate
(world vs my-own-machinery) is metacognitive, not predictive. HOT-2 is the primary
mapping; PP-1 is recorded as a secondary adjacency the same mechanism touches, not the
theory the roadmap claims.

## 6. The four layers, separated

**6.1 Prerequisites (what must hold before the mechanism can be built — and none of
these is content self-production).**

- The route memory (C7) is a maintained, damageable, paid-maintained representation —
  already true in the AC105 body.
- There is a place to store a new vulnerable register — the AC12 dead-rule free-bit
  pattern already exists and is proven inert.
- The two causes (world-moved vs machinery-impaired) are **distinguishable from the
  organism's own action-observation histories** — this is the C1 distinguishability
  argument, and it is a prerequisite to demonstrate *before* building, not assumed.

**6.2 Functional evidence already in hand (levels b and c).** Route memory acquired and
flexibly consumed (relinquish vs restore, AC15/AC18/AC75); the decision register
(relinquishment streak); the paid maintenance of every component. This is the substrate
the estimate builds on, and it is *organismal-autonomy and cognitive-representation*
evidence — it does **not** by itself say anything about consciousness.

**6.3 Theory-specific relevance (level d).** The estimate, if it behaves as §4 requires,
satisfies a *candidate* HOT-2 indicator at a *degree* to be graded. The strongest wording
this earns is "meets candidate indicator HOT-2 at degree Y". Nothing stronger.

**6.4 Unsupported subjectivity claims (level e).** Out of scope, never claimed, not
assessed. The estimate is not evidence of phenomenal consciousness; satisfying an
indicator raises probability and is bounded by the level-(d)/(e) boundary. This roadmap
does not and will not cross it.

## 7. What this hands to C1 (and C2)

C1 designs the discriminating task and its predictions. It receives from here: (1) the
chosen mechanism and its two-cause structure (§4); (2) the requirement that the organism
receive observations, not a diagnosis; (3) the requirement of ≥2 distinct ways the
estimate's content affects behaviour; (4) the rivals that must fail — a state-blind fixed
policy and a simple history-based rival; (5) the falsification — scrambling the estimate
must change behaviour. C2 receives the separability requirement: the estimate's causal
role must be distinguished from resource costs, sensor damage, motor impairment, and
memory capacity.

## 8. Falsification of this roadmap

This roadmap fails — and must be rewritten — if its chosen mechanism cannot be stated in
falsifiable, computational terms for this organism. It **can**: §4 states the estimate,
its update rule, its two distinct consumptions, and the exact measurement (scramble the
estimate, observe behaviour) that would falsify it. If C1 finds a simple rival reproduces
the behaviour, the mechanism is falsified at the task level and the roadmap is refined,
not concealed — that outcome is anticipated by C1's own falsification rule.

## 9. Controls, confounds, and limits

The distinction "meets a candidate indicator" vs "is conscious" is absolute and is not
crossed anywhere in this document. Indicator satisfaction is **never** treated as proof
of subjective experience. The estimate's causal role must be separated from the confounds
listed in §7 before any claim is made. The mapping in §5 is a flagged modeling judgment.
The ceiling of a positive result is a bounded, theory-specific claim, and that ceiling is
a discipline constraint, not a reason to stop.

## 10. Status after the K-series (2026-09-23) — the mechanism was built, tested, and NOT falsified

The chosen mechanism (§4) has now been built and frozen, and the roadmap's own falsification test
(§4/§8 — scramble/cut the estimate, observe behaviour) was **not reached**:

- **Discrimination tier — PASSED (K6, `AC107_RESULTS_v1.md`, finals 6000–6007).** The maintained
  cause-estimate discriminates the two causes at decision times with 0 mistakes across 32
  individuals, and the discrimination depends on the maintained storage's content
  (observer-discard 16/16 + no-cause identity 16/16). The K1 confound that had produced the AC106
  "carries no cause information" negative was an implementation defect (the update rule dropped the
  organism's own `bound` flag), now closed.
- **Coupling tier — PASSED (K7, `AC108_RESULTS_v1.md`, finals 6100–6107, 7/7 gates).** Both
  directions hold by selective single-flag interventions: maintenance → accuracy (16/16) and use
  (behavioural), and representation content → adaptation and production/viability (16/16 in the move
  direction). This is the roadmap's §4 "flexible consumption" and "causal role" requirement, met.
- **Reliability tier — BLOCKED, not falsified (K8, `K8_DISPOSITION_v1.md`).** The estimate is
  ceiling-accurate (0 mistakes), so there is no error variance for a second-order reliability state
  to predict. The HOT-2 metacognitive-monitoring tier remains open at the reliability level; its
  reopening conditions (relax identifiability / degrade the observation interface / add a third
  cause) are on record and are the mirror of the earlier C3 wall.

What this does **not** change: the survival *advantage* of the estimate is seed-bounded (K6 Q4), and
its causal role in the cut is behavioural rather than survival-level; the mapping in §5 remains a
flagged modeling judgment; the level-(d)/(e) boundary is untouched. The roadmap is **not** superseded
and **not** fulfilled to the reliability tier — it has advanced two of its three tiers and parked at
the third. The next step on this track is gated by `K9_SYNTHESIS_v1.md`: do not re-open K8 until a
mechanism change introduces a non-zero, non-trivial error rate.
