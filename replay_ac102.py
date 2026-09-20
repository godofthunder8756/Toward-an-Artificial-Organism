"""AC102 replay: sampled exact reruns of the frozen rows, plus observer-discard and arm-identity.

Distinct from audit_ac102.py (which re-derives WITHOUT simulating). This file re-runs a sample
of the frozen individuals byte-for-byte (state_hash) to confirm the runner reproduces its own
freeze.
"""
import json
import sys
from pathlib import Path
import ac102


def main():
    root = Path('ac102_results_v1')
    rows = [json.loads(l) for l in (root / 'rows.jsonl').read_text().splitlines()]

    # 1. one exact rerun per arm, on the first seed (byte-identical state_hash)
    arm_ok = {}
    first = rows[0]
    seed, history = first['seed'], first['history']
    for arm in ac102.ARMS:
        r = ac102.run(seed, history, arm)
        frozen = next(x for x in rows if x['seed'] == seed and x['history'] == history
                      and x['arm'] == arm)
        arm_ok[arm] = r['state_hash'] == frozen['state_hash']

    # 2. one exact rerun of the failing death seed under `both` and `staged`
    death_seed = ac102.UNSEEN[0]
    d_both = ac102.run(death_seed, 0, 'both')
    d_both_frozen = next(x for x in rows if x['seed'] == death_seed and x['history'] == 0
                         and x['arm'] == 'both')
    d_staged = ac102.run(death_seed, 0, 'staged')
    d_staged_frozen = next(x for x in rows if x['seed'] == death_seed and x['history'] == 0
                           and x['arm'] == 'staged')

    # 3. observer-discard 1/1 (per-tick byte-identical)
    obs = ac102.observer_discard_equivalence(death_seed, 0)

    # 4. arm identity 1/1
    ident = ac102.arm_identity(death_seed, 0)
    ident['staged_nobudget_is_both'] = ac102.staged_nobudget_identity(death_seed, 0)

    print('exact reruns (state_hash):', json.dumps(arm_ok))
    print(f'death seed {death_seed} both rerun identical: '
          f'{d_both["state_hash"] == d_both_frozen["state_hash"]}, '
          f'first_dead {d_both["first_dead"]} (frozen {d_both_frozen["first_dead"]})')
    print(f'death seed {death_seed} staged rerun identical: '
          f'{d_staged["state_hash"] == d_staged_frozen["state_hash"]}, '
          f'first_dead {d_staged["first_dead"]} (frozen {d_staged_frozen["first_dead"]})')
    print('observer-discard:', obs.get('per_tick_identical'), obs.get('status'),
          'swap_tick', obs.get('swap_tick'))
    print('arm identity:', json.dumps(ident))

    ok = (all(arm_ok.values())
          and d_both['state_hash'] == d_both_frozen['state_hash']
          and d_staged['state_hash'] == d_staged_frozen['state_hash']
          and obs.get('per_tick_identical')
          and all(ident.values()))
    if not ok:
        sys.exit(1)
    print('\nAC102 replay passed: sampled exact reruns byte-identical, observer-discard 1/1, '
          'arm-identity 1/1.')


if __name__ == '__main__':
    main()
