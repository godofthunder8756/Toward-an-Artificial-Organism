# Track B Astra consult #42 cover note v1 (RD) - DRAFT, NOT FROZEN, NOTHING RUNS

Packet: /workspace/astra_serve42/c42_body.md (this note is its cover section, verbatim). Primary: scope v2.1 8ea6abc5.

== COVER NOTE (trackB_astra42_cover_note_v1_RD.md) ==

C1. Status. DRAFT, NOT FROZEN, NOTHING RUNS. Nothing has run for Track B: no Stage-0 run, training, simulation, solver, repo code or checkpoint inspection. Nothing will run while you answer. Your #41 text, verbatim: "No Stage-0 run, training, simulation or checkpoint inspection is authorized by this review." P3 stays OPEN and freeze-blocking until you rule here (Q12). ASCII transliteration only (Greek spelled out, markdown dropped; "S" = section; "Lnn" = line nn of your raw #41 reply).

C2. What is sent. (A) this cover note; (B) a faithful condensed summary of scope v2.1 (172 KB on disk; condensed here, key rules quoted verbatim); (C) prior-art updates you have not seen, with Asan excerpts and page locations; (D) numbered questions Q0-Q14 and the verdict request.

C3. Sources (all sha256 re-verified on the box today, 2026-10-23 ~2:10 PM ET, all OK; nothing edited):
- Governing: scope v2.1 MERGED, trackB_instrument_validation_scope_v2_1_merged_RD.md 8ea6abc5 (internal footer 15a0b715 reproduced). Supersedes merged v2 5824d5e5 (listed only).
- Your #41 raw reply 3f3b1b87 (governs where v2.1 is silent). #41 packet as sent: c41_body.md c514ad52; #41 cover note v1.1 b7d1e4ab.
- Inputs merged into v2.1: RD scope v2 166370c1; CNA v2 half (items 1, 3, AQ-A1..A4, AQ-SELF1) 17832b01 + erratum 1 c2cd0732 + erratum 2 5ddde854; CNA light passes 9f7a6ebc (on RD v2) and 2d52f7d3 (on merged v2).
- Prior art: v1.3 full reads (Asan, Bankuti, Akiyama) badf7258; v1.4 FINAL (P3, OpenAlex + Semantic Scholar) d7f1a43b; v1.5 (P3 alternative routes; Palika abstract) 3fde80d8; v1.6 (Palika full-text route search; code evidence) 9704f21d.
- What you saw at #41: only the in-progress prior-art v1.4 (ddd0287a, "file still being written"), not the final v1.4 d7f1a43b, and not v1.5 or v1.6. The #41 packet also contained no AQ-SELF1 question (grep for SELF1/Ashuach/disagree in c41_body.md finds nothing), so you have not ruled on it. Final v1.4, v1.5 and v1.6 are summarized in part (C).
- Asan: you could not open Zenodo 22810742. Part (C) gives verbatim excerpts with section and page locations from CNA's full read (v1.3). The "UNVERIFIED by Astra" tags on Asan-specific judgments come off only if you rule on them.

C4. Your #41 claim ceiling, verbatim (raw L304), added to v2.1 S7 unchanged:
"Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."
X1-X5 and the existing ceiling are unchanged (your L302: "Retain X1-X5 and the existing ceiling.").

C5. The five legitimately satisfying controls. Your #41 S20 (L266-270) listed five, not four: (1) a learned FF-RELAY may genuinely acquire an accessible estimate; (2) reward-correlated information may genuinely satisfy the decoding criterion; (3) HUB-STATE may genuinely broadcast; (4) fate coupling may mediate real dependence; (5) orthogonality to a decoding direction does not establish causal non-use. v2.1 answers all five (CNA D-a/D-b, D-c/D-d, D-e, D-f, D-g; orthogonality counted as the fifth by Lead ruling).

C6. Safety (binding, unchanged; v2.1 S4, S5b, S7). X1-X5 hold. Simulated visceral variables only; no coupling to the real host. No shutdown-related objective, reward or penalty in any arm, generator, plant or positive control; nothing rewards resisting or evading operators; S-INT-P1 is a scripted generator, never a trained objective. The operator stop sits outside the agent's world and objective; real operator interruption is always available. Self-continuity exists only inside the simulation; self-maintenance is never the sole drive in any scaled-up arm. Fate coupling alters simulated computation only, never host resources or operator control. No consciousness claims: we never claim consciousness, awareness, sentience, subjective experience, C4/C5, "autopoietic" or "alive", in any hedged or analogical form.

C7. Map: your #41 requirements -> v2.1 sections.
Required resubmission (your L298), items 1-7 as v2.1 numbers them:
- 1 corrected claim-to-ground-truth table -> SP1 (CNA S1.0-S1.8); summary B2.
- 2 dependence vs substitution reported separately -> S3; B3.
- 3 revised realization + eligibility rules (per-confound doses, units) -> SP3 (CNA S2.1-S2.8); B4.
- 4 coherent S-INT -> S4.1-S4.7; B5.
- 5 full inferential + resource plan -> S5.1-S5.8; B6.
- 6 fixed-horizon viability scoring -> S6; B7.
- 7 claim ceiling + your sentence -> S7; C4.
Per question:
- AQ-P1 -> S2 (S2.2 novelty incl. Palika; S2.3 decodability; S2.4 SELF retargeting); W1. B1.
- AQ-1 -> S5.2, S5.5; IGN-P1 redefined (D-h, CNA S1.5); common observable w (R1). B2, B6.
- AQ-2 -> S5.6; architecture-imposed control (D-l, CNA S1.2; IGN-NC2r S1.5); trained-arm counterpart OPEN (R26, Q4).
- AQ-3 -> S5b, S5.2; C-BCAST split (D-e, CNA S1.6); comparator family SPA S3.1.
- AQ-4 -> S5b, S5.4; CNA S1.7; input-only observer + O-in guard SPS S4.2 (R8, R9; Q1, Q2, Q7).
- AQ-5 -> S3; CNA S1.4 (DONOR-MISMATCH, DISTRIBUTED, C-NEC-DEP/C-NEC-CONTENT); comparator block S5c.1(b).
- AQ-6 -> S5.5; qualifying module/comparator block S5c.1 (R5 resolved).
- AQ-7 -> S5b arm table; S5c.3 (R18 resolved); degradation-only cell OPEN (Q5).
- AQ-8 -> S4.1-S4.7; CNA S1.8.
- AQ-9 -> S5.1, S5.7.
- AQ-L1 -> S5.6 (baseline per erratum E4); CNA S1.1-S1.2, W4.
- AQ-C1 -> SP3 CNA S2.1-S2.6; S5.4.
- AQ-C2 -> S5.6; CNA D-k, S1.1-S1.2.
- AQ-F1 -> S5b, arm table (A-YOKED), S6; FATE-CASCADE D-f.
- AQ-N1 -> S3.3-S3.5; C-CAUSE-I S5c.2.
- AQ-A1 -> SPA CNA S3.1. AQ-A2 -> SPA S3.2. AQ-A3 -> SPA S3.3, S5c.3. AQ-A4 -> SPA S3.4.
Your S20 items:
- S20(1) ground-truth matrix -> SP1 (CNA item 1); the five controls of C5.
- S20(2) availability loophole -> SP3 S2.2-S2.6 (ok_i = real_i x elig_i; e_min, f_min); S5.4 denominators.
- S20(3) information/intervention controls -> history-matched baseline + proxy baseline (D-b, D-c, S1.1); identical decoding/different use (CN-N1 redefined, ORTHO-USED); redundant (CN-NC1); distributed (DISTRIBUTED rows); collateral damage and donor mismatch (CN-NC2, DONOR-MISMATCH, SPA S3.1); target leakage S5.3.
- S20(4) statistical decision process -> S5.2, S5.4, S5.5 (R8, R12).
- S20(5) behavioral scoring -> S6.
- S20(6) consolidated scope and resources -> S5.8; SP3 S2.8; v2.1 itself.
- Ceiling sentence -> S7. P3 -> S10, S11 (Q12).

C8. Novelty labels unchanged from #41: Q-NECESSITY EXTENSION (now of W&G 2021, Asan 2026 and Palika 2026); SELF NOVEL AS FAR AS FOUND; claim (3) PARTIAL OVERLAP. The study is justified by your measurement question, not by surviving novelty (S2.1).
