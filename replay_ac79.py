"""AC79 replay: sampled exact reruns from the frozen source, in a fresh process."""
import json
from pathlib import Path
import ac79


def main(root='ac79_results_v1', n=6):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    sample = [r for r in rows if r['history'] == 0][:n]
    ok = 0
    for r in sample:
        rr = ac79.run(r['seed'], r['history'], r['arm'], r['corrupt'])
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in ('completed', 'first_dead', 'program_correct',
                                             'flipped_still_wrong', 'description_correct',
                                             'description_valid', 'description_same',
                                             'demand', 'register'))
        if match and fields:
            ok += 1
        else:
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} corrupt={r['corrupt']} "
                  f"hash_match={match} fields_match={fields}")
    print(f'replay: {ok}/{len(sample)} exact (state_hash and endpoint fields)')
    return ok == len(sample)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
