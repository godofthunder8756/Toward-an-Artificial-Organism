"""replay_ac114.py — sampled exact reruns of the frozen AC114 confirmation.

Re-runs a sample of the frozen rows from scratch via ac114.run and checks every
field (including state_hash) is identical to `ac114_results_v1/rows.jsonl`, after
normalising the tuple/list and int/str-key JSON round-trip (the AC15/AC79 lesson).
This is the replay half of the split verification (audit_ac114.py is the other
half). It is a determinism/integrity check on this host, NOT independent
confirmation.

Verification-tool: NOT in the frozen source hash set (AC16/AC17's rule).
"""
import json
import sys
from pathlib import Path

import ac114

ROOT = Path(__file__).parent
SAVED = [json.loads(l) for l in
         (ROOT / 'ac114_results_v1' / 'rows.jsonl').read_text().splitlines() if l.strip()]
TABLE = {(r['seed'], r['history'], r['arm']): r for r in SAVED}

# one condition per arm, the two ends, and the decisive D1 pair on extra seeds
SAMPLES = ([(6500, 0, arm) for arm in ac114.ARMS]
           + [(6507, 1, 'keep'), (6507, 1, 'B_rescue'),
              (6500, 1, 'no_B_retention'), (6500, 1, 'no_B_retention_ref'),
              (6501, 0, 'puncture'), (6501, 0, 'rival_puncture'),
              (6502, 1, 'puncture'), (6502, 1, 'rival_puncture'),
              (6503, 0, 'puncture_non_gate'), (6503, 0, 'permeant')])


def norm(x):
    return json.loads(json.dumps(x))


def main():
    exact = 0
    mismatches = []
    for seed, history, arm in SAMPLES:
        live = norm(ac114.run(seed, history, arm))
        ref = TABLE[(seed, history, arm)]
        diff = [k for k in ref if live.get(k) != ref[k]]
        if diff:
            mismatches.append((seed, history, arm, diff))
            continue
        assert live['state_hash'] == ref['state_hash'], (seed, history, arm)
        exact += 1
    ok = not mismatches
    print('replay ac114_results_v1 ->', 'PASS' if ok else 'FAIL',
          f'({exact}/{len(SAMPLES)} sampled conditions)')
    for m in mismatches[:30]:
        print('  MISMATCH:', m)
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
