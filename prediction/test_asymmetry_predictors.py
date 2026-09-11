"""Offline leakage and role-orientation checks for the predictor comparison."""
from copy import deepcopy
import json
import unittest

from prediction import asymmetry_predictors as p
from prediction import asymmetry_smoke as s


def training_fixture():
    traces = []
    for left in s.SCHEDULES:
        for right in s.SCHEDULES:
            game = s.make_game(left,right)
            for reverse in range(2):
                for swap in range(2):
                    spec = dict(id=f'{left}-{right}-{reverse}-{swap}',game_id=game['id'],
                                models=s.PLAYERS[::-1] if reverse else s.PLAYERS,swap=bool(swap))
                    turns = [dict(round=i+1,actions=[i%2,(i//2)%2],payoffs=s.payoff(game,i%2,(i//2)%2)) for i in range(8)]
                    traces.append(dict(spec=spec,game=game,rounds=turns))
    return traces


class PredictorTests(unittest.TestCase):
    def test_equivalent_action_and_role_copies_group_together(self):
        game = s.make_game('pd','chicken')
        expected = p.shape_id(game)
        for swap0 in range(2):
            for swap1 in range(2):
                copied = deepcopy(game)
                copied['matrix'] = [[game['matrix'][a ^ swap0][b ^ swap1] for b in range(2)] for a in range(2)]
                self.assertEqual(p.shape_id(copied),expected)
                copied['matrix'] = [[copied['matrix'][b][a][::-1] for b in range(2)] for a in range(2)]
                self.assertEqual(p.shape_id(copied),expected)
        copied = deepcopy(game)
        copied['matrix'] = [[[2*u+7,3*v-4] for u,v in row] for row in game['matrix']]
        self.assertEqual(p.shape_id(copied),expected)

    def test_grid_has_ten_groups(self):
        self.assertEqual(len({p.shape_id(s.make_game(a,b)) for a in s.SCHEDULES for b in s.SCHEDULES}),10)

    def test_both_role_payoff_features(self):
        game = s.make_game('pd','harmony')
        row = p.features(game,1,True)
        self.assertEqual([row[f'self_payoff_{a}{b}'] for a,b in s.PROFILES],[3,2,1,0])
        self.assertEqual([row[f'other_payoff_{a}{b}'] for a,b in s.PROFILES],[3,0,5,1])
        self.assertEqual(row['self_dominant_0'],1)
        self.assertEqual(row['other_dominant_1'],1)
        self.assertEqual(row['pure_nash_01'],1)

    def test_metadata_does_not_consume_outcomes(self):
        trace = training_fixture()[0]
        del trace['rounds']
        rows = p.rows_for(trace,False)
        self.assertEqual(len(rows),2)
        self.assertTrue(all('targets' not in row for row in rows))

    def test_outer_holdout_removes_all_mirror_repetitions(self):
        traces = training_fixture()
        game = s.make_game('pd','chicken')
        allowed = p.training_for(traces,game)
        self.assertEqual(len(allowed),56)
        self.assertFalse({'pd__chicken','chicken__pd'} & {t['game']['id'] for t in allowed})

    def test_examples_are_three_distinct_allowed_groups(self):
        traces = training_fixture()
        game = s.make_game('pd','chicken')
        spec = dict(models=s.PLAYERS,swap=False)
        examples = p.select_examples(traces,game,spec)
        self.assertEqual(len({x['group_id'] for x in examples}),3)
        for ex in examples:
            self.assertNotEqual(ex['group_id'],p.shape_id(game))
            self.assertEqual(ex['rounds'],16)
            self.assertEqual(sum(ex['joint_counts']),16)
            self.assertEqual(set(ex['display_swaps']),{False,True})
            self.assertEqual(ex['models'],spec['models'])

    def test_changing_heldout_labels_cannot_change_training_or_examples(self):
        traces = training_fixture()
        changed = deepcopy(traces)
        game = s.make_game('stag','chicken')
        spec = dict(models=s.PLAYERS,swap=False)
        for t in changed:
            if p.shape_id(t['game']) == p.shape_id(game):
                for turn in t['rounds']: turn['actions']=[1,1]
        self.assertEqual(p.training_for(traces,game),p.training_for(changed,game))
        self.assertEqual(p.select_examples(traces,game,spec),p.select_examples(changed,game,spec))

    def test_example_display_swap_maps_payoffs_and_joint_counts(self):
        game = s.make_game('pd','chicken')
        spec = dict(models=s.PLAYERS,swap=True)
        examples = p.select_examples(training_fixture(),game,spec)
        examples[0]['joint_counts']=[1,2,5,8]
        content = p.few_messages(game,spec,examples)[1]['content']
        payload = json.loads(content.split('\n',1)[1].split('\n\nTARGET GAME:')[0])
        self.assertEqual(payload[0]['observed_joint_frequencies_AA_AB_BA_BB'],[.5,5/16,2/16,1/16])
        self.assertEqual(payload[0]['payoffs'][0]['points'],examples[0]['matrix'][1][1])

    def test_numerical_fit_sees_both_players_and_no_heldout_group(self):
        traces = training_fixture()
        for k,t in enumerate(traces):
            for turn in t['rounds']: turn['actions']=[int(k%3==0),int(k%4==0)]
        game = s.make_game('stag','chicken')
        train = [r for t in p.training_for(traces,game) for r in p.rows_for(t)]
        model = p.FittedPredictor(p.ModelSpec('test','logistic','structural','both'),'action0').fit(train)
        keys = {key for source,key in model.metadata()['feature_keys']}
        self.assertIn('self_payoff_00',keys)
        self.assertIn('other_payoff_11',keys)
        self.assertNotIn(p.shape_id(game),model.training_groups)
        query = p.rows_for(dict(game=game,spec=dict(id='heldout',models=s.PLAYERS,swap=False)),False)
        self.assertTrue(all(0<=x<=1 for x in model.predict(query)))


if __name__=='__main__': unittest.main()
