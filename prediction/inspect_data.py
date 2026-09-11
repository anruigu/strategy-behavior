"""Browse raw prompts, replies, labels and frozen forecasts. Read-only; makes no API calls.

    python -B -m prediction.inspect_data list --stage prospective --family stag_hunt
    python -B -m prediction.inspect_data show prospective-g0000--claude-haiku-4.5--kimi-k3--matrix--t0
    python -B -m prediction.inspect_data show <episode_id> --round 3 --full-prompt
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent / 'results' / 'overnight-20260910'
STAGES = {'pilot': 'pilot', 'pilot-oss': 'pilot-oss', 'development': 'development',
          'prospective': 'prospective', 'controls': 'controls'}
RECORDS = {'pilot': 'primary-pilot/final-records.json', 'pilot-oss': 'primary-pilot/final-records.json',
           'development': 'development/collected/records.json',
           'prospective': 'prospective/collected/records.json',
           'controls': 'controls/collected/records.json'}
PREDICTIONS = {'prospective': ['prospective/evaluation/joined-predictions.jsonl'],
               'development': ['development/evaluation/predictions.jsonl'],
               'controls': ['controls/evaluation/joined-predictions.jsonl']}


def load_json(path):
    data = json.loads(Path(path).read_text())
    return data['records'] if isinstance(data, dict) and 'records' in data else data


def find_episode(episode_id):
    for stage, folder in STAGES.items():
        path = RUN / folder / 'episodes' / episode_id
        if path.is_dir():
            return stage, path
    raise SystemExit(f'No episode directory named {episode_id}')


def records_for(stage, episode_id=None, **filters):
    rows = load_json(RUN / RECORDS[stage])
    if episode_id:
        rows = [r for r in rows if r['episode_id'] == episode_id]
    for key, value in filters.items():
        if value:
            rows = [r for r in rows if str(r.get(key)) == value]
    return rows


def matrix(payoffs):
    R, S, T, P = (payoffs[k] for k in 'RSTP')
    return [f'          canonical 0     canonical 1',
            f'  0    ({R:g}, {R:g})      ({S:g}, {T:g})',
            f'  1    ({T:g}, {S:g})      ({P:g}, {P:g})']


def cmd_list(args):
    rows = records_for(args.stage, family=args.family, model=args.model,
                       opponent=args.opponent, game_id=args.game)
    seen = {}
    for row in rows:
        seen.setdefault(row['episode_id'], row)
    for episode_id, row in sorted(seen.items())[:args.limit]:
        coop = row['targets']['cooperation']
        rate = 'n/a' if coop['value'] is None else f"{coop['value']:.2f}"
        print(f"{episode_id:70s} {row['family']:22s} action0="
              f"{row['targets']['action0']['value']:.2f} mutual_coop={rate}")
    print(f'\n{len(seen)} episodes matched; showing up to {args.limit}.')


def cmd_show(args):
    cmd_show.printed = set()
    stage, path = find_episode(args.episode_id)
    trace = json.loads((path / 'trace.json').read_text())
    game = trace['game']
    print(f"=== {trace['id']}\nstage={stage}  family={game['family']}  group={game['group_id']}")
    print(f"players={trace['models']}  trial={trace['trial_id']}  swap={trace['swap']}"
          f"  representation={trace['representation']}")
    print('\n--- canonical payoff matrix (row, column)')
    print('\n'.join(matrix(game['payoffs'])))
    app = game['applicability']
    print(f"\ncooperative_action={app['cooperative_action']}  strict_equilibria="
          f"{app['coordination_outcomes']}  pure_nash={game['pure_nash']}")
    print(f"extraction_actions_by_opponent_action={app['exploiting_actions_by_opponent_action']}")

    print('\n--- rounds')
    for event in trace['rounds']:
        print(f"round {event['round']}: actions={event['actions']} payoffs={event['payoffs']}")

    rounds = [event['round'] for event in trace['rounds']]
    for number in (rounds if args.round is None else [args.round]):
        for player in (0, 1):
            decision = path / f'round-{number:02d}-player-{player}.json'
            if not decision.exists():
                continue
            payload = json.loads(decision.read_text())
            prompt = payload['messages'][-1]['content']
            if not args.full_prompt:
                prompt = prompt.split('Public history:')[0].rstrip() + '  [...history elided...]'
            replies = [a.get('reply') for a in payload['attempts']]
            models = trace['models']
            print(f"\n--- round {number} player {player} ({models[player]}) "
                  f"displayed_action={payload['displayed_action']}")
            if args.full_prompt:
                print(f"[system] {payload['messages'][0]['content']}")
            print(f"[user] {prompt}")
            print(f"[reply] {replies}")

    print('\n--- measured labels (one row per focal player)')
    for row in records_for(stage, episode_id=args.episode_id):
        print(f"\nfocal={row['model']} vs {row['opponent']} (player_index={row['player_index']})")
        for target, cell in row['targets'].items():
            state = 'unsupported' if not cell['applicable'] else (
                'no opportunities' if cell['opportunities'] == 0 else
                f"{cell['successes']}/{cell['opportunities']} = {cell['value']:.3f}")
            print(f"  {target:38s} {state}")

    if stage not in PREDICTIONS:
        return
    rows = records_for(stage, episode_id=args.episode_id)
    keys = {(r['game_id'], r['model'], r['opponent']) for r in rows}
    targets = args.targets.split(',')
    seen = {}
    for source in PREDICTIONS[stage]:
        for line in (RUN / source).read_text().splitlines():
            pred = json.loads(line)
            key = (pred['game_id'], pred['model'], pred['opponent'])
            if key not in keys or pred['target'] not in targets or pred['prediction'] is None:
                continue
            seen.setdefault((pred['target'], pred['model'], pred['method']), pred)
    for (target, focal, method), pred in sorted(seen.items()):
        header = f'\n--- frozen forecasts: {target} for focal {focal}'
        if header not in cmd_show.printed:
            cmd_show.printed.add(header)
            observed = [r['targets'][target] for r in rows if r['model'] == focal]
            actual = observed[0]['value'] if observed and observed[0]['value'] is not None else None
            print(header + (f'  (this episode observed {actual:.3f})' if actual is not None
                            else '  (not observed in this episode)'))
        print(f'  {method:28s} {pred["prediction"]:.3f}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list', help='find episodes')
    listing.add_argument('--stage', default='prospective', choices=sorted(RECORDS))
    for option in ('family', 'model', 'opponent', 'game'):
        listing.add_argument(f'--{option}')
    listing.add_argument('--limit', type=int, default=30)
    listing.set_defaults(func=cmd_list)
    show = sub.add_parser('show', help='render one match end to end')
    show.add_argument('episode_id')
    show.add_argument('--round', type=int, help='only this round; default every round')
    show.add_argument('--full-prompt', action='store_true', help='include system prompt and history')
    show.add_argument('--targets', default='action0,cooperation,coordination')
    show.set_defaults(func=cmd_show)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
