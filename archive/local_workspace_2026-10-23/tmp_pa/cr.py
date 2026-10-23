import json,sys,urllib.request,urllib.parse,concurrent.futures as cf
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
def f(q):
    u="https://api.crossref.org/works?rows=3&mailto=research@example.com&select=DOI,title,author,container-title,issued,type&query.bibliographic="+urllib.parse.quote(q)
    import time; time.sleep(2)
    try: d=json.load(urllib.request.urlopen(u,timeout=60))
    except Exception as e: return q,[str(e)]
    out=[]
    for w in d["message"]["items"]:
        au=", ".join((a.get("family") or "") for a in w.get("author",[])[:6])
        out.append(f'{w.get("issued",{}).get("date-parts",[[None]])[0][0]} | {(w.get("title") or [""])[0]} | {au} | {(w.get("container-title") or [""])[0]} | https://doi.org/{w["DOI"]} | {w.get("type")}')
    return q,out
with cf.ThreadPoolExecutor(1) as ex:
    for q,o in ex.map(f,qs):
        print("##",q); [print("  ",x) for x in o]
