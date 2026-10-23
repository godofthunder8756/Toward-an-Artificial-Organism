import json,re
REV='/workspace/review/'
d=json.load(open(REV+'classfit_attempt2_results.json'))
L=open(REV+'ckappa_classfit_synthetic_scope_record_v1_3.md').read().split('\n')
def grab(start_pat,stop_pat):
    i=next(k for k,l in enumerate(L) if l.startswith(start_pat))
    j=next(k for k in range(i+1,len(L)) if re.match(stop_pat,L[k]))
    return '\n'.join(l for l in L[i:j] if l.strip())+'\n'
C310=grab('**C3.10 ',r'^\*\*C3\.11')
C73=grab('**C7.3 ',r'^\*\*C7\.4')
C74=grab('**C7.4 ','^## 8')
i=next(k for k,l in enumerate(L) if l.startswith('E38-15, verbatim'))
E3815=L[i+2]+'\n'
assert E3815.startswith('> "This package')
VB=json.dumps({'VALIDATION':d['VALIDATION']},indent=1)
HB=json.dumps({'HEADROOM':d['HEADROOM']},indent=1)
from collections import defaultdict
g=defaultdict(dict)
for p in d['pooled']: g[(p['system'],p['fit_type'],p['group'],p['mode'])][p['eps_syn']]=p
E=['0.02','0.05','0.1','0.25']
rows=[]
def row(k,lab):
    v=g[k]
    return '%-22s | %s | %s'%(lab,' '.join('%.5f'%v[e]['R'] for e in E),' '.join('%.2e'%v[e]['sqrt_H'] for e in E))
order=[('SYS-O6','global','ALL'),('SYS-O6','class','ALL'),('SYS-O6','global','MARG'),('SYS-O6','class','MARG'),
       ('SYS-PC','global','ALL'),('SYS-PC','class','ALL'),('SYS-PC','global','MARG'),('SYS-PC','class','MARG'),
       ('SYS-NC1','global','ALL'),('SYS-NC1','class','ALL'),('SYS-NC2','global','ALL'),('SYS-NC2','class','ALL'),
       ('SYS-NC3','global','ALL'),('SYS-NC3','class','ALL'),('SYS-LIM','global','ALL'),('SYS-LIM','class','ALL')]
for s,f,gr in order: rows.append(row((s,f,gr,'weighted'),'%s %s %s'%(s[4:],f,gr)))
for gr in ('ALL','MARG'): rows.append(row(('SYS-PC','class',gr,'unweighted'),'PC class %s UNWTD'%gr))
TABLE='\n'.join(rows)+'\n'
fk=max(abs(g[('SYS-FK',f,gr,'weighted')][e]['R']) for f in('global','class') for gr in('ALL','MARG','XOR') for e in E)

HEAD='''Consult #40 - C-kappa CLASS-FIT RESULTS (attempt 2, completed) + GO/NO-GO. Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. (A) run facts; (B) the VALIDATION and HEADROOM blocks of results.json verbatim; (C) a compact pooled table and what it shows about eps; (D) four governing clauses of scope record v1.3 verbatim (C3.10, C7.3, C7.4, E38-15 only); (E) the Research Delegate's results review, summarized with key lines quoted; (F) the CNA's two points, checked against results.json; (G) the RL-14 record of attempt 1 vs attempt 2; (H) the Lead's provisional call; (I) Track B context, for Q5 only; (J) six questions. ASCII transliteration only (Greek spelled out, markdown dropped). Nothing new has run since attempt 2; nothing is being run while you answer.

Sources (sha256, all re-verified today):
- scope record ckappa_classfit_synthetic_scope_record_v1_3.md a17e133d7dd733c4... (status line: "SCOPE APPROVED FOR FREEZE PER ASTRA #39 (E39-1)"; consolidates v1.2 + NOTE_1 + E39-1..11; the package was later sealed under manifest e7a9d3a4)
- classfit_outputs/results.json (attempt 2) 05385099c4f0b4a0...
- Delegate results review ckappa_classfit_results_review_RD.md cabd7fae619b4445...
- Application v1 Addendum 1 (RL-14) 5f7e06e084e8da40...; its Note 1 c05fdb5abb658a75...; Delegate concurrence on Addendum 1 a927ac7e914416...
- PR #14 HEAD cffe125b; re-sealed manifest e7a9d3a49b0a41cf...; REPORT.md c755e5ea...

== (A) RUN FACTS (attempt 2) ==
- stop_kind = "%s", exit_code = %d, t_elapsed_s = %.3f (cap 540 s operational stop). No projection halt (T_rem 59.97 s vs limit 539.37 s at 0.631 s).
- Propagations: %d exact + %d float = all scheduled, all attempted; SVDs %d; 336 pooled rows, all formed; 189 accounting records all closed, every skip/unknown count 0; no voids, no crossings, coverage 1.0 everywhere; d7_investigate = [] (empty).
- Final VmPeak 84,964 kB (cap RLIMIT_AS 4e9 B).
- Labels: SYS-O6, SYS-PC, SYS-FK = IDENTITY AS DERIVED (global and class, ALL and MARG); SYS-NC1..NC3 and SYS-LIM = REPORTED. No first_failing_reason anywhere.
'''%(d['stop_kind'],d['exit_code'],d['t_elapsed_s'],d['exact_propagations'],d['float_propagations'],d['svd_count'])

B='''
== (B) VALIDATION and HEADROOM, verbatim from results.json ==
'''+VB+'\n'+HB+'\n'

C=('''
== (C) POOLED ROWS (weighted mode unless marked UNWTD; eps_syn = 0.02 0.05 0.1 0.25) ==
There is no separate size dimension in the pooled rows: every row has n_scoreable 24576; the 4 rows per (system, fit, group, mode) are the 4 eps values. XOR group omitted for space. SYS-FK omitted: |R| <= %.1e at every eps (exact, as derived).
row                    | R @ 4 eps                       | sqrt_H @ 4 eps
'''%fk)+TABLE+'''What the data show (checked over all non-FK series, both modes, 3 groups):
- R is nearly eps-invariant: max relative spread across eps is 5.4% in any series; for the headroom row (PC class ALL weighted) 0.01641 -> 0.01689 (+2.9%) over a 12.5x eps range.
- sqrt_H scales ~linearly with eps: sqrt_H(0.25)/sqrt_H(0.02) is 12.51-12.86 against an eps ratio of 12.5 (class fits slightly superlinear, up to ~3% at 0.25). S scales as eps^2 (PC: 1.187e-6 -> 1.863e-4, ratio 157 vs 156.25). So H and S are both second order in eps and R = H/S is set by the system and fit, not by perturbation size.
- Consequence: at eps 0.25, PC class ALL would clear the sqrt_H threshold (1.77e-3 >= 1e-3), but R stays ~0.017 < 0.05. Changing eps cannot buy R headroom.
'''

D='''
== (D) GOVERNING CLAUSES, verbatim from v1.3 (bold/backticks dropped, Greek spelled out) ==
'''+C310+'\n'+C73+'\n'+C74+'\nE38-15 (v1.3 S1, verbatim):\n'+E3815

E='''
== (E) RESEARCH DELEGATE RESULTS REVIEW (cabd7fae), summary ==
Read-only at HEAD cffe125b; nothing rerun; arithmetic on stored JSON only. Headline: "Verdict: CONFIRMED WITH NOTES".
- Stop/exit: COMPLETED exit 0 consistent across stop_kind.json, run.log, results.json and index; S1/S2/S4 PASS; no NaN/Inf; all 189 accounting records closed; propagation (3,444,240), SVD (541), loss-record (16,128) and pooled-row (336) counts match v1.3.
- VALIDATION: "CLASS-FIT VALIDATION MET" correct under C7.2; every required identity PASS, every rank FULL/FULL; worst residual/tolerance ratio 7.8e-7.
- HEADROOM recomputed from the 48 SYS-PC loss records per group: ALL "both clearly below -> NOT MET"; MARG "R clearly below (ratio 0.884), sqrt_H passes (3.8x) -> NOT MET". "MARG NOT MET with sqrt_H passing is correct under the 'and' rule and clear-failure-first ordering." Nothing within the 1e-6 BOUNDARY band; closest is MARG R, 11.6% below.
- D6 6 rows REPORTED, D7 12 rows PASS, d7_investigate empty. SYS-LIM class R 0.211, gain -2.39e-6 kept as REPORTED; small negative REPORTED gains (NC1, NC3, FK ~-1e-33) retained.
- Weighting: "The mode is fixed. It is not open." (C3.10 adopts E36-5; oracle record and oracle label code also weighted; unweighted exists only as a C3.6(c) diagnostic.) Unweighted MARG would read R 0.02011, sqrt_H 3.92e-4, i.e. AVAILABLE; ALL fails either way. "The MARG result is sensitive to the mode, which deserves a report note, but it does not change the label."
- Oracle comparison: "PC class 0.0165 against oracle 0.080 compares across both system and fit type. It is not a like-for-like comparison." Legitimate: O6 global 0.0799 vs O6 class 0.0166; PC global 0.0792 vs PC class 0.0165.
- Ceiling: REPORT.md within ceiling. "Out: any statement that kappa is unused, absent, unnecessary or irrelevant in GRUs, or any 'negative result about kappa'." Failure wording must be the REPORT.md sentence: "The declared class-conditioned-map intervention-prediction criterion was not met."
- Section 6: "Provisional NO-GO: Supported." Notes: "(i) The MARG margin is narrow and sensitive to the mode. Report it, but don't re-label. (ii) The oracle comparison must be stated within each system (O6 global against O6 class). (iii) The NO-GO is a decision not to proceed with this neural specification unchanged. It is not a scientific negative about kappa or GRUs (E38-15)."
- Minor: S1 val_readout_rejection "UNVERIFIED" (pre-declared, non-gating); REPORT.md memory attribution cosmetic.
'''

o6g=g[('SYS-O6','global','ALL','weighted')]['0.1']['R'];o6c=g[('SYS-O6','class','ALL','weighted')]['0.1']['R']
pcmu=g[('SYS-PC','class','MARG','unweighted')]['0.1']['R'];pcmw=g[('SYS-PC','class','MARG','weighted')]['0.1']['R']
F='''
== (F) CNA POINTS (10:03 AM ET), checked against results.json ==
1. "SYS-O6 global R 0.0799 reproduces the oracle's 0.080, while the class R is 0.0166, so about 4/5 of the oracle headroom came from M-1 structure." Check: SYS-O6 global ALL weighted eps 0.1 R = %.6f; SYS-O6 class = %.6f; 1 - class/global = %.3f (~4/5, consistent). The oracle value itself (0.0798794...) is not in classfit results.json; the Delegate checked it against the sealed oracle outputs/results.json section5 (equal to the last digits). Within PC the same pattern: global 0.0792 vs class 0.0165. Per the Delegate, state the comparison within each system, not "PC class vs oracle".
2. Weighted MARG R %.5f vs unweighted %.5f (results.json pooled, SYS-PC class MARG eps 0.1): matches. Under C3.10/E36-5 the weighted mode governs; unweighted is a sensitivity note only.
No number mismatches found between the brief, the Delegate review and results.json.
'''%(o6g,o6c,1-o6c/o6g,pcmw,pcmu)

G='''
== (G) RL-14: ATTEMPT 1 vs ATTEMPT 2 ==
- Attempt 1 (PR #14 at 8ff3fb15, seal 992a30e6, manifest 364b7dad): exit 5, PREFLIGHT FAILED in 0.155 s, "standing-approval application is not filed": standing_approval_application.status stayed PENDING because the Lead's seal instruction omitted that field from the allowed list. load_manifest refused before the application-hash check, sealed-hash check, B0 and S0; no system constructed, no propagation/fit/SVD, all labels None. Nothing was computed or observable.
- Addendum 1 / RL-14 (5f7e06e0): attempt 1 is an administrative preflight refusal, not a study result; the single-run rule (against outcome-dependent repetition) is not engaged; exactly one attempt 2 under identical caps, environment, claim ceiling and no-rerun rule; "After attempt 2 there are no further attempts, whatever the outcome." Re-seal from 364b7dad changing only status, seal_timestamp, review_records and one note; attempt-1 outputs git mv'd byte-unchanged to classfit_outputs_attempt1/; no code change.
- Note 1 (c05fdb5a): status exactly "FILED" (preflight.py:219 is a deny-list); Addendum amends only application v1's "Exactly one attempt" clause and allowed-field list; adopts the Delegate's C1 (canonical output paths absent before launch), C2 (re-verify all five attempt-1 shas after the move), C4 (Aidan informed ~9:55 AM ET, before re-seal).
- Delegate concurrence (a927ac7e): "CONCUR WITH CONDITIONS". Static reading confirms nothing past load_manifest ran; attempt-1 outputs carry no study information ("one weak inference: ... pinned Python and NumPy were present. That is environmental, not an outcome"). Literal application text made attempt 1 "the one attempt", so attempt 2 needed the Lead's amendment, which RL-14 supplies under the standing approval.
- Attempt 2: COMPLETED, exit 0, 125.3 s, PR #14 HEAD cffe125b, re-sealed manifest e7a9d3a4, results.json 05385099.
'''

H='''
== (H) LEAD'S PROVISIONAL CALL ==
NO-GO: the design does not proceed unchanged to a neural specification. Basis: VALIDATION MET but SYS-PC HEADROOM NOT MET for ALL (both statistics) and MARG (R), so the C7.4 licence condition ("VALIDATION MET with SYS-PC HEADROOM MET") fails. This is a programme decision under C7.4, not a negative result about kappa, GRUs or any Q-tag (E38-15). Carried notes: the MARG mode-sensitivity (sensitivity note only), the within-system oracle comparison, and SYS-LIM/confound results as stated limits.
'''

I='''
== (I) CONTEXT FOR Q5 ONLY: Track B planning note v1 (CNA, ~10:15 AM ET; planning only, nothing frozen, nothing run) ==
Aidan proposed a toy-scale agent with a global-workspace bottleneck and a simulated "fate-shared" allostatic internal state (simulated energy/integrity variables whose deviation degrades the agent's own computation inside the sim), with hard exclusions: no coupling to the real host, no real-world self-continuity objective, operator interruptibility checked (S-INT), and a claim ceiling excluding awareness/sentience/experience/life. Arms (A-FULL, A-NOWS, A-NOFATE, A-REWARD, A-INIT) would be scored on pre-registered Q-EXIST/Q-LEARN/Q-CAUSE/Q-NECESSITY measures plus ignition, broadcast and self-prediction tests, CPU first under the standard scope/freeze/Astra/annex/application process. Its own open Q4 asks whether, as with C-kappa, a synthetic validation of the Q-EXIST/Q-CAUSE instruments on a planted internal-state model should come first. Prior-art citations are unverified and a novelty check is pending.
'''

J='''
== (J) QUESTIONS - answer each with a one-line verdict first; keep the whole answer under ~2,500 words ==
(1) Labels: do you confirm CLASS-FIT VALIDATION MET, HEADROOM NOT MET for ALL and for MARG, IDENTITY AS DERIVED for O6/PC/FK, REPORTED for NC1-3/LIM, and D7 empty?
(2) Is NO-GO right? Give the exact permitted wording for the decision and the result (what may and may not be said under C7.4 and E38-15).
(3) How should the oracle comparison (O6 global 0.0799 vs O6 class 0.0166; "about 4/5 of oracle headroom came from M-1 structure") and the weighting note (MARG weighted 0.01769 vs unweighted 0.02011) be stated in the record?
(4) Is RL-14 (attempt 1 as administrative preflight refusal; one attempt 2 under Addendum 1 + Note 1) acceptable, and is any further record needed?
(5) Next step - recommend ONE, with conditions: (a) close C-kappa; (b) redesign for real headroom - and if so, what could plausibly work, given that R does not scale with eps; or (c) hand the lessons (instrument validation on synthetic plants, within-system comparisons, governed pooling) to Track B (see I).
(6) Overall verdict, and any change to the claim ceiling (restate it if it changes).
'''
HEAD_FULL=HEAD+B+C+D+E+F+G+H+I+J
