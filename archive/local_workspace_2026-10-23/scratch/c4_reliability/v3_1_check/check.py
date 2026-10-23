import hashlib,re
R="/workspace/review/"
S3=open(R+"c4_reliability_exact_check_spec_v3.md").read()
A31=open(R+"c4_reliability_assessment_admission_v3_1.md").read()
A=open("/workspace/astra_consult23_response.txt").read()
ok=True
def chk(n,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+n)
norm=lambda x:re.sub(r"\s+"," ",x.replace("**","").replace(">","").replace("`",""))
An=norm(A)
spec_req={
"Q1label":"CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED",
"Q1b":"This is a scientific outcome, not UNRESOLVED-DESIGN. Report which controls share the conjunction and where their statistics differ. Neither functional-role identification nor absence follows automatically.",
"Q1c":"Keep reproduction and criterion attainment as separate per-control columns.",
"Q1d":"Issue DISTINGUISHES NAMED CONTROLS only when every comparable, eligible control demonstrably fails at least one core criterion.",
"Q2":"These analytic predictors share the oracle's binary decisions on the tested observation domain. The analysis therefore does not test whether assessment tracks predictor-specific departures from oracle correctness.",
"Q2b":"That exposes the probability differences hidden by identical decisions, but does not independently establish an evaluation role.",
"Q2c":"A scoring-rule reward would change optimal checking and warrants a separate version.",
"Q3":"Effect-size and reproduction margins may be chosen prospectively with a written rationale.",
"Q3b":"The 2*epsilon bound applies to action-value perturbations, not automatically to changes in p0.",
"Q3c":"For these exact analytic agents, use exact equality for the proposed invariant pre-check probabilities and binary decisions.",
"Q4":"Fixed-cost episodes support the exact-optimum designation. Under switches, use R-HAC-MB-CE, with the persistence assumption explicit; it is not the optimal controller for an unspecified changing-cost process.",
"Q5":"A gamma = 1 variant needs a separately specified return, cost treatment, bootstrap and terminal rule.",
"Q6":"Acceptable as a named compound intervention, not as a pure content intervention. It changes both content and updating.",
"Q6b":"PM-ACT must implement these clamp transitions explicitly; normal machine transitions do not automatically represent suspended updates.",
"Q7":"A T = 4 result cannot claim to distinguish MF.",
"Q7b":"These are bounded implementation comparisons, not evidence about longer horizons or the full cost grid.",
"Q8":"NOT APPLICABLE is appropriate for a genuinely absent transplant target. It is not a failed criterion and cannot itself establish separation. A stateless control can still fail an applicable criterion. If it passes everything evaluable but leaves an essential comparison unavailable, report that comparison as unresolved.",
"Q9":"It is not a full-output implementation of MB.",
"Q9b":"Differences caused by substituting F0 for MB's probability output must be attributed to that substitution, not credited as assessment-role separation.",
"Q9c":"A probability-preserving minimized comparator could answer another question; it is not required here.",
"Q10":"W-REL: admitted as a theory-stage C4 candidate. Exact-check specification under revision; execution pending Aidan's approval. No change to the C4 evidence or status row, and no system-level C4 conclusion.",
"E1":"Reproduction triggers examination of what the reproducing implementation does. Revision is required when the procedure fails to identify the proposed role, not merely because another implementation reproduces it.",
"E2":"m_a(H, I) = E[K_a | recipient information H,\n                    declared intervention procedure I,\n                    do(action = a)]",
"E2b":"Selecting recipients by Z is part of that procedure. Do not silently substitute the ordinary observational posterior when evaluating a Z-selected recipient population.",
"E2c":"Do not recalibrate them on corrupted-state outcomes: doing so could erase the assessment error being measured.",
"E3":"NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated.",
"E3b":"Overestimating correctness is not automatically a false alarm about unreliability; those labels require a separately defined alarm convention.",
"E4":"Agreement with the shadow validates the repair operation. It is not, by itself, credited rescue.",
"E5":"The construction must cover all reachable states under the tested forced actions, donor substitutions, clamps and releases. Include any necessary clamp status and timing. Ordinary reachable belief nodes alone do not establish this closure.",
"E5b":"action outputs cannot depend on the later check observation or revealed X.",
"E5c":"If they are not, report UNRESOLVED-DESIGN rather than supplying an ad hoc transition.",
"E6":"Expected Brier scores remain rational; log scores generally do not.",
"E7":"Identical available donor contents are not evidence that assessment is absent.",
"E7b":"Do not search for replacement donors after seeing results.",
"E8":"subset agreement is not verification of every unreplayed quantity.",
"D":"Scope attachment to the pending W-REL approval question: the executable specification will be [FINAL filename], SHA256 [full hash], with implementation manifest [identifier and hash], incorporating consult #23's required edits. Execution covers ITEM-1 through ITEM-9 only: bounded exact analysis of the world and named analytic controllers. Limits are one CPU process, no GPU, at most four hours total wall-clock, at most one cumulative hour per named item including retries, and at most 8 GB resident memory. Verification and replay count toward these limits. The exclusions in the original approval question remain unchanged. This attachment records scope; it is not an approval.",
"Db":"The currently submitted spec hash 04992f86 is not the final executable identifier after these edits.",
"Dc":"The existing question still matches this bounded theory-only scope. No replacement question is needed.",
}
for k,s in spec_req.items():
    chk("spec3 has "+k, s in S3 or (k=="Q4" and norm(s) in norm(S3))); chk("  source#23 has "+k, norm(s) in An)
for ph in ["[AIDAN'S VERBATIM ANSWER","[YYYY-MM-DD]","[HH:MM ET]","[e.g. widget id","[FINAL filename]","[full hash]","[identifier and hash]"]:
    chk("spec3 placeholder "+ph, ph in S3)
appr="Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."
chk("spec3 approval q", appr in S3); chk("admission3.1 approval q", appr in A31)
chk("spec3 6 labels", all(l in S3 for l in ["DISTINGUISHES NAMED CONTROLS","PATTERN REPRODUCED BY NAMED CONTROL","CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED","REFERENCE CRITERIA NOT MET","UNRESOLVED-DESIGN","UNRESOLVED-COMPUTE"]))
chk("spec3 NOT RUN/PENDING", "NOT RUN" in S3 and "PENDING" in S3)
chk("spec3 ITEM-1 count corrected", "3,006,865 histories, including the empty history" in S3 and "3,006,864" in S3)
# stale absent in spec3
for bad in ["label rule incomplete","Unassigned case","placeholder 1/","ILLUSTRATIVE placeholders","log score)","Brier and log","false-alarm","FA_a","Miss_a","(false-alarm direction)","(miss direction)","|B − C| ≤ ρ_RES","illustrative proposals","Σ_{t≤3} 144^t = 3,006,865","Open questions for consult #23","γ = 1, terminal target"]:
    chk("spec3 absent: "+bad, bad not in S3)
# admission 3.1 required + stale
for k in ["E1","Q2","Q10"]:
    chk("adm3.1 has "+k, spec_req[k] in A31)
chk("adm3.1 card status", "ADMIT AS THEORY-STAGE C4 CANDIDATE" in A31 and "card status only, not a C4 claim" in A31)
chk("adm3.1 tie rule", "d_t(a) = 1 iff p̂ᵃ_t > 1/2, otherwise 0" in A31)
chk("adm3.1 shared label", "CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED" in A31)
for bad in ["sign(p̂","A log-loss variant is reported separately","Any empirical study must first revise the criteria under a new version.","F-ID: revise the criteria under a new version.","spec v2 §","exact_check_spec_v2.md`. This is the revision","reports one of five labels","outcome-level false-alarm","Below C4 throughout","then park"]:
    chk("adm3.1 absent: "+bad, bad not in A31)
# earlier files unchanged
exp={R+"c4_reliability_assessment_admission_DRAFT.md":"dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c",
R+"c4_reliability_assessment_admission_v2.md":"ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162",
R+"c4_reliability_assessment_admission_v3.md":"f122b47fbdd281a444f862021428dd3fa4e2569627f9aa745fa016fb9bde677a",
R+"c4_reliability_exact_check_spec_draft_v1.md":"c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4",
R+"c4_reliability_exact_check_spec_v2.md":"04992f86089c616e8d8aedcd1fa5242423a242507e8be9d657ad0747f2c6601a",
"/workspace/scratch/c4_reliability/v2_check/check.py":"fefda82355a9ff1a27506dcb06a0333589d5555b714e0f3b47606b9bdc2a2697",
"/workspace/scratch/c4_reliability/v2_check/check.log":"e6a384725bbeb5095ce62d36b40e0548d08ab7b88f4f230f74240f91757880ef",
"/workspace/scratch/c4_reliability/v3_check/check.py":"f20be5057db87ef71f83d615f361dacde11a9c51866936669e39ca88ab300c0b",
"/workspace/scratch/c4_reliability/v3_check/check.log":"7da1558aca37a14d859833b216e0b86c414c3f26a9272b6e2783aa892afee924",
"/workspace/scratch/c4_reliability/v3_build/build_v3.py":"de315b83f3c5d70148b5a2c97758312ca2719aa85dee019b603d740aba64e4cb",
"/workspace/scratch/c4_reliability/v3_build/patch_v3.py":"6daa8defdd5255a28380b4ee441fb9f29149169ff1d8bdac7b032ac59a7327fc",
"/workspace/scratch/c4_reliability/demo.py":"046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d",
"/workspace/scratch/c4_reliability/demo.log":"d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b",
"/workspace/scratch/c4_reliability/demo_results.json":"e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478",
"/workspace/scratch/c4_reliability/demo2.py":"9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb",
"/workspace/scratch/c4_reliability/demo2.log":"a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727",
"/workspace/scratch/c4_reliability/plan_counts.py":"7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391",
"/workspace/scratch/c4_reliability/plan_counts.log":"c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b"}
for f,h in exp.items(): chk("unchanged "+f.replace("/workspace/",""), hashlib.sha256(open(f,'rb').read()).hexdigest()==h)
from math import comb
chk("counts", sum(144**t for t in range(4))==3006865 and sum(144**t for t in range(1,4))==3006864 and sum(144**t for t in range(3))==20881 and 2*1365+66*2*2*11==5634 and 2*364+11*2*2*11==1212 and 3*5634==16902 and 6*8*4*8==1536 and comb(51,3)==20825 and 2*270725==541450)
print("ALL PASS" if ok else "SOME FAIL")
