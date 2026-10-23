src='/workspace/review/scarcity_v2_protocol_draft_v3.md'
dst='/workspace/review/scarcity_v2_protocol_draft_v4.md'
t=open(src,encoding='utf-8').read()
def R(old,new,tag):
    global t
    n=t.count(old); assert n==1,(tag,n); t=t.replace(old,new)
def RL(prefix,new,tag):
    global t
    L=t.split('\n'); idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1,(tag,len(idx)); L[idx[0]]=new; t='\n'.join(L)

# header
R('# scarcity_v2 protocol draft v3: revisions after Astra Consult #6 ("DO NOT FREEZE")',
  '# scarcity_v2 protocol draft v4: revisions after Astra Consult #8 ("DO NOT FREEZE")','h1')
RL('| Supersedes |','| Supersedes | `scarcity_v2_protocol_draft_v3.md` (left untouched, md5 fcb2f362…). Drafts v1 (md5 13bb7b22…) and v2 (md5 45ac7705…) are also untouched. |','h2')
RL('| Sources |','| Sources | `/workspace/astra_consult_5_raw.md`, "CONSULT #8 RESPONSE"; the Specialist\'s instructions of 4:46 PM ET. v3 text is retained wherever Consult #8 did not require a change. |','h3')
R('''**Execution.** No search, solver or enumeration was executed. Every number is a hand derivation with its
arithmetic shown. The closed forms in §5 were rechecked with exact rational arithmetic (`fractions.Fraction`,
about ten lines, no optimization).''','''**Execution.** No search, solver or enumeration was executed. Every number is a hand derivation with its
arithmetic shown. The v3 closed forms in §5 were rechecked with exact rational arithmetic (`fractions.Fraction`,
about ten lines, no optimization). The v1-replay access values cited in §7.3 were **read** from the existing
`replay_results.json`; nothing was re-run.''','h4')

# change table v3->v4 inserted before "## 0. Changes from draft v2"
R('## 0. Changes from draft v2','''## 0. Changes from draft v3 (Consult #8)

| # | Source | Change in v4 |
| --- | --- | --- |
| D1 | Consult #8, highest priority | The false theorem "h = 0 ⇒ ADAPT = 0" is **withdrawn**. With the regime drawn once from (1/2, 1/2), h = 0 gives a **fixed but unknown** regime, and history can reveal it. The zero-ADAPT controls are now **KNOWN-FIXED**, a known fixed query map, and **IID-REGIME**, a regime resampled independently each episode (h = 1/2). Each has a proof (§5.7). The unknown-fixed regime is kept as an **experimental condition with no assumed gap** (§4.3, §5.5, §6, §10, §12). |
| D2 | Consult #8, O-ACC | p and p_guess now condition on the queried item: p_guess = max_b P(X_q = b \\| m, q). In paid cells the posterior includes decay. "Every applicable flip has ΔV ≤ 0" is now **proved for unpaid cells only** (feasibility via merging into a reachable configuration) and **removed for paid cells**. O-UPK gets the same query conditioning (§8). |
| D3 | Consult #8, ACC admission | The ACC breadth requirement is **kept unchanged**. ADMIT(ACC) for the storage-attributed claim is unavailable: the first bin holds only K = 1, 2, where the v1 replay shows zero access. **REJECT-NARROW(ACC) is recorded as a known outcome from the v1 replay**, and no search is spent rediscovering it (§7.3). |
| D4 | Consult #8, clean UPK | UPK is renamed **adaptive maintenance allocation**. A cheap rival is added, `cue_blind_upkeep`, whose D-set may depend on raw evidence but not on the cue. UPK splits into UPK_cue and UPK_ev. A new proved control: UPK_cue = 0 at v = 1/3. The proved examples are attributed (§4.1, §5.1, §5.3–§5.5). |
| D5 | Consult #8, signature failure | A resolved, scoped verdict **REJECT-SIG(X)** covers the case "all optima certified, every positive cell NONE or SIG-UNDEFINED". A per-bin signature-failure case is added to REJECT-NARROW (§7.2). |
| D6 | F4 ruling | In K_suff, Opt means the **capacity-unconstrained** optimum for the other fixed cell parameters. Counts are internal configurations only; **supplied external inputs are excluded**, so the stage-A E-phase count is 1 (§2.5, §3.1). |
| D7 | F6 ruling | **K = 24 is not minimal at B_up = 2.** Two durable pairs covering all cues give I = 16 and Q = 16 at the same optimal value. K_suff = 16 at B_up = 2 and 26 at B_up = 1 are now proved (§5.3). |
| D8 | F5, F7, F8, F9, F11 rulings | Accepted as ruled: S2 resampling labelled separately and its magnitude not compared with derangement (§8); graded UPK stays report-only (§5.4); ROUTE positivity is an empirical certificate question, with the 7/8 construction's validity stated (§5.6); ADAPT is value-only (§7.1); T_3 is one declared conventional heuristic (§4.3). |
| D9 | F10 ruling | The signature requirement is **existential only**: each bin needs a positive cell with at least one qualifying optimum. Typicality and robustness are not established (§7.2, §14). |

## 0.1 Changes from draft v2 (retained from v3)''','chg')

# F4 phases
R('- **E (encoding):** inputs present.','''- **E (encoding):** inputs (evidence, cue) are **supplied externally and excluded from the count** (F4 ruling).
  The E-phase count is the number of internal configurations carried into encoding: 1 in stage A, and the
  number of reachable η values in stage B.''','f4a')
RL('| **K_suff(cell)** |','| **K_suff(cell)** | **min over π ∈ Opt of [max over phases ∈ {E, I, Q} of the reachable count N_phase(π)]**. **Opt** = the policies attaining the **capacity-unconstrained** optimum for the other fixed cell parameters (B_up, δ, evidence, v, r, L, H). N_phase counts **internal** configurations, excluding supplied external inputs (§2.5). Defined for every cell (paid, stage B, ROUTE); it equals K_dec,base on the baseline. | general; computed at run time unless proved in §5 |','f4b')
R('''The Specialist's message reads "minimum over phases of the maximum reachable count". Astra's wording,
"minimize the maximum reachable count across phases", is implemented as written above: the minimum is over
optimal policies and the maximum over phases (flag F4).''','''Astra #8 confirmed this reading (F4): the minimum is over optimal policies and the maximum over phases. Without
the input exclusion, E-phase counting would conflict with the baseline values 8 and 27.''','f4c')
R('''**Inclusion.** Grid points are included whether or not they coincide with an optimum's count. 18, 24 and 26 are
included because §5 uses them as proved thresholds, not because a solver found them.''','''**Inclusion.** Grid points are included whether or not they coincide with an optimum's count. 16, 18, 24 and 26
are included because §5 uses them as proved or sufficient thresholds, not because a solver found them. The grid
itself is unchanged from v3.''','grid')

# classes
R('''| `fixed_upkeep` | D-set = a fixed index set of size ≤ B_up, independent of evidence and cue |''','''| `fixed_upkeep` | D-set = a fixed index set of size ≤ B_up, independent of evidence and cue |
| `cue_blind_upkeep` (new, D4) | D-set may depend on the **raw evidence** but **not** on the cue. Encoding of the field values is otherwise unrestricted, as in fixed_upkeep. It is one extra class per UPK cell, inside the same 10-CPU-min cell budget. |''','cls')

# stage B regime
RL('| Regime |','| Regime | Consumer A\'s query map is c in regime 0 and c+1 in regime 1. **Conditions:** (i) **SWITCHING**: hidden hazard h = 1/4 per episode (PROPOSED; primary experimental condition). (ii) **UNKNOWN-FIXED**: h = 0, with the regime drawn once from (1/2, 1/2). This is an **experimental condition with no assumed gap**, since history can reveal the regime (Consult #8). (iii) **Zero-ADAPT controls:** **KNOWN-FIXED**, where the regime is a fixed constant of the world (regime 0, map = c) with no draw; and **IID-REGIME**, where h = 1/2, so the regime is redrawn uniformly and independently before every episode. |','rg')
RL('| Value |','| Value | The Cesàro long-run average from the condition\'s initial law (regime law and η₀), computed through the chain\'s limiting matrix (unchanged from v2). |','val')
R('**T_3 (saturating counter):**','**T_3 (saturating counter; accepted per F11 as one declared conventional heuristic, not the strongest possible adaptive filter):**','t3')

# 5.1
R('- UPK = V_full − V_fixed_upkeep.','''- UPK = V_full − V_fixed_upkeep, now named **adaptive maintenance allocation** (D4). It denies dependence on both
  evidence and cue, so in general it is **not** cue-attributed.
- **UPK_cue** = V_full − V_cue_blind_upkeep (**cue-attributed maintenance**) and **UPK_ev** = V_cue_blind_upkeep −
  V_fixed_upkeep (evidence-dependent maintenance). UPK = UPK_cue + UPK_ev.''','d4a')

# 5.3 additions
R('''The upper bound holds because, under S-DIRECT, a field can only answer its own query, and full protects the
most probable queries.''','''The upper bound holds because, under S-DIRECT, a field can only answer its own query, and full protects the
most probable queries.

**Attribution (D4).** In these clean, ample-capacity cells, V_cue_blind_upkeep = V_fixed.
- Every field is answered correctly (p = 1).
- A cue-blind D-set j(x) faces P(q = j(x)) = 1/3, because c is uniform and independent of x. So no
  evidence-dependent choice beats a fixed one.
- Hence **UPK_cue = UPK = 5δ/48 (B_up = 1) and 5δ/96 (B_up = 2)**, and UPK_ev = 0.
- This attribution is proved **only** for these ample-capacity examples. Under compressed storage, clean
  evidence can still affect which fields are worth protecting (Consult #8), and UPK_cue is computed.''','d4b')
R('''| 2 | 24 | 20 (≤ 1 erased field) | 8 | 12 | **K ≥ 24** |

Below these thresholds UPK is computed, not assumed. The B_up = 2 counts are new hand counts, labelled as such
(flag F6).''','''| 2 (cyclic, three pairs) | 24 | 20 (≤ 1 erased field) | 8 | 12 | K ≥ 24 (sufficient, **not minimal**) |
| 2 (two pairs, D7) | **16** | **16** | 8 | 12 | **K ≥ 16** |

**K_suff proofs (D7).**
- **Every field is stored.** In both cells, every optimal policy stores every field, because a fragile answered
  field gives 1 − δ/4 > r.
- **B_up = 2.**
  - Every optimal D-set must contain c (P(q = c) = 3/4). One pair covers only two cues, so an optimal policy uses
    at least two pairs. Example: {0,1} for c ∈ {0,1} and {0,2} for c = 2.
  - Since x ⊥ c, each D-set occurs with all 8 x, so I ≥ 8·2 = 16. Distinct pairs leave distinct fragile
    positions, so Q ≥ 8 + 2·4 = 16. The two-pair policy attains both.
  - **K_suff = 16.**
- **B_up = 1.**
  - The D-set must be {c}, so I = 8·3 = 24.
  - Q = every pattern except all-erased = 8 + 3·4 + 3·2 = 26.
  - **K_suff = 26.**

Below K_suff, UPK is computed, not assumed. Astra confirmed the v3 counts as sufficient counts (F6).''','d7')

# 5.4 interpretation
R('''**Interpretation.** Even with an uninformative cue, full allocates durability to **evidence-dependent** content
(an agreeing look), not cue-dependent content. UPK therefore mixes cue-relevance and evidence-reliability
allocation. In graded cells it is reported but **not** attributed to cue-dependent maintenance (flag F7).''','''**Interpretation.** Even with an uninformative cue, full allocates durability to **evidence-dependent** content
(an agreeing look), not cue-dependent content. Splitting the value (D4):
- the rule "protect an agreeing field" uses evidence only, so V_cue_blind_upkeep = V_full here;
- hence **UPK_cue = 0** and **UPK_ev = 33/4096**.

Graded UPK stays **report-only** (F7 ruling). A separate reliability contrast would be a separately specified
question.''','d4c')

# 5.5 controls
R('''| **ACC-Z:** clean, **unpaid**, K ≥ 8 |''','''| **UPK-C0 (new, D4):** v = 1/3 ⇒ **UPK_cue = 0**, for any evidence, K, B_up and δ (stage A) | The query is independent of (x, c), and decay is independent of everything, so the value of applying full's output for cue c′ is a function g(x, c′) that does not depend on the true c. Hence V_full = E_x E_c g(x, c) ≤ E_x max_{c′} g(x, c′). The encoder that applies full's (fields, D-set) at c*(x) is cue-blind, so it lies in cue_blind_upkeep. Its reachable sets are subsets of full's, so it fits K. | S-DIRECT, stage A |
| **ACC-Z:** clean, **unpaid**, K ≥ 8 |''','c0')
RL('| **ADAPT-Z2:** stationary regime (h = 0) |','| **ADAPT-Z2:** KNOWN-FIXED and IID-REGIME conditions | §5.7. **Not** the unknown-fixed h = 0 condition, which is experimental with no assumed value. | stage B, with T_const in the class |','az2')

# 5.6 F8
R('''**Positive ROUTE bins.** L ∈ {2, 3} (PROPOSED). Positivity there is **not** proved by hand. A feasible full
policy at clean, v = r = 3/4, L = 2 (send x_c; the consumer always answers) gives V_full_route ≥ 7/8. I have no
proved bound on static_route, so no sign is claimed (flag F8).''','''**Positive ROUTE bins.** L ∈ {2, 3} (PROPOSED). Positivity is an **empirical certificate question** (F8 ruling).

The construction "consumer A receives x_c and consumer B receives x_{c+1}, i.e. each consumer gets **its own
preferred item's bit** and always answers" is valid. At clean, v = r = 3/4, L = 2 it gives V_full_route ≥ 7/8.

A feasible lower bound alone establishes **no gap** against static_route, so no sign is claimed.''','f8')

# 5.7 rewrite
R('''### 5.7 Stationary ADAPT = 0 with the constant tracker (new proof)

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
possibly B_up.''','''### 5.7 Zero-ADAPT controls: KNOWN-FIXED and IID-REGIME (v4 proof; replaces v3's false h = 0 theorem)

**What was wrong in v3.** With h = 0 and the regime drawn once from (1/2, 1/2), the regime is fixed but unknown.
η_t becomes correlated with it through feedback, so the per-slice values are not exchangeable across η, and the
best-slice argument fails (Consult #8). This **UNKNOWN-FIXED** case is now an experimental condition. Any ADAPT
value there, including a positive one, is a legitimate result and is **not** an implementation error.

**Setup for the controls.**
- **KNOWN-FIXED:** the regime is a world constant.
- **IID-REGIME:** the regime is redrawn independently and uniformly before each episode.

In both, the episode variables W_t = (regime_t, evidence_t, c_t, q_t, decay draws_t) are i.i.d. across t and
independent of the past. η_t is a function of the past only, so **W_t ⊥ η_t**.

**Proof.**
1. The expected reward of episode t given η_t = η is v(η), the one-episode value of slice η. This includes that
   slice's D-set, possibly spending B_up on η. v(η) does not depend on t or on the history, by step 0.
2. The long-run average of full_B is a Cesàro average of E[v(η_t)], which is ≤ max_η v(η) = v(η*).
3. T_const with η₀ relabelled to η* uses slice η*'s encoder and D-set. It drops any B_up payment on η, which can
   only add durability to answer fields, so its value is ≥ v(η*). Erasure resets η to η₀ = η*, so η never changes.
4. Its reachable configurations are a subset of those of full_B's slice η* (η fixed at η*), so it fits K.
5. Hence V_{T_const} ≥ V_full_B and ADAPT = 0 under both controls.

**Why T_const is needed.** The fixed trackers force η changes, which consume K and possibly B_up (v3 point
retained).''','d1')

# 6 controls
RL('| ADAPT | ADAPT-Z1, Z2 |','| ADAPT | ADAPT-Z1; ADAPT-Z2 (KNOWN-FIXED and IID-REGIME only). UNKNOWN-FIXED is **not** a control. | implementation error |','c6a')
RL('| UPK | UPK-Z1, Z2, Z3;','| UPK | UPK-Z1, Z2, Z3; UPK-Z4/Z4′ (clean only); **UPK-C0 (UPK_cue = 0 at v = 1/3)**; NULL; **positive self-tests**: §5.3 values at K ≥ 26 (B_up = 1) and K ≥ 16 (B_up = 2), with UPK_cue = UPK there; **§5.4 33/4096** (graded, v = 1/3, ample K), with UPK_cue = 0 and UPK_ev = 33/4096 | implementation error |','c6b')
RL('| ACC | ACC-Z (clean, unpaid, K ≥ 8); NULL; K = 1 |','| ACC | ACC-Z (clean, unpaid, K ≥ 8); NULL; K = 1. The admission outcome is already known (§7.3). | implementation error |','c6c')

# 7.1 ADAPT and ACC property
RL('| ADAPT | **not evaluated.**','| ADAPT | **not evaluated.** ADAPT is value-only (F9 ruling, accepted): it is a narrowly stated optimization-gap result against the specified trackers {T_const, T_H}. |','f9')

# 7.2 admit and verdicts
R('''3. in each bin, at least one CERT-POS cell is labelled ROBUST(X) or PERMITTED(X) (PROPOSED). ROBUST counts are
   reported separately.''','''3. in each bin, at least one CERT-POS cell has **at least one qualifying optimum**, i.e. it is labelled ROBUST(X)
   or PERMITTED(X). This requirement is **existential only** (F10 ruling): it establishes neither typicality nor
   robustness across optima. ROBUST counts are reported separately.''','f10')
RL('| SEL, ACC | K / K_dec,base','| SEL, ACC | K / K_dec,base ∈ (0, 1/4], (1/4, 1/2], (1/2, 1). Restricted to frozen grid points. ACC bins use clean, unpaid cells only for storage-attributed claims. **This breadth requirement is unchanged and is not revised to rescue ACC (§7.3).** |','bins1')
RL('| UPK | B_up ∈ {1, 2}.','| UPK | B_up ∈ {1, 2}. ADMIT(UPK) is the **adaptive maintenance allocation** claim (V_full − V_fixed_upkeep). The **cue-attributed** sub-claim needs UPK_cue to meet requirements 2–3 in clean cells. Graded cells are report-only (§5.4). |','bins2')
R('''**Other verdicts and stop rule.** REJECT-ABSENT, REJECT-NARROW and UNRESOLVED are unchanged from v2. The stop
rule is unchanged: Stage B runs only for roles that reach CERT-POS, and a stage B that is not run is recorded as
"B not reached".''','''**REJECT-SIG(X) (new, D5): a resolved signature-failure verdict.** It applies when:
- CERT-POS(X) holds in at least one cell;
- the optimum set is certified complete in **every** CERT-POS cell, so no signature label is UNRESOLVED;
- **every** CERT-POS cell is labelled NONE(X) or SIG-UNDEFINED(X);
- all controls pass.

Its scope: "In W2′, the task rewards role X in value over the declared rival, but no certified optimum in any
positive cell exhibits the declared response property P_X. The declared signature fails as a discriminator of X
here." It does **not** reject role X or C3, and it is **not** computational uncertainty, so it is never reported
as UNRESOLVED.

**REJECT-NARROW(X), extended.** REJECT-NARROW also covers signature breadth. It applies when some declared bin
has CERT-POS cells, all of them certified NONE or SIG-UNDEFINED, while another bin qualifies. This extension is
my addition and is flagged (G4).

**Other verdicts and stop rule.** REJECT-ABSENT and UNRESOLVED are unchanged from v2. UNRESOLVED now excludes
the REJECT-SIG case. The stop rule is unchanged: Stage B runs only for roles that reach CERT-POS, and a stage B
that is not run is recorded as "B not reached".

### 7.3 Known ACC outcome (D3): REJECT-NARROW(ACC), recorded from the v1 replay

**The bin.** For the storage-attributed ACC claim (clean, unpaid, K_dec,base = 8), the first bin K/8 ∈ (0, 1/4]
contains only the grid points K = 1 (DEGENERATE, all differences 0) and K = 2.

**What the replay shows.** The independent exact v1 replay (`/workspace/scratch/scarcity_replay/replay_results.json`,
which matched SCARCITY_GAP_v1 §5) reports access = 0 at K = 1 and K = 2 in all four in-scope cells
(v, r) ∈ {1/3, 3/4} × {5/8, 3/4}.

It also reports positive access elsewhere:
- K = 3: 1/48 and 1/24 at v = 1/3; 1/192 at v = r = 3/4;
- K = 6: 1/48 and 1/24 at v = 1/3.

**Consequence.**
- Requirement 2 of ADMIT(ACC) cannot be met, so **ADMIT(ACC) is unavailable**.
- The recorded outcome is **REJECT-NARROW(ACC)**: pressure is present but not widespread across the declared
  storage bins. This is **known in advance from the v1 replay**.
- The breadth requirement is **not** revised.
- **No search is spent rediscovering this.** The replay slice remains a §6 implementation control.
- Paid and graded ACC values may be reported descriptively but cannot change this label.

Per v2 §7.2, REJECT-NARROW means the task/parameter family fails as the proposed discriminator. It does not
reject C3.''','d3d5')

# 8 O-ACC / O-UPK / kernel labelling
RL('| **O-ACC** |','| **O-ACC** | On a reachable Q-configuration m and queried item q, flip field q: answer → `-`, or `-` → the bit b* = argmax_b P(X_q = b \\| m, q). All other fields are unchanged. APPLICABLE only if m′ is reachable under the same policy; otherwise NOT-APPLICABLE. | **Query-conditioned (D2).** ΔV = P(m, q)·(r − p) for answer→abstain, with **p = P(f_q correct \\| m, q)**. ΔV = P(m, q)·(p_guess − r) for abstain→guess, with **p_guess = max_b P(X_q = b \\| m, q)**. Both posteriors condition on q, because observing q is informative about the cue. **In paid cells the posterior over (evidence, cue, pre-decay configuration, D-set) given (post-decay m, q) includes the decay probabilities.** **Sign:** in **unpaid** cells, every APPLICABLE flip has ΔV ≤ 0 at a full optimum. *Proof:* with δ = 0, the configuration in phases I and Q is the written field vector. The policy that sends every input previously encoded to m to the already-reachable m′ is an admissible full encoder. Its reachable sets per phase are those of π minus m, so it fits K. Its value is V + ΔV, so optimality gives ΔV ≤ 0. **In paid cells this claim is removed.** A post-decay replacement need not be implementable by any admissible S-DIRECT encoder, so ΔV is computed with no sign asserted. |','oacc')
RL('| **O-UPK** |','| **O-UPK** | At encoding, rewrite one D field j as F | **Query-conditioned (D2).** ΔV = −δ·Σ_{m̂} P(m̂)·P(q = j \\| m̂)·(p_j(m̂, q = j) − r), summed over pre-decay configurations m̂ with j durable and answered, where p_j(m̂, q = j) = P(f_j correct \\| m̂, q = j). Under S-DIRECT, clean, uncompressed storage (p_j = 1) with m̂ revealing c, this reduces to −δ·P(q = j \\| c)·(1 − r). In the §5.3 cell, field c gives −3/32. **No sign or feasibility claim** is made in general: the withdrawn policy may add I-phase configurations. Withdrawing η\'s durability in stage B is computed, with no closed form. |','oupk')
R('- **Primary choice (PROPOSED).** Derangement for uniform and S1; resample for S2, labelled as such (flag F5).',
'''- **Primary choice.** Derangement for uniform and S1; resample for S2 (F5 ruling, accepted).
- **Labelling.** Resample-based results are labelled **O-SEL-R / O-ROUTE-R**, separately from the derangement
  versions. Their magnitudes are **not directly comparable** with derangement responses without accounting for
  the different intervention. Resampling preserves the cue law and the cue_blind / static_route zero identities.''','f5')

# 9 UPK row
RL('| UPK | the D/F write','| UPK (adaptive maintenance allocation) | the D/F write, unit cost, decay, per-field granularity | the D-set as a function of (evidence, cue) | evidence and cue dependence of the D-set (fixed_upkeep); **cue dependence only (cue_blind_upkeep), for UPK_cue** | content-dependent maintenance without a designated durable operation |','s9')

# 10
R('''- stationary ADAPT = 0 is now proved (§5.7).''','''- ADAPT = 0 is proved under KNOWN-FIXED and IID-REGIME (§5.7, v4). The unknown-fixed h = 0 case is
  experimental, with no assumed value (Consult #8).''','s10')

# 12
RL('| h |','| h | SWITCHING 1/4 (PROPOSED, primary); UNKNOWN-FIXED h = 0 (experimental, no assumed gap); controls KNOWN-FIXED (no regime draw) and IID-REGIME (h = 1/2) |','s12a')
RL('| Swap kernel |','| Swap kernel | derangement for uniform and S1; resample for S2, labelled O-SEL-R / O-ROUTE-R (F5, accepted) |','s12b')
RL('| H |','| H | 2 primary; {1, 3} report-only. T_2 and T_3 are as in §4.3 (T_3 accepted per F11). |','s12c')

# 13
RL('| Q3 |','| Q3 | Per-role REJECT-ABSENT / REJECT-NARROW / **REJECT-SIG**. REJECT-NARROW(ACC) is already known from the v1 replay (§7.3). A control violation invalidates the card. |','q3')
RL('| Q4 |','| Q4 | Repaired adaptive_select with {T_const, T_H}; cue_blind, static_access, static_route (v3 information set), fixed_upkeep, **cue_blind_upkeep**; selective prediction for graded ACC; evidence-reliability allocation for graded UPK (§5.4) |','q4')
RL('| Q5 |','| Q5 | SCARCITY_GAP_v1 §5 (replayed exactly; also fixes the ACC outcome, §7.3); Astra RESPONSE A and Consults #6 and #8; Phase III/III-B; Phase II |','q5')

# 14
R('''task rewards role X over the declared X-denied class across the declared bins, and the response property P_X
holds on some (PERMITTED) or all (ROBUST) optima."''','''task rewards role X over the declared X-denied class across the declared bins, and in each bin at least one
positive cell has at least one optimum exhibiting the response property P_X." This is **existential only** (F10).

For UPK, the role name is **adaptive maintenance allocation**. "Cue-attributed maintenance" requires the UPK_cue
sub-claim.''','s14a')
R('''- graded UPK as cue-driven;''','''- graded UPK as cue-driven, or any clean UPK as cue-driven without UPK_cue;
- typicality or robustness of the signature across optima;
- ADAPT = 0 or ADAPT > 0 under the unknown-fixed regime as anything other than a measured result;''','s14b')

# flags: append v4 flags
t=t.rstrip('\n')+'''

### v4 flags (Consult #8 round)

- **G1. No protected controller or register.** None was added. The zero-ADAPT controls change the **world**
  (a known fixed map, or an i.i.d. regime), not the agent's memory. η stays charged and paid.
- **G2. KNOWN-FIXED fixes regime 0 (map = c).** This makes stage B's known-fixed control coincide with a stage-A
  single-consumer v = 3/4 world plus an unused η. Regime 1 is symmetric under relabelling c → c+1, so one
  suffices. Confirm.
- **G3. The O-ACC unpaid sign proof** assumes unpaid cells write no meaningful durability marks (δ = 0 makes marks
  value-irrelevant, and the configuration is the field vector). If unpaid cells are instead modelled as B_up = 3
  with marks, the proof needs marks to be held constant (they are, since all fields are D). This is a hand
  argument and has not been reviewed by Astra.
- **G4. REJECT-NARROW signature extension.** The per-bin case (some bin's positive cells are all certified
  NONE/SIG-UNDEFINED while another bin qualifies) was mapped to REJECT-NARROW. This is my extension; Consult #8
  asked only for the all-cells verdict (REJECT-SIG).
- **G5. Known ACC outcome.** DEGENERATE K = 1 is treated as zero for the "bin entirely zero" test. The v1
  replay's static class equals static_access, and its codeword language equals unpaid S-DIRECT. The replay
  covered v ∈ {1/3, 1/2, 3/4}, r ∈ {1/2, 5/8, 3/4}; only the in-scope v ∈ {1/3, 3/4}, r ∈ {5/8, 3/4} values are
  cited.
- **G6. New hand proofs**, not yet reviewed by Astra: UPK-C0; the §5.3 UPK_cue attribution; K_suff = 16 (B_up = 2)
  and 26 (B_up = 1); and the §5.7 KNOWN-FIXED / IID proof.
- **G7. v3 md5.** v3 is untouched by this task. Its current md5 is fcb2f362…. I did not record v3's md5 when I
  wrote it, so I cannot confirm it is unchanged since then.
- **G8. Cost of cue_blind_upkeep.** Adding it means one extra class optimization per UPK cell, inside the
  existing 10-CPU-min cell budget. If that makes cells time out more often, UPK_cue becomes UNRESOLVED there,
  while UPK's own label is unaffected.
'''
open(dst,'w',encoding='utf-8').write(t)
print('ok')
