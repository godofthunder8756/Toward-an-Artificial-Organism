"""AC86: replacement of the information-bearing components (recipe succession).

AC81 (milestone 2) showed the organism repeatedly replaces W/C/B components, but NEVER the
recipe-bearing storage itself (the 78-bit description in traces[1,:78]). This study closes that
gap: the recipe storage becomes a replaceable component.

The recipe lives in SLOTS=4 interchangeable storage slots in bank 1 (traces[1, 78*g : 78*(g+1)]),
with a 2-bit generation pointer also in bank 1 (traces[1, 312:314], after the four slots) selecting
the active slot. The generic decode reads the ACTIVE slot. In-place majority-repair (AC80's
reg_description, pointer-directed) keeps the active slot correct against the recipe damage stream,
and the pointer has its own integrity trigger + paid majority-restore (it lives in bank 1 and is
damaged by the recipe stream, so it must not depend on the program bank's action-2 repair).

On top of that maintenance, the organism SUCCEEDS the storage: on the recipe's own degradation
signal (the active slot's minority count reaching DESC_TRIGGER), rate-limited by a declared
cooldown, it constructs a functional successor copy of the active slot in the next slot (paid,
W-catalyzed), verifies the successor decodes to a valid program, switches the pointer, and only
then removes (clears) the old slot. Provenance (generation index, ticks, source/target, content
correctness) is tracked per succession.

The generic decode is ORDER-PRESERVING: AC80's build_program produces prog.program order, but the
acquired program is ac9_priority_v2's reorder (resource words 0-3, bank rules, boundary word last),
so AC80's re-instantiation reorders the bank. This runner reproduces the acquired layout.

Arms:
  succession   - repair + replaceable storage + succession machinery (the mechanism)
  repair       - AC80's in-place repair, no succession machinery (the baseline)
  unmaintained - no repair, no succession (maintenance contrast)

damage=True/False turns the recipe damage stream on/off (no-damage control: the mechanism is
inert). The succession is a paid capability, NOT a survival necessity -- in-place repair alone
already keeps the recipe correct (AC80) -- and the protocol states this plainly.
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
import ac80

TICKS = ac76.TICKS
DESC_TRIGGER = ac80.DESC_TRIGGER          # 2
DESC_BITS = ac80.DESC_BITS                # 78
PERM_OFFSET = ac80.PERM_OFFSET            # 70

SLOTS = 4                                  # interchangeable recipe slots in bank 1
SLOT_BITS = DESC_BITS
# Succession cadence: a new succession may start no sooner than this many ticks after the previous
# one started. The raw recipe-degradation trigger fires ~200x per horizon; the cooldown rate-limits
# the ~300-write replacement to an affordable cadence. Declared format-level constant.
SUCC_MIN_SPACING = 2400
# Max succession writes per tick (spreads the ~300-write copy+remove over many ticks so it does not
# front-load into the W/C collapse). Declared format-level constant.
SUCC_BUDGET = 6
# Pointer integrity trigger: the 2-bit pointer lives in bank 1 (recipe stream) and needs its own
# minority-count trigger (like DESC_TRIGGER for the 78-bit description). Declared constant.
POINTER_TRIGGER = 2

ARMS = ('succession', 'repair', 'unmaintained')

SOURCES = ['ac86.py', 'ac80.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC86_PROTOCOL_v1.md']

# The generation pointer lives in bank 1 (the recipe storage), at a fixed offset after the four
# slots. It is recipe metadata -- which slot holds the active copy -- so it belongs in the recipe
# bank, is damaged by the recipe stream, and is maintained by the recipe machinery, not by the
# program bank's action-2 repair (which fires far too slowly for a 2-bit pointer).
PTR_BASE = SLOTS * SLOT_BITS
PTR_OFFS = [PTR_BASE, PTR_BASE + 1]


def slot_offset(g):
    return g * SLOT_BITS


def read_slot(o, g):
    """Read slot g's 78-bit description by 7-replica majority."""
    off = slot_offset(g)
    return (o.body.traces[1, off:off + SLOT_BITS].sum(axis=-1) > 3).astype(np.uint8)


def read_pointer(o):
    """The generation pointer (which slot is active), read by majority from PTR_OFFS[0]=MSB,
    PTR_OFFS[1]=LSB, both in bank 1."""
    bits = (o.body.traces[1, PTR_OFFS].sum(axis=-1) > 3).astype(np.uint8)
    return int(2 * bits[0] + bits[1])


def desc_minority_active(o):
    """Minority count of the ACTIVE slot (the one the pointer selects)."""
    g = read_pointer(o)
    ones = o.body.traces[1, slot_offset(g):slot_offset(g) + SLOT_BITS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def resolve_offsets(o):
    """Register offsets (AC12's four allocation bits in the dead rule), resolved once from the
    pristine program. The generation pointer lives in bank 1 (see PTR_OFFS), not the program bank.
    """
    idx = ac12.dead_rule_index(o)
    return [14 * idx + 1 + k for k in range(4)]


def write_toward_slot(o, e, g, desired, budget=None):
    """Write slot g's replicas toward `desired` (78-bit), paid at the frozen per-action cap.
    `budget` optionally caps the per-tick write count (spreads a copy over several ticks).
    Returns the number of replicas written."""
    b = o.body
    off = slot_offset(g)
    sites = np.argwhere(b.traces[1, off:off + SLOT_BITS] != desired[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    if budget is not None:
        cap = min(cap, budget)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, off + idx[:, 0], idx[:, 1]] = desired[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['succ_writes'] = e.get('succ_writes', 0) + n
    return n


def write_pointer(o, e, g):
    """Write the generation pointer bits to point at slot g (paid). Returns replicas written."""
    b = o.body
    bits = np.array([(g >> 1) & 1, g & 1], dtype=np.uint8)
    sites = np.argwhere(b.traces[1, PTR_OFFS] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, [PTR_OFFS[i] for i in idx[:, 0]], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['succ_writes'] = e.get('succ_writes', 0) + n
    return n


class Succession:
    """State machine for one individual's recipe-succession machinery.

    mode 'real': copy -> verify -> switch -> remove, all paid writes through the body's own
    W-catalyzed write primitive. mode 'none': the machinery is absent (repair/unmaintained arms).
    `now` is set by the runner each tick; provenance is logged per completed succession.
    """
    def __init__(self, mode, encoded, min_tick=0, min_spacing=SUCC_MIN_SPACING,
                 budget=SUCC_BUDGET):
        self.mode = mode
        self.encoded = encoded               # acquisition description (observer-only provenance)
        self.min_tick = min_tick             # no succession before this tick
        self.min_spacing = min_spacing       # min ticks between succession starts
        self.budget = budget                 # max succession writes per tick (spreads the copy out)
        self.trigger = 'dm'                  # 'dm' (recipe degradation) or 'obs2' (program corruption)
        self.now = 0
        self.active = False
        self.phase = None
        self.source = None
        self.target = None
        self.last_start = -10**9
        self.log = []
        self._n = 0
        self._entry = None

    def start(self, o):
        g = read_pointer(o)
        self.source = g
        self.target = (g + 1) % SLOTS
        self.phase = 'copy'
        self.active = True
        self._entry = dict(n=self._n, source=g, target=self.target, start=self.now,
                           source_correct=int(np.array_equal(read_slot(o, g), self.encoded)))
        self._n += 1

    def advance(self, o, e, trigger):
        if self.mode != 'real':
            return
        if not self.active:
            if trigger and self.now >= self.min_tick and self.now - self.last_start >= self.min_spacing:
                self.start(o)
        if not self.active:
            return
        if self.phase == 'copy':
            src_maj = read_slot(o, self.source)
            write_toward_slot(o, e, self.target, src_maj, self.budget)
            if np.array_equal(read_slot(o, self.target), src_maj):
                perm = ac80.decode_perm(read_slot(o, self.target)[PERM_OFFSET:PERM_OFFSET + 8])
                self._entry['copy_done'] = self.now
                self._entry['verified_valid'] = int(sorted(perm) == list(range(4)))
                self._entry['target_correct'] = int(
                    np.array_equal(read_slot(o, self.target), self.encoded))
                self.phase = 'switch'
        elif self.phase == 'switch':
            write_pointer(o, e, self.target)
            if read_pointer(o) == self.target:
                self._entry['switch_tick'] = self.now
                self.phase = 'remove'
        elif self.phase == 'remove':
            write_toward_slot(o, e, self.source, np.zeros(SLOT_BITS, dtype=np.uint8), self.budget)
            if not o.body.traces[1, slot_offset(self.source):slot_offset(self.source) + SLOT_BITS].any():
                self._entry['remove_tick'] = self.now
                self._entry['done'] = True
                self.log.append(self._entry)
                self.active = False
                self.phase = None
                self.last_start = self.now


def reg_description_active(o, e):
    """Paid majority-restore of the ACTIVE recipe slot (AC80's reg_description, pointer-directed)."""
    b = o.body
    g = read_pointer(o)
    bits = read_slot(o, g)
    off = slot_offset(g)
    sites = np.argwhere(b.traces[1, off:off + SLOT_BITS] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, off + idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def pointer_minority(o):
    """Minority count of the 2 generation-pointer bits (their own integrity statistic)."""
    ones = o.body.traces[1, PTR_OFFS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def reg_pointer(o, e):
    """Paid majority-restore of the 2 generation-pointer bits (their own maintenance).

    The pointer lives in bank 1 and is damaged by the recipe stream. It needs its own integrity
    trigger, exactly as the 78-bit description needs DESC_TRIGGER; riding the program bank's
    action-2 repair (obs bit 2) would be far too slow and a majority flip would get cemented
    (AC61). Cheap (at most 14 writes), format-level (majority read, paid write)."""
    b = o.body
    bits = (b.traces[1, PTR_OFFS].sum(axis=-1) > 3).astype(np.uint8)
    sites = np.argwhere(b.traces[1, PTR_OFFS] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, [PTR_OFFS[i] for i in idx[:, 0]], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def rebuild_active(o):
    """Generic decode of the ACTIVE slot (AC80's rebuild, pointer-directed, order-preserving).

    AC80's `build_program` produces `prog.program` order (5 rule words then 4 bank rules), but the
    ACQUIRED program is `ac9_priority_v2`'s reorder: resource/production words 0-3, then the four
    bank rules (from the permutation), then the boundary word (mask 256) LAST. Re-instantiating in
    prog.program order therefore REORDERS the bank (verified in engineering: the dead rule moves
    from index 4 to index 5). The generic decode here reproduces the ACQUIRED layout so
    re-instantiation is order-preserving. Still format-only: words 0-3 verbatim, bank rules derived
    by the convention bank b -> (1, 4<<b, 2+b), word 4 last."""
    desc = read_slot(o, read_pointer(o))
    priority = ac80.decode_perm(desc[PERM_OFFSET:PERM_OFFSET + 8])
    if sorted(priority) != list(range(4)):
        return None
    words = desc[:PERM_OFFSET].reshape(5, prog.WIDTH)          # 5 rule words
    bank = np.concatenate([prog.encode_rule(1, 4 << b, 2 + b) for b in priority])
    return np.concatenate([words[:4].ravel(), bank, words[4]])


def reg_from_active(o, e, reg_offs):
    """Re-instantiate the program from the ACTIVE slot, excluding the register bits (dynamic
    decision state). The pointer is in bank 1, not the program bank, so it is untouched."""
    b = o.body
    target = rebuild_active(o)
    if target is None:
        return
    exclude = set(reg_offs)
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


def maintain(o, e, succ, reg_offs, repair):
    """The injected maintenance step: repair the active slot + pointer, advance succession,
    re-instantiate.

    Mirrors AC80's _reg_generic: the re-instantiation trigger is obs bit 2 (always) plus the
    active slot's minority count when repair is enabled. The pointer gets its OWN integrity trigger
    (`pointer_minority >= POINTER_TRIGGER`), independent of the recipe slot's damage, so it is
    maintained even when the active slot is clean. The succession trigger is the recipe's own
    degradation signal (`trigger='dm'`); with no damage the recipe never degrades so it never fires.
    """
    obs2 = bool(ac9.observe(o) & 4)
    dm = desc_minority_active(o)
    pm = pointer_minority(o)
    reg_trigger = obs2 or (repair and (dm >= DESC_TRIGGER or pm >= POINTER_TRIGGER))
    if succ.trigger == 'obs2':
        succ_trigger = obs2
    else:
        succ_trigger = dm >= DESC_TRIGGER
    if repair:
        if reg_trigger:
            reg_description_active(o, e)
        if pm >= POINTER_TRIGGER:
            reg_pointer(o, e)
    succ.advance(o, e, succ_trigger)
    if reg_trigger:
        reg_from_active(o, e, reg_offs)


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


def build(arm, alloc, succ, reg_offs, repair):
    """Build the AC76-style step, injecting `maintain` as the re-instantiation/maintenance call."""
    base, cut = ac71.arm_parts('allocate')
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = maintain
    ns['succ'] = succ
    ns['reg_offs'] = reg_offs
    ns['repair'] = repair
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(ACTION_LINE) == 1
    src = src.replace(ACTION_LINE, "        maintain(o,e,succ,reg_offs,repair)\n" + ACTION_LINE)
    assert src.count(BALANCE_LINE) == 1
    src = src.replace(BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)\n" + BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac86_step', 'exec'), ns, fns)
    return fns['step']


# per-arm config: (repair, succession_mode)
ARM_PARTS = {
    'succession':   (True,  'real'),
    'repair':       (True,  'none'),
    'unmaintained': (False, 'none'),
}


def run(seed, history, arm, damage=True, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    reg_offs = resolve_offsets(o)
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :DESC_BITS] = encoded[:, None]          # slot 0 = acquisition recipe
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    repair, mode = ARM_PARTS[arm]
    succ = Succession(mode, encoded)
    step = build(arm, alloc, succ, reg_offs, repair)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for the recipe
    total = ac9.event()
    total['reg_writes'] = 0
    total['succ_writes'] = 0
    first_dead = None
    for t in range(ticks):
        alloc.now = t
        succ.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage:
            g = read_pointer(o)
            off = slot_offset(g)
            o.body.traces[1, off:off + SLOT_BITS] |= (rng1.random((SLOT_BITS, 7)) < .0001).astype(np.uint8)
            o.body.traces[1, PTR_OFFS] |= (rng1.random((2, 7)) < .0001).astype(np.uint8)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    desc_bits = read_slot(o, read_pointer(o))
    desc_priority = ac80.decode_perm(desc_bits[PERM_OFFSET:PERM_OFFSET + 8])
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    # program_correct excludes the register bits: they are dynamic decision state, not program
    # content. (The pointer is in bank 1, so it is not part of the program bank at all.)
    static = np.ones(prog.PROGRAM_BITS, dtype=bool)
    static[list(reg_offs)] = False
    return dict(seed=seed, history=history, arm=arm, damage=damage, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                successions=len([s for s in succ.log if s['done']]),
                succession_log=succ.log,
                pointer=read_pointer(o),
                description_correct=int((desc_bits == encoded).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                program_correct=int((decoded[static] == acquired[static]).sum()),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']),
                routes=[o.memory.read(k) for k in (0, 1)], demand=o.memory.demand().tolist(),
                state_hash=o.digest())


def gates(rows):
    def pick(arm, damage):
        return [r for r in rows if r['arm'] == arm and r['damage'] == damage]

    succ = pick('succession', True)
    repair = pick('repair', True)
    unmaintained = pick('unmaintained', True)
    succ_ctrl = pick('succession', False)
    repair_ctrl = pick('repair', False)
    unmaintained_ctrl = pick('unmaintained', False)
    return {
        'G1_succession_occurs': all(
            r['successions'] >= 2 for r in succ if r['completed']),
        'G2_successor_functional': all(
            (r['successions'] >= 2 and
             all(s['verified_valid'] == 1 and s['target_correct'] == 1 for s in r['succession_log'] if s['done'])
             and r['description_correct'] == 78 and r['description_valid'] == 1)
            for r in succ if r['completed']),
        'G3_remove_after_verify': all(
            all(s['remove_tick'] >= s['switch_tick'] >= s['copy_done'] >= s['start']
                for s in r['succession_log'] if s['done'])
            for r in succ if r['completed']),
        'G4_recipe_maintained': (
            all(r['description_correct'] == 78 for r in succ if r['completed'])
            and all(r['description_correct'] == 78 for r in repair if r['completed'])
            and all(r['description_correct'] < 78 for r in unmaintained)),
        'G5_succession_is_the_replacer': (
            all(r['successions'] == 0 for r in repair)
            and all(r['successions'] == 0 for r in unmaintained)
            and all(r['successions'] >= 2 for r in succ if r['completed'])),
        'G6_control_clean': (
            all(r['successions'] == 0 for r in succ_ctrl + repair_ctrl + unmaintained_ctrl)
            and all(r['description_correct'] == 78 for r in succ_ctrl)
            and all(r['description_correct'] == 78 for r in repair_ctrl)
            and all(r['description_correct'] == 78 for r in unmaintained_ctrl)
            and all(succ_ctrl[i]['state_hash'] == repair_ctrl[i]['state_hash']
                    for i in range(len(succ_ctrl)))),
        'G7_completeness_determinism': None,
    }


def preflight(protocol='AC86_PROTOCOL_v1.md'):
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
                    for damage in (True, False):
                        r = run(seed, history, arm, damage)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['damage'], r['completed'], r['first_dead'],
                 r['successions'], r['description_correct'], r['pointer'],
                 r['writes'])
                for r in rows[-2 * len(ARMS) * 2:]]), default=str), flush=True)
    g = gates(rows)
    g['G7_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS) * 2
        and all(run(s, h, a, d) == orig for s, h, a, d, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['damage'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac86_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac86_results_v1', [4016, 4017, 4018, 4019])


if __name__ == '__main__':
    main()
