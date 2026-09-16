"""Audit AC57: recompute the frozen record's hashes and gates independently."""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac57_order as a57
import ac38_variance as ac38

ROOT = Path('ac57_results_v1')


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
    opt = post('optimal'); wst = post('worst')
    lrn = post('learner'); nrl = post('no_release'); rnd = post('random')
    d_load = np.asarray([a - b for a, b in zip(opt, wst)], dtype=float)
    d_re = np.asarray([a - b for a, b in zip(lrn, nrl)], dtype=float)
    res_load = ac38.sign_flip_test(list(d_load))
    res_re = ac38.sign_flip_test(list(d_re))
    dead = sum(r[a]['dead'] for r in rows for a in a57.ARMS)
    o600 = float(np.mean(opt))
    o1500 = float(np.mean([a57.a50.run(a57.OPT_B, s, a57.RATES_B, a57.VALUES_B, ticks=a57.HORIZON)['produced']
                           for s in a57.FINAL_SEEDS]))
    steady = o1500 / o600
    gates = {
        'G1_load_resolvable': bool(res_load['p'] <= a57.P_BAR and res_load['n'] >= a57.MIN_N),
        'G2_load_effect': bool(float(np.median(d_load)) >= a57.BAR),
        'G3_reacq_resolvable': bool(res_re['p'] <= a57.P_BAR and res_re['n'] >= a57.MIN_N),
        'G4_reacq_effect': bool(float(np.median(d_re)) >= a57.BAR),
        'G5_stability_no_death': bool(dead == 0),
        'G6_horizon_robust': bool(a57.STEADY_LO <= steady <= a57.STEADY_HI),
        'G7_state_blind': bool(float(np.mean(rnd)) < float(np.mean(opt))),
        'G8_headroom': bool(float(np.mean(wst)) <= a57.HEADROOM_FRAC * a57.CEILING),
        'G9_register_in_loop': bool(all(tuple(r['learner_order']) == a57.reg.unlehmer(a57.reg.lehmer(r['learner_order']))
                                         for r in rows)),
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
