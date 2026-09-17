"""AC80: internalize the reconstruction recipe — generic decode from a 78-bit description.

AC79 froze that the 8-bit priority description's STORAGE + MAINTENANCE are endogenous, but the
reconstruction RECIPE is still external: `reg_maintained` (ac79.py) computes
`target = prog.program(priority)`, and `prog.program` (ac5_program.py) hard-codes the five
resource/production/repair rule words `(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)` — the
controller's organization — with only the four bank rules derived from the stored permutation.
So AC79 shows reconstruction is FUNDED through vulnerable paid machinery (an economic dependency),
NOT that the information/machinery performing it is internalized.

This study removes that scaffold. The complete organism-specific description — the five rule words
(5 x 14 = 70 bits) + the 8-bit permutation = 78 bits — is stored in vulnerable, damage-streamed,
paid-maintained state (`traces[1,:78]`, 7 replicas/bit). During life the re-instantiation no longer
calls `prog.program`; it calls a GENERIC decode that reads the 78-bit description by majority and
rebuilds the 126-bit program. The generic layer knows only the FORMAT (14-bit word =
enabled | mask<<1 | action<<10, the 5-word + 4-bank layout, bank b -> mask 4<<b / action 2+b,
majority read, paid write). No function on the reconstruction path knows any rule word value or the
permutation — those are read from the vulnerable state.

`prog.program` is retained ONLY in the observer (corruption setup and endpoint scoring), never on
the organism's reconstruction path.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = ac76.TICKS
CORRUPT_TICK = ac76.CORRUPT_TICK
CORRUPT_BITS = ac76.CORRUPT_BITS

ARMS = ('internalized', 'pristine', 'unmaintained', 'no_repair')

# each arm -> (ac_arm for ac71.build-style surgery, damage the description?, maintain (repair) it?)
# pristine = 78-bit description NEVER damaged (hidden-backup baseline, generic decode, no repair)
# unmaintained = 78-bit description damaged, NOT repaired (generic decode reads a degrading description)
ARM_PARTS = {
    'internalized':  ('regen',     True,  True),   # desc damaged + repaired + generic decode
    'pristine':      ('regen',     False, False),  # desc never damaged (hidden backup), generic decode
    'unmaintained':  ('regen',     True,  False),  # desc damaged, NO repair, generic decode
    'no_repair':     ('no_repair', True,  False),  # loop cut (load-bearing control)
}

SOURCES = ['ac80.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC80_PROTOCOL_v1.md']

DESC_BITS = 78                      # 5 rule words (5x14) + 8-bit permutation
NWORDS = 5
PERM_OFFSET = NWORDS * prog.WIDTH   # 70

# The description repair trigger threshold. AC79 rode the program's corruption signal (obs bit 2),
# which is conservative only because the program (126 bits) is 16x the 8-bit description. At 78 bits
# the program is only ~1.6x larger and, measured in engineering, obs bit 2 does NOT fire early enough
# for some individuals — a description WORD or PERM bit reaches a majority flip first, corrupting the
# controller. The description therefore needs its OWN trigger: the description's minority count
# (sum over bits of min(ones, 7-ones), the same integrity statistic obs bit 2 computes for the
# program) reaching DESC_TRIGGER. This is format-level (7 replicas per bit, minority detectable), no
# new observation bit, and no policy knowledge.
DESC_TRIGGER = 2


def desc_minority(o):
    """The description's minority count: sum over bits of min(ones, 7-ones)."""
    ones = o.body.traces[1, :DESC_BITS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


# The five resource/production/repair rule words = the controller's organization. This is the
# INHERITED CONTENT installed at acquisition. It is forbidden on the reconstruction path (rebuild
# reads these bits back from the vulnerable state; it never references FIXED_WORDS).
FIXED_WORDS = ((1, 1, 0), (1, 2, 1), (1, 64, 6), (1, 128, 7), (1, 256, 8))


def encode_perm(priority):
    return ac76.encode_priority(priority)


def decode_perm(bits):
    return tuple(int((bits[2 * i] << 1) | bits[2 * i + 1]) for i in range(4))


def description_bits(priority):
    """The 78-bit description installed at acquisition (inherited content, allowed at acquisition)."""
    words = np.concatenate([prog.encode_rule(*w) for w in FIXED_WORDS])
    return np.concatenate([words, encode_perm(priority)])


def read_description(o):
    """Read the 78-bit description by 7-replica majority (the same convention as prog.choose)."""
    return (o.body.traces[1, :DESC_BITS].sum(axis=-1) > 3).astype(np.uint8)


def build_program(desc, priority):
    """Rebuild the 126-bit program from a 78-bit description. GENERIC — format only.

    The five rule words are copied VERBATIM from the description (their content is entirely in the
    vulnerable state); the four bank rules are derived from the permutation via the architectural
    convention bank b -> (enabled=1, mask=4<<b, action=2+b). No rule word value is known here.
    """
    words = desc[:PERM_OFFSET]
    bank = np.concatenate([prog.encode_rule(1, 4 << v, 2 + v) for v in priority])
    return np.concatenate([words, bank])


def rebuild(o):
    """Generic decode: read the 78-bit description by majority, rebuild the 126-bit program.

    Returns None if the decoded permutation is not a valid permutation. Does NOT call prog.program.
    """
    desc = read_description(o)
    priority = decode_perm(desc[PERM_OFFSET:PERM_OFFSET + 8])
    if sorted(priority) != list(range(4)):
        return None
    return build_program(desc, priority)


def reg_description(o, e):
    """Paid majority-restore of the 78-bit description in bank 1.

    Same primitive as AC79's 8-bit repair, widened to 78 bits. Restores each bit's minority
    replicas to its 7-replica majority under the frozen per-action cap; charges 1 energy + 1
    material per repaired replica.
    """
    b = o.body
    bits = read_description(o)
    sites = np.argwhere(b.traces[1, :DESC_BITS] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def _reg_generic(o, e, repair_desc):
    """Re-instantiate the program from the 78-bit description when the trigger fires.

    The trigger is (obs bit 2 = program corruption) OR, for the maintained arm, the description's own
    minority count reaching DESC_TRIGGER. `repair_desc` controls whether the description is first
    majority-restored (paid). The generic decode is `rebuild`; the program is re-instantiated to its
    output, excluding the 4 register bits (dynamic decision state) in the dead rule's low mask bits,
    exactly as AC76/AC79.
    """
    b = o.body
    trigger = bool(ac9.observe(o) & 4)
    if repair_desc:
        trigger = trigger or (desc_minority(o) >= DESC_TRIGGER)
    if not trigger:
        return
    if repair_desc:
        reg_description(o, e)
    target = rebuild(o)
    if target is None:
        return
    desc = read_description(o)
    priority = decode_perm(desc[PERM_OFFSET:PERM_OFFSET + 8])
    dead_idx = 4 + priority.index(3)                              # mask-32 rule (bank 3)
    exclude = {14 * dead_idx + 1 + k for k in range(4)}           # its 4 register bits
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[0, idx[:, 0], idx[:, 1]] = target[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


def reg_maintained(o, e):
    _reg_generic(o, e, True)


def reg_pristine(o, e):
    _reg_generic(o, e, False)


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


def build(ac_arm, alloc, reg_fn):
    """Build the AC76-style step, injecting `reg_fn` as the re-instantiation called on obs bit 2.

    `reg_fn` is reg_maintained (internalized), reg_pristine (pristine/unmaintained), or None
    (no_repair — the loop is cut and the injected call is a no-op with no regen surgery).
    """
    base, cut = ac71.arm_parts(ac_arm)
    regen = reg_fn is not None
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['reg_from_priority'] = (reg_fn if regen else (lambda o, e: None))
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    if regen:
        assert src.count(ACTION_LINE) == 1
        src = src.replace(ACTION_LINE, "        reg_from_priority(o,e)\n" + ACTION_LINE)
        assert src.count(BALANCE_LINE) == 1
        src = src.replace(BALANCE_LINE, "    e['writes']+=e.get('reg_writes',0)\n" + BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac80_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm, corrupt=True, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = description_bits(priority)
    o.body.traces[1, :DESC_BITS] = encoded[:, None]
    ac_arm, damage_desc, maintained = ARM_PARTS[arm]
    reg_fn = reg_maintained if maintained else (reg_pristine if ac_arm == 'regen' else None)
    step = build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    alive_at_corruption = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :DESC_BITS] |= (rng1.random((DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            correct = prog.program(priority)   # observer-only: sets up the intervention
            for bit in range(CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == CORRUPT_TICK:
            alive_at_corruption = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)   # observer-only: endpoint ground truth
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = read_description(o)
    desc_priority = decode_perm(desc_bits[PERM_OFFSET:PERM_OFFSET + 8])
    return dict(seed=seed, history=history, arm=arm, damage_desc=damage_desc,
                maintained=maintained, corrupt=corrupt, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_corruption=alive_at_corruption,
                program_correct=int((decoded == target).sum()), program_bits=prog.PROGRAM_BITS,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != target[:CORRUPT_BITS]).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_word_correct=int((desc_bits[:PERM_OFFSET] == encoded[:PERM_OFFSET]).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                routes=[o.memory.read(k) for k in (0, 1)], demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs], state_hash=o.digest())


def gates(rows):
    def pick(arm, corrupt):
        return [r for r in rows if r['arm'] == arm and r['corrupt'] == corrupt]

    def alive8192(rs):
        return [r for r in rs if r['alive_at_corruption']]

    internalized = pick('internalized', True)
    pristine = pick('pristine', True)
    unmaintained = pick('unmaintained', True)
    no_repair = pick('no_repair', True)
    internalized_ctrl = pick('internalized', False)
    pristine_ctrl = pick('pristine', False)
    return {
        # recovery + description integrity are clean only for survivors: the paid maintenance stops
        # at death, and the AC68 W/C collapse kills internalized and pristine alike. Survival is
        # reported as a bimodality-aware lower bound, not gated to an exact count.
        'G1_internalized_recovers': all(
            r['flipped_still_wrong'] == 0 and r['description_same'] == 1
            for r in internalized if r['completed']),
        'G2_unmaintained_fails': all(
            r['flipped_still_wrong'] > 0 and r['description_valid'] == 0
            for r in alive8192(unmaintained)),
        'G3_maintenance_load_bearing': (
            all(not r['completed'] and r['first_dead'] is not None
                for r in alive8192(unmaintained))
            and any(r['completed'] for r in internalized)),
        'G4_no_repair_dies': all(not r['completed'] for r in no_repair),
        'G5_control_clean': (
            all(r['flipped_still_wrong'] == 0 for r in internalized_ctrl + pristine_ctrl)
            and all(r['description_same'] == 1 for r in pristine_ctrl)
            and all(r['description_same'] == 1 for r in internalized_ctrl if r['completed'])),
        'G6_completeness_determinism': None,
    }


def preflight(protocol='AC80_PROTOCOL_v1.md'):
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
                    for corrupt in (True, False):
                        r = run(seed, history, arm, corrupt)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['corrupt'], r['completed'], r['first_dead'],
                 r['flipped_still_wrong'], r['description_same'], r['description_valid'],
                 r['description_word_correct'])
                for r in rows[-2 * len(ARMS) * 2:]]), default=str), flush=True)
    g = gates(rows)
    g['G6_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS) * 2
        and all(run(s, h, a, c) == orig for s, h, a, c, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['corrupt'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac80_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac80_results_v1', [4008, 4009, 4010, 4011])


if __name__ == '__main__':
    main()
