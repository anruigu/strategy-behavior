"""Readable derived figures for supervisor-verified secondary analyses only."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
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

TARGETS = ('action0', 'cooperation', 'coordination')
TARGET_LABELS = ('Action 0', 'Mutual cooperation', 'Coordination')
METHODS = (
    ('nash', 'Original equilibrium selector'),
    ('secondary_payoff_dominant', 'Payoff-dominant selector [secondary]'),
    ('pair', 'Ordered model/opponent mean'),
    ('secondary_pair_event', 'Event-weighted context [secondary]'),
    ('family', 'Game-family mean'),
    ('raw_logistic', 'Raw payoffs: logistic'),
    ('combined_logistic_both', 'Game + identities: logistic'),
    ('combined_mlp_both', 'Game + identities: MLP'),
    ('llm_zero_shot', 'LLM: zero-shot'),
    ('llm_few_shot', 'LLM: few-shot'),
    ('llm_game_theory', 'LLM: game-theory prompt'))
LEARNED = (('raw_logistic', 'Raw payoffs\nlogistic'),
           ('combined_logistic_both', 'Game + identities\nlogistic'),
           ('combined_mlp_both', 'Game + identities\nMLP'))
BASELINES = (('secondary_payoff_dominant', 'Payoff-dominant selector', '#B24E17', 'o', -.14),
             ('secondary_pair_event', 'Event-weighted ordered context', '#1968A6', 's', .14))
SPLITS = ('family', 'random_group', 'interpolation', 'extrapolation', 'pair', 'model',
          'prospective', 'prospective_pair', 'prospective_model', 'prospective_controls')
SPLIT_LABELS = dict(family='Unseen game families', random_group='Unseen game shapes',
                    interpolation='Payoff interpolation', extrapolation='Payoff extrapolation',
                    pair='Held-out model pairings', model='Unseen models',
                    prospective='New games: forecasts frozen before play',
                    prospective_pair='New games + held-out pairing',
                    prospective_model='New games + held-out model',
                    prospective_controls='Predefined affine and text controls')
STAGES = {
    'pilot': ('independent-analysis/pilot-secondary', 'Pilot', 'retrospective'),
    'development': ('independent-analysis/development-secondary', 'Combined pilot + development', 'retrospective'),
    'prospective': ('secondary-baselines/full/prospective-comparison', 'Prospective cohort', 'prospective'),
    'pair': ('secondary-baselines/excluded_pair/prospective-comparison', 'Pair-transfer cohort', 'prospective'),
    'model': ('secondary-baselines/excluded_model/prospective-comparison', 'Model-transfer cohort', 'prospective'),
    'controls': ('secondary-baselines/full/controls-comparison', 'Control cohort', 'prospective')}


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _new_json(path, value):
    with Path(path).open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write('\n')


def finite(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def display_support(row):
    if not row or not row.get('rows'):
        return 'No common supported rows'
    return f"{row['groups']:,} games · {row['rows']:,} scored rows"


def save_formats(fig, folder, stem):
    result = []
    for suffix in ('png', 'svg', 'pdf'):
        path = folder/(stem+'.'+suffix)
        fig.savefig(path, dpi=180, facecolor='white')
        result.append(path.name)
    plt.close(fig)
    return result


def title(fig, stage_label, split, prospective):
    fig.suptitle(stage_label+' · '+SPLIT_LABELS.get(split, split.replace('_', ' ')),
                 x=.035, y=.978, ha='left', fontsize=15, fontweight='bold')
    fig.text(.035, .926, 'Secondary post-pilot prospective comparison' if prospective else
             'Secondary post-pilot retrospective sensitivity', fontsize=10.5, color='#49515A')


SHORT_METHODS = {
    'nash': 'Original\nNash', 'secondary_payoff_dominant': 'Payoff-\ndominant',
    'pair': 'Ordered\ncontext', 'secondary_pair_event': 'Event\ncontext', 'family': 'Family\nmean',
    'raw_logistic': 'Raw\nlogistic', 'combined_logistic_both': 'Game+ID\nlogistic',
    'combined_mlp_both': 'Game+ID\nMLP', 'llm_zero_shot': 'LLM\nzero-shot',
    'llm_few_shot': 'LLM\nfew-shot', 'llm_game_theory': 'LLM\ntheory'}
SHORT_SPLITS = dict(family='Game families', random_group='Game shapes', interpolation='Interpolation',
                    extrapolation='Extrapolation', pair='Model pairs', model='Unseen model',
                    prospective='New games', prospective_pair='New games + pair',
                    prospective_model='New games + model', prospective_controls='Affine + text controls')
LEARNED_COLORS = ('#1968A6', '#008578', '#B24E17')


def stage_title(fig, stage_label, prospective, heading):
    fig.suptitle(stage_label+' · '+heading, x=.035, y=.975, ha='left', fontsize=16, fontweight='bold')
    fig.text(.035, .91, 'Secondary post-pilot prospective comparison' if prospective else
             'Secondary post-pilot retrospective sensitivity', fontsize=11, color='#49515A')


def brier_overview(summary, stage_label, splits, prospective, folder, vmax):
    source = [row for row in summary['scores'] if row['split'] in splits and row['target'] in TARGETS]
    present = {row['method'] for row in source}
    methods = [(key, label) for key, label in METHODS if key in present]
    index = {}
    for row in source:
        key = row['split'], row['method'], row['target']
        if key in index:
            raise ValueError('Duplicate split/method/target score')
        index[key] = row
    if not methods:
        return [], None
    fig, axes = plt.subplots(1, 3, figsize=(18., max(5.0, 3.0+.47*len(splits))), squeeze=False)
    fig.subplots_adjust(left=.115, right=.93, top=.77, bottom=.235, wspace=.20)
    stage_title(fig, stage_label, prospective, 'Brier scores by test population')
    cmap = plt.get_cmap('Blues').copy(); cmap.set_bad('#E7E9EB')
    for target_index, target in enumerate(TARGETS):
        ax = axes[0, target_index]
        matrix = np.array([[index.get((split, method, target), {}).get('event_brier')
                            if finite(index.get((split, method, target), {}).get('event_brier')) else np.nan
                            for method, _ in methods] for split in splits], dtype=float)
        im = ax.imshow(np.ma.masked_invalid(matrix), cmap=cmap, vmin=0, vmax=vmax, aspect='auto')
        ax.set_title(TARGET_LABELS[target_index], fontsize=12, fontweight='bold', pad=12)
        ax.set_xticks(range(len(methods)), [SHORT_METHODS[method] for method, _ in methods], fontsize=8.3)
        plt.setp(ax.get_xticklabels(), rotation=35, ha='right', rotation_mode='anchor')
        ax.tick_params(axis='both', length=0, pad=8)
        supports = [next((index.get((split, method, target)) for method, _ in methods
                          if index.get((split, method, target), {}).get('rows', 0) > 0), None) for split in splits]
        labels = [(SHORT_SPLITS.get(split, split)+'\n' if target_index == 0 else '')+
                  (f"{row['groups']} groups" if row else 'No support') for split, row in zip(splits, supports)]
        ax.set_yticks(range(len(splits)), labels, fontsize=9)
        ax.set_xticks(np.arange(-.5, len(methods), 1), minor=True)
        ax.set_yticks(np.arange(-.5, len(splits), 1), minor=True)
        ax.grid(which='minor', color='white', linewidth=1.5)
        ax.tick_params(which='minor', bottom=False, left=False)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for i in range(len(splits)):
            for j in range(len(methods)):
                value = matrix[i, j]
                ax.text(j, i, f'{value:.3f}' if math.isfinite(value) else '—', ha='center', va='center',
                        fontsize=8.8, color='white' if math.isfinite(value) and value > .58*vmax else '#17212A')
    bar = fig.colorbar(im, cax=fig.add_axes([.946, .22, .012, .48]))
    bar.set_label('Event Brier · lower is better', fontsize=10)
    bar.ax.tick_params(labelsize=9)
    fig.text(.035, .081, 'Groups are canonical payoff shapes; affine/text variants share a group. Rows retain separate test populations and original all-method common support.',
             fontsize=10, color='#49515A')
    fig.text(.035, .035, 'Game-equal event weighting. Payoff-dominant and event-context controls were designed after the pilot. Full method names, row counts and values: plotted-values.json.',
             fontsize=9.5, color='#49515A')
    selected = [index[split, method, target] for split in splits for method, _ in methods for target in TARGETS
                if (split, method, target) in index]
    return save_formats(fig, folder, 'brier-overview'), dict(kind='brier', splits=splits, rows=selected,
                                                           color_limits=[0, vmax], methods=methods)


def uncertainty_overview(summary, stage_label, splits, prospective, folder):
    rows = [row for row in summary.get('comparisons_to_secondary', []) if row['split'] in splits
            and row['target'] in TARGETS and row['method'] in {method for method, _ in LEARNED}
            and row['baseline'] == 'secondary_payoff_dominant']
    index = {}
    for row in rows:
        key = row['split'], row['target'], row['method']
        if key in index:
            raise ValueError('Duplicate paired secondary comparison')
        index[key] = row
    if not rows:
        return [], None
    fig, axes = plt.subplots(2, 3, figsize=(16.8, max(7.0, 4.2+1.0*len(splits))), sharey=True)
    fig.subplots_adjust(left=.12, right=.97, top=.80, bottom=.19, wspace=.17, hspace=.38)
    stage_title(fig, stage_label, prospective, 'Learned-model improvement over the payoff-dominant selector')
    labels = ('Raw-payoff logistic', 'Game + identities: logistic', 'Game + identities: MLP')
    handles = [Line2D([0], [0], color=color, marker='o', linewidth=1.5, markersize=4, label=label)
               for color, label in zip(LEARNED_COLORS, labels)]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.56, .90), ncol=3, frameon=False, fontsize=10.5)
    metrics = (('event_brier', 'Brier improvement'), ('event_log_loss', 'Log-loss improvement'))
    for metric_index, (metric, metric_label) in enumerate(metrics):
        extent = [0.]
        for row in rows:
            point = row.get('improvement', {}).get(metric)
            interval = row.get('intervals', {}).get(metric, {})
            extent += [value for value in (point, interval.get('lower'), interval.get('upper')) if finite(value)]
        low, high = min(extent), max(extent)
        span = max(high-low, .01)
        limits = (low-.07*span, high+.07*span)
        for target_index, target in enumerate(TARGETS):
            ax = axes[metric_index, target_index]
            ax.axvspan(0, max(limits[1], 0), color='#F0F7F1', zorder=0)
            ax.axvline(0, color='#62686E', linewidth=1, linestyle='--', zorder=1)
            for split_index, split in enumerate(splits):
                shown = False
                for method_index, ((method, _), color) in enumerate(zip(LEARNED, LEARNED_COLORS)):
                    row = index.get((split, target, method))
                    if row is None:
                        continue
                    point = row.get('improvement', {}).get(metric)
                    if not finite(point):
                        continue
                    shown = True
                    interval = row.get('intervals', {}).get(metric, {})
                    y = split_index+(-.22, 0, .22)[method_index]
                    lower, upper = interval.get('lower'), interval.get('upper')
                    if finite(lower) and finite(upper):
                        ax.hlines(y, lower, upper, color=color, linewidth=1.5, zorder=2)
                        ax.vlines([lower, upper], y-.035, y+.035, color=color, linewidth=1, zorder=2)
                    ax.plot(point, y, marker='o', color=color, markersize=4.3, linestyle='none', zorder=3)
                if not shown:
                    ax.text(.5, split_index, 'No estimate', transform=ax.get_yaxis_transform(), ha='center',
                            va='center', fontsize=9, color='#62686E')
                if split_index < len(splits)-1:
                    ax.axhline(split_index+.5, color='#ECEEF0', linewidth=.6, zorder=0)
            ax.set_xlim(*limits); ax.set_ylim(len(splits)-.45, -.55)
            ax.set_yticks(range(len(splits)), [SHORT_SPLITS.get(split, split) for split in splits], fontsize=9.5)
            ax.tick_params(axis='both', labelsize=9.5)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.grid(axis='x', color='#DDE1E5', linewidth=.55, zorder=0)
            ax.set_xlabel(metric_label, fontsize=11)
            if metric_index == 0:
                ax.set_title(TARGET_LABELS[target_index], fontsize=12, fontweight='bold', pad=10)
            for spine in ('top', 'right'):
                ax.spines[spine].set_visible(False)
    fig.text(.035, .067, 'Positive (right of zero) means the learned model has lower loss than the payoff-dominant secondary selector. Each row retains its original test population.',
             fontsize=10, color='#37434A')
    fig.text(.035, .035, 'Bars: paired 95% game/episode bootstrap, fixed fitted forecasts, unadjusted. No bar: interval unavailable. Scores and intervals are copied; primary gates are unchanged.',
             fontsize=9.5, color='#49515A')
    return save_formats(fig, folder, 'secondary-uncertainty'), dict(kind='secondary_contrasts', splits=splits, rows=rows,
        baseline='secondary_payoff_dominant')


def render_stage(run_root, key, output_root):
    relative, label, kind = STAGES[key]
    source = run_root/relative
    wrapper, scores = source/'supervisor-audit.json', source/'scores.json'
    if not wrapper.exists() or not scores.exists():
        return dict(stage=key, status='not_yet_verified', source=str(source))
    initial = {str(path.resolve()): file_hash(path) for path in (wrapper, scores, Path(__file__))}
    audit = json.loads(wrapper.read_text())
    if audit.get('status') != 'verified':
        return dict(stage=key, status='not_verified', source=str(source))
    if audit.get('output_sha256', {}).get(str(scores.resolve())) != initial[str(scores.resolve())]:
        raise ValueError('Scores differ from the supervisor-verified output: '+str(scores))
    expected = ('secondary_post_pilot_retrospective_sensitivity' if kind == 'retrospective' else
                'secondary_post_pilot_prospective_comparison')
    if audit.get('classification') != expected:
        raise ValueError('Unexpected secondary analysis classification: '+str(source))
    summary = json.loads(scores.read_text())
    if summary.get('secondary_classification') != expected:
        raise ValueError('Score and supervisor classifications differ')
    splits = {row['split'] for row in summary['scores'] if row['target'] in TARGETS}
    if any(split.startswith('unverified') for split in splits):
        raise ValueError('Cannot present unverified forecasts as prospective evidence')
    destination = output_root/key
    old_derivation = destination/'derivation.json'
    if old_derivation.exists():
        old = json.loads(old_derivation.read_text())
        if old.get('input_sha256') == initial and all(Path(path).is_file() and file_hash(path) == expected_hash
                for path, expected_hash in old.get('output_sha256', {}).items()):
            return dict(stage=key, status='unchanged', source=str(source), directory=str(destination),
                        figures=old['figures'], derivation=str(old_derivation))
    values = [row['event_brier'] for row in summary['scores'] if row['target'] in TARGETS
              and row['method'] in dict(METHODS) and finite(row.get('event_brier'))]
    vmax = min(1., max(.05, math.ceil(max(values, default=.25)*20)/20))
    output_root.mkdir(parents=True, exist_ok=True)
    selected, files = [], []
    with tempfile.TemporaryDirectory(prefix='.secondary-figures-', dir=output_root) as temporary:
        temporary = Path(temporary)
        ordered_splits = sorted(splits, key=lambda s: (SPLITS.index(s) if s in SPLITS else len(SPLITS), s))
        for function in (brier_overview, uncertainty_overview):
            args = (summary, label, ordered_splits, kind == 'prospective', temporary)
            names, data = function(*args, vmax) if function == brier_overview else function(*args)
            files.extend(names)
            if data is not None:
                selected.append(data)
        _new_json(temporary/'plotted-values.json', selected)
        # Verify the audited scores, audit wrapper and renderer bytes again before publishing derivatives.
        for path, expected_hash in initial.items():
            if file_hash(path) != expected_hash:
                raise ValueError('A secondary figure input/source changed during rendering: '+path)
        destination.mkdir(parents=True, exist_ok=True)
        for path in temporary.iterdir():
            os.replace(path, destination/path.name)
        if old_derivation.exists():
            old = json.loads(old_derivation.read_text())
            for filename, expected_hash in old.get('output_sha256', {}).items():
                path = Path(filename)
                if path.parent == destination and path.name not in files+['plotted-values.json'] and path.is_file():
                    if file_hash(path) != expected_hash:
                        raise ValueError('An earlier derived figure was edited; refusing to remove it: '+str(path))
                    path.unlink()
    output_hashes = {str((destination/name).resolve()): file_hash(destination/name) for name in files+['plotted-values.json']}
    figures = [dict(stage=key, splits=entry['splits'], kind=entry['kind'],
                    png=str(destination/('brier-overview.png' if entry['kind'] == 'brier' else 'secondary-uncertainty.png')))
               for entry in selected]
    derivation = dict(status='verified_derived_figure', classification=expected, input_sha256=initial,
        output_sha256=output_hashes, figures=figures, source_directory=str(source),
        plotting_versions=dict(matplotlib=matplotlib.__version__, numpy=np.__version__),
        design=dict(targets=list(TARGETS), methods=[method for method, _ in METHODS], learned=[method for method, _ in LEARNED],
                    splits_separate=True, common_support_preserved=True, brier_color_limits=[0, vmax]),
        validation='Input/audit/renderer hashes matched before and after rendering; original audited files were never written.',
        interpretation='Post-pilot secondary analyses; prospective only where the supervisor verified pre-outcome forecasts. No scientific refitting or recomputation of scores/intervals.')
    with tempfile.NamedTemporaryFile(mode='w', dir=destination, suffix='.json', delete=False) as handle:
        json.dump(derivation, handle, indent=2, allow_nan=False); handle.write('\n')
        temporary_derivation = Path(handle.name)
    os.replace(temporary_derivation, old_derivation)
    return dict(stage=key, status='generated', source=str(source), directory=str(destination), figures=figures,
                derivation=str(old_derivation))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--stage', choices=['all', *STAGES], default='all')
    args = parser.parse_args(argv)
    root = args.run_root.resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not root.is_dir():
        parser.error('run-root must be an existing directory under /shared/allie')
    output = root/'report-figures'/'secondary'
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42,
                         'axes.labelcolor': '#26343B', 'text.color': '#26343B', 'savefig.facecolor': 'white'})
    with (output/'figures.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        stages = list(STAGES) if args.stage == 'all' else [args.stage]
        result = [render_stage(root, key, output) for key in stages]
        index_path = output/'index.json'
        index = json.loads(index_path.read_text()) if index_path.exists() else {}
        index.update({item['stage']: item for item in result})
        with tempfile.NamedTemporaryFile(mode='w', dir=output, suffix='.json', delete=False) as handle:
            json.dump(index, handle, indent=2); handle.write('\n')
            temporary = Path(handle.name)
        os.replace(temporary, index_path)
        stage_derivations, figure_hashes = {}, {}
        for key in STAGES:
            path = output/key/'derivation.json'
            if not path.exists():
                continue
            derivation = json.loads(path.read_text())
            if derivation.get('status') != 'verified_derived_figure':
                raise ValueError('Unexpected derived figure audit status: '+str(path))
            for filename, expected_hash in derivation['output_sha256'].items():
                if file_hash(filename) != expected_hash:
                    raise ValueError('Derived figure differs from its audit: '+filename)
                figure_hashes[filename] = expected_hash
            stage_derivations[str(path.resolve())] = file_hash(path)
        aggregate = dict(status='verified_derived_figure_collection',
            renderer_sha256=file_hash(Path(__file__)), index_sha256=file_hash(index_path),
            stage_derivation_sha256=stage_derivations, output_sha256=figure_hashes,
            audited_scientific_sources_unchanged=True, max_main_pngs_per_stage=2)
        with tempfile.NamedTemporaryFile(mode='w', dir=output, suffix='.json', delete=False) as handle:
            json.dump(aggregate, handle, indent=2); handle.write('\n')
            temporary = Path(handle.name)
        os.replace(temporary, output/'derivation.json')
        print(json.dumps([dict(stage=item['stage'], status=item['status'], figures=len(item.get('figures', []))) for item in result]))


if __name__ == '__main__':
    main()
