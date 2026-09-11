"""Offline plot gallery: engine stages and independently judged discovery.

No model calls. Original reports and scores are left untouched.
"""
import argparse
import csv
import hashlib
import html
import json
import math
import os
from pathlib import Path

from .evaluator import evaluate
from .specs import SPECS

GROUPS = {
    'A. RULE / ENFORCEMENT': ('unchecked_self_report', 'unenforced_limit', 'undelivered_punishment', 'rule_precedence'),
    'B. INFORMATION / INTERFACE': ('information_overflow', 'meta_rule_exploit'),
    'C. STATE / TIME': ('resource_conversion', 'state_reset', 'timing_exploit', 'terminal_condition_rushing'),
    'D. MULTIPLAYER / OBJECTIVE': ('commitment_exploit', 'objective_substitution', 'sacrificial_play', 'board_state_poisoning'),
}
CATEGORY_LABELS = {
    'unchecked_self_report': 'Unchecked self-report', 'unenforced_limit': 'Unenforced limits',
    'undelivered_punishment': 'Undelivered punishment', 'rule_precedence': 'Rule-order / precedence',
    'information_overflow': 'Information overflow', 'meta_rule_exploit': 'Meta-rule exploits',
    'resource_conversion': 'Resource conversion', 'state_reset': 'State reset / refresh',
    'timing_exploit': 'Turn-order / timing', 'terminal_condition_rushing': 'Terminal-condition rushing',
    'commitment_exploit': 'Threat / commitment', 'objective_substitution': 'Objective substitution',
    'sacrificial_play': 'Sacrificial / negative-value play', 'board_state_poisoning': 'Board-state poisoning',
}
GAME_LABELS = {'gen_seven_seal': 'Seven Seal', 'ref_commons': 'Commons', 'ref_hanabi': 'Hanabi',
               'ta_ipd': 'Prisoner’s Dilemma', 'ref_exchange': 'Exchange',
               'ta_winasmuch': 'Win As Much', 'ta_ipd3': 'Three-player IPD'}
MODEL_LABELS = {'qwen-3.8-27b': 'Qwen 3.8 27B', 'kimi-k3': 'Kimi K3', 'glm': 'GLM 5.3',
                'claude-haiku-4.5': 'Claude Haiku 4.5', 'gpt-5-mini': 'GPT-5 mini',
                'gemini-3.7-flash': 'Gemini 3.7 Flash'}
METRICS = ('attempted', 'executed', 'successful', 'discovered')
METRIC_LABELS = {'attempted': 'Attempted', 'executed': 'Executed', 'successful': 'Successful',
                 'discovered': 'Discovery (judge)'}
COLORS = {'attempted': '#8aa4bb', 'executed': '#168c91', 'successful': '#ed9a28', 'discovered': '#854bb0'}


def cumulative(values):
    """Missing is unknown, unless an earlier/current positive establishes ever."""
    seen = False
    missing = False
    result = []
    for value in values:
        seen |= value is True
        missing |= value is None
        result.append(True if seen else None if missing else False)
    return result


def fixed_rate(values):
    """Never shrink denominators when observations are absent."""
    return sum(values) / len(values) if values and all(v is not None for v in values) else None


def csv_write(path, rows):
    with path.open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_data(root):
    config = json.loads((root / 'config.json').read_text())['args']
    source_hashes = {}
    for name in ('games.py', 'evaluator.py', 'specs.py'):
        current = Path(__file__).with_name(name).read_bytes()
        archived = root/'source'/'benchmark'/name
        if archived.exists() and archived.read_bytes() != current:
            raise ValueError(f'{name} differs from the archived run; use the matching source before recomputing engine labels')
        source_hashes[name] = hashlib.sha256(current).hexdigest()
    specs = [s for s in SPECS if s.game_id in config['games']]
    assigned = [c for cs in GROUPS.values() for c in cs]
    assert len(assigned) == len(set(assigned)) == 14
    assert {s.category for s in specs} <= set(assigned)
    by_category = {c: group for group, cs in GROUPS.items() for c in cs}
    traces = {}
    manifest = []
    versions = set()
    for path in sorted(root.glob('*/traces/*.json')):
        raw = path.read_bytes()
        t = json.loads(raw)
        key = (t['model_id'], t['game_id'], t['iteration'])
        if key in traces:
            raise ValueError(f'Duplicate trace {key}')
        if t['model_id'] not in config['models'] or t['game_id'] not in config['games']:
            continue
        if not 1 <= t['iteration'] <= config['iterations']:
            raise ValueError(f'Unexpected repetition {key}')
        traces[key] = t
        manifest.append({'path': str(path.relative_to(root)), 'sha256': hashlib.sha256(raw).hexdigest()})
        if t['status'] == 'complete':
            versions.add(t.get('discovery_judge', {}).get('evaluator_version', 'legacy'))
    if len(versions) > 1:
        raise ValueError(f'Mixed discovery evaluator versions: {versions}; rescore uniformly first')
    # Execution is independent of whether the semantic judge has completed.
    observations = []
    for model in config['models']:
        for game in config['games']:
            for iteration in range(1, config['iterations'] + 1):
                t = traces.get((model, game, iteration))
                finished = bool(t and t.get('episode', {}).get('extras', {}).get('final_state', {}).get('done'))
                engine = {r['exploit_id']: r for r in evaluate(game, t['episode']['extras']['events'])} if finished else {}
                judgments = {r['exploit_id']: r for r in t.get('evaluation', [])} if t and t['status'] == 'complete' else {}
                for spec in [s for s in specs if s.game_id == game]:
                    row = {'model_id': model, 'game_id': game, 'exploit_id': spec.exploit_id,
                           'category': spec.category, 'group': by_category[spec.category], 'iteration': iteration}
                    for metric in METRICS:
                        source = judgments if metric == 'discovered' else engine
                        value = source.get(spec.exploit_id, {}).get(metric)
                        if value is not None and type(value) is not bool:
                            raise ValueError(f'Invalid {metric} for {spec.exploit_id}')
                        row[metric] = value
                    observations.append(row)
    metadata = {'source': str(root), 'config': config, 'judge_versions': sorted(versions), 'source_traces': manifest,
                'games_present': len(traces), 'engine_games': sum(bool(t.get('episode', {}).get('extras', {}).get('final_state', {}).get('done')) for t in traces.values()),
                'judged_games': sum(t['status'] == 'complete' for t in traces.values()),
                'expected_games': len(config['models']) * len(config['games']) * config['iterations'],
                'groups': {g: list(cs) for g, cs in GROUPS.items()}, 'analysis_source_hashes': source_hashes}
    return config, specs, observations, metadata


class Cube:
    def __init__(self, models, specs, iterations, observations):
        self.models, self.specs, self.iterations = models, specs, iterations
        self.lookup = {(r['model_id'], r['exploit_id'], r['iteration']): r for r in observations}
        self.values = {}
        for m in models:
            for spec in specs:
                for metric in METRICS:
                    current = [self.lookup[m, spec.exploit_id, i][metric] for i in range(1, iterations + 1)]
                    self.values[m, spec.exploit_id, metric, 'current'] = current
                    self.values[m, spec.exploit_id, metric, 'cumulative'] = cumulative(current)

    def curve(self, model, specs, metric, mode):
        return [fixed_rate([self.values[model, s.exploit_id, metric, mode][i] for s in specs]) for i in range(self.iterations)]

    def export(self):
        rows = []
        selections = [('model', 'all', self.specs)]
        selections += [('game', g, [s for s in self.specs if s.game_id == g]) for g in dict.fromkeys(s.game_id for s in self.specs)]
        selections += [('hole', s.exploit_id, [s]) for s in self.specs]
        selections += [('group', g, [s for s in self.specs if s.category in cs]) for g, cs in GROUPS.items()]
        for scope, name, specs in selections:
            if not specs:
                continue
            for model in self.models:
                for mode in ('current', 'cumulative'):
                    for metric in METRICS:
                        for i, rate in enumerate(self.curve(model, specs, metric, mode), 1):
                            values = [self.values[model, s.exploit_id, metric, mode][i-1] for s in specs]
                            rows.append(dict(scope=scope, selection=name, model_id=model, mode=mode, metric=metric,
                                             iteration=i, numerator=sum(v is True for v in values),
                                             denominator=len(values), known=sum(v is not None for v in values), rate=rate))
        return rows


def draw(root, output):
    output.mkdir(parents=True, exist_ok=True)
    os.environ['MPLCONFIGDIR'] = str(output / '.matplotlib-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.lines import Line2D
    from matplotlib.colors import LinearSegmentedColormap

    cfg, specs, observations, meta = load_data(root)
    (output / 'manifest.json').write_text(json.dumps(meta, indent=2))
    csv_write(output / 'observations.csv', observations)
    cube = Cube(cfg['models'], specs, cfg['iterations'], observations)
    csv_write(output / 'rates.csv', cube.export())
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titleweight': 'semibold', 'savefig.facecolor': 'white'})
    models = cfg['models']
    model_colors = dict(zip(models, plt.rcParams['axes.prop_cycle'].by_key()['color']))
    x = list(range(1, cfg['iterations'] + 1))
    records = []
    coverage = f"{meta['engine_games']}/{meta['expected_games']} engine games · {meta['judged_games']}/{meta['expected_games']} judged"
    footer = coverage + ' · Discovery uses existing judge labels; known inconsistencies remain.\nPersistent cross-game chains; descriptive results, not independent replicates.'
    if cfg['scope'] != 'cross-game' or cfg['condition'] != 'persistent':
        footer = coverage + ' · Discovery uses existing judge labels.\nDescriptive results; no independent-replicate uncertainty estimates.'
    handles = [Line2D([], [], color=COLORS[k], linestyle='--' if k == 'discovered' else '-', marker=mk, label=METRIC_LABELS[k])
               for k, mk in zip(METRICS, ['o', 's', '^', 'D'])]
    atlas = PdfPages(output / 'all_plots.pdf')

    def save(fig, name, title, section, description):
        fig.suptitle(title, fontsize=16, fontweight='semibold', y=.98)
        fig.text(.5, .012, footer, ha='center', fontsize=8, color='#53606b')
        fig.savefig(output / (name + '.png'), dpi=160, bbox_inches='tight')
        fig.savefig(output / (name + '.pdf'), bbox_inches='tight')
        atlas.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        records.append(dict(name=name, title=title, section=section, description=description))
        print(name, flush=True)

    def axis(ax, binary=False):
        ax.set(xticks=x, xlim=(.8, cfg['iterations'] + .2), ylim=(-5, 105), xlabel='Repetition')
        ax.set_yticks([0, 100] if binary else [0, 25, 50, 75, 100])
        ax.set_yticklabels(['No', 'Yes'] if binary else ['0%', '25%', '50%', '75%', '100%'])
        ax.grid(axis='y', alpha=.17)

    def plot_stages(ax, model, selected, mode, binary=False):
        # Different widths and open markers keep coincident binary series visible.
        for metric, marker, width, size in zip(METRICS, ['o', 's', '^', 'D'], [5, 3.5, 2, 1.6], [11, 8, 6, 4]):
            vals = [np.nan if v is None else 100*v for v in cube.curve(model, selected, metric, mode)]
            ax.plot(x, vals, color=COLORS[metric], linestyle='--' if metric == 'discovered' else '-',
                    marker=marker, linewidth=width, markersize=size, markerfacecolor='white',
                    markeredgewidth=1.3, drawstyle='steps-post' if binary else 'default', label=METRIC_LABELS[metric])
        axis(ax, binary)

    def model_grid(selected, mode, name, title, section, binary=False):
        cols = min(3, len(models)); rows = math.ceil(len(models)/cols)
        fig, axes = plt.subplots(rows, cols, figsize=(13, 3*rows+1.4), squeeze=False)
        for ax, model in zip(axes.flat, models):
            plot_stages(ax, model, selected, mode, binary)
            ax.set_title(MODEL_LABELS.get(model, model), pad=10)
        for ax in list(axes.flat)[len(models):]: ax.set_visible(False)
        fig.legend(handles=handles, loc='lower center', ncol=4, bbox_to_anchor=(.5, .075), frameon=False)
        fig.subplots_adjust(top=.84, bottom=.23, hspace=.58, wspace=.25)
        detail = ('Each panel is one model × game × hole; values are binary.' if binary else f'Equal weight per game-specific hole; {len(selected)} holes per model.')
        detail += ' Cumulative = ever observed through that repetition.' if mode == 'cumulative' else 'Current = observed in that repetition only.'
        save(fig, name, title, section, detail)

    for mode in ('current', 'cumulative'):
        label = 'Per repetition' if mode == 'current' else 'Cumulative coverage'
        model_grid(specs, mode, 'models_' + mode, f'{label}: attempts, execution, success and discovery', 'Models')
        for game in cfg['games']:
            selected = [s for s in specs if s.game_id == game]
            model_grid(selected, mode, 'game_' + game + '_' + mode,
                       f'{GAME_LABELS.get(game, game)} · {label.lower()}', 'Games')

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, mode in zip(axes, ('current', 'cumulative')):
        for model in models:
            vals = cube.curve(model, specs, 'discovered', mode)
            ax.plot(x, [np.nan if v is None else 100*v for v in vals], '-o', color=model_colors[model], label=MODEL_LABELS.get(model, model))
        axis(ax); ax.set_title('Discovery credited this repetition' if mode == 'current' else 'Ever credited with discovery')
    fig.legend(*axes[0].get_legend_handles_labels(), loc='lower center', ncol=3, bbox_to_anchor=(.5, .065), frameon=False)
    fig.subplots_adjust(top=.80, bottom=.31, wspace=.2)
    save(fig, 'discovery_comparison', 'Discovery across repetitions', 'Overview', 'Current and cumulative judge-scored discovery, with a fixed set of holes.')

    # Stages share the same coverage denominator. Discovery is not a fourth funnel stage.
    for mode in ('current', 'cumulative'):
        cols = min(3, len(models)); nr = math.ceil(len(models)/cols)
        fig, axes = plt.subplots(nr, cols, figsize=(13, 3*nr+1.4), squeeze=False)
        for ax, model in zip(axes.flat, models):
            vals = [cube.curve(model, specs, k, mode)[-1] for k in METRICS]
            ys = [np.nan if v is None else 100*v for v in vals]
            ax.bar([0, 1, 2, 3.5], ys, color=[COLORS[k] for k in METRICS], width=.65)
            ax.plot([0, 1, 2], ys[:3], color='#263642', marker='o', linewidth=1)
            ax.axvline(2.75, color='#aab2b8', linestyle=':', linewidth=1)
            for pos, yv in zip([0, 1, 2, 3.5], ys):
                if not np.isnan(yv):ax.text(pos, yv+3, f'{yv:.0f}%', ha='center')
            ax.set(xticks=[0, 1, 2, 3.5], xticklabels=['Attempt', 'Execute', 'Success', 'Discovery'], ylim=(0, 110), title=MODEL_LABELS.get(model, model))
            ax.grid(axis='y', alpha=.15)
        for ax in list(axes.flat)[len(models):]:ax.set_visible(False)
        fig.subplots_adjust(top=.83, bottom=.15, hspace=.45, wspace=.28)
        title = 'Attempted → executed → successful; discovery alongside'
        save(fig, 'stages_' + mode, title + (' · ever by final repetition' if mode == 'cumulative' else ' · final repetition only'), 'Stages',
             'All bars use the same hole denominator. Discovery is a separate judge label. Success is positive predefined local benefit, not probability of winning.')

    groups = [g for g, cs in GROUPS.items() if any(s.category in cs for s in specs)]
    if len(groups) >= 3:
        angles = np.linspace(0, 2*np.pi, len(groups), endpoint=False)
        closed = np.r_[angles, angles[0]]
        for mode in ('current', 'cumulative'):
            cols = min(3, len(models)); nr = math.ceil(len(models)/cols)
            fig, axes = plt.subplots(nr, cols, figsize=(14, 5*nr+1.1), subplot_kw={'projection': 'polar'}, squeeze=False)
            labels = []
            for group in groups:
                n = sum(s.category in GROUPS[group] for s in specs)
                labels.append(group.replace(' / ', '\n/ ') + f'\n(n={n})')
            for ax, model in zip(axes.flat, models):
                ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
                for metric in ('executed', 'discovered'):
                    rates = [cube.curve(model, [s for s in specs if s.category in GROUPS[g]], metric, mode)[-1] for g in groups]
                    vals = [np.nan if v is None else 100*v for v in rates]
                    ax.plot(closed, vals+[vals[0]], color=COLORS[metric], marker='o', linewidth=2,
                            linestyle='--' if metric == 'discovered' else '-', label='Discovery (judge)' if metric == 'discovered' else 'Exploit execution (engine)')
                    ax.fill(closed, vals+[vals[0]], color=COLORS[metric], alpha=.07)
                ax.set_xticks(angles, labels, fontsize=8)
                ax.tick_params(axis='x', pad=14)
                ax.set_ylim(0, 100); ax.set_yticks([25, 50, 75, 100], ['25%', '50%', '75%', '100%'], fontsize=7)
                ax.set_rlabel_position(45)
                ax.set_title(MODEL_LABELS.get(model, model), y=1.25, fontsize=11)
                ax.spines['polar'].set_visible(True)
            for ax in list(axes.flat)[len(models):]:ax.set_visible(False)
            fig.legend(*axes.flat[0].get_legend_handles_labels(), loc='lower center', ncol=2, bbox_to_anchor=(.5, .065), frameon=False)
            fig.subplots_adjust(top=.81, bottom=.20, left=.09, right=.91, hspace=.9, wspace=.65)
            save(fig, 'radar_' + mode, 'Discovery and exploit rates by your four groups' + (' · cumulative' if mode == 'cumulative' else ' · final repetition'), 'Groups',
                 'Each axis is the share of game-specific holes in that group. A/B/C/D denominators are shown; categories with more game instances receive more weight. Exploit rate is unconditional engine execution, not execution conditional on discovery.')

    for metric in ('discovered', 'executed'):
        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        for ax, (group, cats) in zip(axes.flat, GROUPS.items()):
            selected = [s for s in specs if s.category in cats]
            for model in models:
                vals = cube.curve(model, selected, metric, 'cumulative')
                ax.plot(x, [np.nan if v is None else 100*v for v in vals], '-o', color=model_colors[model], label=MODEL_LABELS.get(model, model))
            axis(ax); ax.set_title(group + f' · {len(selected)} holes')
        fig.legend(*axes.flat[0].get_legend_handles_labels(), loc='lower center', ncol=3, bbox_to_anchor=(.5, .065), frameon=False)
        fig.subplots_adjust(top=.84, bottom=.23, hspace=.50, wspace=.22)
        save(fig, 'groups_' + metric, 'Cumulative ' + ('discovery' if metric == 'discovered' else 'exploit execution') + ' by group', 'Groups', 'Group learning curves; equal weight per game-specific hole within each group.')

    # Each individual hole gets current and cumulative curves for every model.
    for spec in specs:
        for mode in ('current', 'cumulative'):
            label = 'Ever by repetition' if mode == 'cumulative' else 'Per repetition'
            model_grid([spec], mode, 'hole_' + spec.exploit_id + '_' + mode,
                       GAME_LABELS.get(spec.game_id, spec.game_id) + ' · ' + CATEGORY_LABELS[spec.category] + '\n' + label,
                       'Holes', binary=True)

    # Compact summary for comparing all holes without overplotting binary curves.
    order = {c: i for i, c in enumerate(c for cs in GROUPS.values() for c in cs)}
    ordered = sorted(specs, key=lambda s: (order[s.category], s.game_id))
    for mode in ('current', 'cumulative'):
        fig, axes = plt.subplots(1, 4, figsize=(16, max(7, .31*len(ordered)+3)), sharey=True)
        for ax, metric in zip(axes, METRICS):
            a = np.array([[np.nan if (v := cube.values[m, s.exploit_id, metric, mode][-1]) is None else int(v) for m in models] for s in ordered])
            cmap = LinearSegmentedColormap.from_list(metric, ['#f0f2f5', COLORS[metric]])
            cmap.set_bad('#bbb')
            ax.imshow(a, aspect='auto', cmap=cmap, vmin=0, vmax=1)
            ax.set_title(METRIC_LABELS[metric])
            ax.set_xticks(range(len(models)), [MODEL_LABELS.get(m, m) for m in models], rotation=60, ha='right', fontsize=8)
            ax.set_yticks(range(len(ordered)), [GAME_LABELS.get(s.game_id, s.game_id) + ' · ' + CATEGORY_LABELS[s.category] for s in ordered], fontsize=8)
            for yy in range(len(ordered)):
                for xx in range(len(models)):
                    if a[yy, xx] == 1: ax.text(xx, yy, '●', ha='center', va='center', color='white', fontsize=7)
            ax.set_yticks(np.arange(-.5, len(ordered), 1), minor=True)
            ax.grid(which='minor', axis='y', color='white', linewidth=.8)
        fig.subplots_adjust(top=.87, bottom=.23, left=.30, right=.98, wspace=.18)
        save(fig, 'hole_matrix_' + mode, 'All models × all holes · ' + ('ever by final repetition' if mode == 'cumulative' else 'final repetition only'), 'Overview', 'Colored cells = yes; pale = no; gray = missing. Rows follow your A–D group order. Discovery is independent of the three engine stages.')

    atlas.close()
    (output / 'plots.json').write_text(json.dumps(records, indent=2))
    write_gallery(output, records, meta, specs)
    print(f'Wrote {len(records)} plots, PNG/PDF pairs, all_plots.pdf and index.html to {output}', flush=True)


def write_gallery(output, records, meta, specs):
    esc = html.escape
    featured = ['radar_cumulative', 'models_cumulative', 'stages_cumulative', 'discovery_comparison', 'hole_matrix_cumulative']
    records = sorted(records, key=lambda r: featured.index(r['name']) if r['name'] in featured else len(featured))
    sections = list(dict.fromkeys(r['section'] for r in records))
    cards = []
    for r in records:
        name = esc(r['name']); title = esc(r['title'])
        cards.append(f'<article data-section="{esc(r["section"])}"><a href="{name}.png"><img loading="lazy" src="{name}.png" alt="{title}"></a><div><small>{esc(r["section"])}</small><h2>{title}</h2><p>{esc(r["description"])}</p><a href="{name}.png">PNG</a> · <a href="{name}.pdf">PDF</a></div></article>')
    groups = ''.join('<li><b>'+esc(g)+'</b>: '+esc(', '.join(CATEGORY_LABELS[c] for c in cs))+'</li>' for g, cs in GROUPS.items())
    buttons = ''.join(f'<button data-filter="{esc(s)}">{esc(s)}</button>' for s in ['All'] + sections)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Benchmark plot gallery</title>
<style>body{font:16px/1.55 system-ui,sans-serif;color:#233342;background:#f4f6f9;margin:0}header,main{max-width:1500px;margin:auto;padding:28px}h1{font-size:36px;margin:0}h2{font-size:18px;margin:4px 0}p{margin:8px 0}a{color:#146783}nav{display:flex;gap:8px;flex-wrap:wrap;position:sticky;top:0;background:#f4f6f9;padding:12px 0;z-index:1}button,input{font:inherit;border:1px solid #ccd4dd;border-radius:6px;padding:8px 12px;background:white}button{cursor:pointer}button.active{background:#233342;color:white}input{flex:1;min-width:180px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,1fr));gap:22px}article{border:1px solid #dce2e9;border-radius:10px;background:white;overflow:hidden}article img{width:100%;display:block}article div{padding:16px}small{color:#666;text-transform:uppercase;letter-spacing:1px}details{padding:12px 0}li{margin-bottom:8px}[hidden]{display:none!important}@media(max-width:450px){.grid{grid-template-columns:1fr}header,main{padding:16px}}</style>
<header><h1>Discovery & exploitation</h1><p>__COUNTS__</p><p><a href="all_plots.pdf">Download all plots (PDF)</a> · <a href="rates.csv">Rates CSV</a> · <a href="observations.csv">Observations CSV</a> · <a href="manifest.json">Snapshot provenance</a></p>
<details open><summary><b>How to read these plots</b></summary><p>Attempted → executed → successful are computed from engine events. Discovery is a separate language-judge label, not a fourth funnel stage. Existing judge inconsistencies remain; these plots do not rescore discovery.</p><p>Per repetition shows that episode alone. Cumulative means ever observed through that repetition. All stage rates use the same fixed set of game-specific holes; success is positive predefined local benefit. Radar exploit rate means engine execution, without conditioning on discovery. Missing observations produce gaps, not zeroes. Individual-hole panels are binary; overlapping lines use different widths and marker shapes.</p><p>Broad-group radar axes give equal weight to each game-specific hole, not each of the 14 category names. One action can trigger multiple hole labels. These are descriptive persistent-chain results, without independent-replicate uncertainty estimates.</p><ul>__GROUPS__</ul></details></header>
<main><nav>__BUTTONS__<input id="search" type="search" placeholder="Filter by game, hole or plot title" aria-label="Filter plots"></nav><p id="count"></p><div class="grid">__CARDS__</div></main>
<script>let selected='All';const cards=[...document.querySelectorAll('article')],buttons=[...document.querySelectorAll('button')],search=document.querySelector('#search');function filter(){const q=search.value.toLowerCase();let n=0;for(const c of cards){c.hidden=!((selected==='All'||c.dataset.section===selected)&&c.textContent.toLowerCase().includes(q));if(!c.hidden)n++}document.querySelector('#count').textContent=n+' plots shown';for(const b of buttons)b.classList.toggle('active',b.dataset.filter===selected)}for(const b of buttons)b.onclick=()=>{selected=b.dataset.filter;filter()};search.oninput=filter;filter();</script></html>'''
    counts = f"{len(records)} plots · {meta['engine_games']}/{meta['expected_games']} engine games · {meta['judged_games']}/{meta['expected_games']} judged · {len(specs)} game-specific holes"
    page = page.replace('__COUNTS__', esc(counts)).replace('__GROUPS__', groups).replace('__BUTTONS__', buttons).replace('__CARDS__', ''.join(cards))
    (output / 'index.html').write_text(page)
    lines = ['# Plot gallery', '', counts, '', '[Browse gallery](index.html) · [All plots PDF](all_plots.pdf)', '',
             'Discovery uses existing judge labels. Exploit rates use engine execution, independently of the judge. Per-repetition and cumulative figures use fixed denominators. See the gallery for definitions.', '']
    for r in records:lines.append(f'- [{r["title"].replace(chr(10), " — ")}]({r["name"]}.png) ([PDF]({r["name"]}.pdf))')
    (output / 'README.md').write_text('\n'.join(lines)+'\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    draw(args.results.resolve(), (args.output or args.results/'plot_gallery').resolve())


if __name__ == '__main__':
    main()
