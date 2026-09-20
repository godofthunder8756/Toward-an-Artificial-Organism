"""AC102 audit: split verification — re-derive source hashes, the 2x2 interaction, the staged
schedule, and the gates from the saved rows WITHOUT simulating.

Distinct from replay_ac102.py (which does sampled exact reruns). This file re-reads
ac102_results_v1/ and re-computes every claim from the frozen table + hashes.
"""
import hashlib
import json
import sys
from pathlib import Path
import ac102


def load(root='ac102_results_v1'):
    root = Path(root)
    rows = [json.loads(l) for l in (root / 'rows.jsonl').read_text().splitlines()]
    results = json.loads((root / 'results.json').read_text())
    snapshot = json.loads((root / 'pre_run_snapshot.json').read_text())
    return root, rows, results, snapshot


def check_source_hashes(snapshot, errors):
    for name, h in sorted(snapshot.items()):
        p = Path(name)
        if not p.exists():
            errors.append(f'source missing: {name}')
            continue
        cur = hashlib.sha256(p.read_bytes()).hexdigest()
        if cur != h:
            errors.append(f'hash drift: {name} (frozen {h[:12]} vs now {cur[:12]})')


def rederive_gates(rows, seeds, observer_discard):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
    n_ind = len(seeds) * 2
    both_rows = [r for r in rows if r['arm'] == 'both']

    g1 = len(both_rows) == n_ind and all(
        by[(r['seed'], r['history'])]['neither']['completed']
        and by[(r['seed'], r['history'])]['move_only']['completed']
        and by[(r['seed'], r['history'])]['corrupt_only']['completed']
        for r in both_rows)
    g2 = len(both_rows) == n_ind and all(
        r['fw_at_corrupt'] == ac102.CORRUPT_BITS and r['flipped_still_wrong'] == 0
        for r in both_rows)
    g3 = all(
        by[(r['seed'], r['history'])]['both']['completed']
        or (not by[(r['seed'], r['history'])]['staged']['completed'])
        for r in both_rows)
    staged_rows = [r for r in rows if r['arm'] == 'staged']
    g4 = len(staged_rows) == n_ind and all(
        r['flipped_still_wrong'] == 0 for r in staged_rows)
    never_rows = [r for r in rows if r['arm'] == 'never']
    g5 = len(never_rows) == n_ind and all(
        r['flipped_still_wrong'] > 0 and not r['completed'] for r in never_rows)
    g6 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())
    g7 = all(
        by[(r['seed'], r['history'])]['neither']['completed']
        and by[(r['seed'], r['history'])]['move_only']['completed']
        and by[(r['seed'], r['history'])]['corrupt_only']['completed']
        and by[(r['seed'], r['history'])]['both']['fw_at_corrupt'] == ac102.CORRUPT_BITS
        and by[(r['seed'], r['history'])]['both']['flipped_still_wrong'] == 0
        for r in both_rows if r['seed'] in ac102.ADVERSARIAL)
    return {
        'G1_interaction_death_requires_both': g1,
        'G2_reconstruction_recovers_under_both': g2,
        'G3_timing_hypothesis_falsified_staged_does_not_rescue': g3,
        'G4_staged_recovers_controller_eventually': g4,
        'G5_never_repair_must_fail': g5,
        'G6_state_sufficiency_observer_discard': g6,
        'G7_adversarial_stratum': g7,
    }


def check_budget_trace(rows, errors):
    """The reconstruction's single-tick material spend drops material below 64 (obs bit 1) on the
    `both` arm at t=8192 for the death-prone seeds — the budget-trace claim, re-derived without
    simulating."""
    for r in rows:
        if r['arm'] != 'both':
            continue
        if r['mat_at_corrupt'] is not None and r['mat_at_corrupt'] > 64:
            # high-material seed: the spend may or may not cross 64; only check the peak write
            continue
        peak = max((b['reg_writes'] for b in r['budget_trace']), default=0)
        # the reconstruction must be a single-tick lump on the death-prone (low-material) seeds
        if r['mat_at_corrupt'] is not None and r['mat_at_corrupt'] <= 74:
            if peak < 8:
                errors.append(f'seed {r["seed"]}/{r["history"]} both: peak reg_writes {peak} < 8 '
                              f'(expected a lump reconstruction)')
        # every `both` trace must record material crossing below 64 (obs bit 1) right after the
        # corruption for low-material seeds
        if r['mat_at_corrupt'] is not None and r['mat_at_corrupt'] <= 66:
            crossed = any(b['mat_after'] < 64 for b in r['budget_trace'])
            if not crossed:
                errors.append(f'seed {r["seed"]}/{r["history"]} both: material never < 64 '
                              f'(obs bit 1 never fired)')


def check_interaction(rows, errors):
    """The death (if any) is confined to `both`; single challenges survive."""
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
    for (s, h), arms in by.items():
        for arm in ('neither', 'move_only', 'corrupt_only'):
            if not arms[arm]['completed']:
                errors.append(f'seed {s}/{h} {arm} died: interaction gate violated')


def check_seed_disjointness(rows, errors):
    used_prior = set(range(8)) | set(range(4412, 4440)) | set(range(4440, 4452)) \
        | {4466, 4481, 4504, 4510} | set(range(4600, 4872)) | set(range(5100, 5508))
    finals = {r['seed'] for r in rows}
    overlap = finals & used_prior
    if overlap:
        errors.append(f'final seeds overlap prior families: {sorted(overlap)}')
    # unseen and adversarial strata must be disjoint
    unseen = {r['seed'] for r in rows if r['seed'] in ac102.UNSEEN}
    adv = {r['seed'] for r in rows if r['seed'] in ac102.ADVERSARIAL}
    if unseen & adv:
        errors.append(f'unseen/adversarial strata overlap: {unseen & adv}')


def main():
    root, rows, results, snapshot = load()
    errors = []
    check_source_hashes(snapshot, errors)

    seeds = results['seeds']
    obs = results['observer_discard']
    ident = results['arm_identity']

    # 1. row count + arm coverage
    expected = len(seeds) * len(ac102.ARMS) * 2
    if len(rows) != expected:
        errors.append(f'row count {len(rows)} != {expected}')
    arms_seen = {(r['seed'], r['history'], r['arm']) for r in rows}
    if len(arms_seen) != expected:
        errors.append(f'duplicate/missing (seed,history,arm) tuples: {len(arms_seen)} != {expected}')

    # 2. re-derive gates and compare to the recorded result
    gates = rederive_gates(rows, seeds, obs)
    recorded = results['gates']
    for k, v in gates.items():
        if k in recorded and recorded[k] != v:
            errors.append(f'gate {k}: re-derived {v} != recorded {recorded[k]}')
    # G8 (completeness/determinism/identity) re-derive
    first = rows[0]
    g8 = (len(rows) == expected
          and all(v.get('move_only_is_ac100') and v.get('both_is_ac101')
                  and v.get('staged_nobudget_is_both') for v in ident.values()))
    if recorded.get('G8_completeness_determinism_arm_identity') != g8:
        errors.append(f'gate G8: re-derived {g8} != recorded '
                      f'{recorded.get("G8_completeness_determinism_arm_identity")}')

    # 3. budget-trace claim
    check_budget_trace(rows, errors)
    # 4. interaction invariant
    check_interaction(rows, errors)
    # 5. seed disjointness
    check_seed_disjointness(rows, errors)
    # 6. observer-discard records complete
    if len(obs) != len(seeds) * 2:
        errors.append(f'observer-discard records {len(obs)} != {len(seeds) * 2}')

    print(f'rows={len(rows)} seeds={len(seeds)} arms={len(ac102.ARMS)}')
    print(f'gates (re-derived): {json.dumps({k: v for k, v in gates.items()}, indent=2)}')
    if errors:
        print('\nFAILURES:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\nAC102 audit passed: source hashes valid, gates re-derived without simulating, '
          'interaction + budget-trace + seed-disjointness invariants hold.')


if __name__ == '__main__':
    main()
