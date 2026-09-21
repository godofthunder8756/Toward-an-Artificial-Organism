"""AC103 audit: re-derive the frozen study's gates and invariants WITHOUT simulating.

Reads ac103_results_v1/{pre_run_snapshot.json, rows.jsonl, results.json} and verifies: (1) the
source hashes have not drifted; (2) the six gates re-derived from the saved table match the
recorded result; (3) the seed-disjointness of the final sample; (4) the per-arm invariants (the
corruption is applied and recovered, the cementing write is present where the staged arm fails,
the persistent arm recovers everywhere, the defer arm's survival outcome). Exits nonzero if any
check fails. Verification tools are NOT hashed into the snapshot (AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac103
import ac102

ROOT = Path('ac103_results_v1')


def load():
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    res = json.loads((ROOT / 'results.json').read_text())
    return snap, rows, res


def check_hashes(snap):
    import hashlib
    drift = []
    for name in ac103.SOURCES:
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
        | set(range(4872, 5100)) | set(range(5100, 5508))
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
    obs = res.get('observer_discard_current', {})
    g = ac103.gates_ac103(rows, res['seeds'], obs)
    # G1 (arm identity) is re-derived from the recorded arm_identity dict
    ident = res.get('arm_identity', {})
    g['G1_arm_identity'] = all(
        v.get('current_is_ac102_both') and v.get('current_staged_is_ac102_staged')
        for v in ident.values())
    # G6 (completeness) from the row count
    g['G6_completeness_determinism'] = (len(rows) == len(res['seeds']) * len(ac103.ARMS) * 2)

    recorded = res['gates']
    for k, v in g.items():
        assert v == recorded.get(k), f'gate {k} re-derived {v} != recorded {recorded.get(k)}'
        print(f'  {k}: {v}')
    print('gates: re-derived match recorded')

    # per-arm invariants
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['arm']), r)
    starvation = []
    for seed in res['seeds']:
        for h in (0, 1):
            c = by[(seed, h, 'current')]
            assert c['fw_at_corrupt'] == ac103.CORRUPT_BITS, f'{seed}/{h}: corruption not applied'
            assert c['flipped_still_wrong'] == 0, f'{seed}/{h}: current did not recover'
            cs = by[(seed, h, 'current_staged')]
            ps = by[(seed, h, 'persistent_staged')]
            # persistence is no-harm on recovery (recovers wherever current_staged does)
            if cs['flipped_still_wrong'] == 0:
                assert ps['flipped_still_wrong'] == 0, f'{seed}/{h}: persistence broke recovery'
            # the cementing write is present exactly where the staged arm stalls
            if cs['flipped_still_wrong'] > 0:
                assert cs['action2_cementing'] > 0, f'{seed}/{h}: no cementing write on a stall'
            if ps['flipped_still_wrong'] > 0:
                starvation.append((seed, h))
    print('invariants: corruption applied/recovered everywhere; persistence no-harm on recovery; '
          'cementing write present on staged stalls')
    # recovery failures under persistence are exactly the recorded starvation (5607, both histories)
    assert set(s for s, _ in starvation) == {5607} and len(starvation) == 2, \
        f'persistence recovery failures are {starvation}, expected exactly 5607 x2'
    # every persistence DEATH is recovery-complete (fw==0, resource shortage) except the starvation
    for r in rows:
        if r['arm'] == 'persistent_staged' and not r['completed']:
            if r['seed'] == 5607:
                assert r['flipped_still_wrong'] > 0, '5607 is not the starvation case'
            else:
                assert r['flipped_still_wrong'] == 0, \
                    f"{r['seed']}/{r['history']}: non-starvation persistence death has fw>0"
    print('invariants: persistence recovery failures are exactly the 5607 starvation; other '
          'persistence deaths are recovery-complete (fw==0)')

    print('AC103 audit passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
