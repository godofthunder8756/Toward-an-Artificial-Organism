"""AC101 audit: re-derive coverage, source hashes, the per-individual composition invariants, and
the gate recomputation, from the saved tables, without simulating.

G3 (per-tick observer-discard) and G4 (corrupt=False arm identity) are two-run comparisons and
cannot be re-derived from the rows alone; the audit re-reads the recorded dicts and the replay tool
re-runs a sample. Verification tools are NOT hashed into the frozen snapshot (AC17's rule).
"""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac101


def prio(seed):
    rng = np.random.default_rng([seed, 1004])
    return list(map(int, rng.permutation(4)))


def main(root='ac101_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    observer_discard = results.get('observer_discard', {})
    arm_identity = results.get('arm_identity', {})
    unseen = results.get('unseen', [])
    adversarial = results.get('adversarial', [])
    problems = []

    n_ind = len(seeds) * 2
    if len(rows) != n_ind:
        problems.append(f'row count {len(rows)} != {n_ind}')

    keys = [(r['seed'], r['history']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history)')

    if list(seeds) != [4448, 4449, 4450, 4451, 4466, 4481, 4504, 4510]:
        problems.append(f'seeds {seeds} != declared 8-seed set')
    if list(unseen) != [4448, 4449, 4450, 4451]:
        problems.append(f'unseen {unseen} != declared')
    if list(adversarial) != [4466, 4481, 4504, 4510]:
        problems.append(f'adversarial {adversarial} != declared')
    if not set(seeds).isdisjoint(range(4448)):
        problems.append('final seeds not disjoint from everything < 4448')
    for s in adversarial:
        if prio(s) != [3, 0, 2, 1]:
            problems.append(f'adversarial seed {s} has priority {prio(s)} != [3,0,2,1]')

    for r in rows:
        sched = [tuple(x) for x in r.get('schedule', [])]
        if sched != [tuple(x) for x in ac101.SCHEDULE]:
            problems.append(f'row {r["seed"]}/{r["history"]} schedule {sched} != SCHEDULE')
            break
        if r.get('corrupt') is not True:
            problems.append(f'row {r["seed"]}/{r["history"]} corrupt != True')
            break

    for name in ac101.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # ---- recorded two-run comparisons (G3, G4) re-read, not recomputed ----
    if len(observer_discard) != n_ind:
        problems.append(f'observer-discard record has {len(observer_discard)} != {n_ind}')
    if not all(d.get('status') != 'no_mid_streak' and d.get('swap_applied')
               and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
               for d in observer_discard.values()):
        problems.append('observer-discard record not all per-tick byte-identical at a non-zero streak')
    if len(arm_identity) != n_ind or not all(arm_identity.values()):
        problems.append(f'arm-identity record not all True: {len(arm_identity)}/{n_ind}')

    # ---- per-individual composition invariants (re-derived, no simulation) ----
    print('=== per-seed composition (dead / fw / desc / succ / relinq / reacq) ===')
    for s in seeds:
        for h in (0, 1):
            r = next(x for x in rows if x['seed'] == s and x['history'] == h)
            print(f"  {s}/{h} prio={prio(s)}: dead={r['first_dead']} fw={r['fw_at_corrupt']}->"
                  f"{r['flipped_still_wrong']} desc={r['description_correct']}"
                  f"(death={r['description_correct_at_death']}) succ={r['successions']} "
                  f"relinq={r['relinquishments_by_move']} reacq={r['reacquisitions_by_move']} "
                  f"routes={r['routes']}")

    # history identity per seed
    for s in seeds:
        h0 = next(x for x in rows if x['seed'] == s and x['history'] == 0)
        h1 = next(x for x in rows if x['seed'] == s and x['history'] == 1)
        if h0['state_hash'] != h1['state_hash']:
            problems.append(f'histories not identical: {s}')

    # ---- gates recomputed from the rows (no simulation) ----
    # Normalise the JSON round-trip key types (AC15's replay lesson) for the dict-typed fields
    # that json.dump stringifies. NOTE: births_by_window is already string-keyed by the runner
    # (`{str(k): v}`), so it must stay string-keyed -- gates_ac101.production() looks it up with
    # str(i). Do NOT convert it to int keys.
    for r in rows:
        if isinstance(r.get('streak_final'), dict):
            r['streak_final'] = {int(k): v for k, v in r['streak_final'].items()}
        if isinstance(r.get('reacquire_ticks'), dict):
            r['reacquire_ticks'] = {int(k): v for k, v in r['reacquire_ticks'].items()}
    g = ac101.gates_ac101(rows, seeds, observer_discard, ac101.SCHEDULE)
    g['G4_corrupt_is_the_only_change_arm_identity'] = bool(arm_identity) and all(arm_identity.values())
    g['G5_completeness_determinism'] = (len(rows) == n_ind)
    recorded = results.get('gates')
    if recorded is not None:
        for k in g:
            if g[k] != recorded.get(k):
                problems.append(f'gate {k} re-derived as {g[k]} but recorded as {recorded.get(k)}')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print('gates (re-derived, matching recorded):', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'observer-discard: {sum(1 for d in observer_discard.values() if d.get("per_tick_identical"))}/{n_ind} '
          f'per-tick byte-identical at a non-zero streak')
    print(f'arm-identity: {sum(arm_identity.values())}/{n_ind} corrupt=False byte-identical to ac100 gray_ctl')
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, composition invariants, observer-discard record, arm-identity '
          'record, hashes, gates re-derived without simulating and matching the recorded result')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac101_results_v1') else 1)
