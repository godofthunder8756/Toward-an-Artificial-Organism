# Track B instrument-validation scope v1: Amendment A1 (additive; RD)
- **Amends:** `/workspace/review/trackB_instrument_validation_scope_v1_RD.md` (sha256 `7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a`). v1 is unchanged; where the two conflict, A1 governs.
- **Inputs:** CNA pre-freeze prior-art note `/workspace/review/trackB_prior_art_verification_v1_1_prefreeze_CNA.md` (sha256 `29068cce219530f459a4a045f349393a2aea9db1253a4c76a654514284017928`), and the Lead's rulings in the ACI Research room, 2026-10-23, about 10:38 ET.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS.

## A1-1. §10 novelty labels (replaces the v1 §10 novelty statement)
| Claim | Label | Cited as closest |
|---|---|---|
| Q-NECESSITY of a learned interoceptive self-model against same-size ablations of other modules | NOVEL AS FAR AS FOUND, NARROWED | Craggs 2026 Block V (osf.io/jz4ed, registered 9 Oct 2026, not yet run), the closest pre-registered test |
| SELF for agents (adapted from Binder et al. 2024) | NOVEL AS FAR AS FOUND | none found |
| Stage-0 known-answer gate that validates the instruments before use | NOVEL AS FAR AS FOUND | none found |
| Pre-registration as such | PARTIAL OVERLAP | Craggs 2026 Blocks I–V; Faeth 2026 (osf.io/69zny) |

The remaining v1 §10 labels are unchanged: the homeostatic setup is SETUP, CITED NOT CLAIMED; fate-sharing, Q-EXIST and Q-CAUSE are PARTIAL OVERLAP; workspace necessity and ignition are a REPLICATION/EXTENSION of Phua 2025; and S-INT is NOT A NOVELTY CLAIM.

Full reads (CNA, 29068cce):
- Hayes 2026 tested "deployed dependence, not retrained necessity" (§6.1, p.23).
- Grimbly 2026 is an active-inference agent with hand-specified routing and no other-module ablations.
- Phua 2025 uses behaviour cloning, and its self-model tracks task confidence.

None of the three ran our Q-NECESSITY test, none is pre-registered, and none has a SELF test.

**Citation correction:** Grimbly 2026 has 10 authors, adding Smith, Solms and Shock (SAB 2026 camera-ready).

## A1-2. Drop rule: assessed difference by difference (replaces the drop rule in v1 §10 P2)
Each of the four differences from the closest prior test (Craggs 2026 Block V, and any later-found work such as Wilterson & Graziano 2021) is reported as HOLDS or DOES NOT HOLD:
- D1: the self-model's content is interoceptive;
- D2: the agent is a learned RL agent;
- D3: the outcome is viability;
- D4: other modules get same-size ablations.

The label follows from those results:
- If all four hold, the claim stays NOVEL AS FAR AS FOUND, NARROWED.
- If at least one fails but D1 holds, it becomes an EXTENSION.
- If all four fail, it becomes a REPLICATION.
- Any combination not covered above, where D1 fails but not all four do, is referred to the Lead and Astra rather than labelled by default.

The v1 P2 rule, which dropped the claim if Hayes or Grimbly had already run our test, is retired. Their full reads have come back and neither ran it.

## A1-3. Pre-freeze items (replaces v1 §10 P1–P4)
**CLOSED:**
- P1 (OSF): 37 queries, listed in CNA Part A. AsPredicted is NOT SEARCHABLE, since public lookup works only by registration number.
- P2: full reads of Hayes 2026, Grimbly 2026 and Phua 2025.
- Pardo et al. 2018 existence: VERIFIED as "Time Limits in Reinforcement Learning", ICML 2018, PMLR 80:4045–4054. This is an existence check only.

**FREEZE-BLOCKING (owner: CNA):**
- F1: a content check of Pardo 2018's argument for bootstrapping at time-limit truncation, and whether it holds for independently seeded operator stops. S-INT's truncation-with-bootstrap rule (plan Addendum 1, 4ecef262) relies on it. Until F1 closes, Pardo stays uncited as support.
- F2: the Craggs 2026 registration files and code, to settle whether its agents are learned. This feeds D2.
- F3: a re-check of OSF jz4ed, gqanp and 69zny for posted results.
- F4: a full read of Wilterson & Graziano 2021 (PNAS), checked against D1–D4.
- F5: searches of Zenodo and the Registered Reports list. Neither has been searched yet.

**Safety record:** OSF registration b4asn lists "mechanical self-preservation" protocols. This is noted only; X1–X5 are unchanged and binding.

## A1-4. Still open for Astra
AQ-C2, how RAND-INIT is treated, stays with CNA. AQ-P1, whether the narrowed novelty statement is enough to justify the study, now refers to A1-1. The packet goes to Astra once F1–F5 are filed.
