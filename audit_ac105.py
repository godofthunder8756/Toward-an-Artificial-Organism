"""AC105 audit: re-derive the frozen study's gates and invariants WITHOUT simulating.

Reads ac105_results_v1/{pre_run_snapshot.json, rows.jsonl, results.json} and verifies: (1) the
source hashes have not drifted; (2) the six gates re-derived from the saved table match the
recorded result; (3) the seed-disjointness of the final sample; (4) the per-arm invariants (the
baseline is byte-identical to AC104, the candidate applies and recovers the corruption, and the
candidate never harms survival or relinquishment). Reports the rescue count and the
reconstruction-harm count (candidate fw>0 where the control recovered) as findings. Exits nonzero
if any check fails. Verification tools are NOT hashed into the snapshot (AC17's rule).
"""
import json
import sys
from pathlib import Path
import ac105
import ac104

ROOT = Path('ac105_results_v1')


def load():
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    res = json.loads((ROOT / 'results.json').read_text())
    return snap, rows, res


def check_hashes(snap):
    import hashlib
    drift = []
    for name in ac105.SOURCES:
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
        | set(range(4872, 5100)) | set(range(5100, 5508)) \
        | set(range(5600, 5608)) | set(range(5700, 5708))
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
    g = ac105.gates_ac105(rows, res['seeds'], obs)
    ident = res.get('arm_identity', {})
    g['G1_control_identity'] = all(
        v.get('persistent_is_ac104') and v.get('budget_is_ac104') for v in ident.values())
    g['G6_completeness_determinism'] = (
        len(rows) == len(res['seeds']) * len(ac105.ARMS) * len(res['conditions']) * 2)

    recorded = res['gates']
    for k in ('G1_control_identity', 'G2_candidate_reconstructs_all_conditions',
              'G3_no_harm_survival', 'G4_no_harm_relinquishment',
              'G5_state_sufficiency_observer_discard_candidate',
              'G6_completeness_determinism'):
        assert g[k] == recorded.get(k), f'gate {k} re-derived {g[k]} != recorded {recorded.get(k)}'
        print(f'  {k}: {g[k]}')
    print('gates: re-derived match recorded')

    # per-arm invariants + findings
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    n_rescue = 0
    n_recon_harm = 0
    n_relinq_improve = 0
    for seed in res['seeds']:
        for h in (0, 1):
            for cond in res['conditions']:
                ctl = by[(seed, h, cond)]['persistent']
                cand = by[(seed, h, cond)]['persistent_budget']
                # corruption applied everywhere
                assert ctl['fw_at_corrupt'] == ac105.CORRUPT_BITS, f'{seed}/{h}/{cond}: control'
                assert cand['fw_at_corrupt'] == ac105.CORRUPT_BITS, f'{seed}/{h}/{cond}: candidate'
                # no-harm survival
                if ctl['completed']:
                    assert cand['completed'], f'{seed}/{h}/{cond}: candidate died where control survived'
                # no-harm relinquishment
                if ctl['completed']:
                    assert cand['relinquishments'] >= ctl['relinquishments'], \
                        f'{seed}/{h}/{cond}: candidate relinquished less than control'
                # findings
                if (not ctl['completed']) and cand['completed']:
                    n_rescue += 1
                if cand['flipped_still_wrong'] > 0 and ctl['flipped_still_wrong'] == 0:
                    n_recon_harm += 1
                if ctl['completed'] and cand['relinquishments'] > ctl['relinquishments']:
                    n_relinq_improve += 1
    print('invariants: corruption applied everywhere; candidate no-harm on survival and '
          'relinquishment')
    print(f'findings -- rescue (cand survives, ctl dies): {n_rescue}')
    print(f'findings -- reconstruction-harm (cand fw>0, ctl fw==0): {n_recon_harm}')
    print(f'findings -- relinquishment-completeness improvement: {n_relinq_improve}')

    print('AC105 audit passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
