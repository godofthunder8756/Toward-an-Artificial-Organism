"""AC16 replay: sampled exact reruns from scratch, compared field for field.

`audit_ac16.py` only inspects the saved table; this re-simulates.
"""
import json
from pathlib import Path
import ac16

SAMPLE=(('allocate_restore',2100,0),('allocate_restore',2103,1),('allocate',2101,0),
        ('preserve',2100,1),('relinquish',2102,1),('restore_disabled',2101,1),
        ('streak_never',2103,0))
SKIP=set()
# JSON round-trips integer keys to strings; normalise before comparing so a genuine
# mismatch cannot hide behind a field excused as a serialization artifact.
DICT_FIELDS=('chan_late','chan_productivity','actions')


def normalise(row):
    out=dict(row)
    for f in DICT_FIELDS:
        v=out.get(f)
        if isinstance(v,dict): out[f]={int(k):val for k,val in v.items()}
    return out


def main():
    rows=json.loads(Path('ac16_results_v1/results.json').read_text())['rows']
    index={(r['arm'],r['seed'],r['history']):r for r in rows}
    ok=0
    for arm,seed,hist in SAMPLE:
        rec=normalise(index[(arm,seed,hist)])
        again=normalise(ac16.run(seed,hist,arm))
        diffs=[k for k in rec if k not in SKIP and rec[k]!=again.get(k)]
        if diffs:
            print(f"MISMATCH {arm} seed{seed} h{hist}: {diffs}")
            for k in diffs[:4]: print(f"   {k}: recorded {rec[k]} replays {again.get(k)}")
        else:
            ok+=1
            print(f"exact {arm:18} seed{seed} h{hist} hash {rec['state_hash'][:16]} "
                  f"moved {rec['productivity_moved']} reacq {rec['reacquired_at']}")
    print(f"REPLAY {ok}/{len(SAMPLE)} exact")


if __name__=='__main__': main()
