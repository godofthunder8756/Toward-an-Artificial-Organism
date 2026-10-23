import re,html,urllib.parse,urllib.request,time,json
terms=["reinforcement learning","artificial agent","homeosta","allosta","interocept","global workspace","self-model","neural network","artificial intelligence","consciousness"]
out=[]
for t in terms:
    q=f'v_article.title contains "{t}" or v_article.abstract contains "{t}"'
    u='https://rr.peercommunityin.org/?keywords='+urllib.parse.quote(q)
    s=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research-readonly'}),timeout=40).read().decode('utf8','replace')
    txt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s)))
    hits=re.findall(r'(\d{1,2} \w{3} \d{4}) (STAGE [12]) (.{0,160}?) (?=[A-Z][a-z]+ [A-Z])',txt)
    ids=sorted(set(re.findall(r'/articles/rec\?id=(\d+)',s)))
    m=re.search(r'(\d+) records? found',txt)
    out.append({'term':t,'url':u,'n_rec_ids':len(ids),'records_found':m.group(1) if m else None,'stage_items':[h[1]+' | '+h[2] for h in hits]})
    print('###',t,'| rec ids',len(ids),'| stage items',len(hits),'| found',m.group(1) if m else None)
    for h in hits: print('    ',h[0],h[1],h[2][:150])
    time.sleep(1)
json.dump(out,open('pcirr_results.json','w'),indent=1)
