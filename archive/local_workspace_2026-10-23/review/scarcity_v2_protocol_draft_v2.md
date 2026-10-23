# scarcity_v2 protocol draft v2: revisions after Astra RESPONSE A ("DO NOT FREEZE")

**Status: DRAFT. NOT FROZEN. NOT RUN.**

- **Layer:** C3 only (retention, access, routing).
- **Supersedes:** `scarcity_v2_protocol_draft.md`, which is left untouched as the record Astra reviewed.
- **Written:** 2026-10-20 (EDT) by Research Delegate for the ACI Research Specialist, on behalf of Aidan Ahern.
- **Source:** `/workspace/astra_consult_5_raw.md`, "RESPONSE A". Part 1 of the draft reached Astra with garbled non-ASCII characters (see §15).
- **No search was executed.** The few numbers below are hand derivations stated with their arithmetic, so a reviewer can check them.
- **Repo:** `/workspace/repo` is untouched.
- **No protected controller or register is introduced** (§15, F2).
- **Claims:** no consciousness claim. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate. **ORIGIN: untested** throughout.

---

## 0. Changes from v1 of this draft

| # | Astra RESPONSE A point | Change here |
| --- | --- | --- |
| 1 | Graded evidence keeps access value at sufficient storage (`ACC = 3/32` at a=r=3/4) | Hand-checked; **confirmed** (§5.2). The zero-ACC control is restricted to **clean evidence, unpaid upkeep, K ≥ K_dec** (§6). Sufficiency-level access is reported separately as `ACC_suff`, and is labelled ordinary selective prediction under observation uncertainty. |
| 2 | Upkeep had two incompatible readings, so UPK might be identically zero | **One definition**: per-field durable writes, chosen at encoding, applied over one decay epoch, with erasure decay (§2.5). **UPK is shown analytically to be non-zero** (§5.3). A B_up grid is proposed (§12). |
| 3 | K_supp conflated posterior support with decision sufficiency; decay sampling was unspecified | K_lossless and K_dec are now separate (§3). Decay acts per field by erasure and never samples codebook states or slots (§2.5). |
| 4 | Several §7 signatures do not follow | Every signature is re-derived (§8). Three are **dropped**: message swap, L-reduction as a lesion, and the uniform-loss/yoke predictions. The cue-swap signature is **fixed**: it no longer claims "= SEL", and keeps only the proved cue_blind identity. Access transplant gets an **operational definition**. Upkeep withdrawal gets a **closed form**. |
| 5 | Add a scaffold accounting table | Added (§9). |
| 6 | The equal-state adaptive rival is necessary but does not test acquisition | Stated (§10). The comparator is **repaired** (§4.2): it was "unrestricted-looking", and now has a specified update restriction, frozen feedback, update order, initialization, and a value definition valid with multiple recurrent classes. |
| — | Outcome semantics, ROUTE bin impossibility, ≤10%-unresolved absence rule, per-role controls, stop rule | §7 is rewritten to Astra's ADMIT / REJECT / UNRESOLVED. It separates "pressure absent" from "pressure present but insufficiently widespread". Absence needs every cell certified. ROUTE is gated over channel-limit bins. |
| — | §12 rulings | a = 3/4 primary. (a=3/5, r=3/4) is an **all-abstain null control**. 5/6 is secondary. Integer K. 10 CPU-min per cell with declared accounting. H = 2 with secondary {1, 3}, applied **only to the repaired comparator** (§4.2, §12). |

---

## 1. Scope

**In scope:** C3 pressure and representability for selection (SEL), state-dependent access (ACC), routing across consumers (ROUTE) and content-dependent upkeep allocation (UPK), within declared finite policy classes.

**Out of scope, carried from v1 §0.1:**

- The social-modelling, curriculum/staging and intrinsic-motivation pressures. Each is GATED or DESIGN-ONLY in `emergence_conditions_v2.md` §3.
- Every C4 component: diagnostic channel, evaluator, meta-d′, and S3.
- The **self-induced-uncertainty** quantity, which is **UNDEFINED and EXCLUDED**.

**Scope limits, per Astra:**

- Remembering upkeep actions and ordinary filtering are not inherently C4.
- Paid protection of memory fields **does not establish an O3 machinery-maintenance bridge** (RESPONSE A §3). No O3 claim is made.

---

## 2. World family W2′

### 2.1 Items, evidence and cue

| Component | Definition |
| --- | --- |
| Items | `x ∈ {0,1}^3`, i.i.d. uniform |
| Evidence `EV` | **clean**: each item is observed exactly. **graded**: two looks per item. **Frozen independence assumption:** looks are i.i.d. given the item, each correct w.p. `a`, and independent across items. The per-item sufficient statistic is the count of 1-looks, `n_i ∈ {0,1,2}`. |
| Look accuracy `a` | **3/4 (primary)**. 5/6 is secondary. **(a=3/5, r=3/4) is the all-abstain null control** (§5.2). The decision role of each value is frozen in §12. |
| Cue | `c ∈ {0,1,2}`, observed at encoding. **Primary: uniform.** The pre-registered sensitivity sweep is carried from v1 §6.4: (1/2,1/4,1/4) and (2/3,1/6,1/6). The sweep describes but does not decide. |
| Query map | For a single consumer, `q = c` w.p. `v`, otherwise uniform on the other two. `v ∈ {1/3 (uninformative control), 3/4}`. |
| Reward | Answer: 1 if correct, 0 if wrong. Abstain (`-`): `r ∈ {5/8, 3/4}`. |

### 2.2 Memory fields

The agent's memory has **three answer fields** `f_0, f_1, f_2`. Field `f_q` holds the action for query `q`: one of `0`, `1` or `-`. This is the codeword language of the v1 replay; no new component is added. During the upkeep interval each non-`-` field also carries a **durability mark**, D (durable) or F (fragile) (§2.5). The mark is a physical property of how the field was written, and it is charged in K.

### 2.3 Consumers and channel

These are carried from v1 §1.

- **Two consumers:** A queries `c` w.p. `v`; B queries `c+1 mod 3` w.p. `v`.
- **Channel:** full, or limited to `L ∈ {1, 2}` symbols per consumer with ample storage, or channel-sufficient (`L` ≥ that consumer's K_dec) as the control.

### 2.4 State budget K: per-phase reachable configurations

Following Astra, K counts **reachable joint configurations**, not the sum of register sizes. Memory must fit **at every decision phase**:

- **E (encoding):** inputs are present. No carried memory is needed in stage A.
- **I (upkeep interval):** field values plus durability marks.
- **Q (query):** field values after decay.
- **Stage B only:** the history register, jointly with E, I and Q (§4.2).

**Constraint:** the number of reachable configurations is ≤ K in each phase separately. K is an integer.

- **Duplicates.** A configuration *is* its field values, plus marks in I and history in stage B. Two "states" with identical configurations are the same state. Duplicates are merged, so they cannot add capacity.
- **K = 1 (the zero-cap case).** There is one configuration per phase. The encoder must therefore be constant. A fragile stored bit would create two Q-phase configurations, so any stored bit must be durable (paid) or `-`.
  - **Result:** for `r ≥ 1/2`, every class's optimum is "abstain on all queries", with V = r.
  - **Consequence:** every role difference is 0. K = 1 cells are reported as **DEGENERATE**, not as evidence.

### 2.5 Upkeep: the single coherent definition

| Element | Definition |
| --- | --- |
| Timing | Allocation is chosen **at encoding (phase E)**, with exactly the encoder's information (looks, cue). There is **no later allocation decision**, so no memory is needed to carry an allocation plan. |
| Operation | Each non-`-` field is written either **durable (D)**, costing 1 upkeep unit, or **fragile (F)**, which is free. A `-` field stores nothing, costs nothing and cannot decay. |
| Budget | Integer `B_up` = the maximum number of D fields per episode (a hard cap). The unit is one field kept intact for one decay epoch. |
| Decay | At the end of phase I, each F field is **erased to `-`** independently w.p. `δ`. D fields persist. Erasure acts **per field**: no codebook state or slot is sampled. |
| Visibility | Erasure is visible as `-`, so an erased field abstains. This *supplies* an access marker (§9). |
| Unpaid control | No decay (δ = 0), or equivalently `B_up = 3`. |
| Proposed values | `δ = 1/2` is carried from v1. `B_up` is proposed in §12. **Both are PROPOSED.** |

**Why this resolves Astra's dichotomy.** Astra's two readings were:

- (i) a protected subset of codebook states, which an optimized fixed rule can copy;
- (ii) protecting the occupied state after encoding, which is always possible when `B_up ≥ 1`.

Here, protection is **per field** within the single occupied configuration, and `B_up` is below the number of stored fields. The genuine restriction that defines the rival is that **`fixed_upkeep` must choose its D-field set independently of the input and the cue** (§4.1). `full` chooses it as a function of (looks, cue). §5.3 shows that the resulting gap is non-zero.

---

## 3. Two capacity notions, kept separate

| Notion | Definition | Clean | Graded (any a) |
| --- | --- | --- | --- |
| **K_lossless** | Number of distinct values of the sufficient statistic of the evidence for every query (posterior support) | 8 (item vectors) | 27 (count patterns `{0,1,2}^3`) |
| **K_dec(world, a, r)** | Minimum number of Q-phase configurations at which the unconstrained optimum value is attained. Depends on the task and the reward. | 8 (r < 1, so answering is always optimal) | **27** for (3/4, ·) and (5/6, ·), since counts 0, 1, 2 give three distinct optimal actions per item. **27** for (3/5, 5/8), since 9/13 > 5/8. **1** for (3/5, 3/4): always abstaining is optimal (§5.2). |

**Rules.**

- The **lossless-capacity control** is `K ≥ K_lossless`.
- The **decision-sufficiency control** is `K ≥ K_dec`.
- Both are reported. Gates use K_dec.
- `ρ_H = log K / H(S)` is descriptive only, as before.
- Under paid upkeep, the Q-phase configuration count of an optimum includes erased variants. The paid-cell K range therefore runs up to the unconstrained optimum's **per-phase reachable count**, which is computed when the protocol runs and is not assumed. In the §5.3 example it is 26 (full) versus 18 (fixed).

---

## 4. Policy classes

### 4.1 Stage A (stationary)

| Class | Restriction relative to `full` (all else matched: observations, actions, upkeep resources, K, decay exposure) |
| --- | --- |
| `full` | None: any deterministic encoder, D-allocation within `B_up`, message map and decoder, within per-phase K |
| `cue_blind` | Encoder **and** D-allocation independent of the cue |
| `static_access` | All reachable Q-phase configurations share one abstention pattern (defined as in the v1 replay, frozen v1 §5) |
| `static_route` | `μ_j` is a fixed, input-independent function of fixed fields |
| `fixed_upkeep` | The D-field set is a fixed set of ≤ `B_up` field indices, independent of looks and cue. Encoding is otherwise unrestricted. |
| `random_yoke` | **Descriptive only.** D-fields are drawn uniformly at random, with full's mean count. It no longer carries a predicted signature (§8). |

### 4.2 Stage B: the repaired adaptive comparator

**What was broken.** v1 gave `adaptive_select` "none in principle" as its denied role, with allocation and routing that looked unrestricted. That made it either identical to `full` or undefined. Astra: "either equality is built in, or any gap reflects specified factorization/update restrictions."

**Repair. Both arms share everything below except the history-update rule.**

| Element | Frozen definition (values PROPOSED where marked) |
| --- | --- |
| Regime | Consumer A's map switches between `c` and `c+1` with hazard `h = 1/4` per episode (PROPOSED, carried from v1). The switch is hidden. |
| History register | `η ∈ {1..H}`, with **H = register cardinality, not history length** (Astra). **Primary H = 2** in both arms; secondary {1, 3} are report-only. There is no per-cell "best H". A policy may leave register values unused. |
| Charging | `η` is jointly charged in every phase: reachable `(η, configuration)` pairs ≤ K per phase. `(K, H)` pairs where even the minimal policy cannot fit are labelled **INFEASIBLE** (not UNRESOLVED) and listed before any search. |
| Not protected | `η` is held in an ordinary field under the **same upkeep rule as answer fields**. Keeping it intact across the episode boundary costs one unit of `B_up` per episode; otherwise it erases w.p. `δ` to its initial value 1. This prevents it becoming "uncharged, decay-proof memory". **Open item O-B1:** this couples history to the upkeep budget. Whether that is the intended design goes to Astra (§15). |
| Feedback | After each episode's query, the agent observes the query index `q`, the cue `c` it encoded with, and its outcome (correct / wrong / abstained). Nothing else. |
| Update order | Query → action → reward → feedback → update `η` → next episode's encoding uses `η`. |
| Initialization | `η_0 = 1`; regime drawn from its stationary distribution (1/2, 1/2). |
| Value | **Long-run average reward from that initial distribution**: the Cesàro limit of the joint chain over (regime, η). It is well defined even with multiple recurrent classes, and is computed exactly through the chain's limiting matrix, not from one stationary solve. |
| `full_B` | Encoder, D-allocation and decoder are arbitrary functions of `(η, inputs)`. **The update `η' = g(η, q, c, outcome)` is optimized.** |
| `adaptive_select` (repaired) | Same as `full_B`, except that the update is a **fixed, prespecified conventional tracker**. For H = 2: `η' = 1` if the last query was `c`, `η' = 2` if it was `c+1`, otherwise `η` is unchanged. Encoder and allocation are still optimized given `η`. |
| `ADAPT` | `V_full_B − V_adaptive_select`. **Meaning:** the value of an optimized history update over the conventional tracker, at identical H, K, feedback and upkeep. It is *not* a test of whether selection exists. A tie supports a conventional explanation while leaving the selection pressure intact (Astra). |

**H = 1** is a degenerate control: no history, so both arms coincide and ADAPT = 0 by construction. **H = 3** tests whether one more register value changes the verdict.

---

## 5. Measured quantities and analytic facts

### 5.1 Frozen definitions (verbatim from v1 §5)

> **Access value** = `V_full − V_static`, where `static` = the best codebook of size
> min(K, |rows|) drawn from codewords that **all share one opt-out pattern**.
> **Selection value** = `V_full − V_cue_blind`, where `cue_blind` = the best codebook whose
> **encoder sees the items only, not the cue**.

These definitions are extended unchanged to W2′, with the class restrictions in §4. In addition:

- `ROUTE = V_full − V_static_route`
- `UPK = V_full − V_fixed_upkeep`
- `ADAPT` as in §4.2

### 5.2 Access at sufficient storage (hand derivation; confirms Astra)

**Setup.** Single consumer, unpaid upkeep, `K ≥ K_dec`. Per item:

- `P(agree) = a² + (1−a)²`, with posterior confidence `a² / (a² + (1−a)²)`.
- A disagreeing pair gives confidence 1/2.

Then, per query:

- `V_full = P(agree)·max(conf, r) + P(disagree)·max(1/2, r)`
- `V_static = max(answer-always, abstain-always)`

| (a, r) | P(agree) | conf | V_full | V_static | **ACC_suff** |
| --- | --- | --- | --- | --- | --- |
| clean, any r < 1 | — | 1 | 1 | 1 | **0** |
| 3/4, 3/4 | 5/8 | 9/10 | 9/16 + 9/32 = **27/32** | max(3/4, 3/4) = 3/4 | **3/32** (matches Astra) |
| 3/4, 5/8 | 5/8 | 9/10 | 9/16 + 15/64 = 51/64 | 3/4 | **3/64** |
| 5/6, 3/4 | 13/18 | 25/26 | 25/36 + 15/72 = 65/72 | max(60/72, 54/72) | **5/72** |
| 5/6, 5/8 | 13/18 | 25/26 | 25/36 + 25/144 = 125/144 | 120/144 | **5/144** |
| **3/5, 3/4** | 13/25 | 9/13 < 3/4 | 3/4 (abstain always) | 3/4 | **0: all-abstain null control** |
| 3/5, 5/8 | 13/25 | 9/13 > 5/8 | 9/25 + 3/10 = 33/50 | max(3/5, 5/8) = 5/8 | **7/200** (not a null; see §12) |

**Reading.** In graded cells, access value at sufficiency is **ordinary selective prediction under observation uncertainty**. It is not storage-scarcity pressure. Therefore:

- Storage-attributed access is claimed **only in clean-evidence cells**.
- In graded cells, `ACC(K)` and `ACC_suff` are reported side by side. The difference `ACC(K) − ACC_suff` is descriptive and can have either sign. No scarcity-attributed access claim is made from graded cells.
- No gate requires an ideal observer to become certain (Astra §12).

### 5.3 UPK is not identically zero (hand derivation)

**Setup.** Clean evidence, single consumer, `v = 3/4`, `r = 3/4`, `δ = 1/2`, `B_up = 1`, ample K. Storing every bit is weakly optimal in both classes: an erased field yields `r`, which is the same as abstaining. Fields are tied to queries, so no class can relocate content between fields.

**`full`: make field `c` durable.**

- `P(q = c) = 3/4`, giving reward 1.
- Otherwise the query hits a fragile field, which survives w.p. 1/2. Its value is `1/2·1 + 1/2·3/4 = 7/8`.
- `V_full = 3/4 + 1/4 · 7/8 = 31/32`.
- This is also the upper bound. Only one field can be durable, and the cued field is the most probable query, so `V_full = 31/32` exactly.

**`fixed_upkeep`: one fixed durable field `j`.**

- `P(q = j) = 1/3`, since the marginal query is uniform under a uniform cue.
- `V = 1/3 + 2/3 · 7/8 = 11/12`, the same for every `j`.

**UPK = 31/32 − 11/12 = 93/96 − 88/96 = 5/96 > 0.**

**`B_up = 2`.**

- `full` makes `c` plus one other field durable: `7/8 + 1/8·7/8 = 63/64`.
- `fixed` makes two fixed fields durable: `2/3 + 1/3·7/8 = 23/24`.
- **UPK = 189/192 − 184/192 = 5/192 > 0.**

**Controls, provable directly:**

- `B_up = 0`: no durable writes in either class, so UPK = 0.
- `B_up = 3` (equivalent to unpaid): everything is durable, so UPK = 0.
- `v = 1/3`: the query is independent of the cue and the items, so no allocation beats a fixed one, and UPK = 0.

**K requirement.** In phase I, `full`'s policy has 8 bit-vectors × 3 durable positions = 24 configurations. In phase Q it has 26 (every field pattern with at least one non-erased field, i.e. 27 − 1). `fixed` needs 8 in phase I and 2·3·3 = 18 in phase Q. **The policy behind `UPK = 5/96` therefore needs `K ≥ 26`.** Below that, UPK is to be computed and is not assumed.

**Note.** This UPK is cue-dependent maintenance allocation. Under the frozen definitions it overlaps conceptually with SEL, but it is a different class contrast: encoding is unrestricted in both arms, and only the D-allocation is restricted.

---

## 6. Controls, applied per role

| Role | Control cells | Prediction | If violated |
| --- | --- | --- | --- |
| ACC | **Clean evidence, unpaid upkeep, K ≥ K_dec** (only these) | ACC = 0 | Implementation error |
| ACC | (a=3/5, r=3/4), any K, unpaid | All values = 3/4, every role difference = 0 | Implementation error |
| SEL | `v = 1/3`; K ≥ K_dec with unpaid upkeep | SEL = 0 | Implementation error |
| UPK | `B_up ∈ {0, 3}`; unpaid; `v = 1/3` | UPK = 0 | Implementation error |
| UPK | §5.3 cell at K ≥ 26 | UPK = 5/96 exactly (B_up = 1), 5/192 (B_up = 2) | Implementation error |
| ROUTE | Channel-sufficient L; `v = 1/3` | ROUTE = 0 | Implementation error |
| ADAPT | Stationary regime; H = 1 | ADAPT = 0 | Implementation error |
| all | v1 replay slice (clean, unpaid, single consumer) reproduces `replay_results.json` | match | Implementation error |
| all | K = 1 | DEGENERATE (all 0) | Implementation error |

Graded cells at K ≥ K_dec are **not** ACC controls. Their `ACC_suff` is reported against §5.2.

---

## 7. Outcome semantics and aggregation (rewritten per Astra)

### 7.1 Per cell

| Label | Condition |
| --- | --- |
| **CERT-POS(X)** | Certified lower bound on X > 0 |
| **CERT-ZERO(X)** | Certified X = 0 |
| **UNRESOLVED** | Bounds straddle 0, the time limit expired without a certificate, or accounting is ambiguous |
| **INFEASIBLE** | The (K, H) or (K, B_up) combination admits no policy (listed before the search) |
| **DEGENERATE** | K = 1 |

**Optimum coverage.** **ROBUST** or **PERMITTED** is assigned only after the §8 intervention analysis is complete over **all** optimal policies of the cell, up to item symmetry. If not all optima are certified, the cell's role-pattern label is UNRESOLVED, even if its value label is certified.

### 7.2 Per role X (protocol verdict)

**ADMIT(X)** requires all four of:

1. every per-role control for X (§6) passes;
2. CERT-POS(X) in at least one cell in **each** declared bin of that role's binding resource;
3. that role's §8 intervention analysis is complete across all optima in the CERT-POS cells;
4. no control for X is UNRESOLVED.

The binding resource, and its bins, differs by role:

| Role | Binding resource | Bins |
| --- | --- | --- |
| SEL, ACC | Storage `K/K_dec` | (0, 1/4], (1/4, 1/2], (1/2, 1) |
| ROUTE | Channel `L / K_dec,j` at ample storage, which repairs the earlier impossible storage-bin requirement | L = 1, L = 2 |
| UPK | `B_up / (number of stored fields)` | B_up ∈ {1, 2} |

**Strongest claim under ADMIT:** "within W2′ and the declared rival classes, the task rewards role X, and an admissible policy realizes it". Neither acquisition nor consciousness follows.

**REJECT-ABSENT(X):** CERT-ZERO(X) in **every** non-control cell of the declared scope. There must be no UNRESOLVED cells. A partially solved grid never certifies absence.

**REJECT-NARROW(X):** CERT-POS(X) somewhere, but some declared bin is entirely CERT-ZERO. That is, pressure is present but insufficiently widespread. The strongest claim is that this task/parameter family fails as the proposed discriminator. It does **not** reject C3.

**UNRESOLVED(X):** anything else, including missing certificates, unresolved controls and incomplete optimum coverage. No directional architectural conclusion is drawn.

### 7.3 Stop rule

- If any control fails, halt. That is an implementation error.
- Stage B runs only for roles that reach CERT-POS somewhere in stage A.
- **Not running B is recorded as "B not reached"**, which preserves uncertainty. It is not ADAPT = 0.

---

## 8. Intervention operators, re-derived

Each operator is frozen. Its consequence is **computed per optimal policy**, and no sign or size is assumed. Only the identities proved below are stated as predictions.

| Operator | Definition | Proved identity / status |
| --- | --- | --- |
| **O-SEL: cue swap** | Encode (and allocate) under cue `c`; draw the query from `P(q \| c′)`, with `c′` uniform on {0,1,2}∖{c} | **For `cue_blind`, ΔV = 0 exactly.** Its encoding is independent of `c`, and `c′` is uniform and independent of `x`, so the query marginal it faces is unchanged. For `full`, ΔV is computed. **v1's claim "size = SEL" is DROPPED.** SEL compares separately optimized policies, and an intervention on one fixed policy need not equal it (Astra). |
| **O-ACC: single-field access flip** | Operational "matched content, different access": take the optimum's configuration `m`. Replace **one** field: an answered field becomes `-`, or a `-` field becomes the decoder's best guess given `m`. All other fields stay identical. Defined only if the resulting `m′` is reachable under the same policy; otherwise it is logged NOT-APPLICABLE. | ΔV per flipped field is computed. **Clean evidence:** answer → `-` changes the query's value from 1 to r, a loss of `(1 − r)·P(q = that field)`. `-` → guess on an unstored field changes it from r to 1/2, a loss of `(r − 1/2)·P(q = that field)`. For `static_access` the operator is **NOT-APPLICABLE**, since every configuration has the same pattern. The v1 "rival: no change" claim is **DROPPED**. |
| **O-UPK: durability withdrawal** | At encoding, rewrite one D field as F; nothing else changes | **Closed form, clean evidence:** ΔV = −δ·P(q = j \| c)·(1 − r) for withdrawn field `j`. In the §5.3 cell, field `c` gives −1/2·3/4·1/4 = **−3/32**. Withdrawing a `-` field is impossible (it has no cost and nothing to lose). **The `random_yoke` "independent of content relevance" prediction is DROPPED** (Astra). |
| **O-ROUTE: cue swap at routing** | Route under cue `c`; draw consumer queries under `c′`, as in O-SEL | For `static_route`, ΔV = 0 by the same argument as O-SEL, since its messages are input-independent of `c`. Otherwise computed. |
| ~~Message swap μ_A ↔ μ_B~~ | — | **DROPPED.** Independently optimized message alphabets have no canonical alignment, so the effects are arbitrary (Astra). |
| ~~L-reduction as a lesion~~ | — | **DROPPED as an intervention.** Reducing L and re-optimizing tests redesign, not a lesion response. L stays a design factor (§7.2 bins). |
| ~~"static router loses uniformly"~~ | — | **DROPPED.** It does not follow. |

These remain representability predictions about optima (Q-EXIST). Their use as Q-CAUSE tests on any developed system needs a separately authorized study.

---

## 9. Scaffold accounting (per role)

**Answer to Astra's question.** Optimization here **fills a lookup table over supplied decision points**: the encoder map, the D-allocation, the abstention entries and the message maps. **No selector module is supplied beyond those tables**, but the decision points themselves, and their information access, are supplied. A later learner would have to acquire the *functional allocation*, i.e. the table, without these decision points being handed to it as separate, labelled operations.

| Role | Supplied by the policy language / world | Chosen by optimization | Removed by the role-denied rival | What a later learner would have to acquire (ORIGIN: untested) |
| --- | --- | --- | --- | --- |
| SEL | Encoder with access to the cue; field-per-query layout; K | The cue-conditioned input → configuration map | Cue dependence of encoder and allocation (`cue_blind`) | A cue-conditioned retention mapping inside a generic state, with no designated per-query fields |
| ACC | The `-` action in every field. **Under paid upkeep, erasure-to-`-` supplies an access marker** (world-side). | Which configurations abstain on which queries | State dependence of abstention (`static_access`) | State-dependent abstention. Under paid upkeep, part of ACC is supplied by erasure visibility, and this must be subtracted before any acquisition claim. |
| ROUTE | Message alphabet L, per-consumer decoders, consumer query maps | Message maps and decoders, **jointly** | Input/cue dependence of messages (`static_route`) | Sender and receiver conventions co-adapted under a channel limit, i.e. emergent communication, which is the harder acquisition target |
| UPK | The durable/fragile write operation, unit cost, decay process, per-field granularity and durability mark | Which fields to make durable, as a function of (looks, cue) | Input/cue dependence of allocation (`fixed_upkeep`) | Content-dependent allocation of maintenance with no designated "durable" operation, e.g. via a costly rehearsal action in a generic state |
| ADAPT (stage B) | History register of cardinality H (charged, unprotected), feedback alphabet, update timing | Encoder/allocation given η; in `full_B`, also the update rule | An optimized update (`adaptive_select` uses the conventional tracker) | A history update rule acquired from feedback, without a designated register |

---

## 10. Adaptive rival: necessary, not an acquisition test

The equal-state adaptive comparator (§4.2) is **necessary** to discipline any claim beyond conventional adaptive selection. It is **not a test of acquisition**: both arms are supplied policy classes optimized by the protocol, and nothing is learned. Matching it rules out nothing about ORIGIN.

Following Astra, the arms are matched on:

- observations;
- available actions;
- upkeep resources;
- memory protection, i.e. neither arm has protected memory;
- state count.

A gap reflects only the specified update restriction. **ORIGIN remains "untested"** for every role whatever this card returns. Showing that a role was acquired requires a later, separately authorized emergence experiment.

---

## 11. Computation accounting (accepted 10 CPU-min rule, made precise)

- **Solver.** The configuration is frozen before the search: method, ordering, bounds and tie-breaking. Single-threaded is preferred. If multiple workers are used, **CPU time is aggregated across all workers**.
- **Restarts and resumptions** count against the same 10 CPU-minutes per cell.
- **What the budget includes:** the optimization, **all-optima certification**, and the §8 intervention analysis.
- **Certified bounds** are saved at **3-CPU-minute checkpoints**. A valid certificate obtained before the timeout remains usable.
- **Timeout** without a decisive certificate means **UNRESOLVED**.
- **30-minute sensitivity.** This is an explicitly separately budgeted re-run of UNRESOLVED cells only. Its results are reported, but **cannot change primary labels**.

---

## 12. Parameters

**Accepted (still unfrozen until a document-level freeze verdict):**

| Item | Status |
| --- | --- |
| `a` | 3/4 primary. 5/6 secondary. (3/5, r = 3/4) is the all-abstain null control. **(3/5, r = 5/8) is not a null** (ACC_suff = 7/200), so it is excluded from the grid, pending Astra (F4). |
| K | Integer per-phase reachable-configuration cap (§2.4) |
| Time limit | 10 CPU-min per cell (§11) |
| H | 2 primary, {1, 3} report-only, **for the repaired comparator only** (§4.2) |

**PROPOSED, NOT FROZEN (for the Specialist to take to Astra):**

| Item | PROPOSED primary | PROPOSED secondary | Justification |
| --- | --- | --- | --- |
| `B_up` (field units per episode) | **1** | {2}; controls {0, 3} | §5.3 proves UPK > 0 at 1 and 2, and UPK = 0 at 0 and 3. That makes 1 the most binding non-degenerate value. |
| `δ` (erasure probability of fragile fields) | 1/2 | {1/4} | Carried from v1. It gives the round numbers used in §5.3. 1/4 checks that UPK's sign does not depend on strong decay. |
| History maintenance in stage B | η costs 1 `B_up` unit per episode to persist | η persists only through ordinary fragile decay (no cost) | This keeps η unprotected and charged (O-B1). Astra should choose. |

---

## 13. Thirteen admission answers

| Q | Answer |
| --- | --- |
| Q1 | C3 bounded prerequisite: which conditions in W2′ reward state-dependent retention, access, routing and upkeep allocation, and which remove that reward |
| Q2 | For each role X: does `full` strictly beat the X-denied class at equal per-phase reachable configurations, matched observations, actions and upkeep, across the declared binding-resource bins, with the per-role controls zero? |
| Q3 | Per-role REJECT-ABSENT or REJECT-NARROW (§7.2). Any control violation invalidates the card until it is fixed. |
| Q4 | The repaired `adaptive_select` (conventional tracker, same H/K/feedback/upkeep); `cue_blind`, `static_access`, `static_route`, `fixed_upkeep`; ordinary selective prediction under observation uncertainty, for graded ACC (§5.2) |
| Q5 | `SCARCITY_GAP_v1.md` §5 (branch, replayed exactly); Astra RESPONSE A blocking corrections; Phase III/III-B, where capacity bound only shallowly; Phase II, where allocation reduced to a threshold |
| Q6 | Use ADMITted roles, and their computed §8 responses, to draft a separately approved prospective emergence experiment, with §9 as the scaffold-subtraction ledger |
| Q7 | REJECT-ABSENT parks role X in W2′ with an exact reason. REJECT-NARROW records the failed bins and redesigns the family, without rejecting C3. UNRESOLVED preserves the open cells, with no post hoc time extension. |
| Q8 | Analytic certificate: exact enumeration, branch-and-bound, exact Markov-chain averages. No neural model, no organism. |
| Q9 | Organizational cognition (reward and representability of a role) |
| Q10 | §14 |
| Q11 | C3. Still unsupported: Q-LEARN, ORIGIN, Q-CAUSE in developed systems, and all C4 |
| Q12 | O0/N1 paid persistence, in field form. **No O3 machinery bridge** (Astra). Supplied: the world, decision points, upkeep operation, decay, consumers and channel. |
| Q13 | ADMIT(X) updates the C3 ledger ceiling and next falsifier. REJECT-* adds collapse-ledger entries scoped to W2′. ADAPT results enter REDUCTION only. ORIGIN is unchanged in every case. |

---

## 14. Claim ceiling

**Under ADMIT(X), the strongest claim is:** "In W2′, at equal per-phase reachable configurations and matched observations, actions, upkeep and memory protection, certified bounds show that the task rewards role X over the declared X-denied class across the declared bins. An admissible policy realizes X, with intervention responses computed across all optima."

**NOT established:**

- acquisition (ORIGIN: untested);
- causal use in any developed system;
- necessity beyond the declared classes;
- C4;
- an O3 machinery-maintenance bridge;
- consciousness.

An optimal codebook is not acquired organization.

---

## 15. Flags

- **F1. Mojibake.** Part 1 of the draft reached Astra with garbled non-ASCII characters, and I cannot tell exactly where Part 1 ended. Several RESPONSE A points touch symbol-heavy text: the K_supp definition (`≥`, `|supp S|`), the ρ bins, `K_content × H ≤ K`, `⌊K/2⌋`, and `δ`/`β` in the upkeep rows. Treat those rulings cautiously. Astra's points were:
  - **ACC = 3/32:** I re-derived this independently (§5.2) and it does not depend on symbols.
  - **The upkeep dichotomy:** this holds under either reading of the garbled text, and I agree with it.
  - **K_supp vs K_dec:** this is confirmed by my own (3/5, 3/4) derivation.
  - **The H-cardinality remark and "count reachable joint configurations, not the sum of register sizes":** these may respond to a garbled `K_content × H`. They are adopted anyway, as the stricter reading.
  - **Recommendation:** re-send §§1–4 in ASCII before the freeze verdict.
- **F2. Protected controller or register: none added.** One design pressure came close. In stage B, a history register that is exempt from decay would be "uncharged, decay-proof memory". I did **not** add one. η is an ordinary charged field under the same upkeep rule (O-B1). If Astra rules that history must persist without upkeep cost, that would make η a protected register. **Stop at that point and route it to Aidan** as a possible new architecture family. Durable writes in §2.5 are paid, charged and per-field, available equally to every class, so they are not a protected controller.
- **F3. Supplied access under erasure.** Erasure-to-`-` makes decay visible, which supplies part of ACC under paid upkeep (§9). If the Specialist prefers hidden decay (bit flips), the bookkeeping of "what was made durable" would have to live in decaying fields. Otherwise it becomes a protected register (F2). Hidden decay is therefore not proposed here.
- **F4. The (a=3/5, r=5/8) cell is not a null.** It has ACC_suff = 7/200, so it is excluded pending Astra's ruling on whether 3/5 is paired only with r = 3/4.
- **F5. Open items:**
  - O-B1: history upkeep cost;
  - `B_up` and `δ` (PROPOSED);
  - the solver configuration, to be frozen;
  - the INFEASIBLE (K, H, B_up) list, to be generated before any search.
- **F6. Hand derivations.** §5.2, §5.3 and §8 are hand arithmetic, shown in full. They are not search output, and they become self-tests (§6) when the protocol is eventually run.
