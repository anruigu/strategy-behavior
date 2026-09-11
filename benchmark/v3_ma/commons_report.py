"""Commons participation and fixed-action payoff comparisons for this screen."""
import argparse
from collections import Counter
import json
from pathlib import Path
import statistics

from benchmark.clients import write_json
from engines_v3_ma import GAMES


def analyze(out):
    report = json.loads((out / 'report.json').read_text())
    results = []
    for game in GAMES.values():
        if game.family != 'commons':
            continue
        episodes = [r for r in report['episodes'] if r['game'] == game.NAME and r['status'] == 'complete']
        rounds = []
        for row in episodes:
            trace = json.loads((out / 'episodes' / row['id'] / 'trace.json').read_text())
            for event in trace['episode']['extras']['events']:
                facts = event['facts']
                actual = facts['settled']
                # Hold the other two submitted actions fixed. This is a one-turn
                # deviation calculation, not an adaptive policy counterfactual.
                compliant = [2, *actual[1:]]
                rounds.append(dict(
                    over=actual[0] > 2, participants=sum(x > 2 for x in actual),
                    focal_payoff=facts['payoff'][0], welfare=sum(facts['payoff']),
                    gain_vs_focal_quota=game.payoff(actual)[0] - game.payoff(compliant)[0]))
        standard = []
        for others_over in range(3):
            others = [6] * others_over + [2] * (2 - others_over)
            payoff = game.payoff([6, *others])
            baseline = game.payoff([2, *others])[0]
            standard.append(dict(other_exploiters=others_over, focal_catch=6,
                focal_payoff=payoff[0], focal_gain_vs_catch2=payoff[0] - baseline,
                welfare=sum(payoff)))
        over = [r for r in rounds if r['over']]
        average = lambda rows, key: statistics.mean(r[key] for r in rows) if rows else None
        results.append(dict(game=game.NAME, complete_episodes=len(episodes), rounds=len(rounds),
            episodes_focal_over_quota=sum(r['marker']['episode_marker'] for r in episodes),
            focal_over_quota_rounds=len(over), participants_per_round=dict(sorted(Counter(r['participants'] for r in rounds).items())),
            mean_focal_payoff_per_round=average(rounds, 'focal_payoff'),
            mean_welfare_per_round=average(rounds, 'welfare'),
            over_quota_rounds_negative_focal_payoff=sum(r['focal_payoff'] < 0 for r in over),
            over_quota_rounds_negative_gain_vs_quota=sum(r['gain_vs_focal_quota'] < -1e-9 for r in over),
            mean_gain_vs_quota_on_over_quota_rounds=average(over, 'gain_vs_focal_quota'),
            standardized_profiles=standard))
    result = dict(scenarios=results, interpretation=[
        'The compliant profile [2,2,2] gives each seat 2 and total welfare 6 per round in all four scenarios.',
        'Standardized profiles are exact payoff calculations for catch 6 versus catch 2, holding the other actions fixed; they are not sampled live-model episodes.',
        'Negative absolute reward, negative advantage over compliance, and negative social impact are different quantities.',
        'Observed one-turn deviations do not predict how other policies would adapt. No weight training or across-episode learning is performed.'])
    write_json(out / 'commons-analysis.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.out), indent=2))
