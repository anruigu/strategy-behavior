"""Standalone figures from completed episode aggregates; never mixes payoff scales."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot(out):
    data = json.loads((out / 'report.json').read_text())
    models = ['claude-haiku-4.5', 'gpt-5-mini', 'qwen-3.8-27b', 'glm']
    labels = ['Haiku 4.5', 'GPT-5 mini', 'Qwen 3.8 27B', 'GLM 5.3']
    games = [g['game'] for g in data['games']]
    lookup = {(c['game'], c['focal'], c['condition']): c for c in data['cells']}
    fig, axes = plt.subplots(1, 2, figsize=(12, max(3.5, .35*len(games)+2)), sharey=True, layout='constrained')
    for ax, condition in zip(axes, ('ordinary', 'nerfed')):
        values = np.full((len(games), len(models)), np.nan)
        counts = {}
        for i, game in enumerate(games):
            for j, model in enumerate(models):
                cell = lookup.get((game, model, condition))
                if cell and cell['complete']:
                    values[i, j] = cell['marker_episodes'] / cell['complete']
                    counts[(i, j)] = f'{cell["marker_episodes"]}/{cell["complete"]}'
        im = ax.imshow(np.ma.masked_invalid(values), vmin=0, vmax=1, cmap='Blues', aspect='auto')
        ax.set_title(condition.capitalize() + ' opponents')
        ax.set_xticks(range(len(models)), labels, rotation=35, ha='right')
        ax.set_yticks(range(len(games)), [g.removeprefix('v3ma_').replace('_', ' ') for g in games])
        for (i, j), count in counts.items():
            ax.text(j, i, count, ha='center', va='center', fontsize=9,
                    color='white' if values[i, j] > .55 else '#17202a')
    fig.colorbar(im, ax=axes, shrink=.7, label='Episodes with diagnostic marker / completed episodes')
    fig.suptitle(f'v3-MA cross-play: {data["outcomes"].get("complete", 0)}/{data["planned"]} episodes complete\n'
                 'Behavioral markers; blank = no applicable completed cell. Commons have no nerfed condition.', fontsize=12)
    fig.savefig(out / 'behavior-markers.png', dpi=180, bbox_inches='tight')
    fig.savefig(out / 'behavior-markers.svg', bbox_inches='tight')
    plt.close(fig)
    pairs = [p for p in data['matched_pairs'] if p['complete']]
    if pairs:
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), sharey=True, layout='constrained')
        for ax, condition in zip(axes, ('ordinary', 'nerfed')):
            values = np.full((len(models), len(models)), np.nan)
            counts = {}
            for i, focal in enumerate(models):
                for j, opponent in enumerate(models):
                    cell = [p for p in pairs if p['focal'] == focal and p['opponent'] == opponent]
                    if cell:
                        hits = sum(p[condition + '_marker'] for p in cell)
                        values[i, j] = hits / len(cell)
                        counts[(i, j)] = f'{hits}/{len(cell)}'
            im = ax.imshow(np.ma.masked_invalid(values), vmin=0, vmax=1, cmap='Blues')
            ax.set_xticks(range(len(models)), labels, rotation=35, ha='right')
            ax.set_yticks(range(len(models)), labels)
            ax.set_title(condition.capitalize() + ' opponents')
            ax.set_xlabel('Opponent model (all other seats)')
            for (i, j), count in counts.items():
                ax.text(j, i, count, ha='center', va='center',
                        color='white' if values[i, j] > .55 else '#17202a')
        axes[0].set_ylabel('Focal model')
        fig.colorbar(im, ax=axes, shrink=.7, label='Diagnostic-marker fraction')
        fig.suptitle('Cross-play matrix: matched completed episodes only\nTen recipient-dependent scenarios; pooled marker counts describe coverage, not intent', fontsize=12)
        fig.savefig(out/'crossplay-matrix.png', dpi=180, bbox_inches='tight')
        fig.savefig(out/'crossplay-matrix.svg', bbox_inches='tight')
        plt.close(fig)
    paired = [g for g in data['games'] if g['matched_pairs']]
    if paired:
        fig, ax = plt.subplots(figsize=(9, 6), layout='constrained')
        for i, g in enumerate(paired):
            x = g['paired_payoff_delta']
            ci = g['paired_payoff_bootstrap95']
            if ci:
                ax.plot(ci, [i, i], color='#2874a6', linewidth=2)
            ax.scatter([x], [i], color='#17202a', zorder=3)
            ax.annotate(f' n={g["matched_pairs"]}', (x, i), xytext=(5, 5), textcoords='offset points', fontsize=8)
        ax.axvline(0, color='gray', linewidth=1)
        ax.set_yticks(range(len(paired)), [g['game'].removeprefix('v3ma_').replace('_', ' ') for g in paired])
        ax.invert_yaxis()
        ax.set_xlabel('Focal payoff: nerfed − ordinary (game-specific points; scales differ)')
        ax.set_title('Paired treatment differences within each scenario\nExploratory 95% episode-bootstrap intervals; fixed model lineups')
        fig.savefig(out / 'paired-payoffs.png', dpi=180, bbox_inches='tight')
        fig.savefig(out / 'paired-payoffs.svg', bbox_inches='tight')
        plt.close(fig)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    plot(a.out)
