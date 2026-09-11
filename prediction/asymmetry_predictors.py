"""Few-shot versus learned bimatrix predictors, frozen before fresh matches.

Training: the first asymmetric pilot. Outer holdout: the entire query payoff
shape, including role swaps, independent action relabeling and positive affine
utility transformations. Test: a fresh balanced replay of the 16-cell grid.
No inference occurs on import or with --action prepare.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
import argparse
import hashlib
import json
import math
from pathlib import Path
import pickle
import random
import shutil
from statistics import mean
import sys

from prediction import asymmetry_smoke as smoke
from prediction.io_utils import digest, now, read_json, write_json
from prediction.client import Client, Ledger, ModelConfig
from prediction.modeling import FittedPredictor, ModelSpec

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260910
METHODS = ('few_shot', 'logistic', 'mlp', 'zero_shot', 'stage_nash', 'uniform')


def normalized(matrix):
    ranges = [(min(matrix[a][b][p] for a,b in smoke.PROFILES),
               max(matrix[a][b][p] for a,b in smoke.PROFILES)) for p in range(2)]
    return [[[(matrix[a][b][p]-ranges[p][0])/(ranges[p][1]-ranges[p][0])
               if ranges[p][1] > ranges[p][0] else 0.0 for p in range(2)] for b in range(2)] for a in range(2)]


def shape_id(game):
    matrix = normalized(game['matrix'])
    variants = []
    for row_swap in range(2):
        for col_swap in range(2):
            m = [[matrix[a ^ row_swap][b ^ col_swap] for b in range(2)] for a in range(2)]
            variants.append(tuple(round(x,10) for a,b in smoke.PROFILES for x in m[a][b]))
            variants.append(tuple(round(x,10) for a,b in smoke.PROFILES for x in m[b][a][::-1]))
    return digest(min(variants))[:24]


def features(game, player, swap):
    result = {}
    for side,p in [('self',player),('other',1-player)]:
        values = [smoke.focal_cell(game,p,a,b)[0] for a,b in smoke.PROFILES]
        lo,hi = min(values),max(values)
        norm = [(v-lo)/(hi-lo) if hi > lo else 0.0 for v in values]
        for (a,b),raw,n in zip(smoke.PROFILES,values,norm):
            result[f'{side}_payoff_{a}{b}'] = raw
            result[f'{side}_normalized_{a}{b}'] = n
        gaps = [norm[b]-norm[2+b] for b in range(2)]
        for b,g in enumerate(gaps): result[f'{side}_gap_against_{b}'] = g
        result[f'{side}_dominant_0'] = float(min(gaps)>0)
        result[f'{side}_dominant_1'] = float(max(gaps)<0)
    pure = [p if player == 0 else p[::-1] for p in game['pure_nash']]
    for a,b in smoke.PROFILES: result[f'pure_nash_{a}{b}'] = float([a,b] in pure)
    result['pure_nash_count'] = len(pure)
    result['display_swap'] = float(swap)
    return result


def rows_for(trace, labels=True):
    game,spec = trace['game'],trace['spec']
    rows = []
    for p in range(2):
        row = dict(episode_id=spec['id'],game_id=game['id'],group_id=shape_id(game),
                   condition=game['condition'],player=p,model=spec['models'][p],opponent=spec['models'][1-p],
                   swap=spec['swap'],features=features(game,p,spec['swap']))
        if labels:
            n = len(trace['rounds'])
            k = sum(t['actions'][p] == 0 for t in trace['rounds'])
            row['targets'] = dict(action0=dict(applicable=True,value=k/n,successes=k,opportunities=n))
        rows.append(row)
    return rows


def training_for(traces, game):
    excluded = shape_id(game)
    return [t for t in traces if shape_id(t['game']) != excluded]


def select_examples(traces, game, spec):
    allowed = training_for(traces,game)
    buckets = defaultdict(list)
    for trace in allowed:
        if trace['spec']['models'] == spec['models']:
            buckets[trace['game']['id']].append(trace)
    q = normalized(game['matrix'])
    candidates = []
    for gid,items in buckets.items():
        g = items[0]['game']
        matrix = normalized(g['matrix'])
        distance = sum((matrix[a][b][p]-q[a][b][p])**2 for a,b in smoke.PROFILES for p in range(2))
        candidates.append((distance,gid,items))
    examples,groups = [],set()
    for distance,gid,items in sorted(candidates):
        g = items[0]['game']
        group = shape_id(g)
        if group in groups: continue
        groups.add(group)
        turns = [t for trace in items for t in trace['rounds']]
        examples.append(dict(game_id=gid,group_id=group,matrix=g['matrix'],models=spec['models'],
                             joint_counts=[sum(t['actions']==list(p) for t in turns) for p in smoke.PROFILES],
                             rounds=len(turns),episodes=[t['spec']['id'] for t in items],distance=distance,
                             display_swaps=[t['spec']['swap'] for t in items]))
        if len(examples) == 3: break
    assert len(examples) == 3 and shape_id(game) not in groups
    return examples


def few_messages(game,spec,examples):
    messages = smoke.forecast_messages(game,spec)
    payload = []
    swap = int(spec['swap'])
    for example in examples:
        cells = [dict(actions=['AB'[a],'AB'[b]],points=example['matrix'][a ^ swap][b ^ swap]) for a,b in smoke.PROFILES]
        rates = [example['joint_counts'][2*(a ^ swap)+(b ^ swap)]/example['rounds'] for a,b in smoke.PROFILES]
        payload.append(dict(player_models=example['models'],payoffs=cells,
                            observed_joint_frequencies_AA_AB_BA_BB=rates,observed_rounds=example['rounds']))
    prefix = ('Three examples from other payoff games played by the same ordered model pair under the same protocol '
              'follow. Observations pool two matches with balanced display labels; payoffs and outcomes have been '
              'mapped to the A/B coordinates shown here. Use these examples to forecast the target game below. '
              'No example comes from the target payoff shape or an equivalent role/action relabeling.\n'
              + json.dumps(payload) + '\n\nTARGET GAME:\n')
    messages[1]['content'] = prefix + messages[1]['content']
    return messages


def archive_sources(out):
    sources = {}
    for module in list(sys.modules.values()):
        name = getattr(module,'__file__',None)
        if not name: continue
        path = Path(name).resolve()
        if path.is_relative_to(ROOT) and path.suffix == '.py' and not {'vendor','results'}.intersection(path.parts):
            relative = str(path.relative_to(ROOT))
            sources[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
            target = out/'source'/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,target)
    return sources


def prepare(out,source):
    if (out/'manifest.json').exists():
        manifest = read_json(out/'manifest.json')
        for name,expected in manifest['sources'].items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
        assert digest(read_json(out/'training-traces.json')) == manifest['training_sha256']
        assert digest(read_json(out/'queries.json')) == manifest['queries_sha256']
        assert digest(read_json(out/'zero-shot.json')) == manifest['zero_shot_sha256']
        return manifest
    assert not list((out/'episodes').glob('**/*.json'))
    old = read_json(source/'manifest.json')
    training = smoke.verify(source,old)
    assert len(training)==64
    games = deepcopy(old['games'])
    assert len({shape_id(g) for g in games}) == 10
    episodes,queries,zero = [],{},{}
    for oldspec in old['episodes']:
        spec = dict(oldspec,id=oldspec['id']+'--fresh')
        game = next(g for g in games if g['id']==spec['game_id'])
        examples = select_examples(training,game,spec)
        queries[spec['id']] = dict(examples=examples,messages=few_messages(game,spec,examples),excluded_group=shape_id(game))
        previous = read_json(source/'forecasts'/(oldspec['id']+'.json'))
        assert previous['messages']==smoke.forecast_messages(game,spec)
        zero[spec['id']] = dict(joint=previous['joint'],source_episode=oldspec['id'],source_forecast_sha256=digest(previous))
        episodes.append(spec)
    random.Random(SEED+1).shuffle(episodes)
    write_json(out/'training-traces.json',training)
    write_json(out/'queries.json',queries)
    write_json(out/'zero-shot.json',zero)
    manifest = dict(created=now(),games=games,episodes=episodes,models=old['models'],protocol=old['protocol'],
                    training_source=str(source.resolve()),training_sha256=digest(training),queries_sha256=digest(queries),
                    zero_shot_sha256=digest(zero),training_manifest_sha256=digest(old),sources=archive_sources(out),
                    design='Leave entire query payoff-equivalence group out of old pilot; forecast fresh balanced replay.',
                    equivalence='Independent action relabeling, player-role swap, independent positive affine utility transforms',
                    few_shot='Three nearest distinct allowed groups by eight normalized payoffs; matching ordered model pair; pooled labels',
                    numerical='Original logistic and 16-unit tanh MLP estimators with new explicit both-player payoff features and model identities',
                    target='Canonical focal action0 probability over eight rounds',primary_comparison='few_shot versus logistic and mlp on asymmetric games',
                    weighting='Fitting: equal equivalence-group mass; scoring: equal ordered payoff pairing',
                    uncertainty='Paired resampling of unordered payoff groups and whole fresh episodes; fixed fits/forecasts, no retraining',
                    budget_usd=20,seed=SEED)
    write_json(out/'manifest.json',manifest)
    return manifest


def fit_numeric(out,manifest):
    path = out/'numeric.json'
    if path.exists(): return read_json(path)
    training = read_json(out/'training-traces.json')
    predictions,folds,artifacts = {},{},{}
    groups = sorted({shape_id(g) for g in manifest['games']})
    for group in groups:
        query_specs = [s for s in manifest['episodes'] if shape_id(next(g for g in manifest['games'] if g['id']==s['game_id']))==group]
        heldout = [g['id'] for g in manifest['games'] if shape_id(g)==group]
        train = [r for t in training if shape_id(t['game'])!=group for r in rows_for(t)]
        metadata = [r for spec in query_specs for r in rows_for(dict(spec=spec,game=next(g for g in manifest['games'] if g['id']==spec['game_id'])),False)]
        assert group not in {r['group_id'] for r in train}
        fold = dict(heldout_games=heldout,training_episodes=sorted({r['episode_id'] for r in train}),
                    training_groups=sorted({r['group_id'] for r in train}),training_rows_sha256=digest(train),models={})
        for method in ('logistic','mlp'):
            # The existing feature-only encoder accepts the explicit bimatrix
            # columns; its legacy representation name is 'structural'. No old
            # four-payoff inputs or fitted symmetric weights are used.
            model = FittedPredictor(ModelSpec('bimatrix_'+method,method,'structural','both'),'action0',SEED).fit(train)
            pred = model.predict(metadata)
            fold['models'][method] = model.metadata()
            target = out/'models'/f'{group}--{method}.pkl'
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream: pickle.dump(model,stream)
            artifacts[str(target.relative_to(out))] = hashlib.sha256(target.read_bytes()).hexdigest()
            for row,p in zip(metadata,pred):
                assert p is not None and math.isfinite(p) and 0<=p<=1
                predictions.setdefault(row['episode_id'],{}).setdefault(method,[None,None])[row['player']] = p
        folds[group] = fold
        print(json.dumps(dict(stage='fit',completed=len(folds),planned=len(groups))),flush=True)
    result = dict(fitted_at=now(),manifest_sha256=digest(manifest),predictions=predictions,folds=folds,model_artifacts=artifacts)
    write_json(path,result)
    return result


def forecast_one(out,query,spec,client):
    path = out/'forecasts'/(spec['id']+'.json')
    item = read_json(path) if path.exists() else dict(messages=query['messages'],attempts=[],status='pending')
    assert item['messages']==query['messages']
    if item['status']=='complete': return item
    while len(item['attempts'])<2:
        reply,meta = client.generate(item['messages'],purpose='few_shot_forecast')
        attempt = dict(reply=reply,meta=meta)
        item['attempts'].append(attempt)
        if meta['status']=='ok':
            try: item.update(joint=smoke.parse_forecast(reply,spec['swap']),status='complete',finished=now())
            except (ValueError,TypeError,KeyError) as exc: attempt['parse_error']=str(exc)
        write_json(path,item)
        if item['status']=='complete': return item
        if meta.get('http_status') in (401,402,403,404): break
    raise RuntimeError('Few-shot forecast failed: '+spec['id'])


def verify(out,manifest):
    frozen = read_json(out/'forecast-freeze.json')
    numeric,queries = read_json(out/'numeric.json'),read_json(out/'queries.json')
    assert frozen['numeric_sha256']==digest(numeric)
    assert frozen['queries_sha256']==digest(queries)==manifest['queries_sha256']
    assert frozen['training_sha256']==digest(read_json(out/'training-traces.json'))==manifest['training_sha256']
    assert frozen['zero_shot_sha256']==digest(read_json(out/'zero-shot.json'))==manifest['zero_shot_sha256']
    assert numeric['fitted_at']<frozen['frozen_at'] and numeric['manifest_sha256']==digest(manifest)
    for name,expected in numeric['model_artifacts'].items():
        assert hashlib.sha256((out/name).read_bytes()).hexdigest()==expected
    training = read_json(out/'training-traces.json')
    train_index = {t['spec']['id']:t for t in training}
    for group,fold in numeric['folds'].items():
        expected = sorted(t['spec']['id'] for t in training if shape_id(t['game'])!=group)
        assert fold['training_episodes']==expected and group not in fold['training_groups']
        assert fold['training_rows_sha256']==digest([r for t in training if shape_id(t['game'])!=group for r in rows_for(t)])
    for spec in manifest['episodes']:
        game = next(g for g in manifest['games'] if g['id']==spec['game_id'])
        query = queries[spec['id']]
        assert query['examples']==select_examples(training,game,spec)
        assert query['messages']==few_messages(game,spec,query['examples'])
        for example in query['examples']:
            assert all(shape_id(train_index[e]['game'])!=shape_id(game) for e in example['episodes'])
        forecast = read_json(out/'forecasts'/(spec['id']+'.json'))
        assert forecast['messages']==query['messages']
        for attempt in forecast['attempts']:
            call = read_json(out/'calls/kimi-k3'/(attempt['meta']['call_id']+'.json'))
            assert call['timestamp']<frozen['frozen_at'] and call['request']['messages']==query['messages']
            assert call['config']==manifest['models']['kimi-k3']
        assert call['response']['choices'][0]['message']['content']==forecast['attempts'][-1]['reply']
    return smoke.verify(out,manifest)


def paired_interval(rows,condition,other,metric,seed=SEED):
    selected = [r for r in rows if condition=='all' or r['condition']==condition]
    groups = sorted({r['group_id'] for r in selected})
    units = {g:sorted({r['episode_id'] for r in selected if r['group_id']==g}) for g in groups}
    differences = {episode:mean(r[metric] for r in selected if r['episode_id']==episode and r['method']=='few_shot')
                  -mean(r[metric] for r in selected if r['episode_id']==episode and r['method']==other)
                   for group in groups for episode in units[group]}
    # The all-grid estimand weights each ordered game equally. Asymmetric
    # groups contain two role orientations, hence twice the symmetric mass.
    game_counts = {g:len({r['game_id'] for r in selected if r['group_id']==g}) for g in groups}
    rng = random.Random(seed)
    draws = []
    for _ in range(4000):
        sample = rng.choices(groups,k=len(groups))
        draws.append(sum(game_counts[g]*mean(differences[e] for e in rng.choices(units[g],k=len(units[g]))) for g in sample)
                     /sum(game_counts[g] for g in sample))
    draws.sort()
    return dict(few_shot_minus_comparator=mean(r[metric] for r in selected if r['method']=='few_shot')
                -mean(r[metric] for r in selected if r['method']==other),descriptive_95_interval=[draws[100],draws[3899]],groups=len(groups))


def analyze(out,manifest):
    traces = verify(out,manifest)
    assert len(traces)==len(manifest['episodes'])==64,'Require complete common support before comparison'
    numerical,zero = read_json(out/'numeric.json'),read_json(out/'zero-shot.json')
    rows = []
    for trace in traces:
        spec,game = trace['spec'],trace['game']
        joint = {'few_shot':read_json(out/'forecasts'/(spec['id']+'.json'))['joint'],
                 'zero_shot':zero[spec['id']]['joint'],'stage_nash':smoke.theory(game),'uniform':[.25]*4}
        predictions = {method:[probs[0]+probs[1],probs[0]+probs[2]] for method,probs in joint.items()}
        predictions.update(numerical['predictions'][spec['id']])
        for method,pred in predictions.items():
            for p in range(2):
                y = mean(t['actions'][p]==0 for t in trace['rounds'])
                q = pred[p]
                clipped = min(1-1e-6,max(1e-6,q))
                rows.append(dict(episode_id=spec['id'],game_id=game['id'],group_id=shape_id(game),condition=game['condition'],
                                 method=method,player=p,model=spec['models'][p],swap=spec['swap'],observed=y,prediction=q,
                                 brier=mean((q-int(t['actions'][p]==0))**2 for t in trace['rounds']),
                                 episode_rate_mse=(q-y)**2,log_loss=-y*math.log(clipped)-(1-y)*math.log(1-clipped)))
    cells = []
    for key in sorted({(r['game_id'],r['model'],r['player'],r['method']) for r in rows}):
        block = [r for r in rows if (r['game_id'],r['model'],r['player'],r['method'])==key]
        q,y = mean(r['prediction'] for r in block),mean(r['observed'] for r in block)
        cells.append(dict(game_id=key[0],model=key[1],player=key[2],method=key[3],condition=block[0]['condition'],
                          rate_mse=(q-y)**2,rate_mae=abs(q-y)))
    scores,contrasts = {},{}
    for condition in ('symmetric','asymmetric','all'):
        subset = [r for r in rows if condition=='all' or r['condition']==condition]
        cc = [r for r in cells if condition=='all' or r['condition']==condition]
        scores[condition] = {method:{**{metric:mean(r[metric] for r in subset if r['method']==method)
                                        for metric in ('brier','log_loss','episode_rate_mse')},
                                    **{metric:mean(r[metric] for r in cc if r['method']==method) for metric in ('rate_mse','rate_mae')}} for method in METHODS}
        contrasts[condition] = {other:paired_interval(rows,condition,other,'brier') for other in METHODS if other!='few_shot'}
    calls = [read_json(p) for p in (out/'calls').glob('*/*.json')]
    players = [c for c in calls if c['purpose']=='play']
    freeze = read_json(out/'forecast-freeze.json')
    assert all(c['timestamp']>freeze['frozen_at'] for c in players)
    for name,expected in manifest['sources'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
        assert hashlib.sha256((out/'source'/name).read_bytes()).hexdigest()==expected
    audit = dict(checked_at=now(),completed=64,actions=1024,forecast_freeze=freeze['frozen_at'],
                 first_player_call=min(c['timestamp'] for c in players),training_matches=64,outer_folds=10,
                 few_shot_queries=64,numeric_forecasts=256,call_states=dict(Counter(c['status'] for c in calls)),
                 source_files_verified=len(manifest['sources']),checks=['whole payoff-group exclusion from fitting and examples',
                 'example selection and counts recomputed from training only','training/source/model/query/forecast hashes',
                 'forecasts before all fresh player calls','complete common support and both role/label orientations',
                 'fresh prompt/action/payoff/raw-call verification'])
    summary = dict(analyzed_at=now(),scores=scores,paired_brier_contrasts=contrasts,audit=audit,
                   budget=Ledger(out/'budget.sqlite',20).summary())
    write_json(out/'analysis-rows.json',rows)
    write_json(out/'analysis-cells.json',cells)
    write_json(out/'AUDIT.json',audit)
    write_json(out/'summary.json',summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--training',type=Path,default=Path('prediction/results/asymmetry-20260910-openrouter'))
    parser.add_argument('--action',choices=('prepare','predict','play','analyze','run'),default='run')
    args = parser.parse_args()
    out = args.out
    manifest = prepare(out,args.training)
    if args.action=='prepare':
        print(json.dumps(dict(episodes=len(manifest['episodes']),queries=64,groups=10)))
        return
    if args.action=='analyze':
        print(json.dumps(analyze(out,manifest),indent=2)); return
    ledger,stage = Ledger(out/'budget.sqlite',20),Ledger(out/'stage-budget.sqlite',20)
    clients = {name:Client(ModelConfig(**cfg),out/'calls'/name,ledger,stage,4096) for name,cfg in manifest['models'].items()}
    frozen_path = out/'forecast-freeze.json'
    if not frozen_path.exists():
        assert args.action!='play','Freeze predictions before starting matches'
        assert not list((out/'episodes').glob('**/*.json'))
        numerical = fit_numeric(out,manifest)
        queries = read_json(out/'queries.json')
        first = manifest['episodes'][0]
        forecast_one(out,queries[first['id']],first,clients['kimi-k3'])
        with ThreadPoolExecutor(max_workers=12) as pool:
            futures = [pool.submit(forecast_one,out,queries[s['id']],s,clients['kimi-k3']) for s in manifest['episodes']]
            for n,f in enumerate(as_completed(futures),1):
                f.result()
                print(json.dumps(dict(stage='few_shot',completed=n,planned=64)),flush=True)
        write_json(frozen_path,dict(frozen_at=now(),manifest_sha256=digest(manifest),numeric_sha256=digest(numerical),
                   forecast_sha256=digest({s['id']:read_json(out/'forecasts'/(s['id']+'.json')) for s in manifest['episodes']}),
                   queries_sha256=manifest['queries_sha256'],training_sha256=manifest['training_sha256'],zero_shot_sha256=manifest['zero_shot_sha256']))
    verify(out,manifest)
    if args.action=='predict': return
    failures = []
    with ThreadPoolExecutor(max_workers=24) as requests,ThreadPoolExecutor(max_workers=12) as episodes:
        futures = {episodes.submit(smoke.play_one,out,manifest,s,clients,requests):s for s in manifest['episodes']}
        for n,f in enumerate(as_completed(futures),1):
            try: f.result()
            except Exception as exc: failures.append(dict(episode=futures[f]['id'],error=type(exc).__name__+': '+str(exc)))
            state = dict(updated=now(),stage='play',processed=n,planned=64,failures=failures,budget=ledger.summary())
            write_json(out/'status.json',state)
            print(json.dumps(state),flush=True)
    print(json.dumps(analyze(out,manifest),indent=2))


if __name__=='__main__': main()
