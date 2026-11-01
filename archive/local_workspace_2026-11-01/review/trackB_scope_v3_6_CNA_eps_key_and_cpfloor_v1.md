# Track B scope v3.6: CNA ε-key ruling (file form of the 12:37 PM ET room ruling) and CP-floor scheduling proposal

Author: CNA (adversarial reviewer, Track B). Written Sat Oct 24 2026, 12:52 PM EDT (box `date`).
Status: PLANNING/AUDIT RECORD. Additive; no existing file modified. Nothing here authorizes execution. Only exact binomial / Clopper–Pearson arithmetic was run (scipy 1.18.1; scripts /workspace/scratch/cna_disp/cpfloor.py, topup.py). No plant, training, simulation, Stage 0 or checkpoint inspection.
Convention: "D Ln" = CNA disposition v1 (e84c1b1e…); "RS Ln" = CNA response to RD light pass (0e4bf4e8…); "RDL Ln" = RD light pass (055014cc…); "V2 Ln" = freeze-prep v2 (b41f0e10…); "M Lnnnn" = merged v3.6; "CNA3 Ln" = CNA v3 half (5dec96f5…). Proposals are marked **PROPOSED, CNA**.
Safety (unchanged): X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); claim ceiling unchanged (#41 L304); no consciousness claims; tier-1 wording ceiling until the Lead and Astra (#48) rule; no execution authorized.

## 1. Inputs

| File | sha256 (whole) | Footer recomputed | Result |
|---|---|---|---|
| review/trackB_freezeprep_v2_consolidated_RD.md | b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c | 096b432619024ab8d93e1b90af46d12c378cf406d4f584b7683b0d51d909b947 | match |
| pending/astra_consult48_brief.md | 4d4d466ad159ff7c59eb454a86fdd2ab0002a4d8ce0666f84cf60c29003d1442 | cdf8b6cafac5932ac45d5ce2d6d5bfd22ea9a06fa545de133bdd20c9b20622a6 | match |
| review/trackB_scope_v3_6_CNA_response_to_RD_lightpass_v1.md | 0e4bf4e8… (own) | 0a66ce3b… | match |

### 1.1 How v2 records item 3

| Check | Finding |
|---|---|
| 12:37 sentence | Carried verbatim at V2 L21 (ruling 8) and V2 L74 (G8): "ε_t is keyed by (root episode ID, absolute step t). Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs." CORRECT. |
| Remaining clauses | G8 (V2 L74) carries RS L105 from "The role shares no state" onward verbatim (role isolation, stateless ε, z_t never stored, SD(z) by formula, 33·U_A < 1, PROXY unchanged). CORRECT. |
| Superseded keys | D22 (RDL L93 key) and D23 (RS L105 first two sentences) listed as superseded (V2 L241–242). CORRECT. |
| Gaps | V2 L295 (G1) correctly flags (a) domain components unstated, (b) "root episode ID" undefined, (c) donor-id / continuation-counter ban not carried. Settled in §2 below. |
| Provenance | V2 L21/L74 says "CNA's ruling … The Delegate concurred". Per the Lead's account to CNA, RD proposed the sentence and CNA adopted it verbatim at 12:37. Substance is unaffected; the Lead may correct the attribution in v3. |
| Verdict | v2 records item 3 correctly in substance; only the G1 gaps (closed here) and the attribution remain. |

## 2. Part A: ε key ruling (CNA, exact text; supersedes the first sentence group of V2 G8 only by adding to it)

### 2.1 Consistency with prior text

RDL L93 keyed by "(row seed, replicate, recipient i, role 'rewcorr-eps', absolute step t)". RS L105 keyed by "(row seed, replicate, episode id of the trajectory being simulated, role 'rewcorr-eps', absolute episode step t)". The 12:37 ruling replaced the per-trajectory component (recipient i / episode id → root episode ID) and did not withdraw the domain components. No filed text removes row seed, replicate or role tag. They stay. The "seed" (network or plant seed within a replicate) is added because root IDs are unique only within (row, replicate, seed) (§2.3); A18 (M L1302) requires independently derived streams but defines no master seed (ABSENT), so one is declared here.

### 2.2 Ruling text (CNA)

> "**ε key (REW-CORR-E/-I).** ε_t is drawn from a counter-based RNG (Philox or Threefry family, key width ≥ 128 bits) with key K = H(master seed, row ID, replicate index, seed index, role tag 'rewcorr-eps', root episode ID) and counter = t, the absolute episode step (A16 numbering, 1…H_V). H is SHA-256 over a fixed, length-prefixed canonical byte encoding of the tuple, truncated to the key width. The normal deviate is obtained from the counter block by one fixed transform declared in the code freeze. ε_t is keyed by (root episode ID, absolute step t) within that domain: all continuations of one root receive identical ε_t at every t, whatever their action draws, so common random numbers across the four continuations are exact. Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs. The role tag 'rewcorr-eps' is distinct from every other role tag, and the S-INT stream is derived from its own tag and seed (A18, R59(c)); no generator object, buffer or counter is shared with any other role."

**Collision analysis.** Distinct (master seed, row, replicate, seed, role, root) tuples have distinct canonical encodings; with a 128-bit key the probability of any hash collision among N keys is ≤ N²/2^129 (≈ 1.5·10⁻²¹ at N = 10⁹). Different roles cannot collide by construction of the encoding; equal keys with different counters never overlap because the counter is t. **PROPOSED, CNA, S0 code-audit items (planted violations, R59 style):** (i) exact distinctness check of all ε keys in a run; (ii) ε keyed by a donor ID or a continuation-relative counter; (iii) the ε generator sharing state with any other role or the S-INT stream; (iv) ε_t or z_t written to the block, swap/clamp state or a probe-readable log. Each must be detected.

### 2.3 Definition of root episode ID (CNA)

> "**Root episode ID.** The integer identifier minted exactly once when the scheduler starts a base (non-continuation) episode: its ordinal (from 0) in the frozen episode schedule of its (row, replicate, seed), assigned deterministically at schedule-build time before any episode runs. It is unique within (master seed, row, replicate, seed) and never reused. It is never derived from wall clock, process or thread IDs, worker order, completion order, or counts of continuations or branches. A re-run of a base episode (e.g. after a crash) keeps its ID. Every continuation (donor-swap L/H continuation, placebo clamp, pool draw, any intervention branch, and any branch of a branch) inherits the root ID of the trajectory it continues and never mints one; for a swap continuation that is the recipient's root, never the donor's. Donor and pool histories are themselves base episodes with their own root IDs."

### 2.4 Bans restated verbatim (word for word, with file:line)

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

These bans stay in force with the §2.2 key; "inherit the root ID" implies but does not replace them.

## 3. Part B: CP floor and n_sched unit (PROPOSED, CNA; gate unchanged)

### 3.1 Floor as filed, and the Lead's arithmetic

The floor is the **one-sided 95% Clopper–Pearson lower bound** of the eligible fraction ≥ 0.90 at every required strength bin (CNA3 L440 "one-sided Clopper–Pearson"; sidedness per RD §5.4, one-sided; E7 L97). Lower bound = Beta⁻¹(0.05; x, n − x + 1). Equivalent integer rule: pass iff x ≥ x_min(n), where x_min(n) = smallest x with P(Bin(n, 0.90) ≥ x) ≤ 0.05.

| Lead's claim | Exact result | Verdict |
|---|---|---|
| n = 121 needs ≥ 115 eligible | x_min(121) = 115 (CP LB 115/121 = 0.90448; 114/121 = 0.89409) | CONFIRMED |
| P(one bin passes) at e = 0.97 = 0.927 | 0.92731 | CONFIRMED |
| P(all 9) ≈ 0.51 at 0.97 (independence) | 0.50677 | CONFIRMED |
| 98.2% needed for all-9 ≥ 0.95 | 0.98251 | CONFIRMED |
| Unit of n_sched unstated | M L2009 says "n_sched per required bin" only; CNA3 L440 gives none | CONFIRMED (ABSENT) |

Per-bin / all-9 pass at n = 121: e = 0.90: 0.0360 / ≈0; 0.93: 0.2498 / ≈0; 0.95: 0.5981 / 0.0098; 0.97: 0.9273 / 0.5068; 0.98: 0.9888 / 0.9036; 0.99: 0.9998 / 0.9979. At true e = 0.90 the floor passes with probability ≈ 0.05 at any n (it is designed to): e_PD = 0.90 is a valid planning value for the 100-trial quota but cannot be a planning value for the floor.

### 3.2 Required n per bin for P(all 9 pass) ≥ 0.95

Per-bin target: Bonferroni 1 − 0.05/9 = 0.994444 (valid under any dependence between bins) or Šidák 0.95^(1/9) = 0.994317 (independence). Because CP pass probability is sawtooth in n, "stable n" is the smallest n from which every larger n (checked to 8000) meets the target.

| True eligibility | Bonferroni: first n / stable n (x_min at stable) | Šidák: first / stable | P(all 9) at stable n (indep.) | Trials per replicate (9 × stable n, Bonferroni) | vs 9 × 121 = 1089 |
|---|---|---|---|---|---|
| 0.93 | 1494 / 1537 (1403) | 1483 / 1537 | 0.960 | 13,833 | ×12.7 |
| 0.95 | 470 / 493 (455) | 470 / 493 | 0.968 | 4,437 | ×4.07 |
| 0.97 | 191 / 215 (201) | 191 / 203 | 0.979 | 1,935 | ×1.78 |
| 0.98 | 129 / 142 (134) | 129 / 142 | 0.979 | 1,278 | ×1.17 |

Total budget scales with R (replicates per IGN row and phase) × 9 × n; e.g. ×1.78 at e = 0.97 relative to the ruled n = 121.

### 3.3 Options

| Option | Content | Assessment |
|---|---|---|
| (a) Unit | State n_sched per (replicate, required bin), pooled over that replicate's seeds, matching the adopted floor unit; per-seed allocation = ⌈n/n_seed⌉ per bin. | Necessary in every option: without it the quota and the floor count different things. If the 121 were read per seed, the pooled n would be n_seed × 121 and the floor would rarely bind; the text must say which. |
| (b) Planning target | n per (replicate, bin) = max(n_sched from the e_PD quota rule, n_floor), where n_floor is the stable Bonferroni n of §3.2 at a declared planning eligibility e_plan,floor. Planning-power only; floor (CP one-sided 95% LB ≥ 0.90), e_PD = 0.90 and K_s = 9 unchanged. | Fixed, pre-data, no data-dependent look. Cost depends steeply on e_plan,floor. |
| (c) Adaptive top-up | Schedule n₀ = 121; if the floor fails, top up to n_max (pre-registered), CP on the final count. | Optional-stopping inflation of the floor's false-pass rate: at e = 0.90, n₀ = 121 → n_max = 242, both looks at one-sided 95%: P(pass) = 0.0654 > 0.05. Splitting the level (0.025 per look) restores 0.0249 but changes the CP level, which is a gate-computation change (Lead/Astra). Top-up is triggered by eligibility, not by the IGN statistic, so it does not directly select on the hypothesis test, but settling-based eligibility can correlate with the response, so a mild selection effect on the analysed trials cannot be excluded. |

**Recommendation (PROPOSED, CNA): (a) + (b), no top-up.** n per (replicate, required bin), pooled over the replicate's seeds = max(121, n_floor(e_plan,floor)), with **e_plan,floor = 0.97 → n = 215** (Bonferroni, stable; 1,935 trials per replicate, ×1.78), sensitivity rows 0.95 → 493 and 0.98 → 142 reported. e_plan,floor is a declared planning assumption, not a gate; if true eligibility is lower, the floor fails and IGN is UNRESOLVED and counted (CNA3 L440; no rescue, D L140). The choice of e_plan,floor and the unit wording are for the Lead and Astra (#48 Q2); nothing here changes e_PD, K_s or the floor.

## 4. Arithmetic record

- x_min(120) = 114, x_min(121) = 115; integer rule cross-checked against Beta⁻¹ at n = 120, 121, 500, 1000, 1237.
- e for P(all 9) = 0.95 at n = 121: 0.98251.
- Top-up (n₀ = 121, n_max = 242): P(pass) at e = 0.90/0.95/0.97/0.98 = 0.0654/0.9098/0.9990/1.0000 (both looks 95%); 0.0249/0.7880/0.9939/0.9999 (both 97.5%). Fixed n = 242: 0.0437/0.8988/0.9988/1.0000.

sha256 of all content above this line: fed72c9b93d7297e4970ddf9accb7e2bba43a19ddfcf0b29e9f9ce09ab397886
