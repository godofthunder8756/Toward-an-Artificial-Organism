"""AC55: the six-region order is load-bearing (concentrated value). A frozen study.

The claim (AC55_PROTOCOL_v1.md): in the scaled body with one critical region worth ~100x the rest and
a stress multiplier of 7, the value-optimal order produces significantly more value than the value-worst
order, at a stable equilibrium, resolvable across two independent engineering seed families. This is the
foundation the developmental-function arc lacked: the 9.49-bit order structure is dynamically
consequential.

World: AC50's verified `World` mechanics, regime B, concentrated values. Arms: optimal, worst, random.
Endpoint: cumulative value-weighted production over 600 ticks.

Final seeds 4824-4835, disjoint from engineering 4612-4635 and scoring 9012-9023.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac50_heterogeneous as a50
import ac38_variance as ac38

VALUES = (1.0, 1.0, 1.0, 1.0, 1.0, 100.0)
STRESS_MULT = 7
RATES = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))
TICKS = a50.TICKS
HORIZON = a50.HORIZON_TICKS
PERIOD = a50.PRODUCTION_PERIOD

OPT = (1, 2, 0, 5, 3, 4)
WORST = (2, 4, 1, 0, 3, 5)

FINAL_SEEDS = tuple(range(4824, 4836))
CEILING = 4.0 * sum(VALUES) * (TICKS / PERIOD)      # all 24 sites alive every tick = 63000
BAR = 5000.0
P_BAR = 0.01
MIN_N = 8
STEADY_LO, STEADY_HI = 2.4, 2.6
HEADROOM_FRAC = 0.9

ARMS = ('optimal', 'worst', 'random')
SOURCES = ['ac55_order.py', 'ac55_engineering.py', 'ac50_heterogeneous.py', 'ac33_search.py',
           'ac30_acquire.py', 'ac38_variance.py', 'AC55_PROTOCOL_v1.md']


def random_order(seed):
    return tuple(int(x) for x in np.random.default_rng([seed, 5502]).permutation(6))


def individual(seed):
    rand = random_order(seed)
    return dict(
        seed=seed,
        optimal=a50.run(OPT, seed, RATES, VALUES),
        worst=a50.run(WORST, seed, RATES, VALUES),
        random=a50.run(rand, seed, RATES, VALUES),
        random_order=list(rand),
    )


def gates(rows):
    post = lambda arm: [r[arm]['produced'] for r in rows]
    opt = post('optimal')
    wst = post('worst')
    rnd = post('random')
    d = np.asarray([a - b for a, b in zip(opt, wst)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(r[a]['dead'] for r in rows for a in ARMS)
    o600 = float(np.mean(opt))
    o1500 = float(np.mean([a50.run(OPT, s, RATES, VALUES, ticks=HORIZON)['produced'] for s in FINAL_SEEDS]))
    steady = o1500 / o600
    impaired = sum(1 for a, b in zip(opt, wst) if b > a)
    return {
        'G1_resolvable': bool(res['p'] <= P_BAR and res['n'] >= MIN_N),
        'G2_median_effect': bool(float(np.median(d)) >= BAR),
        'G3_stability_no_death': bool(dead == 0),
        'G4_horizon_robust': bool(STEADY_LO <= steady <= STEADY_HI),
        'G5_state_blind': bool(float(np.mean(rnd)) < float(np.mean(opt))),
        'G6_headroom': bool(float(np.mean(wst)) <= HEADROOM_FRAC * CEILING),
        'G7_complete': bool(len(rows) == len(FINAL_SEEDS) and all(a in r for r in rows for a in ARMS)),
        'G8_determinism': None,
    }, res, d, steady, dead, impaired


def preflight(protocol='AC55_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac55_results_v1'):
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
            print(json.dumps(dict(seed=seed, optimal=row['optimal']['produced'],
                                  worst=row['worst']['produced'],
                                  random=row['random']['produced'])), flush=True)
    g, res, d, steady, dead, impaired = gates(rows)
    g['G8_determinism'] = all(individual(s) == r for s, r in zip(seeds[:2], rows[:2]))
    post = lambda arm: [r[arm]['produced'] for r in rows]
    summary = {arm: dict(min=min(post(arm)), mean=float(np.mean(post(arm))), max=max(post(arm)))
               for arm in ARMS}
    summary['resolvability'] = res
    summary['median_difference'] = float(np.median(d))
    summary['mean_difference'] = float(np.mean(d))
    summary['steady_state_ratio'] = steady
    summary['dead'] = dead
    summary['impaired'] = impaired
    (outdir / 'results.json').write_text(json.dumps(
        dict(bar=BAR, steady_lo=STEADY_LO, steady_hi=STEADY_HI, ceiling=CEILING,
             headroom_frac=HEADROOM_FRAC, values=list(VALUES), stress_mult=STRESS_MULT,
             seeds=list(seeds), hashes=hashes, opt=list(OPT), worst=list(WORST),
             gates=g, summary=summary, rows=rows), indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac55_order.py finals')
        print('Protocol: AC55_PROTOCOL_v1.md (final seeds 4824-4835)')
