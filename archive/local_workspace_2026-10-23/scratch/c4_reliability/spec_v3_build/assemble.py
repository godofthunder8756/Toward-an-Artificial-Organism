v2=open("/workspace/review/c4_reliability_exact_check_spec_v2.md").read()
pa=open("part_a.md").read(); pb=open("part_b.md").read(); pm=open("part_pm.md").read()
t=v2
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:70],t.count(a)); t=t.replace(a,b)
# header
hs=t.index("## 0. World, event order")
t='''# W-REL bounded exact admission check: analysis specification and compute limit (v3, for clearance before freezing)

**Status.**
- Spec v3, revising `c4_reliability_exact_check_spec_v2.md` after Astra consult #23, part A: "REVISE the spec before freezing."
- Earlier files are left untouched:

  | file | sha256 |
  | --- | --- |
  | `c4_reliability_exact_check_spec_v2.md` | 04992f86089c616e8d8aedcd1fa5242423a242507e8be9d657ad0747f2c6601a |
  | `c4_reliability_exact_check_spec_draft_v1.md` | c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4 |

- **NOT FROZEN. NOT RUN. Execution waits on Aidan's approval (§8, PENDING).** No item, partial item or test run of any item has been executed.
- Written 2026-10-21, about 5:10–5:40 AM ET.

**Scope.**
- Theory-only. No new world, no training, no neural network, no exhaustive all-controller certificate.
- No new architecture family, no protected controller or register.
- No C4, C5 or consciousness claim.
- Companion: `c4_reliability_assessment_admission_v3_1.md` (admission v3.1). Admission v3's file is untouched.
- **Card status (consult #23):** admission v3 retains **ADMIT AS THEORY-STAGE C4 CANDIDATE** "as a card status". This is an admission status only, not a C4 claim.

**Values.** All world rates and costs remain illustrative. The analysis thresholds are **frozen in §4.6**, prospectively and with a written rationale, and are never retuned after any value is seen.

---

'''+t[hs:]
rep("- A switch-aware planning value, with the schedule known, may be reported **descriptively** as a labelled non-comparator.",
"- **Switch-aware values** (consult #23, Q4): planning with the switch schedule known is reported **descriptively** only.\n  - Its **additional information** is the identity and timing of the future cost pair.\n  - Its difference from any agent denied the schedule is **not** called a fair performance advantage.\n  - Consult #23: \"Fixed-cost episodes support the exact-optimum designation. Under switches, use **R-HAC-MB-CE**, with the persistence assumption explicit; it is not the optimal controller for an unspecified changing-cost process.\"")
rep("Σ_{t≤3} 144^t = 3,006,865 histories.","Σ_{t=0..3} 144^t = **3,006,865 histories, including the empty history** (named edit 8; lengths 1–3 alone total 3,006,864).")
rep('- c is the current cost, assumed to persist (certainty-equivalent; "R-HAC-MB-CE" under switches).',
'- c is the current cost, assumed to persist.\n  - Under fixed costs this is the exact optimum.\n  - Under switches the agent is **R-HAC-MB-CE**, with the persistence assumption explicit. It is not the optimal controller for an unspecified changing-cost process.')
rep("### 3.3 R-BLIND and R-CONF-S","### 3.3 R-BLIND / R-CONF-S (one control, both names; consult #23, Q8)")
rep("So **R-CONF-S coincides with R-BLIND by definition**; it is reported once, with this identity disclosed.",
"So **R-CONF-S coincides with R-BLIND by definition**. It is recorded as **one control, \"R-BLIND / R-CONF-S\"**, with both names and the identity disclosed.")
rep("This is a myopic contextual learner by declaration. A bootstrapped variant is an open question (§9).",
"R-HAC-MF is explicitly a **myopic contextual action-value learner** (consult #23, Q5). No γ = 1 variant is included.\n- Consult #23: \"A gamma = 1 variant needs a separately specified return, cost treatment, bootstrap and terminal rule.\"\n- The non-myopic Bayes reference supplies the planning comparison.")
s=t.index("### 3.7 PM-ACT"); e=t.index("### 3.8 Resource ledger")
t=t[:s]+pm+t[e:]
rep('''- R-BLIND (≡ R-CONF-S);''','''- R-BLIND / R-CONF-S (one control);''')
rep('''- Labels are issued per (T_SEP, cost pair).''','''- Labels are issued separately per setting (T_SEP, cost pair), each with its eligible-control list:
  - **T_SEP = 3:** MB-myopic, R-BLIND / R-CONF-S, R-CONF-A (9), R-CG (6), R-HAC-MF (2), PM-ACT.
  - **T_SEP = 4:** the same without R-HAC-MF. "A T = 4 result cannot claim to distinguish MF."''')
s=t.index("### 4.2 Reachable states"); t=t[:s]+pa+pb
open("/workspace/review/c4_reliability_exact_check_spec_v3.md","w").write(t)
print(len(t))
