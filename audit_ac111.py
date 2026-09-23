"""audit_ac111.py — re-derive coverage, gates, and source hashes from the saved table WITHOUT
simulating. This is the SPLIT verification half (replay_ac111.py does the sampled exact reruns).

The verification tools are deliberately NOT in the frozen source set (AC16/17's drift rule): the
frozen sources of truth are the protocol + the simulation code (ac111.py and its frozen
dependencies), which is what could tune a result.

G3 and G5 are recorded as FAILURES at the measured values (12/16 each), per the
results doc — not moved. The G3 failure cells are 6306 (the cut never bit, estimate unwritten, so
bel=1) and 6307 (a seed-dependent spurious relinquishment during the cut, recovered), and the G5
failure cells are 6303 (an extra 1-replica re-correction) and 6306 (the cut never bit, estimate
unwritten). All are behavioural, not survival-level: every corrupt-arm cell completes and holds
route-1 at the horizon."""

import hashlib
import json
from pathlib import Path

ROOT = Path('ac111_results_v1')
SOURCES = ['ac111.py', 'ac110.py', 'ac107.py', 'ac106.py', 'ac104.py', 'ac103.py',
           'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py',
           'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
           'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
           'AC111_PROTOCOL_v1.md']
FINAL_SEEDS = [6300, 6301, 6302, 6303, 6304, 6305, 6306, 6307]
ARMS = ('est', 'est_corrupt', 'est_corrupt_budget')
CONDITIONS = ('no_cause', 'move', 'cut')
CORRUPT_BITS = 8


def main():
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())

    # 1. source hashes still valid
    drifted = {}
    for n in SOURCES:
        cur = hashlib.sha256(Path(n).read_bytes()).hexdigest()
        if snap.get(n) != cur:
            drifted[n] = (snap.get(n), cur)
    if drifted:
        print('HASH DRIFT:', drifted)
        raise SystemExit(1)
    print('source hashes valid (%d files)' % len(SOURCES))

    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    print('rows:', len(rows))

    # 2. coverage: 8 seeds x 2 histories x 3 conditions x 3 arms = 144, no duplicates
    cells = {(r['seed'], r['history'], r['condition'], r['arm']) for r in rows}
    assert len(cells) == 144, f'coverage {len(cells)} != 144'
    seeds = sorted({r['seed'] for r in rows})
    assert seeds == FINAL_SEEDS, seeds
    print('coverage OK: seeds', seeds)

    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['condition'], r['arm'])] = r
    inds = [(s, h) for s in seeds for h in (0, 1)]
    n_cells = len(inds)  # 16

    def cell(s, h, c, arm):
        return by[(s, h, c, arm)]

    # 3. gates re-derived from the saved table
    ident = json.loads((ROOT / 'results.json').read_text())['est_is_ac110']
    g1 = sum(1 for v in ident.values() if v)

    g2 = sum(1 for s, h in inds for c in CONDITIONS
             if cell(s, h, c, 'est_corrupt_budget')['fw_at_corrupt'] == CORRUPT_BITS
             and cell(s, h, c, 'est_corrupt_budget')['flipped_still_wrong'] == 0
             and cell(s, h, c, 'est_corrupt_budget')['recovery_tick'] is not None)

    g3_bel = sum(1 for s, h in inds
                 if cell(s, h, 'cut', 'est_corrupt_budget')['bel_at_cut_end'] == 0)
    g3_relq = sum(1 for s, h in inds
                  if cell(s, h, 'cut', 'est_corrupt_budget')['relinquishments'] == 0)
    g3_route = sum(1 for s, h in inds
                   if cell(s, h, 'cut', 'est_corrupt_budget')['route1_bound_at_horizon'])
    g3 = sum(1 for s, h in inds
             if cell(s, h, 'cut', 'est_corrupt_budget')['bel_at_cut_end'] == 0
             and cell(s, h, 'cut', 'est_corrupt_budget')['relinquishments'] == 0
             and cell(s, h, 'cut', 'est_corrupt_budget')['route1_bound_at_horizon'])

    g4 = sum(1 for s, h in inds
             if cell(s, h, 'move', 'est_corrupt_budget')['relinquishments'] >= 1)

    g5 = sum(1 for s, h in inds
             if cell(s, h, 'cut', 'est_corrupt_budget')['bel_writes'] == 7
             and cell(s, h, 'cut', 'est')['bel_writes'] == 7)

    g6 = sum(1 for s, h in inds for c in CONDITIONS
             if not (cell(s, h, c, 'est_corrupt')['completed']
                     and not cell(s, h, c, 'est_corrupt_budget')['completed']))

    print(f'G1 est identity: {g1}/48 (PASS={g1 == 48})')
    print(f'G2 reconstruction completes: {g2}/{n_cells * len(CONDITIONS)} '
          f'(PASS={g2 == n_cells * len(CONDITIONS)})')
    print(f'G3 cut estimate holds: {g3}/{n_cells} (recorded FAIL, prespecified 16/16) — '
          f'bel==0 {g3_bel}/16, relinq==0 {g3_relq}/16, route-held {g3_route}/16')
    print(f'G4 move estimate relinquishes: {g4}/{n_cells} (PASS={g4 == n_cells})')
    print(f'G5 reacquisition untouched: {g5}/{n_cells} (recorded FAIL, prespecified 16/16)')
    print(f'G6 no-harm survival budget: {g6}/{n_cells * len(CONDITIONS)} '
          f'(PASS={g6 == n_cells * len(CONDITIONS)})')

    # 4. survival: every corrupt-arm cell completes (the interference is behavioural, not survival)
    surv = sum(1 for s, h in inds for c in CONDITIONS
               for a in ('est_corrupt', 'est_corrupt_budget')
               if cell(s, h, c, a)['completed'])
    print(f'corrupt-arm survival: {surv}/{2 * n_cells * len(CONDITIONS)}')

    # 5. the passing gates must hold; the recorded failures must be at their measured values.
    assert g1 == 48
    assert g2 == n_cells * len(CONDITIONS)
    assert g3 == 12, f'G3 measured {g3}, expected 12 (recorded failure)'
    assert g3_route == 16
    assert g4 == n_cells
    assert g5 == 12, f'G5 measured {g5}, expected 12 (recorded failure)'
    assert g6 == n_cells * len(CONDITIONS)
    assert surv == 2 * n_cells * len(CONDITIONS)
    print('AC111 audit passed: coverage, ledgers, gate tallies and source hashes valid '
          '(G3 recorded at 12/16, G5 at 12/16 — behavioural, seed-dependent, per the results doc)')


if __name__ == '__main__':
    main()
