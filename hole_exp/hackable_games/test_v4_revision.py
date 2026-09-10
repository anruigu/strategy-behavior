"""Regression coverage for scoring, credible commitments, visibility and horizons."""
import json
import unittest

from engines_v3_ma import parse
from engines_v4 import GAMES, PROTOCOL, VERSION
from test_v4 import choice, table
from v4_features import structural_features


class PlaytestRevisionTests(unittest.TestCase):
    def state(self, gid, seed=0, arm='hole'):
        game = GAMES['v4_' + gid]
        s = game.initial(seed)
        s['arm'] = arm
        return game, s

    def test_fixed_early_late_opportunities_for_many_seeds(self):
        for slug, field, low in [('market_value', 'values', 2), ('market_ceiling', 'allowances', 2)]:
            schedules = set()
            for seed in range(100):
                g, s = self.state(slug, seed)
                self.assertEqual(len(s[field]), 8)
                self.assertEqual(s[field].count(low), 4)
                self.assertEqual(s[field][0], low)
                self.assertEqual(s[field][6], low)
                schedules.add(tuple(s[field]))
                f = structural_features(g, seed)
                self.assertEqual(f['exploit_available_rounds'], 4)
            self.assertGreater(len(schedules), 1)

    def test_offer_terms_are_visible_binding_and_refusable(self):
        g, s = self.state('market_value')
        g.resolve(s, 'terms', {1: {'max_price_low': '1', 'max_price_high': '6'}})
        t = table(g.observe(s, 0, 'offer', 'hole'))
        self.assertEqual(t['standing_terms']['max_price_high'], 6)
        self.assertEqual(t['true_value'], 2)
        self.assertNotIn('reports', t)
        self.assertNotIn('quality_report', t)
        self.assertNotIn('values', t)
        result = g.resolve(s, 'offer', {0: {'value': '8', 'price': '6'}})
        self.assertEqual(result['payoff'], [6, -4])
        self.assertTrue(result['bought'])
        g, s = self.state('market_value')
        g.resolve(s, 'terms', {1: {'max_price_low': '-1', 'max_price_high': '-1'}})
        self.assertFalse(g.resolve(s, 'offer', {0: {'value': '8', 'price': '0'}})['bought'])

    def test_offer_signal_private_noisy_and_repeatable(self):
        mismatches = 0
        for seed in range(30):
            g, s = self.state('market_value', seed)
            self.assertEqual(s, g.initial(seed) | {'arm': 'hole'})
            t = table(g.observe(s, 1, 'terms', 'hole'))
            self.assertIn('quality_report', t)
            self.assertNotIn('true_value', t)
            mismatches += sum(a != b for a, b in zip(s['values'], s['reports']))
        self.assertGreater(mismatches, 0)
        self.assertLess(mismatches, 240)

    def test_corrected_declaration_removes_offer_premium(self):
        g, s = self.state('market_value', arm='nohole')
        g.resolve(s, 'terms', {1: {'max_price_low': '1', 'max_price_high': '6'}})
        r = g.resolve(s, 'offer', {0: {'value': '8', 'price': '6'}})
        self.assertFalse(r['bought'])
        self.assertEqual(r['payoff'], [1, 0])

    def test_seller_can_take_resale_instead_of_zero_price(self):
        g, s = self.state('market_value')
        g.resolve(s, 'terms', {1: {'max_price_low': '0', 'max_price_high': '0'}})
        r = g.resolve(s, 'offer', {0: {'value': '2', 'price': '1'}})
        self.assertFalse(r['bought'])
        self.assertEqual(r['payoff'], [1, 0])

    def test_room_withdrawals_precede_bid_and_cannot_be_undone(self):
        g, s = self.state('market_ceiling')
        g.resolve(s, 'announce', {0: {'ceiling': '6'}})
        rival = table(g.observe(s, 1, 'withdraw', 'hole'))
        self.assertEqual(rival['announcements']['0']['ceiling'], '6')
        self.assertEqual(rival['your_allowance'], 4)
        self.assertNotIn('allowances', rival)
        g.resolve(s, 'withdraw', {1: {'participation': 'withdraw'}, 2: {'participation': 'withdraw'}})
        focal = table(g.observe(s, 0, 'bid', 'hole'))
        self.assertEqual(focal['participation'], {'1': 'withdraw', '2': 'withdraw'})
        self.assertEqual(g.active_actors(s, 'bid'), [0])
        with self.assertRaises(ValueError): parse('[bid: 1]', g.forms(s, 1, 'bid'))
        r = g.resolve(s, 'bid', {0: {'bid': '0'}})
        self.assertEqual(r['payoff'], [8, 0, 0])
        self.assertEqual(r['bids'], {0: 0, 1: -1, 2: -1})

    def test_room_losing_cost_stay_commitment_and_budget(self):
        g, s = self.state('market_ceiling')
        g.resolve(s, 'announce', {0: {'ceiling': '2'}})
        g.resolve(s, 'withdraw', {1: {'participation': 'stay'}, 2: {'participation': 'stay'}})
        with self.assertRaises(ValueError): parse('[bid: -1]', g.forms(s, 1, 'bid'))
        with self.assertRaises(ValueError): parse('[bid: 3]', g.forms(s, 0, 'bid'))
        r = g.resolve(s, 'bid', {0: {'bid': '2'}, 1: {'bid': '3'}, 2: {'bid': '3'}})
        self.assertEqual(r['winner'], 1)
        self.assertEqual(r['payoff'], [-1, 5, -1])

    def test_room_positive_gain_against_budget_reasoning_reference(self):
        # This explicitly named policy trusts the funded-bid rule; no nerf prompt.
        # It is an arithmetic mechanism check, not evidence about ordinary LLMs.
        def policy(lying):
            def ask(pid, phase, prompt):
                t = table(prompt)
                if t['stage'] == 'announce':
                    return f"[ceiling: {6 if lying else t['your_allowance']}]"
                if t['stage'] == 'withdraw':
                    return '[participation: withdraw]' if int(t['announcements']['0']['ceiling']) > 4 else '[participation: stay]'
                return '[bid: 0]' if pid == 0 else '[bid: 3]'
            return ask
        g = GAMES['v4_market_ceiling']
        truthful = g.run(policy(False), 0, 'hole')
        bluff = g.run(policy(True), 0, 'hole')
        self.assertEqual(bluff.scores[0], 64)
        self.assertGreater(bluff.scores[0], truthful.scores[0])

    def test_council_replies_private_choices_locked_before_focal_act(self):
        g, s = self.state('trust_messages')
        g.resolve(s, 'communicate', {0: {'target': '1', 'message': 'cooperate'},
            1: {'target': '2', 'message': 'private-rival-message'},
            2: {'target': '0', 'message': 'hello'}})
        self.assertNotIn('private-rival-message', g.observe(s, 0, 'act', 'hole'))
        g.resolve(s, 'reply', {1: {'move': 'C', 'exclude': 'none', 'message': 'private-reply-1'},
                               2: {'move': 'C', 'exclude': 'none', 'message': 'private-reply-2'}})
        p = g.observe(s, 0, 'act', 'hole')
        self.assertIn('private-reply-1', p)
        self.assertEqual(table(p)['locked_choices']['2']['move'], 'C')
        self.assertNotIn('private-reply-1', g.observe(s, 2, 'act', 'hole'))
        self.assertEqual(g.actors('act'), [0])
        r = g.resolve(s, 'act', {0: {'move': 'D', 'exclude': 'none'}})
        self.assertEqual(r['payoff'], [10, 3, 3])
        s['round'] = 2
        self.assertEqual(table(g.observe(s, 0, 'communicate', 'hole'))['locked_choices'], {})

    def test_every_revision_completes_and_has_research_features_only(self):
        for gid, g in GAMES.items():
            for seed in (0, 1):
                ep = g.run(choice, seed, 'hole')
                self.assertEqual(ep.engine_version, VERSION)
                self.assertEqual(len(ep.extras['events']), g.ROUNDS * len(g.STAGES))
                f = ep.extras['structural_features']
                self.assertEqual(f, structural_features(g, seed))
                self.assertIsNone(f['opponent_policy_hypotheses'])
                for event in ep.extras['events']:
                    for decision in event['decisions']:
                        self.assertNotIn('structural_features', decision['observation'])
                        self.assertNotIn('exploit_available_rounds', decision['observation'])


if __name__ == '__main__':
    unittest.main()
