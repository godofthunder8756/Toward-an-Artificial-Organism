"""AC84: milestone 2 strengthened -- component turnover reported unconditionally.

AC81 (milestone 2) froze replacement-across-generations but survivor-gated: its turnover gates
(G1-G3) were conditioned on `completed`, and the final family was collapse-dominated (internalized
2/8), so the turnover claim rested on 2 survivors -- the survivor-conditioning weakness flagged in
AC79's and AC80's G1.

This study reports the same turnover claim UNCONDITIONALLY, across the whole planned cohort. The
components (W catalysts, C converters, B boundary) turn over continuously with NO intervention, so
the t=8192 kill intervention is dropped entirely: the claim is demonstrated by counting
construction (births), use (repair writes, energy conversion) and replacement (births >= the slot
complement) per individual over a horizon chosen to sit inside the pre-collapse window (4096 ticks,
well before the AC68 W/C collapse onset ~7400-7800). Turnover is NOT gated on survivors: every
individual in the cohort, dead or alive, is scored on the same turnover floors. If the AC68 collapse
still kills some individuals, that is reported as a finding about the body's fragility, not used as
a licence to gate.

The mechanism is AC80's, unchanged: the production rules (W/C/B birth) are the description's words
3-5; the program is rebuilt from the 78-bit description by the generic decode; the description is
maintained by its own DESC_TRIGGER. Arms are internalized (the claim), unmaintained (recipe degrades
-> turnover is not sustained) and no_repair (loop cut -> turnover halts). `pristine` (AC80's hidden
backup) is dropped: its description is never damaged, so it is not a test of the maintained recipe,
and its early W/C collapses (t=439-673 in engineering) give it non-unconditional turnover, muddying
the contrast. The load-bearing arms establish that the turnover is driven by the internally-retained,
maintained recipe.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = 4096                       # inside the pre-collapse window; turnover is ~20x by then
ARMS = ('internalized', 'unmaintained', 'no_repair')

SOURCES = ['ac84.py', 'ac80.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC84_PROTOCOL_v1.md']

# The turnover floors = the physical slot complement of each component class (16 W slots, 4 C slots,
# 20 B sites). "births >= complement" means the class has been fully replaced at least once over the
# horizon. Declared as the unconditional floor: every individual in the cohort, dead or alive, must
# meet it. Measured in engineering across 256 individuals (seeds 0-127): the earliest W/C-collapse
# individual (t=603) still reaches W=30, C=5, B=37 -- above each complement -- because the collapse
# cascade takes hundreds of ticks to develop, during which the production rules keep birthing. So the
# floor is met by every individual, survivor or not. "Multiple turnover cycles" is the stronger
# claim, demonstrated by the per-individual distribution (healthy ~20x, earliest collapse ~1.3-1.9x),
# reported descriptively rather than gated.
W_SLOTS, C_SLOTS, B_SLOTS = 16, 4, 20
W_BIRTH_FLOOR = W_SLOTS
C_BIRTH_FLOOR = C_SLOTS
B_BIRTH_FLOOR = B_SLOTS


def run(seed, history, arm, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    ac_arm, damage_desc, maintained = ac80.ARM_PARTS[arm]
    reg_fn = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)
    step = ac80.build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    first_acquire = [None, None]                    # tick each route was first bound
    first_loss = None                               # tick a previously-held route first lapsed
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        for k in (0, 1):
            if first_acquire[k] is None and o.memory.read(k) is not None:
                first_acquire[k] = t
        if first_loss is None:
            for k in (0, 1):
                if first_acquire[k] is not None and o.memory.read(k) is None:
                    first_loss = t
                    break
        if first_dead is None and o.body.dead:
            first_dead = t
    desc_bits = ac80.read_description(o)
    desc_priority = ac80.decode_perm(desc_bits[ac80.PERM_OFFSET:ac80.PERM_OFFSET + 8])
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                W_birth=int(total['W_birth']), C_birth=int(total['C_birth']),
                B_birth=int(total['B_birth']),
                writes=int(total['writes']), converted=int(total['converted']),
                particle_export=int(total['particle_export']),
                W_live=int((o.body.life[:16] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                routes=[o.memory.read(k) for k in (0, 1)],
                first_acquire=first_acquire, first_route_loss=first_loss,
                demand=o.memory.demand().tolist(),
                description_correct=int((desc_bits == encoded).sum()),
                description_same=int(desc_priority == tuple(priority)),
                energy=inv[0], material=inv[1], fuel=inv[2], state_hash=o.digest())


def gates(rows):
    def pick(arm):
        return [r for r in rows if r['arm'] == arm]

    internalized = pick('internalized')
    unmaintained = pick('unmaintained')
    no_repair = pick('no_repair')
    return {
        # G1: turnover is UNCONDITIONAL -- every internalized individual, dead or alive, fully
        # replaces each component class (births >= complement). No `completed` filter (the AC81
        # weakness this study fixes).
        'G1_turnover_unconditional': all(
            r['W_birth'] >= W_BIRTH_FLOOR and r['C_birth'] >= C_BIRTH_FLOOR
            and r['B_birth'] >= B_BIRTH_FLOOR
            for r in internalized),
        # G2: use is UNCONDITIONAL -- every internalized individual repaired (W), converted (C), and
        # built its acquired organization (both routes bound during development).
        'G2_use_unconditional': all(
            r['writes'] > 0 and r['converted'] > 0
            and r['first_acquire'][0] is not None and r['first_acquire'][1] is not None
            for r in internalized),
        # G3: the reconstruction loop is load-bearing (AC80 control, categorical).
        'G3_loop_load_bearing': all(not r['completed'] for r in no_repair),
        # G4: the recipe degrades when unmaintained -- the maintenance is what keeps it intact.
        'G4_recipe_degrades_unmaintained': all(
            r['description_correct'] < 78 for r in unmaintained),
        # G5: recipe maintained in survivors -- the only endpoint that is genuinely survivor-scoped
        # (the paid description maintenance stops at death, AC79's post-mortem degradation). Turnover
        # is NOT gated on survivors; this gate is about the description, not the turnover.
        'G5_recipe_maintained_survivors': all(
            r['description_correct'] == 78 for r in internalized if r['completed']),
        'G6_completeness_determinism': None,
    }


def preflight(protocol='AC84_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), \
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}'
    missing = [s for s in declared if not Path(s).exists()]
    assert not missing, f'declared sources missing: {missing}'
    return declared


def collect(root, seeds):
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm)
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['completed'], r['first_dead'],
                 r['W_birth'], r['C_birth'], r['B_birth'],
                 r['writes'], r['converted'], r['particle_export'],
                 r['description_correct'], r['routes'], r['first_acquire'], r['first_route_loss'])
                for r in rows[-2 * len(ARMS):]]), default=str), flush=True)
    g = gates(rows)
    g['G6_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS)
        and all(run(s, h, a) == orig for s, h, a, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac84_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac84_results_v1', [4020, 4021, 4022, 4023])


if __name__ == '__main__':
    main()
