import ac117, numpy as np, time

# sweep bel_damage: measure case-3 base rate (fixed_duty trajectory) and monitor vs reflex wrongness
def h1_cases(r):
    s = r['h1_series']
    ons = np.array([x[1] for x in s]); lw = np.array([x[2] for x in s])
    ob2 = np.array([x[3] for x in s]); risk = np.array([x[4] for x in s])
    wrong = np.array([x[5] for x in s])
    pw = np.array([x[0] for x in s]) >= 8288
    case1 = int(((ons == 3) & (lw == 0))[pw].sum())
    case3 = int(((ons >= 4) & (ob2 == 0) & (lw == 0))[pw].sum())
    case4 = int(((ons <= 3) & (risk.astype(bool)) & (lw == 0))[pw].sum())
    wrong_pw = int(wrong[pw].sum())
    return case1, case3, case4, wrong_pw

for bd in (0.0, 0.003, 0.01, 0.03):
    t0 = time.monotonic()
    rows = {'monitor': [], 'reflex': [], 'fixed_duty': []}
    for seed in (0, 1, 2, 3):
        m = ac117.run(seed, 0, 'monitor', 'cut', duty_period=50, history_threshold=2, bel_damage=bd)
        x = ac117.run(seed, 0, 'reflex', 'cut', duty_period=50, history_threshold=2, bel_damage=bd)
        f = ac117.run(seed, 0, 'fixed_duty', 'cut', duty_period=50, history_threshold=2, bel_damage=bd)
        rows['monitor'].append(m); rows['reflex'].append(x); rows['fixed_duty'].append(f)
    mw = [r['bel_wrong_ever'] for r in rows['monitor']]
    xw = [r['bel_wrong_ever'] for r in rows['reflex']]
    cases = [h1_cases(r) for r in rows['fixed_duty']]
    print(f'bd={bd:.3f}: monitor wrong_ever={mw} | reflex wrong_ever={xw}')
    print(f'   fixed_duty case1/3/4/wrong_postwindow per seed: {cases}')
    print(f'   monitor erepair={[r["erepair_writes"] for r in rows["monitor"]]}  (%.1fs)' % (time.monotonic()-t0))
