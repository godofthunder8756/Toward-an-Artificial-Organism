# S0 synthesis v1 — what the arc established, and the single strongest next question

2026-09-24. Terminal synthesis for the S0 card (`t_4ab7a944`). It reads the five
predecessor deliverables — P3 (`P3_CORRECTIONS_v1.md`), P6 (`AC113_RESULTS_v1.md`),
P7 (`P7_FEASIBILITY_v1.md`), A0 (`A0_SUCCESSOR_SPEC_v1.md`), W0/P1
(`P1_MANUSCRIPT_DRAFT_v1.md`) — together with the P-series record
(`C4_P2_EQUIVALENCE_v1.md` = P2, `P4_COGNITION_CONTINUATION_v1.md` = P4),
`S1_SYNTHESIS_v2.md`, `EVIDENCE_INDEX_v3.md`, `AUTONOMY_RESEARCH_STATUS.md`, and
`CONSCIOUSNESS_ROADMAP_v1.md`. It runs nothing, re-hashes nothing, freezes nothing,
and edits no frozen artifact. It reports the eight required items and chooses one
next research question with its cost and falsification risk. It is derived and is not
hashed into any study's `pre_run_snapshot.json`.

Architecture baseline declared by the card is `add3bb5` + all P/A/W outputs; the
working tree HEAD at writing is `e3fae26` (the P2 commit), with the P/A/W
deliverables present as working-tree additions/modifications.

---

## Verdict (one paragraph)

Two tracks, one reconciled and now *measured* account. The **autonomy** track is
stable within the current model: production closure (M&V clause i) is SUPPORTED
bounded, and the full two-clause criterion is NOT ESTABLISHED for a reason that is a
modeling limitation, not an empirical gap — with exactly **one** finite successor
requirement (SR-1, boundary-mediated exchange) that can move the clause-(ii) verdict,
and only by a re-architecture, not an in-model run. The **cognition** track is
characterized and now twice-bounded on first-order uncertainty: the graded posterior is
an integer counter (P2, exact), and the heterogeneous-weighting generalization is
equivalence at organism scale (AC113 F1) — a maintained integer counter suffices, and
the load-bearing objects are decisive-observation handling plus a counter threshold,
not a graded register. History, uncertainty, acquisition, and repair were all
distinguished successfully. Three paper-ready claims stand. The single strongest next
question is **SR-1** (does the produced boundary mediate the organism–environment
exchange), because it is the only open question that moves the program's central
verdict; the cognition track's reliability tier is the named next-after, gated on a
cheap harness probe. Neither breakthrough nor exhaustion is claimed.

---

## 1. What the posterior audit established (P2 equivalence / disagreement)

P2 (`C4_P2_EQUIVALENCE_v1.md`) resolved the C4 sufficient-statistic rival by
**analytic equivalence plus executable verification**, and found a **rival defect**,
not a property of gradedness, behind the prior dominance:

- **Equivalence (outcome a).** Under C4's stationary two-cause model the graded
  log-odds posterior is computationally equivalent to an integer ambiguous-failure
  counter with matched decisive-observation handling, aligned by
  `N = ceil(logit θ / log(4/3))`. Every ambiguous (occluded-unproductive) contact
  contributes the same `LR = log(4/3)`, so the float log-odds is a scaled, translated
  copy of the count. Exact equality was verified over the full 6-symbol alphabet for
  horizons 1–7 (279,936 histories at H=7) and 200,000 random length-96 histories —
  identical act-tick on every admissible history, not within-MC-noise.
- **The disagreement (a C4 §10 claim is false).** C4's "no uniform counter can express
  that split" is false for this construction: the split is
  decisive-observations-act-immediately vs weak-observations-accumulate-slowly, and an
  integer counter expresses exactly that split once the three decisive observations are
  handled the same way.
- **The reported dominance was a rival defect (outcome c, identified).** `binary+imm`
  reset its streak on an occluded-**productive** contact instead of treating it as
  decisive-C. Fixing that one observation makes it bit-for-bit the integer counter,
  hence bit-for-bit the graded policy, and the dominance vanishes (`graded == int ==
  binary+imm(full)` to 1e-12 at their optima). The load-bearing objects are (i)
  decisive-observation handling and (ii) a counter threshold — **not** a graded
  register.
- **Calibration survives** — it is a claim about confidence tracking error frequency,
  not about dominance, and is untouched.

P4 (`P4_COGNITION_CONTINUATION_v1.md`) then generalized to the one change that breaks
the equivalence premise: **heterogeneous** likelihood ratios (relax "M never yields" to
a residual yield ε). The sufficient statistic becomes a two-dimensional weighted count
`(n_u, n_p)`; a graded register is an exact re-encoding of the integer pair (verified
46,656 histories × 10 thresholds, zero mismatches). The load-bearing object is
**heterogeneous weighting, not gradedness**.

AC113 (P6, `AC113_RESULTS_v1.md`) carried that to organism scale and **falsified it as
equivalence (F1)**: at q=0.9 the maintained two-counter does not beat the strongest
single-counter on post-cause income in either regime (ε=0.08: mean −2336, sign-flip
p=0.375; ε=0.02: mean −2344, p=0.305; 16 paired finals 6400–6407). The P4
decision-theoretic regret gap (+0.03…+0.32) does **not** transfer, for two measured
reasons: contact quantization makes the integer weight match the non-integer ratio, and
"false-relinquish costs R=4" is false at organism scale (holding has entry-expiry cost;
a false relinquish refreshes the entry). The P2 conclusion — a maintained integer
counter suffices — **survives the heterogeneous likelihood ratio at organism scale**.

## 2. What the organism experiment established or falsified

**AC113 (P6) established:** the maintained estimate's content is **informative and
causally effective** but **not useful as a graded/weighted magnitude**. V1 clean
control passes (64/64); V2 passes (the accumulator's read content drives a
false-relinquishment under cut in 4/16 where the read-forced scramble holds 0/16);
V3 observer-discard passes (16/16 per-tick byte-identity). The comparison gate G-COMPARE
returns **F1** — equivalence, recorded, not moved. Two engineering-selected-aggressive
thresholds (θ*=0.5) collapse on 2/16 finals (route loss → death under cut): AC39's
engineering-vs-finals transfer failure in the unfavourable direction, and the finals'
own optima still tie.

**Falsified:** the hypothesis that heterogeneous (two-dimensional, non-integer)
weighting is load-bearing at the organism scale. Also falsified (by AC113's two death
tails and by AC107 Q4/AC108 12/16): any survival advantage for the estimate — survival
is seed-bounded throughout.

**Established by the wider arc (carried, not re-litigated):** a maintained one-bit
cause-estimate discriminates two causes at ceiling accuracy (0/32 mistakes, AC107) and
is causally coupled to its maintenance in both directions, each isolated by single-flag
intervention (AC108); its storage is inert in the clean task while its content is
load-bearing (AC109); repair is not load-bearing for correctness/use in the decision
window but is load-bearing for post-window storage (AC110 G4); the direct composition
channels are clean (AC111).

## 3. Were history, uncertainty, acquisition, and repair distinguished successfully?

**Yes — all four, cleanly, each with its qualifier attached.**

- **Useful history — distinguished.** In the clean task, persistent history contributes
  nothing: a direct diagnostic reading the same `(bound, used_held, productive)` triple
  transiently matches the stored estimate on 48/48 behavioural endpoints at lower cost
  (AC109, engineering). A task where history *is* load-bearing exists by design: the C2
  occluded-`used_held` gate makes the two causes produce an identical current
  observation while their histories differ (identifiability demonstrated, not assumed).
  So "history is useful" is task-conditional and the condition is named.
- **Uncertainty — distinguished, and resolved to a wall.** First-order uncertainty is a
  counter: graded ≡ integer counter (P2, exact), heterogeneous weighting ≡ single
  counter at organism scale (AC113 F1). The second-order (reliability) tier — the
  evidence channel's own diagnostic value ε/`P_YIELD` — is a distinct object about the
  estimator's inputs, deferred on the AC113 per-action-economics wall (P7), not conflated
  into the first-order result.
- **Acquisition — distinguished.** The load-bearing maintenance is the **paid
  acquisition/update write** (`bel_write`, one atomic 7-replica flip at cause-onset),
  established in both directions by AC108. This is *not* ongoing repair.
- **Repair — distinguished.** Repair is not load-bearing for correctness/use in the
  96-tick decision window (correctness rides reacquisition, AC110 G2/G3) but *is*
  load-bearing for post-window storage protection (AC110 G4: maintained 16/16 vs
  no_repair 8/16). The distinction is conditional on the frozen ambient 1e-4 damage
  rate and the window length; it is not "repair is falsified" in general.

## 4. What composes in the current architecture

- **The autonomy body composes (AC105, 6/6 gates):** Gray-coded relinquishment streak
  (AC99/100) + persistent reconstruction trigger (AC103) + allowance-42 budget
  (AC104/105), all under corruption across a predeclared grid of timings, priorities,
  and repeated moves.
- **The internal-state milestone composes (AC86–89):** description, derived program,
  pointer, coordination state, and decision state are each maintained, reconstructed,
  and succeeded, with the succession controller's working state itself in the
  maintained substrate and a real verify gate (AC87/88/89).
- **The cognitive mechanism composes on its direct channels (AC111/P7):** the estimate
  bit is excluded from `reg_from_active` (verified under a live reconstruction), and the
  allowance-42 budget never starves reacquisition (`bel_write`/`counter_write` are
  W-gated, not allowance-gated). G2/G4/G6 pass. **Full composition is NOT established:**
  the corrupted contact rule re-schedules reacquisition, producing a seed-dependent,
  survival-neutral behavioural interference (G3/G5 12/16, finals 6306/6307).
- **The counter bits compose** with corruption + reconstruction via the AC96 streak
  free-bits (`exclude_offs = reg_offs + streak_offs + [bel_off]`); the one unexercised
  detail (counter bits under a *live* reconstruction, AC113 ran `corrupt=False`) is a
  unit-level assertion, not a study (P7).

## 5. The bounded autopoiesis verdict and concrete successor requirements

**Verdict.** Clause (i) **production closure — SUPPORTED, bounded** (K3): components
{W, C, B, description, derived program} meet C1–C5 and maintained state {pointer,
coordination, route memory, decision state} meets S1–S4, one strongly-connected
production-dependency network with no external root, under the accepted substrate
convention (J1 = substrate, resolved). Clause (ii) **spatial unity — NOT ESTABLISHED**:
met only at the constituent-retention level (the produced boundary retains W/C inside a
bounded interior), limited by three modeling declarations, none an empirical gap: (a)
supplied space/geometry, (b) supplied non-boundary-mediated exchange interface, (c)
non-spatial controller. Not "autopoietic" unqualified, not "alive."

**Concrete successor requirement — exactly one (SR-1, from A0).** Make the produced
boundary the site of the organism–environment exchange: re-specify `react` actions 0/1
so intake `in_m`/`in_f` is conditioned on the produced boundary's state (an aggregate
integrity gate, e.g. `(b.boundary > 0).sum() >= B_MIN`), rather than on a fixed
constant. Three properties make it minimal: it changes a supplied reaction's
*dependence* (no new mechanism/component/state); it is expressible inside the frozen
balance identities (`in_m`/`in_f` are variables, so gating satisfies the identity by
construction — the AC15 lesson); and it is non-spatial. Four prespecified causal tests
gates it: T1 retention continuity (reproduce AC10 `no_B` field-for-field), T2
exchange-mediation (`no_B_retention` dies by income starvation, not export — the
decisive test), T3 unity (boundary state is the sole antecedent of retention + exchange;
`B_rescue` EXTERNAL control), T4 inertness (gate-disabled byte-identical `state_hash`).

**Explicitly NOT successor requirements:** supplied space (permanent substrate —
infinite regress), and the non-spatial controller (a separate full re-architecture, out
of scope). The claim ceiling SR-1 earns, if T1–T4 pass, is a one-step upgrade: "the
produced boundary retains constituents *and* mediates the intake that funds production,
for the material layer" — not full clause (ii).

## 6. Which consciousness-related mechanism, if any, gained evidence

The roadmap's chosen mechanism — the **internally maintained cause-attribution
estimate** (a second-order state about why a first-order route-memory representation is
failing: E_world "obsolete" vs E_machinery "access degraded"), mapped to **HOT-2
metacognitive monitoring** (Butlin et al. 2023) — gained evidence at two of its three
tiers and was bounded at the third:

- **Discrimination tier — gained evidence (AC107):** 0/32 mistakes on fresh cohorts;
  storage maintenance confirmed (observer-discard + no-cause identity 16/16).
- **Coupling tier — gained evidence (AC108):** both directions by single-flag
  intervention (paid acquisition/update write, not ongoing repair), with the survival
  caveat (adaptation reversal 16/16, survival reversal 12/16).
- **First-order uncertainty generalization — falsified as equivalence (P2 + AC113):**
  the graded/weighted form of the estimate buys nothing over a maintained integer
  counter. This bounds the *representation*, not the mechanism's content/coupling.
- **Reliability tier (estimate the evidence channel's own diagnostic value) — deferred,**
  gated on a harness-level probe (P7): distinct and identifiable, but its premise (an
  estimated weight restores a discriminating weighting a frozen weight supplies) is the
  kind of decision-theoretic claim AC113 just showed fails to transfer at organism
  scale.

The strongest wording any of this earns is "meets candidate indicator HOT-2 at degree
Y" — never "metacognitive", never "conscious" (the level-(d)/(e) boundary is untouched,
and the HOT-2 mapping carries a flagged adaptation from perceptual to
interoceptive/route-level content).

## 7. Which manuscript claims are ready

Three paper-ready claims, each with its exact scope and the negatives that must travel
with it (P1 §0):

1. **Level (a) production closure** — SUPPORTED, bounded (K3), with the A2 boundary
   correction attached.
2. **Level (b) adaptive autonomy** — ESTABLISHED (AC99–AC105): acquired and relinquished
   route content on the organism's own viability conditions, with reconstruction and
   decision spending coordinated internally.
3. **Level (c) representational coupling** — a maintained one-bit cause-estimate
   discriminates two causes at ceiling accuracy and is causally coupled to its
   maintenance (the paid acquisition/update write) in both directions, **with the
   survival caveat attached**.

Not claimable (and removed where previously claimed): "autopoietic" unqualified,
"alive", any survival-advantage claim for the estimate, any reliability/monitoring
claim, and the graded-posterior "strict dominance" advantage (removed, P2). The novelty
statement is honest: no conceptual novelty against M&V / M&M / Di Paolo / Butlin; the
contribution is a falsification-disciplined worked demonstration plus a reproducible
catalog of structural walls.

## 8. The single strongest next research question

**Chosen: SR-1 — does the produced boundary mediate the organism–environment exchange?**
(Build the A0 successor: gate `react` actions 0/1 intake on produced boundary state,
and run T1–T4 on a new `acN.py`.)

**Why this is the strongest, against the named alternatives.** It is the only open
question that moves the program's **central** verdict. The autonomy verdicts are stable
under every in-model experiment — moving clause (ii) requires exactly the re-
architecture SR-1 specifies — and it is finite, conservation-safe, non-spatial, and
falsifiable at the gate level. The cognition track's remaining items are either gated
behind a cheap probe (the reliability tier, P7), robustness continuations that do not
move the central goal (three-cause integration, ongoing-repair isolation, the
re-acquisition boundary), or now resolved to a wall twice over (first-order
uncertainty: P2, AC113). This is a judgment about the program's charter question — can
a bounded individual maintain the organization that enables its own activity — not a
claim that the cognition track is closed.

**Cost.** One new runner built by asserted source surgery on `ac4.react`'s actions 0/1
(no frozen file edited; the gate rides the existing `in_m`/`in_f` variables), engineering
seeds first, then the protocol (hashed pre-run), then disjoint final seeds, with
audit/replay/unit tests per the extension checklist. Compute is negligible (the AC line
runs ~0.17 s/condition). The real cost is the build + protocol + 4-test gate +
verification discipline — comparable to the AC112/AC113 effort (one runner, one
protocol, three verification tools, a unit-test file; a few sessions). No frozen
artifact touched, re-run, or re-hashed.

**Falsification risk (two kinds, named separately).**

1. **Hard falsification (low probability):** T2 fails — rescuing retention
   (`no_B_retention`) also rescues the organism under SR-1 — meaning the boundary is not
   constitutive of exchange and the successor is a no-op. Recorded, not moved. Low
   probability because the gate makes intake depend on boundary matter by construction.
2. **Weak-positive risk (moderate, the honest one):** the aggregate integrity gate may
   establish only "B gates intake" — a supplied-reaction dependence — without
   establishing exchange *through* the boundary (semipermeability/mediation in the
   membrane sense), so the result could fall short of the one-step clause-(ii) upgrade
   A0 set as its ceiling. If it does, it is reported at the weaker level ("B is
   constitutive of intake"), not reworded to the stronger one; A0's per-channel
   refinement is the named, deliberately out-of-scope path to true semipermeability.

**Labeling discipline attached to the choice.** SR-1 is a **re-architecture** (a change
to a supplied reaction's dependence), not an in-model experiment. The P3 stability claim
must therefore be restated precisely: no in-model run moves the clause-(ii) verdict; SR-1
moves it precisely *because* it is a model change. That is a feature of the choice, and
it must be said, not hidden.

**Named, not authorized now (so this is a bounded disposition, not exhaustion).** (1)
The reliability-tier organism-scale study — deferred, gated on the P7 harness probe
(corrected economics, varying ε, estimated-vs-frozen weight), whose outcome either
authorizes a bounded study or defers the tier with a named wall. (2) The three-cause
integration, the ongoing-repair isolation, and the re-acquisition boundary — robustness
continuations on record, subordinate to SR-1.

---

## Sources

`P3_CORRECTIONS_v1.md` (t_5308450a), `AC113_RESULTS_v1.md` + `AC113_PROTOCOL_v1.md`
(t_9c80a9ad, P6), `P7_FEASIBILITY_v1.md` (t_4aefbe19), `A0_SUCCESSOR_SPEC_v1.md`
(t_89213031), `P1_MANUSCRIPT_DRAFT_v1.md` (t_a6d71e28, W0), `C4_P2_EQUIVALENCE_v1.md`
(P2), `P4_COGNITION_CONTINUATION_v1.md` (P4), `S1_SYNTHESIS_v2.md`,
`EVIDENCE_INDEX_v3.md`, `AUTONOMY_RESEARCH_STATUS.md`, `CONSCIOUSNESS_ROADMAP_v1.md`,
`AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`, `AC109_ENGINEERING_v1.md`,
`AC110_RESULTS_v1.md`, `AC111_RESULTS_v1.md`, `AC105_RESULTS_v1.md`,
`CLOSURE_VERDICT_v1.md` (K3), `A2_BOUNDARY_VERDICT_v1.md`. This document is derived and
is not hashed into any study's `pre_run_snapshot.json`.
