import json,sys,urllib.request,urllib.parse,concurrent.futures as cf
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
def f(q):
    u="https://api.openalex.org/works?per-page=3&mailto=x@example.com&search="+urllib.parse.quote(q)
    try:
        d=json.load(urllib.request.urlopen(u,timeout=40))
    except Exception as e: return q,[str(e)]
    out=[]
    for w in d.get("results",[]):
        au=", ".join(a["author"]["display_name"] for a in w.get("authorships",[])[:6])
        src=((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        out.append(f'{w.get("publication_year")} | {w.get("title")} | {au} | {src} | {w.get("doi") or w.get("id")}')
    return q,out
with cf.ThreadPoolExecutor(6) as ex:
    for q,o in ex.map(f,qs):
        print("##",q); [print("  ",x) for x in o]
