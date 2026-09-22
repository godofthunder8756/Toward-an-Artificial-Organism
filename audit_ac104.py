"""AC104 audit: re-derive the frozen study's gates and invariants WITHOUT simulating.

Reads ac104_results_v1/{pre_run_snapshot.json, rows.jsonl, results.json} and verifies: (1) the
source hashes have not drifted; (2) the six gates re-derived from the saved table match the
recorded result; (3) the seed-disjointness of the final sample; (4) the per-arm invariants (the
control is byte-identical to AC103 persistent, the candidate completes reconstruction, the
candidate never harms survival/relinquishment, and the allowance is preserved no worse than the
control). Exits nonzero if any check fails. Verification tools are NOT hashed into the snapshot
(AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac104
import ac103

ROOT = Path('ac104_results_v1')


def load():
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    res = json.loads((ROOT / 'results.json').read_text())
    return snap, rows, res


def check_hashes(snap):
    import hashlib
    drift = []
    for name in ac104.SOURCES:
        if not Path(name).exists():
            drift.append(f'{name} (missing)')
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if name in snap and snap[name] != h:
            drift.append(name)
    return drift


def check_seed_disjointness(seeds):
    prior = set(range(8)) | set(range(4412, 4440)) | set(range(4440, 4444)) \
        | set(range(4444, 4448)) | set(range(4448, 4452)) \
        | {4466, 4481, 4504, 4510} | set(range(4600, 4872)) \
        | set(range(4872, 5100)) | set(range(5100, 5508)) | set(range(5600, 5608))
    overlap = set(seeds) & prior
    dup = len(set(seeds)) != len(seeds)
    return overlap, dup


def main():
    snap, rows, res = load()
    drift = check_hashes(snap)
    if drift:
        print(f'FAIL: source hash drift: {drift}')
        sys.exit(1)
    print('hashes: no drift')

    overlap, dup = check_seed_disjointness(res['seeds'])
    assert not overlap, f'final seeds overlap prior families: {overlap}'
    assert not dup, 'duplicate final seeds'
    print('seeds: disjoint and unique')

    # re-derive the gates from the saved rows (no simulation)
    obs = res.get('observer_discard_candidate', {})
    g = ac104.gates_ac104(rows, res['seeds'], obs)
    # G1 (control identity) is re-derived from the recorded arm_identity dict
    ident = res.get('arm_identity', {})
    g['G1_control_identity'] = all(
        v.get('persistent_is_ac103') for v in ident.values())
    # G6 (completeness) from the row count
    g['G6_completeness_determinism'] = (len(rows) == len(res['seeds']) * len(ac104.ARMS) * 2)

    recorded = res['gates']
    for k, v in g.items():
        assert v == recorded.get(k), f'gate {k} re-derived {v} != recorded {recorded.get(k)}'
        print(f'  {k}: {v}')
    print('gates: re-derived match recorded')

    # per-arm invariants
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['arm']), r)
    n_rescue = 0
    for seed in res['seeds']:
        for h in (0, 1):
            ctl = by[(seed, h, 'persistent')]
            cand = by[(seed, h, 'persistent_budget')]
            # corruption applied + recovered everywhere (both arms)
            assert ctl['fw_at_corrupt'] == ac104.CORRUPT_BITS, f'{seed}/{h}: control corrupt'
            assert cand['fw_at_corrupt'] == ac104.CORRUPT_BITS, f'{seed}/{h}: candidate corrupt'
            assert ctl['flipped_still_wrong'] == 0, f'{seed}/{h}: control did not recover'
            assert cand['flipped_still_wrong'] == 0, f'{seed}/{h}: candidate did not recover'
            # no harm: candidate survives + relinquishes >= control
            if ctl['completed']:
                assert cand['completed'], f'{seed}/{h}: candidate died where control survived'
            assert cand['relinquishments'] >= ctl['relinquishments'], \
                f'{seed}/{h}: candidate relinquished less than control'
            # allowance preservation no worse
            assert cand['allowance_breached'] <= ctl['allowance_breached'], \
                f'{seed}/{h}: candidate breached the allowance more than control'
            if not ctl['completed'] and cand['completed']:
                n_rescue += 1
    print('invariants: corruption applied/recovered everywhere; candidate no-harm on survival, '
          'relinquishment, and allowance preservation')
    print(f'rescue count on the final sample: {n_rescue} individuals')

    print('AC104 audit passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
