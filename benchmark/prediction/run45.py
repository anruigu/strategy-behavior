"""Retrospective grouped out-of-sample prediction feasibility pilot. No model calls."""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from model45 import METHODS,L2,fit,predict,make_folds,losses

SCHEMES=('edition','family','mechanism','mechanism_purged_family')


def read_dataset(out):
    features=json.loads((out/'features.json').read_text());lookup={(r['target'],r['seed']):r for r in features}
    provenance=json.loads((out/'outcome-provenance.json').read_text())
    assert hashlib.sha256((out/'outcomes.csv').read_bytes()).hexdigest()==provenance['outcomes_sha256']
    fprov=json.loads((out/'feature-provenance.json').read_text())
    assert hashlib.sha256((out/'features.json').read_bytes()).hexdigest()==fprov['features_sha256']
    rows=[];seen=set()
    with (out/'outcomes.csv').open() as f:
        for raw in csv.DictReader(f):
            assert raw['protocol']=='revised45'
            assert raw['executed'] in ('True','False','1','0'),'Unknown outcome label'
            feature=lookup[(raw['target'],int(raw['seed']))]
            ident=(raw['model'],raw['phase'],raw['target'],int(raw['seed']))
            assert ident not in seen;seen.add(ident)
            assert raw['category']==feature['mechanism'] and raw['game']==feature['game']
            rows.append(dict(index=len(rows),model=raw['model'],phase=raw['phase'],target=raw['target'],
                seed=int(raw['seed']),game=feature['game'],family=feature['family'],mechanism=feature['mechanism'],
                features=feature['features'],y=int(raw['executed']=='True' or raw['executed']=='1')))
    return rows


def block_interval(rows,difference):
    # Descriptive uncertainty conditional on these fitted OOF forecasts, not a fresh experiment.
    blocks=sorted({r['family'] for r in rows})
    sums=np.array([sum(d for r,d in zip(rows,difference) if r['family']==b) for b in blocks])
    counts=np.array([sum(r['family']==b for r in rows) for b in blocks])
    rng=np.random.default_rng(450910);draws=rng.integers(0,len(blocks),(2000,len(blocks)))
    vals=sums[draws].sum(axis=1)/counts[draws].sum(axis=1)
    return [float(v) for v in np.quantile(vals,[.025,.975])]


def evaluate(rows,game_features,witness_features,cohort):
    summaries=[];forecasts=[];foldlog=[]
    y=np.array([r['y'] for r in rows])
    for scheme in SCHEMES:
        probabilities={m:np.full(len(rows),np.nan) for m in METHODS}
        for held,train_idx,test_idx in make_folds(rows,scheme):
            train=[rows[i] for i in train_idx];test=[rows[i] for i in test_idx]
            foldlog.append(dict(cohort=cohort,scheme=scheme,held_out=held,train_rows=len(train),test_rows=len(test),
                train_targets=sorted({r['target'] for r in train}),test_targets=sorted({r['target'] for r in test}),
                train_families=sorted({r['family'] for r in train}),test_families=sorted({r['family'] for r in test}),
                test_indices=[r['index'] for r in test],train_indices=[r['index'] for r in train]))
            for method in METHODS:
                artifact=fit(train,method,game_features,witness_features)
                probabilities[method][test_idx]=predict(artifact,test)
        assert all(np.isfinite(p).all() for p in probabilities.values())
        base_loss=losses(y,probabilities['model_prompt'])[0]
        for method,prob in probabilities.items():
            brier,logloss=losses(y,prob);delta=brier-base_loss
            summaries.append(dict(cohort=cohort,scheme=scheme,method=method,n=len(rows),positive=int(y.sum()),
                brier=float(brier.mean()),log_loss=float(logloss.mean()),
                family_macro_brier=float(np.mean([brier[[r['family']==f for r in rows]].mean() for f in sorted({r['family'] for r in rows})])),
                delta_brier_vs_context=float(delta.mean()),delta_brier_cluster_interval=block_interval(rows,delta),
                skill_vs_context=float(1-brier.mean()/base_loss.mean()),
                per_phase={phase:dict(n=sum(r['phase']==phase for r in rows),brier=float(brier[[r['phase']==phase for r in rows]].mean()),
                    context_brier=float(base_loss[[r['phase']==phase for r in rows]].mean())) for phase in sorted({r['phase'] for r in rows})}))
            for row,p in zip(rows,prob):
                forecasts.append({k:row[k] for k in ['index','model','phase','target','game','family','mechanism','seed','y']}|
                    dict(cohort=cohort,scheme=scheme,method=method,probability=float(p)))
        print(cohort,scheme,[(s['method'],round(s['brier'],4)) for s in summaries if s['cohort']==cohort and s['scheme']==scheme],flush=True)
    return summaries,forecasts,foldlog


def run(out):
    schema=json.loads((out/'feature-schema.json').read_text());game=list(schema['game_features']);witness=list(schema['witness_features'])
    # This protocol is saved before loading outcomes or fitting models.
    protocol=dict(created=datetime.now(timezone.utc).isoformat(),purpose='Retrospective feasibility of predicting behavioral activation from game structure.',
        target='Binary engine activation per player model / prompt / exploit / seed; never discovered.',
        features=dict(interface=game,structure=game+witness),methods=list(METHODS),l2=L2,hyperparameter_selection='Fixed, no tuning.',
        cv_schemes=list(SCHEMES),primary_cv='family',stress_test='mechanism_purged_family',
        covariates='Known model × prompt identity is a nuisance context, included for all learned predictors.',
        taxonomy='Taxonomy-only baseline uses category dummies; categories never enter interface or structure predictors.',
        scaling='Numeric means/scales and categorical vocabularies fit on training fold only.',
        grouping='All models, prompts and seeds for a held-out unit stay out of training. Strict mechanism folds also exclude every base-game family represented in test.',
        response_cohorts='Unhinted win_only+exploration primary; hinted diagnostic outcomes modeled separately due to selection on prior misses.',
        metrics='Brier and log loss; paired Brier differences against context-only model. Family-block bootstrap is descriptive and conditional on OOF fits.',
        evidence_rule='Positive feasibility signal if structure beats context Brier on both family holdout and family-purged mechanism holdout; this is exploratory, not a prospective success claim.',
        limitations=['17 editions / 10 families / 16 eligible types, not hundreds of independent games.',
            'The feature design follows observation of aggregate benchmark results; this is not preregistered or prospective.',
            'Canonical witnesses are designer/oracle access; witness features do not measure spontaneous discovery.',
            'Held-out folds use existing games; fresh unseen games and preregistered forecasts remain necessary.',
            'Outcome-complete samples omit API failures and may be selected. No probability of discovery or execution given discovery can be estimated without independent discovery labels.'])
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    rows=read_dataset(out);summaries=[];forecasts=[];folds=[]
    for cohort in ['unhinted','hinted']:
        selected=[r for r in rows if (r['phase']=='hinted')==(cohort=='hinted')]
        s,f,a=evaluate(selected,game,witness,cohort);summaries+=s;forecasts+=f;folds+=a
        final=fit(selected,'structure',game,witness)
        final.update(cohort=cohort,feature_schema=schema,trained_rows=len(selected),known_player_models=sorted({r['model'] for r in selected}),
                     trained_targets=sorted({r['target'] for r in selected}),note='Fit on all snapshot data for future forecasting, not scored as in-sample evidence.')
        (out/f'final-model-{cohort}.json').write_text(json.dumps(final,indent=2)+'\n')
    (out/'metrics.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (out/'folds.json').write_text(json.dumps(folds,indent=2)+'\n')
    with (out/'out-of-fold-predictions.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(forecasts[0]));writer.writeheader();writer.writerows(forecasts)
    result=dict(completed=datetime.now(timezone.utc).isoformat(),rows=len(rows),folds=len(folds),forecast_rows=len(forecasts),
        source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'run.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);a=parser.parse_args();run(a.out)
