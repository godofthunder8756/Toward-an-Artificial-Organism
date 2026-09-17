"""AC73 engineering: does a POPULATION-BASED self-directed learner close the local-optima gap?

Why this, now
-------------
The AC72 gap: the organism's rules are self-maintained but externally acquired. The prototype that
would close it is AC30's mutate-and-keep learner -- a search over the six-position order scored by the
organism's own production signal (sites retained). But AC30's single-climber captured only ~63% of the
world's margin (mean gap 1.83 of a 5.00 spread) because single-seed scoring makes it stop on a lucky
draw (local optima). AC32/AC33 fixed the *reliability* of that search with a 12-seed ORACLE score and
steepest ascent -- but that score is an external evaluator averaging 12 parallel worlds, which an
organism cannot do. The handoff's proposed next step is a POPULATION-BASED learner.

The question this measures, before any protocol
-----------------------------------------------
A population is the natural answer to *self-directed* noise: each member lives ONE life (one seed, one
800-tick run -- the organism's own realized outcome, no external oracle, no multi-seed averaging), and
selection over generations accumulates the signal that any single life lacks. Does that reach the level
the world permits, where AC30's single-climber stopped at 63%?

To separate two possible limits I measure BOTH:
  * mechanism limit  -- is the 63% cap just the single-climber's local optima? (population + oracle
                       scoring would then reach the ceiling like AC33's steepest ascent);
  * information limit -- is 63% the ceiling of *single-lifetime* evaluation no matter the mechanism?
                       (population + single-life scoring would then cap near 63% too).

If the population reaches the ceiling on SINGLE-life scoring, self-direction is sufficient and the next
study ports it into the organism. If it caps near 63%, the limit is the information in one lifetime,
not the search -- a different and harder reframing of "self-produced rules".

This is engineering. No protocol, no final seeds, no claim.
"""
import itertools
import json
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
SCORING = ac32.SCORING_SEEDS                       # 9000..9011 -- external 12-seed oracle, REPORTING only
CEILING_ORDER, CEILING = ac32.DECLARED_OPTIMA['B']  # (2,0,1,3,5,4), 12.67
WORST_SCORE = ac32.rating(tuple(range(6)), RATES_B)  # placeholder; replaced below
TICKS = acq.TICKS
TRIALS = tuple(range(8000, 8012))                  # engineering seeds, disjoint from every frozen family


def oracle_rating(order, seed=None):
    """External 12-seed score. REPORTING ONLY -- a self-directed learner never sees this.
    (Takes an ignored `seed` so it shares the score(m, seed) signature with single_life.)"""
    return ac32.rating(order, RATES_B, SCORING, TICKS)


def single_life(order, seed):
    """The organism's own realized outcome: one 800-tick life, one environmental seed."""
    return acq.run(order, seed, TICKS, rates=RATES_B)[0]


# ---- population learner -------------------------------------------------------

def order_crossover(a, b, rng):
    """Order crossover (OX) for permutations, preserving positions from each parent."""
    n = len(a)
    i, j = sorted(rng.integers(0, n + 1, 2))
    seg = list(a[i:j])
    taken = set(seg)
    tail = [x for x in b if x not in taken]      # b's order, minus the segment already placed
    child = tail[:i] + seg + tail[i:]            # tail wraps around the preserved segment
    assert len(child) == n and set(child) == set(range(n))
    return tuple(child)


def mutate(order, rng, swaps=1):
    o = list(order)
    for _ in range(swaps):
        i, j = rng.integers(0, len(o), 2)
        o[i], o[j] = o[j], o[i]
    return tuple(o)


def population_learn(seed, pop=16, gens=10, score=single_life, elite=2, tour=3):
    """A population of rules, each evaluated on its own single life (self-directed), evolved by
    tournament selection + order crossover + swap mutation. Returns the best member ever seen."""
    rng = np.random.default_rng([seed, 7301])
    members = [tuple(int(x) for x in rng.permutation(6)) for _ in range(pop)]
    best = members[0]; best_score = -1.0
    for _ in range(gens):
        fits = [score(m, seed) for m in members]
        for m, f in zip(members, fits):
            if f > best_score:
                best, best_score = m, f
        ranked = sorted(range(pop), key=lambda k: -fits[k])
        nxt = [members[ranked[0]], members[ranked[1]]]      # elitism
        while len(nxt) < pop:                                # tournament + crossover + mutation
            pool = rng.choice(pop, size=tour, replace=False)
            pa = members[max(pool, key=lambda k: fits[k])]
            pool = rng.choice(pop, size=tour, replace=False)
            pb = members[max(pool, key=lambda k: fits[k])]
            nxt.append(mutate(order_crossover(pa, pb, rng), rng))
        members = nxt
    fits = [score(m, seed) for m in members]
    k = int(np.argmax(fits))
    if fits[k] > best_score:
        best, best_score = members[k], fits[k]
    return best, best_score


def mutate_and_keep(seed, evals=160, score=single_life):
    """AC30's original single-climber (the 63% baseline), with the same evaluation budget."""
    rng = np.random.default_rng([seed, 3101])
    current = tuple(int(x) for x in rng.permutation(6))
    best = score(current, seed)
    for _ in range(evals):
        i, j = rng.integers(0, 6, 2)
        cand = list(current); cand[i], cand[j] = cand[j], cand[i]; cand = tuple(cand)
        s = score(cand, seed)
        if s >= best:
            current, best = cand, s
    return current, best


def report(trials=TRIALS):
    rows = {}
    # 1. AC30's single-climber, single-life scoring -- the 63% baseline
    mk = [mutate_and_keep(s, 160) for s in trials]
    mk_gap = [CEILING - oracle_rating(o) for o, _ in mk]
    rows['mutate_and_keep_single_life'] = dict(
        best_gap_min=float(min(mk_gap)), best_gap_mean=float(np.mean(mk_gap)),
        best_gap_max=float(max(mk_gap)), ceiling=CEILING)

    # 2. population, single-life scoring -- the proposed self-directed mechanism
    pop = [population_learn(s, pop=16, gens=10, score=single_life) for s in trials]
    pop_gap = [CEILING - oracle_rating(o) for o, _ in pop]
    rows['population_single_life'] = dict(
        best_gap_min=float(min(pop_gap)), best_gap_mean=float(np.mean(pop_gap)),
        best_gap_max=float(max(pop_gap)), ceiling=CEILING)

    # 3. population, oracle scoring, few trials -- INTERNAL CHECK ONLY. If this fails to reach the
    #    ceiling the population mechanism itself is broken (I know oracle+population should reach it,
    #    because AC33's steepest ascent already did with the same oracle). Guards arm 2 against a
    #    "mechanism bug" being misread as an "information limit".
    pop_o = [population_learn(s, pop=12, gens=8, score=oracle_rating) for s in trials[:4]]
    pop_o_gap = [CEILING - oracle_rating(o) for o, _ in pop_o]
    rows['population_oracle_check'] = dict(
        best_gap_min=float(min(pop_o_gap)), best_gap_mean=float(np.mean(pop_o_gap)),
        best_gap_max=float(max(pop_o_gap)), ceiling=CEILING)

    # 4. larger budget, single-life -- does more self-directed signal help?
    pop_big = [population_learn(s, pop=24, gens=20, score=single_life) for s in trials]
    pop_big_gap = [CEILING - oracle_rating(o) for o, _ in pop_big]
    rows['population_single_life_big'] = dict(
        best_gap_min=float(min(pop_big_gap)), best_gap_mean=float(np.mean(pop_big_gap)),
        best_gap_max=float(max(pop_big_gap)), ceiling=CEILING)

    # margin context from the declared optimum (AC32): ceiling 12.67, AC30's original spread 5.00
    rows['regime'] = dict(ceiling=CEILING, ceiling_order=list(CEILING_ORDER),
                          ac30_original_spread=5.00, note='AC30 spread measured in the original world')
    return rows


if __name__ == '__main__':
    import sys
    rows = report()
    print(json.dumps(rows, indent=2))
    for k, v in rows.items():
        if 'gap' in v:
            print(f'{k:32s}  gap-to-ceiling  min {v["best_gap_min"]:.2f}  '
                  f'mean {v["best_gap_mean"]:.2f}  max {v["best_gap_max"]:.2f}')
