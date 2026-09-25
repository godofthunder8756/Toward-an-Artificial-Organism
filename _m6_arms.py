import ac117, json

# compare all 5 arms on cut, seed 0/0
for arm in ac117.ARMS:
    r = ac117.run(0, 0, arm, 'cut', duty_period=50, history_threshold=2)
    print(f"{arm:12s} bel_at_horizon={r['bel_at_horizon']} bel_wrong_ever={r['bel_wrong_ever']:5d} "
          f"erepair={r['erepair_writes']:4d} m_writes={r['m_writes']:2d} reg={r['reg_writes']:5d} "
          f"retention={r['route1_retention']:.3f} income={r['income_post']} routes={r['routes']}")

print()
# check a few more seeds for the monitor vs reflex bel_wrong_ever contrast
for seed in (1, 2, 3, 4):
    m = ac117.run(seed, 0, 'monitor', 'cut', duty_period=50, history_threshold=2)
    x = ac117.run(seed, 0, 'reflex', 'cut', duty_period=50, history_threshold=2)
    print(f"seed={seed}: monitor wrong_ever={m['bel_wrong_ever']} erepair={m['erepair_writes']} | "
          f"reflex wrong_ever={x['bel_wrong_ever']} erepair={x['erepair_writes']}")
