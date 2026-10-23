import re,hashlib,subprocess
D="/workspace/review/track_a_lineage_triage_v1_1_astra_digest.md"; S="/workspace/review/track_a_lineage_triage_v1_1.md"
V1="/workspace/review/track_a_lineage_triage_v1.md"
d=open(D).read(); s=open(S).read(); ok=True
def chk(n,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+n)
n=int(subprocess.run(["wc","-c",D],capture_output=True,text=True).stdout.split()[0])
chk(f"(a) byte size {n} <= 35840",n<=35840)
for i in range(1,12):
    m=re.search(rf'^### U{i}[\. ]',d,re.M); nx=re.search(r'^(### |---$)',d[m.end():],re.M)
    b=d[m.start():m.end()+nx.start()].rstrip('\n')+'\n'
    chk(f"(b) U{i} byte-exact substring of v1.1 ({len(b.encode())} B) and has rival/relevance/stopping", b in s and "Simplest rival" in b and "Relevance" in b and "Stopping criterion" in b and (i==10 or "Exact missing" in b))
ids=[f"{p}{i}" for p,n_ in [("F",5),("S",15),("R",11),("U",11)] for i in range(1,n_+1)]
missing=[x for x in ids if not re.search(rf'\*\*{x}\*\*|^### {x}[\. ]',d,re.M)]
chk(f"(c) all 42 ids present (missing={missing})",not missing)
bad=["C4 established","C5 established","consciousness established","is conscious","necessity established","autopoietic system","alive system","proves consciousness"]
chk("(d) forbidden phrases absent",not [b for b in bad if b in d])
chk("header cites path and full sha","`/workspace/review/track_a_lineage_triage_v1_1.md`" in d and "d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef" in d)
chk("caveats: S12 UNVERIFIED, PR#3, quoted numbers, Q-lock, W-REL sha, ceiling", all(k in d for k in ["**S12:**","PR #3 re-audit limit","UNVERIFIED at row level","Q-separation lock","be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687","No C4, C5 or consciousness claim"]))
chk("B4 METHOD ONLY label and 8/10 default", "METHOD ONLY, RESULTS PENDING" in d and "defaults that each Track B study must freeze" in d)
chk("v1.1 unchanged", hashlib.sha256(open(S,'rb').read()).hexdigest()=="d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef")
chk("v1 unchanged", hashlib.sha256(open(V1,'rb').read()).hexdigest()=="b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b")
subprocess.run(["python3","build_digest.py","/tmp/_dg.md"],check=True,capture_output=True)
chk("rebuild byte-identical", open("/tmp/_dg.md","rb").read()==open(D,"rb").read())
print("digest sha256",hashlib.sha256(open(D,'rb').read()).hexdigest())
print("ALL PASS" if ok else "SOME FAIL")
