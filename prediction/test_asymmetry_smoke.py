"""Offline checks for the role and scoring hazards in the asymmetric pilot."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from prediction import asymmetry_smoke as a
from prediction.games import make_game, payoff as symmetric_payoff


class AsymmetryTests(unittest.TestCase):
    def test_independent_payoffs_and_column_perspective(self):
        game = a.make_game('pd', 'harmony')
        self.assertEqual(game['matrix'], [[[3,3],[0,1]],[[5,2],[1,0]]])
        self.assertEqual(a.focal_cell(game,1,0,1),[2,5])
        for player in range(2):
            for own,other in a.PROFILES:
                scores = a.payoff(game,own,other) if player == 0 else a.payoff(game,other,own)
                self.assertEqual(a.focal_cell(game,player,own,other),[scores[player],scores[1-player]])

    def test_symmetric_controls_match_original_payoff(self):
        for name,schedule in a.SCHEDULES.items():
            original = make_game(name,*[schedule[x][y] for x,y in a.PROFILES])
            game = a.make_game(name,name)
            for x,y in a.PROFILES:
                self.assertEqual(a.payoff(game,x,y),list(symmetric_payoff(original,x,y)))

    def test_column_prompt_and_label_swap(self):
        game = a.make_game('pd','harmony')
        self.assertIn('| A | (3, 3) | (2, 5) |',a.table(game,1))
        self.assertIn('| A | (0, 1) | (1, 0) |',a.table(game,1,True))
        history = [dict(round=1,actions=[1,0],payoffs=[5,2])]
        text = a.messages_for(game,history,1,True)[1]['content']
        self.assertIn('you B, other A; your points 2, other points 5',text)

    def test_mixed_equilibrium_indifference(self):
        for left,right in [('stag','chicken'),('chicken','stag')]:
            game = a.make_game(left,right)
            self.assertEqual(game['pure_nash'],[])
            joint = a.theory(game)
            q0,q1 = joint[0]+joint[1],joint[0]+joint[2]
            self.assertAlmostEqual(sum(joint),1)
            self.assertAlmostEqual(sum((q1 if b == 0 else 1-q1)*a.payoff(game,0,b)[0] for b in range(2)),
                                   sum((q1 if b == 0 else 1-q1)*a.payoff(game,1,b)[0] for b in range(2)))
            self.assertAlmostEqual(sum((q0 if x == 0 else 1-q0)*a.payoff(game,x,0)[1] for x in range(2)),
                                   sum((q0 if x == 0 else 1-q0)*a.payoff(game,x,1)[1] for x in range(2)))

    def test_pure_equilibrium_selectors(self):
        self.assertEqual(a.theory(a.make_game('pd','harmony')),[0,0,1,0])
        self.assertEqual(a.theory(a.make_game('chicken','chicken')),[0,.5,.5,0])
        self.assertEqual(a.theory(a.make_game('stag','stag')),[1,0,0,0])

    def test_forecast_validation_and_decoding(self):
        self.assertEqual(a.parse_forecast('{"joint":[0.1,0.2,0.3,0.4]}',True),[.4,.3,.2,.1])
        for probs in ([1,1,1,1],[True,0,0,0],[-1,1,1,0],[float('nan'),0,0,1]):
            with self.assertRaises(ValueError):
                a.parse_forecast(json.dumps(dict(joint=probs)),False)

    def test_schedule_balance(self):
        games = [a.make_game(x,y) for x in a.SCHEDULES for y in a.SCHEDULES]
        self.assertEqual(sum(g['condition']=='symmetric' for g in games),4)
        self.assertEqual(len({g['role_equivalence_group'] for g in games}),10)
        for side in range(2):
            for schedule in a.SCHEDULES:
                self.assertEqual(sum(g['schedules'][side]==schedule and g['condition']=='asymmetric' for g in games),3)

    def test_episode_records_actual_column_payoffs(self):
        class FakeClient:
            def __init__(self,reply): self.reply=reply
            def generate(self,messages): return self.reply,dict(status='ok')
        game = a.make_game('pd','harmony')
        spec = dict(id='test',game_id=game['id'],models=['left','right'],swap=False)
        manifest = dict(games=[game])
        with TemporaryDirectory(dir='/shared/allie',prefix='asymmetry-test-') as folder, ThreadPoolExecutor(2) as pool:
            trace = a.play_one(Path(folder),manifest,spec,dict(left=FakeClient('B'),right=FakeClient('A')),pool)
            self.assertEqual(len(trace['rounds']),8)
            self.assertTrue(all(t['actions']==[1,0] and t['payoffs']==[5,2] for t in trace['rounds']))
            checkpoint = json.loads((Path(folder)/'episodes/test/round-02-player-1.json').read_text())
            self.assertIn('you A, other B; your points 2, other points 5',checkpoint['messages'][1]['content'])


if __name__ == '__main__': unittest.main()
