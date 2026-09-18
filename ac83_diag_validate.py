import numpy as np
import ac83
import ac75
import ac12
import ac9
import ac4
import ac5_program as prog
import ac80
import ac71

print("=== validation 1: ac83 with simultaneous ticks (8192,8192) should reproduce AC82 internalized perm+corrupt ~14/16 survive, ~10/16 hold-both ===")
for seed in (0, 1, 2, 3, 4, 5, 6, 7):
    for history in (0, 1):
        r = ac83.run(seed, history, 'internalized', 'perm', True, 8192, 8192)
        print(f"s{seed}h{history}: done={int(r['completed'])} fw={r['flipped_still_wrong']} "
              f"routes={r['routes']} hold={int(ac83._holds_both(r))}")

print("\n=== validation 2: AC75 erase, transition='none' (no move) on seed 4 — does the MOVE cause the churn? ===")
def ac75_hold_frac(seed, history, transition):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc = ac75.ALLOC['erase']('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = ac71.build('allocate', alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    held = 0
    for t in range(ac75.TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        e = step(o, core, noise, directions, coin, tuple(ac75.mapping_at(base_map, t, transition)),
                 [True, True], True)
        if o.memory.demand().tolist() == [42, 0]:
            held += 1
    return held / ac75.TICKS, [o.memory.read(k) for k in (0, 1)]

for transition in ('none', 'perm'):
    for history in (0, 1):
        f, r = ac75_hold_frac(4, history, transition)
        print(f"AC75 erase s4h{history} {transition}: hold-frac={f:.3f} final={r}")
