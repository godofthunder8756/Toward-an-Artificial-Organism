# Run from the repository root: python trackc_bypass_diag/posthoc_position.py
"""Post-hoc (after the frozen diagnosis): cell decoder under intact and full erasure, and
the share of probes at which the agent stands in a cell that shows walls."""
import json, sys, numpy as np, torch
from multiprocessing import Pool
sys.path.insert(0, '.')
from trackc_swap.bypass import run_condition, cell_decoder_accuracy
from trackc_swap.env import WorldConfig
wc = WorldConfig(wear=0.001)
per = json.load(open('trackc_bypass_diag/scores.json'))['scores']['per_agent']
def job(k):
    r = per[k]
    f = f"trackc_swap_v6/pair_weights/M1_seed{r['seed']}_FATE.pt" if r['arm']=='FATE' else (
        f"trackc_swap_v6/pair_weights/M1_seed{r['seed']}_YOKED.pt" if r['arm']=='YOKED' else f"trackc_swap_v6/phase1_weights/M1_seed{r['seed']}.pt")
    torch.set_num_threads(1)
    sd = torch.load(f, weights_only=False)
    out = {'key': k, 'group': r['group']}
    for name, p in (('intact', 0.0), ('full', 0.3), ('memoryless', 1.0)):
        c = run_condition(sd, r['seed'], wc, 128, 4, p, None, 3, record=True)
        cells = np.asarray(c['cells']); x, y = cells % 7, cells // 7
        edge = (x < 2) | (x > 4) | (y < 2) | (y > 4)
        out[name] = (round(cell_decoder_accuracy(c['cells'], c['targets'], 7), 3), round(float(edge.mean()), 2))
    return out
keys = [k for k in per if per[k]['group'] in ('bypass_fate', 'regulator_fate') or k.startswith('NOFATE_60')][:40]
with Pool(4) as pool:
    for o in pool.imap(job, keys):
        print(o['key'], o['group'], 'cell decoder / share at a wall: intact', o['intact'], 'full', o['full'], 'memoryless', o['memoryless'])
