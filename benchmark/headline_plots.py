"""Offline headline figures: calibrated MA doses and revised45 prompt profiles.

The two experiments retain separate cohorts, outcomes, and protocol labels.
No model calls, human comparison, or transfer estimate is made here.
"""
import argparse
from collections import defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT/'benchmark/results/headline-plots-20260911'
SOURCES = {
    'ma_data': ROOT/'benchmark/results/ma-extension-20260910/plots/plot-data.json',
    'ma_plan': ROOT/'benchmark/results/ma-extension-20260910/dose/plan.json',
    'ma_roster': ROOT/'benchmark/results/ma-extension-20260910/crossplay/plan.json',
    'prompt_data': ROOT/'benchmark/results/prompt-results-20260909/data.json',
    'prompt_rows': ROOT/'benchmark/results/prompt-results-20260909/observations.csv',
}
INK = '#243345'
MUTED = '#647183'
GRID = '#d8dfe7'
MODEL_COLORS = {
    'claude-opus-5': '#59718e', 'gpt-5.6-sol': '#8260bc', 'gemini-3.1-pro': '#238a79',
    'claude-sonnet-5': '#d58b29', 'gpt-5': '#b85f81', 'gemini-3.7-flash': '#568d9a',
    'qwen-3.8-27b': '#267cac', 'glm': '#768e39', 'grok-4.6': '#db8927',
}
NAMES = {
    'claude-opus-5': 'Opus 5', 'gpt-5.6-sol': 'GPT-5.6 Sol', 'gemini-3.1-pro': 'Gemini Pro',
    'claude-sonnet-5': 'Sonnet 5', 'gpt-5': 'GPT-5', 'gemini-3.7-flash': 'Gemini Flash',
    'qwen-3.8-27b': 'Qwen 3.8 27B', 'glm': 'GLM 5.3', 'grok-4.6': 'Grok 4.6',
    'qwen-3.8-27b-medium': 'Qwen 3.8 27B', 'kimi-k3': 'Kimi K3',
    'deepseek-v4-pro': 'DeepSeek V4-Pro', 'gemma-4-31b': 'Gemma 4 31B',
    'qwen-3.5-9b': 'Qwen 3.5 9B', 'gpt-oss-20b': 'GPT-OSS-20B',
}
PHASES = ('win_only', 'exploration', 'hinted')
PHASE_NAMES = {'win_only': 'Win only', 'exploration': 'Exploration', 'hinted': 'Hinted rescue'}
PHASE_COLORS = {'win_only': '#287ba4', 'exploration': '#d4842a', 'hinted': '#8060b7'}
SPOKES = ['Rule /\nenforcement', 'Information /\ninterface', 'State /\ntime', 'Multiplayer /\nobjective']


def mean(values):
    return statistics.mean(values) if values else None


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')


def load_sources(out, inputs=None):
    """Snapshot each input once, including any source CSV quoting and newlines."""
    data, manifest = {}, {}
    for key, source in SOURCES.items():
        original_source = source
        if inputs is not None:
            source = inputs/(key+source.suffix)
        raw = source.read_bytes()
        target = out/'inputs'/(key+source.suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        manifest[key] = dict(source=str(original_source), read_from=str(source), snapshot=str(target.relative_to(out)),
                             sha256=hashlib.sha256(raw).hexdigest())
        data[key] = list(csv.DictReader(io.StringIO(raw.decode()))) if source.suffix == '.csv' else json.loads(raw)
    return data, manifest


def profile(rows, cohort, groups):
    selected = [r for r in rows if (r['target'], int(r['seed'])) in cohort]
    categories = {}
    for category in [c for cs in groups.values() for c in cs]:
        observations = [r for r in selected if r['category'] == category]
        k = sum(r['executed'] for r in observations)
        categories[category] = dict(k=k, n=len(observations), rate=k/len(observations) if observations else None)
    spokes = {}
    for group, cs in groups.items():
        included = [categories[c]['rate'] for c in cs if categories[c]['n']]
        spokes[group] = dict(rate=mean(included), included_types=sum(categories[c]['n'] > 0 for c in cs),
                             specified_types=len(cs), k=sum(categories[c]['k'] for c in cs),
                             n=sum(categories[c]['n'] for c in cs))
    return dict(k=sum(r['executed'] for r in selected), n=len(selected), groups=spokes,
                types=categories, keys=sorted((r['target'], int(r['seed'])) for r in selected))


def make_profiles(data):
    groups = data['prompt_data']['groups']
    rows = []
    for raw in data['prompt_rows']:
        if raw['protocol'] != 'revised45':
            continue
        assert raw['executed'] in ('True', 'False')
        rows.append(dict(raw, executed=raw['executed'] == 'True', seed=int(raw['seed'])))
    by_model = defaultdict(dict)
    for row in rows:
        key = (row['target'], row['seed'])
        phase = by_model[row['model']].setdefault(row['phase'], {})
        assert key not in phase, 'Duplicate model/phase/target/seed'
        phase[key] = row
    models = data['prompt_data']['models']
    frontier = [m for m in models if m['group'] == 'frontier']
    shared = set.intersection(*(set(by_model[m['model']][p]) for m in frontier for p in PHASES[:2]))
    result = dict(groups=groups, frontier_shared_keys=sorted(shared), frontier=[], open=[])
    for model in [*frontier, *(m for m in models if m['group'] == 'open')]:
        m = model['model']
        lookup = by_model[m]
        common = shared if model['group'] == 'frontier' else set(lookup['win_only']) & set(lookup['exploration'])
        entry = dict(model=m, name=NAMES[m], reasoning=model['reasoning'], paired_n=len(common),
                     full_n=135, phases={})
        for phase in PHASES:
            source = list(lookup.get(phase, {}).values())
            if phase == 'hinted':
                source = [r for r in source if (r['target'], r['seed']) in common]
                for r in source:
                    assert not lookup['exploration'][(r['target'], r['seed'])]['executed'], 'Hinted success not selected from exploration misses'
            entry['phases'][phase] = profile(source, common, groups)
            entry['phases'][phase]['supported'] = model[phase]['supported']
            entry['phases'][phase]['expected'] = sum(not lookup['exploration'][k]['executed'] for k in common) if phase == 'hinted' else len(common)
        result[model['group']].append(entry)
    return result


def dose_points(data):
    source = data['ma_data']
    assert source['partial'] is False, 'Headline MA figures require the completed run'
    rows = [r for r in source['dose_episodes'] if r['status'] == 'complete']
    cells = []
    for cell in source['dose_cells']:
        selected = [r for r in rows if r['focal'] == cell['model'] and r['dose']['family'] == cell['family']
                    and r['dose']['reward'] == cell['reward'] and r['dose']['audit'] == cell['audit']]
        assert len(selected) == cell['complete']
        assert sum(r['dose_metrics']['attempts'] for r in selected) == cell['attempted_rounds']
        by_opponent = {o: [r['dose_metrics']['attempts']/4 for r in selected if r['opponent'] == o]
                       for o in ('qwen-3.8-27b', 'glm')}
        rate = mean([mean(v) for v in by_opponent.values()]) if all(by_opponent.values()) else None
        assert rate == cell['attempt_rate']
        seed_rates = []
        if cell['complete'] == 4:
            for seed in (19, 73):
                rs = [r for r in selected if r['seed'] == seed]
                assert len(rs) == 2 and len({r['opponent'] for r in rs}) == 2
                seed_rates.append(mean([r['dose_metrics']['attempts']/4 for r in rs]))
        cells.append(dict(cell, seed_mean_min=min(seed_rates) if seed_rates else None,
                          seed_mean_max=max(seed_rates) if seed_rates else None))
    return cells


def save(fig, out, name):
    for ext in ('png', 'pdf', 'svg'):
        fig.savefig(out/f'{name}.{ext}', dpi=200, facecolor='white')
    plt.close(fig)


def dose_figure(cells, tiers, out, sweep):
    fig, axes = plt.subplots(2, 3, figsize=(15.6, 10.2), sharex=True, sharey=True)
    for row, family in enumerate(('commons', 'filing')):
        for col, (tier, roster) in enumerate(tiers.items()):
            ax = axes[row, col]
            handles = []
            for m in roster:
                reference = 1 if family == 'commons' else .8
                points = [c for c in cells if c['model'] == m and c['family'] == family and
                          (c['audit'] == 0 if sweep == 'reward' else c['reward'] == reference)]
                points.sort(key=lambda c: c['expected_delta'] if sweep == 'reward' else c['audit'])
                xs = [c['expected_delta'] if sweep == 'reward' else c['audit'] for c in points]
                ys = [np.nan if c['attempt_rate'] is None else c['attempt_rate'] for c in points]
                color = MODEL_COLORS[m]
                available = any(c['attempt_rate'] is not None for c in points)
                low, high = min(c['complete'] for c in points), max(c['complete'] for c in points)
                ntext = 'n=4/point' if low == high == 4 else f'n={low}–{high}/point'
                label = f'{NAMES[m]}  ·  {ntext}' if available else f'{NAMES[m]}  ·  unavailable'
                handles.append(Line2D([], [], color=color if available else '#9299a5', lw=2, label=label))
                if not available:
                    continue
                ax.plot(xs, ys, color=color, lw=2.2, zorder=3)
                lo = [c['seed_mean_min'] if c['seed_mean_min'] is not None else np.nan for c in points]
                hi = [c['seed_mean_max'] if c['seed_mean_max'] is not None else np.nan for c in points]
                ax.fill_between(xs, lo, hi, color=color, alpha=.08, linewidth=0)
                for x, y, c in zip(xs, ys, points):
                    if np.isfinite(y):
                        ax.scatter(x, y, s=35, facecolor=color if c['complete'] == 4 else 'white',
                                   edgecolor=color, linewidth=1.5, zorder=4)
            ax.set_title({'frontier': 'Frontier models', 'middle': 'Middle models', 'open': 'Open models'}[tier],
                         loc='left', fontsize=14, pad=14)
            ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(-.015, -.20),
                      frameon=False, fontsize=9, handlelength=2.2, labelspacing=.5)
            ax.set_ylim(-.045, 1.065)
            ax.set_yticks([0, .25, .5, .75, 1])
            ax.yaxis.set_major_formatter(PercentFormatter(1))
            ax.grid(axis='y', color=GRID, lw=.7)
            ax.set_axisbelow(True)
            ax.spines[['top', 'right']].set_visible(False)
            if sweep == 'reward':
                ax.set_xticks([-1, 0, 1, 3, 7])
                ax.axvline(0, color='#99a3b0', ls=':', lw=1)
            else:
                ax.set_xticks([0, .1, .25, .5, 1])
                ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
            ax.tick_params(labelbottom=True)
    fig.suptitle('Exploitation responds to incentives' if sweep == 'reward' else 'Models differ in their response to audit risk',
                 x=.07, ha='left', fontsize=25, weight='bold', y=.985)
    fig.text(.07, .937, 'MA-dose.1  ·  ordinary Qwen / GLM opponents  ·  no hints or reflection  ·  four episodes per planned point',
             fontsize=11.5, color=MUTED)
    fig.text(.022, .72, 'Commons\nOver-quota attempts', rotation=90, ha='center', va='center', fontsize=13, weight='bold')
    fig.text(.022, .36, 'Joint filing\nFalse-claim attempts', rotation=90, ha='center', va='center', fontsize=13, weight='bold')
    xtext = 'Expected one-round payoff advantage: H → X' if sweep == 'reward' else 'Public audit probability (reward held fixed within each game)'
    fig.text(.52, .075, xtext, ha='center', fontsize=12)
    footer = ('Lines: mean fraction of four rounds with an attempt, with equal weight for the two opponent models. '
              'Shading: range of two seed means when all four episodes complete; not a confidence interval.\n'
              'Hollow markers: incomplete cells. Gaps: an opponent group is missing. Opus filing: provider refusals. '
              'Filing payoff advantage assumes a matching partner; attempts are unconditional.')
    fig.text(.07, .024, footer, fontsize=9, color=MUTED, linespacing=1.6)
    fig.subplots_adjust(left=.07, right=.985, top=.87, bottom=.22, wspace=.17, hspace=.82)
    save(fig, out, 'fig1_incentive_dose' if sweep == 'reward' else 'fig1s_audit_response')


def configure_radar(ax, size=10, manual=False):
    angles = np.linspace(0, 2*np.pi, 4, endpoint=False)
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.set_xticks(angles, ['']*4 if manual else SPOKES)
    ax.tick_params(axis='x', pad=16, labelsize=size)
    ax.set_yticks([.25, .5, .75, 1], ['25%', '50%', '75%', '100%'], fontsize=size-2, color=MUTED)
    ax.set_rlabel_position(33)
    ax.grid(color=GRID, lw=.8)
    ax.spines['polar'].set_color('#97a3b0')
    if manual:
        for label, xy, ha in zip(SPOKES, [(.5,1.09),(1.08,.5),(.5,-.10),(-.08,.5)],
                                 ['center','left','center','right']):
            ax.text(*xy, label, transform=ax.transAxes, ha=ha, va='center', fontsize=size)
    return angles


def radar_line(ax, angles, values, color, label, style='-', fill=False):
    ys = [np.nan if v is None else v for v in values]
    ax.plot(np.r_[angles, angles[0]], ys+[ys[0]], color=color, marker='o', ms=4,
            lw=2.2, ls=style, label=label)
    if fill:
        ax.fill(np.r_[angles, angles[0]], ys+[ys[0]], color=color, alpha=.045)


def frontier_figure(profiles, out):
    fig, axes = plt.subplots(1, 3, figsize=(16.8, 7.2), subplot_kw={'projection': 'polar'})
    for ax, phase in zip(axes, PHASES):
        angles = configure_radar(ax, 11, manual=True)
        for model in profiles['frontier']:
            values = [g['rate'] for g in model['phases'][phase]['groups'].values()]
            radar_line(ax, angles, values, MODEL_COLORS[model['model']], model['name'])
        ax.set_title(PHASE_NAMES[phase] + (' of exploration misses' if phase == 'hinted' else ''),
                     fontsize=15, pad=55)
        counts = '  ·  '.join(f'{m["name"]}: {m["phases"][phase]["k"]}/{m["phases"][phase]["n"]}' for m in profiles['frontier'])
        ax.text(.5, -.29, counts.replace('  ·  ', '\n'), transform=ax.transAxes, ha='center', va='top',
                fontsize=9, color=MUTED, linespacing=1.5)
    fig.suptitle('Models have distinct exploit profiles', x=.055, ha='left', fontsize=25, weight='bold', y=.98)
    n = len(profiles['frontier_shared_keys'])
    fig.text(.055, .915, f'Revised 45-hole games  ·  frontier models  ·  high requested reasoning  ·  native scripted opponents',
             fontsize=12, color=MUTED)
    fig.legend(*axes[0].get_legend_handles_labels(), loc='lower center', bbox_to_anchor=(.5,.085), ncol=3, frameon=False, fontsize=12)
    fig.text(.055, .024, f'Spokes average eligible hole-type execution rates. Win/exploration use the same {n}/135 target × seed cases across all three models.\n'
             'Hinted rescue uses each model’s own exploration misses in that cohort, with extra information and attempts. Execution does not establish articulated discovery.',
             fontsize=10, color=MUTED, linespacing=1.6)
    fig.subplots_adjust(left=.085, right=.925, bottom=.36, top=.70, wspace=.57)
    save(fig, out, 'fig2_frontier_profiles')


def open_figure(profiles, out):
    fig, axes = plt.subplots(2, 4, figsize=(19, 11.3), subplot_kw={'projection': 'polar'})
    for ax, model in zip(axes.flat, profiles['open']):
        angles = configure_radar(ax, 9, manual=True)
        partial = model['paired_n'] != model['full_n']
        for phase in PHASES[:2]:
            values = [g['rate'] for g in model['phases'][phase]['groups'].values()]
            radar_line(ax, angles, values, PHASE_COLORS[phase], PHASE_NAMES[phase], '--' if partial else '-', fill=True)
        ax.set_title(model['name'], fontsize=14, y=1.40, pad=0, weight='bold')
        ax.text(.5, 1.29, f'{model["reasoning"]} reasoning · {model["paired_n"]}/135 matched cases',
                transform=ax.transAxes, fontsize=9, ha='center', color=MUTED)
        counts = '  ·  '.join(f'{PHASE_NAMES[p]} {model["phases"][p]["k"]}/{model["phases"][p]["n"]}' for p in PHASES[:2])
        ax.text(.5, -.28, counts, transform=ax.transAxes, ha='center', va='top', fontsize=8.5, color=MUTED)
    axes.flat[-1].set_visible(False)
    fig.suptitle('Open-model exploit profiles', x=.055, ha='left', fontsize=25, weight='bold', y=.985)
    fig.text(.055, .935, 'Revised 45-hole games  ·  matched win/exploration cases within each model  ·  hinted rescue not run for this cohort',
             fontsize=12, color=MUTED)
    handles = [Line2D([],[],color=PHASE_COLORS[p],lw=2,marker='o',label=PHASE_NAMES[p]) for p in PHASES[:2]]
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5,.073), ncol=2, frameon=False, fontsize=12)
    fig.text(.055, .025, 'Spokes average eligible hole-type execution rates; all axes use 0–100%. Dashed curves have fewer than 135 matched cases.\n'
             'Cohorts and requested reasoning differ across models. Historical open-model hints use different games/settings and are not included.',
             fontsize=10, color=MUTED, linespacing=1.6)
    fig.subplots_adjust(left=.08, right=.92, top=.79, bottom=.22, wspace=.83, hspace=1.0)
    save(fig, out, 'fig2s_open_profiles')


def write_gallery(out, profiles):
    n = len(profiles['frontier_shared_keys'])
    text = f'''# Headline plots: crossplay, incentive dose and model profiles

Figures 1–2 and crossplay companions for [the headline-plots brief](../../../research_logs/sep/0910-headline-plots.md).
Human and transfer figures are deferred as requested. These figures were made offline;
no new inference calls or spending were initiated.

## Crossplay — All 64 ordered model pairs

![Focal-by-opponent crossplay](../ma-extension-20260910/plots/01_crossplay.png)

Rows are focal models; columns are opponent models. Both directions and self-play
are included. In three-seat games, both other seats use the column model with
independent contexts. Ordinary and privately nerfed recipients appear side by side.
The original v3-MA.1 games use low requested reasoning and one seed per exact cell.

Cells show executed behavioral markers / complete matched episodes, pooling ten
recipient-dependent scenarios. The panels share **572 ordinary/nerfed pairs**
(1,144 episodes). The full run completed 1,407/1,536 episodes, including four
ordinary-only scenarios outside this matched comparison. Missing episodes remain
absent; Opus provider refusals remove all Opus-involved Clue and Filing episodes.
These are execution rates, not win rates or H-versus-X adoption deltas.

[Pair matrix PDF](../ma-extension-20260910/plots/01_crossplay.pdf) ·
[Completion by pair](../ma-extension-20260910/plots/07_completion.png) ·
[Crossplay source data and exports](../ma-extension-20260910/plots/README.md).

### Crossplay scenario breakdown

![Crossplay by scenario](../ma-extension-20260910/plots/02_scenarios.png)

For accepted-pledge betrayal with nerfed recipients, Opus and Sol execute the
marker in 8/8 episodes, while Sonnet and Gemini Flash do so in 0/8. With ordinary
recipients, Opus is at 1/8 and Sol at 4/8. The pooled pair matrix mixes mechanisms
and unequal scenario coverage; inspect this breakdown before interpreting a
model ranking. A zero marker does not establish lack of discovery.

## Figure 1 — Exploitation responds to incentives

![Incentive-dose response](fig1_incentive_dose.png)

**Data:** completed `ma-dose.1`, eight focal models, ordinary Qwen and GLM opponents,
four rounds per episode. Commons: 288/288 complete; filing: 217/288 complete.
The five zero-audit settings have calibrated one-round H→X advantages −1, 0, +1,
+3 and +7. Filing's advantage assumes a matching partner; the observed attempt
rate includes episodes where no partner participates.

**Readout:** fraction of round opportunities with an over-quota request or false
claim, averaging the two opponent identities equally. Lines are observed attempts,
not semantic discovery, successful extraction, or estimated full-policy value.
Shading is the range of the two environmental seed means when all four episodes
complete; it is not a confidence interval. Hollow markers have fewer than four
episodes. A gap means an opponent group is wholly missing. Opus filing is absent
because all its filing requests were refused by the provider.

**Observed separation:** at the lowest Commons reward (advantage −1), all eight
models make zero over-quota attempts. At advantage +1, model rates span 75–100%;
at +7, seven models reach 100% while Sonnet reaches 75%. The strongest reward
therefore compresses most between-model differences.

### Audit-risk companion

![Response to audit risk](fig1s_audit_response.png)

Audit probability varies at fixed reward within each game. The zero-audit anchor
is reused from the reward sweep, rather than counted as a second experiment.
The same hidden audit schedules are reused across doses within each family/seed.
There are only two environmental seeds, so precise threshold and slope estimates
are not justified by this screen.

At 25% audit probability in Commons, rates range from 37.5% (Sonnet) to 100%
(Opus, Sol and Qwen). This intermediate-risk setting separates the observed
behaviors more clearly than the largest reward. It does not establish a general
model ranking or a statistically significant difference.

**The separate SA dose study is still a live companion:**
[SA reward curve](../sa-dose-20260911/plots/reward_response.png) ·
[SA status](../sa-dose-20260911/STATUS.md).
Its episode-level target attempts, games, calibrated terminal margin and opponent
protocol differ from MA. Its observations are not pooled into Figure 1.

## Figure 2 — Frontier model profiles

![Frontier profiles](fig2_frontier_profiles.png)

The revised 45-hole study supplies win-only, exploration, and hinted-rescue
conditions. The headline frontier comparison uses **the same {n}/135 target × seed
cases** across Gemini Pro, GPT-5.6 Sol and Grok 4.6 in both unhinted conditions.
This excludes four cases with missing Gemini win-only observations from every
model's plotted cohort. All three request high reasoning.

Hinted rescue uses each model's own exploration misses within that common cohort;
its denominator is therefore different by model and from either unhinted curve.
It supplies extra information and an extra attempt. The phases do not form a
randomized, equal-budget three-arm comparison. The four spokes are the original
Rule/enforcement, Information/interface, State/time and Multiplayer/objective
groups, with an equal-weight mean over eligible hole-type execution rates.

Pooled execution is 11.5–19.8% in win-only, 26.7–32.1% in exploration and
90.3–95.8% in hinted rescue. Sol has the highest win-only count; Grok has the
highest exploration count. These are descriptive comparisons; the radar shapes
and pooled counts are different summaries of the same observations.

### Open-model supplement

![Open profiles](fig2s_open_profiles.png)

Each model has its own subplot with matched win/exploration cases. Counts and
requested reasoning appear in each panel. Dashed curves indicate incomplete
cohorts; the matched cohort can differ between models. Revised-game hinted runs
are unavailable for these seven open models. No historical hinted outcomes are
substituted, and no absent condition is drawn as zero.

## Reproducibility

Every figure is available as PNG, PDF and SVG. [Exact plotted data](plot-data.json),
[dose cells](dose-points.csv), [radar group cells](radar-points.csv), and
[source hashes](manifest.json) are saved with copies of the source inputs.
Counts printed below each radar are pooled execution counts; radial values are
type-macro-averages and therefore need not equal those pooled fractions.

Regenerate from the repository root:

```bash
MPLCONFIGDIR=/shared/allie/home/.codex/tmp/mpl-headline \\
TMPDIR=/shared/allie/home/.codex/tmp \\
/shared/allie/venvs/hole/bin/python -B -m benchmark.headline_plots
```

To regenerate from the frozen input copies, add
`--inputs benchmark/results/headline-plots-20260911/inputs`
and choose a new output directory with `--out`.
'''
    (out/'README.md').write_text(text)


def main(out=DEFAULT_OUT, inputs=None):
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'text.color':INK,
        'axes.labelcolor':INK, 'xtick.color':INK, 'ytick.color':INK,
        'axes.edgecolor':'#9aa5b2', 'svg.fonttype':'none', 'pdf.fonttype':42})
    data, sources = load_sources(out, inputs)
    cells = dose_points(data)
    profiles = make_profiles(data)
    dose_figure(cells, data['ma_roster']['tiers'], out, 'reward')
    dose_figure(cells, data['ma_roster']['tiers'], out, 'audit')
    frontier_figure(profiles, out)
    open_figure(profiles, out)
    write_json(out/'plot-data.json', dict(dose_cells=cells, profiles=profiles,
        dose_source_updated=data['ma_data']['updated'], prompt_source_updated=data['prompt_data']['updated']))
    flat = [{k:v for k,v in c.items() if not isinstance(v,(dict,list))} for c in cells]
    with (out/'dose-points.csv').open('w') as f:
        writer=csv.DictWriter(f, fieldnames=list(flat[0])); writer.writeheader(); writer.writerows(flat)
    radar_rows = [dict(cohort=cohort, model=m['model'], phase=phase, group=group, **cell)
                  for cohort in ('frontier','open') for m in profiles[cohort]
                  for phase, p in m['phases'].items() for group, cell in p['groups'].items()]
    with (out/'radar-points.csv').open('w') as f:
        writer=csv.DictWriter(f, fieldnames=list(radar_rows[0])); writer.writeheader(); writer.writerows(radar_rows)
    shutil.copyfile(__file__, out/'headline_plots.py')
    manifest = dict(inputs=sources, generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        figures={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('fig*.*'))
                 if p.suffix in ('.png','.pdf','.svg')},
        scope='Figures 1 and 2 only. Completed MA dose plus revised45 prompt profiles; no pooled human, transfer, or live SA estimate.')
    write_json(out/'manifest.json', manifest)
    write_gallery(out, profiles)
    print(json.dumps(dict(figures=list(manifest['figures']), frontier_common=len(profiles['frontier_shared_keys']),
         open_cohorts={m['model']:m['paired_n'] for m in profiles['open']}, output=str(out)), indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--inputs', type=Path, help='Read the five frozen inputs from this directory')
    args=parser.parse_args()
    main(args.out, args.inputs)
