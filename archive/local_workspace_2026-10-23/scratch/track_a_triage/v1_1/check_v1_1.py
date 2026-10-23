import re,subprocess,hashlib,os
DOC="/workspace/review/track_a_lineage_triage_v1_1.md"; R="/workspace/repo"
V1="/workspace/review/track_a_lineage_triage_v1.md"; V1_SHA="b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b"
AP="/workspace/review/c4_reliability_APPROVAL_RECORD.md"; AP_SHA="be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687"
t=open(DOC).read(); ok=True
def chk(n,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+n)
def g(*a): return subprocess.run(["git","-C",R,*a],capture_output=True,text=True)
PRHEADS={"efceef3","5d9d8a7","88b500a","5f65315","379bb01","a5225eb","4f6fc4c","0329818"}
# outside the verbatim fences for citation check
body=re.sub(r"````text\n.*?````","",t,flags=re.S)
pairs=sorted(set(re.findall(r'`([^`\s]+)` @ `([0-9a-f]{7,40})`',body)))
bad=0
for p,c in pairs:
    if g("cat-file","-e",f"{c}:{p}").returncode!=0: bad+=1; print("  MISSING",p,c); continue
    if c not in PRHEADS:
        last=g("log","-1","--format=%h","master","--",p).stdout.strip()
        if last[:7]!=c[:7]: bad+=1; print("  LASTTOUCH-MISMATCH",p,c,last)
chk(f"citations exist at cited commit / last-touch ({len(pairs)} pairs)",bad==0)
# counts
for pre,n in [("F",5),("S",15),("R",11),("U",11)]:
    ids=set(re.findall(rf'^### ({pre}\d+)[\. ]',t,re.M)) if pre in "FU" else set(re.findall(rf'^\| ({pre}\d+) \|',t,re.M))
    chk(f"{pre} count {len(ids)}=={n}",len(ids)==n)
# block helper
def block(id_):
    m=re.search(rf'^### {id_}[\. ]',t,re.M); s=m.end(); n=re.search(r'^(### |## )',t[s:],re.M); return t[s:s+n.start()]
# U fields + rival
for i in range(1,12):
    b=block(f"U{i}")
    need=["Relevance","Stopping criterion","Simplest rival"]+([] if i==10 else ["Exact missing"])
    chk(f"U{i} fields {need}",all(k in b for k in need))
# F rival + exclusion + citation
for i in range(1,6):
    b=block(f"F{i}")
    m=re.search(r'\*\*Simplest rival\.\*\*(.*?)\*\*Why foundational',b,re.S)
    chk(f"F{i} Simplest rival + Excluded + citation", bool(m) and "Excluded?" in m.group(1) and re.search(r'` @ `[0-9a-f]{7}',m.group(1)))
# S and R rival bullets (multi-line bullet: up to next top-level bullet)
for i in range(1,16):
    m=re.search(rf'^- \*\*S{i}\. Simplest rival:\*\*(.*?)(?=^- \*\*S|^\*\*|\Z)',t,re.M|re.S)
    ln=m.group(1) if m else ""
    chk(f"S{i} Simplest rival + exclusion + citation", bool(m) and re.search(r'[Ee]xcluded|[Rr]efuted|[Aa]dopted|UNVERIFIED',ln) and re.search(r'` @ `[0-9a-f]{7}',ln))
for i in range(1,12):
    chk(f"R{i} Simplest rival", re.search(rf'^- \*\*R{i}\. Simplest rival:\*\*',t,re.M))
# B3 verbatim fences
proto=g("show","0329818:frozen_recurrent_compensation_protocol_FINAL.md").stdout
chk("protocol sha eca2121c", hashlib.sha256(proto.encode()).hexdigest().startswith("eca2121c5972138580ebd8ab"))
b3=t[t.index("### B3."):t.index("### B4.")]
fences=re.findall(r"````text\n(.*?)````",b3,re.S)
chk(f"B3 has 7 verbatim excerpts ({len(fences)})",len(fences)==7)
for k,f in enumerate(fences,1):
    parts=[p for p in f.split("\n\n> \"R-FIX-32")] if k==1 else [f]
    if k==1: parts=[parts[0]+"\n","> \"R-FIX-32"+parts[1]]
    if k==7: a,b=f.split("\n\n### 8.3",1); parts=[a+"\n","### 8.3"+b]
    chk(f"B3 excerpt {k} verbatim substring(s) of protocol", all(p in proto for p in parts))
for key in ["VERIFIED TARGET PASS:\n    both evaluators give T < 1 - t","abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))",
            "assert before optimization that weight_hh is the only frozen parameter tensor","At least eight final verified passes earns TARGET REACHED REPRODUCIBLY"]:
    chk(f"B3 contains verbatim key: {key[:50]!r}", key in b3 and key in proto)
# B4 / U10
chk("B4 labelled METHOD ONLY, RESULTS PENDING", "### B4. W-REL named-rival battery (theory-stage) — METHOD ONLY, RESULTS PENDING" in t)
u10=block("U10")
chk("U10 cites approval record + sha + running", AP in u10 and AP_SHA in u10 and "Currently running" in u10 and "8:58 AM ET" in u10)
chk("approval record exists and sha matches", os.path.exists(AP) and hashlib.sha256(open(AP,'rb').read()).hexdigest()==AP_SHA)
# defaults
b5=t[t.index("### B5."):t.index("### B6.")]
chk("B5 presents defaults", "DEFAULTS each Track B study must freeze" in b5 and "These are defaults, not universal rules." in b5 and "Default 1" in b5 and "Default 2" in b5)
chk("old universal B5 header absent", "### B5. Seed bar and invalid-seed rule (shared by B1–B3)" not in t)
chk("U9 refers to frozen default", "B5 default bar" in block("U9"))
chk("stale W-REL text absent", "Executing now; results UNVERIFIED" not in t and "approved and executing; no results" not in t)
# changelog
chk("changelog present", "## Changelog against v1" in t)
# no claims
for bad_ in ["C4 established","consciousness established","is conscious","C5 established","necessity established"]:
    chk(f"forbidden phrase absent: {bad_}", bad_ not in t)
# v1 untouched + reproducible build
chk("v1 unchanged", hashlib.sha256(open(V1,'rb').read()).hexdigest()==V1_SHA)
subprocess.run(["python3","build_v1_1.py","/tmp/_v11.md"],check=True,capture_output=True)
chk("rebuild byte-identical", open("/tmp/_v11.md","rb").read()==open(DOC,"rb").read())
print("v1.1 sha256", hashlib.sha256(open(DOC,'rb').read()).hexdigest())
print("ALL PASS" if ok else "SOME FAIL")
