p="/workspace/review/c4_reliability_assessment_admission_v3.md"; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:60],t.count(a)); t=t.replace(a,b)
rep("and spec §2 VOI |","and spec v2 §2 (planning and adaptive-information advantages) |")
rep("Finite-horizon values against adaptive controllers are spec §2–§3 (pending).","Finite-horizon values against adaptive controllers are spec v2 §2–§3 (pending, not run).")
rep("- **F-W2 (history-level) [new].** A-SYM (spec §1) finds a non-RECHECK history with Z-dependent likelihood. L1 is then false, and the persistent-world identifiability claim is withdrawn.",
"- **F-W2 (history-level) [new; revised in v3].** A-SYM (spec v2 ITEM-1) finds a non-RECHECK history with a Z-dependent likelihood.\n  - Because the audit checks the implementation, the discrepancy is first diagnosed: implementation error, or violation of assumptions (i)–(iv).\n  - If the factorization proof itself is shown wrong, L1 and the persistent-world claim are withdrawn.")
rep("| 2. PM test / SEPARATES |","| 2. PM test and the v2 binary label |")
open(p,"w").write(t)
