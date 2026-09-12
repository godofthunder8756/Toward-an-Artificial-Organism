"""Audit frozen sources, complete data coverage, and exact checkpoint replay."""
import csv
import hashlib
import json
from pathlib import Path
from replay_e1 import replay


def read(p):
    with p.open() as f:
        return list(csv.DictReader(f))


def verify(root):
    project = Path(__file__).parent
    freeze = json.loads((project / 'E1_FREEZE.json').read_text())
    unchanged = all(hashlib.sha256((project / p).read_bytes()).hexdigest() == sha
                    for p, sha in freeze['files'].items())
    assert unchanged, 'Frozen protocol/code changed'
    run = json.loads((root / 'run.json').read_text())
    assert run['status'] == 'completed'
    cfg = run['config']
    evaluations = read(root / 'evaluation.csv')
    expected = cfg['seeds'] * 4 * 7 * cfg['eval_worlds']
    keys = {(r['seed'], r['variant'], r['stage'], r['world']) for r in evaluations}
    assert len(evaluations) == len(keys) == expected
    for r in evaluations:
        assert 0 < int(r['active_trials']) <= int(r['planned_trials'])
        assert float(r['precursor_rate_unconditional']) <= float(r['precursor_rate_active']) + 1e-12
        assert float(r['task_success_unconditional']) <= float(r['recall_accuracy_active']) + 1e-12
    seed = cfg['seed_start']
    original = read(root / f'seed_{seed}' / 'trace.csv')
    replayed_rows = 0
    for variant in ('neural_q', 'frozen_neural_q', 'tabular_q', 'fixed_drive_q'):
        for stage in ('pre', 'acute', 'acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness'):
            prior = [r for r in original if r['variant'] == variant and r['stage'] == stage]
            new = replay(root, seed, variant, stage)
            assert len(prior) == len(new)
            for a, b in zip(prior, new):
                for k, v in b.items():
                    assert float(a[k]) == float(v), (variant, stage, k)
            replayed_rows += len(new)
    budgets = read(root / 'budgets.csv')
    assert len(budgets) == cfg['seeds'] * 4 * 6
    report = {'frozen_files_unchanged': unchanged,
              'unique_evaluation_rows': len(evaluations),
              'independent_developmental_seeds': cfg['seeds'],
              'checkpoint_replays': 28,
              'exactly_reproduced_trace_rows': replayed_rows,
              'planned_maintenance_training_slots': sum(int(b['planned']) for b in budgets),
              'actual_active_maintenance_training_slots': sum(int(b['actual']) for b in budgets),
              'active_and_unconditional_metric_checks': 'passed',
              'raw_file_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (root / 'evaluation.csv', root / 'assays.csv', root / 'budgets.csv')}}
    (root / 'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('results', type=Path)
    args = p.parse_args()
    print(json.dumps(verify(args.results), indent=2))
