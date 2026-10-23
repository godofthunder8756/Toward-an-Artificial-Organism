import json, time, urllib.parse, urllib.request, urllib.error, sys
from queries import Q
ep = sys.argv[1]
out = {}
def get(url, tries, waits):
    log=[]
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"CNA-prior-art-check (mailto:aidan@example.invalid)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                log.append(200); return 200, json.loads(r.read()), log
        except urllib.error.HTTPError as e:
            log.append(e.code)
            if e.code != 429 and e.code < 500: return e.code, None, log
        except Exception as e:
            log.append(str(e)[:60])
        if i < tries-1: time.sleep(waits[i])
    return log[-1], None, log
for qid, q in Q:
    if ep == "oa":
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search":q,"filter":"from_publication_date:2015-01-01","per-page":25,"mailto":"aidan@example.invalid"})
        code, js, log = get(url, 4, [5,15,40])
    else:
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({"query":q,"limit":25,"year":"2015-","fields":"title,authors,year,venue,externalIds,url,publicationDate"})
        code, js, log = get(url, 6, [5,10,20,40,60])
    out[qid] = {"q":q,"url":url,"status":code,"attempts":log,"ts":time.strftime("%Y-%m-%d %H:%M:%S %Z"),"data":js}
    print(qid, code, log, (js or {}).get("meta",{}).get("count") if ep=="oa" else (js or {}).get("total"), flush=True)
    time.sleep(3 if ep=="s2" else 1.5)
json.dump(out, open(f"{ep}_results.json","w"), indent=1)
