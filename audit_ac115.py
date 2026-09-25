"""audit_ac115.py — re-derive the AC115 (I4) frozen confirmation from the saved table,
WITHOUT simulating.

Verifies, from `ac115_results_v1/rows.jsonl`, `results.json`, and the pre-run
snapshot only (stdlib, no `ac115`/`ac105` import):

  (1) source hashes match the pre-run snapshot (declaration + runner + frozen deps),
  (2) row coverage is complete (8 seeds x 2 histories x 13 arms = 208, no dupes),
  (3) the prespecified gates G1-G8 are recomputed from the saved rows,
  (4) the observer-discard (state-sufficiency) record is intact,
  (5) survival and the keep-arm mechanism-exercise endpoints are reported as
      separate outcomes.

This is the split-verification audit half (AC9's pattern). replay_ac115.py does
the sampled exact reruns; test_ac115.py pins the implementation law. The audit
does NOT import the runner (no simulation). It hardcodes the declared constants
(PUNCTURE_TICK=512, PUNCTURE_TICK_SIMULT=8192, CORRUPT_BITS=8, DESC_BITS=130)
exactly as the protocol declares them.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULT = ROOT / 'ac115_results_v1'
ARMS = ('keep', 'reference', 'rival',
        'puncture', 'rival_puncture', 'puncture_non_gate',
        'no_B', 'no_B_retention', 'no_B_retention_ref', 'B_rescue',
        'puncture_simult', 'rival_puncture_simult', 'permeant')
SEEDS = list(range(6600, 6608))
TICKS = 16384
PUNCTURE_TICK = 512
PUNCTURE_TICK_SIMULT = 8192
CORRUPT_BITS = 8
DESC_BITS = 130


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def alive_admission(row, channel, lo):
    """Per-channel per-contact admission over the alive window [lo, first_dead]. Mirrors
    ac115._alive_admission exactly (a react call on action 0/1 IS an attempted contact)."""
    end = row['first_dead'] if row['first_dead'] is not None else TICKS
    lo = lo if lo is not None else 0
    attempted = admitted = 0
    for (t, ch, adm) in row['admission_events']:
        if ch == channel and lo <= t < end:
            attempted += 1
            admitted += adm
    return attempted, admitted


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
    results = json.loads((RESULT / 'results.json').read_text())
    ident = results['gates']['arm_identity']

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

    # basic row sanity
    for r in rows:
        assert r['ticks'] == TICKS and r['arm'] in ARMS
        assert r['seed'] in SEEDS and r['history'] in (0, 1)

    gate = {}

    # G1 -- single-change license: keep/rival/reference byte-identical to each other AND to
    # AC105 persistent_budget (ac105_hash recorded in results.json at collect time);
    # non-vacuous (corruption applied + reconstruction/succession recorded active).
    g1 = []
    for s in SEEDS:
        for h in (0, 1):
            keep = by_key[(s, h, 'keep')]
            ref = by_key[(s, h, 'reference')]
            rival = by_key[(s, h, 'rival')]
            ac105_hash = ident[f'{s}/{h}']['ac105_hash']
            same = (keep['state_hash'] == ref['state_hash'] == rival['state_hash']
                    == ac105_hash)
            nonvac = (keep['fw_at_corrupt'] == CORRUPT_BITS
                      and keep['successions'] >= 1
                      and keep['flipped_still_wrong'] == 0)
            g1.append(same and nonvac)
    gate['G1_single_change_license'] = all(g1)

    # G2 -- D1 link-specific admission (paired per seed): puncture (site) ch0 alive-window
    # admission == 0 with attempted > 0; rival_puncture (count) ch0 admission > 0.
    g2 = []
    for s in SEEDS:
        for h in (0, 1):
            p = by_key[(s, h, 'puncture')]
            rp = by_key[(s, h, 'rival_puncture')]
            p_att, p_adm = alive_admission(p, 0, PUNCTURE_TICK)
            rp_att, rp_adm = alive_admission(rp, 0, PUNCTURE_TICK)
            g2.append(p_att > 0 and p_adm == 0 and rp_adm > 0)
    gate['G2_D1_link_specific_admission'] = all(g2)

    # G3 -- D2 local admission: puncture_non_gate admits > 0 on BOTH channels post-puncture.
    g3 = []
    for s in SEEDS:
        for h in (0, 1):
            r = by_key[(s, h, 'puncture_non_gate')]
            c0_att, c0_adm = alive_admission(r, 0, PUNCTURE_TICK)
            c1_att, c1_adm = alive_admission(r, 1, PUNCTURE_TICK)
            g3.append(c0_adm > 0 and c1_adm > 0)
    gate['G3_D2_local_admission'] = all(g3)

    # G4 -- T2 boundary production supports entry: no_B (site) gate links dead + admission==0
    # on both channels (non-vacuous on ch1) + does NOT complete; no_B_retention_ref (none)
    # admits every contact on both channels and completes.
    g4 = []
    for s in SEEDS:
        for h in (0, 1):
            nb = by_key[(s, h, 'no_B')]
            nr = by_key[(s, h, 'no_B_retention_ref')]
            nb0a, nb0d = alive_admission(nb, 0, nb['gate0_dead_tick'])
            nb1a, nb1d = alive_admission(nb, 1, nb['gate1_dead_tick'])
            nr0a, nr0d = alive_admission(nr, 0, nr['gate0_dead_tick'])
            nr1a, nr1d = alive_admission(nr, 1, nr['gate1_dead_tick'])
            ok = (nb['gate0_dead_tick'] is not None and nb['gate1_dead_tick'] is not None
                  and nb0d == 0 and nb1d == 0 and nb1a > 0 and not nb['completed']
                  and nr0d == nr0a and nr1d == nr1a and nr1a > 0 and nr['completed'])
            g4.append(ok)
    gate['G4_T2_boundary_supports_entry'] = all(g4)

    # G5 -- retention vs admission separated: no_B_retention (site) gate dead + admission==0
    # on both channels + does NOT complete; no_B_retention_ref admits and completes.
    g5 = []
    for s in SEEDS:
        for h in (0, 1):
            nbr = by_key[(s, h, 'no_B_retention')]
            nr = by_key[(s, h, 'no_B_retention_ref')]
            nbr0a, nbr0d = alive_admission(nbr, 0, nbr['gate0_dead_tick'])
            nbr1a, nbr1d = alive_admission(nbr, 1, nbr['gate1_dead_tick'])
            nr0a, nr0d = alive_admission(nr, 0, nr['gate0_dead_tick'])
            nr1a, nr1d = alive_admission(nr, 1, nr['gate1_dead_tick'])
            ok = (nbr['gate0_dead_tick'] is not None and nbr['gate1_dead_tick'] is not None
                  and nbr0d == 0 and nbr1d == 0 and nbr1a > 0 and not nbr['completed']
                  and nr0d == nr0a and nr1d == nr1a and nr1a > 0 and nr['completed'])
            g5.append(ok)
    gate['G5_retention_vs_admission'] = all(g5)

    # G6 -- endogenous renewal vs external: keep B_births>0, external_B==0, export==0;
    # B_rescue external_B>0, B_births==0, completes (labelled EXTERNAL).
    g6 = []
    for s in SEEDS:
        for h in (0, 1):
            k = by_key[(s, h, 'keep')]
            br = by_key[(s, h, 'B_rescue')]
            ok = (k['B_births'] > 0 and k['external_B'] == 0 and k['particle_export'] == 0
                  and br['external_B'] > 0 and br['B_births'] == 0 and br['completed'])
            g6.append(ok)
    gate['G6_endogenous_vs_external'] = all(g6)

    # G7 -- composition under stress: rival_puncture_simult reconstructs + holds desc +
    # completes; puncture_simult ch0 admission == 0 post-puncture under corruption+move.
    g7 = []
    for s in SEEDS:
        for h in (0, 1):
            rps = by_key[(s, h, 'rival_puncture_simult')]
            ps = by_key[(s, h, 'puncture_simult')]
            ps_att, ps_adm = alive_admission(ps, 0, PUNCTURE_TICK_SIMULT)
            ok = (rps['fw_at_corrupt'] == CORRUPT_BITS and rps['flipped_still_wrong'] == 0
                  and rps['description_correct'] == DESC_BITS and rps['successions'] >= 1
                  and rps['completed'] and ps_att > 0 and ps_adm == 0)
            g7.append(ok)
    gate['G7_composition_under_stress'] = all(g7)

    # G8 -- completeness (audit half; the exact rerun is replay_ac115's half).
    g8 = len(rows) == 8 * 2 * len(ARMS) and len(by_key) == len(rows)
    gate['G8_completeness'] = g8

    # 4. observer-discard (state sufficiency), recorded in results.json
    obs = results.get('observer_discard_keep', {})
    obs_ok = True
    obs_n = 0
    for key, entry in obs.items():
        obs_n += 1
        if not (entry.get('per_tick_identical') and entry.get('terminal_identical')):
            obs_ok = False
            errors.append(f'observer-discard not identical: {key}')

    # 5. survival (SEPARATE outcome) and keep-arm mechanism exercise
    survival = {a: sum(1 for s in SEEDS for h in (0, 1) if by_key[(s, h, a)]['completed'])
                for a in ARMS}
    keep_rows = [by_key[(s, h, 'keep')] for s in SEEDS for h in (0, 1)]
    exercise = {
        'reconstruction_all': all(r['fw_at_corrupt'] == CORRUPT_BITS
                                  and r['flipped_still_wrong'] == 0 for r in keep_rows),
        'succession_all': all(r['successions'] >= 1 and r['description_correct'] == DESC_BITS
                              for r in keep_rows),
        'relinquishment_all': all(r['relinquishments'] > 0 for r in keep_rows),
        'paid_updates_all': all(r['reg_writes'] > 0 and r['succ_writes'] > 0
                                and r['ctrl_writes'] > 0 for r in keep_rows),
        'boundary_production_all': all(r['B_births'] > 0 and r['particle_export'] == 0
                                       for r in keep_rows),
    }

    for gname, passed in gate.items():
        if not passed:
            errors.append(f'gate failed: {gname}')

    ok = not errors
    print('audit ac115_results_v1 ->', 'PASS' if ok else 'FAIL')
    for e in errors[:60]:
        print('  ERROR:', e)
    print('  rows:', len(rows), 'snapshot files:', len(snap))
    print('  gates:', json.dumps(gate))
    print('  observer-discard identical:', f'{obs_ok} ({obs_n} individuals)')
    print('  survival (of 16):', json.dumps(survival))
    print('  keep-arm exercise (all 16):', json.dumps(exercise))
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
