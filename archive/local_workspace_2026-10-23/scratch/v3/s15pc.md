## 15. Settlement of CNA's dependencies on RD (CNA v3 §12) [v3 C25]

| ID | CNA dependency (verbatim, CNA v3 §12) | Settlement and section |
|---|---|---|
| D-RD1 | The environment spec must include metabolic-cost pulses and token events at λ = 4/H_V in training and evaluation (DISSOC support, §4.1; MEM, §3.3). It must also declare d_c, so that W_B = max(16, 2·d_c) is defined | **Settled.** Environment spec defaults §14 D0: pulses and tokens at λ = 4/H_V = 0.008/step in training and every evaluation world; d_c = 5, so W_B = 16 (D36). Layout items OPEN FOR #43 (D0). |
| D-RD2 | Multiplicity family: add E-ATTR, I-ATTR (each one member per declared function) and C-NEC-CONTENT (already in). The SELF conjunction is one member (§6.3). State whether α controls false MET only or both directions (#42 L156) | **Settled.** §2.6, §5.4: E-ATTR, I-ATTR and C-NEC-CONTENT are family members; SELF is one member; m = 13 (D11). **α controls false MET only** (D10; #42 L156). |
| D-RD3 | AQ-F1 must freeze g (the deviation-to-noise function) and its memory length L_m. DL-CONTENT (§7.1(d)) and the κ_f units depend on them | **Settled.** §14 D19: g(d) = min(1, d) with d in half-band units, memoryless, **L_m = 1**; κ_f units = noise SD per unit g, in units of s_core. |
| D-RD4 | Q-EXIST statistic (v2.1 §2.1 L96, §5.6 L503): replace max(H, P) with the joint J of §3.1. Q-LEARN inherits it. The individual baselines become diagnostics | **Settled.** §2 [v3 C3] and §2.7: max rule struck; Q-EXIST ΔR² vs J (CNA v3 §3.1); Q-LEARN inherits it (§5.6); H, P and max(H, P) REPORTED diagnostics. |
| D-RD5 | Calibration / selection / confirmation split (E42-8): CNA's R_cal = 50 dose-calibration replicates must sit outside the confirmation allocation and outside the n_seed calibration role | **Settled.** §5.9 and §14 D16: R_cal,dose = 50 sits outside confirmation (R_rep = 200) and outside the n_seed calibration set (R_cal,n = 200); disjoint RNG streams. |
| D-RD6 | v2.1 header P3 status → CLOSED (#42 L251). Retire v2.1 V11's plateau route (§6.3). Replace v2.1 §5c.1 (a) and (b) item 5 with §7.3, and §5c.3's arm wording with §7.4 | **Settled.** Header [v3 C2] (P3 CLOSED; correction for the record); §5d (V11 plateau route withdrawn); §5c struck clauses with CNA v3 §7.3(a), §7.3(b) and §7.4 as replacement text (Lead accepted, 2:39 PM ET). |
| D-RD7 | The SELF primary horizon h and the observer-loss floor L_O are RD's. The observers match the agent's cutoff and h. The agent's tuning budget and whether training trajectories are archived must be declared in the training protocol (§6.2) | **Settled.** §5d and §14: h = 1 (D3); L_O ≥ 0.20·Var(y) (D21); agent tuning budget 16 × 3 and full trajectory archiving (D31). |
| D-RD8 | A-EXT interface (#42 L13) is RD's. No CNA row depends on it beyond the unchanged A-EXT veto row | **Settled.** A-EXT stays RD-owned: §3.3 and §14 D17. |
| D-RD9 | The S-INT decoding label and origin (E42-6) are RD's. CNA §1.8 S-INT rows defer to it. The "Schedule-leak" row should use RD's at-risk or fixed-origin label | **Settled.** S-INT stays RD-owned: §4.3a and §14 D5–D8. The CNA "Schedule-leak" row uses the §4.3a next-step hazard label (fixed-origin label as its REPORTED secondary). |
| D-RD10 | Viability (E42-7): DL-NEC, DL-CONTENT and E-ATTR evaluations run under uninterrupted scheduled evaluation. Incomplete paired episodes follow RD's conservative rule; CNA rows add none of their own | **Settled.** §6 and §14 D20: uninterrupted scheduled evaluation and the incomplete-paired rule apply to DL-NEC, DL-CONTENT and E-ATTR/I-ATTR evaluations; CNA rows add no rule of their own. |

CNA values given as functions of RD quantities are concrete at the §14 defaults (D36).

---

## §PC1. MIXED-CODE plant (E42-2) — PENDING CNA FILE

Astra, verbatim: "Include a mixed-code plant: E is decodable beyond the baseline, but the downstream controller uses only a separate reward-related component. It should pass generic dependence and fail E-use attribution." (#42 L63) **Lead ruling (2:39 PM ET, CNA D1):** the raw wording governs — the plant must pass generic dependence and must fail E-use attribution. **Status: PENDING CNA FILE → filed** as CNA v3 §5 (`5dec96f5…`); content enters at the v3 merge. RD inputs: J (§2.7), family level (§14 D11–D12), floors (D21).

## §PC2. Labelled dissociation contrast (E42-1) — PENDING CNA FILE

Astra, verbatim: "For E-attributed conclusions, require a prespecified contrast in which E and reward-history information vary independently within declared support. Freeze the competing behavioral predictions and the relevant equivalence or effect margins. Apply the same principle to I and to content-attributed dependence." (#42 L61) **Status: PENDING CNA FILE → filed** as CNA v3 §4 (E-ATTR, I-ATTR, wording rule §4.4); content enters at the v3 merge. RD inputs: environment drivers (§14 D0), H_V (D1), family membership (§2.6), incomplete-pair rule (D20).

## §PC3. Observer pathway matching and budgets (E42-3) — PENDING CNA FILE

Astra, verbatim: "E42-3. Replace the SELF plateau exemption with a fixed required observer comparison. Account for the representation-producing pathway and training expenditure; keep smaller observers and plateau analyses diagnostic." (#42 L235) and "Charging only its head parameters against an observer's encoder-plus-head creates an asymmetric comparison." (#42 L112) "There is no uniquely correct parameter-count equation, but the accounting must expose rather than hide the asymmetry." (#42 L122) **Status: PENDING CNA FILE → filed** as CNA v3 §6.2–§6.3 (observer family, accounting table, plateau sweep diagnostic); content enters at the v3 merge. RD inputs: §5d, §14 D3, D21, D31.

## §PC4. Donor and intervention laws (E42-9) — PENDING CNA FILE

Astra, verbatim: "conditional donor construction" (#42 L13) (#42 L13 list) and "Match the declared coupling/noise law and relevant history. If matching removes all content variation or lacks support, CONTENT is unresolved." (#42 L218) **Status: PENDING CNA FILE → filed** as CNA v3 §7 (DL-CAUSE, DL-NEC, DL-ATTR, DL-CONTENT, DL-COV, DL-PATCH; comparator family §7.2; R5/R18 corrections §7.3–§7.4); content enters at the v3 merge. RD inputs: g and L_m (§14 D19), H_V (D1), comparator budget (D23).
