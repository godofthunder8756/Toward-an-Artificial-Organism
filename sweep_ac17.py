"""AC17 engineering sweep: blind rival families and the learner's own family.

Engineering seeds 0-1 x 2 histories. Written to ac17_engineering_sweep.json, which
audit_ac17.py reads to extend G7 beyond the table's own arms ("no swept duty/period
configuration reaches 0.90"). Engineering seeds are excluded from the final sample.

Note on per-config constants: ac12's constant defaults are applied by ac17.run before any
arm-specific override, so setting a sweep value immediately before each run takes effect.
AC16's first sweep got this wrong and every configuration silently ran the default.
"""
import json
import statistics
import ac17, ac12, ac15

IND=[(s,h) for s in (0,1) for h in (0,1)]
out={}


def batch(label, arm, **kw):
    rs=[]
    for s,h in IND:
        for k,v in kw.items(): setattr(ac12,k,v)
        rs.append(ac17.run(s,h,arm))
    moved=[r['productivity_moved'] for r in rs if r['productivity_moved'] is not None]
    out[label]=dict(arm=arm,kw=kw,n=len(rs),alive=sum(r['completed'] for r in rs),
                    moved_mean=(statistics.mean(moved) if moved else None),
                    kept_mean=statistics.mean(r['productivity_kept'] or 0 for r in rs),
                    reacquired=[r['reacquired_at'] for r in rs])
    o=out[label]
    print(f"{label:26} alive {o['alive']}/{o['n']} kept {o['kept_mean']:.3f} "
          f"moved {('%.3f'%o['moved_mean']) if o['moved_mean'] is not None else 'None'} "
          f"reacq {o['reacquired'][:3]}",flush=True)


if __name__=='__main__':
    for p in (1,2,4,8): batch(f"fixed_period_{p}",'fixed_schedule',FIXED_PERIOD=p)
    for p in (0.25,0.5,0.75): batch(f"random_p{p}",'random',RANDOM_P=p)
    for n in (2,4,6,8): batch(f"learner_streak_{n}",'allocate_restore',STREAK_N=n)
    out['_note']=("Engineering seeds 0,1 x 2 histories; excluded from the AC17 final sample. "
                  "Read by audit_ac17.py to extend G7: no swept blind configuration may reach 0.90. "
                  "The learner's own family is swept here for disclosure only; the final learner "
                  "configuration is prespecified at STREAK_N=6, not chosen from this sweep.")
    json.dump(out,open('ac17_engineering_sweep.json','w'),indent=2)
    print('WROTE ac17_engineering_sweep.json')
