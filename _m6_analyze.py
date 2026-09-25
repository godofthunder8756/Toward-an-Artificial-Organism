import json, numpy as np
from math import comb
from pathlib import Path

FINALS = 'ac117_results_v1'
POST = 8288

rows = [json.loads(l) for l in Path(f'{FINALS}/rows.jsonl').read_text().splitlines()]
print(f'loaded {len(rows)} rows')

def auc(score, truth):
    score = np.asarray(score, dtype=float); truth = np.asarray(truth, dtype=bool)
    n_pos = int(truth.sum()); n_neg = int((~truth).sum())
    if n_pos == 0 or n_neg == 0:
        return float('nan')
    order = np.argsort(score, kind='stable')
    s = score[order]; t = truth[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        ranks[i:j] = (i + 1 + j) / 2.0
        i = j
    rank_sum_pos = ranks[t].sum()
    return (rank_sum_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)

def brier(p, truth):
    p = np.asarray(p, dtype=float); truth = np.asarray(truth, dtype=float)
    return float(np.mean((p - truth) ** 2))

def ece(score, truth, nbins=4):
    score = np.asarray(score, dtype=float); truth = np.asarray(truth, dtype=float)
    bins = np.linspace(0, 1, nbins + 1)
    err = 0.0; n = len(truth)
    for i in range(nbins):
        mask = (score >= bins[i]) & (score <= bins[i + 1])
        if mask.sum() == 0:
            continue
        err += (mask.sum() / n) * abs(np.mean(score[mask]) - np.mean(truth[mask]))
    return err

def readouts(series, history_threshold=2):
    """Recompute the four readouts from an h1 series (list of 7-tuples)."""
    t = np.array([x[0] for x in series])
    ones = np.array([x[1] for x in series])
    last_write = np.array([x[2] for x in series])
    ob2 = np.array([x[3] for x in series]).astype(bool)
    risk = np.array([x[4] for x in series]).astype(bool)
    wrong = np.array([x[5] for x in series]).astype(bool)
    mon_unrel = (last_write == 0) & ((ones >= 4) | risk)
    mon_r = np.where(last_write == 1, 0, np.where(risk, 3, np.minimum(3, ones)))
    ref_unrel = ob2
    dir_unrel = (ones >= 4)
    hist_unrel = np.zeros_like(ob2, dtype=bool)
    ctr = 0
    for i, ob in enumerate(ob2):
        if ob:
            ctr += 1
        if ctr >= history_threshold:
            hist_unrel[i] = True
            ctr = 0
    return dict(
        t=t, wrong=wrong,
        monitor=dict(unrel=mon_unrel, score=mon_r),
        reflex=dict(unrel=ref_unrel, score=ref_unrel.astype(int)),
        direct=dict(unrel=dir_unrel, score=dir_unrel.astype(int)),
        history=dict(unrel=hist_unrel, score=hist_unrel.astype(int)),
    )

# ---- H1: pooled readout-truth series on the fixed_duty cut trajectory ----
fd_cut = [r for r in rows if r['arm'] == 'fixed_duty' and r['condition'] == 'cut']
print(f'fixed_duty cut rows with h1: {len(fd_cut)}')

pooled = {k: dict(unrel=[], score=[], wrong=[]) for k in ('monitor', 'reflex', 'direct', 'history')}
case1 = case3 = case4 = n_post = 0
for r in fd_cut:
    rd = readouts(r['h1_series'])
    pw = rd['t'] >= POST
    n_post += int(pw.sum())
    ones = np.array([x[1] for x in r['h1_series']]); lw = np.array([x[2] for x in r['h1_series']])
    ob2 = np.array([x[3] for x in r['h1_series']]).astype(bool)
    risk = np.array([x[4] for x in r['h1_series']]).astype(bool)
    case1 += int(((ones == 3) & (lw == 0))[pw].sum())
    case3 += int(((ones >= 4) & (~ob2) & (lw == 0))[pw].sum())
    case4 += int(((ones <= 3) & risk & (lw == 0))[pw].sum())
    for k in pooled:
        pooled[k]['unrel'].append(rd[k]['unrel'][pw])
        pooled[k]['score'].append(rd[k]['score'][pw])
        pooled[k]['wrong'].append(rd['wrong'][pw])

wrong_all = np.concatenate(pooled['monitor']['wrong'])
print(f'post-window ticks: {n_post}, wrong fraction: {wrong_all.mean():.4f}')
print(f'case1 (ones=3): {case1}  case3 (ones>=4, obs2 silent): {case3}  case4 (risk, ones<=3): {case4}')

print('\n--- H1 metrics (post-window, pooled) ---')
for k in ('monitor', 'reflex', 'direct', 'history'):
    score = np.concatenate(pooled[k]['score']).astype(float)
    unrel = np.concatenate(pooled[k]['unrel']).astype(bool)
    wrong = np.concatenate(pooled[k]['wrong'])
    if k == 'monitor':
        score = score / 3.0   # graded r/3 as P(wrong)
    a = auc(score, wrong)
    b = brier(score, wrong)
    e = ece(score, wrong)
    tp = int((unrel & wrong).sum()); fp = int((unrel & ~wrong).sum())
    fn = int((~unrel & wrong).sum()); tn = int((~unrel & ~wrong).sum())
    far = fp / (fp + tn) if (fp + tn) else float('nan')
    miss = fn / (fn + tp) if (fn + tp) else float('nan')
    print(f'  {k:9s}: AUC={a:.4f}  Brier={b:.4f}  ECE={e:.4f}  mean={score.mean():.3f}')
    print(f'          2x2: TP={tp} FP={fp} FN={fn} TN={tn}  false-alarm={far:.3f} miss={miss:.3f}')

# ---- H2: monitor vs rivals (cut) ----
print('\n--- H2: monitor vs rivals (cut) ---')
by = {}
for r in rows:
    if r['condition'] == 'cut':
        by[(r['seed'], r['history'], r['arm'])] = r
arms = ['monitor', 'fixed_duty', 'reflex', 'direct', 'history']
seeds = sorted(set(r['seed'] for r in rows))

def per_seed(metric):
    return {a: [by[(s, h, a)][metric] for s in seeds for h in (0, 1)] for a in arms}

for metric in ('bel_wrong_ever', 'erepair_writes', 'income_post', 'route1_retention'):
    ps = per_seed(metric)
    print(f'\n  {metric}:')
    for a in arms:
        print(f'    {a:11s}: mean={np.mean(ps[a]):10.2f}  per-seed={[round(x,1) for x in ps[a]]}')

def sign_flip(diffs, better_when_positive):
    d = np.array([x for x in diffs if x != 0])
    n = len(d)
    if n == 0:
        return 0.0, 0, (0, 0)
    npos = int((d > 0).sum()); nneg = int((d < 0).sum())
    k = npos if better_when_positive else nneg
    p = 2 * sum(comb(n, i) for i in range(k, n + 1)) / (2 ** n)
    return p, n, (npos, nneg)

print('\n--- sign-flip tests (per-seed differences) ---')
for rival in ('fixed_duty', 'reflex', 'direct', 'history'):
    m_w = per_seed('bel_wrong_ever')['monitor']; r_w = per_seed('bel_wrong_ever')[rival]
    p, n, s = sign_flip([m - r for m, r in zip(m_w, r_w)], better_when_positive=False)
    m_i = per_seed('income_post')['monitor']; r_i = per_seed('income_post')[rival]
    pi, ni, si = sign_flip([m - r for m, r in zip(m_i, r_i)], better_when_positive=True)
    print(f'  monitor vs {rival:11s}: wrong_ever p={p:.5f} (n={n} pos/neg={s}) | '
          f'income p={pi:.5f} (n={ni} pos/neg={si})')
