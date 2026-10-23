import hashlib,re
R="/workspace/review/"
V3=open(R+"c4_reliability_assessment_admission_v3.md").read()
S2=open(R+"c4_reliability_exact_check_spec_v2.md").read()
A=open("/workspace/astra_consult22_response.txt").read()
ok=True
def chk(n,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+n)
norm=lambda x:re.sub(r"\s+"," ",x.replace("**","").replace(">","").replace("`",""))
An=norm(A)
v3_req={
"status":"A: ADMIT AS THEORY-STAGE C4 CANDIDATE, with the interpretive edits below.** This admits the question for analytic investigation, not the proposed separation test or any C4 conclusion.",
"assumptions":"State explicitly that X values, costs and policy randomization are independent of Z, and that Z evolves exogenously. Under those assumptions, the L1 factorization argument is sound.",
"L1":"Without recheck observations, the observation history supplies no information about Z beyond its propagated prior. Recheck observations can be informative. This does not imply perfect identification of the realized regime within a finite horizon.",
"audit":"The T <= 3 audit checks the implementation. The factorization proof, not that finite audit alone, supports the general horizon claim.",
"edit8":"The analysis reports which prespecified response patterns distinguish the named analytic implementations. Policy minimization alone does not establish absence of an assessment role. Any stronger construct-identification claim requires additional justification.",
"RCG":"A prespecified family of cost-general conventional baselines; conclusions are restricted to these implementations.",
"acq":"The analytic agents have supplied mechanisms and update rules. Their results cannot establish acquisition, even if a controller updates its counts online.",
"fixedreplay":"A fixed replay produces one counterfactual outcome. It does not produce `E[K(a) | information]`.",
"bound":"If every estimated action correctness changes by at most epsilon,\nan action-value gap greater than 2*epsilon cannot change sign.",
"approvalrec":"Add the final spec identifier and the four-hour/one-hour/eight-GB limits to the approval record. Do not ask Aidan to approve the same scope again if he approves that question with this specification attached.",
}
s2_req={
"eventorder":"prior over current Z\n-> current y\n-> action\n-> check observation, if any\n-> prediction\n-> outcome X revealed\n-> posterior update using feedback\n-> regime transition\n-> next trial",
"tie":"prediction 1 iff `p > 1/2`, otherwise 0",
"noleak":"The ten likelihood-ratio classes use revealed X. They may compress the feedback update; they must not leak X into the preceding prediction",
"switch":"old costs through trial `floor(T/2)`, new costs thereafter",
"bayesinfo":"Bayes planning must use the same available information as the rivals.",
"voi":"planning_advantage_T = V* - V_myopic\nadaptive_information_advantage_T = V* - V_blind\noracle_gap_T = V_oracle - V*",
"voi2":"Both Bayes agents acquire and use information, so their difference is not total information value.",
"F0":"A common fixed first-order predictor is permissible for analytic controls, but must be declared as supplied and used consistently.",
"enum":"the nine deterministic tables are an enumeration of mappings, not automatically nine versions of that formula.",
"untaken":"Untaken-action replay remains analysis-only.",
"edit7":"Primitive world probabilities have terminating decimal denominators. Posterior normalization, count estimates and randomized policies may introduce other factors. All computations use exact rationals with unrestricted positive integer denominators.",
"edit8":v3_req["edit8"],
"acq":v3_req["acq"],
"RCG":v3_req["RCG"],
"noreg":"Lack of a named posterior register is not a failed criterion.",
"beliefnodes":"Belief nodes do not uniquely specify count-controller or Q-controller states.",
"donor":"An extreme Bayes belief need not correspond to a unique count or Q state.",
"m_a":"m_a(H) = sum_omega P(omega | H) *\n         1[agent_prediction(H, do(a), omega) = X(omega)]",
"recipient":"retain the recipient's world distribution while changing the specified agent content. Do not replace the recipient's world with the donor's world.",
"score":"Score expected correctness against expected correctness.",
"calib":"even a perfectly calibrated predictor sometimes encounters an unlikely outcome.",
"reset":"A reset followed by an intact rerun remains integrity-only",
"lab1":"the reference meets the prespecified core criteria, and every eligible named control fails at least one core criterion under comparable procedures.",
"lab2":"at least one control reproduces the full prespecified response pattern.",
"lab3":"the reference does not meet the required conjunction.",
"lab4":"an output, intervention correspondence or criterion is undefined.",
"lab5":"the required calculation is incomplete.",
"neither":"Neither of the first two labels automatically establishes assessment-versus-policy separation. That interpretation additionally requires a justified account of whether the reproducing control implements the role.",
"pmnot":"PM_k is therefore not automatically a known \"role-absent\" control.",
"cap1":"Include replay and restarts after engineering failures in the accounting.",
"cap2":"Preserve completed exact results when a cap is reached, but do not issue an overall label whose required comparisons remain incomplete.",
"cap3":"Mark dependent unexecuted work as NOT-RUN, rather than pretending it failed scientifically.",
"cap4":"No in-place reduction of horizons or variants.",
"bound":v3_req["bound"],
"L1":v3_req["L1"],
"audit":v3_req["audit"],
"approvalrec":"Add the final spec identifier and the four-hour/one-hour/eight-GB limits to the approval record.",
"reapproval":"Do not ask Aidan to approve the same scope again if he approves that question with this specification attached.",
}
appr="Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."
for k,s in v3_req.items():
    chk("v3 has "+k, s in V3); chk("  source#22 has "+k, norm(s) in An)
for k,s in s2_req.items():
    chk("spec2 has "+k, s in S2)
    if k not in ("F0x",): chk("  source#22 has "+k, norm(s) in An or k in ("edit8x",))
chk("v3 approval q", appr in V3); chk("spec2 approval q", appr in S2)
chk("five labels in spec2", all(l in S2 for l in ["DISTINGUISHES NAMED CONTROLS","PATTERN REPRODUCED BY NAMED CONTROL","REFERENCE CRITERIA NOT MET","UNRESOLVED-DESIGN","UNRESOLVED-COMPUTE"]))
chk("core criteria named", "C-REF, C-T2, C-SEL, C-FO and the specified rescue" in S2)
chk("spec2 PENDING/NOT RUN", "PENDING" in S2 and "NOT RUN" in S2)
chk("cap numbers", all(x in S2 for x in ["≤ 4 hours total","≤ 1 hour per named item","≤ 8 GB"]))
# stale text absent
for bad in ["VOI_T","SEPARATES","DOES-NOT-SEPARATE","fixed noise seed","powers of 2 and 5","decisive conventional rival]","9,075 recipient","T·v_blind, by the L1"]:
    chk("spec2 absent: "+bad, bad not in S2 or (bad=="9,075 recipient" and False))
for bad in ["SEPARATES","fixed noise seed","the decisive conventional rival]","(decisive)","re-replay","then park","Below C4 throughout","separate an assessment variable from a policy-minimal machine","can separate an own-correctness","draft_v1.md`. It is PENDING","What is the finite-horizon VOI"]:
    chk("v3 absent: "+bad, bad not in V3)
chk("spec2 mentions 9,075 only as not applied", S2.count("9,075")==1 and "is **not** applied" in S2)
chk("v3 admission status != C4 claim stated", "It is **not a C4 claim**" in V3)
# hashes of earlier files unchanged
exp={R+"c4_reliability_assessment_admission_DRAFT.md":"dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c",
R+"c4_reliability_assessment_admission_v2.md":"ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162",
R+"c4_reliability_exact_check_spec_draft_v1.md":"c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4",
"/workspace/scratch/c4_reliability/v2_check/check.py":"fefda82355a9ff1a27506dcb06a0333589d5555b714e0f3b47606b9bdc2a2697",
"/workspace/scratch/c4_reliability/v2_check/check.log":"e6a384725bbeb5095ce62d36b40e0548d08ab7b88f4f230f74240f91757880ef",
"/workspace/scratch/c4_reliability/demo.py":"046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d",
"/workspace/scratch/c4_reliability/demo.log":"d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b",
"/workspace/scratch/c4_reliability/demo_results.json":"e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478",
"/workspace/scratch/c4_reliability/demo2.py":"9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb",
"/workspace/scratch/c4_reliability/demo2.log":"a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727",
"/workspace/scratch/c4_reliability/plan_counts.py":"7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391",
"/workspace/scratch/c4_reliability/plan_counts.log":"c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b"}
for f,h in exp.items(): chk("unchanged "+f.split('/')[-1]+(" (v2_check)" if "v2_check" in f else ""), hashlib.sha256(open(f,'rb').read()).hexdigest()==h)
from math import comb
chk("counts", comb(52,4)==270725 and comb(51,3)==20825 and sum(48**t for t in range(4))==112945 and sum(2**t*comb(t+10,10) for t in range(5))==18591 and comb(22,12)-1==646645 and sum(comb(t+10,10) for t in range(5))==1365 and sum(comb(t+10,10) for t in range(4))==364 and sum(sum(11**t for t in range(T+1)) for T in range(1,6))==194870 and sum(24**t for t in range(5))==346201 and comb(17,11)==12376 and comb(20,12)==125970)
print("ALL PASS" if ok else "SOME FAIL")
