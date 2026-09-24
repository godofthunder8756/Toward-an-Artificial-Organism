"""AC114: minimal boundary-exchange successor (SR-2) — engineering v1.

Implements the A1 exchange model (A1_EXCHANGE_SPEC_v1.md, SR-2): each contact
channel's intake is a function of the LOCAL live-state of a declared set of
boundary links (its *gate links*), not of the aggregate boundary count. The
aggregate B-count gate survives as a comparison arm ("rival") whose ceiling is
explicitly "B-dependent intake."

The change is confined to `ac4.react` actions 0/1 (admission gated on the gate
links) and — for the puncture arms only — a restriction of the action-8
candidate set (exclude the punctured link index). Every conservation identity in
`ac4.balance` is untouched: intake is carried as a variable, and gating `in_c`
to 0 when the gate link is a hole satisfies each identity by construction
(AC15's lesson point 1). The puncture zeroing is booked as `B_discard`, so the
boundary-count identity still holds.

The `reference` arm calls the frozen `ac9.step` object itself (no surgery), so
continuity is established by construction and the T5 inertness test is a
byte-identity comparison. `no_B_retention_ref` reproduces the frozen AC10
`no_B_retention` arm field-for-field (`state_hash` included) as the T1 retention
continuity check.

Engineering cohorts first (A2, seeds 0-7); the frozen confirmation is A3's job
(`--finals`, untouched seeds 6500-6507).
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import inspect
import json
import sys
import numpy as np
import ac9
import ac9_priority_v2 as v2
import ac4
import ac4_transport as tr
from ac1 import decode

# ---------------------------------------------------------------------------
# Supplied world constants (charter v2 §5). Fixed at protocol time.
# ---------------------------------------------------------------------------
# Channel c's intake is a function of the local live-state of GATE_LINKS[c]
# alone, and no other link. Singleton gates give the sharpest discrimination.
GATE_LINKS = {0: (0,), 1: (1,)}
# Aggregate rival threshold. Chosen so the rival (a) is inert in ordinary
# operation (count is always 20), (b) cuts intake when the boundary is fully
# gone (count 0), and (c) still admits after a single gate link is punctured
# (count 19). Any B_MIN in [2, 19] has all three properties; 10 is "half the
# perimeter".
B_MIN = 10
# Yields are the frozen values (ac4.react actions 0/1), unchanged.
YIELD = {0: 32, 1: 64}

# The puncture intervention: set the named link(s) to lifetime 0 and exclude
# them from action-8 candidates, leaving >= 1 non-gate link live.
PUNCTURE_LINKS = (0,)      # channel 0's gate link (D1/T4 decisive test)
NONGATE_PUNCTURE_LINKS = (5,)  # a non-gate link (D2: admission is local)

ARMS = ('keep', 'reference', 'rival', 'no_B', 'no_B_retention',
        'no_B_retention_ref', 'permeant', 'B_rescue', 'puncture',
        'rival_puncture', 'puncture_non_gate')
ONSET = 512

# ---------------------------------------------------------------------------
# Frozen source and surgery markers (asserted before every replacement).
# ---------------------------------------------------------------------------
STEP_SRC = inspect.getsource(ac9.step)
REACT_SRC = inspect.getsource(ac4.react)

B_EXPIRY_LINE = "    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1"
MOVE_CALL = "tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool))"
MOVE_CALL_NEW = "tr.move(b.pos,inactive,b.boundary,directions,impermeant_mask,retention_rescue)"

# ac4.react actions 0/1, gated on the admission decision.
INTAKE_BLOCK = ("    if action==0:\n"
                "        e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)\n"
                "    elif action==1:\n"
                "        e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)")
INTAKE_BLOCK_GATED = ("    if action==0:\n"
                      "        if ADMIT(b,0):\n"
                      "            e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)\n"
                      "    elif action==1:\n"
                      "        if ADMIT(b,1):\n"
                      "            e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)")
# action-8 candidate set, restricted by the puncture mask.
CANDIDATES_LINE = "            candidates=np.flatnonzero(near & (b.boundary<=64))"
CANDIDATES_LINE_PUNCTURED = "            candidates=np.flatnonzero(near & (b.boundary<=64) & ~PUNCTURE)"


# ---------------------------------------------------------------------------
# Admission decisions (the two models plus the disabled/continuity case).
# ---------------------------------------------------------------------------
def _admit_site(b, channel):
    """SR-2: intake iff at least one of channel c's gate links is live."""
    return bool((b.boundary[GATE_LINKS[channel]] > 0).any())


def _admit_count(b, channel):
    """Aggregate rival: intake iff the live-link count meets B_MIN."""
    return bool((b.boundary > 0).sum() >= B_MIN)


def _admit_none(b, channel):
    """Continuity: the frozen always-admit behaviour (exchange bypass)."""
    return True


ADMIT_FN = {'site': _admit_site, 'count': _admit_count, 'none': _admit_none}
GATE = {'keep': 'site', 'rival': 'count', 'no_B': 'site',
        'no_B_retention': 'site', 'no_B_retention_ref': 'none',
        'permeant': 'site', 'B_rescue': 'site', 'puncture': 'site',
        'rival_puncture': 'count', 'puncture_non_gate': 'site'}
NO_B_ARMS = ('no_B', 'no_B_retention', 'no_B_retention_ref', 'B_rescue')


def make_react(admit, puncture_mask, no_B=False):
    """Compile ac4.react with the admission gate and (optionally) the puncture.

    The gate wraps actions 0/1 in `if ADMIT(c)`. The puncture adds `& ~PUNCTURE`
    to the action-8 candidate set. `no_B` suppresses action 8 entirely by
    routing through the frozen `arm` guard, exactly as AC10 does.
    """
    src = REACT_SRC
    assert src.count(INTAKE_BLOCK) == 1, 'unexpected react text (intake)'
    src = src.replace(INTAKE_BLOCK, INTAKE_BLOCK_GATED)
    assert src.count(CANDIDATES_LINE) == 1, 'unexpected react text (candidates)'
    src = src.replace(CANDIDATES_LINE, CANDIDATES_LINE_PUNCTURED)
    ns = dict(vars(ac4))
    ns['ADMIT'] = admit
    ns['PUNCTURE'] = puncture_mask
    fns = {}
    exec(compile(src, 'ac114_react', 'exec'), ns, fns)
    react = fns['react']
    if no_B:
        def react(b, action, arm, e, _f=react):
            return _f(b, action, 'no_B', e)
    return react


def shim(react):
    """ac4 with only `react` replaced; the rest of the module stays frozen."""
    ns = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    ns['react'] = react
    return SimpleNamespace(**ns)


def external_B_restore(b, e):
    """AC4's frozen no_B_rescue restoration, reused verbatim (AC10)."""
    missing = b.boundary == 0
    e['external_B'] = int(missing.sum())
    b.boundary[missing] = 256


def make_puncture_gate(links):
    """Zero the punctured links once, booking each live link as B_discard.

    Idempotent: after the first tick the links are already 0 (and excluded from
    action-8 candidates, so never re-born), so subsequent calls are no-ops.
    """
    links = np.asarray(links, dtype=int)

    def puncture_gate(b, e):
        live = (b.boundary[links] > 0)
        if live.any():
            e['B_discard'] += int(live.sum())
            b.boundary[links] = 0
    return puncture_gate


def step_variant(react, permeant=False, retention_rescue=False, rescue_B=False,
                 puncture_links=None):
    """Return a step equal to the frozen one apart from the named edits."""
    src = STEP_SRC
    ns = dict(vars(ac9))
    ns['ac4'] = shim(react)
    if permeant or retention_rescue or rescue_B:
        assert src.count(MOVE_CALL) == 1, 'unexpected step text (transport call)'
        ns['impermeant_mask'] = np.zeros(20, dtype=bool) if permeant else np.ones(20, dtype=bool)
        ns['retention_rescue'] = bool(retention_rescue)
        src = src.replace(MOVE_CALL, MOVE_CALL_NEW)
    if rescue_B:
        assert src.count(B_EXPIRY_LINE) == 1, 'unexpected step text (B expiry)'
        src = src.replace(B_EXPIRY_LINE, B_EXPIRY_LINE + '\n    external_B_restore(b,e)')
        ns['external_B_restore'] = external_B_restore
    if puncture_links is not None:
        assert src.count(B_EXPIRY_LINE) == 1, 'unexpected step text (B expiry)'
        src = src.replace(B_EXPIRY_LINE, B_EXPIRY_LINE + '\n    puncture_gate(b,e)')
        ns['puncture_gate'] = make_puncture_gate(puncture_links)
    fns = {}
    exec(compile(src, 'ac114_step', 'exec'), ns, fns)
    return fns['step']


def build(arm):
    """Return (step_pre_onset, step_post_onset).

    `reference` is the frozen `ac9.step` object itself. Every other arm shims
    `ac4.react` with the arm's admission gate; the puncture arms run the normal
    step before ONSET and switch to a punctured step (gate links zeroed and
    excluded from action-8 candidates) at ONSET.
    """
    assert arm in ARMS, arm
    if arm == 'reference':
        return ac9.step, ac9.step
    admit = ADMIT_FN[GATE[arm]]
    no_B = arm in NO_B_ARMS
    kwargs = {}
    if arm == 'permeant':
        kwargs['permeant'] = True
    elif arm in ('no_B_retention', 'no_B_retention_ref'):
        kwargs['retention_rescue'] = True
    elif arm == 'B_rescue':
        kwargs['rescue_B'] = True

    if arm in ('puncture', 'rival_puncture', 'puncture_non_gate'):
        links = NONGATE_PUNCTURE_LINKS if arm == 'puncture_non_gate' else PUNCTURE_LINKS
        mask = np.zeros(20, dtype=bool)
        for link in links:
            mask[link] = True
        pre = step_variant(make_react(admit, np.zeros(20, dtype=bool), no_B=no_B), **kwargs)
        post = step_variant(make_react(admit, mask, no_B=no_B), puncture_links=links, **kwargs)
        return pre, post

    react = make_react(admit, np.zeros(20, dtype=bool), no_B=no_B)
    step = step_variant(react, **kwargs)
    return step, step


def run(seed, history, arm, ticks=2048):
    assert arm in ARMS, arm
    pre, post = build(arm)
    o = v2.acquire(seed)
    mapping = (seed % 2, (seed // 2) % 2)
    reference = decode(o.body.traces[0, :126]).copy()
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    assay = ac9.event()
    chrono = dict(first_acquire=None, first_loss=None, first_export=None,
                  first_dead=None, first_w_empty=None, first_c_empty=None,
                  first_gate_dead=None)
    had_both = False
    for t in range(ticks):
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        activation = [history == r for r in range(2)] if t < ONSET else [True, True]
        e = pre(o, core, noise, directions, coin, mapping, activation, t < ONSET) if t < ONSET \
            else post(o, core, noise, directions, coin, mapping, activation, t < ONSET)
        for k in total:
            total[k] += e[k]
        if t >= ONSET:
            for k in assay:
                assay[k] += e[k]
        routes = [o.memory.read(k) for k in (0, 1)]
        both = all(r is not None for r in routes)
        if both:
            had_both = True
            if chrono['first_acquire'] is None:
                chrono['first_acquire'] = t
        elif had_both and chrono['first_loss'] is None:
            chrono['first_loss'] = t
        if chrono['first_export'] is None and total['particle_export'] > 0:
            chrono['first_export'] = t
        if chrono['first_dead'] is None and o.body.dead:
            chrono['first_dead'] = t
        if chrono['first_gate_dead'] is None and not (o.body.boundary[GATE_LINKS[0][0]] > 0) \
                and not (o.body.boundary[GATE_LINKS[1][0]] > 0):
            chrono['first_gate_dead'] = t
        a = ac4.available(o.body)
        if chrono['first_w_empty'] is None and int(a[:16].sum()) == 0:
            chrono['first_w_empty'] = t
        if chrono['first_c_empty'] is None and int(a[16:].sum()) == 0:
            chrono['first_c_empty'] = t
    good = decode(o.body.traces[0, :126]) == reference
    return dict(seed=seed, history=history, arm=arm, ticks=ticks, mapping=mapping,
                activity=total['active'] / ticks, completed=total['active'] == ticks,
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                occupied_sites=int(o.memory.occupied().sum()),
                policy_accuracy=float(good.mean()),
                final_available=ac4.available(o.body).astype(int).tolist(),
                chrono=chrono, ledger=total, assay=assay,
                final_inventory=ac4.inventory(o.body), state_hash=o.digest())


def snapshot(names):
    return {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}


NAMES = ['ac114.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py',
         'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
         'AC114_PROTOCOL_v1.md']

# Untouched final seeds (disjoint from the engineering cohort 0-7 and from all
# prior final families). Seeds are the replication unit; the two histories per
# seed are repeated measures, not independent units (AC88).
FINAL_SEEDS = list(range(6500, 6508))


def collect(root, seeds):
    root = Path(root)
    root.mkdir(exist_ok=False)
    hashes = snapshot([n for n in NAMES if Path(n).exists()])
    (root / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (root / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[(r['history'], r['arm'],
                  round(r['activity'], 3), r['routes']) for r in rows[-2 * len(ARMS):]])), flush=True)
    (root / 'results.json').write_text(json.dumps(dict(hashes=hashes, rows=rows), indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac114_engineering_v1', list(range(8)))
        return
    collect('ac114_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
