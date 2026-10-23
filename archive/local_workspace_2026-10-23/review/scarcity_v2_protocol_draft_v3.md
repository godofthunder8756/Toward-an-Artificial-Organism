# scarcity_v2 protocol draft v3: revisions after Astra Consult #6 ("DO NOT FREEZE")

**Status: DRAFT. NOT FROZEN. NOT RUN.**

| Item | Value |
| --- | --- |
| Layer | C3 only: retention, access, routing, upkeep allocation |
| Supersedes | `scarcity_v2_protocol_draft_v2.md` (left untouched, md5 45ac7705…). Draft v1 `scarcity_v2_protocol_draft.md` is also untouched (md5 13bb7b22…). |
| Written | 2026-10-20 (EDT) by Research Delegate for the ACI Research Specialist, on behalf of Aidan Ahern |
| Sources | `/workspace/astra_consult_5_raw.md`, "CONSULT #6 RESPONSE"; the Specialist's flag rulings (1)–(4) and blockers (a)–(f) of 4:26 PM |
| Repo | `/workspace/repo` untouched |

**Execution.** No search, solver or enumeration was executed. Every number is a hand derivation with its
arithmetic shown. The closed forms in §5 were rechecked with exact rational arithmetic (`fractions.Fraction`,
about ten lines, no optimization).

**Scaffolding.** No protected controller or register is introduced. Ruling (1) explicitly keeps the history
register charged (§4.3, §15 F2).

**Claim discipline.** No consciousness claim. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.
ORIGIN is **untested** throughout. An optimal codebook is not acquired organization.

---

## 0. Changes from draft v2

| # | Source | Change in v3 |
| --- | --- | --- |
| C1 | Confirmed results | ACC_suff = 3/32, UPK = 5/96 and UPK = 5/192 are kept, each with an explicit **scope statement**. The UPK bounds hold only under **direct per-query field semantics** (S-DIRECT), clean evidence and ample capacity. They are not claimed for any decoder that can reinterpret other fields (§5.2, §5.3). |
| C2 | Ruling (1) | The history register keeps its 1-unit upkeep charge. O-B1 is closed. No free or persistent register. A free register would be a protected-memory scaffold, i.e. an apparatus change (§4.3, §15). |
| C3 | Ruling (2) | Visible `-` erasure is kept and marked as **supplied access**. The promise to "subtract" it numerically is **withdrawn**. Acquisition attribution would need matched scaffold controls (§9). |
| C4 | Ruling (3) | (3/5, 3/4) is the **only** null. (3/5, 5/8) is excluded **on scope grounds**: its positive ACC_suff is not the reason (§12). |
| C5 | Ruling (4) | δ = 1/2 is primary and δ = 1/4 secondary. The secondary's decision role is frozen: it is report-only and cannot change any primary label. In the proved examples UPK is linear in δ (§5.3, §12). |
| C6 | Blocker (a) | The v2 control "v = 1/3 ⇒ UPK = 0" is **false under graded evidence**. Hand-verified: UPK = **33/4096** at a = r = 3/4, δ = 1/2, B_up = 1 (§5.4). Zero-UPK controls are restricted to **proved** cases (§6). Storage-attributed ACC is restricted to **clean, unpaid** cells. |
| C7 | Blocker (b) | ROUTE at L = 1 is now a **null control** (proof in §5.6). `static_route` is redefined with an explicit information set: the evidence statistic only, with no cue and no encoder-written fields. O-ROUTE's zero identity is re-proved for that definition (§4.2, §8). |
| C8 | Blocker (c) | Explicit **policy semantics per condition** (§2.6): S-DIRECT for all storage and upkeep cells and for stage B; S-MSG only for ROUTE cells. Arbitrary memory decoders are removed from §4. Further changes: K_dec = 8/27 is scoped to the clean/graded **unpaid, full-channel** baseline; a new **K_suff** is min over optimal policies of max over phases of the reachable count (§3); a **frozen outer K grid** is set independently of any solver optimum (§3.3). |
| C9 | Blocker (d) | The O-ACC identities are rewritten with the actual conditional correctness p: answer→abstain changes reward by (r − p), abstain→guess by (p_guess − r), each weighted by P(q \| m). O-SEL and O-ROUTE use a **cue-law-preserving swap kernel**. A derangement kernel exists only if max π(c) ≤ 1/2, so the S2 sweep (2/3, 1/6, 1/6) uses independent resampling (§8). |
| C10 | Blocker (e) | Stage B gains a selectable **constant tracker** (§4.3). The new pieces are: the H = 3 tracker; the timing of register updates, durability payment and erasure; the observation that B_up = 3 no longer guarantees persistence with a fourth field; the scope "positive ADAPT is evidence only against this tracker set"; and a new proof that stationary ADAPT = 0 (§5.7). |
| C11 | Blocker (f) | A per-role **response property** P_X now defines ROBUST / PERMITTED / NONE / SIG-UNDEFINED. NOT-APPLICABLE never counts as a signature (§7.1). |

---

## 1. Scope

**In scope:** C3 pressure and representability for selection (SEL), state-dependent access (ACC), routing across
consumers (ROUTE) and content-dependent upkeep allocation (UPK), within declared finite policy classes.

**Out of scope (unchanged from v2):**
- the social-modelling, curriculum and intrinsic-motivation pressures (GATED / DESIGN-ONLY, `emergence_conditions_v2.md` §3);
- every C4 component;
- the self-induced-uncertainty quantity (UNDEFINED, EXCLUDED);
- any O3 machinery-maintenance bridge.

---

## 2. World family W2′

### 2.1 Items, evidence, cue, reward (unchanged from v2)

| Component | Definition |
| --- | --- |
| Items | x ∈ {0,1}³, i.i.d. uniform |
| Evidence EV | **clean**: exact observation. **graded**: two looks per item, i.i.d. given the item, each correct w.p. a. Statistic n_i ∈ {0,1,2}. |
| a | 3/4 primary; 5/6 secondary; (a = 3/5, r = 3/4) is the **only** null (§12) |
| Cue | c ∈ {0,1,2}, observed at encoding. Primary law π uniform. Sweep S1 = (1/2, 1/4, 1/4) and S2 = (2/3, 1/6, 1/6), descriptive only. |
| Query map | Single consumer: q = c w.p. v, otherwise uniform on the other two; v ∈ {1/3 (uninformative), 3/4}. Two consumers (ROUTE only): A as above; B with c+1 in place of c. |
| Reward | correct answer 1; wrong answer 0; abstain (`-`) r ∈ {5/8, 3/4} |

### 2.2 Memory fields (S-DIRECT cells)

- **Answer fields.** Three answer fields f₀, f₁, f₂ ∈ {0, 1, `-`}.
- **Durability mark.** During phase I, each non-`-` field also carries D or F.
- **History field (stage B only).** A fourth field η ∈ {1..H} with its own D/F mark (§4.3).

### 2.3 Upkeep (unchanged definition)

- **Allocation.** The D-set is chosen at encoding, with |D-set| ≤ B_up.
- **Decay.** At the end of phase I, each F field decays independently w.p. δ: an answer field is erased to `-`;
  η is reset to its initial value. D fields persist.
- **`-` fields.** They cost nothing and cannot decay.
- **Unpaid control.** δ = 0, or B_up ≥ the number of fields: B_up = 3 in stage A, **B_up = 4 in stage B**.

### 2.4 Consumers and channel (ROUTE cells only)

- Channel: L ∈ {1, 2, 3} symbols per consumer, or channel-sufficient L ≥ K_dec,base (8 clean, 27 graded).
- Storage in ROUTE cells is **ample and unpaid**. It is not modelled beyond §2.6.

### 2.5 Phases

- **E (encoding):** inputs present.
- **I (upkeep interval):** fields plus marks (plus η in stage B).
- **Q (query):** fields after decay (plus η).
- **Reachable-configuration cap K:** applies in **each** phase separately; integer; duplicates merged (as in v2 §2.4).

### 2.6 Policy semantics, fixed per condition (new; resolves the §2/§5 vs §4 conflict)

| Semantics | Used in | Definition |
| --- | --- | --- |
| **S-DIRECT** (literal fields) | **All** SEL, ACC and UPK cells, unpaid and paid, clean and graded; all of stage B | The encoder maps (evidence, cue[, η]) to field values and a D-set. **The action at query q is the post-decay value of f_q.** There is no decoder, so no field can be reinterpreted. An erased field abstains. This is the v1 replay's codeword language, where a configuration *is* its action vector. |
| **S-MSG** (messages) | ROUTE cells only | The sender sees the information set allowed by its class (§4.2) and emits μ_j ∈ {1..L} to each consumer j. Consumer j acts by an arbitrary decoder d_j(μ_j, q_j). Memory is ample and unpaid, so the sender's information set is available losslessly (K ≥ 3·K_lossless: 24 clean, 81 graded). |

**Equivalence note.** In unpaid single-consumer cells, S-DIRECT gives the same optimal values as a decoder
language: any decoder over K abstract labels defines K action vectors. In paid cells the two differ, because a
decoder could read other fields after an erasure. **This protocol adopts S-DIRECT for paid cells.** No result
is claimed for the decoder language there (flag F3).

---

## 3. Capacity notions

### 3.1 Definitions

| Notion | Definition | Scope |
| --- | --- | --- |
| **K_lossless** | number of values of the evidence sufficient statistic: 8 clean, 27 graded | descriptive |
| **K_dec,base** | the minimal per-phase count at which the unconstrained optimum is attained, in the **clean/graded, unpaid, single-consumer, full-channel baseline**. Clean 8. Graded 27 for (3/4, ·) and (5/6, ·). 1 for the null (3/5, 3/4). | **only** that baseline (Astra #6) |
| **K_suff(cell)** | **min over optimal policies π of [max over phases ∈ {E, I, Q} of the reachable count N_phase(π)]**. Defined for every cell (paid, stage B, ROUTE); it equals K_dec,base on the baseline. | general; computed at run time and never assumed |

The Specialist's message reads "minimum over phases of the maximum reachable count". Astra's wording,
"minimize the maximum reachable count across phases", is implemented as written above: the minimum is over
optimal policies and the maximum over phases (flag F4).

### 3.2 Rules

- **Sufficiency control.** K ≥ K_suff(cell).
- **ACC/SEL gate bins.** These are indexed by K / K_dec,base. For paid cells this ratio is a **frozen index,
  not a sufficiency claim**.

### 3.3 Frozen outer K grid (independent of any solver optimum)

**K ∈ {1, 2, 3, 4, 6, 8, 12, 16, 18, 24, 26, 27, 32, 48, 64, 96, 125}** for stage A.

**Why 125 is ample.** Under S-DIRECT, the stage-A I-phase count is at most Σ over patterns of field states.
Each field is `-`, or one of 2 values × 2 marks, i.e. 5 states, giving ≤ 5³ = 125. The Q-phase count is
≤ 3³ = 27. So K = 125 admits **every** stage-A policy.

**Stage B.** The grid is the stage-A grid × {1, H, 2H}, capped at the ample value 125·2H. The η field has H
values × 2 marks.

**Inclusion.** Grid points are included whether or not they coincide with an optimum's count. 18, 24 and 26 are
included because §5 uses them as proved thresholds, not because a solver found them.

---

## 4. Policy classes

### 4.1 Stage A, S-DIRECT

| Class | Restriction relative to `full` (everything else matched) |
| --- | --- |
| `full` | Any deterministic encoder (evidence, cue) → (fields, D-set), within per-phase K and B_up |
| `cue_blind` | Encoder and D-set independent of the cue |
| `static_access` | All reachable **Q-phase** configurations share one `-` pattern. Under paid upkeep this is usually infeasible except with all-D or all-`-` patterns, so paid-cell ACC is descriptive (§5.5). |
| `fixed_upkeep` | D-set = a fixed index set of size ≤ B_up, independent of evidence and cue |
| `random_yoke` | Descriptive only |

### 4.2 ROUTE classes, S-MSG

| Class | Information set of the sender | Message map |
| --- | --- | --- |
| `full_route` | (EVstat, c): EVstat = x (clean) or (n₀, n₁, n₂) (graded) | μ_j = g_j(EVstat, c), arbitrary |
| `static_route` | **EVstat only.** The permitted "fields" are the three raw evidence-statistic fields. There is no cue, no encoder-written field, and no access to the other consumer's query. | μ_j = g_j(EVstat), arbitrary but cue-independent |

**What static_route denies.** It denies exactly the cue-dependent choice of which content is sent to which
consumer, i.e. routing. Because its inputs are raw evidence fields and not cue-dependent encoded fields, Astra's
leak ("a cue-independent router can still receive cue-dependent encoded fields") cannot arise.

**Consumers.** Consumer decoders d_j are arbitrary in both classes.

**Value.** The mean of the two consumers' expected rewards.

### 4.3 Stage B (repaired comparator v3)

| Element | Definition |
| --- | --- |
| Regime | Consumer A's query map switches between c and c+1 with hidden hazard h = 1/4 per episode (PROPOSED). The stationary control has h = 0. |
| η field | η ∈ {1..H}; H = 2 primary; H ∈ {1, 3} report-only. η₀ = 1 for H = 2 and η₀ = 2 for H = 3. Erasure resets η to η₀. |
| Charging | (η, fields, marks) are jointly counted per phase against K. **η costs 1 unit of B_up per episode to be durable (ruling (1)).** A free or persistent η would be a protected-memory scaffold and is **not** used. |
| Fields and B_up | There are **four** fields (f₀, f₁, f₂, η). **B_up = 3 no longer guarantees that everything persists.** The unpaid control is B_up = 4 or δ = 0. |
| **Timing (episode t)** | 1. **E_t:** the encoder reads (evidence_t, c_t, η_t) and writes f₀..f₂ and a D-set ⊆ {f₀, f₁, f₂, η} with \|D\| ≤ B_up. This is the only durability payment of episode t. 2. **End of I_t:** each fragile field decays w.p. δ, so answer fields → `-` and η → η₀. Call the result η̃_t. 3. **Q_t:** query q_t; action = post-decay f_{q_t}; reward. 4. **Feedback:** (q_t, c_t, outcome_t ∈ {correct, wrong, abstained}). 5. **Update:** η_{t+1} = g(η̃_t, q_t, c_t, outcome_t), used at E_{t+1}. |
| `full_B` | Encoder and D-set are arbitrary functions of (η, evidence, cue); g is optimized. |
| `adaptive_select` (v3) | The encoder and D-set are optimized given η. **g is selected from the fixed set {T_const, T_H}**; the class value is the max of the two. **T_const:** η_{t+1} = η₀ always. Its reachable η count is 1 and it never needs η upkeep. **T_2:** η′ = 1 if q = c; η′ = 2 if q = c+1; else η′ = η̃. **T_3 (saturating counter):** if q = c then η′ = max(η̃ − 1, 1); if q = c+1 then η′ = min(η̃ + 1, 3); else η′ = η̃. Here 1 = "regime c likely", 3 = "regime c+1 likely" and 2 = neutral. |
| `ADAPT` | V_full_B − max(V_{T_const}, V_{T_H}). It is also reported per tracker. **Scope:** a positive ADAPT is evidence only against **this** tracker set {T_const, T_H} at equal H, K, feedback and upkeep, not against conventional adaptive selection in general. |
| Value | The Cesàro long-run average from (stationary regime, η₀), computed through the chain's limiting matrix (unchanged from v2) |

---

## 5. Analytic facts (hand-derived; scope stated per item)

### 5.1 Frozen definitions (unchanged)

- Access = V_full − V_static_access.
- Selection = V_full − V_cue_blind.
- ROUTE = V_full_route − V_static_route.
- UPK = V_full − V_fixed_upkeep.
- ADAPT as in §4.3.

### 5.2 ACC_suff (v2 table retained)

**Scope.** Single consumer, unpaid, K ≥ K_dec,base, S-DIRECT.

| (a, r) | ACC_suff |
| --- | --- |
| clean | 0 |
| (3/4, 3/4) | **3/32** (confirmed by Astra #6) |
| (3/4, 5/8) | 3/64 |
| (5/6, 3/4) | 5/72 |
| (5/6, 5/8) | 5/144 |
| (3/5, 3/4) | **0, all-abstain null** |

Graded ACC_suff is ordinary selective prediction under observation uncertainty and is **never**
storage-attributed.

### 5.3 UPK > 0 under clean evidence (confirmed), with δ-scaling

**Scope.** S-DIRECT; clean evidence; single consumer; v = 3/4; r = 3/4; uniform cue; K ≥ the thresholds below.
These are not claimed for decoder semantics.

**Values.** An answered fragile field is worth (1−δ)·1 + δ·r = 1 − δ/4.

- **B_up = 1.**
  - V_full = 3/4 + (1/4)(1 − δ/4) = 1 − δ/16.
  - V_fixed = 1/3 + (2/3)(1 − δ/4) = 1 − δ/6.
  - **UPK = 5δ/48.** δ = 1/2 → **5/96** (confirmed); δ = 1/4 → 5/192.
- **B_up = 2.**
  - V_full = 1 − (1/8)(δ/4) = 1 − δ/32.
  - V_fixed = 1 − (1/3)(δ/4) = 1 − δ/12.
  - **UPK = 5δ/96.** δ = 1/2 → **5/192** (confirmed); δ = 1/4 → 5/384.

The upper bound holds because, under S-DIRECT, a field can only answer its own query, and full protects the
most probable queries.

**K thresholds** (S-DIRECT counts):

| B_up | full: phase I | full: phase Q | fixed: phase I | fixed: phase Q | K needed for the stated full policy |
| --- | --- | --- | --- | --- | --- |
| 1 | 24 | 26 | 8 | 18 | **K ≥ 26** |
| 2 | 24 | 20 (≤ 1 erased field) | 8 | 12 | **K ≥ 24** |

Below these thresholds UPK is computed, not assumed. The B_up = 2 counts are new hand counts, labelled as such
(flag F6).

### 5.4 Graded evidence breaks the "v = 1/3 ⇒ UPK = 0" control (Blocker (a), verified)

**Setup.** S-DIRECT; graded; a = r = 3/4; δ = 1/2; B_up = 1; v = 1/3 (uniform query, independent of cue and
items); ample K (≤ 125 by §3.3).

**Per item.**
- P(agree) = a² + (1−a)² = 5/8, with confidence 9/10 > r. That field is answered.
- P(disagree) = 3/8, with confidence 1/2 < r. That field is `-`, which neither needs nor benefits from
  durability.

**Gain from durability.** Making an answered field durable gains δ(9/10 − r)·P(q = j) = (1/2)(3/20)(1/3) = 1/40.
Answering a fragile field is never worse than `-`, since (1−δ)(9/10) + δr ≥ r. So:

- V_full = base + (1/40)·P(at least one field agrees) = base + (1/40)(1 − (3/8)³) = base + (1/40)(485/512).
- V_fixed = base + (1/40)·P(fixed field j agrees) = base + (1/40)(5/8) = base + (1/40)(320/512).

**UPK = (1/40)(165/512) = 165/20480 = 33/4096 > 0.**

This matches Astra's formula δ(9/10 − r)/3 · [P(≥1 agreement) − P(fixed field agrees)]. Exact rational arithmetic
gives 33/4096 at δ = 1/2 and 33/8192 at δ = 1/4, again linear in δ.

**Interpretation.** Even with an uninformative cue, full allocates durability to **evidence-dependent** content
(an agreeing look), not cue-dependent content. UPK therefore mixes cue-relevance and evidence-reliability
allocation. In graded cells it is reported but **not** attributed to cue-dependent maintenance (flag F7).

### 5.5 Proved zero controls (only these are controls)

| Control | Proof sketch | Scope |
| --- | --- | --- |
| **UPK-Z1:** B_up = 0 | No D writes in either class | all cells |
| **UPK-Z2:** B_up ≥ number of fields (3 in stage A) | All fields durable in both classes | all stage-A cells |
| **UPK-Z3:** δ = 0 | Durability is irrelevant | all cells |
| **UPK-Z4:** clean, v = 1/3, B_up = 1, K ≥ 18 | Every field answered correctly is weakly optimal (1 − δ/4 ≥ r). P(q = j) = 1/3 for every j, so any single D field yields 1 − (2/3)(δ/4) and that is also full's upper bound. The fixed all-answer policy needs ≤ 8 (I) and 18 (Q) configurations. | clean, S-DIRECT only. **Not graded** (§5.4). |
| **UPK-Z4′:** clean, v = 1/3, B_up = 2, K ≥ 12 | Same argument, with fixed counts 8 (I) and 12 (Q) | clean, S-DIRECT |
| **ACC-Z:** clean, **unpaid**, K ≥ 8 | full stores x (V = 1). An all-answer static pattern also gives V = 1. | clean, unpaid only. Storage-attributed ACC is claimed only in clean, unpaid cells. |
| **NULL:** (a = 3/5, r = 3/4), any K, any B_up, any class | Every answer has conf ≤ 9/13 < r. All-`-` attains r, needs no upkeep and fits K = 1. Every class therefore has V = r and every role difference is 0. | graded |
| **SEL-Z:** v = 1/3, unpaid, any K | The query is independent of (c, x), so a cue-dependent choice among codebook entries is never better than the best fixed choice | S-DIRECT |
| **ROUTE-Z1:** L = 1 | Both classes send a constant message, so the decoders face identical information | §5.6 |
| **ROUTE-Z2:** v = 1/3 | Queries are independent of (c, x). V_full_route = E_c[V(g(·, c))] ≤ max_c V(g(·, c)), which static_route attains with g(·, c*). | S-MSG |
| **ROUTE-Z3:** L ≥ K_dec,base (8 clean, 27 graded) | The per-query optimal action depends on evidence only, never on c. static_route sends the full optimal action profile. | S-MSG |
| **ADAPT-Z1:** H = 1 | Both arms coincide | stage B |
| **ADAPT-Z2:** stationary regime (h = 0) | §5.7 | stage B, with T_const in the class |
| **K = 1** | DEGENERATE | all |

**Removed as controls.** v2's "UPK = 0 at v = 1/3" in graded cells is false (§5.4). Paid-cell ACC is not a
control and is not storage-attributed: paid erasure can create access variation without storage scarcity.

### 5.6 ROUTE at L = 1 is a null

With one symbol, μ_j is constant in both classes. Each consumer's best decoder is then the same function of q_j
alone, so V_full_route = V_static_route and ROUTE = 0. L = 1 moves from "required positive bin" to **null
control**.

**Positive ROUTE bins.** L ∈ {2, 3} (PROPOSED). Positivity there is **not** proved by hand. A feasible full
policy at clean, v = r = 3/4, L = 2 (send x_c; the consumer always answers) gives V_full_route ≥ 7/8. I have no
proved bound on static_route, so no sign is claimed (flag F8).

### 5.7 Stationary ADAPT = 0 with the constant tracker (new proof)

**Setup.** h = 0. Episodes are i.i.d. given the policy, and η affects reward only through the encoder and D-set.

**Proof.**
1. Any full_B policy's long-run value is a convex combination over η-states of per-η episode values. Paying
   upkeep on η or holding more η values only consumes B_up or K.
2. Let η* be the η-slice with the highest per-episode value. The policy "use slice η* with η constant" (T_const,
   with η₀ relabelled to η*) attains at least that value.
3. Its reachable counts are ≤ the counts of full_B's slice η*, and therefore ≤ K.
4. It spends no B_up on η.
5. So V_{T_const} ≥ V_full_B, and ADAPT = 0.

**Why this was false in v2.** v2 lacked T_const. The fixed tracker forces η changes, which consume K and
possibly B_up.

---

## 6. Controls applied per role

| Role | Controls (all proved in §5.5) | If violated |
| --- | --- | --- |
| ACC | ACC-Z (clean, unpaid, K ≥ 8); NULL; K = 1 | implementation error |
| SEL | SEL-Z; NULL | implementation error |
| UPK | UPK-Z1, Z2, Z3; UPK-Z4/Z4′ (clean only); NULL; **positive self-tests**: §5.3 values at K ≥ 26 / 24, and **§5.4 33/4096** (graded, v = 1/3, ample K) | implementation error |
| ROUTE | ROUTE-Z1 (L = 1), Z2 (v = 1/3), Z3 (L ≥ K_dec,base) | implementation error |
| ADAPT | ADAPT-Z1, Z2 | implementation error |
| all | the v1 replay slice (clean, unpaid, single consumer, S-DIRECT) reproduces `replay_results.json` | implementation error |

Any cell not listed here is **not** a control and carries no predicted value.

---

## 7. Outcome semantics

### 7.1 Per cell

**Value labels (unchanged from v2).** CERT-POS(X), CERT-ZERO(X), UNRESOLVED, INFEASIBLE, DEGENERATE.

**Response property P_X (new; Blocker (f)).** Each property is evaluated on one optimal `full`-class policy π
in exact arithmetic.

| Role | P_X(π) holds iff |
| --- | --- |
| SEL | the O-SEL response ΔV(π) < 0 strictly (by §8, cue_blind has ΔV = 0 exactly) |
| ACC | (i) π's reachable Q-configurations show ≥ 2 distinct `-` patterns; **and** (ii) at least one O-ACC flip is APPLICABLE with ΔV < 0 strictly. In paid cells, (i) must hold among **pre-decay** (phase-I) patterns, so that erasure alone cannot satisfy it. |
| UPK | (i) π's D-set varies with (evidence, cue) on a set of positive probability; **and** (ii) at least one APPLICABLE O-UPK withdrawal has ΔV < 0 strictly |
| ROUTE | the O-ROUTE response ΔV(π) < 0 strictly (static_route has ΔV = 0, §8) |
| ADAPT | **not evaluated.** ADAPT is value-only and no signature is claimed (flag F9). |

**Signature labels.** These are assigned only after the optimum set is complete, up to item symmetry.

| Label | Condition |
| --- | --- |
| ROBUST(X) | every optimum satisfies P_X |
| PERMITTED(X) | some but not all optima satisfy P_X |
| NONE(X) | no optimum satisfies P_X, and at least one optimum has an applicable operator |
| SIG-UNDEFINED(X) | the operator is NOT-APPLICABLE on every optimum |
| UNRESOLVED | the optimum set is not certified complete |

NOT-APPLICABLE never counts toward P_X.

### 7.2 Per role X

**ADMIT(X)** requires all of:
1. every §6 control for X passes;
2. CERT-POS(X) in at least one cell in each declared bin;
3. in each bin, at least one CERT-POS cell is labelled ROBUST(X) or PERMITTED(X) (PROPOSED). ROBUST counts are
   reported separately.
4. no control is UNRESOLVED.

**Bins.**

| Role | Bins |
| --- | --- |
| SEL, ACC | K / K_dec,base ∈ (0, 1/4], (1/4, 1/2], (1/2, 1). Restricted to frozen grid points. ACC bins use clean, unpaid cells only for storage-attributed claims. |
| ROUTE | L = 2, L = 3. L = 1 is a null control. |
| UPK | B_up ∈ {1, 2}. Clean cells give cue-attributed UPK claims; graded cells are reported only (§5.4). |

**Other verdicts and stop rule.** REJECT-ABSENT, REJECT-NARROW and UNRESOLVED are unchanged from v2. The stop
rule is unchanged: Stage B runs only for roles that reach CERT-POS, and a stage B that is not run is recorded as
"B not reached".

---

## 8. Intervention operators (v3)

**Cue-law-preserving kernel κ(c′ | c) (new).** Used by O-SEL and O-ROUTE.

- **Requirement.** Σ_c π(c) κ(c′|c) = π(c′), with c′ drawn independently of x given c.
- **Derangement version (c′ ≠ c).** This exists iff max π(c) ≤ 1/2, because the flow out of the largest cue
  must fit into the others.
  - Uniform: κ = uniform on the other two.
  - S1 (1/2, 1/4, 1/4): κ(·|0) = (0, 1/2, 1/2); κ(·|1) = κ(·|2) = (1, 0, 0). Check: column sums are
    1/4 + 1/4 = 1/2, 1/4 and 1/4.
  - S2 (2/3, 1/6, 1/6): **no derangement exists** (2/3 > 1/3).
- **Resample version.** κ(c′|c) = π(c′), allowing c′ = c. It is defined for every π.
- **Primary choice (PROPOSED).** Derangement for uniform and S1; resample for S2, labelled as such (flag F5).

**Operators.**

| Operator | Definition | Proved identity |
| --- | --- | --- |
| **O-SEL** | Encode under c; draw q from P(q \| c′), with c′ ~ κ(·\|c) | **cue_blind: ΔV = 0.** Its encoding depends only on x. c′ is independent of x with marginal π, so the joint law of (x, q) is unchanged. full: computed. |
| **O-ACC** | On a reachable Q-configuration m, flip **one** field q: answer → `-`, or `-` → p_guess-best bit. All other fields are unchanged. APPLICABLE only if m′ is reachable under the same policy; otherwise NOT-APPLICABLE. | **ΔV = P(m)·P(q \| m)·(r − p)** for answer→abstain, where p = P(stored answer correct \| m, q), computed from the posterior over (evidence, cue) that the encoder maps to m. **ΔV = P(m)·P(q \| m)·(p_guess − r)** for abstain→guess, where p_guess = max_b P(x_q = b \| m). p = 1 and p_guess = 1/2 are **not** assumed, not even with clean evidence. Under compression a stored answer can be wrong and an abstained item can be partly predictable. At an optimum ΔV ≤ 0 for every APPLICABLE flip, because the flipped policy is feasible: m is merged into the reachable m′. |
| **O-UPK** | At encoding, rewrite one D field j as F | **ΔV = −δ·Σ_m P(m)·P(q = j \| m)·(p_j(m) − r)** over configurations where j is D and answered. Under S-DIRECT, clean, uncompressed storage (p_j = 1) this reduces to −δ·P(q = j \| c)·(1 − r). In the §5.3 cell, field c gives −3/32. Withdrawing η's durability in stage B is computed, with no closed form. |
| **O-ROUTE** | Route under c; draw both consumers' queries under c′ ~ κ(·\|c) | **static_route: ΔV = 0.** Its messages are functions of EVstat only (§4.2), and (EVstat, q_A, q_B) has the same law under κ. This identity requires the v3 static_route definition. Under v2's definition (encoder-written fields) it did not follow. |

Dropped operators remain dropped (as in v2): the message swap; L-reduction as a lesion; "static router loses
uniformly"; the random_yoke prediction.

These remain representability statements about optima (Q-EXIST). Q-CAUSE in any developed system needs a
separately authorized study.

---

## 9. Scaffold accounting (v3)

| Role | Supplied | Chosen by optimization | Denied by rival | Later learner must acquire (ORIGIN: untested) |
| --- | --- | --- | --- | --- |
| SEL | cue access at encoding; field-per-query layout (S-DIRECT); K | cue-conditioned field map | cue dependence (cue_blind) | cue-conditioned retention in a generic state |
| ACC | the `-` action. **Under paid upkeep, visible erasure-to-`-` is SUPPLIED ACCESS (ruling (2)).** It is marked, never numerically subtracted. | which configurations abstain | state dependence of abstention | state-dependent abstention. Attribution against supplied erasure requires **matched scaffold controls**, e.g. an otherwise identical cell with hidden decay, designed later and separately approved. No additive decomposition is assumed. |
| ROUTE | message alphabet L; consumer decoders; the evidence-statistic fields (S-MSG) | message and decoder maps | cue dependence of messages | co-adapted sender/receiver conventions |
| UPK | the D/F write, unit cost, decay, per-field granularity | the D-set as a function of (evidence, cue) | evidence/cue dependence of the D-set | content-dependent maintenance without a designated durable operation |
| ADAPT | η field (charged, **paid upkeep**, not protected); feedback alphabet; timing (§4.3); the tracker set {T_const, T_H} | encoder/D-set given η; in full_B, also g | an optimized g | an acquired history update |

---

## 10. Adaptive rival

Unchanged from v2: the rival is necessary but is not an acquisition test. Two additions in v3:
- ADAPT is scoped to the tracker set {T_const, T_H};
- stationary ADAPT = 0 is now proved (§5.7).

---

## 11. Computation accounting

Unchanged from v2 §11:
- 10 CPU-min per cell, aggregated across workers, with restarts included;
- certificates checkpointed every 3 CPU-min;
- a timeout means UNRESOLVED;
- a 30-min sensitivity re-run is report-only.

The frozen outer K grid (§3.3) is part of the pre-search freeze.

---

## 12. Parameters

| Item | Status |
| --- | --- |
| a | 3/4 primary; 5/6 secondary |
| (a, r) null | **(3/5, 3/4) only** |
| (3/5, 5/8) | **Excluded on scope grounds** (limited grid). Its ACC_suff = 7/200 is recorded but is not the reason. |
| δ | **1/2 primary; 1/4 secondary.** The secondary's **decision role is frozen as report-only**: it cannot create, remove or change any CERT, signature or ADMIT/REJECT label. Expected scaling in the proved examples: UPK ∝ δ (5δ/48, 5δ/96, and the graded 33/4096 → 33/8192). |
| B_up | 1 primary; 2 secondary. Stage A controls are 0 and 3. **Stage B unpaid control is 4.** |
| History upkeep | **Charged: 1 unit per episode for durable η (ruling (1)).** No free register. |
| K | the frozen outer grid (§3.3) |
| H | 2 primary; {1, 3} report-only. T_2 and T_3 are as in §4.3. |
| h | 1/4 (PROPOSED); 0 for the stationary control |
| L (ROUTE) | null 1; positive bins {2, 3} (PROPOSED); sufficient ≥ 8 (clean) / 27 (graded) |
| Swap kernel | derangement for uniform and S1; resample for S2 (PROPOSED) |
| Time limit | 10 CPU-min per cell |

---

## 13. Thirteen admission answers (v2 retained, deltas marked)

| Q | Answer |
| --- | --- |
| Q1 | C3 bounded prerequisite: which W2′ conditions reward state-dependent retention, access, routing and upkeep allocation, and which remove that reward |
| Q2 | For each role X: does `full` strictly beat the X-denied class at equal per-phase reachable configurations (frozen K grid), under the declared semantics (S-DIRECT / S-MSG), across the bins, with the **proved** controls zero and the self-tests matched? |
| Q3 | Per-role REJECT-ABSENT / REJECT-NARROW. A control violation invalidates the card. |
| Q4 | Repaired adaptive_select with {T_const, T_H}; cue_blind, static_access, static_route (v3 information set), fixed_upkeep; selective prediction for graded ACC; **evidence-reliability allocation for graded UPK** (§5.4) |
| Q5 | SCARCITY_GAP_v1 §5 (replayed exactly); Astra RESPONSE A and Consult #6; Phase III/III-B; Phase II |
| Q6 | ADMITted roles and their signature labels feed a separately approved emergence design, with §9 as the scaffold ledger |
| Q7 | REJECT-ABSENT parks role X. REJECT-NARROW redesigns the family. UNRESOLVED preserves the open cells. |
| Q8 | Analytic certificate: exact enumeration, branch-and-bound, exact Markov limits. No neural model, no organism. |
| Q9 | Organizational cognition |
| Q10 | §14 |
| Q11 | C3. Q-LEARN, ORIGIN, Q-CAUSE and C4 remain unsupported. |
| Q12 | O0/N1 paid persistence, in field form; no O3 bridge. Supplied: the world, the decision points, upkeep, decay (visible erasure = supplied access), consumers and channel. |
| Q13 | ADMIT(X) updates the C3 ceiling. REJECT-* adds scoped collapse entries. ADAPT feeds REDUCTION only, and only against {T_const, T_H}. ORIGIN is unchanged. |

---

## 14. Claim ceiling

**Under ADMIT(X), the strongest claim is:** "In W2′, under the declared semantics, at equal per-phase reachable
configurations and matched observations, actions, upkeep and memory protection, certified bounds show that the
task rewards role X over the declared X-denied class across the declared bins, and the response property P_X
holds on some (PERMITTED) or all (ROBUST) optima."

**NOT established:**
- acquisition;
- causal use in a developed system;
- necessity beyond the declared classes;
- UPK results under decoder semantics;
- graded UPK as cue-driven;
- C4;
- an O3 bridge;
- consciousness.

---

## 15. Flags

- **F1. Mojibake (carried over).** Astra #6 says the mojibake did not drive its objections. The recommendation
  to send §§1–4 in ASCII before freezing stands.
- **F2. No protected controller or register.** Ruling (1) is applied: η is charged and pays upkeep. B_up = 3 is
  no longer the unpaid control in stage B (4 is). Nothing in v3 needed a protected element.
- **F3. Semantics choice.** S-DIRECT is adopted for every storage, upkeep and stage-B cell, and S-MSG for ROUTE.
  A decoder language for paid cells is **not** covered. If wanted, it needs its own proofs, because the UPK
  bounds may fail there.
- **F4. K_suff wording.** The Specialist wrote "minimum over phases of the maximum". I implemented Astra's
  "minimize the maximum reachable count across phases", i.e. min over optimal policies of max over phases. Please
  confirm.
- **F5. Swap kernel.** No derangement kernel preserves S2 = (2/3, 1/6, 1/6). Resampling is proposed for S2;
  it allows c′ = c, which dilutes O-SEL responses. The sweep is descriptive, so no decision depends on it.
- **F6. New hand counts.** These are the B_up = 2 phase counts (24, 20; 8, 12), UPK-Z4's K ≥ 18 and Z4′'s
  K ≥ 12, and K = 125 as ample. They are hand-derived and unverified by Astra.
- **F7. Graded UPK attribution.** 33/4096 shows that UPK in graded cells includes evidence-reliability
  allocation. Graded UPK is report-only, and cue-attributed UPK claims are clean-only. Astra may prefer a
  separate "reliability-UPK" contrast.
- **F8. ROUTE positive bins are unproved.** L ∈ {2, 3} positivity is not shown by hand. If the search certifies
  ROUTE = 0 in both, the result is REJECT-NARROW or REJECT-ABSENT, as designed.
- **F9. ADAPT has no response property.** ADAPT is value-only. If a signature is wanted (e.g. an η-lesion), it
  needs a definition.
- **F10. Signature gate.** The ADMIT requirement "ROBUST or PERMITTED in at least one CERT-POS cell per bin" is
  PROPOSED.
- **F11. The H = 3 tracker and η₀ = 2** are my specifications. Erasure resets to η₀, which for H = 3 is the
  neutral state.
