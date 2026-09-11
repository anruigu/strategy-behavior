"""Human eval parity, policy isolation, traces and simultaneous-stage checks."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import catalog
from collector import PlayCollector
from engines_v3_ma import GAMES as ORIGINAL, parse
from engines_v4 import GAMES, PROTOCOL, FROZEN_PROTOCOL, HumanEval, VERSION
from v4_features import structural_features
from eval_opponents import EvalOpponent
import play_server
import views


def table(prompt):
    return json.loads(re.search(r'^Table: (.+)$', prompt, re.M)[1])


def choice(pid, phase, prompt):
    forms = json.loads(re.search(r'^Actions: (.+)$', prompt, re.M)[1])
    t = table(prompt)
    values = {}
    for f in forms[0]['fields']:
        options = f.get('options', [])
        values[f['name']] = options[(t['round'] + pid) % len(options)] if options else 'Please cooperate'
    return ' '.join(f'[{k}: {v}]' for k, v in values.items())


class Client:
    def __init__(self, replies=None):
        self.replies = list(replies or [])
        self.calls = []
        self.chat = SimpleNamespace(completions=self)
    def create(self, **kw):
        self.calls.append(deepcopy(kw))
        if self.replies:
            text = self.replies.pop(0)
        else:
            prompt = kw['messages'][-1]['content']
            text = choice(table(prompt)['seat'], 'move', prompt)
        return SimpleNamespace(model=kw['model'], usage=None,
            choices=[SimpleNamespace(finish_reason='stop', message=SimpleNamespace(content=text))])


class V4Tests(unittest.TestCase):
    def test_frozen_engine_and_roster(self):
        self.assertEqual(len(GAMES), 10)
        self.assertEqual(len(catalog.V0_IDS), 19)
        self.assertTrue(all(g.family != 'commons' for g in GAMES.values()))
        path = Path(__file__).with_name('engines_v3_ma.py')
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), FROZEN_PROTOCOL['source_hashes']['hole_exp/hackable_games/engines_v3_ma.py'])
        for gid in GAMES:
            self.assertTrue(views.build(play_server._board_gid(gid), 'move', GAMES[gid].observe(GAMES[gid].initial(0),0,GAMES[gid].STAGES[0],'hole')))

    def test_every_observation_action_resolution_and_score_matches_eval(self):
        for gid, game in GAMES.items():
            for seed in (0, 1):
                with self.subTest(game=gid, seed=seed):
                    reference = ORIGINAL[game.ORIGINAL].run(choice, seed, 'hole')
                    frozen = HumanEval(ORIGINAL[game.ORIGINAL])
                    frozen.ENGINE_VERSION = 'v4-human-eval-1'
                    actual = frozen.run(choice, seed, 'hole')
                    self.assertEqual(actual.scores, reference.scores)
                    self.assertEqual(actual.decisions, reference.decisions)
                    self.assertEqual(actual.extras['events'], reference.extras['events'])

    def test_independent_seats_start_together(self):
        for gid in ('v4_trust_messages', 'v4_market_ceiling', 'v4_filing_settlement'):
            g = GAMES[gid]
            barriers = {}
            def ask(pid, phase, prompt):
                t = table(prompt)
                # Dynamic Room bid stages omit rivals who already withdrew.
                n = len(g.actors(t['stage']))
                if t['stage'] == 'bid':
                    n = 1 + sum(v == 'stay' for v in t['participation'].values())
                key = (t['round'], t['stage'])
                barrier = barriers.setdefault(key, threading.Barrier(n, timeout=3))
                barrier.wait()
                return choice(pid, phase, prompt)
            g.run(ask,0,'hole')

    def test_policy_only_changes_designated_recipients(self):
        for gid in GAMES:
            canonical=GAMES[gid].ORIGINAL
            policy = PROTOCOL['systems'][canonical]
            self.assertEqual(policy['ordinary']['0'], policy['nerfed']['0'])
            self.assertEqual(policy['ordinary']['0'], policy['defensive']['0'])
            self.assertNotEqual(policy['ordinary']['1'], policy['nerfed']['1'])
            self.assertNotEqual(policy['ordinary']['2'],policy['nerfed']['2'])
            self.assertEqual(policy['nerfed']['1'],policy['nerfed']['2'])

    def test_exact_prompts_settings_private_memory_and_correction(self):
        game=GAMES['v4_trust_pledge']; s=game.initial(0)
        prompt=game.observe(s,1,'communicate','hole')
        client=Client(['[move: C]', '[statement: pledge]', '[statement: none]'])
        bot=EvalOpponent(game.ORIGINAL,'nerfed','glm',client)
        self.assertEqual(bot(1,'move',prompt),'[statement: pledge]')
        first, repair=client.calls
        self.assertEqual(first['messages'],[{'role':'system','content':PROTOCOL['systems'][game.ORIGINAL]['nerfed']['1']},{'role':'user','content':prompt}])
        self.assertEqual(first['model'],'glm-5.3')
        self.assertEqual(first['max_tokens'],8192)
        self.assertNotIn('temperature',first)
        self.assertEqual(first['reasoning'],{'effort':'low'})
        self.assertIn('No game action has occurred.',repair['messages'][-1]['content'])
        bot(2,'move',prompt)
        self.assertEqual(len(client.calls[-1]['messages']),2)
        self.assertEqual(client.calls[-1]['messages'][0]['content'],PROTOCOL['systems'][game.ORIGINAL]['nerfed']['2'])
        self.assertEqual(len([r for r in bot.records if r.get('format_error')]),1)

    def test_invalid_opponent_never_becomes_scripted(self):
        g=GAMES['v4_signal_notes']; s=g.initial(0)
        s['clue']={'axis':'red','matching_slots':[1,2],'message':'none'}
        c=Client(['[play: 999]','[play: 999]'])
        bot=EvalOpponent(g.ORIGINAL,client=c)
        with self.assertRaises(RuntimeError): bot(1,'move',g.observe(s,1,'play','hole'))
        self.assertEqual(len(c.calls),2)

    def test_human_has_only_focal_information(self):
        g=GAMES['v4_trust_messages']; s=g.initial(0); s['arm']='hole'
        g.resolve(s,'communicate',{0:{'target':'1','message':'from-human'},1:{'target':'2','message':'private-rival'},2:{'target':'0','message':'to-human'}})
        prompt=g.observe(s,0,'act','hole')
        self.assertIn('to-human',prompt)
        self.assertNotIn('private-rival',prompt)
        self.assertNotIn('enact this strategy',prompt)
        signal=GAMES['v4_signal_notes']; s=signal.initial(0)
        rival=signal.observe(s,1,'play','hole')
        self.assertNotIn('marked_slot',rival)
        self.assertNotIn('targets',rival)

    def test_referee_patch_rejected(self):
        for g in GAMES.values():
            with self.assertRaises(ValueError): g.run(choice,0,'nohole')

    def test_run_traces_seeds_fresh_memory_and_final_view(self):
        made=[]
        def factory(game_id, condition='nerfed', model='qwen-3.8-27b'):
            bot=EvalOpponent(game_id,condition,model,Client()); made.append(bot)
            bot.fresh=lambda:factory(game_id,condition,model)
            return bot
        with tempfile.TemporaryDirectory() as tmp, patch('eval_opponents.EvalOpponent',side_effect=factory):
            c=PlayCollector(tmp)
            run=play_server.Run('eval-test','v4_signal_notes','hole',2,'ai',0,c,[],opponent='glm',condition='ordinary',seed=0)
            for seed in (0,1):
                session=run.start_next()
                deadline=time.time()+5
                while not session.done.is_set() and time.time()<deadline:
                    if session.pending:
                        turn=session.turn
                        prompt=session.pending['prompt']
                        session.submit(choice(0,'move',prompt))
                        while session.pending and session.turn==turn and time.time()<deadline: time.sleep(.002)
                    else: time.sleep(.002)
                self.assertTrue(session.done.is_set())
                self.assertIsNone(session.error)
                state=session.public_state()
                self.assertEqual(len(state['final_view']['public_state']['history']),4)
                self.assertNotIn('systems',json.dumps(state))
                run.close_play()
            rows=c.player_plays('eval-test')
            self.assertEqual([r['seed'] for r in rows],[0,1])
            self.assertEqual(len(made),2)
            for r in rows:
                self.assertEqual(r['study']['condition'],'ordinary')
                self.assertEqual(r['opponent']['model_key'],'glm')
                self.assertEqual(r['schema'],6)
                self.assertEqual(r['engine_version'], VERSION)
                self.assertEqual(r['study']['protocol'], 'v4-human-playtest.3')
                self.assertIn('engines_v4_revision.py', r['study']['source_hashes'])
                self.assertIn('structural_features', r['engine_trace'])
                self.assertEqual(len(r['engine_trace']['events']),8)
                self.assertTrue(all(m['observation'] for m in r['moves']))
                self.assertEqual(r['moves'][0]['observation'],r['engine_trace']['events'][0]['decisions'][0]['observation'])
            run.kill()

    def test_completed_stages_survive_abandonment(self):
        with tempfile.TemporaryDirectory() as tmp:
            c=PlayCollector(tmp)
            pid=c.start(player='partial',game='v4_signal_notes',seat=0,arm='hole',seed=0,bots='ai',run_id='run',play_index=0,study={'condition':'nerfed'})
            c.record_engine_event(pid,{'stage':'clue','actions':{'0':{'clue':'red','message':'none'}}})
            c.finish(pid,None,abandoned=True)
            row=c.player_plays('partial')[0]
            self.assertTrue(row['abandoned'])
            self.assertEqual(row['engine_trace']['events'][0]['stage'],'clue')
            self.assertEqual(row['study']['condition'],'nerfed')


if __name__ == '__main__': unittest.main()
