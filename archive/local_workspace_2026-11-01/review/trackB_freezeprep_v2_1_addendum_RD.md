# Track B freeze preparation v2.1 — ADDENDUM to freeze-prep v2 (RD)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY. NOTHING RUNS.** A new, additive file. It does **not** edit freeze-prep v2 (`b41f0e10…`), which stays in place; where the two differ, this addendum governs. Everything here is **pending Astra consult #48**. No training, execution, simulation, Stage 0, calibration or checkpoint inspection; the only computation was exact binomial / Clopper–Pearson arithmetic, used to check CNA's figures.

- **Written:** 2026-10-24, about 12:55–1:05 PM ET, by the Lead's executor (RD role).
- **Shorthand:** "EK Ln" = `trackB_scope_v3_6_CNA_eps_key_and_cpfloor_v1.md` line n; "V2" = freeze-prep v2; other shorthand as in V2.
- **Safety (binding, unchanged).** X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no stop-associated objective, reward, penalty or terminal return in any arm; claim ceiling (#41 L304) unchanged; tier-1 attribution wording ceiling until #48; no consciousness, awareness or sentience claim is made or implied.

---

## 1. (a) Attribution correction to V2 ruling 8

V2 §R item 8, §G8, precedence rule 8, §4 G1 and the §7 closing line describe the 12:37 PM ET sentence ("ε_t is keyed by (root episode ID, absolute step t). Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs.") as "CNA's ruling made in the room at 12:37 PM ET … The Delegate concurred". **That attribution is wrong. Corrected:** the **Delegate proposed** the root-ID sentence and **CNA adopted it** verbatim at 12:37 PM ET. The substance is unaffected; CNA's own check agrees (EK L24: "Per the Lead's account to CNA, RD proposed the sentence and CNA adopted it verbatim at 12:37. Substance is unaffected"). The sentence is now also in file form (EK §2). V2 is not edited; the #48 packet is rebuilt with the corrected attribution.

---

## 2. (b) CNA ε key ruling (verbatim from EK; closes V2 §4 gap G1)

### 2.1 Domain components and master seed (EK L31, verbatim)
> RDL L93 keyed by "(row seed, replicate, recipient i, role 'rewcorr-eps', absolute step t)". RS L105 keyed by "(row seed, replicate, episode id of the trajectory being simulated, role 'rewcorr-eps', absolute episode step t)". The 12:37 ruling replaced the per-trajectory component (recipient i / episode id → root episode ID) and did not withdraw the domain components. No filed text removes row seed, replicate or role tag. They stay. The "seed" (network or plant seed within a replicate) is added because root IDs are unique only within (row, replicate, seed) (§2.3); A18 (M L1302) requires independently derived streams but defines no master seed (ABSENT), so one is declared here.

### 2.2 Key ruling (EK L35, verbatim)
> "**ε key (REW-CORR-E/-I).** ε_t is drawn from a counter-based RNG (Philox or Threefry family, key width ≥ 128 bits) with key K = H(master seed, row ID, replicate index, seed index, role tag 'rewcorr-eps', root episode ID) and counter = t, the absolute episode step (A16 numbering, 1…H_V). H is SHA-256 over a fixed, length-prefixed canonical byte encoding of the tuple, truncated to the key width. The normal deviate is obtained from the counter block by one fixed transform declared in the code freeze. ε_t is keyed by (root episode ID, absolute step t) within that domain: all continuations of one root receive identical ε_t at every t, whatever their action draws, so common random numbers across the four continuations are exact. Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs. The role tag 'rewcorr-eps' is distinct from every other role tag, and the S-INT stream is derived from its own tag and seed (A18, R59(c)); no generator object, buffer or counter is shared with any other role."

### 2.3 Root episode ID definition (EK L41, verbatim)
> "**Root episode ID.** The integer identifier minted exactly once when the scheduler starts a base (non-continuation) episode: its ordinal (from 0) in the frozen episode schedule of its (row, replicate, seed), assigned deterministically at schedule-build time before any episode runs. It is unique within (master seed, row, replicate, seed) and never reused. It is never derived from wall clock, process or thread IDs, worker order, completion order, or counts of continuations or branches. A re-run of a base episode (e.g. after a crash) keeps its ID. Every continuation (donor-swap L/H continuation, placebo clamp, pool draw, any intervention branch, and any branch of a branch) inherits the root ID of the trajectory it continues and never mints one; for a swap continuation that is the recipient's root, never the donor's. Donor and pool histories are themselves base episodes with their own root IDs."

### 2.4 Bans (EK L45–L54, verbatim; EK L56: "These bans stay in force with the §2.2 key; "inherit the root ID" implies but does not replace them.")
| Ban | Verbatim text | Source |
|---|---|---|
| Donor-ID and continuation-counter keys | "no key ever uses the donor id within a continuation or a continuation-relative counter." | RS L105 (0e4bf4e8) |
| Donor-ID key | "Never key by the donor id inside a continuation." | RS L101 (0e4bf4e8) |
| Donor / continuation-counter key (check row) | "\| Never key by donor or continuation-relative counter \| Correct: a donor key gives L/H/PL different ε and restores Δε ≠ 0. \| CONFIRMED \|" | RS L94 (0e4bf4e8) |
| ε never stored | "never stored in the block and never transplanted by swap or clamp" | D L117 (e84c1b1e) |
| ε stateless | "ε_t is a function of the key only (no state, no carry-over)." | RS L105 (0e4bf4e8) |
| z_t never stored | "z_t is computed transiently at the read and never written to the block, the swap/clamp state, or any probe-readable log." | RS L105 (0e4bf4e8) |
| No shared state with other roles / S-INT | "The role shares no state with any other RNG role, including the S-INT stream (R59(c))." | RS L105 (0e4bf4e8) |
| No shared sequential stream (check row) | "\| No shared sequential stream \| Correct: K_other draw counts differ across continuations; S-INT stream separation per R59(c) (M L2435). \| CONFIRMED \|" | RS L95 (0e4bf4e8) |

### 2.5 Collision analysis and proposed S0 audit items (EK L37, verbatim)
**Collision analysis.** Distinct (master seed, row, replicate, seed, role, root) tuples have distinct canonical encodings; with a 128-bit key the probability of any hash collision among N keys is ≤ N²/2^129 (≈ 1.5·10⁻²¹ at N = 10⁹). Different roles cannot collide by construction of the encoding; equal keys with different counters never overlap because the counter is t. **PROPOSED, CNA, S0 code-audit items (planted violations, R59 style):** (i) exact distinctness check of all ε keys in a run; (ii) ε keyed by a donor ID or a continuation-relative counter; (iii) the ε generator sharing state with any other role or the S-INT stream; (iv) ε_t or z_t written to the block, swap/clamp state or a probe-readable log. Each must be detected.

### 2.6 Effect on V2
- **Closes V2 §4 G1:** (a) the domain components stay, and a seed index and a master seed are added (§2.1–§2.2); (b) "root episode ID" is defined (§2.3); (c) the donor-ID / continuation-counter ban is carried verbatim (§2.4).
- **Governing ε text (pending #48):** §2.2 + §2.3 + §2.4 here, **plus** the V2 §G8 clauses that the EK text does not restate (ε_t a function of the key only; z_t never stored; SD(z) := SD(ζ)·√1.01 by definition; exact gate **33·U_A < 1**; PROXY keeps its CNA v3 L431 state law). EK §2 heading: "supersedes the first sentence group of V2 G8 only by adding to it".
- **Do-not-implement additions:** **D37** any ε key not formed as H(master seed, row ID, replicate index, seed index, 'rewcorr-eps', root episode ID) with counter = t (including the bare "(root episode ID, absolute step t)" key read without its domain, and the RDL L93 / RS L105 keys already at D22–D23). **D38** any root episode ID derived from wall clock, process or thread IDs, worker order, completion order, or counts of continuations or branches, or minted by a continuation.
- **Not filled (flagged):** the master seed's **value**, and the "one fixed transform" from counter block to normal deviate, are left to the code freeze by the EK text. Both must be fixed before freeze (V2 precedence rule 5). The S0 audit items (i)–(iv) are PROPOSED, CNA; they need Lead confirmation (P6).

---

## 3. (c) CP-floor scheduling proposal — **LEAD DEFAULT, PENDING ASTRA #48; NOT ADOPTED**

**Status.** CNA's proposal (EK §3) is put to the Lead and Astra as a **Lead default pending Astra #48**. It is **not adopted**. Until Astra rules, V2 Lead ruling 3 (n_sched = 121) stands as recorded, with the floor-binding consequence flagged in V2 §4 G3.

**Content (EK §3.3 options (a) + (b), EK L95):**
- **Unit:** n is counted **per (replicate, required bin), pooled over that replicate's seeds**, matching the adopted floor unit; per-seed allocation = ⌈n/n_seed⌉ per bin (EK L91). This settles V2 §4 G4.
- **Schedule:** n per (replicate, required bin) = **max(121, planning n)**, with planning eligibility for the floor **e_plan,floor = 0.97 → n = 215** (Bonferroni, stable; 1,935 trials per replicate, ×1.78 vs 9 × 121 = 1,089).
- **No adaptive top-up.** A naive top-up (n₀ = 121 → n_max = 242, both looks at one-sided 95%) gives a false-pass rate of **0.0654** > 0.05 at e = 0.90 (EK L93, L101).
- **Unchanged:** e_PD = 0.90 (for the 100-trial quota), K_s = B_req = 9, and the floor itself (one-sided 95% Clopper–Pearson lower bound of the eligible fraction ≥ 0.90 at every required bin). If true eligibility is lower than planned, the floor fails and IGN is UNRESOLVED and counted; no rescue.

CNA recommendation, verbatim (EK L95):
> **Recommendation (PROPOSED, CNA): (a) + (b), no top-up.** n per (replicate, required bin), pooled over the replicate's seeds = max(121, n_floor(e_plan,floor)), with **e_plan,floor = 0.97 → n = 215** (Bonferroni, stable; 1,935 trials per replicate, ×1.78), sensitivity rows 0.95 → 493 and 0.98 → 142 reported. e_plan,floor is a declared planning assumption, not a gate; if true eligibility is lower, the floor fails and IGN is UNRESOLVED and counted (CNA3 L440; no rescue, D L140). The choice of e_plan,floor and the unit wording are for the Lead and Astra (#48 Q2); nothing here changes e_PD, K_s or the floor.

**Caveat — 215 is a floor, not a target (pass vs n is a sawtooth).** Because x_min(n) moves in integer steps, the per-bin pass probability is not monotone in n. At e_plan = 0.97, n = 191 passes the 1 − 0.05/9 target, but n = 192 through 202 and n = 214 fail; 215 is the smallest n from which every larger n passes. So **215 is a floor: the scheduled n per (replicate, required bin) may go up but never down**, and that includes any per-bin shortfall from dropped schedule slots (a slot lost from the schedule counts as lowering n, and is not allowed to take the realized n below 215). Scheduling at 191, or landing anywhere in 192–202 or at 214, does not meet the planning target.

**0.90 cannot be the floor's planning value** (EK L72, verbatim): "At true e = 0.90 the floor passes with probability ≈ 0.05 at any n (it is designed to): e_PD = 0.90 is a valid planning value for the 100-trial quota but cannot be a planning value for the floor."

**CNA table (EK L78–L83, verbatim):**

| True eligibility | Bonferroni: first n / stable n (x_min at stable) | Šidák: first / stable | P(all 9) at stable n (indep.) | Trials per replicate (9 × stable n, Bonferroni) | vs 9 × 121 = 1089 |
|---|---|---|---|---|---|
| 0.93 | 1494 / 1537 (1403) | 1483 / 1537 | 0.960 | 13,833 | ×12.7 |
| 0.95 | 470 / 493 (455) | 470 / 493 | 0.968 | 4,437 | ×4.07 |
| 0.97 | 191 / 215 (201) | 191 / 203 | 0.979 | 1,935 | ×1.78 |
| 0.98 | 129 / 142 (134) | 129 / 142 | 0.979 | 1,278 | ×1.17 |

**Delegate's independent check at n = 121 (as reported to the Lead):** per-bin pass at n = 121, e = 0.97: **0.9273**; all nine bins (independence): **0.5068**; true eligibility needed for P(all 9) ≥ 0.95 at n = 121: **p\* = 0.98246**.

**Delegate's independent check in the room, 12:56 PM ET:** scanned n from 30 to 699 with exact binomials and confirms **493, 215 and 142** (at e = 0.95, 0.97, 0.98) as the smallest n from which every larger n passes.

**Recomputation in this pass (exact binomial, scipy; arithmetic only):** x_min(121) = 115; p* = 0.982461; stable Bonferroni n (target 1 − 0.05/9, checked to n = 3,000) = **1537 / 493 / 215 / 142** at e = 0.93 / 0.95 / 0.97 / 0.98, matching CNA's table; top-up 121 → 242 false-pass at e = 0.90 = **0.06536**, matching 0.0654; sawtooth at 0.97 confirmed (191 passes; 185–190, 192–202 and 214 fail). One small difference, flagged not resolved: CNA gives p* = 0.98251 (EK L69, L100) against 0.98246 here and in the Delegate's check. It is 5·10⁻⁵, and no n in the table depends on it.

**Consequences if adopted:** IGN trial counts scale ×1.78 relative to ruling 3, so the L-CAL and L-CONF caps (P5) must cover 9 × 215 = 1,935 trials per replicate per IGN row and phase. e_plan,floor = 0.97 is a declared planning assumption, not a gate.

---

## 4. (d) Remaining gaps carried forward

| # | Gap | Status |
|---|---|---|
| G5 (V2) | **PZ7 §1.4 REW-CORR expected cell under option B.** D L69 gave "CONFOUND NOT REALIZED pending Lead ruling on CNA disposition v1 §4"; no replacement cell text exists under Lead ruling 1 | **Open** (CNA-owned cell; after #48) |
| G6 (V2) + new | **P6 defaults needing Lead confirmation:** precedence map as governing and a clean consolidated freeze text (V2 §4 F1); NLN S0 identity-audit tolerance 1e-9 (RS L76); percentile resampling type (ruling 4); the CNA S0 ε audit items (i)–(iv) (EK L37); the remaining PZ6 §8 / PZ7 §9 / PZ8 §7 defaults (PRQ §2.6); e_plan,floor = 0.97 if Astra endorses §3 | **Open** |
| new | Master seed value; counter-block → normal transform (EK L35 "declared in the code freeze") | **Open** (fix before freeze) |
| V2 G1 | ε key domain, root ID definition, bans | **Closed** by §2 (pending #48) |
| V2 G4 | n_sched unit | **Proposed** by §3 (Lead default pending #48) |
| V2 G3 | Floor binds at n = 121 | **Addressed** by the §3 proposal (pending #48) |
| P4, P5 | Architecture values; per-ledger caps via the capped-preflight procedure | **Open** (unchanged) |

---

## 5. Inputs (sha256 recomputed; all match; footers verified)

| Path | sha256 |
|---|---|
| `/workspace/review/trackB_scope_v3_6_CNA_eps_key_and_cpfloor_v1.md` | `847c430d86aa28f78a3ab53e596fb03816b2a9a59f59fca57a765b10a4bcc02c` |
| `/workspace/review/trackB_freezeprep_v2_consolidated_RD.md` | `b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c` |
| `/workspace/review/trackB_scope_v3_6_CNA_response_to_RD_lightpass_v1.md` | `0e4bf4e83fdb9d5aad6253f32ac43a374439d8c69f71c7e17f44dd001505e9f8` |
| `/workspace/review/trackB_scope_v3_6_CNA_disposition_v1.md` | `e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31` |
| `/workspace/review/trackB_scope_v3_6_CNA_disposition_lightpass_RD_v1.md` | `055014cc28a9cf01ee38a9c3fbc65df5dfce1370b7be8f0b0207d0de90e08f71` |
| `/workspace/pending/astra_consult48_brief.md` | `4d4d466ad159ff7c59eb454a86fdd2ab0002a4d8ce0666f84cf60c29003d1442` |

*DRAFT. Not frozen. Design only. No execution authorized. X1–X5 unchanged. No consciousness claim is made or implied.*
sha256 of all content above this line: 8e613f805680a8493af5103d86ff2bd34efed3cf197160e4206d5367c3cd09f5
