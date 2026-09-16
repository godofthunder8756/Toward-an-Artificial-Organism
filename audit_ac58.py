"""Audit AC58: recompute the frozen record's hashes and gates independently."""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac58_order as a58
import ac38_variance as ac38

ROOT = Path('ac58_results_v1')


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
    prot = post('protected'); rep = post('repaired'); unrep = post('unrepaired')
    d = np.asarray([a - b for a, b in zip(rep, unrep)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead_rep = sum(1 for r in rows if r['repaired']['dead'])
    dead_prot = sum(1 for r in rows if r['protected']['dead'])
    dead_unrep = sum(1 for r in rows if r['unrepaired']['dead'])
    retention = all(a == b for a, b in zip(prot, rep))
    r600 = float(np.mean(rep))
    r1500 = float(np.mean([a58.run_register(s, 'repaired', ticks=a58.HORIZON)['produced']
                           for s in a58.FINAL_SEEDS]))
    steady = r1500 / r600
    gates = {
        'G1_resolvable': bool(res['p'] <= a58.P_BAR and res['n'] >= a58.MIN_N),
        'G2_effect': bool(float(np.median(d)) >= a58.BAR),
        'G3_retention': bool(retention),
        'G4_repaired_stability': bool(dead_rep == 0),
        'G5_protected_stability': bool(dead_prot == 0),
        'G6_corruption_consequential': bool(dead_unrep >= 1),
        'G7_horizon_robust': bool(a58.STEADY_LO <= steady <= a58.STEADY_HI),
    }
    for k, v in gates.items():
        assert rec['gates'][k] == v, f'{k}: recorded {rec["gates"][k]} != recomputed {v}'
    return gates


def main():
    rec = load()
    n_hashes = check_hashes(rec)
    gates = check_gates(rec)
    print(f'hashes OK: {n_hashes}/{n_hashes}')
    print(f'gates recomputed independently: {sum(1 for v in gates.values() if v)}/{len(gates)} true')


if __name__ == '__main__':
    main()
