"""Secondary input-only control: pool labels for identical visible examples."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from copy import deepcopy
from pathlib import Path
import json
from prediction.io_utils import read_json,write_json,digest,now
from prediction.client import Client,ModelConfig,Ledger
from . import DATA,STUDY
from .labels import TARGETS
from .predict import OUT,prompt,retrieve,generate_batch,request_size,parse

FOLDER=OUT/'supplemental-pooled-n440'


def pool_visible(groups):
    by_input=defaultdict(list)
    for row in groups:by_input[digest(row['inputs'])].append(row)
    result=[]
    for rr in by_input.values():
        # Preserve the original deterministic retrieval winner/ID. Only its
        # observed means and counts change; examples and their order do not.
        rr=sorted(rr,key=lambda r:r['id']);row=deepcopy(rr[0])
        assert all(r['supported']==row['supported'] for r in rr)
        for t in TARGETS:
            n=sum(r['target_counts'][t] for r in rr)
            row['targets'][t]=sum(r['targets'][t]*r['target_counts'][t] for r in rr if r['targets'][t] is not None)/n if n else None
            row['target_counts'][t]=n
        row['n']=sum(r['n'] for r in rr);row['episodes']=sum([r['episodes'] for r in rr],[])
        row['pooled_condition_ids']=[r['id'] for r in rr];result.append(row)
    return sorted(result,key=lambda r:r['id'])


def prepare():
    assert not (FOLDER/'manifest.json').exists()
    parent=read_json(OUT/'n440/manifest.json');groups=read_json(OUT/'n440/groups.evaluator.json');pool=pool_visible(groups)
    queries={q['id']:q for q in parent['queries']};specs=read_json(DATA/'mechanics.v2.json');batches=[]
    assert not {r['opening_group'] for r in groups}&{q['opening_group'] for q in queries.values()}
    assert not {digest(r['inputs']) for r in pool}&{digest(q['inputs']) for q in queries.values()}
    for q in queries.values():
        for shots in (4,8,16):assert [r['id'] for r in retrieve(q,groups,shots)]==[r['id'] for r in retrieve(q,pool,shots)]
    for b in parent['batches']:
        if b['kind']!='test':continue
        batch=deepcopy(b);messages,ids=prompt([queries[q['id']] for q in b['queries']],pool,specs,b['shots'],'test')
        assert ids==b['example_ids'] and request_size(messages)<=40000
        batch.update(messages=messages,example_ids=ids);batch.pop('id');batch['id']='pooled-'+digest(batch)[:20];batches.append(batch)
    m=dict(created=now(),source_sha256=digest(Path(__file__).read_text()),parent_source_sha256=parent['source_sha256'],
        parent_manifest_sha256=digest(parent),training_groups_sha256=digest(groups),pooled_groups_sha256=digest(pool),specification_sha256=digest(specs),
        predictor=parent['predictor'],max_tokens=parent['max_tokens'],max_attempts=3,queries=parent['queries'],batches=batches,
        timing='secondary control specified after test play began; inputs and training labels only; not part of the prospective primary comparison',
        change='Exact same nested demonstration IDs/order as original n440. Means/counts pool all training conditions with identical full visible inputs. No test outcomes are read or used.',
        original_conditions=len(groups),distinct_visible_inputs=len(pool),training_episodes=sum(r['n'] for r in pool))
    write_json(FOLDER/'groups.evaluator.json',pool);write_json(FOLDER/'manifest.json',m)
    return dict(batches=len(batches),conditions=len(groups),visible_inputs=len(pool))


def collect(workers=4):
    m=read_json(FOLDER/'manifest.json');assert m['source_sha256']==digest(Path(__file__).read_text())
    client=Client(ModelConfig(**m['predictor']),FOLDER/'raw_calls',Ledger(STUDY/'budget.sqlite',75),Ledger(OUT/'budget.sqlite',50),max_tokens=m['max_tokens'])
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(generate_batch,FOLDER,b,client,m['max_attempts']) for b in m['batches']]
        for i,f in enumerate(as_completed(futures),1):print('pooled',i,len(futures),f.result(),flush=True)


def export():
    m=read_json(FOLDER/'manifest.json');result=[];query={q['id']:q for q in m['queries']};calls=[]
    assert m['source_sha256']==digest(Path(__file__).read_text())
    assert m['parent_manifest_sha256']==digest(read_json(OUT/'n440/manifest.json'))
    assert m['pooled_groups_sha256']==digest(read_json(FOLDER/'groups.evaluator.json'))
    for batch in m['batches']:
        r=read_json(FOLDER/'batches'/(batch['id']+'.json'));assert r['status']=='complete'
        assert parse(r['attempts'][-1]['raw'],batch)==r['predictions']
        for a in r['attempts']:
            call=read_json(FOLDER/'raw_calls'/(a['meta']['call_id']+'.json'));calls.append(call['call_id'])
            assert call['request']['messages']==batch['messages'] and call['config']==m['predictor']
            assert call['status']==a['meta']['status'] and call['request']['max_tokens']==m['max_tokens']
            if call['status']=='ok':assert call['response']['choices'][0]['message']['content']==a['raw']
        for ident,values in r['predictions'].items():result.append(dict(size=440,query_id=ident,suite=query[ident]['suite'],method='pooled_few_'+str(batch['shots']),forecast=values,timing='secondary_after_test_started'))
    assert len(result)==264 and len(calls)==len(set(calls))
    assert set(calls)=={p.stem for p in (FOLDER/'raw_calls').glob('*.json')}
    write_json(FOLDER/'test-predictions.json',result)
    write_json(FOLDER/'audit.json',dict(created=now(),calls=len(calls),predictions=len(result),same_example_ids_and_order=True,timing=m['timing'],source_sha256=m['source_sha256']))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','collect','export']);parser.add_argument('--workers',type=int,default=4);args=parser.parse_args()
    if args.action=='prepare':print(prepare())
    elif args.action=='collect':collect(args.workers)
    else:print('Exported',len(export()))
