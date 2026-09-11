"""Audit raw requests, private histories, checkpoint integrity, and aggregates."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import statistics

from benchmark.clients import write_json
from benchmark.v3_ma.reflection import digest, history_block, final_observation, GAMES


def live_final_observation(trace):
    """Restore engine seat keys before reproducing a live final observation."""
    game = GAMES[trace['task']['game']]
    state = deepcopy(trace['episode']['extras']['events'][-1]['after'])
    if 'inbox' in state:
        state['inbox'] = {int(pid): messages for pid, messages in state['inbox'].items()}
    return game.observe(state, 0, game.STAGES[-1], trace['task']['arm'])


def verify(out, complete_only=False):
    plan = json.loads((out/'plan.json').read_text())
    report = json.loads((out/'report.json').read_text())
    report_rows = {r['id']: r for r in report['episodes']}
    tasks = {t['id']: t for t in plan['tasks']}
    issues, checks = [], 0
    def check(ok, detail):
        nonlocal checks
        checks += 1
        if not ok:
            issues.append(detail)
    def read(path):
        return json.loads(path.read_text())
    check(len(tasks) == 896 and len(plan['chains']) == 256, 'schedule size')
    amendment_path = out/'transport-amendment.json'
    if amendment_path.exists():
        amendment = read(amendment_path)
        check(hashlib.sha256((out/'plan.json').read_bytes()).hexdigest() == amendment['plan_sha256'], 'transport amendment changed the frozen plan')
        check(hashlib.sha256((out/amendment['source_file']).read_bytes()).hexdigest() == amendment['source_sha256'], 'transport amendment source')
        check(amendment['recovery_timeout_seconds'] == 600 and amendment['workers'] == 24, 'recovery transport settings')
    for relative, sha in plan['source_hashes'].items():
        check(hashlib.sha256((out/'source'/relative).read_bytes()).hexdigest() == sha, 'source snapshot '+relative)
    for ref in plan['baselines']:
        original = Path(ref['path'])
        check(hashlib.sha256(original.read_bytes()).hexdigest() == ref['sha256'], 'baseline source '+ref['id'])
        copied = read(out/'episodes'/ref['id']/'trace.json')
        source = read(original)
        check(copied['decisions'] == source['decisions'] and copied['episode'] == source['episode'], 'shared baseline changed '+ref['id'])
        last = [d for d in source['decisions'] if d['pid'] == 0][-1]
        call = read(original.parent/'calls'/(last['metadata']['call_id']+'.json'))
        visible = call['request']['messages'][1:] + [dict(role='assistant',content=last['reply'])]
        expected = history_block(visible, final_observation(copied), 1)
        check(copied['focal_history'] == expected, 'baseline focal history altered '+ref['id'])
    seen_notes, submissions = set(), Counter()
    traces = {}
    for chain in plan['chains']:
        if complete_only and report_rows[chain['episodes'][-1]]['status'] != 'complete':
            continue
        base = read(out/'episodes'/chain['baseline_id']/'trace.json')
        history = deepcopy(base['focal_history'])
        for eid in chain['episodes']:
            task = tasks[eid]
            if chain['learning_arm'] == 'reflection':
                folder = out/'chains'/chain['id']/f'after-play-{task["iteration"]-1}'
                if not (folder/'reflection.json').exists():
                    check(not (out/'episodes'/eid/'trace.json').exists(), 'play without reflection '+eid)
                    break
                note = read(folder/'reflection.json')
                expected = [dict(role='system',content=plan['reflection_system']), *history,
                            dict(role='user',content=plan['reflection_request'])]
                check(digest(expected) == note['context_sha256'], 'reflection history mismatch '+eid)
                call = read(folder/'calls'/(note['metadata']['call_id']+'.json'))
                check(call['request']['messages'] == expected, 'raw reflection has extra/missing context '+eid)
                check(note['metadata']['actual_model'] == plan['models'][task['focal']]['provider_model'], 'reflection model '+eid)
                seen_notes.add(str(folder))
                history.extend([dict(role='user',content=note['request']),dict(role='assistant',content=note['reply'])])
            path = out/'episodes'/eid/'trace.json'
            if not path.exists():
                break
            trace = read(path)
            traces[eid] = trace
            check(trace['task'] == task and trace['memory_sha256'] == digest(history), 'task/memory mismatch '+eid)
            start = dict(role='user',content=f'BEGIN NEW PLAY {task["iteration"]} of 4. The game has reset. '
                         'Other players have fresh contexts. Use your previous experience and play to maximize your score.')
            per_seat = {int(p): deepcopy(history)+[start] if int(p)==0 else [] for p in trace['systems']}
            for d in trace['decisions']:
                pid = d['pid']
                config = plan['models'][task['focal'] if pid == 0 else task['opponent']]
                call = read(path.parent/'calls'/(d['metadata']['call_id']+'.json'))
                messages = call['request']['messages']
                check(messages[0] == dict(role='system',content=trace['systems'][str(pid)]), 'private system mismatch '+eid)
                check(messages[1:-1] == per_seat[pid], 'cross-seat or cross-play context leak '+eid)
                check(digest(messages) == d['request_sha256'], 'checkpoint request hash '+eid)
                if d['correction_attempt'] == 0:
                    check(messages[-1] == dict(role='user',content=d['observation']), 'observation mismatch '+eid)
                else:
                    check(messages[-1]['content'].startswith('Your submission was not accepted: '), 'nonneutral correction '+eid)
                check(d['metadata']['actual_model'] == config['provider_model'] == call['request']['model'], 'actual model '+eid)
                table = json.JSONDecoder().raw_decode(d['observation'].split('\nTable: ',1)[1])[0]
                check(table['seat'] == pid, 'observation shown to wrong seat '+eid)
                per_seat[pid].extend([messages[-1],dict(role='assistant',content=d['reply'])])
                submissions[config['model_id']] += 1
            for previous in (path.parent/'previous-attempts').glob('*.json'):
                old = read(previous)
                check(trace['decisions'][:len(old['decisions'])] == old['decisions'], 'recovery changed an earlier reply '+eid)
            if trace['status'] != 'complete':
                break
            ep = trace['episode']
            check(ep['seed'] == (1 if task['iteration']==4 else 0), 'wrong continuation seed '+eid)
            accepted = [d for d in trace['decisions'] if not d.get('format_error')]
            events = [d for e in ep['extras']['events'] for d in e['decisions']]
            check([(d['pid'],d['observation'],d['reply']) for d in accepted] ==
                  [(d['pid'],d['observation'],d['reply']) for d in events], 'engine/accepted decisions '+eid)
            check([ep['scores'][str(p)] for p in range(ep['n_players'])] == ep['extras']['events'][-1]['after']['scores'], 'final scores '+eid)
            check(trace['final_observation'] == live_final_observation(trace), 'final focal observation '+eid)
            block = history_block(per_seat[0][len(history)+1:],trace['final_observation'],task['iteration'])
            check(block == trace['focal_history'], 'outgoing history includes extra material '+eid)
            history.extend(trace['focal_history'])
    report_new = {r['id']:r for r in report['episodes'] if r['iteration']>1}
    for eid, trace in traces.items():
        check(report_new[eid]['status'] == trace['status'], 'report completion '+eid)
        if trace['status'] == 'complete':
            check(report_new[eid]['focal_score'] == trace['episode']['scores']['0'], 'report score '+eid)
    for summary in report['summaries']:
        pairs = [r for r in report['paired_reflection'] if r['complete'] and
                 all(r[k] == summary[k] for k in ('game','condition','iteration'))]
        check(len(pairs) == summary['complete_pairs'], 'paired denominator '+str(summary))
        if pairs:
            check(abs(statistics.mean(r['score_delta'] for r in pairs)-summary['mean_score_delta']) < 1e-9, 'paired payoff '+str(summary))
    result = dict(passed=not issues, checks=checks, issues=issues, complete_chains_only=complete_only,
                  new_traces_checked=len(traces),
                  reflection_notes_checked=len(seen_notes), submissions_by_model=dict(submissions), outcomes=report['new_outcomes'],
                  serialization_note='Council inbox keys become strings in JSON. The audit restores integer seat keys for live final observations. '
                  'The reused baseline wrapper omits that duplicate inbox, but its exact original final action request retains the messages in both branches.')
    write_json(out/('verification.partial.json' if complete_only else 'verification.json'),result)
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--complete-only',action='store_true');args=p.parse_args()
    result=verify(args.out,args.complete_only);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
