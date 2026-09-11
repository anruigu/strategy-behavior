"""Independent plan/trace/aggregate consistency checks for the completed screen."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from benchmark.clients import write_json


def verify(out):
    plan = json.loads((out/'plan.json').read_text())
    report = json.loads((out/'report.json').read_text())
    status = json.loads((out/'status.json').read_text())
    issues = []
    checks = 0
    def check(value, detail):
        nonlocal checks
        checks += 1
        if not value:
            issues.append(detail)
    for relative, digest in plan['source_hashes'].items():
        check(hashlib.sha256((out/'source'/relative).read_bytes()).hexdigest() == digest, 'snapshot hash: ' + relative)
    check(len(plan['tasks']) == 768, 'main schedule size')
    check(len({r['id'] for r in plan['tasks']}) == 768, 'unique tasks')
    states = Counter()
    models = Counter()
    complete = 0
    for task in plan['tasks']:
        row = json.loads((out/'episodes'/task['id']/'trace.json').read_text())
        check(row['task'] == task, 'task mismatch: ' + task['id'])
        states[row['status']] += 1
        if row.get('recovery'):
            previous = json.loads((out/'episodes'/task['id']/'previous-attempts'/'0001.json').read_text())
            count = len(previous['decisions'])
            check(row['decisions'][:count] == previous['decisions'], 'recovery changed saved replies: ' + task['id'])
            check(row['recovery']['replayed_decisions'] == count, 'incomplete prefix replay: ' + task['id'])
        if row['status'] != 'complete':
            continue
        complete += 1
        ep = row['episode']
        check(ep['game'] == task['game'] and ep['seed'] == task['seed'] and ep['arm'] == task['arm'], 'episode identity: ' + task['id'])
        accepted = [d for d in row['decisions'] if not d.get('format_error')]
        check(len(accepted) == sum(ep['decisions'].values()), 'decision count: ' + task['id'])
        engine = [d for event in ep['extras']['events'] for d in event['decisions']]
        check([(d['pid'], d['observation'], d['reply']) for d in accepted] ==
              [(d['pid'], d['observation'], d['reply']) for d in engine], 'accepted/engine alignment: ' + task['id'])
        final = ep['extras']['events'][-1]['after']['scores']
        check(all(abs(ep['scores'][str(p)]-value) < 1e-8 for p, value in enumerate(final)), 'final score: ' + task['id'])
        for d in row['decisions']:
            model = task['focal'] if d['pid'] == 0 else task['opponent']
            models[model] += 1
            check(d['metadata']['actual_model'] == plan['models'][model]['provider_model'], 'actual model: ' + task['id'])
            call = out/'episodes'/task['id']/'calls'/(d['metadata']['call_id']+'.json')
            check(call.exists(), 'missing raw call: ' + task['id'])
    check(dict(states) == report['outcomes'], 'report/status counts')
    check(dict(states) == status['outcomes'], 'status/trace counts')
    check(status['status'].startswith('finished'), 'campaign has not finished')
    check(sum(c['complete'] for c in report['cells']) == complete, 'cell denominators')
    check(sum(g['planned_pairs'] for g in report['games']) == 320, 'planned ordinary/nerfed pairs')
    check(len(report['episodes']) == 768, 'report task count')
    result = dict(checks=checks, passed=not issues, issues=issues, outcomes=dict(states),
                  completed_episodes=complete, logged_submissions_by_model=dict(models))
    write_json(out/'verification.json', result)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    result = verify(a.out)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
