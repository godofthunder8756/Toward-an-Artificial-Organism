import json, time, urllib.request, urllib.error
d=json.load(open("s2_results.json"))
for qid,v in d.items():
    if v["status"]==200: continue
    for i in range(2):
        try:
            req=urllib.request.Request(v["url"],headers={"User-Agent":"CNA-prior-art-check (mailto:aidan@example.invalid)"})
            with urllib.request.urlopen(req,timeout=40) as r:
                v["data"]=json.loads(r.read()); v["status"]=200; v["attempts"].append("pass2:200"); break
        except urllib.error.HTTPError as e:
            v["attempts"].append(f"pass2:{e.code}")
        except Exception as e:
            v["attempts"].append("pass2:"+str(e)[:40])
        time.sleep(30)
    v["ts2"]=time.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(qid,v["status"],v["attempts"],(v["data"] or {}).get("total"),flush=True)
    time.sleep(10)
json.dump(d,open("s2_results_final.json","w"),indent=1)
