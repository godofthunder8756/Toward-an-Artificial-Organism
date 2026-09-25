"""replay_ac115.py — sampled exact reruns of the frozen AC115 (I4) confirmation.

Re-runs a sample of the frozen rows from scratch via ac115.run and checks every
field (including state_hash) is identical to `ac115_results_v1/rows.jsonl`, after
normalising the tuple/list and int/str-key JSON round-trip (the AC15/AC79 lesson).
This is the replay half of the split verification (audit_ac115.py is the other
half). It is a determinism/integrity check on this host, NOT independent
confirmation.

Verification-tool: NOT in the frozen source hash set (AC16/AC17's rule).
"""
import json
import sys
from pathlib import Path

import ac115

ROOT = Path(__file__).parent
SAVED = [json.loads(l) for l in
         (ROOT / 'ac115_results_v1' / 'rows.jsonl').read_text().splitlines() if l.strip()]
TABLE = {(r['seed'], r['history'], r['arm']): r for r in SAVED}

# one condition per arm, the two ends, and the decisive D1/composition pairs on
# extra seeds — plus the failing individuals (G4/G5/G6 on 6602, G6 on 6606,
# G7 on 6601/6605) so the recorded failures are confirmed deterministic.
SAMPLES = ([(6600, 0, arm) for arm in ac115.ARMS]
           + [(6607, 1, 'keep'), (6607, 1, 'B_rescue'),
              (6601, 0, 'puncture'), (6601, 0, 'rival_puncture'),
              (6602, 1, 'puncture_simult'), (6602, 1, 'rival_puncture_simult'),
              (6603, 0, 'no_B_retention'), (6603, 0, 'no_B_retention_ref'),
              (6602, 0, 'no_B_retention_ref'), (6602, 0, 'B_rescue'),
              (6601, 0, 'rival_puncture_simult'), (6605, 1, 'rival_puncture_simult'),
              (6606, 0, 'keep')])


def norm(x):
    return json.loads(json.dumps(x))


def main():
    exact = 0
    mismatches = []
    for seed, history, arm in SAMPLES:
        live = norm(ac115.run(seed, history, arm))
        ref = TABLE[(seed, history, arm)]
        diff = [k for k in ref if live.get(k) != ref[k]]
        extra = [k for k in live if k not in ref]
        if diff or extra:
            mismatches.append((seed, history, arm, diff, extra))
            continue
        assert live['state_hash'] == ref['state_hash'], (seed, history, arm)
        exact += 1
    ok = not mismatches
    print('replay ac115_results_v1 ->', 'PASS' if ok else 'FAIL',
          f'({exact}/{len(SAMPLES)} sampled conditions)')
    for m in mismatches[:30]:
        print('  MISMATCH:', m)
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
