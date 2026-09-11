"""Render the prediction pilot's held-out metrics and calibration, with honest scope."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model45 import losses

NAMES={'global_rate':'Global rate','model_prompt':'Model + prompt','taxonomy':'Taxonomy + context','interface':'Interface + context','structure':'Structure + context'}
SCHEMES={'edition':'Held-out edition','family':'Held-out game family','mechanism':'Held-out mechanism','mechanism_purged_family':'Held-out mechanism + its families'}


def build(out):
    metrics=json.loads((out/'metrics.json').read_text());protocol=json.loads((out/'protocol.json').read_text())
    provenance=json.loads((out/'feature-provenance.json').read_text());outcomes=json.loads((out/'outcome-provenance.json').read_text())
    with (out/'out-of-fold-predictions.csv').open() as f:predictions=list(csv.DictReader(f))
    for r in predictions:r.update(y=int(r['y']),probability=float(r['probability']))
    plots=out/'plots';plots.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    def save(fig,name):
        for ext in ['png','svg','pdf']:fig.savefig(plots/f'{name}.{ext}',dpi=170,bbox_inches='tight',facecolor='white')
        plt.close(fig)
    colors=['#b5bdc4','#587286','#bb874b','#719d93','#226a92']
    for cohort in ['unhinted','hinted']:
        fig,axes=plt.subplots(2,2,figsize=(13,9),sharey=True);fig.subplots_adjust(hspace=.50,wspace=.25,top=.86,bottom=.15)
        for ax,(scheme,title) in zip(axes.flat,SCHEMES.items()):
            selected=[r for r in metrics if r['cohort']==cohort and r['scheme']==scheme]
            ax.bar(range(len(selected)),[r['brier'] for r in selected],color=colors)
            ax.set_xticks(range(len(selected)),[NAMES[r['method']] for r in selected],rotation=22,ha='right',fontsize=9)
            for i,r in enumerate(selected):ax.text(i,r['brier']+.004,f"{r['brier']:.3f}",ha='center',fontsize=9)
            ax.set_title(title,weight='bold');ax.set_ylim(0,.36 if cohort=='unhinted' else .25);ax.set_ylabel('Out-of-sample Brier score ↓');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
            ax.spines[['top','right']].set_visible(False)
        fig.suptitle('Prediction pilot · '+('unhinted activation' if cohort=='unhinted' else 'hinted execution on selected prior misses'),fontsize=19,weight='bold')
        fig.text(.05,.045,'Lower is better. All seeds, player models and prompt variants of a held-out unit are excluded from training.',fontsize=10,color='#617780')
        fig.text(.05,.015,'Structure includes canonical-witness features; this is a retrospective pilot, not prospective or discovery prediction.',fontsize=10,color='#617780')
        save(fig,cohort+'_heldout_brier')
    fig,axes=plt.subplots(1,2,figsize=(13,5.8));fig.subplots_adjust(bottom=.20,top=.82,wspace=.30)
    calibration=[]
    for ax,cohort in zip(axes,['unhinted','hinted']):
        ax.plot([0,1],[0,1],ls='--',color='#a6afb6')
        for method,color in [('model_prompt','#587286'),('structure','#226a92')]:
            rows=[r for r in predictions if r['cohort']==cohort and r['scheme']=='family' and r['method']==method]
            points=[]
            for i in range(10):
                selected=[r for r in rows if min(9,int(r['probability']*10))==i]
                if not selected:continue
                point=dict(cohort=cohort,method=method,bin=i,n=len(selected),predicted=float(np.mean([r['probability'] for r in selected])),observed=float(np.mean([r['y'] for r in selected])))
                calibration.append(point);points.append(point)
            ax.plot([p['predicted'] for p in points],[p['observed'] for p in points],marker='o',color=color,label=NAMES[method])
        ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_xlabel('Predicted activation probability');ax.set_ylabel('Observed activation frequency')
        ax.set_title(cohort.capitalize());ax.legend(frameon=False);ax.grid(alpha=.15)
    fig.suptitle('Calibration on held-out game families',fontsize=19,weight='bold')
    fig.text(.05,.045,'Fixed 0.1 probability bins; bin counts are exported. Points are descriptive, not independent confidence intervals.',fontsize=10,color='#617780')
    save(fig,'calibration')
    (out/'calibration.json').write_text(json.dumps(calibration,indent=2)+'\n')
    diagnostics=[]
    for cohort in ['unhinted','hinted']:
        relevant=[r for r in predictions if r['cohort']==cohort and r['scheme']=='family']
        for family in sorted({r['family'] for r in relevant}):
            d=dict(cohort=cohort,family=family)
            for method in ['model_prompt','interface','structure']:
                rows=[r for r in relevant if r['family']==family and r['method']==method]
                y=[r['y'] for r in rows];p=[r['probability'] for r in rows]
                d[method]=dict(n=len(rows),observed=float(np.mean(y)),predicted=float(np.mean(p)),brier=float(losses(y,p)[0].mean()))
            diagnostics.append(d)
    (out/'family-diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    def metric(cohort,scheme,method):return next(r for r in metrics if (r['cohort'],r['scheme'],r['method'])==(cohort,scheme,method))
    main=metric('unhinted','family','structure');base=metric('unhinted','family','model_prompt')
    strict=metric('unhinted','mechanism_purged_family','structure');strict_base=metric('unhinted','mechanism_purged_family','model_prompt')
    positive=main['brier']<base['brier'] and strict['brier']<strict_base['brier']
    lines=['# Prediction pilot: can game structure predict activation?','',
        '**Result: '+('positive retrospective signal under both primary holdouts.' if positive else 'this first structural predictor does not generalize better than the model/prompt baseline.')+'**',
        '',f"On held-out game families, structural Brier is **{main['brier']:.3f}** versus **{base['brier']:.3f}** for the baseline. Holding out a mechanism and every game family containing it gives **{strict['brier']:.3f}** versus **{strict_base['brier']:.3f}**. Lower is better. This is a negative result for the specified features/model, not evidence that the entire research direction is impossible.",
        '', '## What was implemented','',
        f"- {provenance['targets']} eligible exploits, {provenance['editions']} editions, {provenance['families']} base-game families, {provenance['mechanisms']} mechanism types, three seeds; exact frozen revised45 engines.",
        f"- Fixed outcome snapshot at {outcomes['snapshot_time']}: **{main['n']} unhinted trials**, plus **{metric('hinted','family','structure')['n']} hinted trials** analyzed separately. No paid inference calls.",
        '- Fourteen programmatic features: seven game/interface features plus seven canonical-witness features. The interface ablation uses only the first seven.',
        '- Five references/predictors: global rate; player-model/prompt context; taxonomy plus context; interface plus context; full structure plus context.',
        '- Four cross-validation schemes: held-out edition, held-out base-game family, held-out mechanism, and mechanism holdout that also excludes its game families.',
        '- Fixed L2 logistic regression (10), training-fold-only scaling/encoding, no hyperparameter search, out-of-fold probability exports and reusable forecast artifacts.',
        '', '## Prediction performance','', 'Brier is mean squared probability error. Positive Δ below means structure is worse than context-only. Each model/prompt/target/seed is a trial; grouped holdouts prevent treating seeds or model variants of a target as unseen games.',
        '', '| Evaluation | Trials | Context Brier | Structure Brier | Δ Brier | Descriptive family-block interval for Δ |',
        '|---|---:|---:|---:|---:|---|']
    for cohort in ['unhinted','hinted']:
        for scheme in SCHEMES:
            s=metric(cohort,scheme,'structure');b=metric(cohort,scheme,'model_prompt');lo,hi=s['delta_brier_cluster_interval']
            lines.append(f"| {cohort}: {SCHEMES[scheme]} | {s['n']} | {b['brier']:.4f} | {s['brier']:.4f} | {s['delta_brier_vs_context']:+.4f} | [{lo:+.4f}, {hi:+.4f}] |")
    lines+=['','![Unhinted held-out prediction](plots/unhinted_heldout_brier.png)',
            '', '![Hinted held-out prediction](plots/hinted_heldout_brier.png)',
            '', '![Held-out calibration](plots/calibration.png)',
            '', 'Intervals resample ten game-family blocks while holding the fitted out-of-fold forecasts fixed. They do not include feature-selection or model-refitting uncertainty and are not a confirmatory significance test.',
            '', '## Where does it fail?','',
            '| Held-out game family | Unhinted trials | Observed activation | Context forecast | Structure forecast | Context Brier | Structure Brier |',
            '|---|---:|---:|---:|---:|---:|---:|']
    for d in sorted([d for d in diagnostics if d['cohort']=='unhinted'],key=lambda d:d['structure']['brier']-d['model_prompt']['brier'],reverse=True):
        s=d['structure'];b=d['model_prompt'];lines.append(f"| {d['family']} | {s['n']} | {s['observed']:.1%} | {b['predicted']:.1%} | {s['predicted']:.1%} | {b['brier']:.3f} | {s['brier']:.3f} |")
    lines+=['','The family-holdout errors show how far forecasts transfer to a different engine template. Good behavior on a held-out mechanism alone would not establish new-game generalization because other mechanisms from the same game family can remain in training.',
            '', '## Feature definition and what the predictor knows','',
            'Ordinary game features: horizon; player count; number of action panels; numeric fields; unconstrained text fields; enumerated options; initial observation length.',
            '', 'Witness features: supplied canonical-witness length; first activation position relative to horizon; bracketed fields per action; auxiliary-interface use; prefix score cost relative to a normal script; own-score and competitive-advantage contrasts under a single-mechanism patch and scripted continuation.',
            '', 'The witness block assumes designer access to a known planted opportunity. It does not claim to infer the opportunity from player-visible rules. Witness length is not minimum search complexity; scripted payoff contrasts are neither optimal exploit values nor expected values over model policies. Generic features can proxy mechanism or game identity, which is why family-purged evaluation is included.',
            '', 'No target/game/family IDs, seed IDs, taxonomy labels, spec descriptions, raw action token identities, model responses or observed behavioral statistics enter the structural design matrix. Model × prompt context is allowed. Category labels appear only in the explicitly named taxonomy baseline and in split construction.',
            '', '## What this does not establish','',
            '- **Discovery remains unmeasured.** These labels estimate activation, not `P(discovery)` or `P(execute | discovered)`. A hinted attempt is conditioned on an earlier miss and reveals a mechanism; it is not independently verified discovery.',
            '- This is retrospective: aggregate outcomes were already known when the feature design was chosen. Cross-validation is genuine out-of-fold scoring, but the pilot is not a preregistered or prospective prediction test.',
            '- Forty-five opportunities are nested inside ten families. More model/seed repetitions do not create more independent game structures. Failed/incomplete API episodes are omitted and may select the observed sample.',
            '- Models and effort settings vary; known model/prompt identities are controlled only as nuisance predictors. Generalization to a new player model has not been tested.',
            '', '## Recommendation','',
            'Treat this as a working evaluation harness and a first representation that failed this evaluation. Do not scale the current predictor into a headline claim or tune repeatedly against these same held-out folds. The next informative step is to specify richer structural variables without outcome access, add genuinely new game families, freeze probability forecasts, and then collect their behavior. Independent discovery annotation is needed before testing the proposed discovery/execution decomposition.',
            '', '## Artifacts and reproduction','',
            '[Protocol](protocol.json) · [Feature definitions](feature-schema.json) · [135 feature rows and witness evidence](features.json) · [Source provenance](feature-provenance.json) · [Outcome snapshot](outcomes.csv) · [Outcome provenance and missingness](outcome-provenance.json)',
            '', '[All metrics](metrics.json) · [Fold membership audit](folds.json) · [Out-of-fold probabilities](out-of-fold-predictions.csv) · [Per-family diagnostics](family-diagnostics.json) · [Calibration bins](calibration.json)',
            '', '[Fitted unhinted forecasting artifact](final-model-unhinted.json) · [Fitted hinted artifact](final-model-hinted.json). These are fitted on all snapshot data for future use; their training predictions are not performance evidence.',
            '', '```bash',
            'cd /shared/allie/strategy-behavior',
            'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /shared/allie/venvs/hole/bin/python -B benchmark/prediction/run45.py --out benchmark/results/prediction45-pilot-20260910',
            'MPLCONFIGDIR=/shared/allie/home/.codex/tmp/matplotlib /shared/allie/venvs/hole/bin/python -B benchmark/prediction/report45.py --out benchmark/results/prediction45-pilot-20260910',
            '```',
            '', 'Use `benchmark/prediction/forecast45.py --help` to create timestamped forecasts from a saved artifact and structural feature JSON. It rejects unseen player-model/prompt contexts, marks previously trained targets, and refuses to overwrite existing forecasts.']
    body='\n'.join(lines)+'\n';(out/'REPORT.md').write_text(body)
    canonical=Path(__file__).resolve().parents[2]/'research_logs/sep/prediction-pilot-results.md'
    import re,os
    canonical.write_text(re.sub(r'(!?\[[^\]]*\]\()([^\)]+)(\))',lambda m:m[1]+os.path.relpath(out/m[2],canonical.parent)+m[3],body))
    print(canonical)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.out)
