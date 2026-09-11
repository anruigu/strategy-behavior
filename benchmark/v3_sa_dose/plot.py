"""Read-only inference analysis, exact plotted CSV and publication-format figures."""
import argparse
from collections import Counter
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from benchmark.clients import now, write_json
from .run import read, file_hash, verify_plan, verify_trace
from .specs import LABELS, MARGINS

MODEL_LABELS = {'gpt-5.6-sol': 'GPT-5.6 Sol', 'gemini-3.1-pro': 'Gemini 3.1 Pro',
                'qwen-3.8-27b-medium': 'Qwen 3.8 27B', 'glm': 'GLM 5.3'}
COLORS = ('#2667b5', '#da7b26', '#268b78', '#9358a4')


def wilson(k, n):
    if n == 0:
        return None, None
    z = 1.959963984540054
    center = (k / n + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(k / n * (1 - k / n) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    # The interval contains the observed proportion. Roundoff at k=0 or k=n
    # can otherwise make an error-bar length negative (e.g. k=0, n=3).
    rate = k / n
    return min(rate, max(0.0, center - half)), max(rate, min(1.0, center + half))


def collect(out):
    plan = read(out / 'plan.json')
    verify_plan(out, plan, sources=False)
    episodes = []
    for task in plan['tasks']:
        path = out / 'episodes' / task['id'] / 'trace.json'
        trace = read(path) if path.exists() else None
        if trace:
            verify_trace(trace, task, plan)
            if trace.get('inference_kind') != 'model':
                raise ValueError('Scripted/demonstration outcomes cannot enter model figures')
        episodes.append(dict(task=task, status=trace['status'] if trace else 'not_started',
                             metrics=trace.get('metrics') if trace and trace['status'] == 'complete' else None,
                             trace_sha256=file_hash(path) if trace else None))
    cells = []
    for family in LABELS:
        for model in plan['models']:
            groups = sorted({e['task']['cell'] for e in episodes
                             if e['task']['family'] == family and e['task']['model'] == model})
            for cell_id in groups:
                group = [e for e in episodes if e['task']['family'] == family
                         and e['task']['model'] == model and e['task']['cell'] == cell_id]
                complete = [e for e in group if e['metrics'] is not None]
                n = len(complete)
                k = sum(e['metrics']['attempted'] for e in complete)
                executed = sum(e['metrics']['executed'] for e in complete)
                low, high = wilson(k, n)
                task = group[0]['task']
                cells.append(dict(family=family, model=model, cell=cell_id, sweep=task['sweep'],
                                  level=task['level'], reward=task['dose']['reward'], audit=task['dose']['audit'],
                                  calibrated_margin_delta=task.get('calibrated_margin_delta'),
                                  n=n, planned=len(group), attempted=k, executed=executed,
                                  rate=k / n if n else None, execution_rate=executed / n if n else None,
                                  ci_low=low, ci_high=high, statuses=dict(Counter(e['status'] for e in group)),
                                  episode_ids=[e['task']['id'] for e in complete],
                                  invalid_actions=sum(e['metrics']['invalid_count'] for e in complete)))
    return dict(protocol=plan['protocol'], plan_identity=plan['identity'], updated=now(),
                source_hashes=plan['source_hashes'], calibration_sha256=plan['calibration_sha256'],
                completion=dict(Counter(e['status'] for e in episodes)),
                interval='95% Wilson interval over independent episode attempts; decisions are not independent samples.',
                cells=cells, episodes=episodes), plan


def save(fig, out, name):
    for suffix in ('png', 'pdf', 'svg'):
        fig.savefig(out / f'{name}.{suffix}', dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def style(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=.18)
    ax.set_axisbelow(True)


def response_plot(data, plan, out, sweep):
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.9), sharey=True)
    complete = data['completion'].get('complete', 0)
    expected = len(plan['tasks'])
    suffix = ' · awaiting model runs' if not complete else ' · provisional' if complete < expected else ''
    fig.suptitle(('SA incentive response' if sweep == 'reward' else 'SA detection-risk response') + suffix,
                 fontsize=18, y=1.03)
    for ax, family in zip(axes, LABELS):
        style(ax)
        ax.set_title(LABELS[family], fontsize=13)
        any_points = False
        for i, model in enumerate(plan['models']):
            rows = [c for c in data['cells'] if c['family'] == family and c['model'] == model
                    and (c['sweep'] == sweep or (sweep == 'audit' and c['cell'] == 'reward-3'))]
            rows.sort(key=lambda c: c['audit'] if sweep == 'audit' else c['level'])
            xs = [c['audit'] if sweep == 'audit' else c['calibrated_margin_delta'] for c in rows]
            ys = [c['rate'] if c['rate'] is not None else np.nan for c in rows]
            # NaNs break curves at missing doses; no interpolation across missing cells.
            ax.plot(xs, ys, 'o-', color=COLORS[i % len(COLORS)], label=MODEL_LABELS.get(model, model), lw=1.8, ms=5)
            for x, c in zip(xs, rows):
                if c['n']:
                    any_points = True
                    ax.errorbar(x, c['rate'], yerr=[[c['rate'] - c['ci_low']], [c['ci_high'] - c['rate']]],
                                fmt='none', color=COLORS[i % len(COLORS)], alpha=.35, capsize=3)
                    ax.annotate(f'n={c["n"]}', (x, c['rate']), xytext=(4, 7 + i * 8),
                                textcoords='offset points', fontsize=7, color=COLORS[i % len(COLORS)])
        if not any_points:
            ax.text(.5, .5, 'No model observations yet', transform=ax.transAxes, ha='center', color='#777777')
        if sweep == 'reward':
            ax.axvline(0, color='#777777', ls=':', lw=1)
            ax.set_xticks(MARGINS)
            ax.set_xlim(-1.5, 7.6)
            ax.set_xlabel('Calibrated final score-margin advantage (X − H)')
        else:
            ax.set_xticks([0, .1, .25, .5, 1])
            ax.set_xlim(-.04, 1.05)
            ax.set_xlabel('Inspection probability (fixed reward)')
        ax.set_ylim(-.04, 1.13)
        ax.set_yticks([0, .25, .5, .75, 1], ['0%', '25%', '50%', '75%', '100%'])
    axes[0].set_ylabel('Episodes with an exploit attempt')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=len(plan['models']), bbox_to_anchor=(.5, -.08), frameon=False)
    fig.text(.5, -.11, 'Attempts precede enforcement · 95% episode-level intervals · missing outcomes stay missing',
             ha='center', fontsize=9)
    fig.tight_layout()
    save(fig, out, f'{sweep}_response')


def calibration_plot(calibration, out):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    for ax, family in zip(axes, LABELS):
        rows = [r for r in calibration['rows'] if r['family'] == family and r['sweep'] == 'reward']
        seed = rows[0]['seed']
        rows = sorted((r for r in rows if r['seed'] == seed), key=lambda r: r['level'])
        ax.plot([r['dose']['reward'] for r in rows], [r['margin_delta'] for r in rows], 'o-', color='#2667b5')
        ax.axhline(0, ls=':', color='#777777')
        for r in rows:
            ax.annotate(f'{r["margin_delta"]:+.0f}', (r['dose']['reward'], r['margin_delta']),
                        xytext=(4, 7), textcoords='offset points')
        ax.set_title(LABELS[family])
        ax.set_xlabel('Payment per excess unit')
        ax.set_ylabel('Final score-margin difference (X − H)')
        ax.set_ylim(-2, 8.5)
        style(ax)
    fig.suptitle('SA engine calibration · scripted policies, not model behavior', fontsize=15, y=1.03)
    fig.tight_layout()
    save(fig, out, 'payoff_calibration')


def report(root):
    root = Path(root).resolve()
    data, plan = collect(root)
    out = root / 'plots'
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'plot-data.json', data)
    columns = ['family', 'model', 'cell', 'sweep', 'level', 'reward', 'audit', 'calibrated_margin_delta',
               'n', 'planned', 'attempted', 'executed', 'rate', 'execution_rate', 'ci_low', 'ci_high', 'invalid_actions']
    with (out / 'dose-cells.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data['cells'])
    response_plot(data, plan, out, 'reward')
    if plan['stage'] == 'full':
        response_plot(data, plan, out, 'audit')
    calibration_plot(read(root / 'calibration.json'), out)
    complete = data['completion'].get('complete', 0)
    text = (f'**SA incentive dose — {complete}/{len(plan["tasks"])} model episodes complete**\n\n'
            f'Updated {data["updated"]}. Completion: `{data["completion"]}`.\n\n'
            '![Reward response](reward_response.png)\n\n')
    if plan['stage'] == 'full':
        text += '![Audit response](audit_response.png)\n\n'
    text += ('![Scripted payoff calibration](payoff_calibration.png)\n\n'
             'Reward x-values are complete fixed-policy score-margin differences, calibrated before inference. '
             'The legal Commons comparator is optimized over all legal catch sequences; the exploit comparator is a fixed policy. '
             'These comparisons do not estimate the advantage of an adaptive model policy.\n\n'
             'The primary outcome is any target-exploit attempt per episode. Zero-price acceptance can still be execution. '
             'Inspection can prevent execution without preventing attempts. Exact execution counts and rates are in '
             '[dose-cells.csv](dose-cells.csv); all planned task statuses and observed trace hashes are in '
             '[plot-data.json](plot-data.json). Refusals, provider failures and missing runs are not zero-rate outcomes.\n\n'
             'Intervals treat episodes as independent sampling replicates, not decisions. Five replicates per cell '
             'support descriptive curves only. No discovery, threshold, asymptotic maximum or exploration-cost estimate is claimed. '
             'All figures have PDF and SVG exports. These variants are separate from historical v3-SA and from MA-dose.\n')
    (out / 'README.md').write_text(text)
    print(f'Plots and exact cells: {out} ({complete} model episodes)', flush=True)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    report(parser.parse_args().root)
