"""audit_ac114.py — re-derive the AC114 frozen confirmation from the saved table,
WITHOUT simulating.

Verifies, from `ac114_results_v1/rows.jsonl` and the pre-run snapshot only:
  (1) source hashes match the pre-run snapshot (ac114.py + frozen deps + protocol),
  (2) row coverage is complete (8 seeds x 2 histories x 11 arms = 176, no dupes),
  (3) the frozen ac4.balance ledger identities hold in every arm,
  (4) arm mechanism invariants hold,
  (5) the prespecified gates G1/G3/G4/G5/G6 are recomputed and pass,
and reports survival as a SEPARATE outcome plus the D3/D5 observations.

This is the split-verification audit half (AC9's pattern): it re-checks coverage,
ledgers, arm invariants, source hashes and gate verdicts from the saved table only.
replay_ac114.py does the sampled exact reruns. The audit does NOT import ac114
(no simulation), only stdlib.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULT = ROOT / 'ac114_results_v1'
ARMS = ('keep', 'reference', 'rival', 'no_B', 'no_B_retention',
        'no_B_retention_ref', 'permeant', 'B_rescue', 'puncture',
        'rival_puncture', 'puncture_non_gate')
SEEDS = list(range(6500, 6508))
SURVIVE_ARMS = ('keep', 'reference', 'rival', 'no_B_retention_ref', 'B_rescue',
                'rival_puncture', 'puncture_non_gate')
DIE_ARMS = ('no_B', 'no_B_retention', 'permeant', 'puncture')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def check_ledger(row):
    """The frozen ac4.balance identities (same form as audit_ac10.py / test_ac114.py)."""
    l = row['ledger']
    inv = row['final_inventory']
    m0 = 128 + 24 + 40 + l['in_m'] + 2 * l['external_B']
    m1 = inv[1] + 4 * inv[3] + 2 * inv[4] + sum(row['demand'])
    spent = l['writes'] - l['memory_writes']
    losses = (l['memory_waste'] + l['memory_expiry'] +
              4 * (l['particle_expiry'] + l['particle_export']) +
              2 * (l['B_expiry'] + l['B_discard']) + l['overflow_m'])
    assert m0 == m1 + spent + losses, (row['seed'], row['history'], row['arm'],
                                       'material identity', m0, m1, spent, losses)
    assert 64 + 8 * l['converted'] == inv[0] + l['spent_e'], \
        (row['seed'], row['history'], row['arm'], 'energy identity')
    assert 32 + l['in_f'] == inv[2] + l['overflow_f'] + l['converted'], \
        (row['seed'], row['history'], row['arm'], 'fuel identity')


def check_arm(row):
    l = row['ledger']
    a = row['arm']
    both = all(x is not None for x in row['routes'])
    if a in ('keep', 'reference', 'rival'):
        assert l['B_birth'] > 0 and l['W_birth'] > 0 and l['C_birth'] > 0
        assert l['external_B'] == 0 and l['particle_export'] == 0
        assert row['completed'] and both
    elif a == 'no_B':
        assert l['B_birth'] == 0 and not row['completed']
        assert l['particle_export'] > 0 and not both
    elif a == 'no_B_retention':
        assert l['B_birth'] == 0 and l['external_B'] == 0
        assert l['particle_export'] == 0 and not row['completed']
        assert row['assay']['in_f'] == 0 and row['assay']['in_m'] == 0
    elif a == 'no_B_retention_ref':
        assert l['B_birth'] == 0 and l['external_B'] == 0
        assert l['particle_export'] == 0 and row['completed']
        assert l['in_f'] > 0 and l['in_m'] > 0
    elif a == 'permeant':
        assert l['particle_export'] > 0 and not row['completed']
    elif a == 'B_rescue':
        assert l['B_birth'] == 0 and l['external_B'] > 0
        assert l['particle_export'] == 0 and row['completed'] and both
    elif a == 'puncture':
        assert row['assay']['in_f'] == 0 and not row['completed']
    elif a == 'rival_puncture':
        assert row['assay']['in_f'] > 0 and row['completed']
    elif a == 'puncture_non_gate':
        assert row['assay']['in_f'] > 0 and row['assay']['in_m'] > 0
        assert row['completed']


def main():
    errors = []
    snap = json.loads((RESULT / 'pre_run_snapshot.json').read_text())

    # 1. source hashes (frozen source of truth = declaration + simulation code)
    for name, digest in snap.items():
        p = ROOT / name
        if not p.exists():
            errors.append(f'source {name} missing')
        elif sha256(p) != digest:
            errors.append(f'source {name} hash drift')

    rows = load_rows(RESULT / 'rows.jsonl')
    by_key = {(r['seed'], r['history'], r['arm']): r for r in rows}

    # 2. coverage
    if len(rows) != 8 * 2 * len(ARMS):
        errors.append(f'row count {len(rows)} != {8 * 2 * len(ARMS)}')
    if len(by_key) != len(rows):
        errors.append('duplicate conditions')
    for s in SEEDS:
        for h in (0, 1):
            for a in ARMS:
                if (s, h, a) not in by_key:
                    errors.append(f'missing row {s}/{h}/{a}')

    # 3+4. ledger identities and arm invariants
    for r in rows:
        assert r['ticks'] == 2048 and r['arm'] in ARMS
        assert r['seed'] in SEEDS and r['history'] in (0, 1)
        try:
            check_ledger(r)
            check_arm(r)
        except AssertionError as e:
            errors.append(str(e))

    # 5. gates
    gate = {}

    # G1 (T5 inertness): keep == reference == rival byte-identical, every individual
    g1 = []
    for s in SEEDS:
        for h in (0, 1):
            keep, ref, rival = (by_key[(s, h, a)] for a in ('keep', 'reference', 'rival'))
            ok = (keep['state_hash'] == ref['state_hash'] == rival['state_hash']
                  and keep['ledger'] == ref['ledger'] == rival['ledger']
                  and keep['final_inventory'] == ref['final_inventory']
                  == rival['final_inventory'])
            g1.append(ok)
    gate['G1_inertness'] = all(g1)

    # G3 (T2 exchange mediation): no_B_retention post-onset admission zero + dies;
    # twin survives.
    g3 = []
    for s in SEEDS:
        for h in (0, 1):
            nb = by_key[(s, h, 'no_B_retention')]
            ref = by_key[(s, h, 'no_B_retention_ref')]
            g3.append(nb['assay']['in_f'] == 0 and nb['assay']['in_m'] == 0
                      and not nb['completed'] and ref['completed'])
    gate['G3_exchange_mediation'] = all(g3)

    # G4 (D1 site vs count, decisive): puncture in_f==0, rival_puncture in_f>0, paired.
    g4 = []
    for s in SEEDS:
        for h in (0, 1):
            pu = by_key[(s, h, 'puncture')]
            rp = by_key[(s, h, 'rival_puncture')]
            g4.append(pu['assay']['in_f'] == 0 and rp['assay']['in_f'] > 0)
    gate['G4_D1_site_vs_count'] = all(g4)

    # G5 (D2 local admission): puncture_non_gate both channels admit.
    g5 = []
    for s in SEEDS:
        for h in (0, 1):
            pn = by_key[(s, h, 'puncture_non_gate')]
            g5.append(pn['assay']['in_f'] > 0 and pn['assay']['in_m'] > 0)
    gate['G5_D2_local_admission'] = all(g5)

    # G6 (T6 external rescue): external_B>0, B_birth==0, export==0, survives.
    g6 = []
    for s in SEEDS:
        for h in (0, 1):
            br = by_key[(s, h, 'B_rescue')]
            g6.append(br['ledger']['external_B'] > 0 and br['ledger']['B_birth'] == 0
                      and br['ledger']['particle_export'] == 0 and br['completed'])
    gate['G6_external_rescue'] = all(g6)

    for gname, passed in gate.items():
        if not passed:
            errors.append(f'gate failed: {gname}')

    # survival as a SEPARATE outcome
    survival = {a: sum(1 for s in SEEDS for h in (0, 1) if by_key[(s, h, a)]['completed'])
                for a in ARMS}

    # D3 (semipermeability) and D5 (renewal), reported not gated
    keep_rows = [by_key[(s, h, 'keep')] for s in SEEDS for h in (0, 1)]
    d3 = all(r['ledger']['particle_export'] == 0 and r['ledger']['in_f'] > 0
             and r['ledger']['in_m'] > 0 for r in keep_rows)
    d5_birth = min(r['ledger']['B_birth'] for r in keep_rows)

    # G2 (T1 retention continuity) is a runner-level check on the AC10 seed family
    # (1300-1303), pinned by test_ac114.py; noted here, not recomputed from this table.

    ok = not errors
    print('audit ac114_results_v1 ->', 'PASS' if ok else 'FAIL')
    for e in errors[:60]:
        print('  ERROR:', e)
    print('  rows:', len(rows), 'snapshot files:', len(snap))
    print('  gates:', json.dumps(gate))
    print('  survival (of 16):', json.dumps(survival))
    print('  D3 semipermeability (keep, all 16):', d3)
    print('  D5 renewal: min keep B_birth =', d5_birth, '-> turnover >=', round(d5_birth / 20, 1), 'x')
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
