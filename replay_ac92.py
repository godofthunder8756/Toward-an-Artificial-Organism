"""AC92 replay: sampled exact reruns from the frozen source, in a fresh process."""
import json
from pathlib import Path
import ac92


def main(root='ac92_results_v1', n=6):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    transition = results['transition']
    sample = [r for r in rows if r['history'] == 0][:n]
    ok = 0
    for r in sample:
        rr = ac92.run(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'],
                      transition, move_tick=ac92.MOVE_TICK)
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in
                     ('completed', 'first_dead', 'first_W_empty', 'W_min_seen',
                      'alive_at_corruption', 'fw_at_corruption', 'alive_pre_rescue',
                      'fw_pre_rescue', 'W_pre_rescue', 'pointer_at_corruption',
                      'pointer_pre_rescue', 'window_reg_writes', 'window_succ_writes',
                      'window_ctrl_writes', 'rescue_applied', 'successions', 'pointer',
                      'ctrl_idle_end', 'ctrl_minority_end', 'description_correct',
                      'description_correct_intervention', 'description_correct_at_death',
                      'description_valid', 'program_correct', 'flipped_still_wrong', 'W', 'C',
                      'energy', 'material', 'fuel', 'W_births', 'region0_births',
                      'region1_births', 'W_births_bank0', 'C_births', 'B_births', 'writes',
                      'reg_writes', 'succ_writes', 'ctrl_writes', 'routes', 'demand'))
        if match and fields:
            ok += 1
        else:
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} d={r['damage']} "
                  f"c={r['corrupt']} hash_match={match} fields_match={fields}")
    print(f'replay: {ok}/{len(sample)} exact (state_hash and endpoint fields)')
    return ok == len(sample)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac92_results_v1') else 1)
