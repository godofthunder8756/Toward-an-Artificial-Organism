import hashlib,sys,re
V2="/workspace/review/c4_reliability_assessment_admission_v2.md"
SP="/workspace/review/c4_reliability_exact_check_spec_draft_v1.md"
DR="/workspace/review/c4_reliability_assessment_admission_DRAFT.md"
v=open(V2).read(); s=open(SP).read()
ok=True
def chk(name,cond):
    global ok; ok&=cond; print(("PASS " if cond else "FAIL ")+name)
req={
"edit1":"Reproduction by a conventional rival is recorded under REDUCTION. It disqualifies the proposed role only when it shows that the observations and interventions do not identify that role. A conventional implementation satisfying the role criteria may provide C4-relevant functional evidence; its ORIGIN is recorded separately.",
"edit2":"The illustrative single-trial construction demonstrates identical default predictive information with different values of alternative checks. It establishes pressure for source-dependent information acquisition. It does not establish assessment of the learner's own representation, history-level source identifiability, or acquired evaluation.",
"edit3":"The assessed object, prediction time and correctness criterion must be specified. Candidate assessment content must predict the learner's own conditional performance, not merely the Bayes oracle's performance. False alarms and misses must concern that assessment and track manipulated assessment content while the declared first-order controls hold.",
"edit4":"C-FO establishes preservation only over the prespecified first-order probe battery. Output preservation alone is not described as preservation of the full first-order state. Direct inference effects under matched subsequent observations are reported separately and constrain the dissociation claim.",
"edit5_world":"Z_t in {S, E}, with a specified persistent transition law. S uses (w,e) = (1/20, 1/5). E uses (w,e) = (1/5, 1/20).",
"edit6":"R-HAC-MB uses the posterior over the specified latent process and a policy accounting for both immediate reward and future information value over the declared horizon. A myopic version is reported separately.",
"edit7":"Decoder or intervention failure means the proposed content was not identified or causally dissociated by this procedure. It does not establish absence of assessment. A failed C4 test does not itself establish a C3 role; only independently supported lower-level claims are retained.",
"edit7b":"Engineering failures require diagnosis; scientific criterion changes require a new version.",
"edit8":'This is **theory about C4 admission**, not evidence that the work is "below C4 throughout." It authorizes no empirical study and establishes no C4 status.',
"Q1":'an ordinary Bayes filter can instantiate a C4-relevant functional role. "REDUCED to a conventional mechanism" does not automatically mean "classified C3." ORIGIN, ROLE and REDUCTION must remain separate.',
"Q2":"Bayes-optimal checking gain is not interchangeable with the learned predictor's correctness gain.",
"Q3":"An otherwise identical external sensor can generate the same observations.",
"Q4":"The second category limits the dissociation claim; it cannot simply be declared irrelevant.",
"Q5":"Decoder accuracy alone does not validate the transplant direction",
"Q6a":"action_value(a) = estimated_correctness(a, history) - current_cost(a)",
"Q6b":"Give every rival the visible costs; do not manufacture separation by withholding them or forcing categorical cost bins.",
"Q6c":"A learned confidence head may carry historical information that an analytic `P(X|y)` head does not.",
"Q7":'Until then, "same-resource ALL(B)" is undefined.',
"Q8":"A Bayes filter followed by myopic action selection is not generally the optimal controller when rechecks inform future trials.",
"Q9":"There is no requirement to execute the older design first.",
}
appr="Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."
for k,t in req.items(): chk("v2 verbatim "+k, t in v)
chk("v2 approval question verbatim", appr in v)
chk("spec approval question verbatim", appr in s)
for bad in ["re-replay","then park","Below C4 throughout","C3-plus-annotation","P(I = faulty | history)","e_ok","R-HAC-ALL(B) at frozen rates"]:
    chk("v2 absent: "+bad, bad not in v)
chk("lowercase 'below C4 throughout' only inside edit 8", v.count("below C4 throughout")==1)
chk("v2 has PENDING", "PENDING" in v); chk("spec has PENDING + NOT RUN","PENDING" in s and "NOT RUN" in s)
chk("spec hard cap present","HARD CAP" in s and "8 GB" in s and "4 hours" in s)
dsha=hashlib.sha256(open(DR,'rb').read()).hexdigest()
chk("DRAFT sha unchanged", dsha=="dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c")
base="/workspace/scratch/c4_reliability/"
exp={"demo.py":"046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d","demo.log":"d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b","demo_results.json":"e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478","demo2.py":"9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb","demo2.log":"a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727","plan_counts.py":"7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391","plan_counts.log":"c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b"}
for f,h in exp.items(): chk("artifact sha "+f, hashlib.sha256(open(base+f,'rb').read()).hexdigest()==h)
from math import comb
chk("counts", comb(21,11)==352716 and comb(20,10)==184756 and comb(20,12)==125970 and sum(11**t for t in range(6))==177156 and comb(12,10)+comb(14,10)+comb(16,10)==9075 and sum(144**t for t in range(4))==3006865)
# astra text presence in consult file
a=open("/workspace/astra_consult21_response.txt").read()
norm=lambda x:re.sub(r"\s+"," ",x.replace("**",""))
an=norm(a)
for k in ["edit1","edit2","edit3","edit4","edit6","edit7","Q2","Q3","Q4","Q5","Q8","Q9"]:
    chk("source contains "+k, norm(req[k]) in an)
chk("source contains approval q", norm(appr) in an)
print("ALL PASS" if ok else "SOME FAIL")
