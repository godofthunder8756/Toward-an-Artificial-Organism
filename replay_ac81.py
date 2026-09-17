"""AC81 replay: sampled exact reruns from the frozen source, in a fresh process."""
import json
from pathlib import Path
import ac81


def main(root='ac81_results_v1', n=6):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    sample = [r for r in rows if r['history'] == 0][:n]
    ok = 0
    for r in sample:
        rr = ac81.run(r['seed'], r['history'], r['arm'], r['loss'])
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in ('completed', 'first_dead', 'W_birth', 'C_birth',
                                             'B_birth', 'C_birth_post', 'B_birth_post',
                                             'writes', 'converted', 'W_live', 'C_live',
                                             'B_live', 'routes', 'demand', 'description_correct',
                                             'description_same'))
        if match and fields:
            ok += 1
        else:
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} loss={r['loss']} "
                  f"hash_match={match} fields_match={fields}")
    print(f'replay: {ok}/{len(sample)} exact (state_hash and endpoint fields)')
    return ok == len(sample)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
