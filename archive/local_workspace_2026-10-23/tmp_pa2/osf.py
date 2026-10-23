import json,urllib.request,urllib.parse,time,sys
UA={'User-Agent':'Mozilla/5.0 research-readonly'}
def get(u):
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except Exception as e:
            err=str(e); time.sleep(3)
    return {'_err':err}
trove=["homeostatic reinforcement learning","allostatic agent","interoceptive agent","interoception artificial agent","homeostatic agent","global workspace agent","global workspace reinforcement learning","global workspace artificial","self-model artificial agent","self-model ablation","causal necessity internal state artificial agent","ablation deep reinforcement learning","reinforcement learning ablation","deep reinforcement learning","artificial consciousness indicators","consciousness artificial intelligence","machine consciousness","introspection language model","privileged access self-prediction","active inference agent simulation"]
out=[]
for q in trove:
    u="https://share.osf.io/trove/index-card-search?"+urllib.parse.urlencode({'cardSearchText':q,'cardSearchFilter[resourceType]':'Registration','page[size]':'25','acceptMediatype':'application/json'})
    d=get(u); time.sleep(1)
    if '_err' in d: out.append(('TROVE',q,'ERR '+d['_err'],[])); continue
    hits=[]
    for c in d.get('data',[]):
        t=(c.get('title') or [{}])[0].get('@value','')
        dc=(c.get('dateCreated') or [{}])[0].get('@value','')
        hits.append((c.get('@id'),dc,t))
    out.append(('TROVE',q,d.get('meta',{}).get('total'),hits))
api=[("title","homeostatic"),("title","homeostasis"),("title","allostatic"),("title","allostasis"),("title","interocept"),("title","global workspace"),("title","reinforcement learning"),("title","self-model"),("title","artificial agent"),("title","consciousness in AI"),("title","machine consciousness"),("title","artificial consciousness"),("description","reinforcement learning agent"),("description","global workspace"),("description","homeostatic"),("description","interoceptive"),("description","allostatic")]
for f,q in api:
    u=f"https://api.osf.io/v2/registrations/?filter%5B{f}%5D%5Bicontains%5D={urllib.parse.quote(q)}&page%5Bsize%5D=100"
    d=get(u); time.sleep(1)
    if '_err' in d: out.append(('API',f+':'+q,'ERR '+d['_err'],[])); continue
    tot=d.get('links',{}).get('meta',{}).get('total') or d.get('meta',{}).get('total')
    hits=[('https://osf.io/'+x['id'],(x['attributes'].get('date_registered') or '')[:10],x['attributes']['title']) for x in d['data']]
    out.append(('API',f+':'+q,tot,hits))
json.dump(out,open('osf_results.json','w'),indent=1)
for s,q,t,h in out:
    print(f"## [{s}] {q!r} total={t} returned={len(h)}")
    for x in h: print("   ",x[1],x[0],x[2][:140])
