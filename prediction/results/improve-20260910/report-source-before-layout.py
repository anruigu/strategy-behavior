"""Render saved improvement-study results and root-owned decisions. No fitting/API calls."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3

TARGETS=('action0','cooperation','coordination')
TARGET_LABELS={'action0':'Canonical action0','cooperation':'Mutual cooperation','coordination':'Coordination'}
SPLITS=('family','interpolation','extrapolation','development','fresh_full','fresh_family_excluded')
SPLIT_LABELS={'family':'Leave one family out','interpolation':'Within-family interpolation',
 'extrapolation':'Within-family extrapolation','development':'Old21 development',
 'fresh_full':'Fresh: full training','fresh_family_excluded':'Fresh: family excluded'}
METHODS=('context','family','nash','payoff_dominant','calibrated_payoff_dominant',
         'normalized_logistic','combined_logistic','qwen3_frozen_head','qwen3_lora_head','llm_few_shot')
LABELS={'context':'Ordered context','family':'Family mean','nash':'Original Nash',
 'payoff_dominant':'Payoff-dominant theory','calibrated_payoff_dominant':'Calibrated theory',
 'normalized_logistic':'Normalized logistic','combined_logistic':'Combined logistic',
 'qwen3_frozen_head':'Qwen frozen head','qwen3_lora_head':'Qwen LoRA head','llm_few_shot':'Kimi few-shot'}
COLORS={'context':'#87929a','family':'#6d7781','nash':'#a6adb3','payoff_dominant':'#577b6b',
 'calibrated_payoff_dominant':'#00856a','normalized_logistic':'#738b9f','combined_logistic':'#405d78',
 'qwen3_frozen_head':'#2166ac','qwen3_lora_head':'#ca5a20','llm_few_shot':'#8757a1'}


def stamp():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def number(value):return f'{value:.4f}' if isinstance(value,(int,float)) and math.isfinite(value) else '—'
def escape(text):return str(text).replace('|','\\|').replace('\n',' ')
def link(label,path,output):return f'[{label}]({os.path.relpath(Path(path).resolve(),Path(output).resolve().parent)})'


class Reader:
    def __init__(self):self.hashes={}
    def read(self,path,optional=True):
        path=Path(path)
        if not path.exists() and optional:return None
        raw=path.read_bytes();self.hashes[str(path.resolve())]=hashlib.sha256(raw).hexdigest()
        return json.loads(raw)


def load_evaluation(path,reader):
    path=Path(path)
    if not (path/'scores.json').exists():return None
    summary=reader.read(path/'scores.json',False)
    comparisons=reader.read(path/'paired-comparisons.json',False)
    audit=reader.read(path/'audit.json',False)
    if audit.get('status')!='verified':raise ValueError('Scores lack verified evaluator audit: '+str(path))
    expected=audit.get('output_sha256',{})
    for name in ('scores.json','paired-comparisons.json','group-level.jsonl'):
        actual=path/name
        # Fleet may mount the identical allie subtree as /mnt/sfs/allie.
        matches=[value for source,value in expected.items() if
                 str(Path(source)).replace('/mnt/sfs/allie/','/shared/allie/')==str(actual.resolve())]
        if len(matches)!=1 or sha(actual)!=matches[0]:
            raise ValueError('Saved evaluation output hash mismatch: '+str(actual))
        reader.hashes[str(actual.resolve())]=matches[0]
    return dict(path=path,summary=summary,comparisons=comparisons)


def support_for(summary,split,target):
    cells={c['support']:c for c in summary.get('coverage',[]) if c['split']==split and c['target']==target}
    if cells.get('all_methods',{}).get('common_examples',0)>0:return 'all_methods'
    return 'numerical_only'


def score_cell(evaluation,split,target,method,support=None):
    if evaluation is None:return None
    summary=evaluation['summary'];support=support or support_for(summary,split,target)
    matches=[r for r in summary['scores'] if r.get('family')=='all' and r['split']==split and
             r['target']==target and r['method']==method and r['support']==support]
    if len(matches)>1:raise ValueError('Duplicate score cell')
    return matches[0] if matches else None


def decision_text(root,reader,output):
    for name in ('final-disposition.json','development-gate.json'):
        value=reader.read(root/name)
        if value is not None:
            status=value.get('decision',value.get('status','Decision recorded'))
            if not isinstance(status,str):status=json.dumps(status,ensure_ascii=False)
            explanation=next((value[k] for k in ('summary','conclusion','reason','message') if isinstance(value.get(k),str)),'')
            return f'**Decision: {escape(status)}.** {escape(explanation)} '+link('Decision record',root/name,output)+'.'
    return '**Decision pending.** No development or final decision has been saved. This report does not infer success from score point estimates.'


def runtime_rows(root,reader):
    jobs={}
    folder=root/'fleet-runtime'
    # Read only allowlisted metadata; never expose submitted environments or credentials.
    for path in sorted(folder.glob('*submit*.json')):
        if path.name.endswith('.intent.json'):continue
        saved=reader.read(path);response=saved.get('response',{}) if isinstance(saved,dict) else {}
        name=response.get('name')
        if isinstance(name,str):jobs[name]=dict(name=name,status='submitted',submitted=saved.get('recorded_at'),source=path)
    history=reader.read(folder/'own-run-history.json') or {}
    for item in history.get('items',[]):
        if item.get('name') in jobs:jobs[item['name']]['status']=item.get('status','unknown')
    events=[]
    for pattern in ('*/latest.json','*/completion.json','*status*.json'):
        for path in folder.glob(pattern):
            saved=reader.read(path)
            event=saved.get('response',saved)
            if event.get('name') in jobs:
                events.append((saved.get('recorded_at',''),path,event))
    for observed,path,event in sorted(events,key=lambda x:x[0]):
        item=jobs[event['name']];item.update(status=event.get('status','unknown'),observed=observed,source=path)
    # Cancellation success is a recorded terminal action even if the live run was reaped.
    for path in folder.glob('*/cancellation-result.json'):
        result=reader.read(path);intent=reader.read(path.with_name('cancellation-intent.json')) or {}
        name=intent.get('name')
        if name in jobs:
            jobs[name].update(status='cancelled / cancellation acknowledged',observed=result.get('recorded_at'),source=path)
    worker=reader.read(folder/'training-status.json')
    if isinstance(worker,dict) and worker.get('fleet_run_id') in jobs:
        item=jobs[worker['fleet_run_id']]
        item['worker_status']=worker.get('status')
        item['worker_started']=worker.get('started_utc')
        item['worker_finished']=worker.get('finished_utc')
    for item in jobs.values():
        try:item['observed_wall_minutes']=(datetime.fromisoformat(item['observed'])-datetime.fromisoformat(item['submitted'])).total_seconds()/60
        except (KeyError,TypeError,ValueError):item['observed_wall_minutes']=None
        try:item['worker_minutes']=(datetime.fromisoformat(item['worker_finished'])-datetime.fromisoformat(item['worker_started'])).total_seconds()/60
        except (KeyError,TypeError,ValueError):item['worker_minutes']=None
    return sorted(jobs.values(),key=lambda x:x.get('submitted') or '')


def ledger_snapshot(path):
    path=Path(path)
    if not path.is_file():return None
    db=sqlite3.connect(str(path),timeout=10)
    try:
        db.execute('PRAGMA query_only=ON');db.execute('BEGIN')
        ceiling=db.execute('SELECT ceiling FROM settings').fetchone()[0]
        count,reported,committed=db.execute('SELECT COUNT(*),COALESCE(SUM(charged),0),COALESCE(SUM(COALESCE(charged,reserved)),0) FROM calls').fetchone()
        return dict(observed_utc=stamp(),ceiling_usd=ceiling,calls=count,reported_usd=reported,committed_usd=committed)
    finally:db.close()


def render_figures(evaluations,folder):
    os.environ.setdefault('MPLCONFIGDIR','/shared/allie/home/.codex/tmp/matplotlib-prediction-improve')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import MaxNLocator
    plt.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':9,'svg.fonttype':'none',
                         'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
    splits=[s for s in SPLITS if s in evaluations]
    if not splits:return []
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    artifacts=[]
    def save(fig,name,title):
        fig.suptitle(title,fontsize=13)
        fig.tight_layout(rect=(0,0,1,.94))
        paths={}
        for ext in ('png','svg','pdf'):
            path=folder/(name+'.'+ext);fig.savefig(path,dpi=220,bbox_inches='tight');paths[ext]=path
        plt.close(fig);artifacts.append(dict(name=name,title=title,paths=paths))
    for metric,title in [('event_brier','Event Brier score — lower is better'),('log_loss','Event log loss — lower is better')]:
        fig,axes=plt.subplots(3,len(splits),figsize=(max(6,3.3*len(splits)),10),squeeze=False)
        for column,split in enumerate(splits):
            for row,target in enumerate(TARGETS):
                ax=axes[row,column]
                plotted=[]
                for index,method in enumerate(METHODS):
                    cell=score_cell(evaluations[split],split,target,method)
                    if cell and cell.get(metric) is not None:
                        ax.plot(cell[metric],index,'o',color=COLORS[method],markersize=5)
                        plotted.append(cell[metric])
                ax.set_yticks(range(len(METHODS)),[LABELS[m] for m in METHODS] if column==0 else ['']*len(METHODS))
                ax.set_ylim(len(METHODS)-.5,-.5);ax.set_xlim(0,max(.05,max(plotted,default=0)*1.12))
                ax.xaxis.set_major_locator(MaxNLocator(nbins=4));ax.grid(axis='x',alpha=.18)
                if row==0:ax.set_title(SPLIT_LABELS[split])
                if column==0:ax.set_ylabel(TARGET_LABELS[target])
                ax.set_xlabel('Brier' if metric=='event_brier' else 'Log loss')
        save(fig,'scores-'+metric,title+'\nFixed candidates; shared support within each target/panel; missing results omitted')
    selected=[s for s in ('family','development','fresh_full','fresh_family_excluded') if s in evaluations]
    calibration_methods=('family','calibrated_payoff_dominant','combined_logistic','qwen3_frozen_head','qwen3_lora_head','llm_few_shot')
    if selected:
        fig,axes=plt.subplots(3,len(selected),figsize=(max(6,3.2*len(selected)),9),squeeze=False)
        for c,split in enumerate(selected):
            for r,target in enumerate(TARGETS):
                ax=axes[r,c];ax.plot([0,1],[0,1],color='#999999',linestyle='--',linewidth=.8)
                for method in calibration_methods:
                    score=score_cell(evaluations[split],split,target,method)
                    bins=score.get('calibration_bins',[]) if score else []
                    points=[b for b in bins if b.get('weight',0)>0]
                    if points:ax.plot([b['mean_prediction'] for b in points],[b['mean_observed'] for b in points],
                                      '-o',color=COLORS[method],linewidth=1,markersize=3,alpha=.8)
                ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_aspect('equal',adjustable='box')
                if r==0:ax.set_title(SPLIT_LABELS[split])
                ax.set_xlabel('Predicted probability')
                if c==0:ax.set_ylabel(TARGET_LABELS[target]+'\nObserved event rate')
        fig.legend([Line2D([],[],color=COLORS[m],marker='o',markersize=3) for m in calibration_methods],
                   [LABELS[m] for m in calibration_methods],loc='lower center',ncol=3,bbox_to_anchor=(.5,-.025),frameon=False)
        save(fig,'calibration','Calibration on shared support\nFixed bins; curves summarize probabilities, not individual trajectories')
    fig,axes=plt.subplots(3,len(splits),figsize=(max(6,3.3*len(splits)),8),squeeze=False)
    for c,split in enumerate(splits):
        for r,target in enumerate(TARGETS):
            ax=axes[r,c];ax.axvline(0,color='#555555',linewidth=.8)
            ax.axvline(.005,color='#bbbbbb',linestyle=':',linewidth=.8)
            support=support_for(evaluations[split]['summary'],split,target)
            for index,method in enumerate(('qwen3_frozen_head','qwen3_lora_head')):
                rows=[v for v in evaluations[split]['comparisons'] if v['split']==split and v['target']==target
                      and v.get('family')=='all' and v['support']==support and v['method']==method
                      and v['baseline']=='calibrated_payoff_dominant']
                if len(rows)>1:raise ValueError('Duplicate paired contrast')
                if not rows:continue
                value=rows[0]
                for key,offset,style in [('game_bootstrap',-.1,'-'),('seven_family_cluster_sensitivity',.1,'--')]:
                    cell=value.get(key,{}).get('intervals',{}).get('event_brier')
                    if cell is None:continue
                    y=index+offset;ax.plot([cell['lower'],cell['upper']],[y,y],style,color=COLORS[method],linewidth=1.5)
                    ax.plot(cell['improvement'],y,'o',color=COLORS[method],markersize=4)
            ax.set_yticks([0,1],['Frozen','LoRA'] if c==0 else ['','']);ax.set_ylim(1.5,-.5)
            ax.set_xlabel('Theory − transformer Brier');ax.grid(axis='x',alpha=.15)
            if r==0:ax.set_title(SPLIT_LABELS[split])
            if c==0:ax.set_ylabel(TARGET_LABELS[target])
    save(fig,'paired-gains','Paired improvement over training-calibrated theory\nPositive favors transformer; solid: game 95% interval; dashed: seven-family sensitivity; dotted reference: 0.005')
    return artifacts


def score_table(evaluation,split,support=None):
    lines=['| Candidate | Action Brier / log loss | Cooperation Brier / log loss | Coordination Brier / log loss |',
           '|---|---:|---:|---:|']
    for method in METHODS:
        cells=[]
        for target in TARGETS:
            score=score_cell(evaluation,split,target,method,support)
            cells.append(number(score.get('event_brier'))+' / '+number(score.get('log_loss')) if score else '—')
        lines.append('| '+LABELS[method]+' | '+' | '.join(cells)+' |')
    return lines


def render(run_root,output,development_eval=None,fresh_eval=None,figures=None):
    root=Path(run_root).resolve();output=Path(output).resolve();reader=Reader()
    development=Path(development_eval) if development_eval else root/'development-evaluation'
    fresh=Path(fresh_eval) if fresh_eval else root/'fresh-evaluation'
    loaded=[v for v in (load_evaluation(development,reader),load_evaluation(fresh,reader)) if v]
    evaluations={}
    for evaluation in loaded:
        for split in {r['split'] for r in evaluation['summary']['scores']}:
            if split in evaluations:raise ValueError('Split appears in multiple evaluation directories')
            evaluations[split]=evaluation
    decision=decision_text(root,reader,output)
    provenance=reader.read(root/'data/provenance.json') or {}
    policy=reader.read(root/'budget-policy.json') or {}
    model=reader.read(root/'model/manifest.json') or {}
    transform=reader.read(root/'transformer-protocol.json') or {}
    jobs=runtime_rows(root,reader)
    budget_error=None
    try:budget=ledger_snapshot(policy.get('stage_ledger',root/'eval-budget.sqlite'))
    except (sqlite3.Error,OSError) as exc:budget=None;budget_error=type(exc).__name__
    artifacts=render_figures(evaluations,figures or root/'report-figures')
    lines=['# Transformer representations for repeated-game prediction','',decision,'',
        'This follow-up compares frozen and LoRA-adapted Qwen probability heads with empirical means, numerical predictors, training-calibrated equilibrium selection, and few-shot prompting. The comparison concerns forecasts before play, not training the game-playing agents.','',
        '## Study and current coverage','',
        'Four players—Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B, and GPT-OSS-20B—play eight simultaneous rounds with public history and an own-points objective. The fixed training snapshot has 72 shapes and 1,918 completed matches. The previously inspected 21-shape cohort is development evidence; it is not a fresh confirmatory test. Fresh evaluation, if completed, uses 28 new shapes (four per existing family) and 560 planned matches. Full-training and family-excluded forecasts answer different questions.','',
        '| Condition | Saved evaluation |','|---|---|']
    for split in SPLITS:
        lines.append('| '+SPLIT_LABELS[split]+' | '+(link('Available',evaluations[split]['path']/'scores.json',output) if split in evaluations else 'Not yet available / unrun')+' |')
    lines += ['', 'Kimi few-shot is not run on the retrospective family/interpolation/extrapolation folds. All-method scores use common support across methods available in that split; numerical-only support retains all seven numerical baselines plus both Qwen heads. A missing result is not a zero score.']
    if not evaluations:lines += ['', '**No comparative results are available yet.** Model/code preparation or an API submission does not establish successful training or improved prediction.']
    for split in SPLITS:
        if split not in evaluations:continue
        evaluation=evaluations[split]
        lines += ['', '## '+SPLIT_LABELS[split], '', 'Scores are Brier / log loss; lower is better. No candidate is designated the winner from these point estimates.', '']
        lines += score_table(evaluation,split)
        supports=[];different=False
        for target in TARGETS:
            selected=support_for(evaluation['summary'],split,target)
            cover=[c for c in evaluation['summary'].get('coverage',[]) if c['split']==split and c['target']==target]
            current=next((c for c in cover if c['support']==selected),{})
            supports.append(f"{TARGET_LABELS[target]}: {current.get('common_games',0)} games, {current.get('common_examples',0)} contexts ({selected})")
            counts={c.get('common_examples') for c in cover}
            different |= len(counts)>1
        lines += ['', '; '.join(supports)+'.']
        if different:
            lines += ['', 'Prompted forecast availability changes common support. The nonprompted comparison is also retained:', '']
            lines += score_table(evaluation,split,'numerical_only')
        lines += ['',link('Paired intervals and family sensitivity',evaluation['path']/'paired-comparisons.json',output)+'; '+link('Per-family scores, calibration, and opportunity counts',evaluation['path']/'scores.json',output)+'.']
    if artifacts:
        lines += ['', '## Figures', '']
        for item in artifacts:
            lines += [f"![{item['title'].split(chr(10))[0]}]({os.path.relpath(item['paths']['png'],output.parent)})",'',
                      link('SVG',item['paths']['svg'],output)+' · '+link('PDF',item['paths']['pdf'],output),'']
    lines += ['', '## Interpretation limits','',
        'The central comparison is structural family transfer against strong calibrated-theory and empirical baselines. Calibration explicitly gives generic softening of extreme equilibrium probabilities a chance to explain log-loss gains. A favorable point estimate or an interval crossing zero is not, by itself, evidence of improvement or absence of signal. The 0.005 Brier reference is not a multiplicity-adjusted significance threshold.','',
        'Training uses one fixed optimization seed. The 500-draw game bootstrap conditions on the fitted forecasts and preserves each game’s observed episodes and both focal roles; it does not refit models or separately resample episodes within games. Seven-family cluster intervals are a sensitivity analysis with only seven declared clusters, and some targets have fewer eligible families. These intervals do not quantify unrestricted training uncertainty or transfer across a population of unseen strategic families.','',
        'Brier/log loss and calibration use equal canonical-game event weights. Cooperation and coordination have structural masks; rate MSE concerns aggregated game/ordered-context rates. Retaliation, forgiveness, and exploitation are outside the primary improvement claim. See '+link('scoring definitions',Path(__file__).with_name('evaluation.md'),output)+'.','',
        '## Training and inference resources','',
        'All empirical baseline means, calibration, preprocessing, heads, and LoRA fitting must run through Fleet Training API jobs. Local work prepares data, applies saved forecasts, scores, and renders. Runtime observations below distinguish job wall time from actual allocated GPU time. Startup and queue time count conservatively toward the six-hour operational limit; they are not measured GPU compute.','',
        '| Fleet job | Latest saved state | Observed wall minutes | Completed worker minutes | Evidence |',
        '|---|---|---:|---:|---|']
    for job in jobs:
        lines.append('| '+escape(job['name'])+' | '+escape(job.get('worker_status',job['status']))+' | '+number(job['observed_wall_minutes'])+' | '+number(job['worker_minutes'])+' | '+link('Record',job['source'],output)+' |')
    if not jobs:lines.append('| — | No returned job names recorded | — | — | — |')
    lines += ['', 'The training service does not expose a dollar price here; no GPU-dollar cost is invented. Job wall-time observations include scheduling/startup and are not a GPU-hour bill.']
    if budget:
        lines += ['',f"The shared new-inference ledger records {budget['calls']:,} calls, ${budget['reported_usd']:.4f} reported and ${budget['committed_usd']:.4f} committed, against its ${budget['ceiling_usd']:.0f} cap. Unknown charges remain reserved. Hosted FLT zero-dollar entries are not zero compute."]
    else:lines += ['', 'The shared new-inference cap is $150. '+('A current ledger snapshot is unavailable ('+budget_error+').' if budget_error else 'No readable inference ledger snapshot is available yet.')]
    prior=policy.get('prior_committed_usd')
    if prior is not None:lines += ['',f"The authorization ledger additionally carries the earlier study’s ${prior:.4f} commitment within the existing $3,000 ceiling. The $150 shared cap is stricter than the initial $200 stage allowance."]
    lines += ['', '## Provenance','']
    for label,path in [('Improvement plan',root.parents[2]/'research_logs/sep/0910-prediction-improve.md'),
                       ('Data and fold provenance',root/'data/provenance.json'),('Training source freeze',root/'training-freeze.json'),
                       ('Transformer protocol',root/'transformer-protocol.json'),('Baseline protocol',root/'baseline-protocol.json'),
                       ('Model revision manifest',root/'model/manifest.json'),('Fresh design audit',root/'prospective-design/audit.json'),
                       ('Budget policy',root/'budget-policy.json'),('Fresh collection/chronology audit',root/'fresh-collected/audit.json')]:
        if path.exists():lines.append('- '+link(label,path,output))
    lines += ['', 'Report generated '+stamp()+'. Saved decisions remain authoritative; pending or unrun conditions are not treated as completed experiments.','']
    # Immutable numerical outputs must still equal the bytes used above. Job and
    # ledger observations are explicitly point-in-time snapshots of live state.
    for evaluation in loaded:
        for name in ('scores.json','paired-comparisons.json','audit.json','group-level.jsonl'):
            path=(evaluation['path']/name).resolve()
            if sha(path)!=reader.hashes[str(path)]:raise ValueError('Evaluation changed during rendering')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text('\n'.join(lines))
    artifact_dir=Path(figures) if figures else root/'report-figures';artifact_dir.mkdir(parents=True,exist_ok=True)
    manifest=dict(created_utc=stamp(),report=str(output),report_sha256=sha(output),input_observation_sha256=reader.hashes,
        inference_ledger_snapshot=budget,figure_sha256={str(p.resolve()):sha(p) for item in artifacts for p in item['paths'].values()},
        fitting_performed=False,decision_inferred_from_scores=False,
        note='Generated presentation artifacts may be refreshed. Numerical source outputs were rechecked; operational status and ledger entries are timed read-only snapshots.')
    (artifact_dir/'report-artifacts.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
    return dict(report=str(output),figures=len(artifacts),evaluation_splits=sorted(evaluations),decision=decision)


def main():
    p=argparse.ArgumentParser();p.add_argument('--run-root',required=True);p.add_argument('--out',required=True)
    p.add_argument('--development-eval');p.add_argument('--fresh-eval');p.add_argument('--figures')
    a=p.parse_args();print(json.dumps(render(a.run_root,a.out,a.development_eval,a.fresh_eval,a.figures)))


if __name__=='__main__':main()
