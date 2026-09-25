import ac117, numpy as np

# 1. scramble_m: monitor readout forced reliable -> no targeted repair, e drifts (like reflex)
m0 = ac117.run(0, 0, 'monitor', 'cut', bel_damage=0.01)
sm = ac117.run(0, 0, 'monitor', 'cut', scramble_m=True, bel_damage=0.01)
x0 = ac117.run(0, 0, 'reflex', 'cut', bel_damage=0.01)
print('scramble_m: monitor erepair=%d wrong=%d | scrambled erepair=%d wrong=%d | reflex wrong=%d' % (
    m0['erepair_writes'], m0['bel_wrong_ever'], sm['erepair_writes'], sm['bel_wrong_ever'], x0['bel_wrong_ever']))

# 2. scramble_e: decision read forced 1 -> decision changes, maintenance (erepair) unchanged
se = ac117.run(0, 0, 'monitor', 'move', scramble_e=True, bel_damage=0.01)
m0m = ac117.run(0, 0, 'monitor', 'move', bel_damage=0.01)
print('scramble_e (move): monitor relinquish=%d erepair=%d | scrambled relinquish=%d erepair=%d' % (
    m0m['relinquishments'], m0m['erepair_writes'], se['relinquishments'], se['erepair_writes']))

# 3. move decoupling (P-G4): under move, m reads reliable throughout, reflex/direct read unreliable
def readout_series(r, kind):
    # recompute readouts from the fixed_duty move trajectory
    s = r['h1_series']
    ones = np.array([x[1] for x in s]); lw = np.array([x[2] for x in s])
    ob2 = np.array([x[3] for x in s]); risk = np.array([x[4] for x in s])
    mon = (lw == 0) & ((ones >= 4) | risk.astype(bool))
    ref = ob2.astype(bool)
    direct = (ones >= 4)
    return mon.mean(), ref.mean(), direct.mean()
f = ac117.run(0, 0, 'fixed_duty', 'move', bel_damage=0.01)
mon_r, ref_r, dir_r = readout_series(f, 'x')
print('move fixed_duty trajectory: monitor unreliable fraction=%.3f reflex=%.3f direct=%.3f' % (mon_r, ref_r, dir_r))

# 4. clean control at bd=0.01
for c in ('no_cause', 'move'):
    hs = [ac117.run(0, 0, arm, c, bel_damage=0.01)['state_hash'] for arm in ac117.ARMS]
    print('clean control %s (bd=0.01): all-identical=%s' % (c, len(set(hs)) == 1))
