"""AC73 engineering addendum: does ACCUMULATED signal across environments lift the single-lifetime cap?

The first measurement (ac73_engineering.py) found the population does NOT beat the single-climber on
single-life scoring -- both cap ~0.85 sites below the ceiling, while oracle scoring reaches it. That
implicates the SIGNAL, not the SEARCH. But "self-directed" need not mean ONE lifetime: a long-lived
organism accumulates its production signal across many successive environments. Does that accumulation
let a self-directed population converge to the ceiling without any external oracle?

Model: a population of orders. Each generation the whole population lives in a NEW environment (new
seed); every member records its own realized sites-retained into a RUNNING MEAN over every environment
it has lived in. Selection (tournament + elitism + order crossover + swap mutation) acts on that
running mean. Elites carry their history; new children are born with none. If accumulated signal lifts
the cap, the running-mean-best order should approach the oracle ceiling as generations grow.

Engineering. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac73_engineering as e

def population_across_envs(seed, pop=16, gens=12):
    rng = np.random.default_rng([seed, 7302])
    members = [tuple(int(x) for x in rng.permutation(6)) for _ in range(pop)]
    sums = {m: 0.0 for m in members}
    cnt = {m: 0 for m in members}
    for g in range(gens):
        env = seed + g
        for m in members:
            sums[m] += e.single_life(m, env)
            cnt[m] += 1
        mean = {m: sums[m] / cnt[m] for m in members}
        ranked = sorted(members, key=lambda m: -mean[m])
        nxt = [ranked[0], ranked[1]]
        while len(nxt) < pop:
            def tour():
                k = int(rng.integers(0, pop, 3).max())  # 3-way tournament on the CURRENT members
                return members[k]
            pa, pb = tour(), tour()
            child = e.mutate(e.order_crossover(pa, pb, rng), rng)
            nxt.append(child)
            sums[child] = 0.0
            cnt[child] = 0
        members = nxt
    # best by running mean (members born in the final generation have no history -- exclude them);
    # report ITS oracle rating (external, honest comparison)
    scored = [m for m in members if cnt[m] > 0]
    best = max(scored, key=lambda m: sums[m] / cnt[m])
    return best, sums[best] / cnt[best]

if __name__ == '__main__':
    trials = e.TRIALS
    gaps = []
    for s in trials:
        best, mean = population_across_envs(s)
        gap = e.CEILING - e.oracle_rating(best)
        gaps.append(gap)
    print(f'across-environments population (12 gens, running-mean selection):')
    print(f'  gap-to-ceiling  min {min(gaps):.2f}  mean {np.mean(gaps):.2f}  max {max(gaps):.2f}')
    print(f'  (single-life population was: min 0.25 mean 0.84 max 1.67; oracle population: mean 0.09)')
