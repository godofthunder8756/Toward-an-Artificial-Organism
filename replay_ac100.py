"""AC100 replay: sampled exact reruns from the frozen source, in a fresh process, including the
per-tick observer-discard (G4) run on gray_res (which the audit cannot re-derive because it
requires simulating) and the single-move arm identity (G6)."""
import json
from pathlib import Path
import ac100


def _norm(v):
    """Normalise JSON round-trip key types (AC15's replay lesson): int dict keys -> str, and
    tuples -> lists (json.dump/load turns tuples into arrays)."""
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


FIELDS = ('completed', 'first_dead', 'routes', 'demand', 'register', 'relinquishments',
          'restorations', 'drop_ticks', 'streak_final', 'reacquire_ticks',
          'relinquishments_by_move', 'reacquisitions_by_move', 'births_by_window',
          'reserve_armed_end', 'reserve_minority_end', 'reserve_arm_ticks',
          'reserve_release_ticks', 'reserve_release_kinds', 'reserve_m', 'reserve_released_m',
          'reserve_writes', 'W', 'C', 'W_births', 'C_births', 'B_births', 'energy', 'material',
          'fuel', 'writes', 'reg_writes', 'succ_writes', 'ctrl_writes', 'streak_writes')


def main(root='ac100_results_v1', n=8):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    seeds = results['seeds']
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
        rr = ac100.run(r['seed'], r['history'], r['condition'], schedule=ac100.SCHEDULE)
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(_norm(rr[k]) == _norm(r[k]) for k in FIELDS if k in rr and k in r)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if k in rr and k in r and _norm(rr[k]) != _norm(r[k])]
            print(f"MISMATCH seed={r['seed']} h={r['history']} cond={r['condition']} "
                  f"hash_match={match} fields_match={fields} bad={bad[:8]}")

    # ---- G4 observer-discard: re-run one individual's per-tick discard (byte-identity) ----
    seed0 = seeds[0]
    d = ac100.observer_discard_equivalence(seed0, 0, ac100.SCHEDULE)
    obs_ok = 1 if (d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                   and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')) else 0

    # ---- G6 arm identity: re-run one individual's single-move byte-identity for each arm ----
    ctrl_ok = 0
    import ac99, ac99_d2
    refs = {
        'bin_res': ac99.run(seed0, 0, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
        'gray_res': ac99_d2.run(seed0, 0, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
        'bin_ctl': ac99.run(seed0, 0, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
        'gray_ctl': ac99_d2.run(seed0, 0, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
    }
    ctrl_ok = sum(1 for code in ac100.ARMS
                  if ac100.run(seed0, 0, code, schedule=ac100.SINGLE_MOVE)['state_hash'] == refs[code]['state_hash'])

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/1 per-tick byte-identical; '
          f'arm-identity {ctrl_ok}/{len(ac100.ARMS)} single-move byte-identical to AC99 runner')
    return (ok == total) and obs_ok and (ctrl_ok == len(ac100.ARMS))


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac100_results_v1') else 1)
