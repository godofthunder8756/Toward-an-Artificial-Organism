import urllib.request, urllib.parse, urllib.error, time, datetime, json, os, re, sys
OUT="/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md"
RAW="/workspace/tmp_p3b/raw"
Q={14:"allostatic reinforcement learning agent",15:"interoceptive reinforcement learning agent",
17:"body model lesion necessity reinforcement learning agent",18:"global workspace agent reinforcement learning",
19:"ignition global workspace artificial neural network",20:"global broadcast workspace deep learning model",
21:"introspection self-prediction privileged access internal states",22:"agent predicts own internal state better than external observer",
24:"random subspace control causal intervention neural network representation"}
UA="CNA-prior-art-check/1.0 (mailto:aidan@example.invalid)"
def now(): return datetime.datetime.now().strftime("%H:%M:%S")
def app(s):
    with open(OUT,"a") as f: f.write(s); f.flush()
def get(url, fn, pace):
    atts=[]; body=None; delays=[5,10,20,40]
    for i in range(5):
        t=now(); st=None
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":UA}),timeout=30)
            st=r.status; body=r.read()
        except urllib.error.HTTPError as e:
            st=e.code; body=e.read()
        except Exception as e:
            st="ERR:"+type(e).__name__; body=None
        atts.append(f"{t} {st}")
        if st==200: break
        if body is not None: open(f"{RAW}/{fn}.err{i}","wb").write(body)
        if i<4 and (st in (429,500,502,503,504) or str(st).startswith("ERR")): time.sleep(delays[i]+pace)
        else: break
    if st==200: open(f"{RAW}/{fn}","wb").write(body)
    time.sleep(pace)
    return st,body,atts
if not os.path.exists(OUT): sys.exit("MISSING")
app("| — | arXiv API (http://) | `allostatic reinforcement learning agent` | from 12:29:08: connection timeouts (60 s each, no HTTP status); attempt loop stopped by operator at "+now()+" | ABANDONED, route switched to https://export.arxiv.org | — | — |\n")
summ={}
for n,q in Q.items():
    if n!=14:
      url="https://api.crossref.org/works?"+urllib.parse.urlencode({"query":q,"rows":25,"mailto":"aidan@example.invalid"})
      st,b,a=get(url,f"crossref_{n}.json",2)
      tot=ret="—"; res="OK" if st==200 else ("NOT SEARCHABLE (RATE-LIMITED)" if st==429 else f"FAILED ({st})")
      if st==200:
        d=json.loads(b); tot=d["message"]["total-results"]; ret=len(d["message"]["items"])
      summ[("cr",n)]=res
      app(f"| {n} | Crossref | `{q}` | {'; '.join(a)} | {res} | {tot} | {ret} |\n")
    url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":"all:"+q,"max_results":25})
    st,b,a=get(url,f"arxiv_{n}.xml",3.5)
    tot=ret="—"; res="OK" if st==200 else ("NOT SEARCHABLE (RATE-LIMITED)" if st==429 else f"FAILED ({st})")
    if st==200:
        s=b.decode("utf8","replace"); m=re.search(r"<opensearch:totalResults[^>]*>(\d+)<",s); tot=m.group(1) if m else "?"; ret=s.count("<entry>")
    summ[("ax",n)]=res
    app(f"| {n} | arXiv API | `{q}` | {'; '.join(a)} | {res} | {tot} | {ret} |\n")
# Google Scholar single attempt
q=Q[14]; t=now()
try:
    r=urllib.request.urlopen(urllib.request.Request("https://scholar.google.com/scholar?"+urllib.parse.urlencode({"q":q}),headers={"User-Agent":UA}),timeout=30)
    st=r.status; b=r.read()
except urllib.error.HTTPError as e: st=e.code; b=e.read()
except Exception as e: st="ERR:"+type(e).__name__; b=b""
open(f"{RAW}/gscholar_14.html","wb").write(b or b"")
s=(b or b"").decode("utf8","replace").lower()
flag=[k for k in ("captcha","unusual traffic","sorry/index","not a robot","gs_captcha") if k in s]
nres=s.count('class="gs_ri"')
app(f"| 14 | Google Scholar (single plain-HTTP attempt) | `{q}` | {t} {st} | {'BLOCKED ('+', '.join(flag)+')' if flag or st!=200 else 'OK ('+str(nres)+' result blocks)'} | — | {nres} |\n")
app(f"\nRun ended {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET.\n")
json.dump({f"{k[0]}_{k[1]}":v for k,v in summ.items()}|{"gs":[str(st),flag,nres]},open("/workspace/tmp_p3b/summary.json","w"))
