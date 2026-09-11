import json
from copy import deepcopy
from pathlib import Path
import random
import tempfile
import unittest

from prediction.io_utils import read_json,write_json
from .catalog import configurations
from .native import Session,messages
from .policies import view,action,word_feedback,code_feedback
from .runner import replay
from .export import action_labels,episode_rows

GAMES={g['family_id']:g for g in configurations() if g['intervention_axis'] is None}


class NativeContract(unittest.TestCase):
    def test_hidden_opponent_data_does_not_enter_bot_view(self):
        cases={
            'kuhn_poker':('player_cards',999),
            'liars_dice':('dice_rolls',[6]*20),
            'blind_auction':('player_item_values',{0:999999}),
            'negotiation':('player_values',{'Gold':999999}),
            'prisoners_dilemma':('decisions','SECRET_PENDING_DECISION'),
            'colonel_blotto':('player_states',{'current_allocation':{'A':999999}}),
        }
        for fid,(key,value) in cases.items():
            with self.subTest(family=fid):
                s=Session(GAMES[fid],6100); actor,_,history=s.observe()
                before=view(s,actor,history); prompt=messages(GAMES[fid],history,'normal')
                s.env.state.game_state[key][1-actor]=value
                self.assertEqual(before,view(s,actor,history))
                self.assertEqual(prompt,messages(GAMES[fid],history,'normal'))

    def test_global_random_and_interleaving_do_not_change_native_chance(self):
        s=Session(GAMES['pig_dice'],6100); t=Session(GAMES['pig_dice'],6100)
        before=random.getstate()
        for i in range(6):
            self.assertEqual(s.observe(),t.observe()); r=s.step('[roll]')
            saved=random.getstate(); random.seed(12345); random.random(); random.setstate(saved)
            Session(GAMES['liars_dice'],999)
            self.assertEqual(r,t.step('[roll]')); self.assertEqual(s.snapshot(),t.snapshot())
        self.assertEqual(before,random.getstate())

    def test_native_invalid_retry_and_penalty_preserved(self):
        s=Session(GAMES['nim'],6100)
        first=s.step('invalid'); self.assertTrue(first['native_invalid']); self.assertFalse(first['done'])
        second=s.step('invalid'); self.assertTrue(second['native_invalid']); self.assertTrue(second['done'])

    def test_native_pd_default_and_opportunity_mask(self):
        s=Session(GAMES['prisoners_dilemma'],6100)
        for _ in range(2): s.observe(); s.step('hello')
        actor,_,h=s.observe(); v=view(s,actor,h); result=s.step('no token')
        label=action_labels(dict(raw_action='no token',visible_state=v,result=result),'prisoners_dilemma')
        self.assertTrue(label['cooperation']); self.assertFalse(label['conforms_to_decision_token'])
        self.assertIsNone(action_labels(dict(raw_action='[Cooperate]',visible_state={'phase':'conversation'},result=result),'prisoners_dilemma')['cooperation'])

    def test_duplicate_letter_feedback(self):
        self.assertEqual(word_feedback('apple','allee'),['G','Y','X','X','G'])
        self.assertEqual(code_feedback([1,1,2],[1,2,2]),(2,0))

    def test_auction_bid_aliases_follow_native_syntax(self):
        labels=action_labels(dict(raw_action='[Bid 0: 10] [bid on item 1 : 20]',visible_state={'phase':'bidding'},result={'native_invalid':False}),'blind_auction')
        self.assertEqual(labels['submitted_bid_total'],30)

    def test_replay_rejects_corrupted_transition(self):
        s=Session(GAMES['nim'],6100); opening=s.snapshot(); observations=s.opening
        actor,incoming,h=s.observe(); v=view(s,actor,h); raw=action(v,6100,0); before=s.snapshot(); result=s.step(raw)
        step=dict(actor=actor,incoming=incoming,visible_state=v,before=before,is_focal=False,raw_action=raw,result=result,after=s.snapshot())
        record=json.loads(json.dumps(dict(opening_state=opening,opening_observations=observations,steps=[step])))
        item=dict(game=GAMES['nim'],seed=6100)
        replay(item,record)
        record['steps'][0]['after']['game_state']['piles'][0]+=1
        with self.assertRaises(AssertionError): replay(item,record)

    def test_prediction_inputs_ignore_evaluator_secrets_and_future(self):
        run=Path('prediction/general_games/runs/pilot-20260910')
        plan=read_json(run/'plan.json'); item=next(x for x in plan['episodes'] if x['game']['family_id']=='mastermind')
        s=Session(item['game'],item['seed']); opening=s.snapshot()
        record=json.loads(json.dumps(dict(item=item,status='censored',opening_state=opening,opening_observations=s.opening,steps=[])))
        splits=read_json(Path(plan['data_dir'])/'splits.json')
        first,_=episode_rows(record,plan,splits)
        record['opening_state']['game_state']['secret_code']=['EVALUATOR_SECRET']
        record['final_state']={'rewards':{'0':12345},'future':'DO_NOT_LEAK'}
        second,_=episode_rows(record,plan,splits)
        self.assertEqual(first['inputs'],second['inputs'])
        self.assertNotIn('EVALUATOR_SECRET',json.dumps(second['inputs']))
        self.assertNotIn('DO_NOT_LEAK',json.dumps(second['inputs']))

    def test_duplicate_openings_share_splits(self):
        data=Path('prediction/general_games/data/20260910-v1')
        instances=read_json(data/'instances.evaluator.json'); splits=read_json(data/'splits.json'); groups={}
        for row in instances:
            key=json.dumps([row['configuration_id'],row['opening_state']],sort_keys=True)
            if key in groups: self.assertEqual(groups[key],row['opening_group'])
            groups[key]=row['opening_group']
            self.assertIn(splits['opening_group'][row['opening_group']],('train','validation','test'))
        self.assertLess(len(groups),len(instances))

    def test_full_plan_crosses_all_seeds_and_seats(self):
        plan=read_json('prediction/general_games/runs/full-catalog-v1/plan.json')
        actual=[(e['game']['configuration_id'],e['seed'],e['seat'],e['model'],e['condition']) for e in plan['episodes']]
        expected={(g['configuration_id'],seed,seat,model,condition) for g in configurations()
                  for seed in (6100,6101,6102,6103) for seat in range(g['num_players'])
                  for model in ('qwen-3.8-27b','glm') for condition in ('normal','active_exploration')}
        self.assertEqual(len(actual),len(set(actual)))
        self.assertEqual(set(actual),expected)
        self.assertEqual(len(actual),1360)


if __name__=='__main__': unittest.main()
