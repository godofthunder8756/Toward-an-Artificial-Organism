# scarcity_v2: pressure-and-representability certificate for C3 retention and routing (analytic protocol draft)

**Status: DRAFT, frozen-ready, NOT RUN.** This is an analytic protocol only. It is a C3 card
(selection, access and routing below sufficiency), so it falls under Aidan's standing
approval for analytic and engineering work. It contains **no C4 component**: there is no
evaluator, no meta-d′, no diagnostic-channel test, and no S3 signature. Anything that drifts
into evaluating the agent's own state is out of scope and goes to the C4-gated designs in
`emergence_conditions_v2.md` §4.

- **Written:** 2026-10-20 (EDT) by Research Delegate for the ACI Research Specialist,
  for Aidan Ahern.
- **Repo:** `/workspace/repo` is untouched.
- **Execution:** when approved for execution, run it in `/workspace/scratch/scarcity_v2/`
  (outside the repo).
- **Basis:**
  - `SCARCITY_GAP_v1.md` §5 and §7.1–7.2, on branch `origin/elminster/loving-ptolemy-ityj4l`
    @ `33fa803`, read with `git show`.
  - Astra consultation #4 (`/workspace/astra_consult_1.md`).
  - The independent replay `/workspace/scratch/scarcity_replay/replay.py`, which matches
    every branch §5 headline number.
- **No consciousness claim.** Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.

---

## 0. What this certificate is, and is not

Astra #4 defines the task as a "pressure & representability certificate (which
conditions reward role, which remove pressure, what interventions identify it), with
sufficient-capacity and unpaid-upkeep controls, adaptive selection comparator, charge
selector state/action history/bookkeeping to budget."

**It answers three questions:**

1. **Pressure.** Under which conditions does the matched-budget optimum strictly reward
   state-dependent **retention** (what to keep and maintain) or **routing** (what to send to
   which consumer)? This is measured against rivals that are denied that dependence.
2. **Removal.** Under which conditions does that reward vanish, as the controls predict?
3. **Identification.** Which later interventions would identify the role in a developed
   system? This step only computes the response pattern the optimum predicts for each
   intervention. Nothing is run on any learner.

**It does not answer:**

- **Q-LEARN.** Whether any learner acquires the role is out of scope.
- **ORIGIN.** Nothing here can be judged ACQUIRED.
- **Q-CAUSE in any developed system.**
- **Q-NECESSITY beyond the declared rival classes.**

**Binding statement.** An optimal codebook is not evidence of acquired organization
(Astra #4: "Optimal codebook != acquired organization"). A positive certificate establishes
only that the declared world, at the declared budget, *rewards* the role, and that the
policy class *can represent* it (Q-EXIST). Sufficient capacity *permits* the role but does
not guarantee that it is acquired or causally organized (Astra #4, verdict (a)).

### 0.1 Explicitly out of scope

The following are **excluded** from scarcity_v2. Each is GATED or DESIGN-ONLY in
`emergence_conditions_v2.md` §3, and none of them may be added to this card:

- the social-modelling pressure. Its self-evaluation part is C4, and a new agent class
  would count as a new architecture family and go to Aidan;
- the curriculum or developmental-staging pressure. It needs a separate card, and any
  training needs separate approval;
- the intrinsic-motivation pressure, which is C4;
- every C4 component: diagnostic channel, evaluator, meta-d′, and the S3 signature;
- the **self-induced-uncertainty** quantity of `SCARCITY_GAP_v1.md` §5. It is **UNDEFINED
  and EXCLUDED**. It is not replayed, not reconstructed and not reported. The .md does not
  define it, and the Specialist ruled against reconstructing a definition.

---

## 1. World family W2 (all parameters are proposed freeze values)

Each episode runs encoding, then an optional upkeep interval, then one query.

| Component | Definition | Levels (proposed freeze) |
| --- | --- | --- |
| Items | `x ∈ {0,1}^3`, i.i.d. uniform | fixed |
| Evidence `EV` | **clean**: each item observed exactly. **graded**: two independent looks per item, each correct w.p. `a`. The per-item sufficient statistic is the count of 1-looks ∈ {0,1,2}. | clean; graded with `a = 3/4` |
| Cue | `c` on {0,1,2}, observed at encoding. **PRIMARY: uniform**, `P(c) = (1/3, 1/3, 1/3)`. This is the analysis that decides. The v1 replay used this definition. | uniform (primary); sensitivity sweep in §6.4 |
| Consumers `CON` | **1**: a single consumer whose query is `q = c` w.p. `v`, otherwise uniform on the other two items. **2**: consumer `j ∈ {A,B}` is drawn w.p. 1/2 after encoding (not known at encoding). A queries `c` w.p. `v`; B queries `c+1 mod 3` w.p. `v`; otherwise each is uniform on the remaining items. | 1; 2 |
| Channel `CH` (CON=2 only) | **full**: the consumer reads the whole state. **limited**: consumer j reads only a message `μ_j(m) ∈ {1..L}` and decodes from `(μ_j, q)`. Storage is set **ample** (`K ≥ |supp S|`) in this condition, so that only the channel binds. This tests Astra's verdict (d). | full; limited with `L = 2`; channel-sufficient `L = |supp S_j|` (control) |
| Upkeep `UP` | **unpaid**: the state persists. **paid**: before the query, each state is maintained or not. An unmaintained state is replaced, with hidden probability `δ`, by a uniformly random state of the codebook. Budget type is PROPOSED in §12: an integer cap `B_up` on maintained states; the earlier expected-mass `β` is a superseded draft. The agent observes nothing about decay (there is no diagnostic channel, because that would be C4). | unpaid; paid with `δ = 1/2`; `B_up` per §12 (PROPOSED) |
| Answer / opt-out | Answer: reward 1 if correct, 0 if wrong. Opt out: sure reward `r`. | `r ∈ {5/8, 3/4}` |
| Cue validity | `v` | `{1/3, 3/4}`; 1/3 is uninformative (control) |
| Total state budget `K` | **Every** distinct internal state the policy can occupy at query time (§2) | `1 … K_supp` for each world (§3) |
| Regime `NS` (stage B only) | **stationary**; or **switching**: consumer A's map switches between `c` and `c+1` with hidden hazard `h` per episode. This is where the adaptive comparator is non-trivial. | stationary; switching with `h = 1/4` |

**Cells.** Stage A is every combination of EV × CON × CH × UP × v × r × K, restricted to the
admissible combinations (CH only applies at CON=2, and limited CH has ample K). The full
list of cells, with their K ranges, is generated from the frozen source **before** any
value is computed, and its hash is recorded. Every cell is reported.

---

## 2. Budget accounting: what K charges

Astra #4: "charge selector state/action history/bookkeeping to budget". `K` is the number
of **distinct internal states** the policy can be in when the query arrives. It is
charged for every one of the following:

- **content** (the stored codeword);
- **access or opt-out flags**, if they are not implied by the codeword;
- **upkeep bookkeeping**, e.g. whether this state was maintained. Codeword × flag counts
  as distinct states;
- **selector state**, e.g. a register recording which consumer or regime is believed
  current;
- **action and outcome history**, i.e. any register carried across episodes in stage B;
- **counters and timers**.

**Not charged:** the policy's fixed parameters (its encoder, decoder and update tables),
which are the same for every class. The **same accounting applies to every class**,
including the rivals. A rival that "gets a free history" is not admissible.

---

## 3. Sufficiency is defined by support, not by entropy

Per Astra #4, verdict (a): `ρ_H = log K / H(S) ≥ 1` does not imply lossless storage, because
entropy is not log support.

- **Definition.** `K_supp(world)` is the number of distinct decision-relevant classes,
  i.e. the minimum number of codewords at which the unconstrained optimum is attained.
  For example, it is 8 in the clean single-consumer world. In the graded world it is
  computed exactly.
- **Sufficient-capacity control:** `K ≥ K_supp`.
- **Reported, descriptive only:** both `ρ_supp = K / K_supp` and `ρ_H`. Neither is used
  in any gate.

---

## 4. Policy classes (all at the same total K, same accounting)

| Class | What it may do | Role it is denied |
| --- | --- | --- |
| `full` | Any deterministic encoder, upkeep allocation, message map and decoder within K. Upkeep is deterministic under the integer cap `B_up` (§12, PROPOSED). If Astra selects the expected-mass alternative instead, randomization is allowed only to meet that budget exactly. | none |
| `cue_blind` | Encoder and upkeep ignore the cue | goal-dependent **selection** |
| `static_access` | Opt-out pattern per query is identical across all states | state-dependent **access** |
| `static_route` (CON=2, limited CH) | `μ_j` carries a fixed, input-independent subset of item information to consumer j | state-/cue-dependent **routing** |
| `fixed_upkeep` (paid UP) | Maintenance decision independent of state and input (a fixed input-independent set or duty schedule of `B_up` maintained states) | content-dependent **maintenance allocation** |
| `random_yoke` (paid UP) | The upkeep schedule is copied from `full`'s marginal maintenance rate, but assigned at random across states | allocation-content coupling (it is a yoke control) |
| **`adaptive_select` (strongest rival)** | Allocation and routing may depend on the cue **and** on a history register of size `H`, updated from the agent's own past queries and outcomes (label-driven) or from unlabeled agreement (R-A1). The total states charged are `K_content × H ≤ K`. The best `H` is chosen per cell. | none in principle. This is the conventional adaptive-selection explanation. If it matches `full`, the role is REDUCED to adaptive selection at parity. |

**Notes on the classes.**

- `adaptive_select` is the **strongest simpler rival** (constitution v3 Q4). In the
  stationary regime, history is uninformative, so it is predicted to equal the best
  `H = 1` member of `full`. This prediction is a self-test of the implementation. In
  the switching regime (stage B), it is the real comparator.
- `no_opt` (ideal-observer wagering, as in the v1 certificate) is reported for
  continuity, but it is not a gate.

---

## 5. Measured quantities (exact Fractions)

**Frozen definitions, verbatim from the independent replay** (`/workspace/scratch/scarcity_replay/replay.py`, which matched the branch exactly). The wording below is frozen:

> **Access value** = `V_full − V_static`, where `static` = the best codebook of size
> min(K, |rows|) drawn from codewords that **all share one opt-out pattern** (the same set of
> queries answered with `-`). The best such pattern is chosen per cell.
>
> **Selection value** = `V_full − V_cue_blind`, where `cue_blind` = the best codebook whose
> **encoder sees the items only, not the cue**. Its value is computed with the
> cue-averaged query distribution per item vector.
>
> `V_class` = `E_{x,c} max_{w ∈ codebook} Σ_q P(q|c) · u(w_q, x_q)`, where `u` = 1 for a
> correct answer, 0 for a wrong one, and `r` for opt-out. Each memory state is identified
> with its codeword, which gives an action per query.

In this card, `ACC` and `SEL` below are exactly these differences, extended to W2's
additional factors with the same class restrictions. No other "access" or "selection"
quantity is defined.

All differences are computed per cell at equal K.

| Quantity | Definition | Pressure for |
| --- | --- | --- |
| `SEL` | `V_full − V_cue_blind` | retention selection |
| `ACC` | `V_full − V_static_access` | state-dependent access |
| `ROUTE` | `V_full − V_static_route` | routing across consumers |
| `UPK` | `V_full − V_fixed_upkeep` (and `− V_random_yoke`) | maintenance allocation |
| `ADAPT` | `V_full − V_adaptive_select` | whether the role exceeds the conventional adaptive explanation (REDUCTION input only) |

**Exactness.** Arithmetic uses `fractions.Fraction`, converted to common-denominator
integers for search, and every incumbent is re-evaluated in Fractions.

**Search method.**

- **Exhaustive** codebook enumeration where `Σ_K C(N_codewords, K) ≤ 5·10^7` per cell.
- Otherwise, **exact branch-and-bound** with a valid per-input upper bound, as in the
  branch method. A cell's value is **certified** only when lower bound = upper bound.
- Upkeep allocation under budget `B_up` (integer, PROPOSED). Given a codebook, choosing which states to maintain is a finite exact search. Under the expected-mass alternative (not primary), the allocation would instead be solved as an
  exact rational LP over maintenance probabilities (a fractional knapsack over
  states, sorted by marginal value per unit of maintained mass). Upkeep randomization is
  allowed only for this purpose.
- Stage-B values are the stationary values of the joint chain (regime, history register),
  solved as an exact rational linear system.

---

## 6. Pre-declared outcomes and decision rules

### 6.1 Per cell

Each cell receives exactly one label:

- **PRESSURE(X).** The quantity X is > 0 (certified). The pre-declared intervention
  responses (§7) are computed for **every** optimal codebook in the cell (all optima, up to
  item symmetry).
  - **ROBUST-ROLE:** the response pattern holds across all optima.
  - **PERMITTED-ROLE:** it holds in some optima only. The replay already found
    non-unique optima, e.g. `00- 01- 1--` vs `0-- 10- 11-` at v=1/3, r=3/4, K=3.
- **NO-PRESSURE(X).** X = 0 (certified).
- **UNRESOLVED.** Bounds have not closed within the frozen time limit, which is
  the per-cell limit PROPOSED in §12 (not frozen). Neither timeout nor solver luck is
  certification (constitution v3).

### 6.2 Control predictions (certificate self-tests, not discoveries)

| Control | Prediction | If violated |
| --- | --- | --- |
| Sufficient capacity (`K ≥ K_supp`), unpaid upkeep, full channel | `SEL = ACC = 0` (Blackwell) | **Implementation error.** Halt and debug before any other cell is read. |
| Unpaid upkeep | `UPK` is undefined (logged as 0); `random_yoke` = `full` | Implementation error |
| Uninformative cue (`v = 1/3`) | `SEL = 0` and `ROUTE = 0` | Implementation error |
| Channel-sufficient (`L = K_supp,j`) with ample K | `ROUTE = 0` | Implementation error |
| Stationary regime | `ADAPT = 0`, with the best `H = 1` | Implementation error |
| Replay | The CON=1, clean, unpaid, `r ∈ {5/8, 3/4}`, `v ∈ {1/3, 3/4}` slice reproduces the v1 values from `replay_results.json` | Implementation error |

Under Astra's verdict (a), these controls show that the **pressure** is removed, *not* that
the role cannot be acquired there.

### 6.3 Family-level conclusions (pre-declared; no single favourable cell counts)

For each role X ∈ {SEL, ACC, ROUTE, UPK}:

- **X-PRESSURE-SUPPORTED** requires all three of:
  - PRESSURE(X) in at least one certified cell in **each** declared `ρ_supp` bin below 1.
    The bins are (0, 1/4], (1/4, 1/2] and (1/2, 1).
  - NO-PRESSURE(X) at every control.
  - For ROUTE, PRESSURE in the **ample-storage, limited-channel** condition. This is the
    direct test of verdict (d).
- **X-PRESSURE-ABSENT:** NO-PRESSURE(X) in every certified scarcity cell, with ≤ 10% of
  cells UNRESOLVED.
- **X-UNRESOLVED:** anything else.

**REDUCTION input (stage B only).**

- If `ADAPT = 0` in every switching-regime cell where X shows pressure, X is logged as
  **REDUCTION-candidate: adaptive selection**. Per R-A1 this includes unlabeled
  agreement.
- If `ADAPT > 0` (certified) in any declared cell, X is logged as **NOT-REDUCED-vs-adaptive
  at parity, in that cell**.

Neither result says anything about ORIGIN.

### 6.4 Pre-registered cue-distribution sensitivity sweep (describes, does not decide)

The primary analysis uses the uniform cue (§1). A sensitivity sweep reruns stage A1, and
stage A2 cells that are PRESSURE in the primary analysis, under **two non-uniform cue
distributions**:

- **S1:** `P(c) = (1/2, 1/4, 1/4)` (mildly skewed);
- **S2:** `P(c) = (2/3, 1/6, 1/6)` (strongly skewed).

Rules:

- Sweep results are **reported per cell next to the primary analysis**.
- They **may describe** how the pressure magnitudes and the set of optimal codebooks
  change.
- They **may not decide** any §6.1–6.3 label, family-level conclusion, REDUCTION input or
  ledger update.
- A primary-versus-sweep disagreement is logged as a robustness note only.
- All controls (§6.2) are re-checked under each sweep distribution, as implementation
  self-tests. A violation there is still an implementation error.

---

## 7. Interventions that would later identify each role (predicted from the optimum; not run on any learner)

For every PRESSURE cell, the certificate computes, for each optimal codebook, the expected
change in reward and in action distribution under the interventions below. These
predictions are the **targets** a later, separately approved Q-CAUSE study would test in a
developed system, with no decoder needed.

| Role | Intervention (at query time or during upkeep) | Predicted signature in a role-bearing optimum | Rival's prediction |
| --- | --- | --- | --- |
| SEL | **Cue swap after encoding**: the query distribution follows a different cue than the one encoded | Loss concentrated on items the swapped cue makes likely; size equals the certified `SEL` contribution | `cue_blind`: no change |
| ACC | **State transplant between matched inputs** that share content but differ in access pattern | Directional opt-out errors on exactly the queries whose access differs | `static_access`: no opt-out change |
| ROUTE | **Message swap between consumers** (`μ_A ↔ μ_B`) | Both consumers degrade, on their cue-predicted items | `static_route`: degradation only on fixed items, independent of cue |
| ROUTE | **Channel-limit change** (`L: 2 → 1`) with storage fixed | Routing re-prioritizes toward the higher-mass consumer-item pairs | `static_route`: uniform loss |
| UPK | **Covert maintenance withdrawal** from one state | Loss concentrated on queries that state serves, across **all** consumers using it | `random_yoke`: loss independent of content relevance |

These are representability predictions about the optimum (Q-EXIST). A learner showing them
would still need the ORIGIN controls (no supplied slots, targets, labels or protected
histories) and the ROLE verification described in `emergence_conditions_v2.md` §1.

---

## 8. Stages and order

- **A1.** CON=1, clean and graded, unpaid and paid. This is the direct extension of the
  branch §7.1–7.2. Run the replay test first.
- **A2.** CON=2, full channel, and limited channel with ample storage. These are the
  routing and verdict-(d) cells.
- **B.** The switching regime (`NS`), solved only for the cells that are PRESSURE in A1
  and A2. This is the `adaptive_select` comparison.
- **Stop rule.** If the A1 controls fail, stop: that is an implementation error. B is not
  run if A1 and A2 find no pressure. In that case B has nothing to compare, and the
  result is X-PRESSURE-ABSENT for all X.

**Cost estimate.** Qualitative, since nothing has been run: minutes to hours of CPU
in total, using stdlib plus numpy. The graded worlds have up to 27 codewords per consumer.
The `K_supp` of the graded single-consumer world is up to 27, so mid-K cells need
branch-and-bound rather than enumeration. That is where UNRESOLVED cells are most likely.

---

## 9. Thirteen admission answers

| Q | Answer |
| --- | --- |
| Q1 | C3 bounded prerequisite: under which conditions does the matched-budget world reward state-dependent retention and routing, and which conditions remove that reward? It also touches the O0/N1 bridge via paid upkeep. |
| Q2 | One question: in W2, does the `full` optimum strictly exceed every role-denied class at equal total state count, below support sufficiency, and including routing at ample storage with a limited channel, while all controls show zero? |
| Q3 | Defeated if any control is violated (that is an implementation error, so the card is invalid until fixed). The claim of pressure is defeated for role X if X-PRESSURE-ABSENT holds (§6.3). Pressure is reduced to adaptive selection if `ADAPT = 0` wherever X shows pressure. |
| Q4 | The strongest simpler explanation is `adaptive_select` at equal total K, with selector, history and bookkeeping charged. Also: `cue_blind`, `static_access`, `static_route`, `fixed_upkeep`, `random_yoke`, and Blackwell sufficiency at the controls. |
| Q5 | Frozen evidence that makes this necessary rather than a repetition: `SCARCITY_GAP_v1.md` §5 (fixed-K, clean, single consumer only; independently replayed to an exact match); Phase III/III-B (`PHASE3_VERDICT_v1.md`, `PHASE3B_R10_CERTIFICATION_v1.md`), where capacity bound only shallowly; Phase II (`BRIDGE_PHASE2_VERDICT_v1.md`), where allocation reduced to a threshold with one cue; Astra #4 verdicts (a) and (d). |
| Q6 | After success: use the PRESSURE cells and their §7 intervention predictions to draft a separately approved prospective Q-LEARN protocol at matched budget, with this optimum as the R10-style ceiling. ORIGIN controls are pre-declared there. |
| Q7 | After failure (pressure absent): park C3 retention/routing in W2 with an exact reason, and move to distributed-information and coordination worlds (verdict d), or to the staging test (`emergence_conditions_v2.md` §3.2). After an unresolved result: close the effort, preserve the open cells, and do not extend the time limit post hoc. |
| Q8 | Minimum apparatus: analytic, i.e. exact enumeration, branch-and-bound and a rational LP. No neural model, no organism. |
| Q9 | Organizational cognition: whether a role is rewarded and representable. Not engineering advantage; the value gaps are reported but are not the claim. |
| Q10 | Claim ceiling, §10. |
| Q11 | Layer C3 (selection, access, routing). Still unsupported: Q-LEARN, ORIGIN, and Q-CAUSE in any developed system. Also unsupported, and out of scope: any C4 role. |
| Q12 | O0/N1 (paid persistence) via the paid upkeep condition; the O3 maintenance → content arrow, in optimal-policy form only. Supplied: the world, the capacity, the decay process, the budget and the consumer structure. |
| Q13 | X-PRESSURE-SUPPORTED updates the C3 ledger: "ceiling" gains "rewarded below support sufficiency in W2", and "next_falsifier" gains the §7 interventions. X-PRESSURE-ABSENT adds a collapse-ledger entry for W2. ROUTE at ample storage resolves Astra's verdict (d) for W2 either way. An `ADAPT = 0` result logs REDUCTION-candidate: adaptive selection. |

---

## 10. Claim ceiling

**The strongest wording a fully positive result can earn:** "In the finite world W2, at
equal total state count (with selector state, history and bookkeeping charged), the optimal
policy strictly rewards state-dependent [selection / access / routing / upkeep allocation]
over the declared role-denied classes. This holds in every declared ρ_supp bin below
support sufficiency and, for routing, also at ample storage with a limited channel. The
reward vanishes at every declared control. The pattern [is / is not] reproduced by an
adaptive-selection comparator at parity. Optimal policies predict the §7 intervention
signatures [across all / some] optima."

**NOT established:**

- that any learner acquires the role (Q-LEARN; ORIGIN stays UNRESOLVED);
- that any developed system uses it (Q-CAUSE);
- necessity beyond the declared classes;
- robustness outside W2;
- any C4 evaluator;
- any self-model;
- anything about consciousness.

An optimal codebook is not acquired organization.

---

## 11. Freeze checklist (before execution)

1. Only after the Specialist and Astra have ruled on §12: freeze this document's grid (§1)
   and its rules (§§2–6). Record the hash. **Nothing is frozen now.**
2. Write the source code in `/workspace/scratch/scarcity_v2/`, independent of the branch
   script. Commit nothing to the repo.
3. Generate the cell list. Hash it.
4. Run the replay test and the control self-tests first. Halt if any fails.
5. Run A1, then A2, then B, as gated by §8. Report every cell.
6. Run an independent second implementation, or a brute-force cross-check, for every
   PRESSURE cell with `K ≤ 4`.

**Open items to settle at freeze:** see §12. They are proposed, not chosen; they go to
the Specialist, and from the Specialist to Astra.

---

## 12. Parameter proposals: PROPOSED, NOT FROZEN

Nothing in this section is chosen. Each primary value and secondary grid is a proposal for
the ACI Research Specialist to take to Astra. Where a v1 or branch value exists, it is
preferred.

| Item | PROPOSED primary | PROPOSED secondary grid | One-line justification |
| --- | --- | --- | --- |
| Look accuracy `a` (graded EV) | **3/4** | {3/5, 5/6} | 3/4 reuses a v1 grid value (v ∈ {1/3, 1/2, 3/4}), keeping denominators shared. 3/5 puts the two-agreeing-looks posterior (9/13) below r = 3/4, so access patterns become non-trivial. 5/6 (posterior 25/26) approaches the clean world. |
| Budget type | **Integer total state count `K`**: a hard cap counting every internal state (content, flags, selector, history, bookkeeping). Paid upkeep is an **integer** per-episode cap `B_up` on the number of maintained states, also hard. | `K ∈ {1 … K_supp}` (v1 used 1..8); `B_up ∈ {1, ⌊K/2⌋}` | v1's `K` was a hard integer count of states. Integers keep the problem a finite exact search and leave no fractional loophole. The earlier expected-mass `β` is withdrawn as primary. |
| Per-cell time limit | **10 CPU-minutes** per cell; over that, the cell is UNRESOLVED | {3, 30} CPU-minutes, reported only as the count of UNRESOLVED cells at each limit, never used to relabel cells after the fact | The v1 certificate ran in about 3 min CPU in total, and the replay ran 72 cells in 49 s. 10 minutes per cell leaves headroom for graded and branch-and-bound cells. Timeout is never certification. |
| History-register size `H` (stage B, adaptive comparator) | **2** | {1 (degenerate control), 3} | H = 1 has no memory, so `adaptive_select` collapses to `full` and ADAPT = 0 by construction. H = 2 is the smallest register that can track the two-state switching regime, the first value at which the comparison is not decided trivially. 3 tests whether one more state changes the verdict. H is charged inside `K`, so `K_content × H ≤ K`. |

