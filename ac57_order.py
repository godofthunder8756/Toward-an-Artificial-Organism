"""AC57: the six-region order is load-bearing AND re-acquirable. A frozen study.

The claim (AC57_PROTOCOL_v1.md): in the scaled body with a concentrated head + graded tail value
structure, the six-position order is (1) load-bearing -- the value-optimal order produces far more value
than the value-worst order -- and (2) re-acquirable -- an organism that releases and re-searches after a
regime A->B change produces far more value than one that keeps its stale order. This resolves the AC56
tension: concentrated value gave load-bearing but no re-acquisition; graded value the reverse; the
partial spread gives both.

World: AC50's verified `World`, regime B for scoring, with the declared orders from engineering.
Arms: optimal, worst, learner (seeded re-search + register), no_release (stale), random.

Final seeds 4836-4847, disjoint from engineering 4612-4635 and scoring 9012-9023.
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
VALUES_A = (100.0, 5.0, 4.0, 3.0, 2.0, 0.5)
VALUES_B = tuple(reversed(VALUES_A))
RATES_A = tuple(r * STRESS_MULT for r in acq.stress_rates())
RATES_B = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))
TICKS = a50.TICKS
HORIZON = a50.HORIZON_TICKS
PERIOD = a50.PRODUCTION_PERIOD

OPT_A = (2, 3, 4, 0, 1, 5)
OPT_B = (5, 1, 2, 4, 3, 0)
WORST_B = (2, 4, 1, 0, 3, 5)

SCORING = tuple(range(9012, 9024))
FINAL_SEEDS = tuple(range(4836, 4848))
CEILING = 4.0 * sum(VALUES_B) * (TICKS / PERIOD)      # 68700
BAR = 6000.0
P_BAR = 0.01
MIN_N = 8
STEADY_LO, STEADY_HI = 2.4, 2.6
HEADROOM_FRAC = 0.9

ARMS = ('optimal', 'worst', 'learner', 'no_release', 'random')
SOURCES = ['ac57_order.py', 'ac57_engineering.py', 'ac50_heterogeneous.py', 'ac33_search.py',
           'ac30_acquire.py', 'ac29_register.py', 'ac38_variance.py', 'AC57_PROTOCOL_v1.md']


def climb(rates, values, start, seeds=SCORING):
    cur = tuple(start)
    sc = a50.rating(cur, rates, values, seeds=seeds)
    while True:
        best, bs = cur, sc
        for cand in a50.asc.swaps(cur):
            s = a50.rating(cand, rates, values, seeds=seeds)
            if s > bs:
                best, bs = cand, s
        if best == cur:
            return cur
        cur, sc = best, bs


def learner_search(seed):
    """Release and re-search under regime B from a seeded start, then hold in a register."""
    start = tuple(int(x) for x in np.random.default_rng([seed, 5704]).permutation(6))
    found = climb(RATES_B, VALUES_B, start)
    r = reg.Register()
    r.write(reg.lehmer(found))
    held = r.read()
    return held


def random_order(seed):
    return tuple(int(x) for x in np.random.default_rng([seed, 5705]).permutation(6))


def individual(seed):
    return dict(
        seed=seed,
        optimal=a50.run(OPT_B, seed, RATES_B, VALUES_B),
        worst=a50.run(WORST_B, seed, RATES_B, VALUES_B),
        learner=a50.run(learner_search(seed), seed, RATES_B, VALUES_B),
        no_release=a50.run(OPT_A, seed, RATES_B, VALUES_B),
        random=a50.run(random_order(seed), seed, RATES_B, VALUES_B),
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
    o1500 = float(np.mean([a50.run(OPT_B, s, RATES_B, VALUES_B, ticks=HORIZON)['produced'] for s in FINAL_SEEDS]))
    steady = o1500 / o600
    register_ok = all(tuple(r['learner_order']) == reg.unlehmer(reg.lehmer(r['learner_order']))
                      for r in rows)
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


def preflight(protocol='AC57_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac57_results_v1'):
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
        dict(bar=BAR, steady_lo=STEADY_LO, steady_hi=STEADY_HI, ceiling=CEILING,
             headroom_frac=HEADROOM_FRAC, values_a=list(VALUES_A), values_b=list(VALUES_B),
             stress_mult=STRESS_MULT, seeds=list(seeds), hashes=hashes,
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
        print('Run the declared finals with: .venv/bin/python -B ac57_order.py finals')
        print('Protocol: AC57_PROTOCOL_v1.md (final seeds 4836-4847)')
