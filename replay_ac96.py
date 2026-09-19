"""AC96 replay: sampled exact reruns from the frozen source, in a fresh process, including the
observer-discard (G1) and interruption (G4) runs (which the audit cannot re-derive because they
require simulating)."""
import json
from pathlib import Path
import ac96


def _norm(v):
    """Normalise JSON round-trip key types (AC15's replay lesson): int dict keys -> str."""
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_norm(x) for x in v]
    return v


FIELDS = ('completed', 'first_dead', 'routes', 'demand', 'register', 'relinquishments',
          'restorations', 'streak_writes', 'streak_final', 'first_streak_write_tick',
          'reacquire_ticks', 'first_W_empty', 'streak_minority_end', 'W', 'C', 'energy',
          'material', 'fuel', 'writes', 'reg_writes', 'succ_writes', 'ctrl_writes')


def main(root='ac96_results_v1', n=12):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    # sample one individual per condition across the four seeds (history 0 and 1)
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
        rr = ac96.run(r['seed'], r['history'], 'gated', r['damage'], r['corrupt'], transition,
                      streak_maintained=r['streak_maintained'])
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(_norm(rr[k]) == _norm(r[k]) for k in FIELDS)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if _norm(rr[k]) != _norm(r[k])]
            print(f"MISMATCH seed={r['seed']} h={r['history']} cond={r['condition']} "
                  f"hash_match={match} fields_match={fields} bad={bad[:6]}")

    # ---- G1 observer-discard: re-run one individual's discard (byte-identity) ----
    seed0 = results['seeds'][0]
    d = ac96.observer_discard_equivalence(seed0, 0)
    obs_ok = 1 if (d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                   and d.get('identical')) else 0

    # ---- G4 interruption: re-run one individual's cut + rescue ----
    i = ac96.interruption_equivalence(seed0, 0)
    int_ok = 1 if (i.get('status') != 'no_mid_streak'
                   and i['cut']['streak_writes_after_cut'] == 0
                   and i['cut']['relinquishments'] == 0
                   and i['rescue']['completed']
                   and i['rescue']['streak_at_rescue'] == i['streak_at_cut']) else 0

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/1 byte-identical; interruption {int_ok}/1 W-gated+rescue')
    return (ok == total) and obs_ok and int_ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac96_results_v1') else 1)
