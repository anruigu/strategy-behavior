"""Readable derivatives of audited primary prospective scores; no refitting or rescoring."""
from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import tempfile

os.environ.setdefault('TMPDIR', '/shared/allie/home/.codex/tmp')
os.environ.setdefault('MPLCONFIGDIR', '/shared/allie/home/.codex/tmp/matplotlib-prediction')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np

from .secondary_analysis import snapshot, unchanged, validate_upstream_markers, verified_evaluation

TARGETS = ('action0', 'cooperation', 'coordination')
TARGET_LABELS = ('Action 0', 'Mutual cooperation', 'Coordination')
METHODS = (
    ('nash', 'Original equilibrium selector', '#70767A'),
    ('pair', 'Ordered model/opponent mean', '#303D48'),
    ('family', 'Game-family mean', '#A1A6AB'),
    ('raw_logistic', 'Raw-payoff logistic', '#397EB0'),
    ('combined_logistic_both', 'Game + identities: logistic', '#008578'),
    ('combined_mlp_both', 'Game + identities: MLP', '#B24E17'),
    ('llm_zero_shot', 'LLM: zero-shot', '#7950A0'),
    ('llm_few_shot', 'LLM: few-shot', '#C24066'),
    ('llm_game_theory', 'LLM: game-theory prompt', '#9B821C'))
CALIBRATION_METHODS = ('pair', 'combined_logistic_both', 'combined_mlp_both',
                       'llm_zero_shot', 'llm_few_shot', 'llm_game_theory')
STAGES = {
    'full': ('prospective/evaluation', 'prospective', 'New games · numerical and prompted forecasts'),
    'numerical': ('prospective/evaluation-numerical', 'prospective', 'New games · numerical forecasts'),
    'pair': ('prospective/evaluation-pair', 'prospective_pair', 'New games + held-out model pairing'),
    'model': ('prospective/evaluation-model', 'prospective_model', 'New games + held-out model'),
    'controls': ('controls/evaluation', 'prospective_controls', 'Known game shapes · affine and text controls')}


def read_json(path):
    return json.loads(Path(path).read_text())


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def save_json(path, value):
    with Path(path).open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write('\n')


def save_formats(fig, folder, stem):
    names = []
    for suffix in ('png', 'svg', 'pdf'):
        name = stem+'.'+suffix
        fig.savefig(folder/name, dpi=180, facecolor='white')
        names.append(name)
    plt.close(fig)
    return names


def prepare(summary, split):
    """Select a fixed display roster on the original all-method common support."""
    index, support = {}, {}
    for row in summary['support']:
        if row['split'] == split and row['target'] in TARGETS:
            if row['target'] in support:
                raise ValueError('Duplicate target support')
            support[row['target']] = row
    for row in summary['scores']:
        if row['split'] != split or row['target'] not in TARGETS:
            continue
        key = row['target'], row['method']
        if key in index:
            raise ValueError('Duplicate target/method score')
        if row['rows'] != support[row['target']]['common_rows']:
            raise ValueError('Saved score does not retain original all-method support')
        index[key] = row
    for target in TARGETS:
        rows = [row for (t, _), row in index.items() if t == target]
        if not rows:
            raise ValueError('Expected broad target missing: '+target)
        for field in ('rows', 'groups', 'episodes', 'opportunities'):
            if len({row[field] for row in rows}) != 1:
                raise ValueError('Methods have inconsistent saved support: '+target+'/'+field)
    methods = [item for item in METHODS if any((target, item[0]) in index for target in TARGETS)]
    return index, support, methods


def support_label(index, target):
    row = next(row for (t, _), row in index.items() if t == target)
    return f"{row['groups']} shape groups · {row['episodes']:,} episodes · {row['rows']:,} focal rows"


def heading(fig, label, subtitle):
    fig.suptitle(label, x=.035, y=.973, ha='left', fontsize=17, fontweight='bold')
    fig.text(.035, .973-.48/fig.get_figheight(), 'Prospective timing verified · '+subtitle, fontsize=11, color='#49515A')


def score_figure(index, methods, label, folder):
    fig, axes = plt.subplots(2, 3, figsize=(16.8, max(8.0, 4.4+.59*len(methods))), sharey=True)
    fig.subplots_adjust(left=.205, right=.97, top=.83, bottom=.15, wspace=.14, hspace=.36)
    heading(fig, label, 'selected methods in fixed order; original common support retained')
    metrics = (('event_brier', 'Event Brier · lower is better'), ('event_log_loss', 'Event log loss · lower is better'))
    for i, (metric, metric_label) in enumerate(metrics):
        upper = []
        for target in TARGETS:
            for method, _, _ in methods:
                row = index.get((target, method), {})
                ci = row.get('intervals', {}).get(metric, {})
                upper.extend(value for value in (row.get(metric), ci.get('upper')) if finite(value))
        limit = max(upper, default=1.)*1.07
        for j, target in enumerate(TARGETS):
            ax = axes[i, j]
            for y, (method, _, color) in enumerate(methods):
                row = index.get((target, method), {})
                point = row.get(metric)
                if not finite(point):
                    ax.text(.5, y, 'Unavailable', transform=ax.get_yaxis_transform(), ha='center', fontsize=9)
                    continue
                ci = row.get('intervals', {}).get(metric, {})
                lower, higher = ci.get('lower'), ci.get('upper')
                if finite(lower) and finite(higher):
                    ax.hlines(y, lower, higher, color=color, linewidth=1.4)
                    ax.vlines([lower, higher], y-.07, y+.07, color=color, linewidth=1.1)
                ax.plot(point, y, 'o', color=color, markersize=5)
                ax.axhline(y+.5, color='#E6E9EC', linewidth=.5, zorder=0)
            ax.set_ylim(len(methods)-.4, -.6)
            ax.set_xlim(0, limit)
            ax.set_yticks(range(len(methods)), [item[1] for item in methods], fontsize=10)
            ax.tick_params(axis='y', length=0, pad=9)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.grid(axis='x', color='#E1E5E8', linewidth=.55)
            ax.set_xlabel(metric_label, fontsize=10.5)
            if i == 0:
                ax.set_title(TARGET_LABELS[j]+'\n'+support_label(index, target), fontsize=10.5, pad=13)
            for spine in ('top', 'right', 'left'):
                ax.spines[spine].set_visible(False)
    fig.text(.035, .075, 'Bars are saved 95% game/episode bootstrap intervals for each score, with fitted forecasts fixed. Interval overlap is not a paired significance test.',
             fontsize=10, color='#37434A')
    fig.text(.035, .042, 'Game-equal event weighting; unadjusted intervals. Three broad targets shown. Other targets and identity/feature ablations remain in the source scores.',
             fontsize=10, color='#49515A')
    return save_formats(fig, folder, 'broad-target-scores')


def calibration_figure(index, methods, label, folder):
    shown = [item for item in methods if item[0] in CALIBRATION_METHODS]
    fig, axes = plt.subplots(1, 3, figsize=(16.8, 7.5), sharex=True, sharey=True)
    fig.subplots_adjust(left=.075, right=.97, top=.685, bottom=.24, wspace=.22)
    heading(fig, label, 'calibration of numerical and prompted forecasts' if any(m[0].startswith('llm_') for m in shown)
            else 'calibration of selected numerical forecasts')
    handles = []
    for method, method_label, color in shown:
        handles.append(Line2D([0], [0], color=color, marker='o', markersize=5,
                             linestyle='--' if method.startswith('llm_') else '-', label=method_label))
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52, .851), ncol=3, fontsize=10, frameon=False)
    for j, target in enumerate(TARGETS):
        ax = axes[j]
        ax.plot([0, 1], [0, 1], '--', color='#91979B', linewidth=1)
        for method, _, color in shown:
            bins = index.get((target, method), {}).get('calibration', [])
            points = sorted((row['prediction'], row['observed'], row['game_equal_event_mass']) for row in bins
                            if finite(row.get('prediction')) and finite(row.get('observed')))
            if not points:
                continue
            x, y, mass = map(np.asarray, zip(*points))
            ax.plot(x, y, color=color, linewidth=1.0, alpha=.8, linestyle='--' if method.startswith('llm_') else '-')
            ax.scatter(x, y, s=14+130*mass, color=color, alpha=.95, edgecolors='white', linewidth=.45, zorder=3)
        ax.set_title(TARGET_LABELS[j]+'\n'+support_label(index, target), fontsize=10.5, pad=11)
        ax.set_xlim(-.03, 1.03); ax.set_ylim(-.03, 1.03)
        ax.set_xticks(np.linspace(0, 1, 6)); ax.set_yticks(np.linspace(0, 1, 6))
        ax.set_xlabel('Mean forecast probability', fontsize=11)
        if j == 0:
            ax.set_ylabel('Observed event rate', fontsize=11)
        ax.grid(color='#E1E5E8', linewidth=.55)
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
    fig.text(.035, .126, 'Points copy the existing 10-bin calibration summaries; marker area increases with game-equal event mass. Connecting lines are visual guides.',
             fontsize=10, color='#37434A')
    fig.text(.035, .081, 'Diagonal = perfect calibration. The same supported rows as the source evaluation are retained. Sparse bins have no displayed uncertainty intervals.',
             fontsize=10, color='#49515A')
    return save_formats(fig, folder, 'broad-target-calibration')


def render_stage(root, key, output_root):
    relative, split, label = STAGES[key]
    source = root/relative
    marker = root/'steps'/('after-'+source.parent.name+'-'+source.name+'.json')
    required = [source/name for name in ('scores.json', 'audit.json', 'coverage.json')]+[marker]
    if not all(path.is_file() for path in required):
        return dict(stage=key, status='not_yet_verified')
    audit = read_json(source/'audit.json')
    if audit.get('prospective_verified') is not True:
        return dict(stage=key, status='not_verified')
    if audit.get('effective_split') != split:
        raise ValueError('Source evaluation has the wrong split')
    initial = snapshot(required+[Path(__file__), Path(__file__).with_name('secondary_analysis.py')]+
                       list(audit.get('source_sha256', {})))
    validate_upstream_markers([marker])
    timing = verified_evaluation(source)
    summary = read_json(source/'scores.json')
    index, support, methods = prepare(summary, split)
    destination = output_root/key
    previous = destination/'derivation.json'
    if previous.exists():
        old = read_json(previous)
        if old.get('input_sha256') == initial and old.get('status') == 'verified_derived_figure':
            unchanged(old['output_sha256']); unchanged(initial)
            return dict(stage=key, status='unchanged', directory=str(destination))
    with tempfile.TemporaryDirectory(prefix='.prospective-figures-', dir=output_root) as temporary:
        temporary = Path(temporary)
        names = score_figure(index, methods, label, temporary)
        names += calibration_figure(index, methods, label, temporary)
        save_json(temporary/'plotted-values.json', dict(split=split, source_directory=str(source),
            selected_methods=[item[0] for item in methods], calibration_methods=list(CALIBRATION_METHODS),
            scores=[index[target, method] for target in TARGETS for method, _, _ in methods if (target, method) in index],
            support=support, full_saved_uncertainty=summary.get('uncertainty'),
            note='Exact saved score, interval and calibration values; no rescore, refit, or test-population pooling.'))
        names.append('plotted-values.json')
        unchanged(initial)
        destination.mkdir(parents=True, exist_ok=True)
        for name in names:
            os.replace(temporary/name, destination/name)
    derivation = dict(status='verified_derived_figure', classification='primary_prospective_plotting_derivative',
        source_directory=str(source), input_sha256=initial,
        output_sha256=snapshot([destination/name for name in names]), timing_recheck=timing,
        replaces_png_paths=[str(source/name) for name in ('comparison.png', 'calibration.png')],
        figures=[str(destination/name) for name in names if name.endswith('.png')],
        validation='Completed primary output hashes and prior-forecast chronology checked; all input/source bytes unchanged before/after rendering.',
        design=dict(targets=list(TARGETS), methods=[item[0] for item in methods], fixed_order=True,
                    original_all_method_common_support=True, scientific_scores_recomputed=False,
                    plotting_versions=dict(matplotlib=matplotlib.__version__, numpy=np.__version__)),
        limitations=['Display selection made after results; original forecasts and scoring protocol are unchanged.',
                     'Only three broad targets and selected baseline/learned/prompted methods are displayed.',
                     'Score intervals are descriptive, unadjusted, and conditional on fixed fitted forecasts.',
                     'Different sources can have different original all-method common support; figures do not pool sources.'])
    with tempfile.NamedTemporaryFile(mode='w', dir=destination, suffix='.json', delete=False) as handle:
        json.dump(derivation, handle, indent=2, allow_nan=False); handle.write('\n')
        temporary_manifest = Path(handle.name)
    os.replace(temporary_manifest, previous)
    return dict(stage=key, status='generated', directory=str(destination), figures=2)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--stage', choices=['all', *STAGES], default='all')
    args = parser.parse_args(argv)
    root = args.run_root.resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not root.is_dir():
        parser.error('run-root must be an existing directory under /shared/allie')
    output = root/'report-figures/prospective'
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42,
                         'axes.labelcolor': '#26343B', 'text.color': '#26343B', 'savefig.facecolor': 'white'})
    with (output/'figures.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        keys = list(STAGES) if args.stage == 'all' else [args.stage]
        print(json.dumps([render_stage(root, key, output) for key in keys]))


if __name__ == '__main__':
    main()
