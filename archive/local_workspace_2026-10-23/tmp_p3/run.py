import json, os, time, urllib.request, urllib.parse, urllib.error, datetime, sys
from zoneinfo import ZoneInfo
ET=ZoneInfo("America/New_York")
OUT="/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md"
RAW="/workspace/tmp_p3/raw"; os.makedirs(RAW,exist_ok=True)
def now(): return datetime.datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S ET")
Q=["homeostatic reinforcement learning deep agent",
"allostatic reinforcement learning agent",
"interoceptive reinforcement learning agent",
"self-model ablation reinforcement learning agent",
"body model lesion necessity reinforcement learning agent",
"global workspace agent reinforcement learning",
"ignition global workspace artificial neural network",
"global broadcast workspace deep learning model",
"introspection self-prediction privileged access internal states",
"agent predicts own internal state better than external observer",
"known-answer validation interpretability method preregistered",
"random subspace control causal intervention neural network representation"]
def url(ep,q):
    if ep=="openalex":
        return "https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":25,"mailto":"aidan@example.invalid"})
    return "https://api.semanticscholar.org/graph/v1/paper/search?"+urllib.parse.urlencode({"query":q,"limit":25,"fields":"title,authors,year,venue,externalIds"})
fd=os.open(OUT,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)  # refuse if exists
f=os.fdopen(fd,"w")
def w(s): f.write(s+"\n"); f.flush(); os.fsync(f.fileno())
w("CNA, 2026-10-23, additive note; planning only; authorizes nothing\n")
w("# Track B prior-art verification v1.4: P3 scholarly-index rerun (OpenAlex, Semantic Scholar) (CNA)\n")
w("- **Amends nothing.** Additive. Repeats the OpenAlex and Semantic Scholar lookups that returned HTTP 429 in v1 (`trackB_prior_art_verification_v1_CNA.md` §0). No existing file was edited. No labels are changed here.")
w("- **Nothing ran** except read-only HTTP GETs to api.openalex.org and api.semanticscholar.org. Raw JSON responses saved under `/workspace/tmp_p3/raw/`.")
w(f"- **Run started** {now()}. Pacing ≥3.5 s between requests; on HTTP 429/5xx, exponential backoff 5/10/20/40 s, at most 4 retries. 12 queries per endpoint; top 25 screened by title (and abstract/landing page where marked).")
w("- **This file is written incrementally**; the query log (Part 1) is appended as each request completes.\n")
w("## Part 1. Query log\n")
w("| # | Endpoint | Query | Attempts (ET, HTTP status) | Result | Total hits |")
w("|---|---|---|---|---|---|")
summary={}
n=0
for ep in ["openalex","s2"]:
    ok=0; rl=0
    for i,q in enumerate(Q,1):
        n+=1
        att=[]; data=None; delay=5
        for a in range(5):
            time.sleep(3.5)
            ts=now()
            try:
                req=urllib.request.Request(url(ep,q),headers={"User-Agent":"CNA-readonly-lit-check (mailto:aidan@example.invalid)"})
                with urllib.request.urlopen(req,timeout=30) as r:
                    body=r.read(); att.append(f"{ts[11:19]} {r.status}"); data=json.loads(body); break
            except urllib.error.HTTPError as e:
                att.append(f"{ts[11:19]} {e.code}")
                if e.code in (429,500,502,503,504) and a<4: time.sleep(delay); delay*=2; continue
                break
            except Exception as e:
                att.append(f"{ts[11:19]} ERR {type(e).__name__}")
                if a<4: time.sleep(delay); delay*=2; continue
                break
        if data is not None:
            ok+=1
            json.dump(data,open(f"{RAW}/{ep}_{i:02d}.json","w"))
            tot=data["meta"]["count"] if ep=="openalex" else data.get("total")
            res="OK"
        else:
            rl+= any(" 429" in x for x in att); tot="—"
            res="NOT SEARCHABLE (RATE-LIMITED)" if att and att[-1].endswith("429") else "FAILED"
        epname="OpenAlex" if ep=="openalex" else "Semantic Scholar"
        w(f"| {n} | {epname} | `{q}` | {'; '.join(att)} | {res} | {tot} |")
        print(ep,i,att,res,tot,flush=True)
    summary[ep]=(ok,rl)
w(f"\nRun ended {now()}. Per endpoint (queries OK / queries ending rate-limited): " + "; ".join(f"{'OpenAlex' if k=='openalex' else 'Semantic Scholar'} {v[0]}/12 OK, {v[1]} rate-limited" for k,v in summary.items())+"\n")
f.close()
