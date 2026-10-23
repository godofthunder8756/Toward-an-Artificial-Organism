import hashlib,re,subprocess
R="/workspace/review/"
F=open(R+"c4_reliability_exact_check_spec_FINAL.md").read()
V=open(R+"c4_reliability_assessment_admission_v3_2.md").read()
A=open("/workspace/astra_consult24_response.txt").read()
ok=True
def chk(n,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+n)
norm=lambda x:re.sub(r"\s+"," ",x.replace("**","").replace(">","").replace("`",""))
An=norm(A); Fn=norm(F)
req={
"e1":"The thresholds are prospective reporting conventions. Effect floors are 0.01 in each statistic's stated units; C-T2 requires a 50% reduction in baseline squared error; reproduction tolerances are 0.001 in each component's stated units. These choices are not derived from the one-trial reward gap, whose units differ. Reproduction means agreement within these declared tolerances, not exact or relative near-identity, and does not guarantee identical criterion flags. Exact statistics and criterion flags are reported separately.",
"e2":"Suspension suppresses every feedback-driven update of the declared content variable. For R-HAC-MF this includes both the q-table and g. It does not suspend trial progression, world evolution, or the matched-history shadow calculation. After the specified release boundary, normal updating resumes. SWAP versus intact is the primary content comparison; CORRUPT versus SUSPEND and the corresponding interaction are descriptive.",
"e3":"Core rescue credit is evaluated for I-SWAP-S and I-SWAP-E separately and requires both directions to pass. CORRUPT and SUSPEND rescue statistics are descriptive. In addition to the existing signed assessment and checking reversals, require L_A - L_B >= 1/100, where L_X is the probability-weighted mean of abs(m_R - m_R(H,I)) over split-read decision points in trial tau+2 on the shared perturbed-history population. The absolute value is taken before averaging. Shadow equality is an integrity check only. This criterion establishes repair of the measured assessment error and checking consequence; it does not by itself establish improved reward.",
"e4a":"For intact C-T2 and lambda_a, choose the trial index uniformly from 1 through T_SEP, draw the decision history from the specified agent's intact forward distribution, condition on a split read, and assign R and M weight 1/2 each for the combined C-T2 error. lambda_a is calculated separately for each action using the reference agent's distribution. Report separate R and M errors as well as the combined error. lambda_a is held fixed across agents and interventions within the setting.",
"e4b":"High-estimate incorrect-outcome frequency: P(K_a = 0 and m_a >= lambda_a). Low-estimate correct-outcome frequency: P(K_a = 1 and m_a < lambda_a). These are descriptive joint-event frequencies, not direct measurements of overestimation or underestimation of conditional correctness.",
"e5a":"Phase-local state retains y and the action actually taken until they are no longer required, and retains the check observation or an exactly sufficient statistic through the feedback update. The repair apparatus retains or incrementally computes the matched-history shadow content through the REPAIR-B boundary. Closure includes these caches, clamp status and all declared repair and release operations.",
"e5b":"Saved pre-perturbation content and shadow bookkeeping belong to the supplied intervention apparatus. They are inaccessible to ordinary action selection, first-order prediction and assessment decoding except through the declared repair operation. Report controller state and intervention-apparatus storage separately. The controlled transducer's equivalence claim includes the declared interventions; it does not imply that the ordinary controller possesses the apparatus's saved information.",
"e5c":"Planning estimate, not a proved upper bound. The implementation reports actual reachable counts, including phase-local caches and repair apparatus. Exceeding an estimate does not authorize truncating the state space; the unchanged hard cap applies.",
"e6":"A decoded readout is conditioned on the declared decision context, including trial, current costs and current read, as well as the decoded controller state. It excludes intervention-apparatus bookkeeping. If a perturbed controller state has zero support under the intact distribution used to define its decoder, that decoded statistic is NOT EVALUABLE unless an extension rule was explicitly specified before execution. No decoder is fitted or recalibrated on intervention outcomes. No ad hoc extension is introduced during implementation.",
"e7":"Reproduction is YES only when every required component is available and within tolerance. It is NO when at least one available component demonstrably exceeds tolerance or disagrees on an exact equality flag. Otherwise it is UNRESOLVED, with the unavailable components listed. Missing components are never imputed. Criterion-conjunction attainment remains a separate column.",
"e8":"Freeze requires incorporation of consult #24's named edits and an implementation manifest satisfying the resulting state, intervention, decoder and aggregation contracts. World parameters, thresholds and procedures become fixed for this analysis at that freeze. Scientific changes beyond these edits require a new reviewed version; engineering failures are handled under the existing integrity and compute rules.",
"r1":"a 0.001 tolerance on squared correctness error can be permissive relative to that error's entire range.",
"r4":"They are not themselves calibration-error measurements.",
"r6":"intervention closure guarantees transitions, not that an intact-distribution decoder is defined everywhere.",
"r7":"An unavailable criterion is neither a failure nor a pass. A control with another demonstrably failed criterion can still be ruled out as attaining the conjunction.",
"d1":"Do not use the submitted v3 hash as the executable identifier after editing.",
"d2":"No item, partial item or test execution is authorized until Aidan answers affirmatively and the cleared specification and implementation are frozen.",
"d3":"incorporating consults #23 and #24's required edits",
"a0":"Clearance is not execution approval: Aidan's answer remains pending.",
}
for k,s in req.items():
    chk("FINAL has "+k, s in F); chk("  source#24 has "+k, norm(s) in An)
appr="Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."
chk("FINAL approval q", appr in F); chk("v3.2 approval q", appr in V)
scope="Scope attachment to the pending W-REL approval question: the executable specification will be `c4_reliability_exact_check_spec_FINAL.md`, SHA256 [full hash], with implementation manifest [identifier and hash], incorporating consults #23 and #24's required edits. Execution covers ITEM-1 through ITEM-9 only: bounded exact analysis of the world and named analytic controllers. Limits are one CPU process, no GPU, at most four hours total wall-clock, at most one cumulative hour per named item including retries, and at most 8 GB resident memory. Verification and replay count toward these limits. The exclusions in the original approval question remain unchanged. This attachment records scope; it is not an approval."
chk("FINAL scope attachment (updated)", scope in F)
for ph in ["[AIDAN'S VERBATIM ANSWER — not yet given]","[YYYY-MM-DD]","[HH:MM ET]","[e.g. widget id / message id]","[full hash]","[identifier and hash]"]:
    chk("FINAL placeholder "+ph, ph in F)
chk("FINAL six labels", all(l in F for l in ["DISTINGUISHES NAMED CONTROLS","PATTERN REPRODUCED BY NAMED CONTROL","CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED","REFERENCE CRITERIA NOT MET","UNRESOLVED-DESIGN","UNRESOLVED-COMPUTE"]))
chk("FINAL NOT RUN / PENDING", "NOT RUN" in F and "PENDING" in F and "No implementation has been written" in F)
chk("FINAL mu_RES,L row", "| μ_RES,L | 1/100 |" in F)
chk("FINAL reproduction UNRESOLVED column","YES / NO / UNRESOLVED" in F)
for bad in ["onservative bound","one-sixth","so that \"reproduces\" means near-identity","one λ_a is shared by all agents","outcome-level overestimation frequency","outcome-level underestimation frequency","Remaining items before freeze are clerical","clerical items before freeze","consult #23's required edits","NOT FROZEN","for clearance before freezing","| reproduction of the full pattern | YES / NO |","[FINAL filename]","(or I-CORRUPT) perturbation"]:
    chk("FINAL absent: "+bad, bad not in F)
for bad in ["outcome-level overestimation and underestimation frequencies","Its §8 carries consult #23's scope attachment verbatim"]:
    chk("v3.2 absent: "+bad, bad not in V)
chk("v3.2 has e4b caveat", "These are descriptive joint-event frequencies, not direct measurements of overestimation or underestimation of conditional correctness." in V)
# reproducibility
for script,out,target in [("build_final.py","/tmp/_f.md",R+"c4_reliability_exact_check_spec_FINAL.md"),("build_v3_2.py","/tmp/_v.md",R+"c4_reliability_assessment_admission_v3_2.md")]:
    subprocess.run(["python3",script,out],check=True,capture_output=True)
    chk("byte-identical regen "+script, open(out,'rb').read()==open(target,'rb').read())
sc="/workspace/scratch/c4_reliability/"
exp={R+"c4_reliability_assessment_admission_DRAFT.md":"dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c",
R+"c4_reliability_assessment_admission_v2.md":"ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162",
R+"c4_reliability_assessment_admission_v3.md":"f122b47fbdd281a444f862021428dd3fa4e2569627f9aa745fa016fb9bde677a",
R+"c4_reliability_assessment_admission_v3_1.md":"79572a1e6925123f144e2ddcf9a684caf9764a40574bfff443ad2f6db0a72e1e",
R+"c4_reliability_exact_check_spec_draft_v1.md":"c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4",
R+"c4_reliability_exact_check_spec_v2.md":"04992f86089c616e8d8aedcd1fa5242423a242507e8be9d657ad0747f2c6601a",
R+"c4_reliability_exact_check_spec_v3.md":"8c36d575895407421fe2ca27e7bda752c7a379a007bf5bd235c6f09c7a20c776",
sc+"v2_check/check.py":"fefda82355a9ff1a27506dcb06a0333589d5555b714e0f3b47606b9bdc2a2697",
sc+"v2_check/check.log":"e6a384725bbeb5095ce62d36b40e0548d08ab7b88f4f230f74240f91757880ef",
sc+"v3_check/check.py":"f20be5057db87ef71f83d615f361dacde11a9c51866936669e39ca88ab300c0b",
sc+"v3_check/check.log":"7da1558aca37a14d859833b216e0b86c414c3f26a9272b6e2783aa892afee924",
sc+"v3_1_check/check.py":"b422ebd6b19cea426cb28afd2ff0acd7f57622cbffc5e4d3213b51933982dcf8",
sc+"v3_1_check/check.log":"818039f3e4982aef0f674c61d50910b73114b100c47a0e6f70d063a2f254e21b",
sc+"v3_build/build_v3.py":"de315b83f3c5d70148b5a2c97758312ca2719aa85dee019b603d740aba64e4cb",
sc+"v3_build/patch_v3.py":"6daa8defdd5255a28380b4ee441fb9f29149169ff1d8bdac7b032ac59a7327fc",
sc+"v3_build/build_v3_1.py":"220635640a82a43c9e1af758a61683b8a496fd8eb8c0f7644b40887622de4616",
sc+"spec_v3_build/assemble.py":"f29b4bba44d15048720a9686c382d996c790247e007d5433db6b8f00616baf78",
sc+"spec_v3_build/part_a.md":"2448eb1bac442191780e48685f9015b87410eb0b300d9556a9a55ac1a5a54927",
sc+"spec_v3_build/part_b.md":"da2542daa201caf925a32591cba582a8d7c64764ab6acd52e6285022e7766df7",
sc+"spec_v3_build/part_pm.md":"89ac7b5f74123852a7188abb9e65c7243c35c6f6e3ac2b79fcd479372469d5f3",
sc+"demo.py":"046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d",
sc+"demo.log":"d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b",
sc+"demo_results.json":"e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478",
sc+"demo2.py":"9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb",
sc+"demo2.log":"a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727",
sc+"plan_counts.py":"7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391",
sc+"plan_counts.log":"c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b"}
for f,h in exp.items(): chk("unchanged "+f.replace("/workspace/",""), hashlib.sha256(open(f,'rb').read()).hexdigest()==h)
print("FINAL sha256", hashlib.sha256(open(R+"c4_reliability_exact_check_spec_FINAL.md",'rb').read()).hexdigest())
print("v3.2 sha256", hashlib.sha256(open(R+"c4_reliability_assessment_admission_v3_2.md",'rb').read()).hexdigest())
print("ALL PASS" if ok else "SOME FAIL")
