"""AC105 replay: sampled exact reruns of the frozen study (byte-identical state_hash).

Re-runs (1) the first row, (2) the baseline identity (persistent / persistent_budget == AC104) on
a sampled individual, (3) the observer-discard on the candidate (per-tick byte-identical) for a
sample individual, and (4) the diagnostic rescue (5603 simult) and a sampled final individual
across a couple of conditions. Compares each against the frozen results. Verification tools are
NOT hashed into the snapshot (AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac105

ROOT = Path('ac105_results_v1')


def main():
    res = json.loads((ROOT / 'results.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition'], r['arm']), r)

    # 1. first row exact rerun
    first = rows[0]
    rerun = ac105.run(first['seed'], first['history'], first['arm'], first['condition'])
    assert rerun['state_hash'] == first['state_hash'], 'first row rerun mismatch'
    print('first-row rerun: byte-identical')

    # 2. baseline identity on a sampled individual (both arms == AC104 at `simult`)
    seed, h = res['seeds'][0], 0
    got = ac105.arm_identity(seed, h)
    want = res['arm_identity'][f'{seed}/{h}']
    assert got['persistent_is_ac104'] and got['budget_is_ac104'], f'{seed}/{h} baseline identity'
    assert want['persistent_is_ac104'] and want['budget_is_ac104'], f'{seed}/{h} recorded identity'
    print(f'baseline identity ({seed}/{h}): byte-identical to AC104 (both arms)')

    # 3. observer-discard per-tick byte-identical on a sample individual (the candidate)
    od = ac105.observer_discard_equivalence(seed, h, 'persistent_budget')
    assert od['per_tick_identical'] and od['swap_applied'], 'observer-discard not per-tick identical'
    print(f'observer-discard ({seed}/{h}, candidate): per-tick byte-identical')

    # 4. sampled final individuals across conditions, byte-identical
    for (s, h, cond, arm) in [(res['seeds'][0], 0, 'simult', 'persistent_budget'),
                              (res['seeds'][0], 0, 'simult3', 'persistent_budget'),
                              (res['seeds'][0], 0, 'late', 'persistent'),
                              (res['seeds'][0], 0, 'corrupt_first', 'persistent_budget')]:
        rr = ac105.run(s, h, arm, cond)
        frozen = by.get((s, h, cond, arm))
        assert frozen is not None, f'missing frozen row {s}/{h}/{cond}/{arm}'
        assert rr['state_hash'] == frozen['state_hash'], f'{s}/{h}/{cond}/{arm} rerun mismatch'
    print('sampled finals: byte-identical across conditions')

    # 5. the diagnostic rescue (5603 simult) confirmed
    for (s, h, cond) in ((5603, 0, 'simult'), (5603, 0, 'simult3'), (5603, 0, 'late')):
        ctl = ac105.run(s, h, 'persistent', cond)
        cand = ac105.run(s, h, 'persistent_budget', cond)
        if cond in ('simult', 'simult3'):
            assert (not ctl['completed']) and cand['completed'], f'{s}/{h}/{cond} rescue'
            assert cand['relinquishments'] == len(ac105.CONDITIONS[cond][1]), 'relinq count'
        else:
            # late: both die; the candidate's reconstruction harm is the recorded finding
            assert (not ctl['completed']) and (not cand['completed']), f'{s}/{h}/{cond} both die'
    print('diagnostic rescue (5603) confirmed; late boundary (both die) confirmed')

    print('AC105 replay passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
