# ACI mission audit v1 — what the artificial-organism program established, and what carries into a consciousness-oriented neural architecture

2026-09-25. Audit deliverable for the Q0 card (t_b6b804ba): *what has the artificial-organism
program (AC1 through AC117, plus the E/A/C/I/P/M/K/S tracks, at HEAD `eb79ecb`) genuinely
established, and which findings are worth carrying into a consciousness-oriented neural-architecture
program?*

This is a synthesis/audit document. It runs nothing, re-hashes nothing, freezes nothing, and edits
no frozen artifact (runner, protocol, results dir, hash, or ledger). Every claim is read from the
frozen sources and the derived reconciliation documents named in §Sources. It is the mission-lock
evidence map for the ACI (Q-series) phase: it separates the organism program's findings into what
the next architecture inherits, what stays behind as artificial-life science, and what was pursued
past its relevance.

**Reading discipline applied throughout.** (1) Negative findings are *part of the architecture
specification*, not noise to be discarded — every section carries them. (2) Historical results are
reported as they were recorded, including their later errata; nothing is rewritten to fit the new
framing. (3) Seeds are the replication unit (N seeds × 2 histories = N independent units). (4)
Survival is a bimodality-aware lower bound (AC68), never a per-seed-family guarantee. (5) "Frozen" =
hashed protocol + `mkdir(exist_ok=False)` results dir + audit (re-derives gates without simulating)
+ replay (sampled exact reruns).

---

## 0. The one-paragraph answer

The artificial-organism program established **three paper-ready claims, all bounded, none
consciousness-bearing**:

1. **Level (a) production closure — SUPPORTED, bounded.** Every necessary component {W, C, B,
   description, derived program} meets C1–C5 and every maintained-state item {pointer, coordination,
   route memory, decision state} meets S1–S4, forming one strongly-connected production-dependency
   network with no external root — *within the declared model and operating range, under the accepted
   substrate convention* (K3, `CLOSURE_VERDICT_v1.md`). Not "autopoietic" unqualified, not "alive."
2. **Level (b) adaptive autonomy — ESTABLISHED** (AC99–AC105): internalized decision state (Gray
   streak + reserve + allowance) that the organism maintains through paid, W-gated writes.
3. **Level (c) representational coupling — a maintained one-bit cause-estimate discriminates two
   causes at ceiling accuracy (0/32 mistakes, AC107) and is causally coupled to its maintenance
   machinery in both directions (AC108, 7/7)** — with the survival caveat attached (the estimate's
   causal role is behavioural, not survival-level).

The **full two-clause autopoiesis criterion is NOT ESTABLISHED**: clause (i) is supported, clause (ii)
(constitute a concrete unity in space) is met only at the material (constituent) layer, and the sole
remaining genuine limitation is the **non-spatial informational core** — a finite successor question
(R1–R4, tests T1–T5), not a permanently untestable fact. The program's *cognition* track — the part
relevant to a neural architecture — is **characterized, not exhausted**, and its sharpest result is a
string of **recorded negatives**: the graded generalization shows no advantage over an integer counter
(AC113/R1), maintained storage shows no significant income advantage over a tuned memoryless rival
(AC116, suspended at the resolution floor), ongoing repair is not load-bearing inside the decision
window (AC110), and the "reliability/monitor" tier, run at the harness level, is **CONTROL-yes /
PREDICTION-no** (AC117/M6). **What the organism program actually transfers to a neural architecture is
not its physics or its specific mechanisms, but a small set of architectural principles — internalized
paid maintenance, causal-role-over-encoding, and a strong-rival + gate-shape discipline — plus a list
of assumptions the neural program must not silently inherit.**

---

## 1. The master audit table

Columns are the eight the card requires. "Exact architecture" names the runner(s) and mechanism, not a
prose paraphrase. "Confidence" uses: HIGH = frozen, byte-identity reproduced, multiple studies; MED =
frozen single study or seed-bounded; LOW = engineering-only, harness-level, or design-only; SUSP =
suspended at the sign-flip/measurement resolution floor. "More organism work?" is the Q7-facing
judgment (does resolving this change the neural architecture we would build?).

### 1.1 Autonomy / organizational track

| Finding | Exact architecture | Evidence | Confidence | Falsified | Unresolved | Neural relevance | More organism work? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Production closure over {W,C,B,description,program} (clause i) | AC105 (ac105.py, seeds 5800–5807), the five-mechanism integration; inherited from AC80–99 via AC104→…→ac95 byte-identity chain | K3 C1–C5 per component + S1–S4 per state item, each code-traced (DEPENDENCY_AUDIT_v2_CORRECTION, CLOSURE_CRITERION_CONSISTENCY); AC10 ablation (9/9), AC91/92 W-dependence | HIGH | — (the criterion itself was *sharpened* by K2: C5/C6/C7/C8 moved to maintained state; C5 network criterion added) | Clause (ii) spatial unity (J4) — outside this criterion's scope | The C1–C5 + S1–S4 *form* (produced-and-replaced vs damaged-and-maintained state; network-criterion closure) is the strongest transferable abstraction: a checkable definition of "self-maintaining organization" | NO (in-model stable; further runs won't change it — A0/I5) |
| Adaptive autonomy (level b): internalized decision state | AC96/AC99/AC99_d2/AC100/AC104/AC105 (streak in dead-rule free bits, Gray coding, reserve bit, allowance-42) | Gray encoding carries AC99/100 success (2×2 factorial isolates Gray, not reserve); allowance-42 6/6 gates, rescues one unseen marginal priority | HIGH | AC97/98 reserve design (withholds/starves the decision it funds); AC102/103 (no universal spending policy) | Seed-dependent decision-state economics (allowance-42 rescues 5804, harms diagnostic 5603) | P2/P5: decision state can be maintained internally and its *encoding* (Gray vs binary) is a cost lever, not a semantic change | NO (established; robustness limits only) |
| Boundary-mediated exchange at the material layer | AC114 (ac114.py, seeds 6500–6507, SR-2 site gate on AC9 body) | D1 site-vs-count, D2 local, D3 semipermeability 16/16; B→(retention+exchange)→production→B by ablation | HIGH | — (A2's "exchange supplied" limitation resolved at material layer) | Exchange *law* (gated react actions) still supplied; exchange role only at material layer | Only as an ALife closure fact; the *site-gate vs count-gate* contrast is a minor principle (local live-state, not aggregate) | NO |
| Exchange composes with the five-mechanism closure | AC115 (ac115.py, seeds 6600–6607, AC114 SR-2 gate on AC105 body) | G1 byte-identity to AC105; G2/G3 admission discriminations; six functions exercised 16/16 | HIGH (mechanism level) | — | Survival-level composition NOT confirmed (G4–G7 retained as failed, seed-dependent) | The *method* — composition licensed by byte-identity (`state_hash`), not prose — is the transferable lesson | NO (mechanism-level done; survival-level is AC68/AC39, a known wall) |
| Whole-organism unity (clause ii) | All architectures (informational core in fixed arrays never passed to tr.move) | Transport call verified (ac9.py:78); I5/A0 code trace | HIGH (as a limitation) | — | Sole remaining clause-(ii) limit = non-spatial informational core; finite successor R1–R4/T1–T5 (S1 spec exists, design-only, AWAITING authorization) | Marginal: a neural architecture has no "spatial unity" question in this sense; but R2 (local access, no host dereference) and R3 (retention vulnerability) map loosely onto "no hidden pristine backup" | NO — defer to the ALife paper (Q7's call; the successor does not change what a neural architecture would build) |
| W production is load-bearing machinery (not just content) | AC91/92 (W-birth block; functional interruption-and-rescue) | Block W-birth → W=0 → 8/8 die with description intact at death; restore before t=63 rescues | HIGH | — | None (W=0 is autocatalytically irreversible — a named cascade) | P2/P7: the machinery that maintains representations is itself produced and load-bearing; a neural architecture's "maintenance" is not free scaffolding | NO |

### 1.2 Cognition / representation track

| Finding | Exact architecture | Evidence | Confidence | Falsified | Unresolved | Neural relevance | More organism work? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| One-bit cause-estimate discriminates two causes at ceiling accuracy | AC107 (ac107.py, seeds 6000–6007; estimate in dead-rule action bit) | 0/32 post-intervention mistakes; observer-discard 16/16; no-cause identity 16/16 | HIGH | AC106 (update rule dropped the `bound` flag — implementation defect, corrected) | Survival advantage seed-bounded (Q4) | P3: a *minimal* maintained state can be causally load-bearing for a discrimination, without graded content | NO (characterized) |
| Causal coupling in both directions (content ↔ maintenance) | AC108 (ac108.py, seeds 6100–6107; no_write / force_machinery / scramble) | 7/7 gates: maintenance→accuracy/use 16/16; content→adaptation/production 16/16 (move direction), survival reversal 12/16 | HIGH | — | Survival reversal is 12/16, not 16/16 (N1 correction) | P3's "flexible consumption": the same content drives ≥2 behaviourally distinct policies (relinquish vs maintain) | NO |
| Storage is inert in the clean world (content load-bearing, not storage) | AC109 (engineering, seeds 0–7; direct-diagnostic rival) | Direct diagnostic matches stored estimate on 48/48 cells at lower cost | MED (engineering) | Persistent-history-as-memory in the clean world | — | P5's sharpest form: the representation's causal role is as a *selector*, not a memory; when the current observation is decisive, storage adds nothing | NO |
| Ongoing repair not load-bearing in the decision window; load-bearing post-window | AC110 (ac110.py, seeds 6200–6207; repair cut vs maintained) | G2/G3/G5 48/48 (correctness rides reacquisition); G4 8/16 (post-window storage drift) | HIGH | "repair sustains function in-window" (N1) | Elevated-rate damage elsewhere would fire action 2 and restore the bit (conditional, not absolute) | P1/P7: correctness and maintenance are temporally separable; the *acquisition/update write* is what carries correctness, not continuous repair | NO |
| Composition with autonomy: direct channels clean, full composition retains two failed gates | AC111 (ac111.py, seeds 6300–6307) | Reconstruction never overwrites estimate; allowance never starves reacquisition; G3/G5 12/16 (corrupted contact rule re-schedules reacquisition) | MED (frozen, partial) | Full composition (2 gates retained as failed) | Seed-dependent behavioural interference (6306/6307) | P7's cautionary form: composing two frozen capabilities can trip an observation threshold neither alone triggers | NO (named interference is the answer) |
| Graded/weighted generalization: no demonstrated advantage | AC113 (ac113.py, seeds 6400–6407; two-counter vs single-counter); R1 reanalysis | Seed-level sign-flip p ≈ 0.71/0.63, n=8; candidate worse on survival/expenditure/false-relinquish | HIGH (negative) | F1 "equivalence" label (R1: nonsignificance ≠ equivalence) | — | P5: a graded register buys nothing over an integer counter; gradedness is not intrinsically better | NO (resolved negative) |
| Graded posterior is an integer counter in float clothing | C4 probe + P2/R2 (decision-theoretic, harness-level) | `N = ceil(logit θ/LR)` exact for every θ; strongest rival made bit-identical once the decisive observation is added | HIGH (mathematical) | "strict dominance over heuristics" was a rival defect | — | The single most important caution for a neural program: before claiming a continuous representation is superior, check it is not an equivalent discrete accumulator | NO |
| Maintained storage vs tuned memoryless rival: no significant income advantage | AC116 (ac116.py, seeds 6600–6607; integer counter vs tuned memoryless) | Mean +200/seed, exact sign-flip p=0.0625 (the resolution floor); weakly dominant (0 worse, 5 better, 3 tied) | HIGH (F1) | "storage line closed" and "maintenance not graded-useful" (M2 errata: both withdrawn) | Storage question SUSPENDED at the resolution floor — not closed, not demonstrated | P1/P5: a genuine mechanism can be causally load-bearing (G3, 4/16 vs 16/16 false-relinquishments) while economically invisible; do not grade usefulness on income alone | NO (further storage runs explicitly not licensed, S0) |
| Reliability/monitor tier: CONTROL-yes, PREDICTION-no | M3 target + M5 design + M6/AC117 (seeds 6800–6815, 480 rows) | Directional repair keeps e correct 32/32 (C-G1–G4); P-G5/P-G6 fail vs transient `ones>=4`; vacuous at ambient damage | HIGH (harness) | "second-order reliability *predictor*" (the monitor is a directional-repair controller, not a reliability grader) | Re-openable only by bidirectional damage with an acquired 1-value | P6 + the control/prediction split: a maintained state can be load-bearing for *control* while inert for *prediction*; do not assume a representation earns its keep by predicting | NO (harness bounded; no organism-scale monitor protocol licensed) |

### 1.3 Methodology / discipline findings (transferable as process, not as claims)

| Finding | Exact architecture | Evidence | Confidence | Falsified | Unresolved | Neural relevance | More organism work? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Strong simple rivals are mandatory and routinely falsify | AC11 (state-blind duty cycle beats adaptive arm), AC16/17 (gate-shape), AC113/116 (counter/memoryless rivals) | Each documented in its protocol/results | HIGH | — | — | P6: the sufficient-statistic / reactive / state-blind / memoryless rival set is the single highest-value transfer | NO |
| Gate shape must match claim shape | AC16 (mean margin missed by 0.006), AC17 (strict dominance unsatisfiable at ceiling), AC45 (heterogeneity is shape not property), AC46 (bimodal endpoint) | Recorded failures, all pinned in test suites | HIGH | — | — | Categorical claims → dominance/separation-of-minima gates; check satisfiability before freezing | NO |
| Byte-identity (`state_hash`) is the composition and equivalence license | AC114 G1, AC115 G1, AC80/85 unit tests, replay discipline | Frozen rows reproduced field-for-field | HIGH | — | — | The discipline of proving a change is inert (byte-identical) before attributing a difference to it | NO |
| Read/repair convention alignment | AC67→AC69→AC71 (register read-1 vs repair trigger ≥4; aligning to majority-read closes all three closure gaps) | 8/8 survival, routes held | HIGH | — | — | A maintained state's read convention and its repair trigger must use the same threshold or the state lapses | NO |
| The optimum can be a level, not a switch | AC11 (learning threshold irrelevant; optimum is intermediate duty) | Swept the learner's own parameters | HIGH | — | — | Before claiming an adaptive policy, sweep the *rival family* and your own parameters | NO |

---

## 2. The six explicit classifications

### 2.1 Findings worth carrying forward (the architectural law that survives)

These are the candidates Q2 will convert into principles (P1–P7). They are listed with the
strongest wording the evidence earns — nothing more.

1. **Representations have maintenance costs, and maintenance is internalized (P1 + P2, S1–S4).**
   A representation that is *in-world* (S1), *damage-reachable* (S2), *paid-maintained through
   produced machinery* (S3), and *correctness-neutral* (S4) is the program's most-repeated positive
   result — established for route memory (AC7/8/15/18/75), the decision register (AC96/99/100), the
   description (AC79/80/85/86), and the estimate (AC107/108). The lesson for a neural architecture is
   not "add repair" — it is that the *cost of maintaining a representation* is a first-class design
   variable, budgeted and gated, not an incidental overhead.
2. **Cognitive state can be load-bearing — as a content *selector*, not a memory (P3, AC107/108/109).**
   The one-bit estimate is causally load-bearing (AC108 7/7) while its *storage* is inert where the
   current observation is decisive (AC109). Content is what matters; persistence is a means, and it is
   a means whose value is bounded by whether the world's history is actually informative.
3. **Encoding is secondary to causal function and cost (P5, AC99/100 + P2/R2 + AC113).** Gray coding
   carries AC99/100's success — the same decision state, a cheaper transition encoding. The graded
   posterior is an integer counter (R2); the two-counter shows no advantage over one (AC113). A neural
   architecture should choose encodings for *cost and causal function*, not for gradedness-as-a-virtue.
4. **Causal load-bearing and economic value are separable (AC110, AC116, AC117).** A mechanism can be
   causally effective and economically invisible (AC116: 4/16 vs 16/16 false-relinquishments, income
   +0.5%; AC117: e correct 32/32, income +3%). Do not grade a representation's worth on its downstream
   reward delta alone.
5. **Strong simple rivals are mandatory, not optional (P6).** The sufficient-statistic rival (P2/R2),
   the direct-diagnostic rival (AC109), the tuned memoryless rival (AC116), the state-blind fixed duty
   (AC11), and the transient `ones>=4` reflex (AC117) are the instruments that killed AC11, AC16,
   AC17, AC113, AC116, and the monitor's prediction claim. Any neural claim about an internal state
   must be tested against the strongest state-blind / reactive / finite-state rival.
6. **Maintenance and cognition must eventually compose (P7, AC111/115).** Composition is established at
   the mechanism level (AC115) and bounded at the survival level (AC115, AC111). The *method* — prove
   the composition is byte-inert at the intact boundary, then test the interaction — is the transfer.
7. **Correctness rides reacquisition, not continuous repair, inside the decision window (AC110).**
   The paid *acquisition/update* write carries accuracy; ongoing repair matters only for post-window
   storage. A neural architecture that assumes a persistent "repair loop" is doing correctness work
   must check whether re-learning on open evidence isn't the thing that actually works.

### 2.2 Findings useful only for the artificial-life paper (do not carry)

1. **The conservation-law physics and the material economy** — `ac4.balance` identities (spent_m,
   spent_e, W/C/B birth costs), fuel/material intake, the 64-tick `life` decay. This is the organism's
   substrate; a neural architecture has no such economy unless one is deliberately chosen.
2. **The specific component machinery** — the autocatalytic W catalyst, the C energy converter, the
   20-link B boundary, the 126-bit rule program, the 130-bit description, the succession
   copy→verify→switch→remove machinery. These are the organism's *realization*; they encode one
   particular answer to "produced, replaced, paid-maintained components," not a universal design.
3. **Boundary-mediated exchange (AC114/AC115)** and the whole **clause-(ii) spatial-successor question
   (S1, R1–R4/T1–T5)**. This is the autopoiesis-completion track. It changes nothing about what a
   neural architecture would build (Q7 evaluates this explicitly). Preserve for the ALife paper.
4. **The AC47/48/49/50 structural limit** — a self-funding world cannot be both stable and graded;
   the order only differentiates outcomes near the death threshold. This is a result about
   self-funded populations, not about representation.
5. **The AC68 W/C bimodality and AC39 engineering-vs-finals transfer failure** — as *facts about this
   lineage's* stochastic stress and seed sampling, they are ALife-paper material; as *lessons*
   (bimodality-aware gates, disjoint seed families, no upper bound on survival), they carry (§2.1#6).

### 2.3 Questions pursued too far relative to their relevance

The criterion here is *not* "was it a mistake to start" — the falsifications were necessary — but
"was it continued past the point where the answer was already implicit, or where the answer no longer
moved the architecture."

1. **The graded/weighted generalization (AC112/AC113).** P2/R2 had already proven at the
   decision-theoretic level that the graded posterior is an integer counter. AC113 ran it at organism
   scale and returned "no demonstrated advantage" (R1) — the answer was implicit in the equivalence
   proof. The organism-scale run was worth *one* confirmation; it should not have been a third study.
2. **The storage comparison (AC116).** Weak dominance at the sign-flip resolution floor
   (p = 0.0625). S0-v3 records it as "not a license for further storage-comparison runs"; the storage
   question is suspended, and continuing to compare maintained-vs-memoryless would not move the
   architecture — it would only re-measure the same floor.
3. **The reliability/monitor tier (C0/C1 → M3/M5/M6/AC117).** The M-track answered the reopened
   question at the harness level: CONTROL-yes / PREDICTION-no / vacuous-at-ambient. Re-testing
   prediction under a different damage model is, per S0, "a robustness re-test, not a new ceiling."
   The tier should be parked (K9 gate: re-open only on a mechanism change introducing a non-trivial
   error rate where the damage count is not already the wrongness signal).

### 2.4 Architectural principles that repeatedly survived falsification

These are the *positive* invariants — each survived at least one targeted ablation/rescue and one
attempted reduction to a simpler rival.

1. **Internalized, paid, W-gated maintenance (S1–S4).** Survived AC10 (no-W/no-C/no-B), AC67 (sticky
   damage), AC79/80/85/86 (description storage), AC91/92 (W production load-bearing). Every component's
   retention is *earned*, and cutting the earning kills the function.
2. **Redundancy + majority-read protects content.** 7 replicas/bit, majority read. The load-bearing
   constraint *shifts* with the read/repair convention (AC67 read-1 → AC69 → AC71 majority-read closes
   the gaps); align the read convention with the repair trigger.
3. **Erase-on-relinquishment as the decision primitive (AC75).** The drop clears the entry so the next
   contact is blind; the no-erase rival dies 8/8 under change. A decision state must *act* on its
   substrate, not just flag it.
4. **Byte-identity as the equivalence/composition license.** A change that leaves the trajectory
   byte-identical (state_hash) cannot have altered any other path (AC114 G1, AC115 G1). This is the
   program's most portable rigor.
5. **Causal-role vs economic-value separation.** Repeated at AC110, AC116, AC117. A mechanism is
   "load-bearing" and "economically marginal" at the same time, and both statements are true.
6. **Content load-bearing, storage context-dependent (AC109).** The representation's causal role as a
   selector is what matters; persistence buys nothing where the observation is decisive.

### 2.5 Assumptions that should NOT be inherited into a neural architecture

Each is an assumption the organism program either falsified directly or proved scoped; inheriting it
silently would re-commit a known error.

1. **The ideal-observer assumption (C0).** Do NOT assume a decision state is its own reliability
   readout ("the posterior is its own confidence"). C0's collapse is valid *only* under that
   assumption; the AC architecture violates it by construction (C1). A neural architecture that wants a
   monitoring/confidence state must build the *separation* (spatial/temporal, different information),
   not assume it away.
2. **Graded/continuous representations are intrinsically better.** Falsified (R2, AC113): the graded
   posterior is an integer counter; the two-counter beats neither. Assume discreteness is the default
   until a graded form is shown to buy a *distinct* causal capability.
3. **More maintained state = better.** Falsified (AC109 storage inert, AC116 suspended): state that is
   never load-bearing is pure cost. Do not add state for richness; add state where a rival without it
   provably fails.
4. **Causal load-bearing ⇒ survival/income advantage.** Falsified (AC107 Q4, AC108, AC110, AC116,
   AC117 — retention 1.00, income +3%). A neural program must not gate on survival/reward deltas for a
   representational claim; gate on the causal contrast.
5. **The optimum is a switch, not a level.** Falsified (AC11): the best maintenance policy is an
   intermediate constant level, not a learned all-or-nothing switch. Sweep the level family before
   claiming a switch.
6. **A maintenance cost/benefit trade-off exists.** Falsified-by-absence (AC11 economy check: the
   frozen economy priced maintenance at ~25× its payoff; AC15 design rule). Measure the payoff against
   the cost in the actual economy before designing an allocation study.
7. **Content self-production is a prerequisite for representation.** Withdrawn (AC78 blocked but NOT
   required; `CONSCIOUSNESS_ROADMAP_v1.md` §2 removed the gate). Regenerating inherited organization
   and discovering better organization are separate problems; a representation claim does not wait on
   self-produced content.
8. **The organism's specific substrate.** The 126-bit rule bank, the conservation economy, the W/C/B
   particles, the succession machinery — none of it is a neural substrate. What transfers is the
   *principles* in §2.1/§2.4, not the physics.

### 2.6 Mechanisms that looked cognitively interesting but collapsed into simpler control policies

These are the program's most instructive negatives — each *started* as a candidate for a genuinely
interesting internal computation and *ended* as a simpler policy or a label applied to first-order
processing.

1. **The self-monitoring / self-repair loop (AC67/AC71) → a watchdog timer.** The paid
   corruption-triggered repair reflex is one bit driving one fixed action, read from host-side
   observation each tick, never stored/maintained/produced. It is homeostatic infrastructure, explicitly
   *not* a consciousness indicator (`CONSCIOUSNESS_ROADMAP_v1.md` §3). The lesson: "pays to repair its
   own corruption" is outside every consciousness framework; do not mistake a watchdog for
   self-representation.
2. **The graded Bayesian posterior (C4) → an integer counter (P2/R2).** Calibrated, "strictly
   dominant" over heuristics — until the one omitted decisive observation was added to the rival, making
   it bit-identical to the graded policy. The graded form was the integer counter in float clothing.
3. **The weighted two-counter (AC113) → no advantage over a single counter.** The heterogeneous
   generalization of the estimate buys nothing the homogeneous counter lacks.
4. **The maintained storage/counter (AC116) → weakly dominant only; the tuned memoryless rival nearly
   ties.** The representation's value is its open-blind latch (a cut-safety edge), which the world's
   economics do not price. The "memory" is not doing the work; the content is.
5. **The reliability/monitor state (AC117) → a directional-repair controller.** Direction knowledge is
   load-bearing for *which way to repair* (control), inert for *predicting wrongness* (the transient
   damage count already predicts perfectly). The "monitor" is a control parameter, not a reliability
   grader.
6. **The adaptive allocation arm (AC11) → beat by a state-blind fixed duty cycle.** The learner's own
   threshold made no difference; the optimum was a *level*, so the whole adaptive family was beatable.
   A state-blind policy matching the best learner configuration is the signature that no acquired
   decision was demonstrated.
7. **The "heterogeneous impairment" effect (AC45) → a response-shape prediction, not a property.** The
   impaired fraction is seed-dependent (0.88/0.875/1.0 across families); gating on "heterogeneity
   present" gated on a shape prediction, not the claim.
8. **The population-based self-directed learner (AC72/73/77/78) → blocked by a locked, path-dependent
   fixed point.** The live-site signal converges to a seed-specific fixed point (N_eff ≈ 1), so no
   within-life learner resolves the fine ranking; the ranking is real only at the coarse level, and only
   via multi-environment averaging. Content self-production is blocked — *not* because the search is bad,
   but because a single life is one sample of a fixed point.

---

## 3. What the program's *negative* ledger specifies for the next architecture

Assembled as a design specification, the negatives above say: the next architecture must (a) not
assume graded representations beat discrete counters; (b) not assume a representation's value is its
reward delta; (c) not assume monitoring/confidence is a free re-encoding of the decision state; (d)
always test against the strongest state-blind / reactive / sufficient-statistic / memoryless rival;
(e) gate categorical claims on dominance or separation-of-minima, never a mean margin; (f) prove
inertness by byte-identity before attributing a difference to a new mechanism; and (g) price a
capability against its maintenance cost in the actual economy before asserting a trade-off exists.

These are not "lessons learned" in the soft sense — each is pinned in a frozen protocol, an errata, or
a test suite, and each maps to a concrete falsification the program actually recorded.

---

## 4. Disposition and what this hands downstream

- **Q1 (target construct).** The program establishes that the closest thing to a
  consciousness-relevant object it built — a maintained cause-attribution estimate — is *first-order
  cause inference*, not a second-order monitor (C0/C1), and its monitoring generalization is a
  directional-repair controller (AC117). The target construct must therefore be defined without
  inheriting "metacognitive monitoring" as an achieved tier; the honest starting point is "internally
  maintained representations that are causally coupled to their maintenance" (level c), which *is*
  established.
- **Q2 (architectural principles).** §2.1 and §2.4 are the candidate-principle shortlist, with §2.5
  as the counter-evidence set and §2.6 as the collapse record. Every principle Q2 promotes must survive
  the concrete falsifications named in §1.2/§2.6.
- **Q7 (organism exit).** The audit's "more organism work?" column is NO across the board: the
  autonomy track is stable in-model, the cognition track is characterized with recorded negatives, and
  the sole remaining organism question (clause ii, S1) is a re-architecture that does not change the
  neural design. The organism line has reached its information-theoretic endpoint; what remains is
  ALife-paper material, not neural-architecture input.

Neither autopoiesis nor consciousness is claimed anywhere in this audit. The strongest wording the
organism program earns, after every correction, is unchanged: production closure SUPPORTED and bounded,
adaptive autonomy ESTABLISHED, representational coupling SUPPORTED with the survival caveat, and the
whole-organism unity and reliability tiers NOT ESTABLISHED / bounded respectively.

---

## Sources

`EVIDENCE_INDEX_v3.md` (authoritative baseline), `S0_SYNTHESIS_v3.md` (terminal synthesis),
`S0_CONTINUATION_DECISION_v1.md` (decision c), `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (I0),
`CLOSURE_VERDICT_v1.md` (K3), `DEFINITIONS_CHARTER_v2.md` (K2 criterion), `A4_EXCHANGE_VERDICT_v1.md`,
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`, `A0_AUTONOMY_VERDICT_v1.md`,
`S1_SPATIAL_SUCCESSOR_SPEC_v1.md` (design-only), `C0_FEASIBILITY_v1.md`,
`C1_RELIABILITY_DISPOSITION_v1.md`, `CONSCIOUSNESS_ROADMAP_v1.md`, `AC115_ERRATA_v1.md` (M1),
`AC116_ERRATA_v1.md` (M2), `AC117_RESULTS_v1.md` (M6), `P1_MANUSCRIPT_DRAFT_v1.md`. Frozen results read,
never re-run or re-hashed: `ac114_results_v1/`, `ac115_results_v1/`, `ac116_results_v1/`,
`ac117_results_v1/` and the earlier frozen dirs. This document is derived and is not hashed into any
study's `pre_run_snapshot.json`.
