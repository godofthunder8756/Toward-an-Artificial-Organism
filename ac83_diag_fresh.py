import sys
import ac83

seeds = [int(x) for x in sys.argv[1:]] or list(range(8, 16))
ticks = ac83.DESIGNS['corrupt_then_move']
print(f"internalized, corrupt_then_move (corrupt={ticks['corrupt_tick']}, move={ticks['move_tick']}), perm+corrupt")
rs = []
for seed in seeds:
    for history in (0, 1):
        r = ac83.run(seed, history, 'internalized', 'perm', True, ticks['corrupt_tick'], ticks['move_tick'])
        rs.append(r)
        hold = ac83._holds_both(r)
        print(f"s{seed}h{history}: done={int(r['completed'])} dead={r['first_dead']} fw={r['flipped_still_wrong']} "
              f"desc={r['description_correct']}/78 routes={r['routes']} r1c={int(r['route1_correct'])} "
              f"demand={r['demand']} hold={int(hold)} W={r['W']} C={r['C']}")
surv = sum(r['completed'] for r in rs)
uncond = sum(r['flipped_still_wrong'] == 0 and r['description_correct'] == 78 and ac83._holds_both(r) for r in rs)
print(f"\nsurvive {surv}/{len(rs)}  unconditional(surv+rec+both) {uncond}/{len(rs)}")
