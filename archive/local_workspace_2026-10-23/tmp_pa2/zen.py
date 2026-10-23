import json,urllib.request,urllib.parse,time,sys
qs=[
 'homeostatic reinforcement learning agent',
 'allostatic agent reinforcement learning',
 'interoceptive reinforcement learning agent',
 '"interoceptive" "self-model" agent',
 'global workspace agent reinforcement learning',
 'global workspace ablation neural network',
 'self-model ablation agent',
 'self-model necessity artificial agent',
 '"attention schema" agent',
 'preregistration artificial agent self-model',
 'homeostatic agent preregistration',
 'privileged access self-prediction agent observer',
]
out=[]
for q in qs:
    u='https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':q,'size':25,'sort':'bestmatch'})
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research-readonly'}),timeout=40))
        tot=d['hits']['total']; hits=[(h['id'],h['metadata'].get('title'),h['metadata'].get('publication_date'),h['metadata'].get('resource_type',{}).get('title'),[c.get('name') for c in h['metadata'].get('creators',[])][:3]) for h in d['hits']['hits']]
    except Exception as e:
        tot='ERR '+str(e); hits=[]
    out.append({'q':q,'url':u,'total':tot,'top25':hits})
    print('###',q,'| total',tot)
    for h in hits: print('   ',h)
    time.sleep(1.5)
json.dump(out,open('zenodo_results.json','w'),indent=1)
