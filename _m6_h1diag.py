import ac117, numpy as np

# H1 diagnostic: what are the ones values on the fixed_duty trajectory (cut)?
r = ac117.run(0, 0, 'fixed_duty', 'cut', duty_period=50, history_threshold=2)
series = r['h1_series']
# series: (t, ones, last_write, obs2, risk, wrong, contact)
ons = np.array([s[1] for s in series])
lw = np.array([s[2] for s in series])
ob2 = np.array([s[3] for s in series])
risk = np.array([s[4] for s in series])
wrong = np.array([s[5] for s in series])
contact = np.array([s[6] for s in series])

print('total ticks t>=8192:', len(series))
print('ones distribution:', {int(k): int(v) for k, v in zip(*np.unique(ons, return_counts=True))})
print('last_write=0 fraction:', float((lw == 0).mean()))
print('obs2 fires:', int(ob2.sum()), 'risk fires:', int(risk.sum()))
print('wrong ticks (decoded e != cause):', int(wrong.sum()))
print('contact1 ticks:', int(contact.sum()))

# case 3: ones>=4 (majority flipped), obs bit 2 silent
case3 = (ons >= 4) & (ob2 == 0) & (lw == 0)
case1 = (ons == 3) & (lw == 0)
case4 = (ons <= 3) & (risk.astype(bool)) & (lw == 0)
print('case1 (ones=3):', int(case1.sum()), 'case3 (ones>=4, obs2 silent):', int(case3.sum()),
      'case4 (risk, ones<=3):', int(case4.sum()))

# post-window only
pw = np.array([s[0] for s in series]) >= 8288
print('--- post-window [8288,16384) ---')
print('ones distribution:', {int(k): int(v) for k, v in zip(*np.unique(ons[pw], return_counts=True))})
print('wrong ticks:', int(wrong[pw].sum()), 'case3:', int(case3[pw].sum()), 'case4:', int(case4[pw].sum()))
print('obs2 fires:', int(ob2[pw].sum()))

# what is _cap typically when ones>=4? check the monitor arm's repair events
m = ac117.run(0, 0, 'monitor', 'cut', duty_period=50, history_threshold=2)
print('monitor repair_events:', m['repair_events'])
