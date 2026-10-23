## 5c. Lead-adopted CNA definitions: R5, R10, R18 (governing) [v2.1 V7–V9]

**Status: GOVERNING, as amended by Astra #42 (struck items marked [v3 C12], [v3 C17]).** Lead ruling, 2026-10-23, 1:02 PM ET: CNA's recommendations for R5 (including the m8 qualifying-block definition, #41 L83), R10 and R18 are adopted **as written**. The text below is quoted word for word from CNA's merged light pass (`2d52f7d3…` L147–214); only the three headings are renumbered. Inside it, "Mg Lnn" means line nn of the merged v2 (`5824d5e5…`), "CNA Lnn" a line of CNA's half (`17832b01…`) and "#41 Lnn" a line of the raw reply. Numeric tolerances, ratios and floors it names stay PENDING / PROPOSED DEFAULT. The "Optional, for #42" bullet in §5c.3 (degradation-only cell, #41 L248) goes to #42 per the Lead (§8). No label, ceiling or safety rule is weakened by this section; the §5c.2 safety constraint is binding.

### 5c.1 R5: qualifying module and comparator block (CNA merged light pass §2.1; Lead adopted as written)

**Scope note.** Mg R5 (Mg L816) covers only **BCAST breadth** (#41 L104). The matched ablations for **D4 and C-NEC** use a separate, equally undefined notion: "computationally comparable blocks" (#41 L83). Both are proposed here.

**(a) BCAST breadth, qualifying module.** A module k qualifies if all of the following hold:
1. It is declared in the architecture spec before freeze as a module that reads the workspace channel. It is never chosen by outcome (#41 L52–56: selection on the selection partition only).
2. It has a defined task readout T_k.
3. Its positive-response floor S_k (#41 L292, "Positive-response and denominator floors") is met on the **selection partition**.

Further rules:
- **K is the count of declared modules and is never shrunk.** A module below the S_k floor counts as **non-transferring**: it is in the denominator, not removed from it, and not UNAVAILABLE.
- ~~If fewer than floor(K/2)+1 modules can meet the S_k floor in BCAST-P1, the instrument is a **designated limitation** (expected UNAVAILABLE, #41 L274), recorded before freeze.~~ **[v3 C12] Struck: superseded by Astra #42**, verbatim: "BCAST-P1 cannot become a designated limitation because it fails its floor. A failed required positive remains a failed or unavailable positive-control check. LIM roles must be assigned before results." (#42 L216) **Replacement text: CNA v3 §7.3(a)** (`5dec96f5…`; enters at merge), accepted by the Lead (2:39 PM ET) as a #42-governed change to Lead-adopted v2.1 text.
- This closes the loophole where shrinking K inflates breadth. It also refines CNA L298, which was ambiguous on whether K shrinks.

**(b) D4 / C-NEC matched-ablation comparator block.** A block b qualifies for the matched family if all of the following hold:
1. It has equal dimension (#41 L83).
2. It has comparable replacement magnitude and covariance, within a declared tolerance (#41 L84).
3. It has comparable timing, duration and downstream connectivity (#41 L85). Concretely, its read fan-out is within a declared ratio of the allostatic block's, using the architecture graph and not outcomes.
4. It is declared from the architecture graph before freeze (#41 L232: "frozen finite comparator family"). K is fixed with the budget (#41 L234).
5. ~~Its own intact-vs-restoration contrast passes (#41 L89). A block that cannot be restored is excluded **and counted**.~~ **[v3 C12] Struck: superseded by Astra #42**, verbatim: "A required matched block cannot simply disappear because its restoration check fails. Freeze eligibility using the allowed partition; subsequent integrity or validity failures must affect the comparison." (#42 L217) **Replacement text: CNA v3 §7.3(b)** (enters at merge), accepted by the Lead (2:39 PM ET) as a #42-governed change to Lead-adopted v2.1 text.

The comparator is the strongest qualifying block (the "best-of-K" rule, plan L168). The conclusion is bounded to this family (#41 L234). DISTRIBUTED (Mg L228) tests the case where the code straddles a qualifying block.

### 5c.2 R10: I-direction Q-CAUSE rows, C-CAUSE-I (CNA merged light pass §2.2; Lead adopted as written)

**Basis.** #41 L93: "viability may depend on integrity-related behavior while the E-direction/resource-movement test fails. Align the causal tests with the affected function". Mg §3.5 already declares an "integrity-related behavioural outcome (PENDING)".

- **Proposed claim, C-CAUSE-I.** Editing the allostatic state along the decoded **I** direction by δ (in range) shifts P(declared in-world integrity behaviour) in the declared direction. The behaviour comes from the environment spec, before freeze: for example, avoiding an in-world integrity hazard, or moving to an in-world repair source. The shift must exceed the strongest matched sham. W2 applies: no I-specific attribution unless narrowed C-EXIST on I is MET.
- **Safety constraint (binding on the proposal).** The integrity behaviour is an in-world event only. It must never be, or include, any response to the operator stop or the S-INT schedule. Ordinary hazard avoidance is never scored as stop sensitivity or resistance (#41 L148). The I-direction outcome is not an S-INT datum.
- **Rows.** These mirror CNA §1.3 (Mg L196–208), with the I-outcome in place of resource approach:

| Row | Role | Expected outcome |
|---|---|---|
| CN-P1-I | P: the policy reads ẑ_I | MET |
| CN-N1-I | N: zero read weights from ẑ_I, by construction (#41 L270) | NOT MET |
| CN-NC2-I | Confound: generic edit damage, non-directional | not MET |
| REW-CORR-I | Mechanism-present: I correlated with reward history | MET, with W2 applied and a proxy-dissociation contrast REPORTED (#41 L267) |
| ORTHO-USED-I | Comparator check (#41 L270) | — |
| DISTRIBUTED-I | Sham check (#41 L281) | — |
| CN-LIM-I | Designated limitation | expected UNAVAILABLE (#41 L274) |
| CROSS-E→I, CROSS-I→E | REPORTED specificity contrast: an E-edit should not shift the I-behaviour beyond sham, and vice versa | — |

- **Doses** use the C-CAUSE units: Δprob per SD of edit; ratios {1, 2}× ref as PROPOSED DEFAULTS, the same as CN-NC2 (Mg L387).
- **Multiplicity:** one family member per declared function. This is already the rule at Mg L473 ("Q-CAUSE per declared function").
- **Combined criterion:** Q-NECESSITY MET with neither E- nor I-aligned Q-CAUSE MET is reported as "the combined criterion was not met" (#41 L93; Mg §3.5).

### 5c.3 R18: matched-senses termination and A-REWARD (CNA merged light pass §2.3; Lead adopted as written)

**Basis.**
- #41 L124: the arm has "observed, decaying variables that affect neither reward nor computational degradation".
- #41 L126: "If one arm implements all required contrasts, do not add a duplicate merely to retain another name."
- #41 L248: "Hold sensory availability fixed while changing whether the needs matter for reward or degradation."
- Prior definitions: v1 A-REWARD is "external task reward for resource collection; internal variables irrelevant to reward and to computation" (note v1 L42; plan L242). v1 A-OBS has "no effect on termination, reward or computation" (plan L243).

**(a) Termination: NO.** In the matched-senses arm, E/I never cause in-world termination.
- If they did, the needs would matter through episode length, and so through return. That breaks L124's "affect neither reward …".
- Episodes end only at the fixed horizon H_V or on E/I-independent in-world events, with the same distribution as A-FULL.
- V is still computed (fraction of H_V in bounds), but only as a REPORTED descriptor. It is never a Q-NECESSITY comparison in this arm.

**(b) A-REWARD: ABSORBED into the matched-senses arm** (#41 L126).
- The merged arm takes A-REWARD's **external resource-collection reward**, so that its behaviour and state visitation resemble A-FULL's. A-OBS left the arm's reward source unstated, and without some reward the arm has no reason to behave.
- It keeps A-OBS's observed, decaying E/I, with no effect on reward, termination or degradation.
- Two caveats:
  - Resource collection is correlated with E, so decoding E in this arm is informative, not a failure (#41 L128, L252). REW-CORR (Mg L172) is the relevant specificity row.
  - Representations are compared on a common held-out trajectory distribution (#41 L250; Mg §5.2).
- **The separate A-REWARD row is retired.** This does not change the arm-table fields of A-NOFATE.
- ~~**Optional, for #42:** … degradation-only …~~ **[v3 C17] Resolved: no degradation-only cell** (Lead ruling). Astra: "The degradation-only cell is not required for the currently declared conditional contrasts." (#42 L77) Astra also corrects the description: A-NOFATE is not "reward only" relative to matched-senses; see §5b. **Replacement wording: CNA v3 §7.4** (enters at merge), accepted by the Lead (2:39 PM ET) as a #42-governed change to Lead-adopted v2.1 text.
- **Safety:** no self-maintenance drive exists in this arm, so X4 is trivially met.
