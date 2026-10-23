import json,glob,sys
for p in sys.argv[1:]:
    d=json.load(open(p)); print("=====",p,d.get("total"))
    for k,r in enumerate(d.get("data",[]),1):
        au=", ".join(a["name"] for a in (r.get("authors") or [])[:3]); x=r.get("externalIds") or {}
        print(f"{k:2d} {r.get('year')} | {(r.get('title') or '')[:110]} | {au} | {r.get('venue','')[:40]} | {x.get('DOI') or ('arXiv:'+x['ArXiv'] if x.get('ArXiv') else r['paperId'])}")
