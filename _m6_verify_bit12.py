import numpy as np
import ac12, ac96, ac106
from ac1 import decode

# verify the dead rule's word bits and that word bit 12 (action bit 2) is a free '1' bit
for seed in (0, 1, 2, 3, 6200, 6800):
    o, offs = ac12.acquire(seed)
    idx = ac12.dead_rule_index(o)
    base = 14 * idx
    word = decode(o.body.traces[0, base:base+14]).reshape(14)
    bel_off = ac106.bel_offset(o)  # 14*idx + 10
    streak = ac96.streak_offsets(o)
    reg = [base+1+k for k in range(4)]
    print(f'seed={seed} dead_idx={idx} base={base}')
    print(f'  word bits 0..13: {word.tolist()}')
    print(f'  bel_off={bel_off} (word bit {bel_off-base})  value={decode(o.body.traces[0,bel_off]).sum():.0f}')
    print(f'  streak word bits: {sorted(s-base for s in streak)}')
    print(f'  register word bits: {sorted(r-base for r in reg)}')
    print(f'  word bit 12 value: {int(word[12])}  (action bit 2)')
    assert bel_off - base == 10
    assert 12 not in [s-base for s in streak], 'bit 12 collides with streak'
    assert 12 not in [r-base for r in reg], 'bit 12 collides with register'
    assert 12 != 10
print('OK: word bit 12 (action bit 2 of dead rule) is free and acquires as 1')
