# P1 manuscript draft v1 — a claim-evidence account, established findings only

2026-09-23 (updated 2026-09-24 with the P-series outcomes, and reconciled the same day
by W0 with the R1/R2 corrections and the A4/C0 results). Derived document for the P1
card (t_2aff2675), updated in place by W0 to reflect the P-series results — P1 (C4
reproducibility), P2 (the sufficient-statistic equivalence, §8), P3 (N-program scope
corrections, already applied), and P4 (the heterogeneous-likelihood-ratio continuation,
§10) — and to carry the R1 AC113 statistical reanalysis (F1 "equivalence" → "no
demonstrated advantage", §8/§10), the R2 P2 proof correction (equivalence exact for
every θ via the `>=` convention, §8), the A4 boundary-exchange verdict (exchange
boundary-mediated at the material layer, §4), and the C0 reliability-identifiability
verdict (the reliability tier is not a separable mechanism, §8/§10). It is a claim-evidence manuscript draft assembled from established findings at
HEAD 77ace95 plus the N1 and A2 corrections. It runs nothing, re-hashes nothing, freezes
nothing, and authorizes no experiment. **This is manuscript development, not authorization to submit or publish
externally.** Every claim carries its evidence (frozen study + exact numbers) or is
explicitly marked engineering-only or pending. No frozen artifact (runner, protocol,
results dir, hash, ledger) is edited.

The discipline enforced throughout: (i) only the strongest wording the evidence earns;
(ii) a death never improves an average — survival is always a bimodality-aware lower
bound, reported separately from raw final-state accuracy; (iii) seeds are the
replication unit (N seeds × 2 histories = N independent units); (iv) "first
demonstrated" means *first in this project's lineage*, never a field-level priority;
(v) pending results and new hypotheses are partitioned from established findings.

---

## 0. Status note (read first)

Three bounded claims are paper-ready; the rest of this document is their exact scope,
their evidence, and the negatives that must travel with them:

1. **Level (a) production closure** — SUPPORTED, bounded (K3), with the A2 boundary
   correction and the A4 exchange extension attached: the produced boundary retains
   constituents *and* mediates the intake that funds production, at the material layer.
2. **Level (b) adaptive autonomy** — ESTABLISHED (AC99–AC105).
3. **Level (c) representational coupling** — a maintained one-bit cause-estimate
   discriminates two causes at ceiling accuracy and is causally coupled to its
   maintenance machinery (the paid acquisition/update write, not an exercised
   ongoing-repair loop) in both directions, **with the survival caveat attached**.
   Its *generalization* to graded/weighted form is **not** a paper-ready claim: the
   maintained two-counter did **not** demonstrate an income advantage over the
   single-counter rival (AC113; R1) — see §10.

Not supportable, and not claimed here: "autopoietic" unqualified, "alive",
"self-sustaining", "conscious", "metacognitive", "self-aware"; any survival-advantage
claim for the cause-estimate; any reliability-monitoring claim (C0: the reliability
tier is not identifiable as a separable second-order mechanism under a label-free
criterion — it collapses to first-order inference).

---

## 1. Abstract (scoped)

We report a simulated bounded individual in which a finite set of produced components
{catalysts W, converters C, boundary B, a controller description, and a derived
program} meets a machine-checkable production-closure criterion — every necessary
component on a production cycle, no external root — *within the declared model and
operating range, under an accepted substrate convention* (level (a); K3,
`CLOSURE_VERDICT_v1.md`). The individual also acquires and relinquishes route content
on its own viability conditions, via a Gray-coded relinquishment streak coordinated
with reconstruction spending (level (b); AC99–AC105). Finally, a one-bit cause-estimate
maintained in vulnerable paid-maintained state discriminates two causes — an
environmental route move versus a read-machinery cut — with **zero mistakes across 32
final individuals**, and is causally coupled to its own maintenance machinery (the paid
acquisition/update write) in both
directions, each direction isolated by a single-flag intervention against matched
rivals (level (c); AC107/AC108).

The negatives are stated with the same weight: the representation's **survival
advantage does not transfer** to fresh families (seed-bounded), its maintenance is a
**single paid acquisition/update write** rather than an exercised ongoing-repair loop,
the **reliability tier is not identifiable** as a separable second-order mechanism (it
collapses to first-order inference, C0), the **weighted (two-counter) generalization
does not demonstrate an income advantage** over a single counter (AC113; R1), and a
direct diagnostic controller that reads the same observation transiently **matches the
stored estimate on every behavioural endpoint** — the estimate's storage is inert *in
the clean task*, its content is load-bearing (C1, engineering; this licenses nothing
about ambiguous-observation worlds, C2). No
conceptual novelty is claimed against any prior theory; the contribution is a worked,
falsification-disciplined demonstration and a reproducible catalog of structural
walls.

---

## 2. Scope statement: what is and is not claimed

The project's question is whether a bounded artificial individual can maintain the
organization that enables its own activity, and acquire maintenance priorities through
that dependence. The claims below are bounded to:

- **A declared model and operating range** (specific seeds, conditions, tick horizons —
  §6 states them per claim). Not universal.
- **A supplied substrate** (§3). The verdict is conditional on and carries this
  classification.
- **Production closure (M&V clause i), not spatial unity (clause ii), not
  consciousness.** Clause (ii) is unresolved and limited by modeling declarations, not
  by missing data (§4).

Explicitly **not** claimed: full two-clause autopoiesis (clause (ii) spatial unity for
the whole organization remains unestablished, A4); any subjectivity or phenomenal
claim; that the boundary mediates exchange for the *whole* organization (established
only at the material layer, A4); that content is self-produced (blocked at AC78 and not
required); any survival advantage for the cause-estimate; any reliability/meta-
monitoring result (not identifiable as a distinct mechanism, C0).

---

## 3. The model and its supplied substrate

The organism is a simulation (`ac9`-family world) whose body carries finite,
damageable state. The substrate — supplied by declaration, never produced by the
organism — is (charter v2 §5, made explicit by A1):

- **Operations and constants**: `prog.choose` (the 14-bit rule interpreter),
  `advance()` (the succession copy→verify→switch→remove state machine), the decode
  format, the observation function, conservation laws, the damage model, the tick
  clock, and world constants.
- **Storage media** (A1's explicit accounting): the `traces` arrays (`(4,1024,7)`),
  the `mem.Memory` arrays (`(2,2,3,7)` bits + life), and the boundary lifetime array
  `boundary[20]` — all allocated at development by the simulator's `acquire()`
  scaffold and never re-allocated during life.

The modeling judgment **J1 is resolved as substrate** (K3): interpretation and
succession semantics are supplied, not undeclared coordinators. This is a modeling
choice, not a measurement — the infinite-regress argument (any self-maintenance
formalization bottoms out in a fixed substrate) makes it empirically unsettleable, and
the verdict carries the classification. One qualification is retained: `advance()` (a
prescribed procedure with a built-in verify gate) is a *larger* substrate concession
than `prog.choose` (a passive interpreter).

The A1 realization ledger accounts for the four necessary operational-state items
(pointer, coordination, route memory, decision state): each is **(b) explicit
substrate provision** for its *storage medium* plus **maintained state** (S1–S4) for
its *value*. None is a produced component (none of the storage regions is produced or
replaced during life); none is an unaccounted dependency (the arrays are supplied, and
the writes that maintain them are paid through the produced W catalyst).

---

## 4. Boundary scope (A2 correction + A4 exchange extension, carried)

The produced boundary B is 20 finite-lived perimeter links (`boundary[20]`), produced
by action 8 (2 material + 2 energy, W-anchored), decaying every tick and turning over
~10× per run. Its ordinary causal role is **retention**: it keeps the produced W and C
constituents inside the 5×5 interior (`|pos| ≤ 2`), blocking the export that kills
them at `|pos| ≥ 6`. In the AC114 successor (SR-2, A4) its role is **extended to
exchange**: each contact channel's intake is gated on the local live-state of a produced
gate link, so the produced perimeter both retains the constituents and admits the intake
that funds production — the causal role becomes retention + exchange, at the material
layer.

- **Verdict (a) — production closure for B: SUPPORTED, unchanged.** B meets C1–C5 and
  sits on the W → B → W cycle. Load-bearing: cutting B production exports 8/8 and
  dies 8/8 (AC10 `no_B`); AC4 no-B drops activity −79/−81 points and terminates all.
- **The rescue controls identify the function, they do not refute it.** `no_B_retention`
  (kernel-forced reflection with zero boundary matter) and `B_rescue` (external B
  matter) each reproduce `keep` 8/8. This shows the acquired organization depends on
  the *retention function*, not the boundary's *mass* — and the organism's own means
  of realizing that function is its produced B. The A2 correction strikes the
  "substitution ⇒ unresolved" reading from the spatial-unity verdict: substitution is
  function-identification, not refutation.

- **Verdict (b) — the complete adopted autopoiesis criterion (production closure AND
  spatial unity for the whole organization): NOT ESTABLISHED.** Clause (ii) is met only
  at the *material (constituent) layer*, and is limited by two modeling declarations,
  each a property of the supplied substrate, not an empirical gap:
  1. **The space is supplied** — geometry, lattice, interior/exterior distinction,
     reflection rule, absorbing bath. The organism produces boundary *state*, not the
     spatial distinction itself.
  2. **The controller is non-spatial** — program, description, route memory, pointer,
     and decision state live in fixed arrays never passed to transport. The produced
     spatial unity is a unity of the *constituent layer*, not of the whole organism.

  The former third limitation — **the exchange interface is supplied, not
  boundary-mediated** — is now **resolved at the material layer** by AC114 (A4, the
  SR-2 successor): intake is admitted at the *local* live-state of a produced gate link,
  and the same produced links that retain the constituents are the sites at which the
  intake that funds production is admitted (`B → retention + exchange → production →
  B`). What remains supplied is the *admission reaction form* (the gated `react` actions
  0/1) and the gate associations (`GATE_LINKS`, yields) — the exchange *function* is
  boundary-mediated, its *law* is supplied. This moves the A2 §4.2 item-2 limitation
  from "supplied" to "boundary-mediated (material layer)", and it does not extend to the
  informational core, which neither retains nor admits anything spatially.

---

## 5. The two reference architectures

Two frozen architectures exist at HEAD 77ace95, and their difference is material to
every level-(c) claim.

### 5.1 Autonomy architecture — the AC105 body

The reference body on which K3 issued the closure verdict. It composes three accepted
mechanisms, all operating under `corrupt=True` across a predeclared grid of challenge
timings, priorities, and repeated route moves:

| Mechanism | Established by |
| --- | --- |
| `gray_ctl` — Gray-coded relinquishment streak (3-bit reflected Gray, 1-bit transitions), no reserve | AC99 (5/5), AC100 (2×2 factorial isolates Gray, not reserve — 6/6) |
| Persistent reconstruction trigger (fire while decoded program ≠ description-derived target) | AC103 |
| Allowance-42 budget `max(0, material − 42)`, `DECISION_ALLOWANCE = STREAK_N × 7`, applied throughout life with no challenge-time knowledge | AC104 (6/6), AC105 (6/6) |

AC105 frozen evidence: seeds 5800–5807 (untouched), 2 histories, 2 arms
(`persistent`/`persistent_budget`), 5 conditions (`simult`, `simult3`, `corrupt_first`,
`move_first`, `late`), 160 rows = 80 matched comparisons, 16,384 ticks. All six gates
pass. The rescue (candidate survives where control dies) is 4/80 matched comparisons =
one fresh seed (5804) × two shared-challenge schedules × two histories — not four
independent replications. One `move_first` boundary (5802) kills both arms via the
re-acquisition path; a retained diagnostic reconstruction-level harm (5603 under
`late`) trades reconstruction completeness for a reserve it cannot use.

### 5.2 Cognition architecture — the AC100-derived, `corrupt=False` two-cause world

AC107/108 derive from AC100's `gray_ctl` architecture but **do not carry** the
corruption challenge or the allowance-42 / persistent-trigger decision-spending
refinements. The world: TICKS=16384, DEV=512, PORTS=4 (blind fallback 1/4), mapping
over {0,1}; a `move` flips channel-1 mapping at t=8192; a `cut` suppresses the
channel-1 read for [8192, 8192+96). It carries a maintained one-bit cause-estimate
`e ∈ {E_world=1, E_machinery=0}` plus an explicit diagnostic interface.

The estimate bit lives in the dead-rule action bit (`14·dead_rule_index + 10`),
damaged by the sticky program damage stream, read by majority, written by the paid
W-gated `bel_write`, excluded from `reg_from_active`. Its update rule reads the
organism's own `(bound, used_held, productive)` triple and gates every conclusion on
its own memory (K1's confound closed):

```
bound & not used_held  -> E_machinery   (cut signature)
used_held & not productive -> E_world   (held entry failed -> stale)
not bound & productive -> E_world       (blind re-bind -> re-acquisition)
```

**The architectural difference, stated plainly:** the level-(c) coupling result is
established in the *clean two-cause* world. Whether the estimate's discrimination and
coupling survive the AC105 *combined-challenge* body (corruption @8192 + route move,
where corruption is a **third** cause) is a **separate, untested** question — the
three-cause integration named in §10, not a verdict on the AC105 body.

---

## 6. Established findings (claim → evidence)

### 6.1 Level (a): production closure — SUPPORTED, bounded (K3)

**Claim.** Every necessary level-(a) component {W, C, B, description, derived program}
satisfies C1–C5 and the maintained state {pointer, coordination, route memory,
decision state} satisfies S1–S4, forming a single strongly-connected
production-dependency network with no external root — *within the declared model and
operating range, under the accepted substrate convention*.

**Evidence (composing, named per component).** W (`life[:16]`, autocatalytic birth,
~766× turnover/16,384 ticks): AC10 no-W dies before any entry is allocated; AC91
blocking W-birth → W=0 → 8/8 die with the description intact at death; AC92 W=0
interrupts reconstruction while alive. C (`life[16:20]`): AC10 no-C → execution dies;
AC91/92 named cascade. B (§4). Description (bank-1 slots, succession turnover):
AC80/85/86 desc held 130/130, unmaintained degrades 23–46 and dies; AC87/89 verified
succession cycles 6–7. Program (`traces[0,:126]`, derived from description):
AC79→AC80 generic decode replaces `prog.program` bit-for-bit; AC87 order-preserving
decode. Maintained state: pointer AC86/87; coordination AC87/88/93/94/95; route memory
AC7/8/15/18/75; decision state AC12/15/75/96/99/100/104/105.

**Evidence split, stated not hidden.** AC105 composes turnover, description
persistence, reconstruction completeness, succession count, and decision operating
range in one run. Necessity-by-ablation (AC10/91/92), replacement verification
(AC87/89), and streak internalization (AC96/99/100) are **inherited from earlier
frozen versions**, not re-tested by AC105. The verdict cites the composition (AC105 +
the AC10–AC95 record); AC105 alone is the wrong study for the production claims.

**Robustness limits are NOT redesign mandates** (K3 §5): seed-dependent decision-state
economics (allowance-42 rescues 5804, retains 5603 harm); the `move_first` boundary
(5802); bimodality (reported as a lower bound). None is a production/closure failure.

### 6.2 Level (b): adaptive autonomy — ESTABLISHED (AC99–AC105)

**Claim.** The organism acquires and relinquishes route content on its own viability
conditions, and coordinates the paid reconstruction write with the paid decision
write. Wording ceiling: "acquired an instrumental priority for adaptive
relinquishment," never "wants"/"needs."

**Evidence.** AC99 (seeds 4440–4443, 5/5 gates): a 3-bit reflected-Gray-coded
relinquishment streak makes every increment a 1-bit (7-replica) transition and
resolves the maintenance/adaptation conflict; the load-bearing direction is real (the
binary control dies on 4442, Gray flips it). AC100 (seeds 4444–4447, 2×2 factorial,
6/6 gates): the **Gray encoding, not the reserve**, carries the success — the
reserve is unnecessary for Gray on the tested cohorts (Gray-no-reserve and
binary-with-reserve both satisfy the per-move adaptation criterion), and the acquired
function sustains across two successive moves. AC104 (5700–5707, 6/6) and AC105
(5800–5807, 6/6): an internally evaluated allowance-42 material budget
(`DECISION_ALLOWANCE = STREAK_N × 7`) coordinates reconstruction with the decision
write, with no challenge-time knowledge in the operational code.

### 6.3 Level (c): representational discrimination and coupling (K6 + K7, with N1 corrections)

**Claim 1 — discrimination (AC107, finals 6000–6007, 240 rows).** The maintained
one-bit cause-estimate reads E_machinery at the cut-window end 16/16 and E_world at
the first drop 16/16, with **0 post-intervention mistakes across 32 final
individuals**, transferring to the untouched family unchanged.

**Claim 2 — storage maintenance in the content sense (AC107 Q3).** Observer-discard
per-tick byte-identity 16/16 (the value is read from vulnerable maintained state, not
host state); no-cause identity 16/16 (the estimate is inert absent a cause);
vulnerable-storage audit (bit in the sticky damage stream, paid W-gated write,
excluded from `reg_from_active`).

**Claim 3 — coupling, both directions (AC108, finals 6100–6107, 288 rows, 7/7 gates).**
- *Direction 1 (maintenance → accuracy/use)*: cutting the estimate's paid write
  (`no_write`) leaves it inaccurate 16/16 in the cut and mis-used (relinquishes a
  still-valid route on 4/8 seeds where the candidate holds), with the write actually
  cut (`bel_writes == 0`, `bel_attempts == 0`).
- *Direction 2 (content → adaptation/production/viability)*: forcing E_machinery
  (`force_machinery`) reverses the adaptation (holds the stale route 16/16 where the
  candidate relinquishes 16/16) and collapses production/viability 16/16 in the move;
  forcing E_world (`scramble`) relinquishes a valid route on 4/8 seeds in the cut
  where the candidate holds.

Each effect is isolated by a single-flag intervention and matched against the
maintained candidate and externally supported fixed-threshold rivals (r2, r4).

**The survival caveat, attached to the claim (not a footnote).** The survival
advantage did not transfer: AC107 Q4 is seed-bounded (candidate 14/16 vs r4 10/16 in
the move, with a both-die seed 6002; no cut-side edge — r2 survives 16/16); AC108's
move-side survival reversal is **12/16** (candidate survives 12/16 where
`force_machinery` dies 16/16; the candidate still dies on 6100/6107), distinct from
the 16/16 *adaptation* reversal. The cut's death bite is priority-corner-specific
(`[3,0,2,1]`) and no final seed in 6000–6007 or 6100–6107 carries it. The candidate's
own move deaths are the re-acquisition boundary (relinquished correctly, failed to
re-bind in a starved economy — the AC83/AC74 path), an operating-range limit, not a
coupling failure.

### 6.4 Task identifiability (K4)

**Claim.** The two causes (E_world route move / E_machinery read cut — identical
immediate failure) produce disjoint action-observation histories on the organism's own
`(bound, used_held, productive)` triple: F1 (held-entry failure, one-sided ⇒ E_world)
and F2 (resumption-via-bound vs -unbound, two-sided ⇒ E_machinery). The separation is
a property of the task, demonstrated by a diagnostic hold-and-observe harness, not
assumed.

---

## 7. Diagnostic acquisition vs. ongoing repair (the central scoping)

This distinction is load-bearing for the level-(c) claim and must not be elided.

- **Diagnostic acquisition (what is established).** The estimate is a *paid* state
  written once at cause-onset: `bel_write` is W-gated through `ac95._cap`, costs
  energy + material per replica, and is excluded from `reg_from_active`. Frozen rows
  show `bel_writes == 7`, `bel_attempts == 1` in `cut` (one atomic 7-replica flip from
  the acquired E_world=1 to the correct E_machinery=0), and `bel_writes == 0` in
  `move` (nothing to write). `no_write` removes exactly that acquisition/update write.

- **Ongoing repair (NOT exercised).** No repair loop that keeps an already-correct
  estimate correct against continuing damage exists or runs in this world. The
  96-tick decision window is far shorter than the 1e-4/replica/tick sticky damage
  rate (the AC13 wall), so a majority flip never accumulates. "Direction 1:
  maintenance is load-bearing" therefore means **"the paid acquisition/update write
  is load-bearing"**, not "ongoing repair is load-bearing." Sustained
  representation-repair coupling is unrun and unclaimed (N1 point 3).

- **C1 (AC109, engineering, seeds 0–7, no freeze) sharpens the distinction from the
  other side.** A direct diagnostic rival that reads `(bound, used_held, productive)`
  transiently — with no stored estimate — matches the stored-estimate candidate on
  every behavioural endpoint (48/48 cells identical), and the stored estimate is pure
  cost (a 7-replica write plus ~100 redundant proactive renewals). The estimate's
  **storage is inert; its content is load-bearing** (as a content *selector*, not a
  memory). The reason is K4's perfect identifiability: the current observation already
  fully determines the cause, so there is nothing for a stored bit to remember. A
  stored estimate only earns its keep in a world where the diagnostic is not a pure
  function of the current observation — partial observation, noise, a third cause, or
  a decision that must outlive the observation that supported it.

- **C2 (design only, no run) names that world.** Occluding the `used_held` observation
  on a Bernoulli(q) fraction of channel-1 contacts makes the two causes produce an
  identical ambiguous observation `(bound=1, used_held=occluded, productive=0)` whose
  correct action differs, so only the accumulated open-gate history separates them —
  making maintained history load-bearing. This is a pending design (§10), not an
  established result.

---

## 8. Candidate failures and model-specific negatives

These are properties of the tested worlds/designs, reported with the same weight as
the positives. None is a refutation of the class; each bounds a claim.

1. **The survival advantage does not transfer (AC107 Q2/Q4).** The estimate's content
   is behaviourally causal but not survival-load-bearing on the fresh families.
2. **The move-side survival reversal is 12/16, not 16/16 (AC108, N1 point 4).** The
   candidate dies on 6100/6107 (re-acquisition boundary); `force_machinery` dies
   16/16. The *adaptation* reversal is 16/16; the *survival* reversal is 12/16.
3. **The reliability tier is not identifiable as a separable mechanism (C0), which
   supersedes the earlier "blocked, with reopening conditions" framing (K8).** Under a
   label-free criterion, "monitoring the reliability of one's own estimate" has no
   referent distinct from (a) estimating the channel's diagnostic value ε (a first-order
   world parameter) or (b) a function of the sufficient statistic (n_u, n_p) (the
   first-order cause posterior). The two are only disambiguated once the cause is
   resolved, so "reliability" is the level of a parameter in a hierarchy, not a distinct
   cognitive mechanism. The residue is a first-order question — acquire and maintain a
   graded estimate of ε when it varies — framed as parameter learning, never as
   reliability monitoring.
4. **The stored estimate adds nothing over a direct diagnostic (C1/AC109,
   engineering).** Storage inert, content load-bearing, pure cost in the un-gated
   (clean) world — this licenses nothing about worlds where the observation is
   ambiguous (C2, design-level).
5. **AC106's negative was an implementation defect, not a capacity absence (K1).** The
   update rule read `productive` and dropped `bound`; r4 had `HOLD_N == STREAK_N`;
   `scramble` was a three-way confound. The valid negative preserved: the estimate *as
   implemented* was not causally load-bearing.
6. **The AC105 `move_first` boundary (5802)** kills both arms via the re-acquisition
   path, independent of the spending rule — an operating-range limit.
7. **The retained reconstruction-level harm (5603 under `late`)** — the allowance
   reserves 42 and starves the reconstruction in an already-doomed economy; did not
   recur on finals.
8. **Negative / falsified ledger (do not inherit as capabilities):** AC11 (state-blind
   duty cycle beats adaptive arm), AC13/AC14 (self-reversing damage), AC16/17
   (gate-shape), AC97/98 (reserve withholds/starves the decision it funds), AC102/103
   (the *distinction* stands, no universal spending policy).
9. **The graded-posterior "strict dominance" over heuristics was a rival defect, not a
   property of gradedness (P2, `C4_P2_EQUIVALENCE_v1.md`).** Under C4's stationary
   two-cause model the graded posterior is computationally equivalent to an integer
   ambiguous-failure counter with matched decisive handling (`N = ceil(logit(θ)/log(4/3))`,
   exact for every θ under the matching `>=` convention — R2 corrects the original
   "LR irrational and θ rational" reasoning without changing this result):
   the float log-odds is a scaled, translated copy of the count, and C4's §10 claim that "no
   uniform counter can express that split" is false for this construction. The reported
   `graded > binary+imm` dominance is entirely attributable to one omitted decisive
   observation in the rival — `binary+imm` reset its streak on an occluded-productive contact
   instead of treating it as decisive-C — and vanishes once that observation is handled the
   same way (the fixed rival is bit-for-bit the graded policy). Calibration survives (it is
   not a dominance claim). The load-bearing objects are decisive-observation handling plus a
   counter threshold, **not** a graded register.

---

## 9. Novelty assessed against primary prior work

The prior work named in the charter — Maturana & Varela 1980 (autopoiesis), Montévil &
Mossio 2015 (organizational closure), Di Paolo 2005 (adaptivity), Butlin et al. 2023
(consciousness indicators), plus the maintenance prior art (cascades, EWC, ECC,
synaptic tagging) — is unchanged. The project adds no concept to any of them.

- **Against M&V / M&M:** the closure criterion (C1–C5, S1–S4) is a *disciplined
  application* of "closure of constraints," not a new operationalization. The
  contribution is the negative finding *about the criterion's limits* — the residual
  to a closure verdict is a named modeling judgment (J1, J4), not missing data.
  **No conceptual novelty.**
- **Against Di Paolo (adaptivity):** level-(b) is an instantiation in a toy model.
  **No theoretical novelty.**
- **Against Butlin et al. (HOT-2):** the K-series tests a concrete HOT-2 candidate at
  two tiers (discrimination, coupling) and shows it is *blocked* at the reliability
  tier. A worked instance, informative, falsifies nothing in the framework. **No
  advance on the framework.**
- **Against maintenance prior art:** reconstruction/renewal is a toy instantiation of
  occupied territory. **No absence-of-prior-art claim.**

**Honest novelty statement.** The project advances no concept in autopoiesis,
adaptivity, or consciousness science. Its legitimate claim is narrower: (i) a worked,
falsification-disciplined example in which a fully-specified simulated organism earns
a bounded production-closure verdict whose residual is a modeling judgment rather than
missing data; (ii) an established adaptive-autonomy result; (iii) the first
demonstrated causal coupling, in both directions, of an internally maintained
representation to its own maintenance machinery **in this project's lineage** — not a
field-level first, since no primary-literature search establishes empirical priority
(N1 point 8); and (iv) a reproducible catalog of structural walls (the economics wall,
the gate-shape wall, the locked-fixed-point signal wall, the reliability-
not-identifiable wall, and the sufficient-statistic wall — the graded posterior is an
integer counter in float clothing, P2/R2).

---

## 10. Pending results and open hypotheses (explicitly separated)

None of the following is an established finding. Each is a new hypothesis or an
untested continuation, and none may be cited as evidence.

- **Three-cause integration (gated, not authorized).** Does the cause-estimate's
  discrimination and coupling survive the AC105 combined-challenge body (corruption
  @8192 + route move), where corruption is a *third* cause? This is **one** candidate
  composition, warranted only if the survival/composition question is judged
  load-bearing — not the only legitimate continuation (N1 point 7; C1/C2/C3/C4/I1 are
  equally open).
- **Ongoing-repair isolation (C3).** Isolate an ongoing, load-bearing repair loop that
  keeps an already-acquired estimate correct against continuing damage — separate
  evidence from the single acquisition/update write (the AC13 wall currently makes
  this unexercised). The C2 occluded-gate task design supplies the world where the
  stored function is genuinely load-bearing.
- **Reliability tier — closed as a second-order track (C0).** Not identifiable: no
  label-free probe separates "monitoring the reliability of one's own estimate" from (a)
  estimating the channel parameter ε or (b) the first-order cause posterior. The residue
  is a first-order acquisition/maintenance question (estimate ε when it varies and beat a
  stale/supplied weight), framed as parameter learning, never as reliability monitoring.
- **Uncertainty, re-scoped by P1/P2/P4/AC113 (R1) and P2's proof correction (R2).** The
  C4 graded-posterior comparison is reproducible (P1). P2 resolved the sufficient-
  statistic rival — under C4's stationary model the graded posterior is an integer
  ambiguous-failure counter in float clothing, so the "graded strictly dominates the
  strongest heuristic" advantage is **removed** (a rival defect); calibration survives;
  and R2 corrected the *reasoning* of that equivalence (the "irrationality" argument was
  false) while making the result **stronger** — `N = ceil(logit(θ)/LR)` is exact for
  every θ under the matching `>=` convention. P4 then generalized to heterogeneous
  likelihood ratios (residual yield ε), making the sufficient statistic a two-dimensional
  weighted count `(n_u, n_p)`. AC113 (P6) carried that to organism scale, and the outcome
  — corrected by R1 — is **no demonstrated advantage**, not equivalence: at the fixed
  engineering-selected parameters the maintained two-counter is statistically
  indistinguishable from the single counter on income (seed-level sign-flip p ≈ 0.71 /
  0.63, n = 8, median difference 0, one collapse seed driving the negative mean), and the
  candidate is worse on survival, expenditure, and cut false-relinquish. The
  "nonsignificance ⇒ equivalence" reading is withdrawn; a genuine equivalence claim would
  need a prespecified margin and a power analysis the sample does not support. The
  load-bearing object remains decisive-observation handling plus a counter threshold, not
  a graded register.
- **Composition without conflating uncertainty (I1) — evaluated (AC111).** The direct
  channels are clean (the estimate bit is excluded from `reg_from_active` under a live
  reconstruction; the spending budget never starves reacquisition); full composition
  retains two failed gates (G3/G5 12/16) as a named seed-dependent behavioural
  interference, survival-neutral. The three-cause integration (corruption as a third
  cause) remains the open composition question.
- **The re-acquisition boundary** (candidate move deaths 6100/6107, 6002) — an
  operating-range question, untested as a mechanism.

---

## 11. Claim-discipline summary (wording ceilings)

- "Acquired an instrumental priority for adaptive relinquishment" — never "wants"/
  "needs."
- "Meets the finite closure criterion within the declared model and operating range,
  under the accepted substrate convention" — never "autopoietic" unqualified, never
  "alive."
- "Causally coupled in both directions, each isolated by a single-flag intervention,
  with the survival caveat attached" — never "load-bearing for survival" in this
  world.
- "First demonstrated in this project's lineage" — never a field-level first.
- Death must never improve an average: survival is a bimodality-aware lower bound,
  reported alongside planned-denominator activity.
- Seeds are the replication unit; engineering seeds are excluded from every final
  sample; survival is never gated to a uniform N/N.

---

## 12. Sources

`CLOSURE_VERDICT_v1.md` (K3), `DEFINITIONS_CHARTER_v2.md` (K2), `K9_SYNTHESIS_v1.md`,
`K8_DISPOSITION_v1.md`, `TASK_IDENTIFIABILITY_v1.md` (K4),
`AC107_RESULTS_v1.md` / `AC107_PROTOCOL_v1.md` / `AC107_ENGINEERING_v1.md` (K5/K6),
`AC108_RESULTS_v1.md` / `AC108_PROTOCOL_v1.md` (K7), `AC106_ERRATA_v1.md` (K1),
`N1_CORRECTIONS_v1.md`, `P3_CORRECTIONS_v1.md`, `A1_REALIZATION_LEDGER_v1.md`, `A2_BOUNDARY_VERDICT_v1.md`,
`AC109_ENGINEERING_v1.md` (C1), `C2_TASK_DESIGN_v1.md`, `C4_TASK_DESIGN_v1.md`,
`C4_REPRODUCIBILITY_v1.md` (P1), `C4_P2_EQUIVALENCE_v1.md` (P2),
`P4_COGNITION_CONTINUATION_v1.md` (P4), `AC105_RESULTS_v1.md` /
`AC105_PROTOCOL_v1.md` / `AC105_ERRATA_v1.md`, `AC100_RESULTS_v1.md`,
`AC99_RESULTS_v1.md`, `AC104_RESULTS_v1.md`, `AC10_RESULTS_v1.md`,
`AC113_RESULTS_v1.md` / `AC113_PROTOCOL_v1.md` (P6), `R1_AC113_REANALYSIS_v1.md`,
`R2_P2_PROOF_CORRECTION_v1.md`, `AC114_RESULTS_v1.md` / `AC114_PROTOCOL_v1.md` (A3),
`A4_EXCHANGE_VERDICT_v1.md`, `C0_FEASIBILITY_v1.md`,
`EVIDENCE_INDEX_v2.md`, `AUTONOMY_RESEARCH_STATUS.md`, `CONSCIOUSNESS_ROADMAP_v1.md`.

This document is derived and is not hashed into any study's `pre_run_snapshot.json`.
