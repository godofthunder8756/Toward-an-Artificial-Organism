import ac117

# scramble_e in CUT: e=0 (hold, no drop); forcing e read to 1 -> drop, maintenance (erepair) unchanged
m = ac117.run(0, 0, 'monitor', 'cut', bel_damage=0.01)
se = ac117.run(0, 0, 'monitor', 'cut', scramble_e=True, bel_damage=0.01)
print('cut: monitor relinquish=%d erepair=%d bel_horizon=%d | scramble_e relinquish=%d erepair=%d bel_horizon=%d' % (
    m['relinquishments'], m['erepair_writes'], m['bel_at_horizon'],
    se['relinquishments'], se['erepair_writes'], se['bel_at_horizon']))
print('  -> scramble_e changes the decision (relinquish) while maintenance (erepair) is ~unchanged')
