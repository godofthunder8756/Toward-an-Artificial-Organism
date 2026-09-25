import ac117

# focused: all 5 arms at bd=0.01, cut, seeds 0-3
for seed in (0, 1, 2, 3):
    print(f'seed={seed}:')
    for arm in ac117.ARMS:
        r = ac117.run(seed, 0, arm, 'cut', duty_period=50, history_threshold=2, bel_damage=0.01)
        print(f'  {arm:11s} wrong_ever={r["bel_wrong_ever"]:5d} bel_horizon={r["bel_at_horizon"]} '
              f'erepair={r["erepair_writes"]:4d} m_writes={r["m_writes"]} routes={r["routes"]} '
              f'retention={r["route1_retention"]:.3f} income={r["income_post"]}')
