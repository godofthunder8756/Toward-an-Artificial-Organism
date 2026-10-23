src='/workspace/review/scarcity_v2_protocol_draft_v4.md'
dst='/workspace/review/scarcity_v2_protocol_FINAL.md'
t=open(src,encoding='utf-8').read()
def R(old,new,tag):
    global t
    n=t.count(old); assert n==1,(tag,n); t=t.replace(old,new)
def RL(prefix,new,tag):
    global t
    L=t.split('\n'); idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1,(tag,len(idx)); L[idx[0]]=new; t='\n'.join(L)

R('# scarcity_v2 protocol draft v4: revisions after Astra Consult #8 ("DO NOT FREEZE")',
  '# scarcity_v2 protocol FINAL: draft v4 plus Astra Consult #10 named edits ("FREEZE WITH NAMED EDITS")','title')
R('**Status: DRAFT. NOT FROZEN. NOT RUN.**','''**Status: FINAL TEXT FOR HASHING. NOT RUN.** The drafter did not freeze it. Freezing is the Specialist's step.
This file is `scarcity_v2_protocol_draft_v4.md` (md5 28c01ba1…, left untouched) plus only the Consult #10 edits
and flag rulings listed in §0.0. Drafts v1–v4 are untouched.''','status')

R('## 0. Changes from draft v3 (Consult #8)','''## 0.0 Edits applied (Astra Consult #10: FREEZE WITH NAMED EDITS)

Source: `/workspace/astra_consult10_response.txt`.

| Consult #10 item | Section(s) changed |
| --- | --- |
| Edit 1: B = 2 capacity proof (≥ 8×2 I-phase configurations; K_suff = 16) | §5.3, K_suff proofs, B_up = 2 |
| Edit 2: zero-ADAPT construction (register fixed at η₀, encoder reproduces η*, no register-durability payment, T_const; configuration-count sentence) | §5.7, proof steps 3–4 |
| Edit 3: unpaid cells canonicalized to field vectors; UPK-C0 on the observed evidence statistic e with conditional expected reward g(e, c′) | §2.6 (new canonicalization note); §5.5 UPK-C0 row; §15 G3 |
| Edit 4: withdrawal event specified; −3/32 self-test = "On every episode, downgrade the cued field j = c from D to F"; configuration-field withdrawals for general signature evaluation | §8 O-UPK row; §7.1 UPK property |
| Edit 5: unresolved-cell loopholes closed in REJECT-SIG and signature REJECT-NARROW; UNRESOLVED if unresolved cells could qualify; precedence REJECT-ABSENT > REJECT-SIG > REJECT-NARROW; ACC replay record preserved | §7.2 |
| Edit 6: deterministic search accounting (class order, certificate preservation, budget allocation); B_up = 2 decision-bearing for UPK breadth | §11; §12 B_up row |
| G2 accepted | §15 G2 |
| G4 accepted with edit 5 | §15 G4; §7.2 |
| G5 accepted | §15 G5 |
| G8 accepted with qualification (an unfinished required control still blocks family-level ADMIT) | §15 G8; §11 |

**Scratch verification** (outside the repo): `/workspace/scratch/scarcity_final/check.py`, log in `check.log`.
Exact rational arithmetic confirms:
- the minimum is 2 distinct durable pairs per x, so I ≥ 16;
- the two-fixed-pair policy has I = 16, Q = 16 and value 63/64;
- V_full(B_up = 1) = 31/32;
- downgrading the cued field every episode gives ΔV = −3/32;
- downgrading fixed field j = 0 whenever durable gives −1/32.

No search or experiment was run.

## 0. Changes from draft v3 (Consult #8)''','table')

# Edit 1
R('''  - Every optimal D-set must contain c (P(q = c) = 3/4). One pair covers only two cues, so an optimal policy uses
    at least two pairs. Example: {0,1} for c ∈ {0,1} and {0,2} for c = 2.
  - Since x ⊥ c, each D-set occurs with all 8 x, so I ≥ 8·2 = 16. Distinct pairs leave distinct fragile
    positions, so Q ≥ 8 + 2·4 = 16. The two-pair policy attains both.
  - **K_suff = 16.**''','''  - For each fixed item vector x, all three cues have positive probability. An optimal policy answers every field
    correctly and uses a durable pair containing the cue. Therefore it needs at least two distinct durable pairs
    for each x. Different item vectors have different field values, giving at least 8×2 = 16 I-phase
    configurations. The displayed policy using two fixed pairs attains I = 16 and Q = 16. Hence K_suff = 16.
  - Example of the displayed policy: {0,1} for c ∈ {0,1} and {0,2} for c = 2.
  - Independence does not make an evidence-dependent D-set independent of x. A universal Q-phase lower bound is
    unnecessary.
  - **K_suff = 16.**''','e1')

# Edit 2
R('''3. T_const with η₀ relabelled to η* uses slice η*'s encoder and D-set. It drops any B_up payment on η, which can
   only add durability to answer fields, so its value is ≥ v(η*). Erasure resets η to η₀ = η*, so η never changes.
4. Its reachable configurations are a subset of those of full_B's slice η* (η fixed at η*), so it fits K.''','''3. Under T_const the register is kept **physically fixed at the declared η₀**. Its encoder is defined to
   **reproduce the best slice η\\***: at η₀ it writes exactly the answer values and answer-durability choices that
   full_B's slice η* writes. Those are left unchanged, and any register-durability payment is removed. Register
   durability does not affect answer rewards, and erasure resets η to η₀, so the register never changes and its
   value is v(η*).
4. Mapping register values to η₀ and removing its durability mark cannot increase the number of reachable
   configurations.''','e2')

# Edit 3
R('''**Equivalence note.** In unpaid single-consumer cells,''','''**Unpaid canonicalization (Consult #10, edit 3).** Unpaid S-DIRECT cells use **field vectors only**, with
durability marks omitted or uniquely determined by those vectors. The configuration in every phase of an unpaid
cell is the written field vector.

**Equivalence note.** In unpaid single-consumer cells,''','e3a')
RL('| **UPK-C0 (new, D4):**','| **UPK-C0 (new, D4):** v = 1/3 ⇒ **UPK_cue = 0**, for any evidence, K, B_up and δ (stage A) | Let e be the **observed evidence statistic** (e = x for clean evidence, e = (n₀, n₁, n₂) for graded), not the latent x. The query is independent of (e, c), and decay is independent of everything. Define **g(e, c′)** as the conditional expected reward, given e, of applying full\'s output for cue c′. It does not depend on the true c. Hence V_full = E_e E_c g(e, c) ≤ E_e max_{c′} g(e, c′). Then selecting c*(e) is an admissible encoder: it applies full\'s (fields, D-set) at c*(e), is a function of e only and hence cue-blind, and so lies in cue_blind_upkeep. Its reachable sets are subsets of full\'s, so it fits K. | S-DIRECT, stage A |','e3b')
R('''- **G3. The O-ACC unpaid sign proof** assumes''','''- **G3 (resolved by Consult #10, edit 3: unpaid cells are canonicalized to field vectors, §2.6).** *Original flag:* **The O-ACC unpaid sign proof** assumes''','e3c')

# Edit 4
RL('| **O-UPK** |','| **O-UPK** | At encoding, downgrade one D field from D to F on **explicitly identified encoding events** | **Withdrawal event (Consult #10, edit 4).** An O-UPK result must identify both the field and the encoding events on which it is downgraded. **For the −3/32 self-test: On every episode, downgrade the cued field j = c from D to F.** In the §5.3 cell (B_up = 1) this gives −δ·P(q = c \\| c)·(1 − r) = −(1/2)(3/4)(1/4) = −3/32. Withdrawing one fixed field j whenever it is durable instead gives −1/32 in that example; that is a different event. **For general signature evaluation, use explicitly identified configuration-field withdrawals, integrating their event probabilities.** This prevents confusing a conditional loss with a whole-distribution loss. **Query-conditioned (D2).** For a withdrawal of field j on the event set A of pre-decay configurations m̂ (j durable and answered): ΔV = −δ·Σ_{m̂ ∈ A} P(m̂)·P(q = j \\| m̂)·(p_j(m̂, q = j) − r), where p_j(m̂, q = j) = P(f_j correct \\| m̂, q = j). **No sign or feasibility claim** is made in general: the withdrawn policy may add I-phase configurations. Withdrawing η\'s durability in stage B is computed, with no closed form. |','e4a')
R('''at least one APPLICABLE O-UPK withdrawal has ΔV < 0 strictly''','''at least one APPLICABLE O-UPK withdrawal, an explicitly identified configuration-field withdrawal (§8), has ΔV < 0 strictly''','e4b')

# Edit 5
R('''**REJECT-SIG(X) (new, D5): a resolved signature-failure verdict.** It applies when:
- CERT-POS(X) holds in at least one cell;
- the optimum set is certified complete in **every** CERT-POS cell, so no signature label is UNRESOLVED;''','''**REJECT-SIG(X) (new, D5): a resolved signature-failure verdict.** It applies when:
- CERT-POS(X) holds in at least one cell;
- **every in-scope cell's value status is resolved** (Consult #10, edit 5): no in-scope cell has an UNRESOLVED
  value label;
- the optimum set is certified complete in **every** CERT-POS cell, so no signature label is UNRESOLVED;''','e5a')
R('''**REJECT-NARROW(X), extended.** REJECT-NARROW also covers signature breadth. It applies when some declared bin
has CERT-POS cells, all of them certified NONE or SIG-UNDEFINED, while another bin qualifies. This extension is
my addition and is flagged (G4).''','''**REJECT-NARROW(X), extended (G4 accepted with Consult #10, edit 5).** REJECT-NARROW also covers signature
breadth. Signature-based REJECT-NARROW requires all of the following:
- **every value status in the failing bin is resolved**;
- **every positive cell there is certified NONE/SIG-UNDEFINED**;
- **another bin must qualify**.

**Unresolved cells.** If unresolved cells could supply a qualifying optimum, use **UNRESOLVED**.

**Precedence.** Where rejection categories overlap, use **REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW**.
ACC's separately established, replay-based REJECT-NARROW record (§7.3) is preserved.''','e5b')

# Edit 6
R('''The frozen outer K grid (§3.3) is part of the pre-search freeze.''','''The frozen outer K grid (§3.3) is part of the pre-search freeze.

**Deterministic search accounting (Consult #10, edit 6).** These rules are frozen with the protocol.

**Class-search order within a cell:**
1. `full` (value, then all-optima certification, then the §8 intervention / signature analysis);
2. the role-denied rivals present in the cell, in this fixed order: `cue_blind`, `static_access`,
   `fixed_upkeep`, `cue_blind_upkeep`, `static_route` (ROUTE cells contain only `full_route` and `static_route`);
3. stage B: `full_B`, then `adaptive_select` with T_const, then with T_H.

**Allocation of the shared ten-minute budget.**
- `full`'s value search, all-optima certification and signature analysis receive the first 4 CPU-min.
- The remaining 6 CPU-min are split equally among that cell's rivals in the order above.
- Unused time rolls forward to the next class in order.
- Time left after the last rival returns to `full`'s unfinished certification or signature analysis, if any.
- The 3-CPU-min checkpoints are taken on cumulative cell time.

**Certificate preservation.**
- Every completed value certificate, all-optima certificate and signature label is written to the cell record
  at completion and at each checkpoint.
- **Completed value and signature certificates are preserved when another class times out.** A timeout makes
  only the role differences that need the unfinished class UNRESOLVED.
- Per G8 (accepted with qualification): a timeout can leave UPK certified while UPK_cue remains UNRESOLVED.
  However, **an unfinished required control still blocks the corresponding family-level ADMIT** under the
  declared rules (§7.2 requirement 4).''','e6a')
RL('| B_up | 1 primary','| B_up | 1 primary; 2 secondary. **B_up = 2 is explicitly decision-bearing for the UPK breadth test** (§7.2 bins B_up ∈ {1, 2}), despite being called "secondary". It is not report-only like secondary δ. Stage A controls are 0 and 3. **Stage B unpaid control is 4.** |','e6b')

# Flags
R('''- **G2. KNOWN-FIXED fixes regime 0 (map = c).**''','''- **G2 (ACCEPTED, Consult #10).** KNOWN-FIXED regime 0 is the stage-A map with an unnecessary register. Regime 1
  is equivalent by relabelling the cue and its distribution. *Original flag:* **KNOWN-FIXED fixes regime 0 (map = c).**''','g2')
R('''- **G4. REJECT-NARROW signature extension.**''','''- **G4 (ACCEPTED with Consult #10 edit 5).** Per-bin signature failure is legitimate narrowness, provided the
  failing bin is fully resolved (§7.2). *Original flag:* **REJECT-NARROW signature extension.**''','g4')
R('''- **G5. Known ACC outcome.**''','''- **G5 (ACCEPTED, Consult #10).** A proven zero at degenerate K = 1 counts as zero for breadth, while remaining
  labelled DEGENERATE. The known ACC outcome appropriately prevents redundant discovery work. *Original flag:* **Known ACC outcome.**''','g5')
R('''- **G8. Cost of cue_blind_upkeep.**''','''- **G8 (ACCEPTED WITH QUALIFICATION, Consult #10).** A timeout can leave UPK certified while UPK_cue remains
  UNRESOLVED. However, an unfinished required control still blocks the corresponding family-level ADMIT under the
  declared rules (§11, §7.2). *Original flag:* **Cost of cue_blind_upkeep.**''','g8')
open(dst,'w',encoding='utf-8').write(t); print('ok')
