
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
import random, math, statistics, hashlib, json
from pathlib import Path

ARCHS = ["S0","S1","S2","S3","S4","H_ERROR","H_EXTERNAL"]
DEV_SEEDS = list(range(52001,52021))

@dataclass
class Trial:
    seed:int
    idx:int
    label:int
    signal:int
    family:str
    difficulty:float
    latent_impairment:float
    diagnostic_a:float
    diagnostic_b:float
    self_relevant:bool

@dataclass
class Outcome:
    architecture:str
    correct:int
    checked:int
    extra_compute:int
    utility:float
    q_used:Optional[float]
    q_self:float
    q_world:float
    impaired:int
    family:str
    idx:int

def clamp(x,a,b): return max(a,min(b,x))

def true_success(t:Trial)->float:
    return clamp(0.5 + (t.difficulty-0.5)*t.latent_impairment,0.5,0.995)

def make_trial(seed:int, idx:int, family:str, impaired:bool, self_relevant:bool=True)->Trial:
    rng=random.Random(seed*1000003 + idx*1009 + (1 if family=="decision" else 7))
    if family=="decision":
        difficulty = [0.68,0.76,0.86,0.92][idx%4]
    elif family=="verification":
        difficulty = [0.66,0.74,0.82,0.90][idx%4]
    else:
        raise ValueError(family)
    # Hidden impairment is only partially reflected in any single diagnostic.
    latent = (0.28 + 0.10*rng.random()) if impaired else (0.92 + 0.06*rng.random())
    da = clamp(latent + rng.gauss(0,0.18),0,1)
    db = clamp(math.sqrt(latent) + rng.gauss(0,0.16),0,1)
    label=rng.randrange(2)
    p=0.5 + (difficulty-0.5)*latent
    signal=label if rng.random()<p else 1-label
    return Trial(seed,idx,label,signal,family,difficulty,latent,da,db,self_relevant)

def self_monitor(t:Trial)->float:
    # Combines two noisy diagnostics; no privileged label/outcome access.
    rel_hat=clamp(0.58*t.diagnostic_a + 0.42*(t.diagnostic_b**2),0,1)
    return clamp(0.5 + (t.difficulty-0.5)*rel_hat,0.505,0.995)

def world_monitor(t:Trial)->float:
    return clamp(t.difficulty,0.505,0.995)

def act(t:Trial, arch:str, *, q_override=None, shuffled_q=None,
        prev_error=False, check_threshold=0.70, compute_threshold=0.68,
        check_cost=0.13, compute_cost=0.05)->Outcome:
    qself=self_monitor(t); qworld=world_monitor(t)
    q=None; checked=0; compute=0
    if arch=="S0": pass
    elif arch=="S1": q=qself
    elif arch=="S2":
        q=qself if q_override is None else q_override
        if t.family=="decision":
            checked=int(q<check_threshold)
        else:
            compute=int(q<compute_threshold)
    elif arch=="S3":
        q=shuffled_q if shuffled_q is not None else qself
        if t.family=="decision": checked=int(q<check_threshold)
        else: compute=int(q<compute_threshold)
    elif arch=="S4":
        q=qworld
        if t.family=="decision": checked=int(q<check_threshold)
        else: compute=int(q<compute_threshold)
    elif arch=="H_ERROR":
        if t.family=="decision": checked=int(prev_error)
        else: compute=int(prev_error)
    elif arch=="H_EXTERNAL":
        q=true_success(t)
        if t.family=="decision": checked=int(q<check_threshold)
        else: compute=int(q<compute_threshold)
    else: raise ValueError(arch)

    if checked:
        rr=random.Random(t.seed*2000003+t.idx*101+31)
        correct=int(rr.random()<0.985)
        utility=correct-check_cost
    elif compute:
        # additional compute selectively improves reliability, not perfectly
        rr=random.Random(t.seed*3000017+t.idx*107+53)
        p=min(0.96,true_success(t)+0.24)
        correct=int(rr.random()<p)
        utility=correct-compute_cost
    else:
        correct=int(t.signal==t.label)
        utility=float(correct)
    return Outcome(arch,correct,checked,compute,utility,q,qself,qworld,
                   int(t.latent_impairment<0.7),t.family,t.idx)

def deranged(values, seed):
    n=len(values); idx=list(range(n)); r=random.Random(seed); r.shuffle(idx)
    if n>1:
        for i in range(n):
            if idx[i]==i:
                j=(i+1)%n; idx[i],idx[j]=idx[j],idx[i]
    return [values[j] for j in idx]

def run_family(seed:int, family:str, arch:str, n=320, *,
               pattern="mixed", self_relevant=True):
    trials=[]
    for i in range(n):
        if pattern=="mixed": impaired=(i%4 in (2,3))
        elif pattern=="healthy": impaired=False
        elif pattern=="blocks": impaired=(i>=n//2)
        elif pattern=="alternating": impaired=(i%2==1)
        else: raise ValueError(pattern)
        trials.append(make_trial(seed,i,family,impaired,self_relevant))
    qs=[self_monitor(t) for t in trials]
    # Exact distribution-matched adversarial shuffle: reverse-rank assignment.
    # This preserves the full multiset of monitor values while maximally breaking
    # correspondence with the current state, making S3 a serious H5.4 control.
    order=sorted(range(len(qs)), key=lambda i: qs[i])
    reversed_vals=[qs[i] for i in reversed(order)]
    shuffled=[None]*len(qs)
    for rank,i in enumerate(order):
        shuffled[i]=reversed_vals[rank]
    out=[]; prev=False
    for i,t in enumerate(trials):
        o=act(t,arch,shuffled_q=shuffled[i],prev_error=prev)
        out.append(o); prev=(o.correct==0)
    return out

def summarise(rows):
    n=len(rows)
    return {
      "accuracy":sum(x.correct for x in rows)/n,
      "utility":sum(x.utility for x in rows)/n,
      "check_rate":sum(x.checked for x in rows)/n,
      "compute_rate":sum(x.extra_compute for x in rows)/n,
    }

def misinformation(seed:int, family:str, n=220):
    trials=[make_trial(seed,i,family,True,True) for i in range(n)]
    cond={"accurate":None,"overconfident":0.96,"underconfident":0.54,"restored":None}
    ans={}
    for name,qfix in cond.items():
        rows=[]
        for t in trials:
            q=self_monitor(t) if qfix is None else qfix
            rows.append(act(t,"S2",q_override=q))
        ans[name]=summarise(rows)
    return ans

def recovery(seed:int, family:str, arch:str, npre=60,npost=120):
    trials=[make_trial(seed,i,family,i>=npre,True) for i in range(npre+npost)]
    qs=[self_monitor(t) for t in trials]
    # Stronger shuffled control: exact multiset from same run but anti-aligned by impairment class.
    healthy=[q for i,q in enumerate(qs) if i<npre]
    impaired=[q for i,q in enumerate(qs) if i>=npre]
    shuf=[]
    r=random.Random(seed+777)
    for i in range(npre+npost):
        pool=impaired if i<npre else healthy
        shuf.append(pool[r.randrange(len(pool))])
    rows=[]; prev=False
    used=[]
    for i,t in enumerate(trials):
        q=None
        if arch=="S3": q=shuf[i]
        o=act(t,arch,shuffled_q=q,prev_error=prev)
        rows.append(o); prev=(o.correct==0); used.append(o.q_used)
    post=rows[npre:]
    lat=None
    for k,o in enumerate(post,1):
        if o.q_used is not None and o.q_used < (0.70 if family=="decision" else 0.78):
            lat=k; break
    return {
      "pre":summarise(rows[:npre]), "post":summarise(post),
      "detection_latency":lat,
      "mean_q_pre":sum(q for q in used[:npre] if q is not None)/max(1,sum(q is not None for q in used[:npre])),
      "mean_q_post":sum(q for q in used[npre:] if q is not None)/max(1,sum(q is not None for q in used[npre:])),
    }

def capability_boundary(seed:int, n=360):
    # Calibration is assessed on the monitor's prediction of the *unassisted*
    # decision outcome, separately from any checking/compute policy. This avoids
    # crediting the monitor with the accuracy improvement caused by its own intervention.
    rows=[]
    for i in range(n):
        family="decision"
        t=make_trial(seed,i,family,False,True)
        t.difficulty=0.58 + 0.40*(i/(n-1))
        q=self_monitor(t)
        correct=int(t.signal==t.label)
        rows.append((q,correct,t.difficulty))
    bins=[]
    for b in range(6):
        lo=.5+b*(.5/6); hi=.5+(b+1)*(.5/6)
        rr=[x for x in rows if lo<=x[0]<(hi if b<5 else hi+1e-9)]
        if rr:
            bins.append(abs(sum(x[0] for x in rr)/len(rr)-sum(x[1] for x in rr)/len(rr)))
    return {"calibration_mae":sum(bins)/len(bins),"n_bins":len(bins)}

def self_vs_world(seed:int,n=240):
    vals=[]
    for i in range(n):
        t=make_trial(seed,i,"decision",i>=n//2,True)
        vals.append((self_monitor(t),world_monitor(t),true_success(t),i>=n//2))
    def mae(j):return sum(abs(x[j]-x[2]) for x in vals)/len(vals)
    return {
      "self_mae":mae(0),"world_mae":mae(1),
      "self_healthy":sum(x[0] for x in vals if not x[3])/(n//2),
      "self_impaired":sum(x[0] for x in vals if x[3])/(n//2),
      "world_healthy":sum(x[1] for x in vals if not x[3])/(n//2),
      "world_impaired":sum(x[1] for x in vals if x[3])/(n//2),
    }

def dev_seed(seed:int):
    data={"seed":seed,"families":{},"misinformation":{},"recovery":{}}
    for fam in ("decision","verification"):
        data["families"][fam]={}
        for arch in ARCHS:
            data["families"][fam][arch]=summarise(run_family(seed,fam,arch))
        data["misinformation"][fam]=misinformation(seed,fam)
        data["recovery"][fam]={a:recovery(seed,fam,a) for a in ARCHS}
    data["boundary"]=capability_boundary(seed)
    data["self_vs_world"]=self_vs_world(seed)
    return data

def aggregate(recs):
    def mean(path):
        vv=[]
        for r in recs:
            x=r
            for p in path:x=x[p]
            vv.append(x)
        return sum(vv)/len(vv)
    A={"n_seeds":len(recs),"families":{},"misinformation":{},"recovery":{}}
    for fam in ("decision","verification"):
        A["families"][fam]={}
        for a in ARCHS:
            A["families"][fam][a]={k:mean(["families",fam,a,k]) for k in ("accuracy","utility","check_rate","compute_rate")}
        A["misinformation"][fam]={}
        for c in ("accurate","overconfident","underconfident","restored"):
            A["misinformation"][fam][c]={k:mean(["misinformation",fam,c,k]) for k in ("accuracy","utility","check_rate","compute_rate")}
        A["recovery"][fam]={}
        for a in ARCHS:
            A["recovery"][fam][a]={
              "post_accuracy":mean(["recovery",fam,a,"post","accuracy"]),
              "post_utility":mean(["recovery",fam,a,"post","utility"]),
              "post_check_rate":mean(["recovery",fam,a,"post","check_rate"]),
              "post_compute_rate":mean(["recovery",fam,a,"post","compute_rate"])
            }
            det=[r["recovery"][fam][a]["detection_latency"] for r in recs if r["recovery"][fam][a]["detection_latency"] is not None]
            A["recovery"][fam][a]["median_detection_latency"]=statistics.median(det) if det else None
    A["boundary_calibration_mae"]=mean(["boundary","calibration_mae"])
    A["self_vs_world"]={k:mean(["self_vs_world",k]) for k in recs[0]["self_vs_world"]}
    A["diagnostics"]={
      "decision_active_passive_gain":A["families"]["decision"]["S2"]["accuracy"]-A["families"]["decision"]["S1"]["accuracy"],
      "verification_active_passive_gain":A["families"]["verification"]["S2"]["accuracy"]-A["families"]["verification"]["S1"]["accuracy"],
      "decision_shuffled_gap":A["families"]["decision"]["S2"]["accuracy"]-A["families"]["decision"]["S3"]["accuracy"],
      "verification_shuffled_gap":A["families"]["verification"]["S2"]["accuracy"]-A["families"]["verification"]["S3"]["accuracy"],
      "decision_recovery_gain":A["recovery"]["decision"]["S2"]["post_accuracy"]-A["recovery"]["decision"]["S1"]["post_accuracy"],
      "verification_recovery_gain":A["recovery"]["verification"]["S2"]["post_accuracy"]-A["recovery"]["verification"]["S1"]["post_accuracy"],
      "decision_overconfidence_effect":A["misinformation"]["decision"]["overconfident"]["accuracy"]-A["misinformation"]["decision"]["accurate"]["accuracy"],
      "verification_overconfidence_effect":A["misinformation"]["verification"]["overconfident"]["accuracy"]-A["misinformation"]["verification"]["accurate"]["accuracy"],
      "decision_rescue":A["misinformation"]["decision"]["restored"]["accuracy"]-A["misinformation"]["decision"]["overconfident"]["accuracy"],
      "verification_rescue":A["misinformation"]["verification"]["restored"]["accuracy"]-A["misinformation"]["verification"]["overconfident"]["accuracy"],
      "self_vs_world_mae_advantage":A["self_vs_world"]["world_mae"]-A["self_vs_world"]["self_mae"],
      "external_bypass_decision_gap":A["families"]["decision"]["S2"]["accuracy"]-A["families"]["decision"]["H_EXTERNAL"]["accuracy"],
      "external_bypass_verification_gap":A["families"]["verification"]["S2"]["accuracy"]-A["families"]["verification"]["H_EXTERNAL"]["accuracy"]
    }
    return A

# ---------- frozen confirmatory scaffold ----------
def load_registry(root:Path):
    p=root/"configs"/"experiment_registry.json"
    return json.loads(p.read_text())

def execution_allowed(root:Path, experiment_id:str)->bool:
    reg=load_registry(root)
    return reg["experiments"][experiment_id]["status"]=="CLEARED_FOR_CONFIRMATORY_EXECUTION"

def verify_lock(root:Path, manifest_name:str):
    mp=root/"configs"/"manifests"/manifest_name
    lp=root/"configs"/"locks"/(manifest_name+".sha256")
    expected=lp.read_text().strip().split()[0]
    actual=hashlib.sha256(mp.read_bytes()).hexdigest()
    return expected==actual
