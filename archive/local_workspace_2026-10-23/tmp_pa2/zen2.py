import json,urllib.request,urllib.parse,time
qs=[
 '"homeostatic reinforcement learning"',
 'homeostatic AND agent AND "reinforcement learning"',
 'allostatic AND agent',
 'interoceptive AND agent AND (learning OR "neural network")',
 'interoception AND "artificial agent"',
 '"global workspace" AND agent',
 '"global workspace" AND (ablation OR lesion)',
 '"self-model" AND (ablation OR lesion OR necessity) AND agent',
 '"attention schema"',
 '"self-model" AND (preregistration OR preregistered OR "pre-registered")',
 '(homeostatic OR homeostasis OR interoceptive) AND (preregistration OR preregistered OR "pre-registered") AND agent',
 '"known-answer" AND (instrument OR assay) AND (neural OR agent)',
]
out=[]
for q in qs:
    u='https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':q,'size':25,'sort':'bestmatch'})
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research-readonly'}),timeout=40))
        tot=d['hits']['total']; hits=[(h['id'],h['metadata'].get('title'),h['metadata'].get('publication_date'),h['metadata'].get('resource_type',{}).get('title'),[c.get('name') for c in h['metadata'].get('creators',[])][:2]) for h in d['hits']['hits']]
    except Exception as e:
        tot='ERR '+str(e); hits=[]
    out.append({'q':q,'url':u,'total':tot,'top25':hits})
    print('###',q,'| total',tot)
    for h in hits: print('   ',h)
    time.sleep(1.5)
json.dump(out,open('zenodo_results2.json','w'),indent=1)
