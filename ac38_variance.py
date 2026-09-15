"""AC38: what noise does a PAIRED arm comparison actually face?

The problem this settles
-----------------------
Every endpoint study since AC32 has had to pass a pre-declared validity criterion: "margin/noise >= 10",
where the margin was the gap between two orders' ratings and the noise was the sd of a single order's
rating across disjoint seed sets. That criterion was declared for AC32 and inherited by AC35, AC36 and
AC37.

But every arm comparison in these studies is **paired**: all arms are scored on the SAME seed set. The
seed-set identity variance that `noise_of_order` measures therefore **cancels from the difference between
arms** -- it is a common offset, not a source of uncertainty about which arm is better. So the inherited
criterion measures the wrong quantity, and AC37 was stopped by it (ratio 7.16) while its arms looked
separated.

What is measured here
---------------------
For a pair of orders (or a pair of arms from a frozen study):

  * **marginal noise** sigma_marginal: sd of one order's rating across disjoint seed sets -- the AC32
    quantity;
  * **paired-difference noise** sigma_delta: sd of the DIFFERENCE `rating(A) - rating(B)` across the same
    sets, with both orders scored on the same set in each set;
  * the **variance-reduction factor** sigma_marginal / sigma_delta, which is what a paired design buys;
  * an exact **sign-flip test** on paired per-individual data: under the null that the arm labels carry
    no information, each individual's difference is equally likely to have either sign, so the observed
    mean difference can be compared against all 2^n sign assignments. This needs no distributional
    assumption and is the honest test for the design these studies actually use.

Applied to the frozen studies: AC33 and AC36 both passed their gates -- this computes the sign-flip
p-values for their key contrasts, as a check on results already recorded (post hoc, and labelled so).
Applied to AC37's engineering pair data, it says what the paired view would have said -- while AC37
stays stopped, because a criterion derived from data it would judge is not a criterion.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np
import ac30_acquire as acq

N_SIGN_FLIPS=1<<12      # exact enumeration up to 12 individuals


def marginal_and_paired(order_a,order_b,rating,rates,sets=8,prefix=9200,set_size=50):
    """Score both orders on the SAME disjoint seed sets, returning the per-set values and both sds."""
    a=[]; b=[]
    for k in range(sets):
        seeds=tuple(range(prefix+set_size*k,prefix+set_size*(k+1)))
        a.append(rating(order_a,rates,seeds))
        b.append(rating(order_b,rates,seeds))
    a=np.array(a); b=np.array(b); d=a-b
    return dict(a=a.tolist(),b=b.tolist(),delta=d.tolist(),
                sigma_marginal=float(np.std(a)),sigma_delta=float(np.std(d)),
                mean_delta=float(np.mean(d)),
                reduction=(float(np.std(a)/np.std(d)) if np.std(d)>0 else float('inf')))


def sign_flip_test(differences):
    """Exact paired sign-flip test. Returns the observed mean, the null distribution's spread, and the
    two-sided p-value over all sign assignments (exact for n <= 12, sampled above that)."""
    d=np.asarray(differences,dtype=float)
    n=len(d); observed=float(np.mean(d))
    if n<=12:
        means=[]
        for mask in range(1<<n):
            signs=np.array([1.0 if (mask>>i)&1 else -1.0 for i in range(n)])
            means.append(float(np.mean(d*signs)))
    else:
        rng=np.random.default_rng(0)
        means=[float(np.mean(d*rng.choice([-1.0,1.0],size=n))) for _ in range(200000)]
    means=np.array(means)
    p=float(np.mean(np.abs(means)>=abs(observed)-1e-12))
    return dict(observed=observed,null_sd=float(np.std(means)),p=p,n=n)


def frozens_rows(root):
    path=Path(root)/'rows.jsonl'
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def contrast(rows,arm_a,arm_b):
    diffs=[r[arm_a]['post']-r[arm_b]['post'] for r in rows]
    return sign_flip_test(diffs)


if __name__=='__main__':
    print(__doc__)
    import ac36_survival as ac36

    print('\n--- 1. what a paired design buys (AC36 world, two real orders) ---')
    o_good=(1,0,2,3,4,5)          # regime B optimum
    o_old=(4,5,1,2,0,3)           # regime A optimum
    m=marginal_and_paired(o_good,o_old,ac36.rating,ac36.RATES_B,sets=8)
    print(f'  per-set ratings of the good order: {[round(v,2) for v in m["a"]]}')
    print(f'  per-set differences (good - old):  {[round(v,2) for v in m["delta"]]}')
    print(f'  sigma_marginal {m["sigma_marginal"]:.3f}   sigma_delta {m["sigma_delta"]:.3f}   '
          f'reduction {m["reduction"]:.2f}x')
    print(f'  mean paired difference {m["mean_delta"]:.2f}')

    print('\n--- 2. sign-flip tests on the FROZEN studies (post hoc, labelled as such) ---')
    for root,arms,label in (('ac33_results_v1',('learner_both','no_release'),
                             'AC33 (ordering, passed all gates)'),
                            ('ac33_results_v1',('learner_both','no_search'),
                             'AC33 vs the state-blind control'),
                            ('ac36_results_v1',('learner_both','no_release'),
                             'AC36 (insufficient income, passed all gates)'),
                            ('ac36_results_v1',('learner_both','no_search'),
                             'AC36 vs the state-blind control'),
                            ('ac32_results_v1',('learner_both','no_release'),
                             'AC32 (G2 FAILED -- control)')):
        rows=frozens_rows(root)
        t=contrast(rows,arms[0],arms[1])
        flag='' if t['p']<=0.01 else '   <- not significant'
        print(f'  {label:44s} mean {t["observed"]:+.2f}  p {t["p"]:.4f}{flag}')

    print('\n--- 3. the paired view of AC37 (which stays STOPPED regardless) ---')
    t=sign_flip_test([5.08-2.58,5.92-1.75,7.67-1.75,6.33-2.58])
    print(f'  AC37 engineering, learner vs no_release (4 individuals): mean {t["observed"]:+.2f} '
          f'p {t["p"]:.4f}')
    print('  NOTE: this neither unstops AC37 nor is a criterion for it; a successor must declare its')
    print('  own threshold, derived from variance it does not then judge.')

    json.dump(dict(reduction=m['reduction'],sigma_marginal=m['sigma_marginal'],
                   sigma_delta=m['sigma_delta'],mean_delta=m['mean_delta'],
                   ac37_engineering=t),open('/tmp/ac38_variance.json','w'),indent=2)
