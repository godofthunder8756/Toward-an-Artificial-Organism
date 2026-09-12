"""Seed-level paired inference and exportable research figure; no timestep p values."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np


def read(path):
    with Path(path).open() as f:
        return list(csv.DictReader(f))


def interval(values):
    a = np.array(values, dtype=float)
    rng = np.random.default_rng(20260909)
    samples = a[rng.integers(0, len(a), (10000, len(a)))].mean(1)
    return {'mean': float(a.mean()), 'ci95': np.quantile(samples, [.025, .975]).tolist(),
            'n_seeds': len(a), 'seed_values': a.tolist()}


def analyze(root, make_figure=True):
    rows = read(root / 'evaluation.csv')
    seeds = sorted(set(int(r['seed']) for r in rows))
    variants = sorted(set(r['variant'] for r in rows))
    stages = ('pre', 'acute', 'acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness')
    metrics = ('precursor_rate_active', 'precursor_rate_unconditional',
               'task_success_unconditional', 'recall_accuracy_active', 'completion',
               'net_energy_per_planned_trial', 'mean_conductance', 'active_trials')
    values = {}
    summary = {'method': '95% percentile bootstrap over paired developmental seed means; 10,000 resamples',
               'seeds': seeds, 'conditions': {}, 'contrasts': {}, 'gates': {}}
    for v in variants:
        summary['conditions'][v] = {}
        for stage in stages:
            summary['conditions'][v][stage] = {}
            for metric in metrics:
                per_seed = [np.mean([float(r[metric]) for r in rows
                                     if r['variant'] == v and r['stage'] == stage
                                     and int(r['seed']) == seed]) for seed in seeds]
                values[v, stage, metric] = np.array(per_seed)
                summary['conditions'][v][stage][metric] = interval(per_seed)
        contrasts = {
            'acquired_minus_pre_precursor': ('acquired', 'pre', 'precursor_rate_active'),
            'acquired_minus_acute_function': ('acquired', 'acute', 'task_success_unconditional'),
            'dependency_minus_rescue_precursor': ('dependency', 'rescue', 'precursor_rate_active'),
            'dependency_minus_sham_precursor': ('dependency', 'sham', 'precursor_rate_active'),
            'dependency_minus_lost_usefulness_precursor': ('dependency', 'lost_usefulness', 'precursor_rate_active'),
        }
        summary['contrasts'][v] = {name: interval(values[v, a, m] - values[v, b, m])
                                   for name, (a, b, m) in contrasts.items()}
        cs = summary['contrasts'][v]
        gates = {name: c['mean'] >= (.15 if name.endswith('function') else .05)
                 and c['ci95'][0] > 0 for name, c in cs.items()}
        summary['gates'][v] = {'behavioral_gates': gates,
                               'all_behavioral_gates_pass': all(gates.values())}
    summary['neural_minus_tabular'] = {
        stage: interval(values['neural_q', stage, 'task_success_unconditional'] -
                        values['tabular_q', stage, 'task_success_unconditional'])
        for stage in ('acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness')}
    assays = read(root / 'assays.csv')
    summary['memory_assays'] = {m: interval([float(a[m]) for a in assays])
                                for m in ('naive_accuracy', 'intact_accuracy', 'lesion_accuracy',
                                          'restored_accuracy', 'degraded_accuracy')}
    summary['memory_gate'] = all(float(a['intact_accuracy']) >= .85
                                 and float(a['lesion_accuracy']) <= .35 for a in assays)
    summary['interpretation_limit'] = ('The primary neural controller IS ordinary energy-based Q learning. '
        'Passing these gates is evidence of a learned instrumental priority in this scaffolded benchmark, '
        'not evidence for a new motivational mechanism, local neural construction, life, or consciousness. '
        'Intervals are descriptive; gates are conjunctive, not independent discoveries.')
    (root / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    lines = ['# E1 results', '', f'{len(seeds)} independent developmental seeds. '
             'Numbers below are seed-mean estimates. See summary.json for paired intervals.', '',
             '| Controller | Stage | Precursor % | Recall successes / planned trials % | Completion % |',
             '| --- | --- | ---: | ---: | ---: |']
    for v in variants:
        for stage in stages:
            c = summary['conditions'][v][stage]
            vals = [100*c[m]['mean'] for m in ('precursor_rate_active', 'task_success_unconditional', 'completion')]
            lines.append(f'| {v} | {stage} | {vals[0]:.1f} | {vals[1]:.1f} | {vals[2]:.1f} |')
    lines += ['', '## Paired contrasts', '', '| Controller | Contrast | Difference, percentage points | 95% seed bootstrap interval |',
              '| --- | --- | ---: | --- |']
    for v in variants:
        for name, c in summary['contrasts'][v].items():
            lo, hi = [100*x for x in c['ci95']]
            lines.append(f"| {v} | {name} | {100*c['mean']:.1f} | [{lo:.1f}, {hi:.1f}] |")
    lines += ['', summary['interpretation_limit'], '']
    (root / 'RESULTS.md').write_text('\n'.join(lines))
    if make_figure:
        plot(root, summary)
    return summary


def plot(root, summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    stages = ('pre', 'acute', 'acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness')
    labels = ('Before\nwithdrawal', 'Immediate\nwithdrawal', 'After\nlearning', 'Continued\ndependency',
              'External\nrepair', 'Ineffective\nprecursor', 'Memory no\nlonger useful')
    fig, axes = plt.subplots(2, 1, figsize=(12.5, 8), sharex=True, layout='constrained')
    styles = [('neural_q', 'Neural Q learning', '#236eaa', -.12),
              ('tabular_q', 'Tabular Q learning', '#208673', 0),
              ('frozen_neural_q', 'Frozen neural policy', '#858890', .12)]
    for ax, metric, ylabel in zip(axes, ('precursor_rate_active', 'task_success_unconditional'),
                                 ('Precursor choices (% of active trials)', 'Correct recall (% of planned trials)')):
        for variant, label, color, offset in styles:
            data = [summary['conditions'][variant][s][metric] for s in stages]
            means = np.array([d['mean'] * 100 for d in data])
            intervals = np.array([np.array(d['ci95'])*100 for d in data]).T
            ax.errorbar(np.arange(len(stages))+offset, means,
                        yerr=np.maximum(0, np.vstack([means-intervals[0], intervals[1]-means])),
                        fmt='o', capsize=3, color=color, label=label, markersize=5)
        ax.set_ylabel(ylabel)
        ax.set_ylim(-3, 103)
        ax.grid(axis='y', alpha=.18)
        ax.axvline(2.5, color='#999999', linewidth=1, linestyle='--')
    axes[0].legend(loc='upper left', bbox_to_anchor=(0, 1.24), ncol=3, frameon=False)
    axes[1].set_xticks(np.arange(len(stages)), labels)
    fig.suptitle('A learned maintenance priority — and its limits\n'
                 f"E1 scaffolded benchmark • {len(summary['seeds'])} developmental seeds • 95% seed bootstrap intervals",
                 fontsize=15)
    fig.supxlabel('Last four conditions branch from the same acquired-policy checkpoint.\n'
                  'Recall is still assayed when its food yield is zero. No language training.', fontsize=10)
    fig.savefig(root / 'E1_RESULTS.png', dpi=180)
    fig.savefig(root / 'E1_RESULTS.pdf')
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('out')
    args = parser.parse_args()
    s = analyze(Path(args.out))
    print(json.dumps({'memory_gate': s['memory_gate'], 'gates': s['gates']}, indent=2))
