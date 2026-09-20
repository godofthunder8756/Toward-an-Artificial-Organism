"""AC101 replay: sampled exact reruns from the frozen source, in a fresh process, including the
per-tick observer-discard (G3) on gray_ctl and the corrupt=False arm identity (G4), which the audit
cannot re-derive because they require simulating."""
import json
from pathlib import Path
import ac101


def _norm(v):
    """Normalise JSON round-trip key types (AC15's replay lesson): int dict keys -> str, tuples ->
    lists."""
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


FIELDS = ('completed', 'first_dead', 'fw_at_corrupt', 'flipped_still_wrong', 'program_correct',
          'description_correct', 'description_correct_at_death', 'description_valid',
          'description_same', 'successions', 'ctrl_idle_end', 'routes', 'demand', 'register',
          'relinquishments', 'restorations', 'drop_ticks', 'streak_final', 'reacquire_ticks',
          'relinquishments_by_move', 'reacquisitions_by_move', 'births_by_window',
          'W', 'C', 'W_births', 'C_births', 'B_births', 'energy', 'material', 'fuel',
          'writes', 'reg_writes', 'succ_writes', 'ctrl_writes', 'streak_writes')


def main(root='ac101_results_v1', n=4):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    seeds = results['seeds']
    # sample one individual per seed across the strata (unseen + adversarial)
    seen = set()
    sample = []
    for r in rows:
        if r['seed'] not in seen:
            seen.add(r['seed'])
            sample.append(r)
        if len(sample) >= n:
            break
    ok = total = 0
    for r in sample:
        rr = ac101.run(r['seed'], r['history'], corrupt=True, schedule=ac101.SCHEDULE)
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(_norm(rr[k]) == _norm(r[k]) for k in FIELDS if k in rr and k in r)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if k in rr and k in r and _norm(rr[k]) != _norm(r[k])]
            print(f"MISMATCH seed={r['seed']} h={r['history']} hash_match={match} "
                  f"fields_match={fields} bad={bad[:8]}")

    # ---- G3 observer-discard: re-run one individual's per-tick discard (byte-identity) ----
    seed0 = seeds[0]
    d = ac101.observer_discard_equivalence(seed0, 0, True)
    obs_ok = 1 if (d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                   and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')) else 0

    # ---- G4 arm identity: re-run one individual's corrupt=False byte-identity ----
    ident_ok = 1 if ac101.arm_identity(seed0, 0) else 0

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/1 per-tick byte-identical; '
          f'arm-identity {ident_ok}/1 corrupt=False byte-identical to ac100 gray_ctl')
    return (ok == total) and obs_ok and ident_ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac101_results_v1') else 1)
