import re,subprocess,sys
DOC="/workspace/review/track_a_lineage_triage_v1.md"
R="/workspace/repo"
t=open(DOC).read()
PRHEADS={"efceef3","5d9d8a7","88b500a","5f65315","379bb01","a5225eb","4f6fc4c","0329818"}
pairs=sorted(set(re.findall(r'`([^`\s]+)` @ `([0-9a-f]{7,40})`',t)))
ok=True
def g(*a): return subprocess.run(["git","-C",R,*a],capture_output=True,text=True)
for p,c in pairs:
    e=g("cat-file","-e",f"{c}:{p}").returncode==0
    msg="EXISTS" if e else "MISSING"
    if e and c not in PRHEADS:
        last=g("log","-1","--format=%h","master","--",p).stdout.strip()
        if last[:7]!=c[:7]: msg+=f" LASTTOUCH-MISMATCH(last={last})"; ok=False
    if not e: ok=False
    print(f"{msg:8} {p} @ {c}")
# counts
for pre,n in [("F",5),("S",15),("R",11),("U",11)]:
    if pre in "FU": ids=set(re.findall(rf'^### ({pre}\d+)[\. ]',t,re.M))
    else: ids=set(re.findall(rf'^\| ({pre}\d+) \|',t,re.M))
    good=len(ids)==n; ok&=good
    print(("PASS" if good else "FAIL"),pre,"count",len(ids),"expected",n,sorted(ids,key=lambda x:int(x[1:])))
# U fields
blocks=re.split(r'^### ',t,flags=re.M)
for b in blocks:
    if re.match(r'U\d+',b):
        hdr=b.split('\n')[0][:40]
        body=b.split('\n## ')[0]
        need=["Exact missing","Relevance","Stopping criterion"]
        miss=[k for k in need if k not in body and k.lower() not in body.lower()]
        if b.startswith("U10"): miss=[k for k in miss if k!="Exact missing"]  # U10 uses 'What resolves it'
        ok&= not miss
        print(("PASS" if not miss else "FAIL"),"fields",hdr,miss)
print("pairs checked:",len(pairs))
print("ALL PASS" if ok else "SOME FAIL")
