"""AC67: organizational closure — non-self-reversing damage makes the repair loop load-bearing.

AC14 cut the repair link and found the loop *arithmetically inert*: the program bank's
7-replica register is damaged by XOR flips, which self-reverse, so a replica that reads
damaged returns to its original value on the next hit, the register never reaches a
majority flip, and the repair action is never actually needed. AC14's option 2 was a
**non-self-reversing damage model** — a flip that stays flipped until repaired — "the
more interesting option because it makes repair load-bearing by construction."

AC67 makes exactly that one change, and nothing else: the program-bank damage is applied
as a sticky SET (`|=`) instead of a toggle (`^=`), so a damaged replica stays damaged
until the paid bank-0 repair rewrites it to the decoded majority. The register read
convention is single-replica (`REGISTER_THRESHOLD=1`), so the decision state is genuinely
at risk the moment one replica is set.

The loop (unchanged from AC12/AC14):

    register (4 bits) in traces[0,:126]
      -> repaired only by the paid bank-0 repair action
      -> whose capacity is the core interior W (group 0)
      -> produced by the action-6 reaction
      -> chosen by the program that contains the register

Claim under test: with sticky damage, the organism's own paid repair maintains its own
decision state against persistent corruption; cutting the repair link degrades the
register and the degradation propagates into the organism's own maintenance decisions
(routes lapse, occupancy falls, survival fails).

Falsifier, declared before running: if cutting the repair link still does not degrade the
register, or the degradation does not propagate into the organism's routes/occupancy/
survival, the loop is not load-bearing and closure is not established.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import inspect
import json
import sys
import numpy as np
import ac9
import ac12
import ac4
from ac1 import decode

ARMS = ('closed', 'no_repair', 'protected_closed', 'protected_no_repair')

PORTS = 4
YIELD_M = 64
YIELD_F = 64
TICKS = 4096          # twice the lineage standard, so unrepaired sticky damage accumulates
DEV = 512

# The one declared change from the frozen physics: program-bank damage is a sticky SET,
# not a self-reversing XOR. A damaged replica stays damaged until the paid repair rewrites
# it. The memory bank's damage is left untouched (XOR), so route loss can only propagate
# from the decision state, not from confounded memory-bank damage.
DAMAGE_LINE = "b.traces[0,:126]^=core_flips"
DAMAGE_LINE_STICKY = "b.traces[0,:126]|=core_flips"


def arm_parts(arm):
    """(ac12 base arm, cut the program-bank repair link?)

    NOTE: a previous draft (and AC14) matched '_no_repair' in arm, but the arm is
    named 'no_repair' (no leading underscore), so the substring test never matched
    and the 'no_repair' arm ran with repair ENABLED -- identical to 'closed'. That
    made the loop look inert by construction. The fix matches 'no_repair' in arm.
    """
    return ('protected' if arm.startswith('protected') else 'allocate',
            'no_repair' in arm)


def build(arm, alloc):
    base, cut = arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    # The declared change: sticky (non-self-reversing) program-bank damage.
    assert src.count(DAMAGE_LINE) == 1, 'unexpected step text (damage line)'
    src = src.replace(DAMAGE_LINE, DAMAGE_LINE_STICKY)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    if base == 'protected':
        shadow = alloc.shadow
        ns['prog'] = SimpleNamespace(choose=lambda tr, ob: ac12.choose_with_shadow(tr, ob, shadow))
    fns = {}
    exec(compile(src, 'ac67_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm, ticks=TICKS):
    base, cut = arm_parts(arm)
    ac12.PORTS = PORTS; ac12.YIELD_M = YIELD_M; ac12.YIELD_F = YIELD_F
    ac12.POST_YIELD_M = None; ac12.MOVE_KEYS = (); ac12.MOVE = 10**9
    ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 1            # single-replica read: the decision is genuinely at risk
    alloc = ac12.Alloc(base, seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    installed = decode(o.body.traces[0, :126]).copy()
    step = build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event(); actions = {}
    first_dead = None; first_register_flip = None; first_rule_error = None
    register_flip_ticks = []
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
        actions[a] = actions.get(a, 0) + 1
        e = step(o, core, noise, directions, coin, base_map, [t < DEV] * 2, t < DEV)
        for k in total:
            total[k] += e.get(k, 0)
        if first_register_flip is None and any(ac12.bit_value(o, off) for off in offs):
            first_register_flip = t
        if first_rule_error is None and (decode(o.body.traces[0, :126]) != installed).any():
            first_rule_error = t
        if first_dead is None and o.body.dead:
            first_dead = t
    dec = decode(o.body.traces[0, :126])
    return dict(seed=seed, history=history, arm=arm, ticks=ticks,
                activity=total['active'] / ticks, completed=total['active'] == ticks,
                first_dead=first_dead,
                program_bits_damaged=int((dec != installed).sum()),
                rules_touched=int(sum(1 for r in range(9)
                                      if (dec[14 * r:14 * r + 14] != installed[14 * r:14 * r + 14]).any())),
                register=[ac12.bit_value(o, off) for off in offs],
                register_any_flip=any(ac12.bit_value(o, off) for off in offs),
                first_register_flip=first_register_flip, first_rule_error=first_rule_error,
                dropped=alloc.log['dropped'], actions=actions,
                demand=o.memory.demand().tolist(), occupied=int(o.memory.occupied().sum()),
                routes=[o.memory.read(k) for k in (0, 1)],
                ledger=total, final_inventory=ac4.inventory(o.body), state_hash=o.digest())


NAMES = ['ac67.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
         'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
         'test_ac67.py', 'AC67_PROTOCOL_v1.md']


def collect(root, seeds):
    root = Path(root); root.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (root / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm); rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['arm'], round(r['activity'], 3), r['completed'],
                 r['program_bits_damaged'], r['rules_touched'],
                 [int(x) for x in r['register']], r['first_register_flip'], r['first_dead'])
                for r in rows[-2 * len(ARMS):]])), flush=True)
    (root / 'results.json').write_text(json.dumps(dict(hashes=hashes, rows=rows), indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac67_engineering_v1', [0, 1, 2]); return
    collect('ac67_results_v1', [2600, 2601, 2602, 2603])


if __name__ == '__main__':
    main()
