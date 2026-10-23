exec(open('h.py').read())
import hashlib,subprocess
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def foot(p):
    L=open(p,'rb').read().split(b'\n')
    if L and L[-1]==b'': L=L[:-1]
    return hashlib.sha256(b'\n'.join(L[:-1])+b'\n').hexdigest(), L[-1].decode()
W='/workspace/'; Rv=W+'review/'
inputs=[
('Astra #42 raw reply (GOVERNING)',W+'astra_consult42_response.txt',None),
('Consult summary incl. #42 entry L157–164 (non-governing; appended over time; hash as read)',W+'astra_consult_1.md',None),
('#42 packet body as sent',W+'astra_serve42/c42_body.md',None),
('#42 cover note v1',Rv+'trackB_astra42_cover_note_v1_RD.md',None),
('Merged scope v2.1 (base; frozen, not edited)',Rv+'trackB_instrument_validation_scope_v2_1_merged_RD.md','ft'),
('CNA v3 half (plants, confounds, observer)',Rv+'trackB_scope_v3_CNA_plants_confounds_observer_v1.md','ft'),
('Astra #41 raw reply (governs where #42 is silent)',W+'astra_consult41_response.txt',None),
('Merged scope v2 (superseded by v2.1)',Rv+'trackB_instrument_validation_scope_v2_merged_RD.md','ft'),
('CNA v2 half',Rv+'trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md','ft'),
('CNA erratum 1 to v2 half',Rv+'trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md','ft'),
('CNA erratum 2 to v2 half',Rv+'trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum2.md','ft'),
('CNA light pass on merged v2',Rv+'trackB_scope_v2_merged_lightpass_CNA_v1.md','ft'),
('CNA prior art v1.3 (full reads; Asan)',Rv+'trackB_prior_art_verification_v1_3_fullreads_CNA.md',None),
('CNA prior art v1.4 (P3)',Rv+'trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md',None),
('CNA prior art v1.5 (P3 alt routes)',Rv+'trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md',None),
('CNA prior art v1.6 (Palika route)',Rv+'trackB_prior_art_verification_v1_6_palika_route_CNA.md',None),
('FoodRL commit list as fetched by CNA (v1.6 raw)',W+'tmp_p6/raw/foodrl_commits.json',None),
('Merged scope v1',Rv+'trackB_instrument_validation_scope_v1_RD.md',None),
('Measurement plan v1',Rv+'trackB_measurement_plan_v1_RD.md',None),
('CNA planning note v1',Rv+'trackB_workspace_allostasis_scope_note_v1.md',None),
]
rows=['| Role | Path | sha256 | Footer check |','|---|---|---|---|']
for role,p,f in inputs:
    h=sha(p); fc='—'
    if f:
        fh,last=foot(p); assert last.endswith(fh),p; fc=f'`{fh}` reproduced'
    rows.append(f'| {role} | `{p}` | `{h}` | {fc} |')
assert sha(W+'astra_consult42_response.txt').startswith('e438e329')
INPUTS='\n'.join(rows)
HDR=f'''# Track B instrument-validation scope v3 — RD half (built on merged v2.1 `8ea6abc5…`)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #42, verbatim: {ql(249)} **P3: CLOSED by Astra #42** ({q(251,'P3: CLOSED for the declared bounded scholarly-index search')}).

- **What this file is.** The RD half of scope v3. It is a new, additive file and edits nothing. v2.1 (`8ea6abc5…`) and every other input stay on disk unchanged. RD holds the merge; CNA's v3 half (`5dec96f5…`) is filed and enters at the merge (§PC1–§PC4).
- **Authority.** Astra #42 raw text first; Astra #41 raw text where #42 is silent; then the Lead's room rulings (2026-10-23, about 2:30 PM and 2:39 PM ET). Astra is quoted verbatim, cited "#42 Lnn" / "#41 Lnn". E42-1..9 are numbered exactly as #42 L231–247.
- **Split (Lead).** CNA drafts the mixed-code plant, the dissociation contrast, observer pathway matching and its budgets, and the donor laws. RD takes every other E42 item and every ruling. Items the raw reply assigns ambiguously are in this half, marked **CNA-overlap, light-pass**.
- **How it is built.** RD-owned sections of v2.1 (§2, §3, §4, §5, §5b, §5c, §6, §7) are carried in full with edits tagged **[v3 Cn]** (listed in §9); struck text is kept visible as ~~strikethrough~~. New sections: §2.6–§2.7, §5.9, §5d–§5f, §14 (pending-choice specification), §15 (CNA dependency settlement), §PC1–§PC4 (CNA placeholders), §8 (response table), §9–§11. v2.1's CNA-owned sections (§P1, §P3, §PA, §PS) are carried **by reference** (§16).
- **Written:** 2026-10-23, about 2:35–2:50 PM ET, by RD. Read-only on the repo and GitHub.
- **Correction for the record [v3 C2] (Lead ruling, 2:39 PM ET; CNA v3 D9).** v2.1's header (v2.1 L3) said "P3 stays OPEN and freeze-blocking pending Astra #42". #42 L251 closed it; this header records P3 CLOSED. v2.1 is not edited.

**Number provenance.** Every number here is (a) an Astra candidate, cited by line; (b) a v1 value carried; (c) a **PROPOSED DEFAULT** with a one-line rationale (§14; CNA v3 for CNA rows); or (d) marked **OPEN FOR #43** where no defensible default exists. None is measured. **Every default is chosen without reference to any instrument outcome** (#41 L186, verbatim: "Do not tune doses on final instrument outcomes."), and **calibration and sample-size choices are fixed in a separate calibration stage before confirmation** (§5.9). Arithmetic in §14 was computed on the box (scipy 1.x in a scratch venv) on proposed values, not data.

**Labels.** Confound rows: PASS / FAIL / CONFOUND NOT REALIZED only; CONFOUND NOT REALIZED → UNRESOLVED, which blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels; UNAVAILABLE is only an instrument-on-system label for eligibility gates and limitation tests designated before results (#42 L216).

## 1. Inputs (all hashed on the box, 2026-10-23 about 2:45 PM ET; none edited)

{INPUTS}

Full hash of the governing raw #42: `{sha(W+'astra_consult42_response.txt')}` (starts `e438e329`, as briefed). All other v2.1 inputs (A1–A7, addendum, earlier CNA files) are listed with full hashes in v2.1 §1 / M1 and are unchanged.

---

## 0. Governing text: Astra #42

- **Verdict, verbatim:** {ql(227)} {q(1,'SP1 addresses all five objections, and SP3 closes the original all-UNAVAILABLE loophole, but several remaining choices determine what a successful result would mean.')}
- **Scientific choices, verbatim:** {q(13,'Some PENDING items are scientific decisions, not implementation details: observer resources, the A-EXT interface, conditional donor construction, prediction horizons, baseline information sets, corruption processes, and the calibration/confirmation split. They must be specified in the revised design. Hashes, paths and counts derived from a complete design can be finalized during implementation and checked before sealing.')}
- **Scope, verbatim:** {ql(15)}
- **Required revision items, verbatim (#42 L231–247):**
'''
for n in (231,233,235,237,239,241,243,245,247):
    HDR+=f'  - {ql(n)}\n'
HDR+=f'''- {ql(229)}

---
'''
open('hdr.md','w').write(HDR)
print('ok')
