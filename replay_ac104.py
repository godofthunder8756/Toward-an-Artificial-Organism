"""AC104 replay: sampled exact reruns of the frozen study (byte-identical state_hash).

Re-runs (1) the first row, (2) the control identity (persistent == AC103 persistent) on a sampled
individual, (3) the observer-discard on the candidate (per-tick byte-identical) for a sample
individual, and (4) the budget-rescued marginal seed (5603) + the closest-to-marginal final seed
(5702). Compares each against the frozen results. Verification tools are NOT hashed into the
snapshot (AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac104

ROOT = Path('ac104_results_v1')


def main():
    res = json.loads((ROOT / 'results.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['arm']), r)

    # 1. first row exact rerun
    first = rows[0]
    rerun = ac104.run(first['seed'], first['history'], first['arm'])
    assert rerun['state_hash'] == first['state_hash'], 'first row rerun mismatch'
    print('first-row rerun: byte-identical')

    # 2. control identity on a sampled individual
    seed, h = 5702, 0
    got = ac104.arm_identity(seed, h)
    want = res['arm_identity'][f'{seed}/{h}']
    assert got['persistent_is_ac103'] and want['persistent_is_ac103'], \
        f'{seed}/{h} control identity mismatch'
    print(f'control identity ({seed}/{h}): byte-identical to AC103 persistent')

    # 3. observer-discard per-tick byte-identical on a sample individual (the candidate)
    od = ac104.observer_discard_equivalence(5702, 0, 'persistent_budget')
    assert od['per_tick_identical'] and od['swap_applied'], 'observer-discard not per-tick identical'
    print('observer-discard (5702/0, candidate): per-tick byte-identical')

    # 4. the budget-rescued marginal seed (diagnostic) + the closest-to-marginal final seed
    for (s, h, a) in ((5603, 0, 'persistent_budget'), (5702, 0, 'persistent'),
                      (5702, 0, 'persistent_budget')):
        rr = ac104.run(s, h, a)
        frozen = by.get((s, h, a))
        if frozen is not None:
            assert rr['state_hash'] == frozen['state_hash'], f'{s}/{h}/{a} rerun mismatch'
            assert rr['flipped_still_wrong'] == frozen['flipped_still_wrong']
    # 5603 is diagnostic (not in the frozen rows), so check its recorded property directly
    rr5603 = ac104.run(5603, 0, 'persistent_budget')
    assert rr5603['completed'] and rr5603['relinquishments'] == 2, '5603 budget did not rescue'
    print('marginal + closest-to-marginal arms: byte-identical / rescue confirmed')

    print('AC104 replay passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
