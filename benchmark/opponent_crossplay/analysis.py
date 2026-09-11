"""Offline per-model and matched-arm tables. No model/API calls."""
import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    traces = {t['task']['id']: t for p in (out / 'matches').glob('*/trace.json')
              for t in [json.loads(p.read_text())]}
    dest = out / 'analysis'
    dest.mkdir(exist_ok=True)
    observations = []
    curves = []
    for task in manifest['tasks']:
        trace = traces.get(task['id'])
        scores = trace['episode']['scores'] if trace else {}
        cooperative = 'hanabi' in task['edition']
        own = scores.get('0')
        best = max(scores.values()) if scores else None
        wins = sum(v == best for v in scores.values())
        evaluation = trace['evaluation'] if trace else {}
        observations.append(dict(match=task['id'], block=task['block'], cell=task['cell'],
            focal=task['seats'][0], opponents=' / '.join(task['seats'][1:]), seed=task['seed'], arm=task['arm'],
            complete=trace is not None, exposed=evaluation.get('exposures', 0) > 0 if trace else None,
            response=evaluation.get('response_signature'), exploited=evaluation.get('exploited_signature'),
            first_response=evaluation.get('first_response_turn'), first_exploitation=evaluation.get('first_exploitation_turn'),
            score=own, team_score=own if cooperative else None,
            win_share=None if cooperative or not trace else (1 / wins if own == best else 0),
            articulated_discovery=None))
        if trace:
            for turn in range(1, 9):
                events = [e for e in evaluation['events'] if e['turn'] <= turn]
                curves.append(dict(match=task['id'], cell=task['cell'], focal=task['seats'][0],
                    seed=task['seed'], arm=task['arm'], turn=turn,
                    reached_turn=turn <= len(trace['episode']['extras']['events']),
                    cumulative_exposure=any(e['exposed'] for e in events),
                    cumulative_response=any(e['response_signature'] for e in events),
                    cumulative_exploitation=any(e['exploited_signature'] for e in events)))
    grouped = defaultdict(list)
    paired = defaultdict(dict)
    for row in observations:
        grouped[row['cell'], row['focal'], row['arm']].append(row)
        paired[row['block']][row['arm']] = row
    aggregates = []
    for (cell, focal, arm), rows in sorted(grouped.items()):
        done = [r for r in rows if r['complete']]
        exposed = [r for r in done if r['exposed']]
        aggregates.append(dict(cell=cell, focal=focal, arm=arm, planned=len(rows), complete=len(done), exposed=len(exposed),
            response_count=sum(bool(r['response']) for r in done), exploitation_count=sum(bool(r['exploited']) for r in done),
            response_rate_complete=sum(bool(r['response']) for r in done) / len(done) if done else None,
            exploitation_rate_complete=sum(bool(r['exploited']) for r in done) / len(done) if done else None,
            response_rate_exposed=sum(bool(r['response']) for r in exposed) / len(exposed) if exposed else None))
    differences = []
    for block, arms in paired.items():
        if not all(arm in arms and arms[arm]['complete'] for arm in ('ordinary', 'nerfed')):
            continue
        a, b = arms['ordinary'], arms['nerfed']
        differences.append(dict(block=block, cell=a['cell'], focal=a['focal'], opponents=a['opponents'], seed=a['seed'],
            ordinary_exposed=a['exposed'], nerfed_exposed=b['exposed'],
            response_difference=int(b['response']) - int(a['response']),
            exploitation_difference=int(b['exploited']) - int(a['exploited']),
            score_difference=b['score'] - a['score']))
    write_csv(dest / 'observations.csv', observations)
    write_csv(dest / 'model_cell_rates.csv', aggregates)
    write_csv(dest / 'paired_differences.csv', differences)
    write_csv(dest / 'within_game_curves.csv', curves)
    (dest / 'README.md').write_text(
        '# Opponent cross-play analysis\n\n'
        f'{len(traces)}/{len(observations)} completed games; {len(differences)} complete arm pairs.\n\n'
        'Rates show completed and exposed denominators. Missing games and unexposed cells are distinct. '
        'Paired differences include only complete same-cell/model/ordered-opponent/seed blocks. '
        'The small initial batch is descriptive; two seed/lineup blocks cannot support precise uncertainty estimates. '
        'There are no across-game learning claims. Curves measure cumulative observed behavior within a game; '
        'the reached-turn flag separates actual turns from carry-forward after early completion. '
        'Semantic discovery remains unscored. Hanabi has team scores and no win shares.\n')
    return dest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('out', type=Path)
    print(analyze(parser.parse_args().out))
