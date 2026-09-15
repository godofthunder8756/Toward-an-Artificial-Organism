import json, statistics, ac15, ac12
ac15.TICKS=2048; ac15.MOVE=1024
IND=[(s,h) for s in ac15.FINALS for h in (0,1)]
out={}
def run(label, arm, **kw):
    for k,v in ac15.DEFAULTS.items(): setattr(ac12,k,v)
    for k,v in kw.items(): setattr(ac12,k,v)
    rs=[ac15.run(s,h,arm) for s,h in IND]
    v=statistics.mean(r['mean_chan_productivity'] for r in rs)
    out[label]=dict(arm=arm,kw=kw,n=len(rs),mean=v,
                    alive=sum(r['completed'] for r in rs),
                    per=sorted(round(r['mean_chan_productivity'],4) for r in rs))
    print(f"{label:26} mean {v:.4f} alive {out[label]['alive']}/{len(rs)}",flush=True)
for p in (1,2,3,4,8): run(f"fixed_period_{p}",'fixed_schedule',FIXED_PERIOD=p)
for p in (0.25,0.5,0.75): run(f"random_p{p}",'random',RANDOM_P=p)
for n in (2,4,6,8): run(f"allocate_streak_{n}",'allocate',STREAK_N=n)
json.dump(out,open('ac15_results_v1/g2_rival_sweep.json','w'),indent=2)
print("WROTE ac15_results_v1/g2_rival_sweep.json")
