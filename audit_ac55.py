"""Audit AC55: recompute the frozen record's hashes and gates independently."""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac55_order as a55
import ac38_variance as ac38

ROOT = Path('ac55_results_v1')


def load():
    return json.loads((ROOT / 'results.json').read_text())


def check_hashes(rec):
    for name, h in rec['hashes'].items():
        got = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        assert got == h, f'hash mismatch for {name}'
    return len(rec['hashes'])


def check_gates(rec):
    rows = rec['rows']
    post = lambda arm: [r[arm]['produced'] for r in rows]
    opt = post('optimal'); wst = post('worst'); rnd = post('random')
    d = np.asarray([a - b for a, b in zip(opt, wst)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(r[a]['dead'] for r in rows for a in a55.ARMS)
    o600 = float(np.mean(opt))
    o1500 = float(np.mean([a55.a50.run(a55.OPT, s, a55.RATES, a55.VALUES, ticks=a55.HORIZON)['produced']
                           for s in a55.FINAL_SEEDS]))
    steady = o1500 / o600
    gates = {
        'G1_resolvable': bool(res['p'] <= a55.P_BAR and res['n'] >= a55.MIN_N),
        'G2_median_effect': bool(float(np.median(d)) >= a55.BAR),
        'G3_stability_no_death': bool(dead == 0),
        'G4_horizon_robust': bool(a55.STEADY_LO <= steady <= a55.STEADY_HI),
        'G5_state_blind': bool(float(np.mean(rnd)) < float(np.mean(opt))),
        'G6_headroom': bool(float(np.mean(wst)) <= a55.HEADROOM_FRAC * a55.CEILING),
        'G7_complete': bool(len(rows) == len(a55.FINAL_SEEDS)
                           and all(a in r for r in rows for a in a55.ARMS)),
    }
    for k, v in gates.items():
        assert rec['gates'][k] == v, f'{k}: recorded {rec["gates"][k]} != recomputed {v}'
    return gates


def main():
    rec = load()
    n_hashes = check_hashes(rec)
    gates = check_gates(rec)
    print(f'hashes OK: {n_hashes}/{n_hashes}')
    print(f'gates recomputed independently: all {sum(1 for v in gates.values() if v)}/{len(gates)} true')
    print(f'RECORDED gates: {rec["gates"]}')
    print(f'impaired (descriptive): {rec["summary"]["impaired"]}/12')


if __name__ == '__main__':
    main()
