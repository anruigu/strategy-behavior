"""Portable numerical baselines; empirical fitting entrypoint is Fleet-only.

No original modeling module/vendor directory is imported. NumPy and SciPy are
imported only inside numerical fitting/prediction functions.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path

from prediction.games import payoff
from prediction.improve.data import TARGETS, canonical_hash, file_hash, game_of, target_weights, write_new

METHODS = ('context', 'family', 'nash', 'payoff_dominant', 'calibrated_payoff_dominant',
           'normalized_logistic', 'combined_logistic')
ALPHAS = (0.001, 0.01, 0.1)
SEED = 20260910
CALIBRATION_EPS = 0.01


def protocol():
    return dict(version='improve-baselines-v1', methods=list(METHODS), targets=list(TARGETS),
        training_authority='Fleet Training API custom job; no empirical local fitting',
        objective='Mean game-equal event binary cross entropy per target; ridge on slopes, unpenalized intercept',
        numerical_features='normalized: original derived normalized strategic features, excluding raw/offset/scale/mean/variance and normalized_R/S/T/P; combined adds raw R/S/T/P',
        identities='Both ordered focal/opponent one-hot; categories/scaling fitted on training partition; unknown identities all-zero',
        logistic_alphas=list(ALPHAS), inner_cv='Three deterministic canonical-group partitions by SHA256(seed,group); all preprocessing/refits train-only; equal-game validation log loss; ties favor stronger regularization',
        calibration='Per-target monotone Platt scaling sigmoid(intercept+slope*logit(clip(theory,.01,.99))); slope>=0; fixed ridge0.01 shrinks slope toward1 and intercept toward0; fit only outer training',
        fallback='No eligible training groups => explicit null; fewer than two groups or constant target => weighted population probability for learned heads; unknown family/context => training population probability',
        equilibrium_ties='Payoff-dominant symmetric pure equilibrium; equal-payoff ties are a joint coordinated-profile mixture, not independent actions',
        seed=SEED, inference_clip='No artificial clipping in exported probabilities; proper-score clipping belongs to fixed scorer')


def equilibrium(row, target, dominant=True):
    game = game_of(row)
    app, f = game['applicability'], game['features']
    if target != 'action0' and not app[target]:
        return None
    symmetric = [p for p in game['pure_nash'] if p[0] == p[1]]
    distribution = []
    if dominant and symmetric:
        best = max(payoff(game,*p)[0] for p in symmetric)
        span = max(game['payoffs'].values())-min(game['payoffs'].values())
        selected = [p for p in symmetric if best-payoff(game,*p)[0] <= 1e-9*span]
        distribution = [(p,1/len(selected)) for p in selected]
    else:
        if f['all_indifferent']:
            q = .5
        elif len(game['pure_nash']) == 1 and symmetric:
            q = float(symmetric[0][0] == 0)
        elif f['has_interior_mixed_equilibrium']:
            q = f['mixed_equilibrium_action0_probability']
        elif f['nash_00']:
            q = 1.0
        elif f['nash_11']:
            q = 0.0
        else:
            return None
        distribution = [((a,b),(q if a==0 else 1-q)*(q if b==0 else 1-q)) for a in (0,1) for b in (0,1)]
    if target == 'action0':
        return sum(p for (a,b),p in distribution if a == 0)
    selected = ({(app['cooperative_action'],app['cooperative_action'])} if target == 'cooperation'
                else {tuple(p) for p in app['coordination_outcomes']})
    return sum(p for actions,p in distribution if tuple(actions) in selected)


def prepared(rows, target):
    import numpy as np
    eligible = [r for r in rows if r['targets'][target]['opportunities'] > 0]
    if not eligible:
        return [], np.asarray([]), np.asarray([])
    index = TARGETS.index(target)
    weights = np.asarray([w[index] for w in target_weights(eligible)], dtype=float)
    y = np.asarray([r['targets'][target]['successes']/r['targets'][target]['opportunities'] for r in eligible])
    return eligible, y, weights


def weighted_mean(y, weights):
    return float((y*weights).sum()/weights.sum()) if len(y) else None


def encoder_fit(rows, weights, representation):
    import numpy as np
    forbidden = {'payoff_offset','payoff_scale','payoff_mean','payoff_variance',
                 'normalized_R','normalized_S','normalized_T','normalized_P'}
    keys = sorted(k for k in game_of(rows[0])['features'] if not k.startswith('raw_') and k not in forbidden)
    fields = [('features',k) for k in keys]
    if representation == 'combined':
        fields = [('payoffs',k) for k in ('R','S','T','P')]+fields
    games = [game_of(row) for row in rows]
    x = np.asarray([[game[source][key] for source,key in fields] for game in games])
    mean = np.average(x, weights=weights, axis=0)
    scale = np.sqrt(np.average((x-mean)**2, weights=weights, axis=0))
    scale[scale < 1e-10] = 1.0
    return dict(fields=fields, mean=mean.tolist(), scale=scale.tolist(),
                categories={field:sorted({r[field] for r in rows}) for field in ('model','opponent')})


def encode(encoder, rows):
    import numpy as np
    values = []
    for row in rows:
        game = game_of(row)
        numeric = [(game[source][key]-mean)/scale for (source,key),mean,scale in
                   zip(encoder['fields'],encoder['mean'],encoder['scale'])]
        identity = [float(row[field] == name) for field in ('model','opponent') for name in encoder['categories'][field]]
        values.append([1.0]+numeric+identity)
    return np.asarray(values, dtype=float)


def logistic_fit(x, y, weights, alpha, calibration=False):
    import numpy as np
    from scipy.optimize import minimize
    from scipy.special import expit
    weights = weights/weights.sum()
    initial = np.zeros(x.shape[1], dtype=float)
    reference = np.zeros_like(initial)
    if calibration:
        initial[1] = reference[1] = 1
        penalty = np.ones_like(initial)
        bounds = [(None,None),(0,None)]
    else:
        mean = min(1-1e-6,max(1e-6,weighted_mean(y,weights)))
        initial[0] = math.log(mean/(1-mean))
        penalty = np.ones_like(initial); penalty[0] = 0
        bounds = None
    def objective(beta):
        z = x@beta
        delta = beta-reference
        loss = float((weights*(np.logaddexp(0,z)-y*z)).sum()+.5*alpha*(penalty*delta**2).sum())
        gradient = x.T@(weights*(expit(z)-y))+alpha*penalty*delta
        return loss, gradient
    fit = minimize(objective, initial, jac=True, method='L-BFGS-B', bounds=bounds,
                   options=dict(maxiter=500,ftol=1e-12,gtol=1e-8))
    if not fit.success or not np.isfinite(fit.x).all():
        raise RuntimeError('Optimization failed: '+str(fit.message))
    return dict(coefficients=fit.x.tolist(), alpha=alpha, converged=bool(fit.success),
                iterations=int(fit.nit), objective=float(fit.fun), gradient_max=float(abs(fit.jac).max()))


def probability(fit, rows):
    import numpy as np
    from scipy.special import expit
    if fit['kind'] == 'constant':
        return [fit['prediction']]*len(rows)
    if fit['kind'] == 'logistic':
        x = encode(fit['encoder'], rows)
    elif fit['kind'] == 'calibration':
        q = [min(1-CALIBRATION_EPS,max(CALIBRATION_EPS,equilibrium(r,fit['target']))) for r in rows]
        x = np.asarray([[1,math.log(v/(1-v))] for v in q])
    else:
        raise ValueError('Unsupported numerical fit')
    return expit(x@np.asarray(fit['optimizer']['coefficients'])).tolist()


def fit_logistic(rows, target, representation, tune=True):
    import numpy as np
    eligible, y, weights = prepared(rows,target)
    mean = weighted_mean(y,weights)
    groups = sorted({r['group_id'] for r in eligible})
    if len(groups) < 2 or not len(y) or min(y) == max(y):
        return dict(kind='constant', prediction=mean, reason='insufficient group support or constant target')
    selection = []
    alpha = 0.01
    if tune and len(groups) >= 3:
        ordered = sorted(groups,key=lambda g:canonical_hash([SEED,g]))
        partitions = [set(ordered[k::3]) for k in range(3)]
        for candidate in ALPHAS:
            losses = []
            for held in partitions:
                inner_train = [r for r in eligible if r['group_id'] not in held]
                inner_test = [r for r in eligible if r['group_id'] in held]
                train, iy, iw = prepared(inner_train,target)
                test, ty, tw = prepared(inner_test,target)
                if len({r['group_id'] for r in train}) < 2 or len(set(iy)) < 2:
                    predictions = np.full(len(test),weighted_mean(iy,iw))
                else:
                    encoder = encoder_fit(train,iw,representation)
                    optimizer = logistic_fit(encode(encoder,train),iy,iw,candidate)
                    predictions = probability(dict(kind='logistic',encoder=encoder,optimizer=optimizer),test)
                p = np.clip(predictions,1e-7,1-1e-7)
                losses.extend(zip((-ty*np.log(p)-(1-ty)*np.log1p(-p)).tolist(),tw.tolist()))
            score = sum(loss*w for loss,w in losses)/sum(w for _,w in losses)
            selection.append(dict(alpha=candidate, game_equal_logloss=score))
        alpha = min(selection,key=lambda x:(x['game_equal_logloss'],-x['alpha']))['alpha']
    encoder = encoder_fit(eligible,weights,representation)
    return dict(kind='logistic', encoder=encoder,
                optimizer=logistic_fit(encode(encoder,eligible),y,weights,alpha),
                inner_selection=selection, training_groups=len(groups))


def fit_methods(rows, target):
    """Call on actual outcomes only inside the authorized Fleet worker."""
    import numpy as np
    eligible, y, weights = prepared(rows,target)
    fallback = weighted_mean(y,weights)
    fits = {}
    for method in ('context','family'):
        buckets = defaultdict(lambda:[0.0,0.0])
        for row,value,weight in zip(eligible,y,weights):
            key = json.dumps([row['model'],row['opponent']]) if method == 'context' else row['family']
            buckets[key][0] += value*weight; buckets[key][1] += weight
        fits[method] = dict(kind=method, fallback=fallback,
                           values={key:k/n for key,(k,n) in buckets.items()})
    fits['nash'], fits['payoff_dominant'] = dict(kind='nash'),dict(kind='payoff_dominant')
    if len({r['group_id'] for r in eligible}) < 2:
        fits['calibrated_payoff_dominant'] = dict(kind='constant',prediction=fallback,reason='insufficient support')
    else:
        q = [min(1-CALIBRATION_EPS,max(CALIBRATION_EPS,equilibrium(row,target))) for row in eligible]
        x = np.asarray([[1,math.log(v/(1-v))] for v in q])
        fits['calibrated_payoff_dominant'] = dict(kind='calibration',target=target,
            optimizer=logistic_fit(x,y,weights,0.01,calibration=True))
    for method, representation in [('normalized_logistic','normalized'),('combined_logistic','combined')]:
        fits[method] = fit_logistic(rows,target,representation)
    return fits


def predict(fit, row, target):
    if target != 'action0' and not game_of(row)['applicability'][target]:
        return None
    kind = fit['kind']
    if kind in ('nash','payoff_dominant'):
        value = equilibrium(row,target,dominant=kind=='payoff_dominant')
    elif kind in ('context','family'):
        key = json.dumps([row['model'],row['opponent']]) if kind=='context' else row['family']
        value = fit['values'].get(key,fit['fallback'])
    else:
        value = probability(fit,[row])[0]
    if value is not None and (not math.isfinite(value) or not 0 <= value <= 1):
        raise ValueError('Nonprobability forecast')
    return value


def forecast_rows(fits, examples, split, fold_id):
    for row in examples:
        for target in TARGETS:
            for method in METHODS:
                yield dict(row_id=row['row_id'], game_id=row['game_id'],group_id=row['group_id'],
                    family=row['family'], model=row['model'],opponent=row['opponent'],
                    method=method,split=split,fold_id=fold_id,target=target,
                    prediction=predict(fits[target][method],row,target))


def fleet_guard(run_id):
    if not run_id or os.environ.get('IMPROVE_TRAINING_AUTHORITY') != 'fleet_api' or os.environ.get('IMPROVE_FLEET_RUN_ID') != run_id:
        raise RuntimeError('Empirical fitting requires the Fleet-submitted worker authority and matching run ID')


def run_worker(data_path, folds_path, out, run_id):
    fleet_guard(run_id)
    import numpy as np
    import scipy
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('Preserve existing worker artifacts')
    out.mkdir(parents=True,exist_ok=True)
    inputs = {str(Path(p).resolve()):file_hash(p) for p in (data_path,folds_path)}
    sources = {str(Path(__file__).resolve()):file_hash(__file__),
               str(Path(__file__).with_name('data.py').resolve()):file_hash(Path(__file__).with_name('data.py'))}
    data, folds = json.loads(Path(data_path).read_text()),json.loads(Path(folds_path).read_text())
    started = datetime.now(timezone.utc).isoformat()
    write_new(out/'run.json',dict(status='running',started_utc=started,run_id=run_id,protocol=protocol(),
                                input_sha256=inputs,source_sha256=sources, numpy=np.__version__,scipy=scipy.__version__))
    artifacts, predictions = {}, []
    for fold in folds:
        train = [data['train_examples'][i] for i in fold['train']]
        dataset = data['train_examples'] if fold['test_dataset']=='train' else data['development_examples']
        test = [dataset[i] for i in fold['test']]
        assert [r['row_id'] for r in train] == fold['train_row_ids']
        assert [r['row_id'] for r in test] == fold['test_row_ids']
        assert not {r['group_id'] for r in train}&{r['group_id'] for r in test}
        fit = {target:fit_methods(train,target) for target in TARGETS}
        artifact = dict(fold_id=fold['fold_id'],split=fold['split'],training_sha256=canonical_hash(train),
                        training_row_ids=[r['row_id'] for r in train],fits=fit)
        artifacts[fold['fold_id']] = artifact
        write_new(out/(fold['fold_id']+'.fit.json'),artifact)
        predictions.extend(forecast_rows(fit,test,fold['split'],fold['fold_id']))
    with (out/'forecasts.jsonl').open('x') as handle:
        for row in predictions:
            handle.write(json.dumps(row,allow_nan=False)+'\n')
    write_new(out/'fits.json',artifacts)
    for path,expected in {**inputs,**sources}.items():
        if file_hash(path) != expected:
            raise ValueError('Worker input/source changed: '+path)
    outputs = {str(p.resolve()):file_hash(p) for p in out.iterdir() if p.is_file()}
    status = dict(status='complete',created_utc=datetime.now(timezone.utc).isoformat(),run_id=run_id,
                  started_utc=started,input_sha256=inputs,source_sha256=sources,output_sha256=outputs,
                  folds=len(folds),forecast_rows=len(predictions),training_authority='fleet_api')
    write_new(out/'completion.json',status)
    return status


def forecast(artifact_path, examples_path, output, split='fresh', fold_id='full'):
    """Apply saved parameters; this function performs no fitting."""
    inputs = {str(Path(p).resolve()):file_hash(p) for p in (artifact_path,examples_path)}
    artifact = json.loads(Path(artifact_path).read_text())
    if 'fits' not in artifact:
        artifact = artifact[fold_id]
    examples = json.loads(Path(examples_path).read_text())
    output = Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as handle:
        for row in forecast_rows(artifact['fits'],examples,split,fold_id):
            handle.write(json.dumps(row,allow_nan=False)+'\n')
    for path,value in inputs.items():
        if file_hash(path) != value:
            raise ValueError('Forecast input changed')
    write_new(output.with_suffix('.manifest.json'),dict(created_utc=datetime.now(timezone.utc).isoformat(),
        input_sha256=inputs,forecast_sha256=file_hash(output),fitting_performed=False,
        training_sha256=artifact['training_sha256'],fold_id=fold_id,split=split))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command',required=True)
    train = sub.add_parser('train')
    for name in ('data','folds','out','fleet-run-id'):
        train.add_argument('--'+name,required=True)
    pred = sub.add_parser('forecast')
    for name in ('artifact','examples','out'):
        pred.add_argument('--'+name,required=True)
    pred.add_argument('--fold-id',default='full'); pred.add_argument('--split',default='fresh')
    args = parser.parse_args()
    if args.command == 'train':
        print(json.dumps(run_worker(args.data,args.folds,args.out,args.fleet_run_id)))
    else:
        forecast(args.artifact,args.examples,args.out,args.split,args.fold_id)


if __name__ == '__main__':
    main()
