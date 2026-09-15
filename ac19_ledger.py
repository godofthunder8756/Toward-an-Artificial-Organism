"""AC19-M2: naming the route -- compare the live and register-cut ledgers.

AC19-M showed the cut arms die with the corruption switched off, so the route is structural to the cut
rather than caused by damage. This compares what each arm actually DOES: its ledger, its demand, and its
repair/relinquish bookkeeping, on the same seeds.
"""
import json
import numpy as np
import ac19

SEEDS=(0,1,2,3)
LIVE='two_way'
CUT='two_way_no_repair'


def collect(arm):
    ledger_keys=None; totals={}; demands=[]; relinq=0; restor=0; completed=0
    for seed in SEEDS:
        r=ac19.run(seed,0,arm)
        completed+=int(bool(r['completed']))
        led=r['ledger']
        ledger_keys=ledger_keys or sorted(led.keys())
        for k,v in led.items(): totals[k]=totals.get(k,0)+v
        demands.append(r['demand'])
        relinq+=int(r.get('register_bits_relinquished_count',0))
        restor+=int(r.get('restorations',0) or 0)
    return dict(completed=completed,ledger=totals,demand=demands,relinquished=relinq,
                restorations=restor, keys=ledger_keys)


if __name__=='__main__':
    live=collect(LIVE); cut=collect(CUT)
    print(f'alive: {LIVE} {live["completed"]}/{len(SEEDS)}   {CUT} {cut["completed"]}/{len(SEEDS)}')
    print(f'\n{"ledger entry":22s} {"live":>10s} {"cut":>10s}')
    for k in live['keys']:
        a=live['ledger'].get(k,0); b=cut['ledger'].get(k,0)
        if a or b:
            print(f'{k:22s} {a:>10d} {b:>10d}')
    print(f'\nrelinquished bits: live {live["relinquished"]}  cut {cut["relinquished"]}')
    print(f'restorations:      live {live["restorations"]}  cut {cut["restorations"]}')
    print(f'\ndemand at the end:')
    for name,data in (('live',live),('cut',cut)):
        print(f'  {name}: {data["demand"]}')
    big=sorted(((abs(live["ledger"].get(k,0)-cut["ledger"].get(k,0)),k) for k in live['keys']),
               reverse=True)[:5]
    print('\nlargest differences:',[(k,live['ledger'].get(k,0),cut['ledger'].get(k,0))
                                    for _,k in big])
    json.dump(dict(live=live,cut=cut),open('/tmp/ac19_ledger.json','w'),indent=2,default=str)
