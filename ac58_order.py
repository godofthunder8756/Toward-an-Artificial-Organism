"""AC58: repair retains the acquired order, preventing corruption-induced collapse. A frozen study.

The claim (AC58_PROTOCOL_v1.md): the acquired six-position order in a replica-encoded register is
corrupted over the run; repair retains it, sustaining production and survival, while an unrepaired
register corrupts and the organism collapses. This turns AC14's integrity channel ON (AC43 left it off)
and joins it to the developmental line (AC57's acquired order).

World: AC57's scaled body (regime B), AC50's World, the order read back from a 10-bit x 7-replica
register each tick. Arms: protected, repaired, unrepaired. Endpoint: value-weighted production over 600
ticks.

Final seeds 4848-4859, disjoint from engineering 4612-4635 and scoring 9012-9023.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac50_heterogeneous as a50
import ac38_variance as ac38

STRESS_MULT = 7
VALUES_B = (0.5, 2.0, 3.0, 4.0, 5.0, 100.0)
RATES_B = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))
OPT_B = (5, 1, 2, 4, 3, 0)
TICKS = a50.TICKS
HORIZON = a50.HORIZON_TICKS

DAMAGE_RATE = 0.005
REPAIR_COST = 1
REPAIR_BUDGET = 10

FINAL_SEEDS = tuple(range(4848, 4860))
BAR = 8000.0
P_BAR = 0.01
MIN_N = 8
STEADY_LO, STEADY_HI = 2.4, 2.6

ARMS = ('protected', 'repaired', 'unrepaired')
SOURCES = ['ac58_order.py', 'ac58_engineering.py', 'ac50_heterogeneous.py', 'ac30_acquire.py',
           'ac29_register.py', 'ac38_variance.py', 'AC58_PROTOCOL_v1.md']


def run_register(seed, arm, ticks=TICKS):
    rng = np.random.default_rng([seed, 5801])
    register = reg.Register()
    register.write(reg.lehmer(OPT_B))
    w = a50.World(seed, RATES_B, VALUES_B)
    for _ in range(ticks):
        if w.dead:
            break
        if arm == 'repaired':
            register.damage(rng, DAMAGE_RATE)
            if w.energy >= REPAIR_COST:
                register.repair(REPAIR_BUDGET)
                w.energy -= REPAIR_COST
        elif arm == 'unrepaired':
            register.damage(rng, DAMAGE_RATE)
        # protected: no damage
        order = register.read()
        word = w.urgency()
        action = None
        if order is not None:
            for pos in order:
                if word >> pos & 1:
                    action = pos
                    break
        w.tick(action)
    return dict(produced=w.produced, dead=w.dead)


def individual(seed):
    return dict(seed=seed,
                protected=run_register(seed, 'protected'),
                repaired=run_register(seed, 'repaired'),
                unrepaired=run_register(seed, 'unrepaired'))


def gates(rows):
    post = lambda arm: [r[arm]['produced'] for r in rows]
    prot = post('protected'); rep = post('repaired'); unrep = post('unrepaired')
    d = np.asarray([a - b for a, b in zip(rep, unrep)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead_rep = sum(1 for r in rows if r['repaired']['dead'])
    dead_prot = sum(1 for r in rows if r['protected']['dead'])
    dead_unrep = sum(1 for r in rows if r['unrepaired']['dead'])
    retention = all(a == b for a, b in zip(prot, rep))
    r600 = float(np.mean(rep))
    r1500 = float(np.mean([run_register(s, 'repaired', ticks=HORIZON)['produced'] for s in FINAL_SEEDS]))
    steady = r1500 / r600
    return {
        'G1_resolvable': bool(res['p'] <= P_BAR and res['n'] >= MIN_N),
        'G2_effect': bool(float(np.median(d)) >= BAR),
        'G3_retention': bool(retention),
        'G4_repaired_stability': bool(dead_rep == 0),
        'G5_protected_stability': bool(dead_prot == 0),
        'G6_corruption_consequential': bool(dead_unrep >= 1),
        'G7_horizon_robust': bool(STEADY_LO <= steady <= STEADY_HI),
        'G8_determinism': None,
    }, res, d, steady, dead_unrep


def preflight(protocol='AC58_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac58_results_v1'):
    preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            row = individual(seed)
            rows.append(row)
            f.write(json.dumps(row) + '\n')
            f.flush()
            print(json.dumps(dict(seed=seed, protected=row['protected']['produced'],
                                  repaired=row['repaired']['produced'],
                                  unrepaired=row['unrepaired']['produced'],
                                  unrepaired_dead=row['unrepaired']['dead'])), flush=True)
    g, res, d, steady, dead_unrep = gates(rows)
    g['G8_determinism'] = all(individual(s) == r for s, r in zip(seeds[:2], rows[:2]))
    post = lambda arm: [r[arm]['produced'] for r in rows]
    summary = {arm: dict(min=min(post(arm)), mean=float(np.mean(post(arm))), max=max(post(arm)))
               for arm in ARMS}
    summary['resolvability'] = res
    summary['median_difference'] = float(np.median(d))
    summary['mean_difference'] = float(np.mean(d))
    summary['steady_state_ratio'] = steady
    summary['dead_unrepaired'] = dead_unrep
    (outdir / 'results.json').write_text(json.dumps(
        dict(bar=BAR, steady_lo=STEADY_LO, steady_hi=STEADY_HI, damage_rate=DAMAGE_RATE,
             repair_cost=REPAIR_COST, seeds=list(seeds), hashes=hashes, opt_b=list(OPT_B),
             gates=g, summary=summary, rows=rows), indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac58_order.py finals')
        print('Protocol: AC58_PROTOCOL_v1.md (final seeds 4848-4859)')
