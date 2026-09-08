"""Decision boundaries, private observations, and committed actions for V4."""
import json
import unittest
from copy import copy, deepcopy
import engines_v4 as V4
import engines_v3_20260908 as V3


def observation(prompt):
    return json.loads(prompt.split('\nObservation: ', 1)[1].split('\nDecision:', 1)[0])


class V4Tests(unittest.TestCase):
    def bind(self, gid, answer='[choice: 0]'):
        game = copy(V4.GAMES[gid])
        game._ep = game._new(0, 'hole')
        game._decisions = []
        game._ask = lambda *args: answer
        return game

    def test_same_editions_and_human_actions(self):
        self.assertEqual(len(V4.GAMES), 19)
        for game in V4.GAMES.values():
            base = V3.GAMES[game.ORIGINAL]
            self.assertEqual([(f['label'], f['token'], f['fields']) for f in game.forms()],
                             [(f['label'], f['token'], f['fields']) for f in base.forms()])
            self.assertEqual(game.CARD['scoring'], base.CARD['scoring'])
            self.assertEqual(game.ROUNDS, base.ROUNDS)

    def test_simultaneous_move_not_disclosed(self):
        for gid, action in [('v4_ta_ipd_palmers_word', 'move'), ('v4_ta_ipd3_alliances', 'move'), ('v4_ta_winasmuch_talk', 'pick')]:
            self.assertIn(gid, V4.GAMES)
            prompts = []
            for value in (('cooperate', 'defect') if action == 'move' else ('X', 'Y')):
                game = self.bind(gid)
                calls = []
                def ask(pid, phase, prompt):
                    if phase in ('move', 'pick'): calls.append(prompt)
                    return '[choice: 0]'
                game._ask = ask
                game.transition(game.initial(0), f'[{action}: {value}]')
                prompts.append(calls)
            self.assertEqual(prompts[0], prompts[1], gid)
            self.assertTrue(prompts[0])

    def test_model_controls_retaliation_without_counterfactual_calls(self):
        game = V4.GAMES['v4_ta_ipd_palmers_word']
        calls = []
        def ask(pid, phase, prompt):
            if pid: calls.append(prompt); return '[choice: 1]'
            return '[move: cooperate]'
        ep = game.run(ask, 0, 'hole')
        self.assertEqual(len(calls), 8)
        self.assertEqual(ep.scores[0], 0)
        self.assertEqual(ep.scores[1], 42)
        self.assertFalse(hasattr(game, '_ask'))

    def test_auction_bid_lock_and_privacy(self):
        game = self.bind('v4_ref_auction_lots', '[choice: 3]')
        s = game.initial(0)
        game.prepare(s)
        self.assertEqual(s['rival_bids'][0], [3, 3])
        game.prepare(s)
        self.assertEqual(len(game._decisions), 2)
        o = game.opponent_observation(s, 1)
        self.assertNotIn('rival_bids', o)
        self.assertNotIn('open_bids', o)
        s, _ = game.transition(s, '[wait: 1]')
        self.assertEqual(s['open_bids'], [3, 3])
        game.prepare(s)
        self.assertEqual(len(game._decisions), 2)

    def test_battleship_warning_is_model_shot_and_hull_hidden(self):
        game = self.bind('v4_ref_battleship_patrol', '[choice: 0]')
        s = game.initial(0)
        game.prepare(s)
        self.assertEqual(s['warning'], 'A1')
        o = game.opponent_observation(s, 1)
        s['own_hull'] = ['D4']
        self.assertEqual(o, game.opponent_observation(s, 1))
        s['own_hull'] = ['A1']
        after, _ = game.transition(s, '[fire: D4]')
        self.assertNotIn('A1', after['own_hull'])

    def test_hanabi_model_can_reject_slot_instruction_and_cannot_see_own_cards(self):
        game = self.bind('v4_ref_hanabi_clues')
        game.native = V4.Partner(); game.native.owner = game
        s = game.initial(0)
        self.assertEqual(s['known'], [{}, {}, {}])
        calls = []
        def ask(pid, phase, prompt):
            calls.append((pid, phase, prompt))
            return '[choice: 1]' if phase == 'play' else '[choice: 0]'
        game._ask = ask
        game.prepare(s)
        card = s['hands'][1][0]
        after, facts = game.transition(s, f'[clue: player 1, {card[0]}; play slot 1]')
        self.assertEqual(facts['chosen'], 1)
        p = next(prompt for _, phase, prompt in calls if phase == 'play')
        o = observation(p)
        self.assertNotIn('1', o['visible_hands'])
        self.assertEqual(len(o['own_marks']), 3)
        self.assertIn('play slot 1', p)
        self.assertEqual(len(after['_marks'][1]), 2)

    def test_invalid_model_reply_has_no_fallback(self):
        game = self.bind('v4_ta_ipd_palmers_word', 'cooperate')
        with self.assertRaisesRegex(RuntimeError, 'no scripted fallback'):
            game.transition(game.initial(0), '[move: defect]')


if __name__ == '__main__': unittest.main()
