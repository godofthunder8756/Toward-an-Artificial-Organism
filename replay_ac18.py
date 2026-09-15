"""AC18 replay: sampled exact reruns from scratch, compared field for field."""
import json
from pathlib import Path
import ac18

SAMPLE=(('allocate_restore',2500,0),('allocate_restore',2503,1),('allocate',2501,0),
        ('preserve',2500,1),('restore_only',2502,0),('restore_disabled',2501,1),
        ('streak_never',2503,0),('relinquish',2502,1))
SKIP=set()


def main():
    rows=json.loads(Path('ac18_results_v1/results.json').read_text())['rows']
    index={(r['arm'],r['seed'],r['history']):r for r in rows}
    ok=0
    for arm,seed,hist in SAMPLE:
        rec=index[(arm,seed,hist)]
        again=ac18.run(seed,hist,arm)
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
