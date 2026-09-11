"""Auditable bounded recovery of actor calls that produced no usable action."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse
import multiprocessing
from pathlib import Path
from prediction.io_utils import read_json,write_json,digest,now
from . import ROOT,STUDY
from .runtime import replay,messages
from .api import Client,ModelConfig,Ledger
from .collection import run_episode

ELIGIBLE={'invalid_response','truncated','transport_error'}


def specify():
    path=STUDY/'recovery-policy.json'
    assert not path.exists() and not list((STUDY/'prediction').glob('*/manifest.json'))
    value=dict(specified_at=now(),source_sha256=digest(Path(__file__).read_text()),max_total_attempts_per_decision=6,
        eligible_statuses=sorted(ELIGIBLE),trigger='One training Wordle checkpoint returned three blank responses before any predictor requests or holdout actor calls.',
        rule='Applies uniformly to both arms and test: after the original three-call allowance is exhausted by transport/empty/truncated responses, make at most three additional identical-context calls. Preserve all attempts, first-failure checkpoints and billing. Never extract reasoning as an action, modify an actor prompt, replace an episode, or call an incomplete native trajectory a loss. Explicit provider refusals are not eligible.',
        original_protocol_sha256=digest(read_json(STUDY/'protocol.json')),global_budget_usd=60,
        scope='Actor inference recovery only. Original collection source and plans stay archived and unchanged. Predictor calibration and fit settings are unchanged.')
    write_json(path,value); return value


def recover_episode(phase,item):
    policy=read_json(STUDY/'recovery-policy.json'); assert policy['source_sha256']==digest(Path(__file__).read_text())
    plan=read_json(STUDY/phase/'plan.json'); folder=STUDY/phase; path=folder/'episodes'/(item['episode_id']+'.json')
    for _ in range(plan['max_focal_actions']):
        record=read_json(path)
        if record['status']=='complete': return item['episode_id'],'complete'
        if record.get('failure_reason')!='inference_attempts_exhausted': return item['episode_id'],record['status']
        index=len(record['steps']); attempts=record['attempts'][str(index)]
        if any(a['meta']['status'] not in ELIGIBLE for a in attempts): return item['episode_id'],'not_eligible'
        archive=STUDY/'recovery'/phase/f"{item['episode_id']}-step-{index}-original.json"
        if not archive.exists(): write_json(archive,record)
        s=replay(item,record,folder/'raw_calls'); actor,_,h=s.observe(); assert actor==item['seat']
        prompt=messages(item['game'],h,item['condition'])
        original=read_json(folder/'raw_calls'/(attempts[0]['meta']['call_id']+'.json')); assert original['request']['messages']==prompt
        client=Client(ModelConfig(**plan['models'][item['model']]),folder/'raw_calls',Ledger(STUDY/'budget.sqlite',60),Ledger(folder/'budget.sqlite',40),max_tokens=plan['max_tokens'])
        record['recovery_policy_sha256']=digest(policy); usable=False
        while len(attempts)<policy['max_total_attempts_per_decision']:
            raw,meta=client.generate(prompt,purpose=item['episode_id']+f'/step-{index}/bounded-recovery')
            attempts.append(dict(raw=raw,meta=meta,recovery=True)); write_json(path,record)
            if meta['status']=='ok': usable=True; break
            if meta['status'] not in ELIGIBLE: break
        if not usable: return item['episode_id'],'recovery_exhausted'
        # The unchanged collector reuses the already recorded successful call
        # and replays the same prefix before executing the next native action.
        result=run_episode(phase,item)
        if result[1]!='incomplete': return result[:2]
    return item['episode_id'],'recovery_limit'


def recover(phase,workers=4):
    policy=read_json(STUDY/'recovery-policy.json')
    assert policy['source_sha256']==digest(Path(__file__).read_text())
    if phase=='test':
        frozen=read_json(STUDY/'prediction/frozen.json'); assert frozen['recovery_policy_sha256']==digest(policy)
    selected=[]
    for item in read_json(STUDY/phase/'plan.json')['episodes']:
        path=STUDY/phase/'episodes'/(item['episode_id']+'.json')
        if path.exists() and read_json(path)['status']=='incomplete': selected.append(item)
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn')) as pool:
        futures=[pool.submit(recover_episode,phase,item) for item in selected]
        for f in as_completed(futures): print('recovery',phase,*f.result(),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['specify','recover']); p.add_argument('--phase',choices=['training','test'],default='training'); p.add_argument('--workers',type=int,default=4); a=p.parse_args()
    if a.action=='specify': print(specify())
    else: recover(a.phase,a.workers)
