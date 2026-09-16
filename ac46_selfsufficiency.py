"""AC46: self-sufficiency -- the AC37 world, re-examined with the correct paired test. A frozen study.

The claim
---------
In a **self-funded** world -- the organism's own productive sites supply its energy, and a constant
metabolic drain sets a population floor -- after the stress regime changes so a different order is best,
an organism that can release its stored order and search again retains more population than one that
cannot.

The world (unchanged from AC37, whose constants were settled by its own scan)
-----------------------------------------------------------------------------
Production period 4, drain 3. The energy balance is

    E' = E + (productive sites)/4 - 3 - 5 * renewals

so self-sufficiency requires `productive sites > 12`: a population floor set by the economy, not by
carrying capacity. This is the fix AC35 lacked -- a constant drain that does not scale with the
organism's own state, so the negative feedback that equalized AC35's outcomes is absent.

Why AC37 stopped, and why that stop is now re-examined
------------------------------------------------------
AC37 stopped on an inherited criterion -- "margin/noise >= 10" -- that measures the *marginal* noise
(sd of one order's rating across disjoint seed sets). AC38 then showed that a paired arm comparison does
not face that variance: every arm is scored on the same seed set, so the seed-set identity variance
cancels in the difference, and the honest test is the exact sign-flip test on the paired per-individual
differences. AC37's own document required this before any successor: "a successor must justify its own
threshold from the variance that actually limits a paired comparison ... before its seeds." AC38 is that
justification.

Engineering re-examination (recorded in AC46_ENGINEERING_v1.md, seeds 4600-4611, before this protocol):
the learner-vs-no_release paired differences resolve at p = 0.00049 (the 2/2^12 floor), 12 of 12
individuals impaired, learner worst 5.00 > no_release best 2.50. The AC37 stop was a criterion artifact.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac33_search as asc
import ac38_variance as ac38

# ---- the economy, pinned from AC37's scan before this protocol was written ----
PRODUCTION_PERIOD = 4
DRAIN = 3
RENEW_ENERGY = 5
STARVATION_TICKS = 60
TICKS = 600
STRESS_MULTIPLIER = 3
BURST_PROBABILITY = 0.03
BURST_WIDTH = 3
RATES_A = tuple(r * STRESS_MULTIPLIER for r in acq.stress_rates())
RATES_B = tuple(reversed(RATES_A))

SCORING_SEEDS = tuple(range(9000, 9012))   # the shared paired scoring set (12 seeds)

ARMS = ('learner_both', 'no_release', 'no_search', 'preserve', 'oracle_a', 'oracle_b')

# Declared optima, from AC37's full 720-order sweep at 600 ticks on the paired scoring seeds
# (recorded in AC37_ENGINEERING_v1.md): regime A optimum (4,5,1,2,0,3)=7.75, regime B optimum
# (0,4,1,3,2,5)=7.67. Used only for the oracle arms.
DECLARED_OPTIMA = {'A': ((4, 5, 1, 2, 0, 3), 7.75), 'B': ((0, 4, 1, 3, 2, 5), 7.67)}

FINAL_SEEDS = tuple(range(4700, 4712))     # 12 individuals, fresh and disjoint from engineering 4600-4611
BAR = 4.0                                   # separation bar, between learner worst (5.00) and
                                            # no_release best (2.50) on engineering seeds
MEDIAN_BAR = 3.0                            # effect size in sites; engineering median 4.5
P_BAR = 0.01
MIN_N = 8
SOURCES = ['ac46_selfsufficiency.py', 'ac33_search.py', 'ac30_acquire.py', 'ac29_register.py',
           'ac38_variance.py', 'AC46_PROTOCOL_v1.md']


class World:
    def __init__(self, seed, rates=None):
        self.rng = np.random.default_rng([seed, 3701])
        self.rates = rates if rates is not None else RATES_A
        self.life = [acq.CHILD_LIFE] * acq.SLOTS
        self.energy = 48
        self.tick_count = 0
        self.starved = 0
        self.dead = False
        self.renewals = 0
        self.refusals = 0
        self.produced = 0
        self.drained = 0

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
            productive = sum(1 for v in self.life if v >= 1)
            self.energy += productive
            self.produced += productive
        self.energy -= DRAIN
        self.drained += DRAIN
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


def run(order, seed, ticks=TICKS, rates=None):
    w = World(seed, rates=rates)
    for _ in range(ticks):
        if w.dead:
            break
        word = w.urgency()
        action = None
        for position in order:
            if word >> position & 1:
                action = position
                break
        w.tick(action)
    return dict(sites=sum(1 for v in w.life if v > 0), dead=w.dead, renewals=w.renewals,
                refusals=w.refusals, produced=w.produced, drained=w.drained)


def rating(order, rates, seeds=SCORING_SEEDS, ticks=TICKS):
    return float(np.mean([run(order, s, ticks, rates=rates)['sites'] for s in seeds]))


def climb(start, neighbourhood=asc.swaps, rates=RATES_A):
    current = tuple(start)
    score = rating(current, rates)
    steps = 0
    while True:
        best = current
        best_score = score
        for cand in neighbourhood(current):
            s = rating(cand, rates)
            if s > best_score:
                best, best_score = cand, s
        if best == current:
            return current, score, steps
        current, score = best, best_score
        steps += 1


def search(rates, start):
    order, score, _ = climb(start, asc.swaps, rates)
    return order, score


def hold(arm_name, seed, opt):
    start = tuple(int(x) for x in np.random.default_rng([seed, 3701]).permutation(6))
    if arm_name in ('learner_both', 'no_release'):
        stored, _ = search(RATES_A, start)
    else:
        stored = start
    if arm_name == 'learner_both':
        r = reg.Register()
        r.write(reg.lehmer(start))          # release: overwrite the store
        stored, _ = search(RATES_B, start)   # then re-acquire under B
    elif arm_name == 'oracle_a':
        stored = opt['A'][0]
    elif arm_name == 'oracle_b':
        stored = opt['B'][0]
    r = reg.Register()
    r.write(reg.lehmer(stored))
    held = r.read()
    assert held is not None, 'a written order must read back'
    return held


def individual(seed, opt):
    row = dict(seed=seed)
    for arm_name in ARMS:
        held = hold(arm_name, seed, opt)
        row[arm_name] = dict(held=list(held), post=rating(held, RATES_B))
    return row


def gates(rows):
    post = lambda arm: [r[arm]['post'] for r in rows]
    learner = post('learner_both')
    no_rel = post('no_release')
    d = np.asarray([a - b for a, b in zip(learner, no_rel)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    return {
        'G1_resolvable': bool(res['p'] <= P_BAR and res['n'] >= MIN_N),
        'G2_median_effect_in_sites': bool(float(np.median(d)) >= MEDIAN_BAR),
        'G3_separation_of_minima': bool(min(learner) >= BAR and max(no_rel) < BAR),
        'G4_oracle_b_ceiling_above_bar': bool(min(post('oracle_b')) >= BAR),
        'G5_oracle_a_floor_below_bar': bool(max(post('oracle_a')) < BAR),
        'G6_state_blind_means_below_bar': bool(float(np.mean(post('no_search'))) < BAR
                                               and float(np.mean(post('preserve'))) < BAR),
        'G7_all_individuals_complete': bool(len(rows) == len(FINAL_SEEDS)
                                             and all(arm in r for r in rows for arm in ARMS)),
        'G8_determinism': None,
        'G9_register_in_the_loop': bool(all(len(r[arm]['held']) == 6 for r in rows for arm in ARMS)),
    }, res, d


def preflight(protocol='AC46_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but the protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac46_results_v1'):
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
                                  no_search=row['no_search']['post'],
                                  oracle_b=row['oracle_b']['post'])), flush=True)
    g, res, d = gates(rows)
    g['G8_determinism'] = all(individual(s, DECLARED_OPTIMA) == r
                              for s, r in zip(seeds[:2], rows[:2]))
    post = lambda arm: [r[arm]['post'] for r in rows]
    summary = {arm: dict(min=min(post(arm)), mean=float(np.mean(post(arm))), max=max(post(arm)))
               for arm in ARMS}
    summary['resolvability'] = res
    summary['median_difference'] = float(np.median(d))
    summary['impaired_fraction'] = float(np.mean(d > 0))
    (outdir / 'results.json').write_text(json.dumps(
        dict(bar=BAR, median_bar=MEDIAN_BAR, seeds=list(seeds), hashes=hashes,
             gates=g, summary=summary, rows=rows), indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac46_selfsufficiency.py finals')
        print('Protocol: AC46_PROTOCOL_v1.md (final seeds 4700-4711, BAR=4.0)')
