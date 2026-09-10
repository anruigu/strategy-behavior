"""Standalone plots for the paired MA reflection screen."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

LABELS = {'v3ma_trust_messages': 'Council', 'v3ma_trust_memory': 'Account reset',
          'v3ma_signal_convention': 'Clue convention', 'v3ma_trust_pledge': 'Pledge'}
MODELS = [('claude-haiku-4.5','Haiku 4.5'), ('gpt-5-mini','GPT-5 mini'),
          ('qwen-3.8-27b','Qwen 3.8 27B'), ('glm','GLM 5.3')]


def plot(out):
    data = json.loads((out / 'report.json').read_text())
    baseline = [r for r in data['episodes'] if r['iteration'] == 1]
    pairs = data['paired_reflection']
    status_path = out/'status.json'
    status = json.loads(status_path.read_text())['status'] if status_path.exists() else ''
    fixed_cohort = status == 'finished_after_recovery' or data['new_outcomes'] == {'complete':768}
    final_ids = {r['baseline_id'] for r in pairs if r['complete'] and r['iteration']==4}
    curve_pairs = [r for r in pairs if not fixed_cohort or r['baseline_id'] in final_ids]
    fig, axes = plt.subplots(2, 4, figsize=(15, 8), sharey=True, layout='constrained')
    for row, condition in enumerate(('ordinary','nerfed')):
        for col, (game, label) in enumerate(LABELS.items()):
            ax = axes[row, col]
            first = [r for r in baseline if r['game'] == game and r['condition'] == condition
                     and (not fixed_cohort or r['id'] in final_ids)]
            rate = sum(r['marker']['episode_marker'] for r in first) / len(first) if first else np.nan
            for arm, name, color in [('transcript','Transcript only','#687a80'),('reflection','Private reflection','#087f74')]:
                points = [rate]
                for iteration in (2,3,4):
                    selected = [r for r in curve_pairs if r['complete'] and r['game'] == game and r['condition'] == condition and r['iteration'] == iteration]
                    points.append(sum(r[arm+'_marker'] for r in selected)/len(selected) if selected else np.nan)
                ax.plot(range(1,5), points, marker='o', color=color, label=name)
            counts = [len(first)] + [sum(r['complete'] and r['game'] == game and r['condition'] == condition and r['iteration'] == i for r in curve_pairs) for i in (2,3,4)]
            ax.set_xticks(range(1,5), [f'{i}\nn={n}' for i,n in zip(range(1,5),counts)])
            ax.set_ylim(-.04, 1.06)
            if game == 'v3ma_signal_convention':
                ax.axvline(3.5, color='#ba9854', linestyle=':', linewidth=1)
            ax.grid(axis='y', alpha=.2)
            ax.set_title(label + ' · ' + condition)
            if col == 0:
                ax.set_ylabel('Episode marker fraction')
            ax.set_xlabel('Play (4 has new clue targets)' if game == 'v3ma_signal_convention' else 'Play (same deterministic start)')
    axes[0,0].legend(loc='upper left', fontsize=8)
    subtitle = ('Same complete four-play lineups at every point; shared first play counted once' if fixed_cohort
                else 'Interim results: available complete pairs at each continuation; denominators may differ')
    fig.suptitle('v3-MA: reflection versus retained transcript\n'+subtitle, fontsize=14)
    for ext in ('png','svg'):
        fig.savefig(out / ('reflection-learning-curves.'+ext), dpi=180, bbox_inches='tight')
    plt.close(fig)
    final = [r for r in pairs if r['complete'] and r['iteration'] == 4]
    fig, axes = plt.subplots(1,2,figsize=(12,6),sharey=True,layout='constrained')
    for ax, condition in zip(axes, ('ordinary','nerfed')):
        values = np.full((4,4), np.nan)
        counts = {}
        for i,(model, _) in enumerate(MODELS):
            for j,game in enumerate(LABELS):
                group = [r for r in final if r['focal'] == model and r['game'] == game and r['condition'] == condition]
                if group:
                    a = sum(r['transcript_marker'] for r in group)
                    b = sum(r['reflection_marker'] for r in group)
                    values[i,j] = (b-a)/len(group)
                    counts[(i,j)] = f'{a}/{len(group)} → {b}/{len(group)}'
        im = ax.imshow(np.ma.masked_invalid(values), vmin=-1, vmax=1, cmap='BrBG', aspect='auto')
        ax.set_title(condition.capitalize()+' opponents')
        ax.set_xticks(range(4), list(LABELS.values()), rotation=30, ha='right')
        ax.set_yticks(range(4), [name for _,name in MODELS])
        for (i,j), count in counts.items():
            ax.text(j,i,count,ha='center',va='center',fontsize=9,color='white' if abs(values[i,j])>.6 else '#18343b')
    fig.colorbar(im, ax=axes, shrink=.7, label='Marker fraction: reflection − transcript')
    fig.suptitle('Play 4 · new clue targets; repeated trust games\nCell counts: transcript only → reflection; at most four opponent lineups per cell', fontsize=13)
    for ext in ('png','svg'):
        fig.savefig(out / ('reflection-model-effects.'+ext), dpi=180, bbox_inches='tight')
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10,6),layout='constrained')
    rows = [r for r in data['summaries'] if r['iteration'] == 4]
    for i,r in enumerate(rows):
        if r['mean_score_delta'] is None:
            continue
        if r['score_delta_bootstrap95']:
            ax.plot(r['score_delta_bootstrap95'],[i,i],color='#087f74',linewidth=2)
        ax.scatter([r['mean_score_delta']],[i],color='#18343b')
        ax.annotate(f' n={r["complete_pairs"]}',(r['mean_score_delta'],i),xytext=(5,5),textcoords='offset points',fontsize=9)
    ax.axvline(0,color='gray',linewidth=1)
    ax.set_yticks(range(len(rows)),[LABELS[r['game']]+' · '+r['condition'] for r in rows])
    ax.invert_yaxis()
    ax.set_xlabel('Final-play focal payoff: reflection − transcript (game-specific points)')
    ax.set_title('Reflection payoff difference at play 4\nExploratory 95% paired-episode bootstrap intervals; fixed model lineups')
    for ext in ('png','svg'):
        fig.savefig(out / ('reflection-payoffs.'+ext), dpi=180, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();plot(args.out)
