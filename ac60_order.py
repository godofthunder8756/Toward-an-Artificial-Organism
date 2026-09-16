"""AC60: the developmental function scales -- a seven-region order is load-bearing and re-acquirable.

The claim (AC60_PROTOCOL_v1.md): in a seven-region scaled body, the order is still load-bearing and
re-acquirable -- the properties AC55/AC57 froze at six positions survive a wider domain (5040 orders,
12.30 bits). World: `ac60_engineering.World7`. Arms: optimal, worst, learner, no_release, random.

Final seeds 4860-4871, disjoint from engineering 4612-4635 and scoring 9012-9023.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac60_engineering as a60
import ac38_variance as ac38

N = a60.N
OPT_A = (2, 4, 3, 0, 1, 5, 6)
OPT_B = (2, 6, 3, 4, 5, 1, 0)
WORST_B = (5, 4, 0, 3, 2, 1, 6)

SCORING = tuple(range(9012, 9024))
FINAL_SEEDS = tuple(range(4860, 4872))
CEILING = 4.0 * sum(a60.VALUES_B) * (a60.TICKS / a60.PRODUCTION_PERIOD)   # 72300
BAR = 10000.0
P_BAR = 0.01
MIN_N = 8
STEADY_LO, STEADY_HI = 2.4, 2.6
HEADROOM_FRAC = 0.9

ARMS = ('optimal', 'worst', 'learner', 'no_release', 'random')
SOURCES = ['ac60_order.py', 'ac60_engineering.py', 'ac38_variance.py', 'AC60_PROTOCOL_v1.md']


def lehmer7(order):
    items = list(range(N)); code = 0
    for position, item in enumerate(order):
        index = items.index(item); code = code * (N - position) + index; items.pop(index)
    return code


def unlehmer7(code):
    if not 0 <= code < 5040:
        return None
    digits = [0] * N
    for position in range(N - 1, -1, -1):
        radix = N - position
        digits[position] = code % radix; code //= radix
    items = list(range(N))
    return tuple(items.pop(digits[position]) for position in range(N))


def learner_search(seed):
    start = tuple(int(x) for x in np.random.default_rng([seed, 6003]).permutation(N))
    found, _ = a60.climb(a60.RATES_B, a60.VALUES_B, start)
    return unlehmer7(lehmer7(found))   # round-trip through the register


def random_order(seed):
    return tuple(int(x) for x in np.random.default_rng([seed, 6004]).permutation(N))


def individual(seed):
    return dict(
        seed=seed,
        optimal=a60.run(OPT_B, seed, a60.RATES_B, a60.VALUES_B),
        worst=a60.run(WORST_B, seed, a60.RATES_B, a60.VALUES_B),
        learner=a60.run(learner_search(seed), seed, a60.RATES_B, a60.VALUES_B),
        no_release=a60.run(OPT_A, seed, a60.RATES_B, a60.VALUES_B),
        random=a60.run(random_order(seed), seed, a60.RATES_B, a60.VALUES_B),
        learner_order=list(learner_search(seed)),
    )


def gates(rows):
    post = lambda arm: [r[arm]['produced'] for r in rows]
    opt = post('optimal'); wst = post('worst')
    lrn = post('learner'); nrl = post('no_release'); rnd = post('random')
    d_load = np.asarray([a - b for a, b in zip(opt, wst)], dtype=float)
    d_re = np.asarray([a - b for a, b in zip(lrn, nrl)], dtype=float)
    res_load = ac38.sign_flip_test(list(d_load))
    res_re = ac38.sign_flip_test(list(d_re))
    dead = sum(r[a]['dead'] for r in rows for a in ARMS)
    o600 = float(np.mean(opt))
    o1500 = float(np.mean([a60.run(OPT_B, s, a60.RATES_B, a60.VALUES_B, ticks=a60.HORIZON_TICKS)['produced']
                           for s in FINAL_SEEDS]))
    steady = o1500 / o600
    register_ok = all(unlehmer7(lehmer7(r['learner_order'])) == tuple(r['learner_order']) for r in rows)
    return {
        'G1_load_resolvable': bool(res_load['p'] <= P_BAR and res_load['n'] >= MIN_N),
        'G2_load_effect': bool(float(np.median(d_load)) >= BAR),
        'G3_reacq_resolvable': bool(res_re['p'] <= P_BAR and res_re['n'] >= MIN_N),
        'G4_reacq_effect': bool(float(np.median(d_re)) >= BAR),
        'G5_stability_no_death': bool(dead == 0),
        'G6_horizon_robust': bool(STEADY_LO <= steady <= STEADY_HI),
        'G7_state_blind': bool(float(np.mean(rnd)) < float(np.mean(opt))),
        'G8_headroom': bool(float(np.mean(wst)) <= HEADROOM_FRAC * CEILING),
        'G9_register_in_loop': bool(register_ok),
        'G10_determinism': None,
    }, res_load, res_re, d_load, d_re, steady, dead


def preflight(protocol='AC60_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac60_results_v1'):
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
                                  learner=row['learner']['produced'],
                                  no_release=row['no_release']['produced'])), flush=True)
    g, res_load, res_re, d_load, d_re, steady, dead = gates(rows)
    g['G10_determinism'] = all(individual(s) == r for s, r in zip(seeds[:2], rows[:2]))
    post = lambda arm: [r[arm]['produced'] for r in rows]
    summary = {arm: dict(min=min(post(arm)), mean=float(np.mean(post(arm))), max=max(post(arm)))
               for arm in ARMS}
    summary['load_resolvability'] = res_load
    summary['reacq_resolvability'] = res_re
    summary['load_median'] = float(np.median(d_load))
    summary['reacq_median'] = float(np.median(d_re))
    summary['steady_state_ratio'] = steady
    summary['dead'] = dead
    (outdir / 'results.json').write_text(json.dumps(
        dict(bar=BAR, steady_lo=STEADY_LO, steady_hi=STEADY_HI, ceiling=CEILING, n=N,
             values_a=list(a60.VALUES_A), values_b=list(a60.VALUES_B), seeds=list(seeds), hashes=hashes,
             opt_a=list(OPT_A), opt_b=list(OPT_B), worst_b=list(WORST_B),
             gates=g, summary=summary, rows=rows), indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac60_order.py finals')
        print('Protocol: AC60_PROTOCOL_v1.md (final seeds 4860-4871)')
