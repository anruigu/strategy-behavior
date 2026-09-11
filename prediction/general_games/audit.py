"""Independent export counts, retry provenance and ledger reconciliation."""
import argparse
from collections import Counter
import json
from pathlib import Path

from prediction.client import Ledger
from prediction.io_utils import read_json,write_json,digest,now
from .dataset import DEFAULT_RUN


def audit(run):
    run=Path(run); plan=read_json(run/'plan.json'); out=run/'export'; summary=read_json(out/'summary.json')
    rows=[json.loads(line) for line in (out/'episodes.jsonl').read_text().splitlines()]
    actions=[json.loads(line) for line in (out/'actions.jsonl').read_text().splitlines()]
    by_episode={r['episode_id']:r for r in rows}; by_action={(r['episode_id'],r['turn']):r for r in actions}
    calls={p.stem:read_json(p) for p in (run/'raw_calls').glob('*.json')}
    linked=[]; statuses=Counter(); focal_count=0; invalid_count=0; transitions=0
    for item in plan['episodes']:
        record=read_json(run/'episodes'/(item['episode_id']+'.json')); row=by_episode[item['episode_id']]
        statuses[record['status']]+=1; transitions+=len(record['steps']); local_count=0; local_invalid=0
        for step in record['steps']:
            if not step['is_focal']: continue
            target=by_action[item['episode_id'],local_count]
            assert target['target_action']==step['raw_action']
            assert target['valid']==(not step['result']['native_invalid'])
            local_count+=1; local_invalid+=step['result']['native_invalid']
            attempts=record['attempts'][str(step['index'])]
            assert len(attempts)<=plan['max_attempts_per_decision']
            assert [a['meta']['status'] for a in attempts].count('ok')==1
            for attempt in attempts:
                ident=attempt['meta']['call_id']; linked.append(ident); call=calls[ident]
                assert call['request']['messages']==step['messages']
                assert call['status']==attempt['meta']['status']
        focal_count+=local_count; invalid_count+=local_invalid
        assert row['labels']['focal_actions']==local_count
        assert row['labels']['behavior']['invalid_action_rate']==(local_invalid/local_count if local_count else None)
        reward=(record['final_state']['rewards'] or {}).get(str(item['seat'])) if record['status']=='complete' else None
        assert row['labels']['outcome']['native_reward']==reward
        assert row['labels']['outcome']['win']==(reward==1 if reward is not None else None)
        # Every unsupported exploit label remains unobserved, not a negative.
        assert row['labels']['behavior']['exploitation_rate']=={'numerator':None,'denominator':0,'value':None}
        assert row['source_plan_sha256']==digest(plan)
    # This release is complete; future incomplete runs can have pending attempt
    # records after their last submitted action. Account for those explicitly.
    for item in plan['episodes']:
        record=read_json(run/'episodes'/(item['episode_id']+'.json'))
        for key,attempts in record['attempts'].items():
            if int(key)<len(record['steps']): continue
            for attempt in attempts:
                linked.append(attempt['meta']['call_id'])
    assert len(linked)==len(set(linked)) and set(linked)==set(calls)
    assert dict(statuses)==summary['statuses']
    assert focal_count==len(actions)==summary['focal_actions']
    assert invalid_count==summary['invalid_actions']
    assert transitions==summary['audit']['replayed_transitions']
    assert summary['label_export_source_sha256']==digest(Path(__file__).with_name('export.py').read_text())
    cost=sum(c.get('budget_cost_usd') or 0 for c in calls.values())
    assert abs(cost-summary['usage']['reported_cost_usd'])<1e-9
    ledgers={name:Ledger(run/name,plan['budget_usd']).summary() for name in ('budget.sqlite','stage-budget.sqlite')}
    for ledger in ledgers.values():
        assert abs(cost-ledger['reported_usd'])<1e-9
        assert sum(x['calls'] for x in ledger['states'].values())==len(calls)
    comparison=[json.loads(line) for line in (out/'comparison-episodes.jsonl').read_text().splitlines()]
    assert sum(r['dataset']=='general_textarena' for r in comparison)==statuses['complete']
    result=dict(created=now(),audit_source_sha256=digest(Path(__file__).read_text()),status='passed',episodes=len(rows),
        focal_actions=focal_count,native_invalid_actions=invalid_count,replayed_transitions=transitions,
        reconciled_attempt_calls=len(linked),reported_cost_usd=cost,ledgers=ledgers,
        comparison_rows=Counter(r['dataset'] for r in comparison),
        artifact_hashes={name:digest((out/name).read_text()) for name in ('episodes.jsonl','actions.jsonl','comparison-episodes.jsonl','REPORT.md','summary.json')})
    write_json(out/'audit.json',result); return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--run',type=Path,default=DEFAULT_RUN); args=parser.parse_args()
    print(json.dumps(audit(args.run),indent=2))
