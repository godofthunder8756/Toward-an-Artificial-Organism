import hashlib, sys
sys.path.insert(0,'/workspace/scratch/u1_audit/v1_1'); from common import *
SRC='/workspace/review/track_a_claim_synthesis_v1.md'; DST='/workspace/review/track_a_claim_synthesis_v1_1.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='95888230db56906b7eb82b0936d04f6a897cbabd8062587c315f4a4aa3f26705'
s=raw.decode()
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:80]); s=s.replace(a,b)
def between(a,b,new):
    global s; i=s.index(a); j=s.index(b,i+len(a)); s=s[:i]+new+s[j:]
rep("# Track A claim synthesis v1 (one page)","# Track A claim synthesis v1.1 (one page)")
rep("Paper only, 2026-10-21. Sources: triage v1.2; the U1 audit (sha256 `48c174f5…f13a`); Astra #25 and #26.",
"Paper only, 2026-10-21. v1.1 is built from v1 (sha256 `95888230…6f705`, unchanged). Sources: triage v1.3; the U1 audit v1.1; Astra #25, #26 and #28 (sha256 `1df2fba3…96ed`).")
between("**Closure sentence (verbatim from the U1 audit §5)**","**What Track A can claim, by Q-tag**",f"""**Closure sentence (verbatim from Astra #28; identical in the U1 audit v1.1 §5)**

> {NEW}

**E28-2 (verbatim):** {E2}

**E28-1 (verbatim):** {E1}

**T1 (verbatim):** {T1Q}

""")
rep("- **Q-EXIST:** the bounded, conditional closure statement above, with reconstruction of inherited content through a supplied decoder (F5).",
"- **Q-EXIST:** the closure statement above, which is bounded and not an established closure claim. It comes with reconstruction of inherited content through a supplied decoder (F5). C1–C5 for W/C/B are not re-certified by the code reading.")
rep("including interruption while alive with machinery-only rescue (F2);","including interruption during function, before death, with machinery-only rescue (F2);")
rep("- Production closure of the full network under the consult #25 rule.",
"- Production closure of the full declared network under the consult #25 rule.\n- That birth targeting is generic chemistry: `ac9.py:L108` @ `6c6323b` is supplied targeting (audit v1.1 §4.1).")
rep("- Per consult #25, U3 is held, not proposed. Proposing it for the Q-CAUSE claim is Aidan's decision.",
"- U3 is held, not proposed (consult #25; on hold per #28). Proposing it is Aidan's decision.")
between("**Top remaining uncertainties.**","3. **The O3 loop (Q-CAUSE).**",f"""**Directives (Astra #28, verbatim).** {STOP} {SKETCH2}

**Top remaining uncertainties.** Each resolution is a future protocol or ruling needing approval; none is proposed or run here.
1. **Forced bank-rule enablement (I3r).** Does it hard-wire an organization-specific action? Paper only. Q-A1 and Q-A2 were ruled in #28.
2. **Can closure hold with coordination and targeting in declared state?** A damageable, declared transition table is SKETCH ONLY, not a proposal. It must cover the table's own production, triggers, scheduling and bootstrapping, and run without host restoration. It needs separate, concrete approval.
""")
open(DST,'w').write(s); print('ok', len(s.split()))
