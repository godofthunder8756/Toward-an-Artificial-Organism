"""AC94 replay: sampled exact reruns from the frozen source, in a fresh process."""
import json
from pathlib import Path
import ac94

FIELDS = ('completed', 'first_dead', 'first_W_empty', 'W_min_seen', 'timer_at_W_empty',
          'timer_at_rescue', 'W_at_rescue', 'timer_at_death', 'timer_increments_after_W_empty',
          'timer_end', 'timer_increments', 'timer_resets', 'split_events',
          'source_intact_at_switch_all', 'verified_all', 'removal_all', 'occupied_slots_end',
          'successions', 'pointer', 'ctrl_idle_end', 'ctrl_minority_end', 'description_correct',
          'description_correct_at_death', 'description_valid', 'description_same',
          'program_correct', 'flipped_still_wrong', 'W', 'C', 'energy', 'material', 'fuel',
          'W_births', 'region0_births', 'region1_births', 'W_births_bank0', 'C_births', 'B_births',
          'writes', 'reg_writes', 'succ_writes', 'ctrl_writes', 'routes', 'demand', 'register',
          'relinquishments', 'restorations')


def main(root='ac94_results_v1', n=7):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    # sample one individual per arm (history 0) across the distinct arms
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
    for r in sample:
        rr = ac94.run(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], transition)
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in FIELDS)
        if match and fields:
            ok += 1
        else:
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} d={r['damage']} "
                  f"c={r['corrupt']} hash_match={match} fields_match={fields}")
    print(f'replay: {ok}/{len(sample)} exact (state_hash and endpoint fields)')
    return ok == len(sample)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac94_results_v1') else 1)
