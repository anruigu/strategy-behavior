"""Read-only live view of the fixed-budget breadth experiment."""
from collections import Counter
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2]/'general_games/breadth_v3'


def read(path): return json.loads(path.read_text())


class BreadthDataset:
    def __init__(self,root=ROOT):
        self.root=Path(root); self.data=self.root/'data'; self.study=self.root/'study'
        self.catalog=read(self.data/'catalog.json'); self.games={g['configuration_id']:g for g in self.catalog['configurations']}
        self.protocol=read(self.study/'protocol.json'); self.plans={p:read(self.study/p/'plan.json') for p in ('training','test')}
        self.items={e['episode_id']:(p,e) for p,plan in self.plans.items() for e in plan['episodes']}; self.cache={}; self.at=0; self.snapshot_cache=None

    def snapshot(self):
        if self.snapshot_cache is not None and time.monotonic()-self.at<10: return self.snapshot_cache
        exported={}
        for phase in self.plans:
            path=self.study/phase/'export/episodes.jsonl'
            if path.exists(): exported.update({r['episode_id']:r for r in map(json.loads,path.read_text().splitlines())})
        rows=[]; progress={}
        for phase,plan in self.plans.items():
            statuses=Counter(); actions=0
            for item in plan['episodes']:
                eid=item['episode_id']; path=self.study/phase/'episodes'/(eid+'.json')
                if not path.exists(): statuses['not_started']+=1; continue
                mtime=path.stat().st_mtime_ns
                if eid not in self.cache or self.cache[eid][0]!=mtime:
                    trace=read(path); focal=[s for s in trace['steps'] if s['is_focal']]
                    row=dict(episode_id=eid,status=trace['status'],phase=phase,arms=item['arms'],family=item['game']['family_id'],
                        model=item['model'],seat=item['seat'],seed=item['seed'],replicate=item['replicate'],
                        actions=len(focal),invalid=sum(s['result']['native_invalid'] for s in focal),targets=None)
                    self.cache[eid]=(mtime,row)
                row=dict(self.cache[eid][1]); row['targets']=exported.get(eid,{}).get('targets')
                rows.append(row); statuses[row['status']]+=1; actions+=row['actions']
            progress[phase]=dict(planned=len(plan['episodes']),statuses=dict(statuses),actions=actions)
        prediction=[]
        for arm in ('depth','breadth'):
            folder=self.study/'prediction'/arm
            if (folder/'manifest.json').exists():
                m=read(folder/'manifest.json'); done=sum(read(p)['status']=='complete' for p in (folder/'batches').glob('*.json'))
                prediction.append(dict(arm=arm,planned=len(m['batches']),complete=done,fitted=(folder/'models.pkl').exists()))
            else: prediction.append(dict(arm=arm,planned=0,complete=0,fitted=False))
        result=read(self.study/'summary.json') if (self.study/'summary.json').exists() else None
        self.snapshot_cache=dict(rows=rows,progress=progress,prediction=prediction,results=result); self.at=time.monotonic()
        return self.snapshot_cache

    def summary(self,args=None):
        args=args or {}; cohort=args.get('cohort',['all'])[0]; family=args.get('family',[''])[0]; snap=self.snapshot()
        def included(item):
            phase=item.get('phase',item.get('suite'))
            return cohort=='all' or cohort=='test' and phase=='test' or cohort in item['arms']
        rows=[r for r in snap['rows'] if included(r) and (not family or r['family']==family)]
        complete=[r for r in rows if r['status']=='complete']; planned=[e for _,e in self.items.values() if included(e) and (not family or e['game']['family_id']==family)]
        families=[]
        for fid,f in self.catalog['families'].items():
            if family and family!=fid: continue
            members=[e for e in planned if e['game']['family_id']==fid]
            if cohort!='all' and not members: continue
            families.append(dict(id=fid,title=f['title'],players=f['num_players'],category=f['category'],information=f['information'],objective=f['objective'],
                role='Holdout' if fid in self.protocol['test_families'] else 'Both training arms' if fid in self.protocol['arms']['depth']['families'] else 'Breadth training only',
                planned=len(members),complete=sum(r['family']==fid for r in complete),game_id=next(g['configuration_id'] for g in self.games.values() if g['family_id']==fid)))
        models=[]
        for model in ('qwen-3.8-27b','glm'):
            rr=[r for r in complete if r['model']==model]
            models.append(dict(model=model,episodes=len(rr),actions=sum(r['actions'] for r in rr),invalid_actions=sum(r['invalid'] for r in rr)))
        return dict(cohort=cohort,counts=dict(families=len(families),planned=len(planned),complete=len(complete),actions=sum(r['actions'] for r in complete)),families=families,models=models,
            lengths=dict(Counter(str(r['actions']) for r in complete)),progress=snap['progress'],prediction=snap['prediction'],results=snap['results'],
            frozen=(self.study/'prediction/frozen.json').exists(),protocol=self.protocol)

    def game(self,ident):
        g=self.games[ident]; fid=g['family_id']; instances=[i for i in read(self.data/'instances.evaluator.json') if i['configuration_id']==ident]
        spec=self.study/'prediction/depth/mechanics.json'
        if not spec.exists(): spec=self.data/'mechanics.json'
        return dict(game=g,family=self.catalog['families'][fid],mechanics=read(spec)[fid],
            opening=dict(seed=instances[0]['seed'],observations=instances[0]['opening_observations']),
            episodes=[r for r in self.snapshot()['rows'] if r['family']==fid])

    def episode(self,ident):
        phase,item=self.items[ident]; trace=read(self.study/phase/'episodes'/(ident+'.json'))
        return dict(id=ident,item=item,status=trace['status'],steps=[{k:s[k] for k in ('index','actor','is_focal','raw_action','result','before','after','incoming','messages') if k in s} for s in trace['steps']])
