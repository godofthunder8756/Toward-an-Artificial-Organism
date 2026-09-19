"""AC95 replay: sampled exact reruns from the frozen source, in a fresh process, including the
observer-discard equivalence runs (which the audit cannot re-derive because they require
simulating)."""
import json
from pathlib import Path
import ac95

FIELDS = ('completed', 'first_dead', 'first_W_empty', 'W_min_seen', 'timer_at_W_empty',
          'timer_at_rescue', 'W_at_rescue', 'timer_at_death', 'timer_increments_after_W_empty',
          'timer_end', 'timer_increments', 'timer_resets', 'split_events',
          'source_intact_at_switch_all', 'verified_all', 'removal_all', 'occupied_slots_end',
          'successions', 'pointer', 'ctrl_idle_end', 'ctrl_minority_end', 'description_correct',
          'description_correct_at_death', 'description_valid', 'description_same',
          'program_correct', 'flipped_still_wrong', 'W', 'C', 'energy', 'material', 'fuel',
          'W_births', 'region0_births', 'region1_births', 'W_births_bank0', 'C_births', 'B_births',
          'writes', 'reg_writes', 'succ_writes', 'ctrl_writes', 'routes', 'demand', 'register',
          'relinquishments', 'restorations', 'reset_start', 'reset_progress_at_cut',
          'reset_completed_tick', 'reset_froze', 'reset_restore_done')


def main(root='ac95_results_v1', n=9):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    # sample one individual per arm (history 0) across the 8 distinct arms
    seen = set()
    sample = []
    for r in rows:
        key = r['arm']
        if key not in seen and r['history'] == 0:
            seen.add(key)
            sample.append(r)
        if len(sample) >= n:
            break
    ok = 0
    total = 0
    for r in sample:
        rr = ac95.run(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], transition)
        total += 1
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in FIELDS)
        if match and fields:
            ok += 1
        else:
            bad = [k for k in FIELDS if rr[k] != r[k]]
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} d={r['damage']} "
                  f"c={r['corrupt']} hash_match={match} fields_match={fields} bad={bad[:6]}")

    # ---- observer-discard equivalence: re-run the two discard points for one individual ----
    obs_ok = 0
    obs_n = 0
    seed0, hist0 = results['seeds'][0], 0
    gated_base = [r for r in rows if r['seed'] == seed0 and r['history'] == hist0
                  and r['arm'] == 'gated' and r['damage'] is True and r['corrupt'] is True][0]
    rr_base = [r for r in rows if r['seed'] == seed0 and r['history'] == hist0
               and r['arm'] == 'reset_rescue'][0]
    gated_swap = ac95.run(seed0, hist0, 'gated', True, True, 'none', swap_succ_at='mid_succession')
    rr_swap = ac95.run(seed0, hist0, 'reset_rescue', True, False, 'none', swap_succ_at='rescue')
    obs_n += 2
    obs_ok += (gated_swap['state_hash'] == gated_base['state_hash'])
    obs_ok += (rr_swap['state_hash'] == rr_base['state_hash'])

    print(f'replay: {ok}/{total} exact (state_hash and endpoint fields); '
          f'observer-discard {obs_ok}/{obs_n} byte-identical')
    return (ok == total) and (obs_ok == obs_n)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac95_results_v1') else 1)
