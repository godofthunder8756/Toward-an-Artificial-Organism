"""AC98 replay: sampled exact reruns from the frozen source, in a fresh process, including the
per-tick observer-discard (G3) run (which the audit cannot re-derive because it requires simulating)."""
import json
from pathlib import Path
import ac98
import ac97


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


def main(root='ac98_results_v1', n=8):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    # sample one individual per condition across the seeds (history 0 and 1)
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
        rr = ac98.run(r['seed'], r['history'], 'gated', reserve=r['reserve'], damage=r['damage'],
                      corrupt=r['corrupt'], transition=transition)
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(_norm(rr[k]) == _norm(r[k]) for k in FIELDS)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if _norm(rr[k]) != _norm(r[k])]
            print(f"MISMATCH seed={r['seed']} h={r['history']} cond={r['condition']} "
                  f"hash_match={match} fields_match={fields} bad={bad[:8]}")

    # ---- G3 observer-discard: re-run one individual's per-tick discard (byte-identity) ----
    seed0 = results['seeds'][0]
    d = ac98.observer_discard_equivalence(seed0, 0)
    obs_ok = 1 if (d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                   and d.get('per_tick_identical')) else 0

    # ---- G5 control equivalence: re-run one individual's no-reserve == ac97 comparison ----
    a = ac98.run(seed0, 0, 'gated', reserve=False, damage=True, corrupt=False, transition=transition)
    b = ac97.run(seed0, 0, 'gated', reserve=False, damage=True, corrupt=False, transition=transition)
    ctrl_ok = 1 if a['state_hash'] == b['state_hash'] else 0

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/1 per-tick byte-identical; '
          f'control-equivalence {ctrl_ok}/1 byte-identical to ac97 no-reserve')
    return (ok == total) and obs_ok and ctrl_ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac98_results_v1') else 1)
