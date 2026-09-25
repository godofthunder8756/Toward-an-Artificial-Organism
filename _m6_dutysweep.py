import ac117

# spend-match sweep: fixed_duty vs monitor at bd=0.01
seed = 0
mon = ac117.run(seed, 0, 'monitor', 'cut', duty_period=50, history_threshold=2, bel_damage=0.01)
print(f'monitor: erepair={mon["erepair_writes"]} wrong_ever={mon["bel_wrong_ever"]} bel_horizon={mon["bel_at_horizon"]}')
print('fixed_duty sweep (duty_period -> erepair, wrong_ever, bel_horizon):')
for K in (1, 2, 3, 4, 5, 8, 12, 20, 30, 40, 50):
    r = ac117.run(seed, 0, 'fixed_duty', 'cut', duty_period=K, history_threshold=2, bel_damage=0.01)
    print(f'  K={K:2d}: erepair={r["erepair_writes"]:4d} wrong_ever={r["bel_wrong_ever"]:5d} '
          f'bel_horizon={r["bel_at_horizon"]}')
