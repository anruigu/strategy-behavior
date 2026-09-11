"""Read-only launch evidence audit; no clients, model fitting, or outcome scoring."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import sys
sys.path.insert(0, '/shared/allie/strategy-behavior')
from prediction.prospective import (build_rows, canonical_hash, validate_compatible,
    _audit_numerical, _audit_llm, _read_forecasts, _check_forecast)

ROOT=Path('/shared/allie/strategy-behavior/prediction/results/overnight-20260910')
OUT=ROOT/'independent-analysis/prospective-launch-audit.json'
assert not OUT.exists()
source_bytes={}
def raw(path):
 path=Path(path).resolve();data=path.read_bytes()
 if str(path) in source_bytes:assert source_bytes[str(path)]==data
 source_bytes[str(path)]=data
 return data
def read(path):return json.loads(raw(path))
def sha(data):return hashlib.sha256(data).hexdigest()
def dt(value):return datetime.fromisoformat(value.replace('Z','+00:00'))
def unchanged():
 for path,data in source_bytes.items():assert Path(path).read_bytes()==data,'Changed frozen input: '+path

stage=ROOT/'prospective';manifest=read(stage/'manifest.json');primary=read(ROOT/'primary-pilot-manifest.json')
for key in ['models','protocol','sources','source_root','ledger']:assert manifest[key]==primary[key],key
for name,expected in manifest['sources'].items():assert sha(raw(Path(manifest['source_root'])/name))==expected
plan=read(ROOT/'after-matrix-plan.json');freeze=read(stage/'forecast-freeze.json')
secondary=read(ROOT/'secondary-baselines/forecast-freeze.json');secondary_plan=read(ROOT/'secondary-baselines/plan.json')
assert sha(raw(ROOT/'secondary-baselines/plan.json'))==secondary['plan_sha256']
for collection in [freeze['sha256'],secondary['forecasts_sha256']]:
 for path,expected in collection.items():assert sha(raw(path))==expected,path
assert plan['pair_holdout']==secondary_plan['pair_exclusion']
assert plan['model_holdout']==secondary_plan['model_exclusion']
assert secondary_plan['manifest_sha256']['prospective']==sha(raw(stage/'manifest.json'))
assert secondary_plan['metadata_sha256']['prospective']==sha(raw(stage/'metadata.json'))
training=read(ROOT/'training-records.json');assert sha(raw(ROOT/'training-records.json'))==plan['training_sha256']==secondary_plan['training_sha256']
planned=build_rows(manifest);assert read(stage/'metadata.json')==planned
query_groups={r['group_id'] for r in planned};train_groups={r['group_id'] for r in training};assert not query_groups&train_groups
assert len(query_groups)==21 and len(train_groups)==72 and len(planned)==840
assert Counter(g['family'] for g in manifest['games'])=={f:3 for f in {r['family'] for r in training}}
specs={s['id']:s for s in manifest['episodes']};assert len(specs)==420
expected_games={g['id']:g for g in manifest['games']}
by_context=Counter((s['game_id'],tuple(sorted(s['models']))) for s in specs.values());assert set(by_context.values())=={2}
assert len(by_context)==210
for key in by_context:
 rows=[s for s in specs.values() if (s['game_id'],tuple(sorted(s['models'])))==key]
 assert {r['swap'] for r in rows}=={False,True} and {r['trial_id'] for r in rows}=={0,1}
assert {s['representation'] for s in specs.values()}=={'matrix'}
pair=lambda r:'|'.join(sorted([r['model'],r['opponent']]))
predicates={'full':lambda r:True,'excluded_pair':lambda r:pair(r)!=plan['pair_holdout'],'excluded_model':lambda r:plan['model_holdout'] not in (r['model'],r['opponent'])}
training_audits={};numerical_audits=[]
for name,predicate in predicates.items():
 rows=read(stage/'training'/(name+'.json'));assert rows==[r for r in training if predicate(r)]
 assert set(Counter(r['episode_id'] for r in rows).values())=={2}
 audit=read(stage/'training'/(name+'.audit.json'));assert audit['filtered_sha256']==sha(raw(stage/'training'/(name+'.json')))
 fit=read(stage/'numerical'/name/'fit.pkl.json');assert fit['training_sha256']==canonical_hash(rows)
 assert read(ROOT/'secondary-baselines'/name/'training.json')==rows
 fit_secondary=read(ROOT/'secondary-baselines'/name/'fit.json')
 # Secondary JSON artifacts bind their exact filtered source file separately.
 assert fit_secondary['training_sha256']==canonical_hash(rows)
 training_audits[name]=dict(rows=len(rows),episodes=len(rows)//2,groups=len({r['group_id'] for r in rows}))
 path=stage/'numerical'/name/'forecasts.jsonl';forecasts=_read_forecasts(path,source_bytes)
 audit=_audit_numerical(path,forecasts,planned,source_bytes);assert not audit['issues'];numerical_audits.append(dict(fit=name,**audit))
 keys=set()
 for row in forecasts:
  _check_forecast(row);index=row['row_index'];assert 0<=index<len(planned)
  metadata=planned[index];assert (row['episode_id'],row['player_index'])==(metadata['episode_id'],metadata['player_index'])
  validate_compatible(row,metadata,'frozen forecast')
  key=(index,row['method'],row['target']);assert key not in keys;keys.add(key)
 assert len(keys)==len(forecasts)==85680
for source in ['full','excluded_pair','excluded_model']:
 path=ROOT/'secondary-baselines'/source/'prospective.jsonl';forecasts=_read_forecasts(path,source_bytes)
 audit=_audit_numerical(path,forecasts,planned,source_bytes);assert not audit['issues'];numerical_audits.append(dict(fit='secondary_'+source,**audit))
llm_path=stage/'llm-forecasts/forecasts.jsonl';llm_rows=_read_forecasts(llm_path,source_bytes)
llm_audit=_audit_llm(llm_path,llm_rows,manifest,planned,source_bytes);assert not llm_audit['issues']
llm_frozen=read(stage/'llm-forecasts/inputs.json');assert llm_frozen['payload']['training_records']==training
status=read(stage/'llm-forecasts/status.json');assert status['status']=='complete' and status['completed']==status['planned']==1008 and status['errors']==[]
contexts=Counter();queries=set()
for row in llm_rows:
 _check_forecast(row);assert row['status']=='complete'
 queries.add((row['game_id'],row['model'],row['opponent'],row['method']))
 contexts[row['method']]+=1
assert len(queries)==1008 and set(contexts.values())=={3696}
assert {q[0] for q in queries}==set(expected_games)
assert Counter(q[3] for q in queries)=={'llm_zero_shot':336,'llm_few_shot':336,'llm_game_theory':336}
# Copy available trace bytes without treating mutable progress bytes as frozen.
observations=[]
for name in ['trace.json','progress.json','incomplete.json']:
 for path in sorted((stage/'episodes').glob('*/'+name)):
  data=path.read_bytes();trace=json.loads(data);spec=specs[trace['id']]
  assert trace['game']==expected_games[spec['game_id']]
  assert trace['models']==spec['models']
  for key in ['trial_id','representation','swap']:assert trace[key]==spec[key]
  observations.append(dict(path=str(path.resolve()),kind=name,started=trace['started'],observed_sha256=sha(data)))
assert observations
first=min(observations,key=lambda x:dt(x['started']));earliest=dt(first['started'])
for audit in numerical_audits+[llm_audit]:assert dt(audit['created_utc'])<earliest
assert dt(freeze['created_utc'])<earliest and dt(secondary['finished'])<earliest
unchanged()
result=dict(created_utc=datetime.now(timezone.utc).isoformat(),status='verified_current_launch_evidence',api_calls=False,
 source_sha256={p:sha(b) for p,b in source_bytes.items()},primary_freeze_utc=freeze['created_utc'],secondary_freeze_utc=secondary['finished'],
 primary_freeze_files=len(freeze['sha256']),secondary_freeze_files=len(secondary['forecasts_sha256']),earliest_observed_trace=first,
 primary_freeze_lead_seconds=(earliest-dt(freeze['created_utc'])).total_seconds(),numerical_forecast_audits=numerical_audits,llm_audit=llm_audit,
 observed_trace_files=len(observations),planned_games=21,planned_episodes=420,planned_focal_rows=840,
 family_counts=dict(Counter(g['family'] for g in manifest['games'])),models=sorted(manifest['models']),protocol=manifest['protocol'],
 training=training_audits,held_pair=plan['pair_holdout'],held_model=plan['model_holdout'],
 held_pair_episodes=sum('|'.join(sorted(s['models']))==plan['pair_holdout'] for s in specs.values()),
 held_model_episodes=sum(plan['model_holdout'] in s['models'] for s in specs.values()),llm_queries_by_method=dict(Counter(q[3] for q in queries)),
 limitation='Current launch evidence only. Final scoring must recheck all actual trace start times, source hashes, completion coverage and outcome identities. Local timestamps/hashes are not external notarization. Both roles are retained for pair/model focus; LLM forecasts use full training, not the excluded fits.')
with OUT.open('x') as handle:json.dump(result,handle,indent=2,allow_nan=False);handle.write('\n')
print(json.dumps({k:result[k] for k in ['status','primary_freeze_utc','secondary_freeze_utc','earliest_observed_trace','primary_freeze_lead_seconds','planned_games','planned_episodes','held_pair_episodes','held_model_episodes','training','llm_queries_by_method']}))
