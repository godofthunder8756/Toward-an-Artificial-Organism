"""AC15 replay: sampled exact reruns from scratch, compared field for field.

Unlike `audit_ac15.py`, which only inspects the saved table, this re-simulates and
compares every recorded field of the sampled rows.
"""
import json
from pathlib import Path
import ac15

SAMPLE=(('allocate',1900,0),('allocate',1903,1),('preserve',1901,0),
        ('relinquish',1902,1),('fixed_period_1',1900,1),('streak_never',1902,0))
SKIP=set()   # every recorded field must match; nothing is excused
# JSON round-trips int keys to strings, so dict-valued fields must be normalised
# before comparison. The values are identical; only the key type differs. Comparing
# raw `!=` here would report a false mismatch on every run.
DICT_FIELDS=('chan_late','chan_productivity','actions')


def normalise(row):
    out=dict(row)
    for f in DICT_FIELDS:
        v=out.get(f)
        if isinstance(v,dict):
            out[f]={int(k):val for k,val in v.items()}
    return out


def main():
    rows=json.loads(Path('ac15_results_v1/results.json').read_text())['rows']
    index={(r['arm'],r['seed'],r['history']):r for r in rows}
    ok=0
    for arm,seed,hist in SAMPLE:
        rec=normalise(index[(arm,seed,hist)])
        again=normalise(ac15.run(seed,hist,arm))
        diffs=[k for k in rec if k not in SKIP and rec[k]!=again.get(k)]
        if diffs:
            print(f"MISMATCH {arm} seed{seed} h{hist}: {diffs}")
            for k in diffs[:4]: print(f"   {k}: recorded {rec[k]} replays {again.get(k)}")
        else:
            ok+=1
            print(f"exact {arm:16} seed{seed} h{hist} hash {rec['state_hash'][:16]}")
    print(f"REPLAY {ok}/{len(SAMPLE)} exact")


if __name__=='__main__': main()
