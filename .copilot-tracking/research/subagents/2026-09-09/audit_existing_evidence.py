"""Read-only evidence audit. Run from the workspace with python -B.

No training, file outputs, verifier edits, or tolerance-based verifier overrides.
All non-research original files are hashed before/after, including validation.
"""
import contextlib
import csv
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import platform
import sys
from collections import Counter, defaultdict
from typing import Any
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))


def emit(name, value):
    print(name + ' ' + json.dumps(value, sort_keys=True, allow_nan=False), flush=True)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def originals():
    result = {}
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_file() and rel.parts[0] not in ('.copilot-tracking', '.git'):
            st = p.stat()
            result[rel.as_posix()] = (st.st_size, st.st_mtime_ns, sha(p))
    return result


def no_writes(event, args):
    if event == 'open':
        _, mode, flags = args
        if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        ):
            raise PermissionError('Audit rejected filesystem write: ' + str(args[0]))
    if event in ('os.remove', 'os.rename', 'os.mkdir', 'os.rmdir', 'os.chmod', 'os.utime', 'os.link', 'os.symlink'):
        raise PermissionError('Audit rejected filesystem mutation: ' + event)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def coverage(data, fields, expected):
    actual = Counter(tuple(str(r[k]) for k in fields) for r in data)
    wanted = {tuple(map(str, key)) for key in expected}
    return dict(rows=len(data), unique=len(actual), expected=len(wanted),
                missing=len(wanted - actual.keys()), unexpected=len(actual.keys() - wanted),
                duplicate_keys=sum(v > 1 for v in actual.values()),
                missing_examples=sorted(wanted - actual.keys())[:3],
                unexpected_examples=sorted(actual.keys() - wanted)[:3])


def comparison(saved, fresh, discrete=()):
    result = dict(saved_rows=len(saved), replay_rows=len(fresh), exact_cells_differ=0,
                  discrete_cells_differ=0, outside_bound=0, max_abs=0., fields={}, examples=[])
    fields = Counter()
    for i, (a, b) in enumerate(zip(saved, fresh)):
        for k, value in b.items():
            if k not in a:
                result['outside_bound'] += 1
                continue
            if isinstance(value, bool):
                old = a[k].lower() == 'true'
                new = value
            elif isinstance(value, str):
                old, new = a[k], value
            else:
                old, new = float(a[k]), float(value)
            if old == new:
                continue
            result['exact_cells_differ'] += 1
            fields[k] += 1
            if k in discrete or isinstance(new, (str, bool)):
                result['discrete_cells_differ'] += 1
            if isinstance(new, (int, float)):
                delta = abs(new - old)
                result['max_abs'] = max(result['max_abs'], delta)
                if not np.isfinite(delta) or delta > 1e-12 + 1e-12 * abs(old):
                    result['outside_bound'] += 1
            if len(result['examples']) < 2:
                result['examples'].append(dict(row=i, field=k, saved=old, replay=new))
    result['fields'] = dict(fields)
    result['exact'] = len(saved) == len(fresh) and not result['exact_cells_differ'] and not result['outside_bound']
    return result


def replays_summary(reports):
    return dict(cases=len(reports), exact=sum(r['exact'] for r in reports),
                rows=sum(r['replay_rows'] for r in reports),
                length_mismatches=sum(r['saved_rows'] != r['replay_rows'] for r in reports),
                discrete_cells_differ=sum(r['discrete_cells_differ'] for r in reports),
                outside_bound=sum(r['outside_bound'] for r in reports),
                exact_cells_differ=sum(r['exact_cells_differ'] for r in reports),
                max_abs=max((r['max_abs'] for r in reports), default=0),
                cases_detail=[{k: v for k, v in r.items() if k not in ('fields', 'examples')} for r in reports],
                differing_fields=dict(sum((Counter(r['fields']) for r in reports), Counter())),
                first_examples=[r for r in reports if not r['exact']][:2])


def same_csv(a, b):
    canonical = lambda rs: Counter(tuple(sorted(r.items())) for r in rs)
    return canonical(a) == canonical(b)


def forbidden_training(*args, **kwargs):
    raise RuntimeError('Training/optimizer step is prohibited in this audit')


sys.addaudithook(no_writes)
before = originals()
emit('BASELINE', dict(files=len(before), bytes=sum(x[0] for x in before.values()),
                      tree_content_sha256=hashlib.sha256(json.dumps({k: v[2] for k, v in before.items()}, sort_keys=True).encode()).hexdigest(),
                      validation={k: v[2] for k, v in before.items() if k.endswith('VALIDATION.json')}))

try:
    import numpy as np
    import pilot
    import verify_e1
    import verify_e2
    from replay_e1 import replay
    from e2.model import Config, Network
    from e2.experiment import rollout
    from e1.circuits import Adam, Circuit

    config_out = io.StringIO()
    with contextlib.redirect_stdout(config_out):
        np.show_config()
    emit('ENVIRONMENT', dict(python=platform.python_version(), executable=sys.executable,
                             numpy=np.__version__, platform=platform.platform(), bytecode_disabled=sys.dont_write_bytecode,
                             numpy_config=config_out.getvalue()))
    runs = {e: load(p + '/run.json') for e, p in [('E0', 'results'), ('E1', 'e1_results'), ('E2', 'e2_results')]}
    for e, run in runs.items():
        emit(e + '_MANIFEST', run)
    for e, entry in [('E1', 'files'), ('E2', 'sources')]:
        frozen = load(e + '_FREEZE.json')[entry]
        current = {k: sha(ROOT / k) for k in frozen}
        emit(e + '_FREEZE', dict(entries=len(frozen), matched=sum(current[k] == v for k, v in frozen.items()),
                                 differences={k: dict(recorded=v, current=current[k]) for k, v in frozen.items() if current[k] != v}))
    e1_source = {'e1/' + k: v for k, v in runs['E1']['source_hashes'].items()}
    e2_source = runs['E2']['sources']
    emit('SOURCE_AND_CONFIG', dict(
        e0_sha=sha(ROOT / 'pilot.py'), e0_matches=sha(ROOT / 'pilot.py') == runs['E0']['source_sha256'],
        e1_sources={k: sha(ROOT / k) == v for k, v in e1_source.items()},
        e1_initial_final_equal=runs['E1']['source_hashes'] == runs['E1']['final_source_hashes'],
        e2_sources={k: sha(ROOT / k) == v for k, v in e2_source.items()},
        e1_config_equal=load('e1/frozen_config.json') == runs['E1']['config'],
        e2_config_equal=load('e2/frozen_config.json') == runs['E2']['config'],
        e1_canonical_config_hash_matches=hashlib.sha256(json.dumps(runs['E1']['config'], sort_keys=True).encode()).hexdigest() == runs['E1']['config_sha256'],
        source_snapshot_dirs={e: (ROOT / folder / 'source').exists() for e, folder in [('E1', 'e1_results'), ('E2', 'e2_results')]}))
    package = load('PACKAGE_MANIFEST.json')
    missing, drift, matched = [], [], 0
    for rel, info in package['files'].items():
        if rel not in before:
            missing.append(rel)
        elif before[rel][0] != info['bytes'] or before[rel][2] != info['sha256']:
            drift.append(dict(path=rel, recorded=info, current_bytes=before[rel][0], current_sha256=before[rel][2]))
        else:
            matched += 1
    unlisted = sorted(set(before) - package['files'].keys())
    emit('PACKAGE', dict(version=package['version'], entries=len(package['files']), matched=matched, missing=missing,
                         drift=drift, unlisted_count=len(unlisted),
                         unlisted_top_level=dict(Counter(p.split('/')[0] for p in unlisted)),
                         unlisted_samples=unlisted[:12]))

    with contextlib.ExitStack() as guards:
        guards.enter_context(patch.object(pilot, 'train', forbidden_training))
        guards.enter_context(patch.object(Circuit, 'train', forbidden_training))
        guards.enter_context(patch.object(Adam, 'step', forbidden_training))
        guards.enter_context(patch.object(Network, 'add_learn', forbidden_training))
        checks = pilot.check_mechanisms()
        emit('E0_MECHANISMS', dict(checks=checks, matches_saved=checks == runs['E0']['mechanism_checks']))
        d0 = rows(ROOT / 'results/episodes.csv')
        scenarios = ('normal', 'scarcity', 'quality_shock')
        conditions = ('evolved', 'telemetry_clamped', 'reset_hidden', 'gain_disconnected', 'sham_repair', 'untrained', 'reflex')
        expected0 = ((sc, co, s, ep) for sc in scenarios for co in conditions
                     for s in range(1 if co == 'reflex' else 6) for ep in range(64))
        emit('E0_COVERAGE', coverage(d0, ('scenario', 'condition', 'seed', 'episode'), expected0))
        with np.load(ROOT / 'results/controllers.npz', allow_pickle=False) as z:
            weights = z['weights'].copy()
        e0_replay = pilot.rollout(weights, pilot.conditions(900000, 64, 600), 600, collect_trace=True)
        emit('E0_SELECTED_REPLAY', comparison(rows(ROOT / 'results/trace_seed0_episode0.csv'), e0_replay['trace'], ('step', 'action', 'active_before')))
        e0_reports = []
        for saved in load('results/summary.json'):
            sub = [r for r in d0 if r['scenario'] == saved['scenario'] and r['condition'] == saved['condition']]
            e0_vector = [float(np.mean([float(r['active_steps']) for r in sub if int(r['seed']) == s])) for s in sorted({int(r['seed']) for r in sub})]
            e0_reports.append(dict(scenario=saved['scenario'], condition=saved['condition'], mean=float(np.mean(e0_vector)),
                                   saved_mean_delta=float(np.mean(e0_vector)) - saved['mean_active_steps'],
                                   seed_vector_delta=float(np.max(np.abs(np.array(e0_vector) - saved['seed_mean_steps'])))))
        emit('E0_ESTIMATES', e0_reports)

        d1, d2 = rows(ROOT / 'e1_results/evaluation.csv'), rows(ROOT / 'e2_results/evaluation.csv')
        v1 = ('neural_q', 'frozen_neural_q', 'tabular_q', 'fixed_drive_q')
        s1 = ('pre', 'acute', 'acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness')
        v2 = ('plastic', 'static', 'shuffled')
        s2 = ('initial', 'developed', 'lesion_all', 'lesion_0', 'lesion_1', 'acute_normal', 'normal',
              'acute_rescue', 'rescue', 'acute_sham', 'sham', 'acute_lost', 'lost', 'acute_swap', 'swap', 'frozen_weights')
        emit('E1_COVERAGE', coverage(d1, ('seed', 'variant', 'stage', 'world'), itertools.product(range(100, 120), v1, s1, range(8))))
        emit('E2_COVERAGE', coverage(d2, ('seed', 'variant', 'history', 'stage', 'world'), itertools.product(range(200, 216), v2, (0, 1), s2, range(6))))
        for name, data, directory in [('E1', d1, 'e1_results'), ('E2', d2, 'e2_results')]:
            parts = [r for p in sorted((ROOT / directory).glob('seed_*/evaluation.csv')) for r in rows(p)]
            emit(name + '_PER_SEED_TABLES', dict(rows=len(parts), equal_top_level=same_csv(data, parts)))
        emit('METRIC_INVARIANTS', dict(
            e1_world_mode_errors=sum(int(r['world_seed']) != 900000000 + int(r['world']) or r['mode'] != ('dependency' if r['stage'] in ('acute', 'acquired') else r['stage']) for r in d1),
            e1_denominator_errors=sum(not (0 < int(r['active_trials']) <= int(r['planned_trials']) == 128) or abs(float(r['precursor_rate_active']) * int(r['active_trials']) - int(r['precursor_count'])) > 1e-10 or abs(float(r['precursor_rate_unconditional']) * 128 - int(r['precursor_count'])) > 1e-10 or abs(float(r['recall_accuracy_active']) * int(r['active_trials']) - float(r['task_success_unconditional']) * 128) > 1e-10 for r in d1),
            e2_denominator_errors=sum(not (0 <= float(r['recall']) <= float(r['active_fraction']) <= 1) or abs(float(r['a_active']) * float(r['active_fraction']) - float(r['a_rate'])) > 1e-12 or abs(float(r['b_active']) * float(r['active_fraction']) - float(r['b_rate'])) > 1e-12 or float(r['a_rate']) + float(r['b_rate']) > float(r['active_fraction']) + 1e-12 for r in d2),
            e2_max_evaluation_ledger=max(float(r['max_balance_error']) for r in d2)))
        budgets = rows(ROOT / 'e1_results/budgets.csv')
        emit('E1_BUDGETS', dict(coverage=coverage(budgets, ('seed', 'variant', 'phase'), itertools.product(range(100, 120), v1, ('pre', 'acquisition', 'dependency', 'rescue', 'sham', 'lost_usefulness'))),
                                 planned=sum(int(r['planned']) for r in budgets), actual=sum(int(r['actual']) for r in budgets),
                                 per_seed_equal=same_csv(budgets, [r for p in (ROOT / 'e1_results').glob('seed_*/budgets.csv') for r in rows(p)])))
        saved1, saved2 = load('e1_results/summary.json'), load('e2_results/summary.json')
        g1, g2 = defaultdict(list), defaultdict(list)
        for r in d1:
            g1[int(r['seed']), r['variant'], r['stage']].append(r)
        for r in d2:
            g2[int(r['seed']), r['variant'], r['stage']].append(r)
        def vec1(v, st, k):
            return np.array([np.mean([float(r[k]) for r in g1[s, v, st]]) for s in range(100, 120)])
        def vec2(v, st, k, h=None):
            return np.array([np.mean([float(r[k]) for r in g2[s, v, st] if h is None or int(r['history']) == h]) for s in range(200, 216)])
        point_deltas1, vector_deltas1 = [], []
        for v, stages in saved1['conditions'].items():
            for st, metrics in stages.items():
                for k, stat in metrics.items():
                    a = vec1(v, st, k)
                    point_deltas1.append(abs(float(a.mean()) - stat['mean']))
                    vector_deltas1.append(float(np.max(np.abs(a - stat['seed_values']))))
        cdefs = dict(acquired_minus_pre_precursor=('acquired', 'pre', 'precursor_rate_active'),
                     acquired_minus_acute_function=('acquired', 'acute', 'task_success_unconditional'),
                     dependency_minus_rescue_precursor=('dependency', 'rescue', 'precursor_rate_active'),
                     dependency_minus_sham_precursor=('dependency', 'sham', 'precursor_rate_active'),
                     dependency_minus_lost_usefulness_precursor=('dependency', 'lost_usefulness', 'precursor_rate_active'))
        c1: dict[str, dict[str, float]] = {}
        for v in v1:
            c1[v] = {}
            for key, (a, b, metric) in cdefs.items():
                vector = vec1(v, a, metric) - vec1(v, b, metric)
                stat = saved1['contrasts'][v][key]
                c1[v][key] = float(vector.mean())
                point_deltas1.append(abs(float(vector.mean()) - stat['mean']))
                vector_deltas1.append(float(np.max(np.abs(vector - stat['seed_values']))))
        emit('E1_ESTIMATES', dict(condition_statistics=224, max_mean_delta=max(point_deltas1), max_seed_vector_delta=max(vector_deltas1),
                                 primary_stages={st: {k: float(vec1('neural_q', st, k).mean()) for k in ('precursor_rate_active', 'task_success_unconditional', 'completion')} for st in s1},
                                 contrasts=c1, saved_gates=saved1['gates']))
        assays = rows(ROOT / 'e1_results/assays.csv')
        emit('E1_ASSAYS', dict(coverage=coverage(assays, ('seed',), ((s,) for s in range(100, 120))),
                                means={k: float(np.mean([float(r[k]) for r in assays])) for k in saved1['memory_assays']},
                                every_seed_gate=all(float(r['intact_accuracy']) >= .85 and float(r['lesion_accuracy']) <= .35 for r in assays),
                                raw_hash_matches={k: sha(ROOT / 'e1_results' / k) == v for k, v in load('e1_results/VALIDATION.json')['raw_file_hashes'].items()}))
        point_deltas2, vector_deltas2 = [], []
        c2: dict[str, Any] = {}
        developed: dict[str, dict[str, float]] = {}
        for v in v2:
            for st, metrics in saved2['summary'][v].items():
                for k, stat in metrics.items():
                    vector = vec2(v, st, k)
                    point_deltas2.append(abs(float(vector.mean()) - stat['mean']))
                    vector_deltas2.append(float(np.max(np.abs(vector - stat['seeds']))))
            developed[v] = {k: float(vec2(v, 'developed', k).mean()) for k in ('recall', 'active_fraction', 'completion')}
            rate = lambda st: vec2(v, st, 'a_rate') + vec2(v, st, 'b_rate')
            vectors = dict(
                development=vec2(v, 'developed', 'recall') - vec2(v, 'initial', 'recall'),
                history_priority=((vec2(v, 'developed', 'a_rate', 0) - vec2(v, 'developed', 'b_rate', 0)) - (vec2(v, 'developed', 'a_rate', 1) - vec2(v, 'developed', 'b_rate', 1))) / 2,
                history_dependence=((vec2(v, 'lesion_1', 'recall', 0) - vec2(v, 'lesion_0', 'recall', 0)) - (vec2(v, 'lesion_1', 'recall', 1) - vec2(v, 'lesion_0', 'recall', 1))) / 2,
                swap_recovery=vec2(v, 'swap', 'recall') - vec2(v, 'acute_swap', 'recall'),
                normal_minus_lost_collection=rate('normal') - rate('lost'), lost_collection=rate('lost'),
                normal_minus_rescue_collection=rate('normal') - rate('rescue'),
                normal_minus_frozen_recall=vec2(v, 'normal', 'recall') - vec2(v, 'frozen_weights', 'recall'))
            c2[v] = {}
            for key, vector in vectors.items():
                stat = saved2['contrasts'][v][key]
                point_deltas2.append(abs(float(vector.mean()) - stat['mean']))
                vector_deltas2.append(float(np.max(np.abs(vector - stat['seeds']))))
                c2[v][key] = dict(mean=float(vector.mean()))
                if key in ('history_priority', 'history_dependence'):
                    c2[v][key]['seed_values'] = vector.tolist()
        for rival in ('static', 'shuffled'):
            vector = vec2('plastic', 'developed', 'recall') - vec2(rival, 'developed', 'recall')
            key = 'plastic_minus_' + rival
            c2[key] = dict(mean=float(vector.mean()), seed_values=vector.tolist())
            point_deltas2.append(abs(float(vector.mean()) - saved2['contrasts'][key]['mean']))
            vector_deltas2.append(float(np.max(np.abs(vector - saved2['contrasts'][key]['seeds']))))
        emit('E2_ESTIMATES', dict(developed=developed, contrasts=c2, max_mean_delta=max(point_deltas2),
                                 max_seed_vector_delta=max(vector_deltas2), saved_gates=saved2['gates']))
        diagnostics = rows(ROOT / 'e2_results/diagnostics.csv')
        ds = load('e2_results/DIAGNOSTICS.json')['summary']
        recomputed_ds = {v: {k: float(np.mean([float(r[k]) for r in diagnostics if r['variant'] == v])) for k in ds[v]} for v in v2}
        emit('E2_SAVED_DIAGNOSTICS', dict(coverage=coverage(diagnostics, ('seed', 'variant', 'history'), itertools.product(range(200, 216), v2, (0, 1))),
                                         summary=recomputed_ds, matches_saved=recomputed_ds == ds, rerun=False))

        allowed = {(ROOT / e / 'VALIDATION.json').resolve() for e in ('e1_results', 'e2_results')}
        captured = {}
        def capture(path, data, *args, **kwargs):
            if path.resolve() not in allowed:
                raise PermissionError('Unexpected validation destination: ' + str(path))
            captured[path.relative_to(ROOT).as_posix()] = json.loads(data)
            return len(data)
        details1 = {}
        original_trace = rows(ROOT / 'e1_results/seed_100/trace.csv')
        def traced_e1(root, seed, variant, stage):
            fresh = replay(root, seed, variant, stage)
            prior = [r for r in original_trace if r['variant'] == variant and r['stage'] == stage]
            report = comparison(prior, fresh, ('trial', 'action', 'precursor', 'gap', 'distance', 'cue_a', 'cue_b', 'door', 'success', 'alive_after'))
            report.update(variant=variant, stage=stage)
            details1[variant, stage] = report
            return fresh
        with patch.object(Path, 'write_text', capture), patch.object(verify_e1, 'replay', traced_e1):
            try:
                result1 = verify_e1.verify(ROOT / 'e1_results')
                emit('E1_VERIFIER', dict(status='returned', result=result1))
            except (AssertionError, SystemExit) as exc:
                emit('E1_VERIFIER', dict(status=type(exc).__name__, message=str(exc), replays_before_exit=len(details1)))
        # Independent supplement, never bypasses or changes the original verifier.
        for variant, stage in itertools.product(v1, s1):
            if (variant, stage) not in details1:
                traced_e1(ROOT / 'e1_results', 100, variant, stage)
        emit('E1_SELECTED_REPLAYS', replays_summary(list(details1.values())))

        details2: list[dict[str, Any]] = []
        stages_replay = ('developed', 'normal', 'rescue', 'sham', 'lost', 'swap', 'frozen_weights')
        cases2 = list(itertools.product(v2, (0, 1), stages_replay))
        def traced_e2(net, body, seed, rounds_count, mode, variant):
            v, h, st = cases2[len(details2)]
            assert v == variant and seed == 80000000
            fresh = rollout(net, body, seed, rounds_count, mode, variant)
            prior = rows(ROOT / f'e2_results/seed_200_{v}_h{h}/{st}_trace.csv')
            report = comparison(prior, fresh, ('trial', 'active', 'action', 'correct', 'resets'))
            report.update(variant=v, history=h, stage=st)
            details2.append(report)
            return fresh
        with patch.object(Path, 'write_text', capture), patch.object(verify_e2, 'rollout', traced_e2):
            try:
                verify_e2.verify(ROOT / 'e2_results')
                emit('E2_VERIFIER', dict(status='returned'))
            except (AssertionError, SystemExit) as exc:
                emit('E2_VERIFIER', dict(status=type(exc).__name__, message=str(exc)))
        emit('E2_SELECTED_REPLAYS', replays_summary(details2))
        emit('CAPTURED_VALIDATION_WRITES', {k: {key: value for key, value in v.items() if key != 'replays'} for k, v in captured.items()})
        cfg = Config(**runs['E2']['config'])
        net, body = Network.load(ROOT / 'e2_results/seed_200_plastic_h0/developed.npz', cfg)
        with np.load(ROOT / 'e2_results/seed_200_plastic_h0/developed.npz', allow_pickle=False) as z:
            saved_keys = {k: list(z[k].shape) for k in z.files}
        emit('E2_CHECKPOINT_STATE', dict(saved_arrays=saved_keys, saved_arrays_finite=all(np.isfinite(v).all() for v in net.p.values()),
                                         dense_parameter_slots=sum(v.size for v in net.p.values()), allowed_edges=int(net.mask.sum()),
                                         loaded_target_equals_p=all(np.array_equal(net.p[k], net.target[k]) for k in net.p),
                                         loaded_adam_t=net.opt.t, loaded_adam_m_v_zero=all(not a.any() for d in (net.opt.m, net.opt.v) for a in d.values()),
                                         loaded_replay_len=len(net.buf), loaded_cursor=net.cursor, restored_update_count=net.updates,
                                         checkpoint_count=len(list((ROOT / 'e2_results').glob('seed_*/*.npz')))))
finally:
    after = originals()
    changed = [k for k in before.keys() & after.keys() if before[k] != after[k]]
    added = sorted(after.keys() - before.keys())
    removed = sorted(before.keys() - after.keys())
    emit('PRESERVATION', dict(before_files=len(before), after_files=len(after), changed=sorted(changed), added=added, removed=removed,
                              byte_hashes_and_sizes_mtimes_equal=before == after,
                              validation={k: v[2] for k, v in after.items() if k.endswith('VALIDATION.json')},
                              tree_content_sha256=hashlib.sha256(json.dumps({k: v[2] for k, v in after.items()}, sort_keys=True).encode()).hexdigest()))
    if before != after:
        raise RuntimeError('Original file preservation check failed')