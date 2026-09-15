"""Sampled exact reruns of the frozen AC10 table, without retraining or tuning.

Each selected condition is recomputed from scratch and compared field-by-field
against `ac10_results_v1/results.json`, including the state digest. This is a
determinism/integrity check on this host; it is not independent confirmation.
"""
from pathlib import Path
import json
import ac10

ROOT=Path(__file__).parent
SAVED=json.loads((ROOT/'ac10_results_v1'/'results.json').read_text())['rows']

# one condition per arm, plus both histories on the two ends of the sample
SAMPLES=[(1300,0,arm) for arm in ac10.ARMS]+[(1303,1,'keep'),(1300,1,'no_B_retention')]


def norm(x): return json.loads(json.dumps(x))


def main():
    table={(r['seed'],r['history'],r['arm']):r for r in SAVED}
    exact=0
    for seed,history,arm in SAMPLES:
        live=norm(ac10.run(seed,history,arm))
        ref=table[(seed,history,arm)]
        diff=[k for k in ref if live.get(k)!=ref[k]]
        assert not diff,f'seed{seed} history{history} {arm}: differing fields {diff}'
        assert live['state_hash']==ref['state_hash']
        exact+=1
    assert exact==len(SAMPLES)
    print(f'AC10 replay passed: {exact}/{len(SAMPLES)} sampled conditions reproduce '
          f'exactly, including state digests')


if __name__=='__main__': main()
