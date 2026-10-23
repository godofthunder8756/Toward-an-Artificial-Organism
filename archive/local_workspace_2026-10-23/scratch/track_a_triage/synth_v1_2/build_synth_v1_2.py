import hashlib, sys
sys.path.insert(0,'/workspace/scratch/astra29'); from common29 import *
SRC='/workspace/review/track_a_claim_synthesis_v1_1.md'; DST='/workspace/review/track_a_claim_synthesis_v1_2.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='41da2819ae6e623041239e6aa6119eafb5099c017baf660effe44de7c428424c'
s=raw.decode()
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:90]); s=s.replace(a,b)
def between(a,b,new):
    global s; i=s.index(a); j=s.index(b,i+len(a)); s=s[:i]+new+s[j:]
rep("# Track A claim synthesis v1.1 (one page)","# Track A claim synthesis v1.2 (one page)")
rep("Paper only, 2026-10-21. v1.1 is built from v1 (sha256 `95888230…6f705`, unchanged). Sources: triage v1.3; the U1 audit v1.1; Astra #25, #26 and #28 (sha256 `1df2fba3…96ed`).",
f"""Paper only, 2026-10-21. v1.2 is built from v1.1 (sha256 `41da2819…8424c`, unchanged). Sources: triage v1.4; the U1 audit v1.2; Astra #25, #26, #28 and #29 (sha256 `38056d55…352ce8`).

**E29-6 (verbatim):** {E296} The PR #11 record supports this: `c4_reliability_exact_check_v1/RESULTS_v3.md` @ `0e17a05` and `c4_reliability_exact_check_v1/RESULTS_A2.md` @ `dddd63c` (triage v1.4 U10).

**Systems separation (Astra #29).** The maintained-component (AC) lineage and the GRU-8 studies (PRs #8–#10, with GRU-8 PRs #5 and #7) are separate systems; their findings do not jointly establish one organism.

""")
between("- **Q-CAUSE:**","- **Q-LEARN:**",f"""- **Q-CAUSE, AC lineage:**
  - within-model ablation dependence, including interruption during function, before death, with machinery-only rescue (F2);
  - W-gated coordinator writes, where refusal at W=0 shows the gate matters (F3);
  - endpoint agreement under the audited observer-discard procedure (F4).
- **Q-CAUSE, GRU-8 (a separate system):** bounded neural causal contribution in PR #9 FO+ISO, REPLICATED at exactly 8/10 under its declared per-seed conjunction D_FO and D_ISO, with materiality M (S15).
""")
rep("- **Q-LEARN:** two-stream acquisition and recurrent-core transfer (S12, S13).","- **Q-LEARN, GRU-8:** two-stream acquisition and recurrent-core transfer (S12, S13).")
rep("- That birth targeting is generic chemistry: `ac9.py:L108` @ `6c6323b` is supplied targeting (audit v1.1 §4.1).",
"- That birth targeting is generic chemistry. `ac9.py:L108` @ `6c6323b` is classified as supplied targeting, PROVISIONAL. The code evidence is the audit v1.2 §4.2: a host bank list selects the functional W groups, with no necessity shown. Astra #28 alone is not a code certification.")
rep("- Any W-REL separation: formal A-SEP is UNRESOLVED-COMPUTE.","- Any W-REL separation. A2 attained the reference conjunction, but named controls were not evaluated (NOT RUN).\n- One organism spanning the AC lineage and the GRU-8 studies.")
rep("3. **The O3 loop (Q-CAUSE).** Resolved by pathway interruption","3. **The O3 loop (Q-CAUSE).** Would be tested by pathway interruption")
i=s.index("6. **W-REL attainability (Track B context).**"); j=s.find("\n",i); j=len(s) if j<0 else j
s=s[:i]+"6. **W-REL (Track B context).** This is the named-control comparison at the two A2 settings. Astra #29 recommends it; it is an approval decision for Aidan (#29 §D), not proposed here. It has no Track A consequence."+s[j:]
rep('identical in the U1 audit v1.1 §5','identical in the U1 audit v1.1 and v1.2 §5')
s=s.replace('one organism.\n\n C1–C5','one organism.\n\nC1–C5')
open(DST,'w').write(s); print('ok',len(s.split()))
