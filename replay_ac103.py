"""AC103 replay: sampled exact reruns of the frozen study (byte-identical state_hash).

Re-runs (1) the first row, (2) the arm-identity checks (current == AC102 both,
current_staged == AC102 staged) on a sampled individual, (3) the observer-discard on `current`
(per-tick byte-identical) for a sample individual, and (4) the marginal death seed's arms. Compares
each against the frozen results. Verification tools are NOT hashed into the snapshot (AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac103

ROOT = Path('ac103_results_v1')


def main():
    res = json.loads((ROOT / 'results.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['arm']), r)

    # 1. first row exact rerun
    first = rows[0]
    rerun = ac103.run(first['seed'], first['history'], first['arm'])
    assert rerun['state_hash'] == first['state_hash'], 'first row rerun mismatch'
    print('first-row rerun: byte-identical')

    # 2. arm-identity on a sampled individual (the marginal/death seed 5603)
    seed, h = 5603, 0
    got = ac103.arm_identity(seed, h)
    want = res['arm_identity'][f'{seed}/{h}']
    for k in ('current_is_ac102_both', 'current_staged_is_ac102_staged'):
        assert got[k] == want[k] and want[k], f'{seed}/{h} {k} mismatch'
    print(f'arm-identity ({seed}/{h}): byte-identical to the frozen references')

    # 3. observer-discard per-tick byte-identical on a sample individual
    od = ac103.observer_discard_equivalence(5601, 0, 'current')
    assert od['per_tick_identical'] and od['swap_applied'], 'observer-discard not per-tick identical'
    print('observer-discard (5601/0): per-tick byte-identical')

    # 4. the marginal death seed's arms + the starvation seed, exact rerun
    for (s, h, a) in ((5603, 0, 'current'), (5603, 0, 'persistent_defer'),
                      (5607, 0, 'persistent_staged')):
        rr = ac103.run(s, h, a)
        assert rr['state_hash'] == by[(s, h, a)]['state_hash'], f'{s}/{h}/{a} rerun mismatch'
        assert rr['flipped_still_wrong'] == by[(s, h, a)]['flipped_still_wrong']
    print('marginal + starvation arms: byte-identical')

    print('AC103 replay passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
