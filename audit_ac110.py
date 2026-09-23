"""audit_ac110.py — re-derive coverage, gates, and source hashes from the saved table WITHOUT
simulating. This is the SPLIT verification half (replay_ac110.py does the sampled exact reruns)."""

import hashlib
import json
from pathlib import Path

ROOT = Path('ac110_results_v1')
SOURCES = ['ac110.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC110_PROTOCOL_v1.md']


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

    # 2. coverage: 8 seeds x 2 histories x 3 conditions x 2 arms = 96, no duplicates
    cells = {(r['seed'], r['history'], r['condition'], r['arm']) for r in rows}
    assert len(cells) == 96, f'coverage {len(cells)} != 96'
    seeds = sorted({r['seed'] for r in rows})
    assert seeds == [6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207], seeds
    print('coverage OK: seeds', seeds)

    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['condition'], r['arm'])] = r
    inds = [(s, h) for s in seeds for h in (0, 1)]

    def pair(s, h, c):
        return by[(s, h, c, 'maintained')], by[(s, h, c, 'no_repair')]

    # 3. gates re-derived from the saved table
    g1 = sum(1 for s, h in inds for c in ('no_cause', 'move')
             if pair(s, h, c)[0]['state_hash'] == pair(s, h, c)[1]['state_hash'])
    g2 = sum(1 for s, h in inds
             if pair(s, h, 'cut')[0]['bel_wrong_in_window'] == pair(s, h, 'cut')[1]['bel_wrong_in_window']
             and pair(s, h, 'cut')[0]['bel_at_cut_end'] == 0
             and pair(s, h, 'cut')[1]['bel_at_cut_end'] == 0)
    g3 = sum(1 for s, h in inds
             if pair(s, h, 'cut')[0]['relinquishments'] == pair(s, h, 'cut')[1]['relinquishments']
             and pair(s, h, 'cut')[0]['routes'] == pair(s, h, 'cut')[1]['routes'])
    g4 = sum(1 for s, h in inds
             if pair(s, h, 'cut')[0]['bel'] == 0 and pair(s, h, 'cut')[1]['bel'] == 1)
    g5 = sum(1 for s, h in inds for c in ('no_cause', 'move', 'cut')
             if pair(s, h, c)[0]['completed'] == pair(s, h, c)[1]['completed']
             and pair(s, h, c)[0]['first_dead'] == pair(s, h, c)[1]['first_dead'])
    print(f'G1 clean control: {g1}/32 (PASS={g1 == 32})')
    print(f'G2 accuracy equality: {g2}/16 (PASS={g2 == 16})')
    print(f'G3 use equality: {g3}/16 (PASS={g3 == 16})')
    print(f'G4 storage dependence: {g4}/16 (recorded FAIL, measured {g4})')
    print(f'G5 viability identity: {g5}/48 (PASS={g5 == 48})')

    # 4. invariant: reacquisition untouched (bel_writes identical across arms)
    belw = all(pair(s, h, c)[0]['bel_writes'] == pair(s, h, c)[1]['bel_writes']
               for s, h in inds for c in ('no_cause', 'move', 'cut'))
    print('bel_writes identical across arms (all 48 cells):', belw)

    # 5. direction invariant: maintained never drifts (bel==0) in cut
    mdrift = sum(1 for s, h in inds if pair(s, h, 'cut')[0]['bel'] == 1)
    print('maintained drifts in cut (must be 0):', mdrift)

    assert g1 == 32 and g2 == 16 and g3 == 16 and g5 == 48 and mdrift == 0 and belw
    print('AC110 audit passed: coverage, ledgers, gate tallies and source hashes valid '
          '(G4 recorded at %d/16 as a seed-dependent storage drift, per the results doc)' % g4)


if __name__ == '__main__':
    main()
