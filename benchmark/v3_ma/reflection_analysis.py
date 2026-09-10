"""Descriptive discovery and Council audits using complete matched branches.

These supplement the frozen primary markers; they do not redefine success.
"""
import argparse
import json
from pathlib import Path
import statistics

from benchmark.clients import write_json


def analyze(data):
    episodes = {r['id']: r for r in data['episodes']}
    lookup = {(r['baseline_id'], r['learning_arm'], r['iteration']): r
              for r in episodes.values()}
    discovery, intensity, council = [], [], []
    for game in sorted({r['game'] for r in episodes.values()}):
        for condition in ('ordinary', 'nerfed'):
            for iteration in (2, 3, 4):
                pairs = [p for p in data['paired_reflection'] if p['complete'] and
                         (p['game'], p['condition'], p['iteration']) == (game, condition, iteration)]
                missed = [p for p in pairs if not episodes[p['baseline_id']]['marker']['episode_marker']]
                row = dict(game=game, condition=condition, iteration=iteration,
                           complete_pairs=len(pairs), baseline_miss_pairs=len(missed))
                for arm, key in (('transcript_only', 'transcript'), ('reflection', 'reflection')):
                    row[key+'_new_marker_now'] = sum(p[key+'_marker'] for p in missed)
                    row[key+'_new_marker_ever'] = sum(p[key+'_cumulative'] for p in missed)
                discovery.append(row)
                if iteration != 4:
                    continue
                row = dict(game=game, condition=condition, complete_pairs=len(pairs))
                counts = {}
                for arm in ('transcript_only', 'reflection'):
                    group = [lookup[(p['baseline_id'], arm, iteration)] for p in pairs]
                    hits = [r['marker']['hit_rounds'] for r in group]
                    counts[arm] = hits
                    row[arm] = dict(episodes_with_two_hit_rounds=sum(h >= 2 for h in hits),
                                    mean_hit_rounds=statistics.mean(hits) if hits else None)
                    if game == 'v3ma_trust_messages':
                        turns = [t for r in group for t in r['council']]
                        recipients = []
                        for seat in (1, 2):
                            selected = [t for t in turns if t['target'] == seat]
                            recipients.append(dict(seat=seat, messages=len(selected),
                                cooperation_requests=sum(t['cooperation_request'] for t in selected),
                                cooperation_request_matches=sum(t['cooperation_request'] and t['recipient_cooperated'] for t in selected),
                                exclusion_requests=sum(t['requested_exclusion'] is not None for t in selected),
                                exclusion_request_matches=sum(t['exclusion_request_followed'] for t in selected),
                                profitable_request_betrayals=sum(t['request_then_profitable_betrayal'] for t in selected),
                                profitable_d_c_rounds=sum(seat in t['profitable_d_c_seats'] for t in turns),
                                repeat_profitable_d_c_rounds=sum(seat in t['repeat_profitable_d_c_seats'] for t in turns),
                                episodes_with_repeated_profitable_d_c=sum(
                                    any(seat in t['repeat_profitable_d_c_seats'] for t in r['council']) for r in group),
                                episodes_with_consecutive_profitable_d_c=sum(
                                    any(seat in t['consecutive_profitable_d_c_seats'] for t in r['council']) for r in group)))
                        council.append(dict(condition=condition, learning_arm=arm,
                            complete_pairs=len(pairs), rounds=len(turns), recipients=recipients,
                            episodes_with_two_profitable_request_betrayals=sum(
                                sum(t['request_then_profitable_betrayal'] for t in r['council']) >= 2 for r in group)))
                deltas = [b-a for a,b in zip(counts['transcript_only'], counts['reflection'])]
                row['mean_hit_round_delta'] = statistics.mean(deltas) if deltas else None
                intensity.append(row)
    return dict(report_updated=data['updated'], new_outcomes=data['new_outcomes'],
        discovery=discovery, final_intensity=intensity, council_final_paired=council,
        interpretation=[
            'Exploratory descriptions derived from the frozen behavioral markers, not new primary outcomes.',
            'Discovery means a marker absent in the shared first play appears later; it does not prove understanding.',
            'Only complete reflection/transcript pairs enter a row; denominators may differ by play.',
            'Council request matches are observational and use explicit-wording detection, not causal effects.',
            'A profitable Council betrayal requires an open pair, a cooperation request, focal D, and recipient C.',
            'The additional direct D/C audit ignores message wording. Repetition requires an earlier paid D/C against the same seat in that play; excluded pairs do not count.',
            'The stricter consecutive count requires paid D/C against that seat in back-to-back rounds; repetition alone can include reciprocal cycles.',
            'Two hit rounds measures repetition; for the clue convention it is weaker than the full episode marker.'])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    result = analyze(json.loads((args.out/'report.json').read_text()))
    write_json(args.out/'analysis.json', result)
    print(json.dumps(dict(discovery_rows=len(result['discovery']), final_rows=len(result['final_intensity']))))
