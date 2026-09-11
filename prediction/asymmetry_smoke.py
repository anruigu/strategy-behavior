"""Small prospective 4x4 payoff-mixing experiment, isolated from the symmetric study.

Each schedule is indexed [own action][other action]. Player 1's schedule
therefore transposes into the shared row/column coordinates. Run with:
  python -B -m prediction.asymmetry_smoke --out prediction/results/asymmetry-20260910
No calls occur on import. Forecasts are frozen before any player decisions.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import math
import random
import shutil
import statistics
import sys

from prediction.client import Client, Ledger, ModelConfig, configurations
from prediction.io_utils import digest, now, read_json, write_json
from prediction.runner import SYSTEM, decision, parse_action

ROOT = Path(__file__).resolve().parents[1]
SCHEDULES = {
    'pd': [[3, 0], [5, 1]],
    'harmony': [[3, 2], [1, 0]],
    'stag': [[3, 0], [2, 1]],
    'chicken': [[3, 1], [5, 0]],
}
PROFILES = list(product(range(2), repeat=2))
PLAYERS = ['qwen-3.8-27b', 'gpt-oss-20b']


def make_game(left, right):
    u, v = SCHEDULES[left], SCHEDULES[right]
    matrix = [[[u[a][b], v[b][a]] for b in range(2)] for a in range(2)]
    pure = [[a, b] for a, b in PROFILES
            if matrix[a][b][0] >= matrix[1-a][b][0]
            and matrix[a][b][1] >= matrix[a][1-b][1]]
    return dict(id=f'{left}__{right}', schedules=[left, right], matrix=matrix,
                condition='symmetric' if left == right else 'asymmetric', pure_nash=pure,
                role_equivalence_group='__'.join(sorted([left, right])))


def payoff(game, a, b):
    return game['matrix'][a][b]


def focal_cell(game, player, own, other):
    scores = payoff(game, own, other) if player == 0 else payoff(game, other, own)
    return [scores[player], scores[1-player]]


def table(game, player=0, swap=False):
    lines = ['You and the other participant each choose A or B simultaneously.',
             "Rows are your choice; columns are the other participant's choice.",
             "Each cell is (your points, other participant's points).",
             '| Your choice / Other choice | A | B |', '|---|---|---|']
    for a in range(2):
        cells = [focal_cell(game, player, a ^ int(swap), b ^ int(swap)) for b in range(2)]
        lines.append('| ' + 'AB'[a] + ' | ' + ' | '.join(f'({u!r}, {v!r})' for u, v in cells) + ' |')
    return '\n'.join(lines)


def messages_for(game, rounds, player, swap):
    labels = ['B', 'A'] if swap else ['A', 'B']
    history = [f"Round {t['round']}: you {labels[t['actions'][player]]}, other {labels[t['actions'][1-player]]}; "
               f"your points {t['payoffs'][player]:g}, other points {t['payoffs'][1-player]:g}." for t in rounds]
    observation = (f'There are exactly 8 rounds. This is round {len(rounds)+1} of 8. '
                   'The other player is an AI agent. Neither player sees the other current action before choosing.\n\n'
                   + table(game, player, swap) + '\n\nPublic history:\n'
                   + ('\n'.join(history) if history else 'No rounds have been played.') + '\n\nChoose A or B now.')
    return [dict(role='system', content=SYSTEM), dict(role='user', content=observation)]


def theory(game):
    """Highest total-payoff pure Nash; tied profiles share joint mass.

    Otherwise use the unique interior mixed equilibrium. This is a fixed
    stage-game comparator, not a theory of history-dependent repeated play.
    """
    pure = game['pure_nash']
    if pure:
        best = max(sum(payoff(game, *p)) for p in pure)
        selected = [p for p in pure if sum(payoff(game, *p)) == best]
        return [float(list(p) in selected) / len(selected) for p in PROFILES]
    d0, d1 = [payoff(game, 0, b)[0] - payoff(game, 1, b)[0] for b in range(2)]
    e0, e1 = [payoff(game, a, 0)[1] - payoff(game, a, 1)[1] for a in range(2)]
    q1, q0 = -d1 / (d0-d1), -e1 / (e0-e1)
    assert 0 < q0 < 1 and 0 < q1 < 1
    return [(q0 if a == 0 else 1-q0) * (q1 if b == 0 else 1-q1) for a, b in PROFILES]


def parse_forecast(reply, swap):
    value = json.loads(reply)
    probs = value['joint']
    if len(probs) != 4 or any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1 for p in probs):
        raise ValueError('Expected four finite probabilities')
    if abs(sum(probs)-1) > 1e-6:
        raise ValueError('Probabilities must sum to one')
    return [probs[2*(a ^ int(swap)) + (b ^ int(swap))] for a, b in PROFILES]


def forecast_messages(game, spec):
    cells = [{'actions': ['AB'[a], 'AB'[b]],
              'points': payoff(game, a ^ int(spec['swap']), b ^ int(spec['swap']))} for a, b in PROFILES]
    content = (f"Predict actual behavior of Player 0 ({spec['models'][0]}) and Player 1 ({spec['models'][1]}) "
               'before an eight-round simultaneous game. Each maximizes its own total points, sees complete public '
               'action/payoff history, and does not know the opponent model identity. Each round is a fresh request '
               'with that public history, temperature 0.7, low reasoning effort and a 4096-token cap. '
               'Their system instruction is: ' + SYSTEM + '\n'
               'Each chooses A or B. Both see both players\' actual payoffs from their own perspective. '
               'The schedules may differ between players. Payoffs below are [Player 0 points, Player 1 points]; '
               'actions are [Player 0 action, Player 1 action].\n' + json.dumps(cells) + '\n'
               'Forecast the expected fraction of the eight rounds with each joint action AA, AB, BA, BB, '
               'averaging over possible play histories. Predict empirical AI behavior, not just optimal play. '
               'Return exactly JSON {"joint": [p_AA, p_AB, p_BA, p_BB]}, four probabilities summing to one.')
    return [dict(role='system', content='You forecast behavior in repeated two-player games. Return only the requested JSON.'),
            dict(role='user', content=content)]


def forecast_one(out, manifest, spec, client):
    game = next(g for g in manifest['games'] if g['id'] == spec['game_id'])
    messages = forecast_messages(game, spec)
    path = out / 'forecasts' / (spec['id'] + '.json')
    item = read_json(path) if path.exists() else dict(messages=messages, attempts=[], status='pending')
    assert item['messages'] == messages
    if item['status'] == 'complete':
        assert item['joint'] == parse_forecast(item['attempts'][-1]['reply'], spec['swap'])
        return item
    while len(item['attempts']) < 2:
        reply, meta = client.generate(messages, purpose='forecast')
        attempt = dict(reply=reply, meta=meta)
        item['attempts'].append(attempt)
        if meta['status'] == 'ok':
            try:
                item.update(joint=parse_forecast(reply, spec['swap']), status='complete', finished=now())
            except (ValueError, KeyError, TypeError) as exc:
                attempt['parse_error'] = str(exc)
        write_json(path, item)
        if item['status'] == 'complete':
            return item
        if meta.get('http_status') in (401, 402, 403, 404):
            break
    raise RuntimeError('Forecast failed: ' + spec['id'])


def play_one(out, manifest, spec, clients, pool):
    game = next(g for g in manifest['games'] if g['id'] == spec['game_id'])
    folder = out / 'episodes' / spec['id']
    path = folder / 'trace.json'
    if path.exists():
        return read_json(path)
    identity = digest(dict(manifest=digest(manifest), spec=spec))
    trace = dict(spec=spec, game=game, started=now(), rounds=[])
    for k in range(8):
        prompts = [messages_for(game, trace['rounds'], p, spec['swap']) for p in range(2)]
        futures = [pool.submit(decision, clients[spec['models'][p]], prompts[p],
                               folder / f'round-{k+1:02}-player-{p}.json', identity, 2) for p in range(2)]
        items = [f.result() for f in futures]
        actions = [item['displayed_action'] ^ int(spec['swap']) for item in items]
        trace['rounds'].append(dict(round=k+1, actions=actions, payoffs=payoff(game, *actions)))
        write_json(folder / 'progress.json', trace)
    trace.update(status='complete', finished=now())
    write_json(path, trace)
    return trace


def freeze(out):
    path = out / 'manifest.json'
    if path.exists():
        saved = read_json(path)
        for name, expected in saved['sources'].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
        return saved
    games = [make_game(a, b) for a, b in product(SCHEDULES, repeat=2)]
    episodes = []
    for game, reverse, swap in product(games, range(2), range(2)):
        episodes.append(dict(id=f"{game['id']}--role{reverse}--swap{swap}", game_id=game['id'],
                             models=PLAYERS[::-1] if reverse else PLAYERS, swap=bool(swap)))
    random.Random(20260910).shuffle(episodes)
    sources = {}
    for module in list(sys.modules.values()):
        source = getattr(module, '__file__', None)
        if not source:
            continue
        source = Path(source).resolve()
        if source.is_relative_to(ROOT) and source.suffix == '.py' and 'results' not in source.parts:
            name = str(source.relative_to(ROOT))
            sources[name] = hashlib.sha256(source.read_bytes()).hexdigest()
            target = out / 'source' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    configs = configurations(PLAYERS + ['kimi-k3'])
    configs['kimi-k3'].update(provider='openrouter',provider_model='moonshotai/kimi-k3',
                              base_url='https://openrouter.ai/api/v1',key_env='OPENROUTER_API_KEY')
    value = dict(created=now(), design='4 schedules crossed independently; 2 model-seat orders x 2 label orientations',
                 games=games, episodes=episodes, models=configs, sources=sources,
                 protocol=dict(rounds=8, temperature=.7, max_tokens=4096, max_attempts=2),
                 budget_usd=20, predictor='Kimi zero-shot joint-action forecast, no training or examples',
                 targets=['focal action0', 'joint action profile'],
                 metrics=['event Brier', 'pooled cell rate MSE', 'pooled cell rate MAE'],
                 uncertainty='Exploratory resampling of 4 symmetric or 6 unordered asymmetric schedule groups; both roles stay together')
    write_json(path, value)
    return value


def verify(out, manifest):
    frozen = read_json(out / 'forecast-freeze.json')
    assert frozen['manifest_sha256'] == digest(manifest)
    assert frozen['forecast_sha256'] == digest({s['id']: read_json(out/'forecasts'/(s['id']+'.json')) for s in manifest['episodes']})
    traces = []
    for spec in manifest['episodes']:
        path = out / 'episodes' / spec['id'] / 'trace.json'
        if not path.exists():
            continue
        trace = read_json(path)
        game = next(g for g in manifest['games'] if g['id'] == spec['game_id'])
        assert trace['spec'] == spec and trace['game'] == game and trace['status'] == 'complete'
        assert len(trace['rounds']) == 8 and trace['started'] > frozen['frozen_at']
        identity = digest(dict(manifest=digest(manifest), spec=spec))
        for k, turn in enumerate(trace['rounds']):
            assert turn['round'] == k+1 and turn['payoffs'] == payoff(game, *turn['actions'])
            for p in range(2):
                item = read_json(path.parent / f'round-{k+1:02}-player-{p}.json')
                messages = messages_for(game, trace['rounds'][:k], p, spec['swap'])
                assert item['messages'] == messages and item['context_sha256'] == digest(dict(identity=identity, messages=messages))
                last = item['attempts'][-1]
                assert last['meta']['status'] == 'ok'
                assert parse_action(last['reply']) ^ int(spec['swap']) == turn['actions'][p]
                for attempt in item['attempts']:
                    call = read_json(out/'calls'/spec['models'][p]/(attempt['meta']['call_id']+'.json'))
                    assert call['timestamp'] > frozen['frozen_at']
                    assert call['request']['messages'] == messages and call['config'] == manifest['models'][spec['models'][p]]
        traces.append(trace)
    for spec in manifest['episodes']:
        item = read_json(out/'forecasts'/(spec['id']+'.json'))
        assert item['status'] == 'complete' and item['finished'] <= frozen['frozen_at']
        assert item['joint'] == parse_forecast(item['attempts'][-1]['reply'], spec['swap'])
    return traces


def mean(values):
    return statistics.mean(values)


def analyze(out, manifest):
    traces = verify(out, manifest)
    rows = []
    for trace in traces:
        spec, game = trace['spec'], trace['game']
        observed = [sum(t['actions'] == list(p) for t in trace['rounds']) / 8 for p in PROFILES]
        predictions = {'kimi': read_json(out/'forecasts'/(spec['id']+'.json'))['joint'],
                       'stage_nash': theory(game), 'uniform': [.25]*4}
        for method, pred in predictions.items():
            for p in range(2):
                q = sum(pred[i] for i, profile in enumerate(PROFILES) if profile[p] == 0)
                y = sum(observed[i] for i, profile in enumerate(PROFILES) if profile[p] == 0)
                rows.append(dict(game_id=game['id'], group=game['role_equivalence_group'], condition=game['condition'],
                                 episode=spec['id'], model=spec['models'][p], player=p, method=method,
                                 prediction=q, observed=y, brier=y*(1-q)**2+(1-y)*q**2,
                                 joint_brier=1 + sum(x*x for x in pred) - 2*sum(x*y for x,y in zip(pred, observed)),
                                 pure_nash_count=len(game['pure_nash'])))
    cells = []
    for key in sorted({(r['game_id'], r['player'], r['model'], r['method']) for r in rows}):
        selected = [r for r in rows if (r['game_id'], r['player'], r['model'], r['method']) == key]
        y, q = mean(r['observed'] for r in selected), mean(r['prediction'] for r in selected)
        cells.append(dict(**{k:selected[0][k] for k in ('game_id','group','condition','player','model','method','pure_nash_count')},
                          observed=y, prediction=q, rate_mse=(q-y)**2, rate_mae=abs(q-y),
                          event_brier=mean(r['brier'] for r in selected), joint_brier=mean(r['joint_brier'] for r in selected)))
    metrics = ['event_brier', 'rate_mse', 'rate_mae', 'joint_brier']
    scores = {condition: {method: {metric: mean(c[metric] for c in cells if c['condition'] == condition and c['method'] == method)
                                  for metric in metrics} for method in predictions}
              for condition in ('symmetric','asymmetric')}
    rng = random.Random(20260910)
    intervals = {}
    for method in predictions:
        intervals[method] = {}
        for metric in metrics:
            groups = {cond: sorted({c['group'] for c in cells if c['condition'] == cond}) for cond in scores}
            values = {cond: {g: mean(c[metric] for c in cells if c['condition'] == cond and c['group'] == g and c['method'] == method)
                             for g in groups[cond]} for cond in scores}
            differences = sorted(mean(values['asymmetric'][g] for g in rng.choices(groups['asymmetric'], k=len(groups['asymmetric'])))
                                 - mean(values['symmetric'][g] for g in rng.choices(groups['symmetric'], k=len(groups['symmetric'])))
                                 for _ in range(2000))
            intervals[method][metric] = dict(asymmetric_minus_symmetric=scores['asymmetric'][method][metric]-scores['symmetric'][method][metric],
                                             descriptive_95_interval=[differences[50], differences[1949]])
    summary = dict(analyzed_at=now(), completed=len(traces), planned=len(manifest['episodes']), scores=scores,
                   contrasts=intervals, budget=Ledger(out/'budget.sqlite',20).summary(),
                   audit='Verified forecast freeze, player chronology, perspective-specific prompts, action decoding, payoffs and call provenance')
    write_json(out/'analysis-rows.json', rows)
    write_json(out/'analysis-cells.json', cells)
    write_json(out/'summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--analyze-only', action='store_true')
    args = parser.parse_args()
    out = args.out
    manifest = freeze(out)
    if args.prepare_only:
        print(json.dumps(dict(games=len(manifest['games']), episodes=len(manifest['episodes']))))
        return
    if args.analyze_only:
        print(json.dumps(analyze(out, manifest), indent=2))
        return
    ledger, stage = Ledger(out/'budget.sqlite',20), Ledger(out/'stage-budget.sqlite',20)
    clients = {name: Client(ModelConfig(**cfg), out/'calls'/name, ledger, stage,4096) for name,cfg in manifest['models'].items()}
    frozen_path = out/'forecast-freeze.json'
    if not frozen_path.exists():
        assert not list((out/'episodes').glob('**/*.json')), 'Player artifacts exist before forecast freeze'
        # Establish endpoint/schema availability before submitting the full batch.
        forecast_one(out,manifest,manifest['episodes'][0],clients['kimi-k3'])
        with ThreadPoolExecutor(max_workers=12) as pool:
            futures = [pool.submit(forecast_one,out,manifest,s,clients['kimi-k3']) for s in manifest['episodes']]
            for n,f in enumerate(as_completed(futures),1):
                f.result()
                print(json.dumps(dict(stage='forecast',completed=n,planned=len(futures))),flush=True)
        write_json(frozen_path, dict(frozen_at=now(), manifest_sha256=digest(manifest),
                   forecast_sha256=digest({s['id']:read_json(out/'forecasts'/(s['id']+'.json')) for s in manifest['episodes']})))
    verify(out, manifest)
    failures = []
    with ThreadPoolExecutor(max_workers=24) as requests, ThreadPoolExecutor(max_workers=12) as episodes:
        futures = {episodes.submit(play_one,out,manifest,s,clients,requests):s for s in manifest['episodes']}
        for n,f in enumerate(as_completed(futures),1):
            try:
                f.result()
            except Exception as exc:
                failures.append(dict(id=futures[f]['id'],error=type(exc).__name__+': '+str(exc)))
            state = dict(updated=now(),stage='play',processed=n,planned=len(futures),failures=failures,budget=ledger.summary())
            write_json(out/'status.json',state)
            print(json.dumps(state),flush=True)
    print(json.dumps(analyze(out,manifest),indent=2))


if __name__ == '__main__':
    main()
