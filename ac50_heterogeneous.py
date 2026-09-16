"""AC50: stable graded self-sufficiency via regime-dependent heterogeneous site value. A frozen study.

The claim
---------
In a self-funded world with **regime-dependent heterogeneous site values**, after the stress regime
reverses, an organism that releases its stored order and re-acquires retains more production value over a
run than one that keeps its stale order -- **and it does so at a stable, steady-state equilibrium, not
during a collapse.**

Why this is the point (the line that got here)
----------------------------------------------
AC47/AC48 showed that under *homogeneous* sites the self-funded world cannot be both stable and graded:
the order's only lever (which site to renew) moves the outcome only under scarcity, and scarcity in
self-funding is the death regime, so the graded region is a transient of collapse. AC49 found the fix:
make sites **heterogeneous in value**, with value **regime-dependent** (region 0 most valuable under A,
region 5 under B, reversing with the stress). Then the order's renewal priority decides *which* sites
survive, and that becomes a persistent production difference at a stable equilibrium. The two properties
AC47/AC48 said were impossible -- stability (no death spiral) and horizon-robustness (steady state) --
are the gates that make this claim what it is.

Endpoint: cumulative value-weighted production under regime B (horizon-robust, like AC43's ledger
totals). Engineering (ac50_engineering.py) measured: p = 0.00098, 0/12 dead, production ratio 2.49 from
600 to 1500 ticks (linear steady state), median paired difference 1012 value-units.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac33_search as asc
import ac38_variance as ac38

# ---- economy and value structure (pinned before the protocol) ----
VALUES_A = (5.0, 4.0, 3.0, 2.0, 1.0, 0.5)
VALUES_B = tuple(reversed(VALUES_A))
STRESS_MULTIPLIER = 3
RATES_A = tuple(r * STRESS_MULTIPLIER for r in acq.stress_rates())
RATES_B = tuple(reversed(RATES_A))
PRODUCTION_PERIOD = 4
DRAIN = 2.0
RENEW_ENERGY = 5
STARVATION_TICKS = 60
BURST_PROBABILITY = 0.03
BURST_WIDTH = 3
TICKS = 600
HORIZON_TICKS = 1500

SCORING_SEEDS = tuple(range(9000, 9012))   # shared paired scoring set

ARMS = ('learner_both', 'no_release', 'no_search', 'preserve', 'oracle_a', 'oracle_b')

# Declared value-optimal orders (24-start climb on the 12 scoring seeds, before any final seed)
OPT_A = (2, 0, 1, 3, 4, 5)
OPT_B = (3, 2, 4, 5, 1, 0)
DECLARED_OPTIMA = {'A': OPT_A, 'B': OPT_B}

FINAL_SEEDS = tuple(range(4800, 4812))     # 12 individuals, disjoint from engineering 4600-4611
BAR = 500.0                                # median paired difference, value-units (engineering 1012)
P_BAR = 0.01
MIN_N = 8
STEADY_LO, STEADY_HI = 2.4, 2.6            # production@1500 / production@600 (linear = 2.50)
SOURCES = ['ac50_heterogeneous.py', 'ac33_search.py', 'ac30_acquire.py', 'ac29_register.py',
           'ac38_variance.py', 'AC50_PROTOCOL_v1.md']


class World:
    def __init__(self, seed, rates, values):
        self.rng = np.random.default_rng([seed, 3701])
        self.rates = rates
        self.values = values
        self.life = [acq.CHILD_LIFE] * acq.SLOTS
        self.energy = 48
        self.tick_count = 0
        self.starved = 0
        self.dead = False
        self.renewals = 0
        self.refusals = 0
        self.produced = 0.0

    def urgency(self):
        word = 0
        for k in range(acq.REGIONS):
            seg = self.life[k * acq.SITES:(k + 1) * acq.SITES]
            if any(0 < v <= acq.URGENT for v in seg):
                word |= 1 << k
        return word

    def _stress_one(self, k):
        seg = slice(k * acq.SITES, (k + 1) * acq.SITES)
        occupied = [i for i in range(acq.SITES) if self.life[seg.start + i] > 0]
        if occupied:
            i = occupied[int(self.rng.integers(0, len(occupied)))]
            self.life[seg.start + i] = acq.URGENT

    def environment_tick(self):
        for k, rate in enumerate(self.rates):
            if self.rng.random() < rate:
                self._stress_one(k)
        if self.rng.random() < BURST_PROBABILITY:
            weights = np.array(self.rates)
            weights = weights / weights.sum()
            for k in self.rng.choice(acq.REGIONS, size=BURST_WIDTH, replace=False, p=weights):
                self._stress_one(int(k))

    def tick(self, action):
        self.tick_count += 1
        for i in range(acq.SLOTS):
            if self.life[i] == 1:
                self.life[i] = 0
            elif self.life[i] > 1:
                self.life[i] -= 1
        if self.tick_count % PRODUCTION_PERIOD == 0:
            val = sum(self.values[k] * sum(1 for v in self.life[k * acq.SITES:(k + 1) * acq.SITES] if v >= 1)
                      for k in range(acq.REGIONS))
            self.energy += val
            self.produced += val
        self.energy -= DRAIN
        acted = False
        if action is not None:
            seg = slice(action * acq.SITES, (action + 1) * acq.SITES)
            live = [i for i in range(acq.SITES) if self.life[seg.start + i] > 0]
            if live and self.energy >= RENEW_ENERGY:
                most_urgent = min(live, key=lambda i: self.life[seg.start + i])
                self.energy -= RENEW_ENERGY
                self.life[seg.start + most_urgent] = acq.CHILD_LIFE
                self.renewals += 1
                acted = True
            elif live:
                self.refusals += 1
        self.starved = self.starved + 1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v > 0) < 1 or self.starved >= STARVATION_TICKS:
            self.dead = True


def run(order, seed, rates, values, ticks=TICKS):
    w = World(seed, rates, values)
    for _ in range(ticks):
        if w.dead:
            break
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
    return dict(produced=w.produced, dead=w.dead)


def rating(order, rates, values, seeds=SCORING_SEEDS, ticks=TICKS):
    out = [run(order, s, rates, values, ticks) for s in seeds]
    return float(np.mean([o['produced'] for o in out]))


def climb(start, rates, values, seeds=SCORING_SEEDS):
    current = tuple(start)
    score = rating(current, rates, values, seeds)
    while True:
        best = current
        bs = score
        for cand in asc.swaps(current):
            s = rating(cand, rates, values, seeds)
            if s > bs:
                best, bs = cand, s
        if best == current:
            return current, score
        current, score = best, bs


def search(rates, values, start):
    return climb(start, rates, values)


def hold(arm_name, seed, opt):
    start = tuple(int(x) for x in np.random.default_rng([seed, 3701]).permutation(6))
    if arm_name in ('learner_both', 'no_release'):
        stored, _ = search(RATES_A, VALUES_A, start)
    else:
        stored = start
    if arm_name == 'learner_both':
        r = reg.Register()
        r.write(reg.lehmer(start))
        stored, _ = search(RATES_B, VALUES_B, start)
    elif arm_name == 'oracle_a':
        stored = opt['A']
    elif arm_name == 'oracle_b':
        stored = opt['B']
    r = reg.Register()
    r.write(reg.lehmer(stored))
    held = r.read()
    assert held is not None, 'a written order must read back'
    return held


def individual(seed, opt):
    row = dict(seed=seed)
    for arm_name in ARMS:
        held = hold(arm_name, seed, opt)
        outs = [run(held, s, RATES_B, VALUES_B) for s in SCORING_SEEDS]
        post = float(np.mean([o['produced'] for o in outs]))
        dead = sum(1 for o in outs if o['dead'])
        row[arm_name] = dict(held=list(held), post=post, dead=dead)
    return row


def gates(rows):
    post = lambda arm: [r[arm]['post'] for r in rows]
    learner = post('learner_both')
    no_rel = post('no_release')
    d = np.asarray([a - b for a, b in zip(learner, no_rel)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    # horizon-robustness: learner at 1500 vs 600, aggregate over individuals
    l1500 = [rating(r['learner_both']['held'], RATES_B, VALUES_B, ticks=HORIZON_TICKS)
             for r in rows]
    l600 = learner
    steady = float(np.mean(l1500)) / float(np.mean(l600))
    dead = sum(r[a]['dead'] for r in rows for a in ARMS)
    return {
        'G1_resolvable': bool(res['p'] <= P_BAR and res['n'] >= MIN_N),
        'G2_median_effect_in_value_units': bool(float(np.median(d)) >= BAR),
        'G3_stability_no_death': bool(dead == 0),
        'G4_horizon_robust_steady_state': bool(STEADY_LO <= steady <= STEADY_HI),
        'G5_oracle_b_ceiling': bool(min(post('oracle_b')) >= min(learner)),
        'G6_state_blind_below_learner': bool(float(np.mean(post('no_search'))) < float(np.mean(learner))
                                             and float(np.mean(post('preserve'))) < float(np.mean(learner))),
        'G7_all_individuals_complete': bool(len(rows) == len(FINAL_SEEDS)
                                             and all(arm in r for r in rows for arm in ARMS)),
        'G8_determinism': None,
        'G9_register_in_the_loop': bool(all(len(r[arm]['held']) == 6 for r in rows for arm in ARMS)),
    }, res, d, steady, dead


def preflight(protocol='AC50_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but the protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac50_results_v1'):
    preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            row = individual(seed, DECLARED_OPTIMA)
            rows.append(row)
            f.write(json.dumps(row) + '\n')
            f.flush()
            print(json.dumps(dict(seed=seed,
                                  learner=row['learner_both']['post'],
                                  no_release=row['no_release']['post'],
                                  oracle_b=row['oracle_b']['post'])), flush=True)
    g, res, d, steady, dead = gates(rows)
    g['G8_determinism'] = all(individual(s, DECLARED_OPTIMA) == r
                              for s, r in zip(seeds[:2], rows[:2]))
    post = lambda arm: [r[arm]['post'] for r in rows]
    summary = {arm: dict(min=min(post(arm)), mean=float(np.mean(post(arm))), max=max(post(arm)))
               for arm in ARMS}
    summary['resolvability'] = res
    summary['median_difference'] = float(np.median(d))
    summary['steady_state_ratio'] = steady
    summary['dead'] = dead
    (outdir / 'results.json').write_text(json.dumps(
        dict(bar=BAR, steady_lo=STEADY_LO, steady_hi=STEADY_HI, seeds=list(seeds), hashes=hashes,
             optima={'A': list(OPT_A), 'B': list(OPT_B)}, gates=g, summary=summary, rows=rows),
        indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac50_heterogeneous.py finals')
        print('Protocol: AC50_PROTOCOL_v1.md (final seeds 4800-4811)')
