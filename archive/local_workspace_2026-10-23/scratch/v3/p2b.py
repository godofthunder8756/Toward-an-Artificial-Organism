exec(open('h.py').read())
S26=f'''
**2.6 Claim-to-decision table (E42-1) [v3 C6].** Astra, verbatim: {ql(231)} Five claim types, never merged. CNA owns the rows and wording (CNA v3 §2, §4); RD owns the decision rules and multiplicity below. Bounds are one-sided at level 1 − α/m with α = 0.05 and m = 13 (§14 D10–D12).

| Claim type | Label (instrument) | Decision rule (RD) | Family member? | What it never licenses |
|---|---|---|---|---|
| Decoding advantage | C-EXIST / Q-EXIST, ΔR² vs joint baseline J (§2.7) | MET iff lower bound of ΔR² > m_EXIST = 0.05; NOT MET iff upper bound < 0.05; else BOUNDARY | yes (1) | use, self-model, E-specific use |
| Generic intervention dependence | C-CAUSE per declared function (E; I per §5c.2); C-NEC-DEP with the A-EXT veto (§3.4) | C-CAUSE: margin m_CAUSE = 0.05 on the stated behavioural probability; C-NEC-DEP: m_NEC = 0.20 on G; A-EXT: §3.3 | yes (C-CAUSE-E, C-CAUSE-I, Q-NEC dependence, A-EXT: 4) | that E (or I) is the information producing the effect. Astra: {q(59,'Decoding and causal use can coexist without referring to the same component.')} |
| Variable-attributed use | E-ATTR, I-ATTR (dissociation contrast, CNA v3 §4; §PC2); C-NEC-CONTENT (mediator-matched, CNA v3 §7.1(d)) | E-ATTR/I-ATTR: m_ATTR = 0.05 (CNA v3 §4.2); wording only per CNA v3 §4.4 | yes (3) | exclusive mediation; transfer of planted facts to trained agents |
| Observer-relative prediction advantage | SELF, one fixed conjunction (§5d; CNA v3 §6.3) | MET iff every required observer comparison clears m_SELF = 0.05 with the L_O floor | yes (1) | privileged information; introspection; optimal input-based prediction |
| Named-signal attribution | SIG-ATTR (CNA v3 §6.6) | only if a named signal is declared before freeze | no by default; +1 (m = 14) if a signal is declared | exclusive mediation |

Other primary labels in the family (unchanged in kind): Q-LEARN, IGN, BCAST broad routing, BCAST workspace advantage (4). Total m = 1 + 4 + 3 + 1 + 4 = **13** (§14 D11). Generic-dependence wording, verbatim: {q(55,'"The declared intervention on this direction/state changed behavior."')} Astra: {q(57,'It is insufficient for even the proposed stronger wording "consistent with E-specific use" if that wording is licensed merely by C-EXIST MET and a reported dissociation.')} That wording is withdrawn (CNA v3 §2).

**2.7 Joint history-plus-proxy comparator (E42-2; CNA-overlap, light-pass) [v3 C3].** Astra, verbatim: {ql(65)} **Adopted by cross-reference:** the Q-EXIST statistic is ΔR² = R²_final(state → E) − R²_final(J → E), with J as defined in CNA v3 §3.1 (one jointly fitted model on the W_B history window plus the proxy set; MLP and linear members; selection on the selection partition). History-only, proxy-only and max(H, P) are REPORTED diagnostics, never labelled. This replaces the max rule of CNA erratum 1 E4 and v2.1 L96/L172/L503 (CNA dependency D-RD4). Q-LEARN inherits it (§5.6). RD-owned inputs to J: W_B = max(16, 2·d_c) = 16 steps and τ_r = H_V/10 = 50 steps at the §14 D0–D1 defaults. Relay and memory capacity (#42 L219–220) are handled in CNA v3 §3.3 (§5e).
'''
S59=f'''
**5.9 Calibration, design selection and confirmation (E42-8) [v3 C14, C15].** Astra, verbatim: {ql(245)}
- **Three roles, three disjoint replicate sets**, each from its own dedicated, seeded and logged generator RNG stream, generated in the order below and never reused across roles (§14 D16):
  1. **Dose calibration (CNA v3 §8.3):** R_cal,dose = 50 replicates per plant that needs a fitted reference or κ_f. Sets doses only; enters no label and no n_seed computation (CNA dependency D-RD5).
  2. **Sample-size calibration (RD, §5.7):** R_cal,n = 200 replicates per generator and dose, used only to select n_seed, the executed-stop count check (§4.4) and coverage. Enters no label.
  3. **Confirmation:** R_rep = 200 fresh replicates per generator and dose (Astra #41 candidate). Only these produce Stage-0 labels and certified operating characteristics.
- **Design selection** (probe hyperparameters, IGN bins, t_r, comparator candidates) happens **inside** each replicate on its selection partition (§5.2), and is part of the frozen procedure, not a calibration role.
- **Frozen before calibration starts:** every grid (n_seed candidates {{9, 12, 16, 24, 32, 48, 63}}, the dose grids, the IGN t_r grid, the plateau-sweep grid of CNA v3 §6.3), the n_seed selection rule (§5.7 step 3), the heterogeneity range (OPEN FOR #43, §14 D13) and the coverage tolerance (§14 D14).
- **Frozen after calibration and before confirmation:** n_seed, κ_f doses, any fitted references. Nothing is revised after confirmation starts; a confirmation FAIL or UNRESOLVED leads to redesign and a new Astra review (§5.8).
- **Error-budget interpretation:** α controls **false MET only** (§5.4, §14 D10). The per-row bound supports 0.08 per declared plant and dose, never a battery-wide figure (#42 L152).
- **Bounded meaning of each operating-characteristic claim:** an OC certified in confirmation holds for that declared plant, dose and sample size only, under the ceiling sentence of §7. Astra: {q(150,'it is not automatically an operational error rate of one instrument.')}
'''
S5d=f'''
## 5d. SELF: gate, conjunction and RD-owned parameters (E42-3, E42-4; CNA-overlap, light-pass) [v3 C4–C6, C26]

- **Wording (verbatim, #42 L183):** {q(183,'SELF measures prediction advantage for simulated body variables over the declared observer family. Attribution to a privileged signal requires separate evidence concerning that signal.')} Named-signal attribution: CNA v3 §6.6.
- **Fixed required observer comparison; plateau route retired.** Astra: {q(17,'Count an all-required SELF conjunction as one family member; reject the proposed plateau exception as a substitute for a required observer comparison.')} and {q(37,'A credible stronger observer that closes the gap must not be bypassed because a smaller family appeared to plateau.')} **v2.1 V11's "or a pre-specified capacity and data sweep shows O-in's held-out loss has plateaued" is withdrawn** (it was a Lead-adopted PROPOSED DEFAULT; withdrawn as a #42-governed change). The plateau sweep is diagnostic only (CNA v3 §6.3).
- **Observer family and pathway matching:** CNA v3 §6.2 (§PC3). Required conjuncts: O-ACT-P (inputs + actions; family includes action-ignoring candidates, #42 L124) and O-IN-P (inputs only). O-HEAD is diagnostic (#42 L114).
- **Multiplicity:** the conjunction is **one** family member (Lead ruling). Astra: {q(21,'P(all comparisons pass) <= P(that null comparison passes) <= a.')} and {q(29,'Separate claims selected from individual observer comparisons need their own inferential treatment.')} Individual-observer comparisons are REPORTED, unlabelled.
- **Unresourced comparison:** Astra: {q(49,'If resources do not permit the required observer comparison, the privileged-information interpretation remains unresolved. A bounded small-observer comparison can still be reported.')} SELF then reads UNRESOLVED (CNA v3 §6.3).
- **RD-owned parameters (CNA dependency D-RD7; §14):** primary horizon h = 1 step (D3); observer-loss floor L_O ≥ 0.20·Var(y) (D21); Var(y) floor (D21); agent tuning budget 16 configurations × 3 initialization seeds and full archiving of training trajectories (D31).
- **AQ-SELF1:** descriptive secondary with no MET label (Lead ruling). Astra: {q(106,'q = 0.20 is defensible as a declared descriptive convention, not an optimal or paper-established value.')} and {q(108,'A secondary success cannot rescue primary SELF failure.')} Rules and the corrected Ashuach description: CNA v3 §6.4–§6.5 (CNA-overlap, light-pass). Astra's correction, verbatim: {q(94,'Ashuach et al. select examples where the underlying target and peer models have different correctness labels. Your proposal selects numerical disagreement between prediction heads. That is an adaptation, not the same analysis.')}
'''
S5e=f'''
## 5e. Astra #42 Q14 corrections and E42-5 (RD rules; CNA-overlap, light-pass) [v3 C12, C13]

Astra, verbatim: {ql(239)}

| #42 item (verbatim key clause) | Handling |
|---|---|
| {q(216,'BCAST-P1 cannot become a designated limitation because it fails its floor.')} | v2.1 §5c.1(a) clause struck (§5c); replacement CNA v3 §7.3(a). **General RD rule:** LIM roles are assigned before any result; a failed required positive is a failed or unavailable positive-control check and blocks that instrument |
| {q(217,'A required matched block cannot simply disappear because its restoration check fails.')} | v2.1 §5c.1(b) item 5 struck; replacement CNA v3 §7.3(b). **General RD rule:** comparator-family membership is frozen on the allowed partition; later failures make the comparison UNRESOLVED, never shrink the family |
| {q(218,'"Same band deviation" need not match the actual degradation mediator.')} | CNA v3 §7.1(d) (mediator-matched donors). RD supplies g and its memory length L_m (§14 D19; D-RD3) |
| {q(219,'The relay-negative construction must ensure that the baseline can represent the composed mapping, not merely share the probe\'s name.')} | CNA v3 §3.3 (composition-complete J for FF-RELAY) |
| {q(220,'Memory plants must match all permitted baseline information, including proxies, not just the observation window.')} | CNA v3 §3.3 (MEM pairs identical in every J input) |
| {q(221,'IGN settling exclusions need coverage checks at every required strength and transition bin.')} | CNA v3 §8.1 (per-bin coverage, else IGN UNRESOLVED); claim stated "under the declared settled-state response protocol" |
| {q(222,'The same results cannot select a sample size and certify its operating characteristics.')} | §5.7, §5.9 |
| {q(223,'The safety bookkeeping prohibition should say "no additional stop-associated reward, penalty or terminal return."')} | §4.1, §5b [v3 C1] |
| Q0: {q(5,'distinguish realization failure from eligibility failure in the stored reasons')} | §5.4 denominators; CNA v3 §5 stores r1/r2 separately |

These overturn two clauses of Lead-adopted v2.1 text (§5c.1) and one wording (§5c.3); the Lead accepted them at 2:39 PM ET. They are recorded as **#42-governed changes** (§9 C12, C17).

## 5f. Stage-L requirement for the AQ-2 architecture-imposed control (Lead ruling; #42 Q4) [v3 C16]

No trained arm is added now. Astra, verbatim: {ql(69)} Recorded requirement, verbatim: {q(71,'Record a Stage-L requirement now: any claim of acquired ignition must confront an architecture-imposed alternative under the relevant training and evaluation conditions. Common input histories and paired initialization remain necessary.')} and {q(73,'The later control must distinguish changes in occupancy or accessibility of an imposed regime from acquisition of the claimed mechanism.')} The Stage-0 plant: {q(75,'The existing Stage-0 plant can validate the statistic against its declared synthetic example. It cannot discharge that later requirement.')} Stage L remains unauthorized.
'''
open('new_sections.py','w').write('S26=%r\nS59=%r\nS5d=%r\nS5e=%r\n'%(S26,S59,S5d,S5e))
print('ok')
