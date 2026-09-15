"""AC45: the repair-capability effect is a FAMILY effect, not one endpoint. A frozen study.

The claim
---------
Repair-maintained register occupancy raises the organism's *production and maintenance* family of
endpoints over a run, relative to its absence, **with corruption absent** (`reg_rate = 0.0`), so AC14's
integrity channel is off by construction.

The family is three quantities, not one:
    ledger.W_birth        W-region births (repair-catalyst production)
    ledger.converted      fuel -> energy conversion (metabolic throughput)
    ledger.memory_writes  memory renewal writes (maintenance)

Why a family, and why these three
---------------------------------
AC44 (engineering) showed the repair-capability effect is ENDPOINT-GENERAL at AC43's final seeds
(8-15): six of six measured quantities rise. But the GATE OUTCOME is endpoint-dependent -- `spent_m`
has the same 87.5% impaired fraction as `W_birth` yet p = 0.0127, above the 0.01 bar, so had it been
the registered endpoint AC43 would have failed its significance gate while passing the rest. A single
endpoint is a bet the survey cannot hedge; a family with a declared rule is the honest shape.

The three members are the *production/maintenance* endpoints, chosen to be independent of one another
and not derived aggregates:
  * `spent_e` and `spent_m` are total-spending sums. AC4's frozen conservation law ties them linearly
    to the production quantities (`spent_m == writes + 4*(W_birth+C_birth) + 2*B_birth`; energy
    balances `8*converted - spent_e`), so they carry no evidence beyond the production endpoints and
    are excluded as double counts. (`spent_e` clears p <= 0.001 on final seeds too -- 0.000895 -- but
    it is a spending aggregate, not a production/maintenance output.)
  * `deposits` is 100% impaired (no heterogeneity), so it fails the bimodality requirement the claim
    carries.
  * `productivity_kept` is inverted (the cut arm scores higher), already flagged by AC42.

The family rule, declared in advance
------------------------------------
  1. every member: median paired difference > 0 AND impaired fraction >= 0.75;
  2. at least 2 of 3 members resolve at p <= 0.01 on the exact sign-flip test.

Both clauses are frozen; no threshold may move after results are seen.

Declared from AC44's measurement at AC43's final seeds (8-15, corruption absent):
    W_birth        median diff 161.0   impaired 87.5%   p 0.000105
    converted      median diff 475.5   impaired 87.5%   p 0.000630
    memory_writes  median diff 1230.5  impaired 87.5%   p 0.000290
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac19
import ac38_variance as ac38

FAMILY = ('W_birth', 'converted', 'memory_writes')
CAPABLE = 'two_way'
CUT = 'two_way_no_repair'
PROTECTED = 'two_way_protected'
REG_RATE = 0.0                    # corruption absent: AC14's integrity channel off by construction
FINAL_SEEDS = tuple(range(16, 24))  # fresh: engineering used 0-7, AC43 finals used 8-15
ENGINEERING_SEEDS = tuple(range(8))
HISTORIES = (0, 1)
IMPAIRED_FLOOR = 0.75
P_BAR = 0.01
MIN_N = 8
N_SIGNIFICANT = 2                # the family significance clause: at least 2 of 3 at p <= 0.01
SOURCES = ['ac45_family.py', 'ac19.py', 'ac38_variance.py', 'AC45_PROTOCOL_v1.md']


def quantity(arm, seed, history, q):
    return float(ac19.run(seed, history, arm, reg_rate=REG_RATE)['ledger'][q])


def individuals(seeds=FINAL_SEEDS, histories=HISTORIES):
    return [(s, h) for s in seeds for h in histories]


def run_study(seeds=FINAL_SEEDS, histories=HISTORIES):
    rows = []
    for s, h in individuals(seeds, histories):
        row = dict(seed=s, history=h)
        for q in FAMILY:
            cap = quantity(CAPABLE, s, h, q)
            cut = quantity(CUT, s, h, q)
            pro = quantity(PROTECTED, s, h, q)
            row[f'{q}_capable'] = cap
            row[f'{q}_cut'] = cut
            row[f'{q}_protected'] = pro
            row[f'{q}_difference'] = cap - cut
        rows.append(row)
    return rows


def per_endpoint(rows):
    out = {}
    for q in FAMILY:
        d = np.asarray([r[f'{q}_difference'] for r in rows], dtype=float)
        res = ac38.sign_flip_test(list(d))
        pro = np.asarray([r[f'{q}_protected'] - r[f'{q}_cut'] for r in rows], dtype=float)
        out[q] = dict(p=res['p'], n=res['n'],
                      median=float(np.median(d)), mean=float(np.mean(d)),
                      impaired=float(np.mean(d > 0)), min=float(d.min()), max=float(d.max()),
                      protected_median=float(np.median(pro)))
    return out


def gates(rows, seeds=FINAL_SEEDS, histories=HISTORIES):
    per = per_endpoint(rows)
    g = {}
    g['G1_family_direction_and_impairment'] = bool(
        all(per[q]['median'] > 0 and per[q]['impaired'] >= IMPAIRED_FLOOR for q in FAMILY))
    n_sig = sum(1 for q in FAMILY if per[q]['p'] <= P_BAR)
    g['G2_family_significance'] = bool(n_sig >= N_SIGNIFICANT)
    g['G3_heterogeneity_present'] = bool(all(0.0 < per[q]['impaired'] < 1.0 for q in FAMILY))
    g['G4_protected_variant_above_cut'] = bool(all(per[q]['protected_median'] > 0 for q in FAMILY))
    expected = [(s, h) for s in seeds for h in histories]
    keys = [(r['seed'], r['history']) for r in rows]
    g['G5_all_individuals_complete'] = bool(
        len(rows) == len(expected) and len(set(keys)) == len(expected))
    g['G6_determinism'] = None
    return g, per


def preflight(protocol='AC45_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), (
        f'runner hashes {sorted(set(SOURCES))} but the protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared), 'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS, root='ac45_results_v1'):
    preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = run_study(seeds)
    with (outdir / 'rows.jsonl').open('x') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    g, per = gates(rows, seeds)
    g['G6_determinism'] = bool(run_study(seeds) == rows)
    summary = dict(n=len(rows),
                   per_endpoint={q: per[q] for q in FAMILY},
                   n_significant=sum(1 for q in FAMILY if per[q]['p'] <= P_BAR),
                   significant=[q for q in FAMILY if per[q]['p'] <= P_BAR])
    (outdir / 'results.json').write_text(json.dumps(
        dict(family=list(FAMILY), impaired_floor=IMPAIRED_FLOOR, p_bar=P_BAR,
             n_significant=N_SIGNIFICANT, seeds=list(seeds), histories=list(HISTORIES),
             gates=g, summary=summary, rows=rows), indent=2))
    print(json.dumps(dict(gates=g, summary=summary), indent=2))
    return g, summary


def engineering(seeds=ENGINEERING_SEEDS, histories=HISTORIES):
    """The AC40 four-check framework on the family endpoints at engineering seeds (0-7), run
    BEFORE the protocol is written. No frozen directory: this informs the protocol, it does not
    judge the finals."""
    from ac40_criterion import resolvability, effect_size, stability
    rows = run_study(seeds, histories)
    report = {}
    for q in FAMILY:
        diffs = [r[f'{q}_difference'] for r in rows]
        live = [r[f'{q}_capable'] for r in rows]
        report[q] = dict(resolvability=resolvability(diffs),
                         effect_size=effect_size(diffs),
                         stability=stability(diffs),
                         headroom=dict(ceiling='none (open-ended count)',
                                       live_sd=float(np.std(live)),
                                       not_saturated=bool(float(np.std(live)) > 0)))
    return report


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'finals':
        main()
    elif len(sys.argv) > 1 and sys.argv[1] == 'engineering':
        rep = engineering()
        for q in FAMILY:
            r = rep[q]
            print(f'{q:14s} p={r["resolvability"]["p"]:.4f} n={r["resolvability"]["n"]} '
                  f'median={r["effect_size"]["median"]:.0f} '
                  f'impaired={r["effect_size"]["impaired_fraction"]:.0%} '
                  f'live_sd={r["headroom"]["live_sd"]:.1f} resolved={r["resolvability"]["resolved"]}')
        json.dump(rep, open('/tmp/ac45_engineering.json', 'w'), indent=2)
    else:
        print(__doc__)
        print('Engineering (four-check, seeds 0-7):  .venv/bin/python -B ac45_family.py engineering')
        print('Declared finals (seeds 16-23):        .venv/bin/python -B ac45_family.py finals')
        print('Protocol: AC45_PROTOCOL_v1.md')
