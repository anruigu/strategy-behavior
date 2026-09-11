import copy
from collections import Counter, defaultdict
import unittest

from prediction.games import generate_games, make_game
from prediction.improve.data import (TARGETS,FAMILIES,aggregate_records,metadata_examples,
    split_coordinate,build_folds,target_weights)

PROTOCOL = dict(rounds=8,temperature=.7,max_tokens=4096,max_attempts=2,
                opponent_identity_disclosed=False,history='complete_public',objective='own_cumulative_points')


def synthetic_records(n=42, seed=1234):
    records = []
    for i,game in enumerate(generate_games(seed,n)):
        for trial in (0,1):
            for focal in (0,1):
                row = dict(game_id=game['id'], group_id=game['group_id'],family=game['family'],
                    payoffs=game['payoffs'], model=('m0','m1')[focal],opponent=('m1','m0')[focal],
                    episode_id=f"e{i}t{trial}", player_index=focal,trial_id=trial,swap=bool(trial),representation='matrix',targets={})
                for target in TARGETS:
                    supported = target == 'action0' or game['applicability'][target]
                    k = (i+trial+focal)%9
                    row['targets'][target] = dict(successes=k if supported else None,opportunities=8 if supported else 0,
                                                 value=k/8 if supported else None,applicable=supported)
                records.append(row)
    return records


class DataTests(unittest.TestCase):
    def test_aggregation_preserves_counts_ids_and_weights(self):
        records = synthetic_records()
        examples = aggregate_records(records,PROTOCOL)
        metadata = metadata_examples(records,PROTOCOL)
        self.assertEqual([r['row_id'] for r in metadata],[r['row_id'] for r in examples])
        self.assertEqual(len(examples),84)
        for target in TARGETS:
            self.assertEqual(sum((r['targets'][target]['successes'] or 0) for r in examples),
                             sum((r['targets'][target]['successes'] or 0) for r in records))
        totals = defaultdict(float)
        for row,weights in zip(examples,target_weights(examples)):
            for t,weight in zip(TARGETS,weights):
                totals[row['group_id'],t] += weight
        self.assertTrue(all(abs(v-1)<1e-10 or v==0 for v in totals.values()))
        for row in metadata:
            self.assertNotIn(row['game_id'],row['input_text'])
            self.assertNotIn('family=',row['input_text'])
            self.assertNotIn('targets',row)

    def test_splits_cover_all_families_and_preserve_coordinate_regions(self):
        rows = aggregate_records(synthetic_records(),PROTOCOL)
        folds = build_folds(rows)
        self.assertEqual(len(folds),9)
        self.assertEqual(sum(f['split']=='family' for f in folds),7)
        for fold in folds:
            self.assertFalse(set(fold['train_groups'])&set(fold['test_groups']))
            if fold['split'] in ('interpolation','extrapolation'):
                self.assertEqual(set(fold['train_family_groups']),set(FAMILIES))
                self.assertEqual(set(fold['test_family_groups']),set(FAMILIES))
                for family,detail in fold['details'].items():
                    lower,middle,upper = (detail['regions'][n] for n in ('lower','middle','upper'))
                    self.assertLess(lower['max'],middle['min'])
                    self.assertLess(middle['max'],upper['min'])
        poisoned = copy.deepcopy(rows)
        for row in poisoned:
            row['targets'] = {'invalid':'These labels must not be inspected'}
            row['y'] = [999]*3;row['mask']=[False]*3
        self.assertEqual(folds,build_folds(poisoned))

    def test_coordinate_affine_and_action_swap_invariance(self):
        for game in generate_games(1234,42):
            p = game['payoffs']; values=[p[k] for k in ('R','S','T','P')]
            affine=make_game('changed',*[3*x+10 for x in values])
            swapped=make_game('swapped',*values[::-1])
            original=split_coordinate(game)
            self.assertEqual(original['name'],split_coordinate(affine)['name'])
            self.assertAlmostEqual(original['value'],split_coordinate(affine)['value'],places=10)
            self.assertAlmostEqual(original['value'],split_coordinate(swapped)['value'],places=10)
        self.assertEqual(split_coordinate(make_game('weak',1,.25,1,0))['name'],'canonical_s')

    def test_bad_counts_and_degenerate_regions_fail_closed(self):
        records=synthetic_records()
        records[0]['targets']['action0']['value']=.12345
        with self.assertRaises(ValueError):aggregate_records(records,PROTOCOL)
        rows=aggregate_records(synthetic_records(7),PROTOCOL)
        with self.assertRaisesRegex(ValueError,'three distinct'):build_folds(rows)

    def test_tied_coordinate_blocks_cannot_leak(self):
        rows=aggregate_records(synthetic_records(),PROTOCOL)
        # A new affine variant retains the whole canonical group and coordinate.
        twin=copy.deepcopy(rows[0]);twin['row_id']='variant';twin['game_id']='variant'
        twin['payoffs']={k:v*2+7 for k,v in twin['payoffs'].items()}
        rows.append(twin)
        for fold in build_folds(rows):
            self.assertEqual(0 in fold['train'],len(rows)-1 in fold['train'])
            self.assertEqual(0 in fold['test'],len(rows)-1 in fold['test'])


if __name__ == '__main__':unittest.main()
