"""Score saved forecasts only; no fitting, checkpoint loading, or API clients."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path

from prediction.improve.data import TARGETS,FAMILIES,file_hash,write_new
from prediction.improve.baselines import METHODS as NUMERICAL_METHODS

SEED = 20260910
BOOTSTRAP = 500
TRANSFORMERS = ('qwen3_frozen_head','qwen3_lora_head')
BASELINES = ('calibrated_payoff_dominant','payoff_dominant','family','combined_logistic','normalized_logistic','llm_few_shot')
METRICS = ('event_brier','log_loss','rate_mse','calibration_ece')


def row_key(row):
    return row['split'],row['fold_id'],row['row_id'],row['target']


def expected_rows(data,folds):
    expected = {}
    for fold in folds:
        training = [data['train_examples'][i] for i in fold['train']]
        dataset = data['train_examples'] if fold['test_dataset']=='train' else data['development_examples']
        tests = [dataset[i] for i in fold['test']]
        if [r['row_id'] for r in training] != fold['train_row_ids'] or [r['row_id'] for r in tests] != fold['test_row_ids']:
            raise ValueError('Fold index/ID disagreement')
        if {r['group_id'] for r in training}&{r['group_id'] for r in tests}:
            raise ValueError('Canonical group straddles fold')
        for row in tests:
            for target in TARGETS:
                key = fold['split'],fold['fold_id'],row['row_id'],target
                if key in expected:
                    raise ValueError('Duplicate planned evaluation query')
                cell = row['targets'][target]
                n,k,value = cell['opportunities'],cell['successes'],cell['value']
                if type(n) is not int or n < 0:
                    raise ValueError('Invalid target opportunity count')
                if n and (type(k) is not int or not 0 <= k <= n or type(value) not in (int,float)
                          or not math.isfinite(value) or abs(value-k/n)>1e-8):
                    raise ValueError('Invalid observed rate/counts')
                if not n and (value is not None or k not in (None,0)):
                    raise ValueError('Missing target is incorrectly encoded as an observation')
                expected[key] = row
    return expected


def join_forecasts(data,folds,forecasts,allow_incomplete=False):
    expected = expected_rows(data,folds)
    seen = {}
    available = defaultdict(set)
    for row in forecasts:
        if row.get('target') not in TARGETS:
            raise ValueError('Unknown primary target')
        method = row.get('method')
        if not isinstance(method,str) or not method:
            raise ValueError('Missing method identifier')
        key = row_key(row)
        if key not in expected:
            raise ValueError('Unplanned forecast query: '+str(key))
        if (method,key) in seen:
            raise ValueError('Duplicate forecast, including an identical duplicate')
        actual = expected[key]
        for field in ('game_id','group_id','model','opponent'):
            if row.get(field) != actual[field]:
                raise ValueError('Forecast metadata mismatch: '+field)
        if 'family' in row and row['family'] != actual['family']:
            raise ValueError('Forecast family mismatch')
        if 'prediction' not in row:
            raise ValueError('Prediction key omitted; missing forecasts must be explicit nulls')
        p = row['prediction']
        if p is not None and (type(p) not in (int,float) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError('Forecast is not a finite probability')
        target = row['target']
        if actual['targets'][target].get('applicable') is not True and p is not None:
            raise ValueError('Structurally undefined target must have a null forecast')
        seen[method,key] = dict(row,successes=actual['targets'][target]['successes'],
            opportunities=actual['targets'][target]['opportunities'],value=actual['targets'][target]['value'],
            family=actual['family'],episode_ids=actual.get('episode_ids',[]))
        available[method].add((key[0],key[1]))
    if not seen:
        raise ValueError('No forecasts')
    missing = []
    for method,scopes in available.items():
        for key in expected:
            if key[0] in {scope[0] for scope in scopes} and (method,key) not in seen:
                missing.append(dict(method=method,split=key[0],fold_id=key[1],row_id=key[2],target=key[3]))
    if missing and not allow_incomplete:
        raise ValueError(f'Missing {len(missing)} declared-scope forecasts; explicit incomplete override required')
    return expected,seen,dict(omitted_forecasts=missing,
        method_declared_scopes={m:[list(x) for x in sorted(s)] for m,s in available.items()},
        incomplete_override=bool(allow_incomplete))


def group_rows(rows):
    """Sufficient statistics preserve exact equal-game event scoring."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['group_id']].append(row)
    output = []
    for group,items in sorted(grouped.items()):
        n = sum(row['opportunities'] for row in items)
        if n <= 0:
            raise ValueError('Group has no scoring opportunities')
        families = {row['family'] for row in items}
        if len(families) != 1:
            raise ValueError('Group has inconsistent family')
        value = dict(group_id=group,family=next(iter(families)),examples=len(items),
            opportunities=n,successes=sum(row['successes'] for row in items),
            episodes=len({e for row in items for e in row.get('episode_ids',[])}),
            event_brier=0.0,log_loss=0.0,rate_mse=0.0,mean_prediction=0.0,mean_observed=0.0,
            bin_weight=[0.0]*10,bin_prediction=[0.0]*10,bin_observed=[0.0]*10)
        for row in items:
            p,y = row['prediction'],row['value']
            w = row['opportunities']/n
            clipped = min(1-1e-7,max(1e-7,p))
            value['event_brier'] += w*(p*p-2*p*y+y)
            value['log_loss'] += w*(-y*math.log(clipped)-(1-y)*math.log1p(-clipped))
            value['rate_mse'] += w*(p-y)**2
            value['mean_prediction'] += w*p
            value['mean_observed'] += w*y
            index = min(9,int(p*10))
            value['bin_weight'][index] += w
            value['bin_prediction'][index] += w*p
            value['bin_observed'][index] += w*y
        output.append(value)
    return output


def summarize(groups):
    if not groups:
        return dict(status='no_common_support',games=0)
    n = len(groups)
    result = {key:sum(g[key] for g in groups)/n for key in
              ('event_brier','log_loss','rate_mse','mean_prediction','mean_observed')}
    bins = []
    ece = 0.0
    for b in range(10):
        weight = sum(g['bin_weight'][b] for g in groups)/n
        predicted = sum(g['bin_prediction'][b] for g in groups)/n
        observed = sum(g['bin_observed'][b] for g in groups)/n
        ece += abs(predicted-observed)
        bins.append(dict(bin=b,weight=weight,mean_prediction=predicted/weight if weight else None,
                         mean_observed=observed/weight if weight else None))
    result.update(status='complete',calibration_ece=ece,calibration_bins=bins,games=n,
        eligible_families=len({g['family'] for g in groups}),examples=sum(g['examples'] for g in groups),
        opportunities=sum(g['opportunities'] for g in groups),episodes=sum(g['episodes'] for g in groups))
    return result


def bootstrap_contrast(baseline,method,repetitions=BOOTSTRAP,seed=SEED,cluster='game'):
    import numpy as np
    if repetitions < 2:
        raise ValueError('At least two bootstrap repetitions required')
    if [g['group_id'] for g in baseline] != [g['group_id'] for g in method]:
        raise ValueError('Paired contrast group support differs')
    if not baseline:
        return dict(status='no_common_support')
    n = len(baseline)
    rng = np.random.default_rng(seed)
    if cluster=='game':
        counts = rng.multinomial(n,np.full(n,1/n),size=repetitions).astype(float)
        clusters = n
    elif cluster=='family':
        family_counts = rng.multinomial(7,np.full(7,1/7),size=repetitions)
        counts = np.asarray([[draw[FAMILIES.index(g['family'])] for g in baseline] for draw in family_counts],dtype=float)
        clusters = 7
    else:
        raise ValueError('Unknown cluster axis')
    denominators = counts.sum(axis=1)
    counts = counts[denominators>0];denominators=denominators[denominators>0]
    samples = {}
    for metric in ('event_brier','log_loss','rate_mse'):
        delta=np.asarray([a[metric]-b[metric] for a,b in zip(baseline,method)])
        samples[metric]=(counts@delta)/denominators
    def ece(groups):
        pred=np.asarray([g['bin_prediction'] for g in groups])
        obs=np.asarray([g['bin_observed'] for g in groups])
        return np.abs(counts@(pred-obs)).sum(axis=1)/denominators
    samples['calibration_ece']=ece(baseline)-ece(method)
    point_a,point_b=summarize(baseline),summarize(method)
    intervals = {metric:dict(improvement=point_a[metric]-point_b[metric],
        lower=float(np.quantile(values,.025)),upper=float(np.quantile(values,.975))) for metric,values in samples.items()}
    return dict(status='complete',cluster=cluster,declared_clusters=clusters,
        eligible_family_clusters=len({g['family'] for g in baseline}),repetitions_requested=repetitions,
        repetitions_with_target_support=len(denominators),seed=seed,intervals=intervals,
        direction='baseline minus method; positive favors method',
        limitation='Descriptive conditional-on-fitted-predictors bootstrap, no multiplicity adjustment or refitting. Family-cluster sensitivity has only seven declared clusters; structurally unsupported draws are excluded.' if cluster=='family' else
                   'Resamples whole canonical games; all observed episodes and both focal roles stay together. No model refitting or separate within-game episode resampling.')


def evaluate(data,folds,forecasts,repetitions=BOOTSTRAP,seed=SEED,allow_incomplete=False):
    expected,joined,audit = join_forecasts(data,folds,forecasts,allow_incomplete)
    splits = sorted({key[0] for key in expected})
    scores,coverage,groups_export,contrasts = [],[],[],[]
    for split in splits:
        for target in TARGETS:
            planned = {k for k,r in expected.items() if k[0]==split and k[3]==target and r['targets'][target]['opportunities']>0}
            methods = sorted({method for method,key in joined if key[0]==split and key[3]==target})
            for support_name,selected in [('numerical_only',[m for m in methods if m in (*NUMERICAL_METHODS,*TRANSFORMERS)]),('all_methods',methods)]:
                if not selected:
                    continue
                present = {m:{k for method,k in joined if method==m and k in planned and joined[method,k]['prediction'] is not None} for m in selected}
                common = set.intersection(*(present[m] for m in selected))
                families = sorted({expected[k]['family'] for k in common})
                coverage.append(dict(support=support_name,split=split,target=target,methods=selected,
                    planned_eligible_examples=len(planned),common_examples=len(common),
                    common_games=len({expected[k]['group_id'] for k in common}),
                    methods_available={m:len(present[m]) for m in selected},
                    omitted_or_null_by_method={m:len(planned-present[m]) for m in selected}))
                for family in ['all']+families:
                    keys = sorted(k for k in common if family=='all' or expected[k]['family']==family)
                    grouped = {}
                    for method in selected:
                        rows = [joined[method,k] for k in keys]
                        group_values = group_rows(rows)
                        grouped[method] = group_values
                        meta = dict(support=support_name,split=split,target=target,family=family,method=method)
                        scores.append(dict(meta,**summarize(group_values)))
                        if family=='all':
                            groups_export.extend(dict(meta,**g) for g in group_values)
                    pairs = [(base,method) for method in TRANSFORMERS if method in selected for base in BASELINES if base in selected]
                    if all(m in selected for m in TRANSFORMERS):
                        pairs.append((TRANSFORMERS[0],TRANSFORMERS[1]))
                    for base,method in pairs:
                        comparison = dict(support=support_name,split=split,target=target,family=family,
                            baseline=base,method=method,
                            game_bootstrap=bootstrap_contrast(grouped[base],grouped[method],repetitions,seed))
                        if split in ('family','fresh_family_excluded') and family=='all':
                            comparison['seven_family_cluster_sensitivity']=bootstrap_contrast(
                                grouped[base],grouped[method],repetitions,seed,cluster='family')
                        contrasts.append(comparison)
    return dict(schema_version='improve-scores-v1',scores=scores,coverage=coverage,
        available_methods_by_split={split:sorted({m for m,k in joined if k[0]==split}) for split in splits},
        numerical_only_method_set=list(NUMERICAL_METHODS)+list(TRANSFORMERS),
        prompted_baseline_scope='Kimi few-shot is reused only where its saved forecasts exist: old21 development and later fresh settings. It was not run on retrospective family/interpolation/extrapolation folds; absent methods are not invented or included in their common-support intersection.',
        primary_targets=list(TARGETS),primary_split='family',
        weighting='Each supported canonical game gets equal mass; within game contexts are weighted by target opportunities. All-method and numerical-only supports reported separately.',
        rate_mse_estimand='Squared error against aggregated game/ordered-context rates, with event weights; not trajectory-level squared error.',
        calibration='Ten fixed equal-width probability bins; game-equal event weights; 1 belongs to last bin.',
        log_loss_clip=1e-7,bootstrap_repetitions=repetitions,seed=seed), contrasts,groups_export,audit


def score_files(data_path,folds_path,forecast_paths,out,repetitions=BOOTSTRAP,allow_incomplete=False):
    code_paths = [Path(__file__),Path(__file__).with_name('data.py'),Path(__file__).with_name('baselines.py'),
                  Path(__file__).resolve().parents[1]/'games.py']
    paths = [Path(data_path),Path(folds_path)]+[Path(p) for p in forecast_paths]+code_paths
    inputs = {str(p.resolve()):file_hash(p) for p in paths}
    data=json.loads(Path(data_path).read_text());folds=json.loads(Path(folds_path).read_text())
    forecasts=[]
    for p in forecast_paths:
        forecasts.extend(json.loads(line) for line in Path(p).read_text().splitlines() if line.strip())
    result,contrasts,groups,audit = evaluate(data,folds,forecasts,repetitions,allow_incomplete=allow_incomplete)
    for path,expected in inputs.items():
        if file_hash(path)!=expected:raise ValueError('Input changed during scoring')
    out=Path(out)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Preserve existing evaluation')
    out.mkdir(parents=True,exist_ok=True)
    write_new(out/'scores.json',result)
    write_new(out/'paired-comparisons.json',contrasts)
    with (out/'group-level.jsonl').open('x') as handle:
        for row in groups:handle.write(json.dumps(row,allow_nan=False)+'\n')
    write_new(out/'audit.json',dict(status='verified',created_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=inputs,source_code_sha256={str(p.resolve()):inputs[str(p.resolve())] for p in code_paths},
        output_sha256={str((out/name).resolve()):file_hash(out/name) for name in ('scores.json','paired-comparisons.json','group-level.jsonl')},
        forecast_rows=len(forecasts),fitting_performed=False,bootstrap_unit='canonical game; entire episodes/focal roles retained',
        **audit))
    return dict(scores=len(result['scores']),contrasts=len(contrasts),groups=len(groups))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data',required=True);p.add_argument('--folds',required=True)
    p.add_argument('--forecasts',nargs='+',required=True);p.add_argument('--out',required=True)
    p.add_argument('--bootstrap',type=int,default=BOOTSTRAP)
    p.add_argument('--allow-incomplete-forecasts',action='store_true')
    a=p.parse_args()
    print(json.dumps(score_files(a.data,a.folds,a.forecasts,a.out,a.bootstrap,a.allow_incomplete_forecasts)))


if __name__=='__main__':main()
