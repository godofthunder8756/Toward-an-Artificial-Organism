"""AC17 replay: sampled exact reruns from scratch, compared field for field."""
import json
from pathlib import Path
import ac17

SAMPLE=(('allocate_restore',2300,0),('allocate_restore',2303,1),('allocate',2301,0),
        ('preserve',2300,1),('restore_only',2302,0),('restore_disabled',2301,1),
        ('streak_never',2303,0),('relinquish',2302,1))
SKIP=set()
DICT_FIELDS=('chan_late','chan_productivity','actions')


def normalise(row):
    out=dict(row)
    for f in DICT_FIELDS:
        v=out.get(f)
        if isinstance(v,dict): out[f]={int(k):val for k,val in v.items()}
    return out


def main():
    rows=json.loads(Path('ac17_results_single_v1/results.json').read_text())['rows']
    index={(r['arm'],r['seed'],r['history']):r for r in rows}
    ok=0
    for arm,seed,hist in SAMPLE:
        rec=normalise(index[(arm,seed,hist)])
        again=normalise(ac17.run(seed,hist,arm))
        diffs=[k for k in rec if k not in SKIP and rec[k]!=again.get(k)]
        if diffs:
            print(f"MISMATCH {arm} seed{seed} h{hist}: {diffs}")
            for k in diffs[:4]: print(f"   {k}: recorded {rec[k]} replays {again.get(k)}")
        else:
            ok+=1
            print(f"exact {arm:17} seed{seed} h{hist} hash {rec['state_hash'][:16]} "
                  f"moved {rec['productivity_moved']} reacq {rec['reacquired_at']}")
    print(f"REPLAY {ok}/{len(SAMPLE)} exact")


if __name__=='__main__': main()
