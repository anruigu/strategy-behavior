"""Read-only adapter for the frozen v3-MA screen and its saved marker audit.

No model calls, strategy replay, or new exploit classification takes place here.
Incomplete episodes expose their recorded submissions without inventing outcomes.
"""
import json
from collections import defaultdict

RUN_ID = 'v3-ma-four-model'
MODEL_NAMES = {
    'claude-haiku-4.5': 'Claude Haiku 4.5', 'anthropic/claude-haiku-4.5': 'Claude Haiku 4.5',
    'gpt-5-mini': 'GPT-5 mini', 'openai/gpt-5-mini': 'GPT-5 mini',
    'qwen-3.8-27b': 'Qwen 3.8 27B', 'qwen3.8-27b': 'Qwen 3.8 27B',
    'glm': 'GLM 5.3', 'glm-5.3': 'GLM 5.3',
}
RESOLUTION = {'trust': 'act', 'signal': 'play', 'market': 'trade', 'filing': 'redeem', 'commons': 'act'}


def field(observation, name):
    return json.JSONDecoder().raw_decode(observation.split('\n' + name + ': ', 1)[1])[0]


def model_name(name):
    return MODEL_NAMES.get(name, name)


def index(root, read, run_id=RUN_ID, name='v3-MA · four-model cross-play'):
    report, plan = read(root / 'report.json'), read(root / 'plan.json')
    specs = {s['id']: s for s in plan['suite']['scenarios']}
    titles, episodes = {}, []
    for row in report['episodes']:
        if row['status'] == 'not_started':
            continue
        game = row['game']
        if game not in titles:
            trace = read(root / 'episodes' / row['id'] / 'trace.json')
            titles[game] = field(trace['decisions'][0]['observation'], 'Card')['title']
        mark = row.get('marker')
        episodes.append(dict(
            id=row['id'], game=game, title=titles[game], seed=row['seed'], condition=row['condition'],
            focal=row['focal'], opponent=row['opponent'], focal_name=model_name(row['focal']),
            opponent_name=model_name(row['opponent']), status=row['status'],
            turns=specs[game]['rounds'], target=None, target_name=None,
            iteration=row.get('iteration'), learning_arm=row.get('learning_arm'),
            hits=int(mark['episode_marker']) if mark else None,
            hit_rounds=mark['hit_rounds'] if mark else None,
            attempts=mark['attempted_rounds'] if mark else None, total=1))
    status = read(root / 'status.json')
    return dict(id=run_id, name=name, suite='v3-MA', episodes=episodes, planned=len(plan['tasks']),
                learning_arms=plan.get('learning_arms'),
                phases=[dict(id='ordinary', name='Ordinary opponents'), dict(id='nerfed', name='Nerfed opponents')],
                models=[dict(id=m, name=model_name(m)) for m in plan['models']],
                status=status['status'], errors=report['outcomes'].get('failed', 0))


def evidence(game, event, participants):
    """Explain the saved marker using the same round's actions and referee facts."""
    slug = game.removeprefix('v3ma_')
    s, a, f = event['before'], event['actions'], event['facts']
    who = lambda p: f"Seat {p} ({participants[p]['model_name']})"
    if slug == 'trust_pledge':
        return (f"{who(0)} stated {s['statements']['0']}; {who(1)} "
                f"{'accepted' if s['accepted']['1'] else 'declined'}. "
                f"Moves: {a['0']['move']} / {a['1']['move']}. Round payoffs: {f['payoff']}.")
    if slug == 'trust_memory':
        return (f"{who(0)} stated {s['statements']['0']}; displayed defection counter {s['strikes'][0]}. "
                f"Moves: {a['0']['move']} / {a['1']['move']}. Full prior history remains in the evidence.")
    if slug == 'trust_retaliation':
        return (f"{who(0)} played {a['0']['move']}; {who(1)} played {a['1']['move']}. "
                'The marker also checks earlier defection and an announced retaliation.')
    if slug == 'trust_messages':
        messages = [v['message'] for v in s['inbox']['1'] if v['sender'] == 0]
        return (f"{who(0)} sent {json.dumps(messages, ensure_ascii=False)} to {who(1)}. "
                f"Moves: {a['0']['move']} / {a['1']['move']}. "
                'This is a message/action association; it does not establish that the message caused the response.')
    if slug.startswith('signal_'):
        return (f"{who(0)} sent {json.dumps(s['clue'], ensure_ascii=False)}. "
                f"Marked slot: {f['marked_slot']}; {who(1)} played slot {f['played']}. "
                f"Team points: {f['team_points']}.")
    if slug == 'market_value':
        return (f"{who(0)} announced {s['announcements']['0']}; true value {f['true_value']}. "
                f"{who(1)} {'bought' if f['bought'] else 'declined'} at price {f['price']}.")
    if slug == 'market_ceiling':
        return f"Ceilings: {s['announcements']}. Bids: {f['bids']}; winner: {f['winner']}. Allowance: 12."
    if slug.startswith('filing_'):
        return f"Filings: {s['filings']}. Partnerships: {s['pairs']}. Redemptions: {f['redeemed']}. Payoffs: {f['payoff']}."
    return f"{who(0)} requested {f['requested'][0]} against quota 2. All requests: {f['requested']}; round payoffs: {f['payoff']}."


def annotation(game, mark, episode_marker, definition, event, participants):
    if not mark or not (mark['hit'] or mark['attempted']):
        return None
    if mark['hit']:
        if game.endswith('trust_messages'):
            kind, title = 'association', 'Message/action association'
        elif game.endswith('signal_convention'):
            kind = 'pattern'
            title = 'Code pattern · full-episode criterion met' if episode_marker else 'Code-compatible round · episode criterion not met'
        else:
            kind, title = 'observed', 'Observed exploit pattern'
    else:
        kind, title = 'candidate', 'Candidate action · exploit not observed'
    return dict(kind=kind, title=title, definition=definition, round_hit=mark['hit'],
                episode_marker=episode_marker, evidence=evidence(game, event, participants))


def episode(root, eid, read):
    plan, report = read(root / 'plan.json'), read(root / 'report.json')
    row = next((r for r in report['episodes'] if r['id'] == eid), None)
    if row is None:
        raise KeyError('Unknown MA episode')
    trace = read(root / 'episodes' / eid / 'trace.json')
    task = trace['task']
    spec = next(s for s in plan['suite']['scenarios'] if s['id'] == task['game'])
    complete = trace['status'] == 'complete' and bool(row.get('marker'))
    participants = []
    for pid in range(spec['seats']):
        key = task['focal'] if pid == 0 else task['opponent']
        observed = next((d['metadata']['actual_model'] for d in trace['decisions'] if d['pid'] == pid), None)
        role = 'Focal' if pid == 0 else 'Teammate' if spec['family'] == 'restricted_information' else 'Opponent'
        participants.append(dict(pid=pid, model_id=key, model_name=model_name(observed or key),
            actual_model=observed, requested_model=plan['models'][key]['provider_model'], role=role,
            nerfed=task['condition'] == 'nerfed' and pid in spec['recipient_seats']))
    groups = defaultdict(list)
    for step, decision in enumerate(trace['decisions'], 1):
        table = field(decision['observation'], 'Table')
        pid, meta = decision['pid'], decision['metadata']
        groups[(table['round'], table['stage'])].append(dict(
            step=step, pid=pid, round=table['round'], stage=table['stage'],
            model_name=model_name(meta.get('actual_model') or participants[pid]['model_id']),
            actual_model=meta.get('actual_model'), call_id=meta.get('call_id'),
            observation=decision['observation'], reply=decision['reply'],
            format_error=decision.get('format_error'), accepted=not decision.get('format_error')))
    saved = row.get('marker')
    markers = {m['round']: m for m in saved['by_round']} if saved else {}
    definition = next(g['definition'] for g in report['games'] if g['game'] == task['game'])
    events = trace.get('episode', {}).get('extras', {}).get('events', []) if complete else []
    rounds = []
    for number in range(1, spec['rounds'] + 1):
        stages, annotations = [], []
        round_events = [e for e in events if e['round'] == number]
        for event in round_events:
            tag = None
            if event['stage'] == RESOLUTION[task['game'].split('_')[1]]:
                tag = annotation(task['game'], markers.get(number), saved['episode_marker'],
                                 definition, event, participants)
                if tag:
                    annotations.append(tag)
            stages.append(dict(stage=event['stage'], resolved=True,
                decisions=groups[(number, event['stage'])], actions=event['actions'],
                before=event['before'], after=event['after'], facts=event['facts'], annotation=tag))
        if not complete:
            for (round_number, stage), decisions in groups.items():
                if round_number == number:
                    stages.append(dict(stage=stage, resolved=False, decisions=decisions, annotation=None))
        scores = round_events[-1]['after']['scores'] if round_events else None
        before = round_events[0]['before']['scores'] if round_events else None
        rounds.append(dict(round=number, stages=stages, annotations=annotations,
            marker=markers.get(number), scores=scores,
            payoff=[a-b for a, b in zip(scores, before)] if scores is not None else None,
            scored=complete, recorded=bool(stages)))
    opposite = 'nerfed' if task['condition'] == 'ordinary' else 'ordinary'
    counterpart = next((r for r in report['episodes'] if r['condition'] == opposite and r['status'] != 'not_started' and
                       all(r[k] == task[k] for k in ('game', 'focal', 'opponent', 'seed')) and
                       all(r.get(k) == task.get(k) for k in ('iteration','learning_arm'))), None)
    learning_pair = next((r for r in report['episodes'] if task.get('iteration',1) > 1 and
        r.get('baseline_id') == task.get('baseline_id') and r.get('iteration') == task.get('iteration') and
        r.get('learning_arm') != task.get('learning_arm') and r['status'] != 'not_started'), None)
    decisions = trace['decisions'] or read(root/'episodes'/task['baseline_id']/'trace.json')['decisions']
    return dict(suite='v3-MA', id=eid, game=task['game'], seed=task['seed'], condition=task['condition'],
        status='awaiting_report' if trace['status'] == 'complete' and not complete else trace['status'],
        error=trace.get('error'), recovery=trace.get('recovery'),
        card=field(decisions[0]['observation'], 'Card'),
        iteration=task.get('iteration'), learning_arm=task.get('learning_arm'),
        incoming_reflections=trace.get('incoming_reflections', []),
        focal=task['focal'], opponent=task['opponent'], participants=participants, rounds=rounds,
        systems=trace['systems'], definition=definition, marker=saved,
        final_scores=[trace['episode']['scores'][str(p)] for p in range(spec['seats'])] if complete else None,
        paired_episode=dict(id=counterpart['id'], condition=opposite, status=counterpart['status']) if counterpart else None,
        paired_learning_episode=dict(id=learning_pair['id'], learning_arm=learning_pair['learning_arm']) if learning_pair else None,
        interpretation='Markers use the saved v3-MA report. They describe observed behavior, not intent, learning, or causal payoff effects. '
                       'Purple marks are limited code-pattern or message-association evidence. Failed episodes are unscored.')
