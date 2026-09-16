"""Audit AC54: recompute the frozen record's hashes and gates independently."""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac54_order as a54
import ac38_variance as ac38

ROOT = Path('ac54_results_v1')


def load():
    return json.loads((ROOT / 'results.json').read_text())


def check_hashes(rec):
    for name, h in rec['hashes'].items():
        got = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        assert got == h, f'hash mismatch for {name}: {got} != {h}'
    return len(rec['hashes'])


def check_gates(rec):
    rows = rec['rows']
    post = lambda arm: [r[arm]['produced'] for r in rows]
    opt = post('optimal'); wst = post('worst'); rnd = post('random')
    d = np.asarray([a - b for a, b in zip(opt, wst)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(r[a]['dead'] for r in rows for a in a54.ARMS)
    o600 = float(np.mean(opt))
    o1500 = float(np.mean([a54.a50.run(a54.OPT, s, a54.RATES, a54.VALUES, ticks=a54.HORIZON)['produced']
                           for s in a54.FINAL_SEEDS]))
    steady = o1500 / o600
    pinned = sum(1 for v in opt if v >= a54.CEILING - 1e-9)
    impaired = sum(1 for a, b in zip(opt, wst) if b > a)
    gates = {
        'G1_resolvable': bool(res['p'] <= a54.P_BAR and res['n'] >= a54.MIN_N),
        'G2_median_effect': bool(float(np.median(d)) >= a54.BAR),
        'G3_stability_no_death': bool(dead == 0),
        'G4_horizon_robust': bool(a54.STEADY_LO <= steady <= a54.STEADY_HI),
        'G5_consistency': bool(impaired == 0),
        'G6_state_blind': bool(float(np.mean(rnd)) < float(np.mean(opt))),
        'G7_headroom': bool(pinned == 0),
    }
    for k, v in gates.items():
        assert rec['gates'][k] == v, f'{k}: recorded {rec["gates"][k]} != recomputed {v}'
    return gates


def main():
    rec = load()
    n_hashes = check_hashes(rec)
    gates = check_gates(rec)
    print(f'hashes OK: {n_hashes}/{n_hashes}')
    print(f'gates recomputed independently: {gates}')
    print(f'RECORDED gates: {rec["gates"]}')
    passed = sum(1 for v in gates.values() if v)
    total = len(gates)
    print(f'audit: {passed}/{total} gates true (the failure is genuine and pinned)')


if __name__ == '__main__':
    main()
