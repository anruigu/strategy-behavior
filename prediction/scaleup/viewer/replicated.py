"""Read-only replicated-study views; serving requires only the standard library."""
from collections import Counter
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2]/'general_games/scaleup_v2'


def read(path):return json.loads(path.read_text())
def rows(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()] if path.exists() else []


class ReplicatedDataset:
    def __init__(self,root=ROOT):
        self.root=Path(root);self.data=self.root/'data';self.study=self.root/'study'
        self.catalog=read(self.data/'catalog.json');self.games={g['configuration_id']:g for g in self.catalog['configurations']}
        self.instances=read(self.data/'instances.evaluator.json');self.plans={};self.paths={};self._cache=None;self._at=0
        for phase in ('training','test'):
            plan=read(self.study/phase/'plan.json');self.plans[phase]=plan
            for item in plan['episodes']:self.paths[item['episode_id']]=self.study/phase/'episodes'/(item['episode_id']+'.json')
        for name in ('pilot-20260910','parameter-check-20260910'):
            folder=self.root.parent/'runs'/name
            for item in read(folder/'plan.json')['episodes']:self.paths[item['episode_id']]=folder/'episodes'/(item['episode_id']+'.json')

    def snapshot(self):
        if self._cache is not None and time.monotonic()-self._at<10:return self._cache
        episodes=rows(self.data/'legacy-episodes.jsonl');collection={}
        for phase,plan in self.plans.items():
            exported={r['episode_id']:r for r in rows(self.study/phase/'export/episodes.jsonl')};status=Counter();actions=0
            for item in plan['episodes']:
                path=self.paths[item['episode_id']]
                if not path.exists():status['not_started']+=1;continue
                trace=read(path);status[trace['status']]+=1
                focal=[s for s in trace['steps'] if s['is_focal']];actions+=len(focal)
                if item['episode_id'] in exported:row=exported[item['episode_id']]
                else:
                    reward=(trace.get('final_state',{}).get('rewards') or {}).get(str(item['seat'])) if trace['status']=='complete' else None
                    row=dict(episode_id=item['episode_id'],source_run='v2-'+phase,status=trace['status'],seed=item['seed'],replicate=item['replicate'],
                        inputs=dict(family_id=item['game']['family_id'],game_id=item['game']['configuration_id'],model=item['model'],seat=item['seat'],prompt=item['condition']),
                        targets=dict(win=float(reward==1) if reward is not None else None,any_invalid=float(any(s['result']['native_invalid'] for s in focal)) if trace['status']=='complete' else None),
                        focal_actions=len(focal),native_reward=reward,invalid_actions=sum(s['result']['native_invalid'] for s in focal))
                episodes.append(row)
            collection[phase]=dict(planned=len(plan['episodes']),statuses=dict(status),actions=actions)
        prediction=[]
        for size in (120,248,440):
            folder=self.study/f'prediction/n{size}';path=folder/'manifest.json'
            if not path.exists():prediction.append(dict(size=size,planned=0,complete=0,status='Awaiting training data'));continue
            manifest=read(path);complete=sum(read(p)['status']=='complete' for p in (folder/'batches').glob('*.json'))
            prediction.append(dict(size=size,planned=len(manifest['batches']),complete=complete,status='Fitted' if (folder/'models.pkl').exists() else 'Forecasts complete' if complete==len(manifest['batches']) else 'Collecting forecasts'))
        pooled=self.study/'prediction/supplemental-pooled-n440';secondary=None
        if (pooled/'manifest.json').exists():
            m=read(pooled/'manifest.json');secondary=dict(planned=len(m['batches']),complete=sum(read(p)['status']=='complete' for p in (pooled/'batches').glob('*.json')))
        result=read(self.study/'summary.json') if (self.study/'summary.json').exists() else None
        self._cache=dict(episodes=episodes,collection=collection,prediction=prediction,secondary=secondary,results=result);self._at=time.monotonic()
        return self._cache

    def summary(self,args=None):
        args=args or {};cohort=args.get('cohort',['all'])[0];family=args.get('family',[''])[0]
        snap=self.snapshot();episodes=[r for r in snap['episodes'] if (not family or r['inputs']['family_id']==family) and
            (cohort=='all' or cohort=='legacy' and not r['source_run'].startswith('v2-') or r['source_run']=='v2-'+cohort)]
        completed=[r for r in episodes if r['status']=='complete'];family_rows=[]
        for fid,f in self.catalog['families'].items():
            configs=[g for g in self.games.values() if g['family_id']==fid]
            family_rows.append(dict(id=fid,title=f['title'],category=f['category'],players=f['num_players'],information=f['information'],objective=f['objective'],
                configurations=len(configs),episodes=sum(r['inputs']['family_id']==fid for r in completed),new=fid in ('ultimatum','two_thirds','secretary','memory')))
        catalog=[dict(g,episodes=sum(r['inputs']['game_id']==g['configuration_id'] for r in completed)) for g in self.games.values() if not family or g['family_id']==family]
        models=[]
        for model in ('qwen-3.8-27b','glm'):
            rr=[r for r in completed if r['inputs']['model']==model]
            models.append(dict(model=model,episodes=len(rr),wins=sum(r['targets'].get('win')==1 for r in rr),invalid=sum(r['invalid_actions'] for r in rr),actions=sum(r['focal_actions'] for r in rr)))
        instances=[i for i in self.instances if not family or i['family_id']==family]
        return dict(counts=dict(families=len({g['family_id'] for g in catalog}),configurations=len(catalog),seeded_instances=len(instances),
            distinct_openings=len({i['opening_group'] for i in instances}),episodes=len(completed),actions=sum(r['focal_actions'] for r in completed)),
            collection=snap['collection'],prediction=snap['prediction'],secondary=snap['secondary'],results=snap['results'],families=family_rows,catalog=catalog,models=models,
            episode_lengths=dict(Counter(str(r['focal_actions']) for r in completed)),cohort=cohort,
            forecast_frozen=(self.study/'prediction/frozen.json').exists())

    def game(self,ident):
        g=self.games[ident];instances=[i for i in self.instances if i['configuration_id']==ident]
        snap=self.snapshot();episodes=[r for r in snap['episodes'] if r['inputs']['game_id']==ident]
        return dict(game=g,family=self.catalog['families'][g['family_id']],example=dict(seed=instances[0]['seed'],observations=instances[0]['opening_observations']),
            mechanics=read(self.data/'mechanics.v2.json')[g['family_id']],episodes=[{k:r[k] for k in ('episode_id','source_run','status','seed','replicate','inputs','targets','focal_actions','native_reward')} for r in episodes])

    def episode(self,ident):
        record=read(self.paths[ident]);rows_by_id={r['episode_id']:r for r in self.snapshot()['episodes']}
        return dict(id=ident,item=record['item'],status=record['status'],measurements=rows_by_id.get(ident),
            steps=[{k:s[k] for k in ('index','actor','is_focal','raw_action','result','before','after','incoming','messages') if k in s} for s in record['steps']])
