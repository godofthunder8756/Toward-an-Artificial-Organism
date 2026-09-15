"""Regenerated AC16 engineering sweep, after the DEFAULTS-ordering fix.

The first sweep ran every config through ac16.run, which (before the fix) reset the
defaults *after* the per-config kwargs, so all fixed_period_* and random_p* entries were
actually the default configuration. The runner's defaults are no longer overridden, but
this script still sets the per-config value *after* the run-level defaults so the config
takes effect.
"""
import json, statistics, ac16, ac12, ac15
ac16.TICKS=4096; ac16.MOVE=1024
IND=[(s,h) for s in (0,1,2) for h in (0,1)]
out={}
def batch(label, arm, **kw):
    # arm kwargs are applied inside ac16.run for ARM_CONFIG arms; for direct arm+kw
    # sweeps we must pass them through ac12 AND have run() not clobber them, which the
    # fixed run() now guarantees by applying DEFAULTS first.
    rs=[]
    for s,h in IND:
        for k,v in kw.items(): setattr(ac12,k,v)
        rs.append(ac16.run(s,h,arm))
    mv=[r['productivity_moved'] for r in rs if r['productivity_moved'] is not None]
    out[label]=dict(arm=arm,kw=kw,n=len(rs),alive=sum(r['completed'] for r in rs),
                    moved_mean=(statistics.mean(mv) if mv else None),
                    kept_mean=statistics.mean(r['productivity_kept'] or 0 for r in rs),
                    reacq=[r['reacquired_at'] for r in rs],
                    relinq=statistics.mean(r['relinquishments'] for r in rs),
                    restore=statistics.mean(r['restorations'] for r in rs))
    o=out[label]
    print(f"{label:28} alive {o['alive']}/{o['n']} kept {o['kept_mean']:.3f} "
          f"moved {('%.3f'%o['moved_mean']) if o['moved_mean'] is not None else 'None'} "
          f"reacq {o['reacq'][:3]} relinq {o['relinq']:.1f} restore {o['restore']:.1f}",flush=True)
for arm in ac16.ARMS: batch(arm, arm)
for p in (1,2,4,8): batch(f"fixed_period_{p}",'fixed_schedule',FIXED_PERIOD=p)
for p in (0.25,0.5,0.75): batch(f"random_p{p}",'random',RANDOM_P=p)
for n in (2,4,6,8): batch(f"two-way streak {n}",'allocate_restore',STREAK_N=n)
# The disable-the-restore control is the `restore_disabled` ARM, not RESTORE=False on
# the allocate_restore arm: run() forces RESTORE=True for that arm, so setting the flag
# outside produces a mislabelled row. The arm carries the control.
json.dump(out,open('ac16_engineering_sweep.json','w'),indent=2)
print("WROTE ac16_engineering_sweep.json (regenerated after the ordering fix)")
