"""AC99 replay: sampled exact reruns from the frozen source, in a fresh process, including the
per-tick observer-discard (G3) run on the Gray arm (which the audit cannot re-derive because it
requires simulating)."""
import json
from pathlib import Path
import ac99_d4
import ac99_d3


def _norm(v):
    """Normalise JSON round-trip key types (AC15's replay lesson): int dict keys -> str, and
    tuples -> lists (json.dump/load turns tuples into arrays)."""
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


FIELDS = ('completed', 'first_dead', 'routes', 'demand', 'register', 'relinquishments',
          'restorations', 'drop_ticks', 'streak_final', 'reacquire_ticks', 'reserve_armed_end',
          'reserve_minority_end', 'reserve_arm_ticks', 'reserve_release_ticks',
          'reserve_release_kinds', 'reserve_m', 'reserve_released_m', 'reserve_writes',
          'W', 'C', 'W_births', 'C_births', 'B_births', 'W_births_post_move',
          'C_births_post_move', 'B_births_post_move', 'energy', 'material', 'fuel',
          'writes', 'reg_writes', 'succ_writes', 'ctrl_writes', 'streak_writes')


def main(root='ac99_results_v1', n=8):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    # sample one individual per arm condition across the seeds
    seen = set()
    sample = []
    for r in rows:
        key = r['condition']
        if key not in seen:
            seen.add(key)
            sample.append(r)
        if len(sample) >= n:
            break
    ok = total = 0
    for r in sample:
        rr = ac99_d4.run(r['seed'], r['history'], r['condition'], transition=transition,
                         damage=True, corrupt=False)
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(_norm(rr[k]) == _norm(r[k]) for k in FIELDS if k in rr and k in r)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if k in rr and k in r and _norm(rr[k]) != _norm(r[k])]
            print(f"MISMATCH seed={r['seed']} h={r['history']} cond={r['condition']} "
                  f"hash_match={match} fields_match={fields} bad={bad[:8]}")

    # ---- G3 observer-discard: re-run one individual's per-tick discard (byte-identity) ----
    seed0 = results['seeds'][0]
    d = ac99_d4.observer_discard_equivalence_gray(seed0, 0)
    obs_ok = 1 if (d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                   and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')) else 0

    # ---- G5 arm identity: re-run one individual's wb_first no-swap == binary comparison ----
    a = ac99_d4.run(seed0, 0, 'binary', transition=transition, damage=True, corrupt=False)
    b_no_swap = ac99_d3.run(seed0, 0, 'gated', reserve=True, damage=True,
                            corrupt=False, transition=transition, wb_first=False)
    ctrl_ok = 1 if b_no_swap['state_hash'] == a['state_hash'] else 0

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/1 per-tick byte-identical; '
          f'arm-identity {ctrl_ok}/1 wb_first no-swap byte-identical to binary')
    return (ok == total) and obs_ok and ctrl_ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac99_results_v1') else 1)
