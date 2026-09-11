"""Read-only analysis of the original MA screen; export model-comparison figures."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import numpy as np

MODELS = ['claude-haiku-4.5', 'gpt-5-mini', 'qwen-3.8-27b', 'glm']
LABELS = ['Haiku 4.5', 'GPT-5 mini', 'Qwen 3.8 27B', 'GLM 5.3']
COLORS = ['#738299', '#8260c5', '#248f80', '#e38a20']
FAMILIES = {
    'Repeated\ninteraction': ['trust_retaliation', 'trust_pledge', 'trust_memory', 'trust_messages'],
    'Restricted\ninformation': ['signal_notes', 'signal_convention'],
    'Joint\nfiling': ['filing_attestation', 'filing_settlement'],
    'Market': ['market_value', 'market_ceiling'],
}
SCENARIOS = {
    'trust_retaliation': 'Missed retaliation', 'trust_pledge': 'Pledge betrayal',
    'trust_memory': 'Account reset', 'trust_messages': 'Council messages',
    'signal_notes': 'Explicit clue notes', 'signal_convention': 'Clue convention',
    'market_value': 'False value claim', 'market_ceiling': 'Unfunded ceiling',
    'filing_attestation': 'False attestation', 'filing_settlement': 'Invoice over-redemption',
}
COMMONS = ['abundant', 'crowded', 'collapse', 'threshold']


def main(root):
    report = json.loads((root / 'report.json').read_text())
    out = root / 'plots' / 'model-separation'
    out.mkdir(parents=True, exist_ok=True)
    pairs = [p for p in report['matched_pairs'] if p['complete']]
    assert len(pairs) == 313
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none', 'pdf.fonttype': 42})
    exported = []

    def save(fig, name):
        for ext in ('png', 'svg', 'pdf'):
            fig.savefig(out / f'{name}.{ext}', dpi=190, facecolor='white')
        plt.close(fig)

    def heading(fig, title, subtitle):
        fig.suptitle(title, fontsize=23, y=.97)
        fig.text(.5, .915, subtitle, ha='center', color='#495566', fontsize=11)

    def legend(fig, y=.085):
        handles = [Line2D([0], [0], color=c, marker='o', lw=2.5, label=l)
                   for c, l in zip(COLORS, LABELS)]
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5, y), ncol=4, frameon=False)

    def cell(game, focal, condition):
        pp = [p for p in pairs if p['game'] == 'v3ma_' + game and p['focal'] == focal]
        return sum(p[condition + '_marker'] for p in pp), len(pp)

    # Macro-average scenario marker rates within a family, same paired sample on both panels.
    fig, axes = plt.subplots(1, 2, figsize=(14, 8), subplot_kw={'projection': 'polar'})
    fig.subplots_adjust(top=.76, bottom=.21, left=.10, right=.86, wspace=.65)
    angles = np.arange(4) * 2 * np.pi / 4
    for ax, condition in zip(axes, ('ordinary', 'nerfed')):
        ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
        ax.set_xticks(angles, FAMILIES.keys()); ax.tick_params(axis='x', pad=17)
        ax.set_ylim(0, 1); ax.set_yticks([.25, .5, .75, 1], ['25%', '50%', '75%', '100%'])
        position = ax.get_position()
        fig.text((position.x0 + position.x1)/2, .855,
                 condition.capitalize() + ' recipients', ha='center', fontsize=16)
        ax.get_xticklabels()[1].set_ha('left')
        ax.get_xticklabels()[3].set_ha('right')
        ax.grid(color='#bec3ca', linewidth=.8)
        for model, label, color in zip(MODELS, LABELS, COLORS):
            values = []
            for family, games in FAMILIES.items():
                rate = np.mean([h/n for h, n in (cell(g, model, condition) for g in games)])
                values.append(rate)
                exported.append(dict(figure='radar', model=model, condition=condition,
                                     group=family.replace('\n', ' '), rate=float(rate)))
            ax.plot(np.r_[angles, angles[0]], values + values[:1], color=color, lw=2.5, marker='o', ms=6)
    heading(fig, 'Model separation in v3-MA', 'Original four-model screen · ordinary versus privately nerfed recipients · no training or reflection')
    legend(fig)
    fig.text(.5, .035, 'Macro-average of scenario marker rates within each family; 313 matched completed pairs.\n'
             'Observed behavior, not inferred discovery. Commons excluded: no nerfed condition was sampled.', ha='center', fontsize=10)
    save(fig, '01_family_radar')

    # Per-scenario rates and denominators expose the differences hidden by a macro-average.
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))
    fig.subplots_adjust(top=.82, bottom=.20, left=.20, right=.89, wspace=.22)
    for ax, condition in zip(axes, ('ordinary', 'nerfed')):
        vals = np.empty((len(SCENARIOS), 4)); counts = {}
        for i, game in enumerate(SCENARIOS):
            for j, model in enumerate(MODELS):
                hits, n = cell(game, model, condition)
                vals[i, j] = hits/n; counts[i,j] = f'{hits}/{n}'
                exported.append(dict(figure='scenario', model=model, condition=condition,
                                     group=game, hits=hits, n=n, rate=hits/n))
        im = ax.imshow(vals, vmin=0, vmax=1, cmap='Blues', aspect='auto')
        ax.set_title(condition.capitalize() + ' recipients', fontsize=16, pad=14)
        ax.set_xticks(range(4), LABELS, rotation=25, ha='right')
        ax.set_yticks(range(len(SCENARIOS)), list(SCENARIOS.values()) if condition == 'ordinary' else ['']*len(SCENARIOS))
        ax.tick_params(length=0)
        for (i,j), count in counts.items():
            ax.text(j, i, count, ha='center', va='center', color='white' if vals[i,j]>.55 else '#152337', fontsize=12)
        for y in (3.5, 5.5, 7.5): ax.axhline(y, color='white', lw=3)
    cax = fig.add_axes([.92, .26, .015, .49]); cb=fig.colorbar(im, cax=cax)
    cb.ax.yaxis.set_major_formatter(PercentFormatter(1)); cb.set_label('Episodes with marker')
    heading(fig, 'Which mechanisms separate the models?', 'Each cell is hit episodes / completed matched pairs · identical ordinary and nerfed denominators')
    fig.text(.5, .04, 'Eight pairs per model/scenario except ceiling (6–7); seven failures excluded from both conditions.\n'
             'Convention consistency may occur by chance; council-message markers are associational. Zeros do not prove robustness.', ha='center', fontsize=10)
    save(fig, '02_scenario_heatmap')

    # Separate focal behavior from opponent susceptibility, using the same matched sample.
    fig, axes = plt.subplots(1, 2, figsize=(12, 7.8))
    fig.subplots_adjust(top=.79, bottom=.23, left=.14, right=.87, wspace=.28)
    for ax, condition in zip(axes, ('ordinary', 'nerfed')):
        vals=np.zeros((4,4)); counts={}
        for i, focal in enumerate(MODELS):
            for j, opponent in enumerate(MODELS):
                pp=[p for p in pairs if p['focal']==focal and p['opponent']==opponent]
                h=sum(p[condition+'_marker'] for p in pp); vals[i,j]=h/len(pp)
                counts[i,j]=f'{h}/{len(pp)}'
                exported.append(dict(figure='crossplay', model=focal, opponent=opponent,
                                     condition=condition, hits=h, n=len(pp), rate=h/len(pp)))
        im=ax.imshow(vals,vmin=0,vmax=.4,cmap='Blues',aspect='equal')
        ax.set_xticks(range(4),LABELS,rotation=25,ha='right')
        ax.set_yticks(range(4),LABELS if condition=='ordinary' else ['']*4)
        ax.set_title(condition.capitalize()+' recipients',fontsize=15,pad=12)
        ax.set_xlabel('Opponent model',labelpad=12); ax.tick_params(length=0)
        for (i,j),count in counts.items():
            ax.text(j,i,count,ha='center',va='center',color='white' if vals[i,j]>.22 else '#152337',fontsize=12)
    axes[0].set_ylabel('Focal model',labelpad=12)
    cax=fig.add_axes([.91,.31,.018,.36]);cb=fig.colorbar(im,cax=cax)
    cb.ax.yaxis.set_major_formatter(PercentFormatter(1));cb.set_label('Marker fraction (0–40% scale)')
    heading(fig,'Does separation depend on the opponent?', 'Ten recipient-dependent scenarios · matched lineups and seeds · raw counts shown')
    fig.text(.5,.045,'Pooled marker frequencies describe scenario coverage, not a general hack rate or model ranking.\n'
             'These are the ordinary/nerfed interventions; no hinted-execution condition was run.',ha='center',fontsize=10)
    save(fig,'03_opponent_crossplay')

    # Commons measures adoption, not different model-specific payoff functions.
    fig, axes=plt.subplots(1,2,figsize=(14,7.5),sharey=True)
    fig.subplots_adjust(top=.78,bottom=.27,left=.08,right=.97,wspace=.15)
    commons_labels=['Abundant\nΔ: + + +','Crowded\nΔ: + − −','Collapse\nΔ: + + +','Threshold\nΔ: − + +']
    width=.19
    for j,(model,label,color) in enumerate(zip(MODELS,LABELS,COLORS)):
        ep_rates=[];round_rates=[];nums=[]
        for variant in COMMONS:
            ee=[e for e in report['episodes'] if e['status']=='complete' and e['focal']==model and e['game']=='v3ma_commons_'+variant]
            assert len(ee)==8
            hits=sum(e['marker']['episode_marker'] for e in ee)
            rounds=sum(e['marker']['rounds'] for e in ee);rh=sum(e['marker']['hit_rounds'] for e in ee)
            assert rounds==32
            ep_rates.append(hits/len(ee));round_rates.append(rh/rounds);nums.append((hits,rh))
            exported.append(dict(figure='commons',model=model,condition='ordinary',group=variant,
                                 hits=hits,n=len(ee),rate=hits/len(ee),round_hits=rh,round_n=rounds,round_rate=rh/rounds))
        x=np.arange(4)+(j-1.5)*width
        for panel,(ax,values) in enumerate(zip(axes,(ep_rates,round_rates))):
            ax.bar(x,values,width=width*.9,color=color,zorder=3)
            for xx,y,(eh,rh) in zip(x,values,nums):
                ax.text(xx,y+.016,str(eh if panel==0 else rh),ha='center',va='bottom',fontsize=9,color=color)
    for ax,title in zip(axes,('Any over-quota action in the episode','How often the focal exceeds quota')):
        ax.set_title(title,fontsize=15,pad=14);ax.set_xticks(range(4),commons_labels)
        ax.set_ylim(0,1.12);ax.set_yticks(np.arange(0,1.01,.25));ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis='y',alpha=.25,zorder=0);ax.tick_params(axis='x',length=0)
    axes[0].set_ylabel('Fraction'); heading(fig,'Commons: adoption differs sharply across models', 'Ordinary opponents only · the Δ(k) payoff schedules are shared by every model')
    legend(fig,y=.12)
    fig.text(.5,.04,'Labels are counts: left out of 8 episodes, right out of 32 rounds per model/variant. Over-quota means catch > 2.\n'
             'Δ signs refer to the one-season H=2 / X=6 comparison; model choices may use other amounts. Repeated rounds are not independent.',ha='center',fontsize=10)
    save(fig,'04_commons_adoption')

    metadata=dict(source=str(root/'report.json'),sha256=hashlib.sha256((root/'report.json').read_bytes()).hexdigest(),
                  complete_episodes=report['outcomes']['complete'],matched_pairs=len(pairs),rows=exported)
    (out/'plot-data.json').write_text(json.dumps(metadata,indent=2)+'\n')
    fields=sorted({k for r in exported for k in r})
    with (out/'plot-data.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(exported)
    (out/'README.md').write_text('''# Model separation in the original v3-MA screen

Source: `v3-ma-four-model-20260909`, 761/768 completed episodes. These figures
do not include the reflection follow-up or revised V4 games. All model labels
refer to the focal unless the axis explicitly says opponent.

1. [Family radar](01_family_radar.png): scenario-macro-averaged marker rates;
   ordinary and nerfed panels use the same 313 completed pairs. Markets remain
   zero for all models. Commons are separate because no nerfed condition exists.
2. [Scenario heatmap](02_scenario_heatmap.png): the most useful view of model
   differences. Exact counts expose the small denominators. Qwen is strongest
   on explicit clue notes; GPT-5 mini on the full-episode convention marker;
   GLM alone activates invoice over-redemption. Pledge is widely activated with
   nerfed recipients, while Haiku accounts for the three ordinary pledge hits.
3. [Opponent cross-play](03_opponent_crossplay.png): checks whether a model's
   apparent advantage depends on the recipient. Pooled heterogeneous markers
   are descriptive coverage, not a general exploit rate. Its color scale is
   explicitly 0–40%; the scenario heatmap uses 0–100%.
4. [Commons adoption](04_commons_adoption.png): episode prevalence and round
   frequency. Qwen/GPT-5 mini exceed quota much more often in crowded Commons
   than GLM; adoption is not synonymous with beneficial action. In crowded
   Commons joining can be disadvantageous when others also exceed quota.

These plots show descriptive separation in this fixed sample, not statistical
model rankings. Each scenario/model generally has only 8 episodes (four opponent
models × two environment seeds). Seven missing ceiling outcomes are excluded
from both members of the paired recipient comparison. Round-level counts are
clustered within episodes. Markers measure behavior, not discovery; conventions
can coincide by chance and council-message markers are associational.

Every figure is exported as PNG, SVG, and PDF. `plot-data.json` and `plot-data.csv`
contain the exact plotted numerators, denominators, and aggregates; JSON also
records the source report hash. No new model calls or simulations are made.

Regenerate from the repository root:

```bash
MPLCONFIGDIR=/shared/allie/home/.codex/tmp/mpl-v3ma-separation \\
  /shared/allie/venvs/hole/bin/python -B -m benchmark.v3_ma.plot_model_separation \\
  --out benchmark/results/v3-ma-four-model-20260909
```
''')
    print(f'Wrote four figures (PNG/SVG/PDF), data, and README to {out}')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path('benchmark/results/v3-ma-four-model-20260909'))
    main(parser.parse_args().out)
