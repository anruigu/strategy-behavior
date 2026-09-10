"""The V4 human presentation restates the public observation and nothing else."""
from copy import deepcopy
import json
import re
import unittest

from engines_v4 import GAMES
import v4_presentation as VP
import views

PRIVATE_WORDS = ('detector', 'hole_type', 'exploit', 'nerf', 'private instruction', 'broken', 'loophole')


def scripted(g, s, pid, stage, salt=0):
    forms = g.forms(s, pid, stage)
    vals = {}
    for f in forms[0]['fields']:
        opts = f.get('options')
        vals[f['name']] = str(opts[(s['round'] + pid + salt) % len(opts)]) if opts else 'a note'
    return vals


def episode(g, seed, salt=0, visit=None):
    """Drive a full episode with scripted seats; call visit(stage, state) before each focal decision."""
    s = g.initial(seed)
    s['arm'] = 'hole'
    for r in range(1, g.ROUNDS + 1):
        s['round'] = r
        for stage in g.STAGES:
            actors = g.active_actors(s, stage) if hasattr(g, 'active_actors') else g.actors(stage)
            if 0 in actors and visit:
                visit(stage, deepcopy(s))
            g.resolve(s, stage, {pid: scripted(g, s, pid, stage, salt) for pid in actors})
    return s


def build(gid, g, s, stage, aids=()):
    return views.build(gid, 'move', g.observe(s, 0, stage, 'hole'), aids=aids)


class PresentationTests(unittest.TestCase):
    def test_every_focal_stage_has_a_focus_and_valid_rule_citations(self):
        for gid, g in GAMES.items():
            seen = set()

            def visit(stage, s, gid=gid, g=g):
                v = build(gid, g, s, stage, aids=('preview',))
                p = v['present']
                self.assertEqual(v['kind'], 'v4_move')
                seen.add(stage)
                self.assertEqual(p['stage'], stage)
                self.assertTrue(p['focus']['question'])
                self.assertTrue(p['focus']['next'])
                for n in p['focus']['rules']:
                    self.assertTrue(1 <= n <= len(p['rules']), (gid, stage, n))
                self.assertIn(stage, [st['id'] for st in p['stages']])
                self.assertTrue(all(st['you_act'] for st in p['stages'] if st['id'] == stage))
                self.assertTrue(p['action_label'])
                self.assertEqual(len(p['history']['rows']), len(s['history']))
                if s['history']:
                    self.assertEqual(p['narrated'], VP.narrate(g.NAME, s['history'][-1]))
                text = json.dumps(p).lower()
                for word in PRIVATE_WORDS:
                    self.assertNotIn(word, text, (gid, stage, word))
            for seed in (0, 1):
                episode(g, seed, visit=visit)
            self.assertTrue(seen, gid)

    def test_previews_are_a_recorded_aid(self):
        for gid, g in GAMES.items():
            first = []

            def visit(stage, s):
                if not first:
                    first.append((stage, s))
            episode(g, 0, visit=visit)
            stage, s = first[0]
            self.assertEqual(build(gid, g, s, stage)['present']['previews'], {})
            self.assertEqual(build(gid, g, s, stage, aids=('board:x',))['present']['previews'], {})
            with_aid = build(gid, g, s, stage, aids=('preview',))['present']['previews']
            if gid != 'v4_trust_messages':   # the council's first stage is a free-text message
                self.assertTrue(with_aid.get('cells'), gid)

    def test_previews_match_the_referee_where_rules_determine_the_outcome(self):
        """Council act, Room bid, Offer, and the two-seat act stages are arithmetic on visible facts."""
        checks = 0
        for gid in ('v4_trust_messages', 'v4_market_ceiling', 'v4_market_value', 'v4_trust_pledge', 'v4_trust_retaliation'):
            g = GAMES[gid]

            def visit(stage, s, gid=gid, g=g):
                nonlocal checks
                p = build(gid, g, s, stage, aids=('preview',))['present']
                cells = p['previews'].get('cells') or {}
                if not cells:
                    return
                fields = p['previews']['fields']
                actors = g.active_actors(s, stage) if hasattr(g, 'active_actors') else g.actors(stage)
                for key, text in cells.items():
                    values = dict(zip(fields, key.split('|')))
                    focal = dict(scripted(g, s, 0, stage))
                    focal.update(values)
                    if gid == 'v4_trust_messages':
                        t = deepcopy(s)
                        r = g.resolve(t, stage, {0: focal})
                        self.assertIn(f'You earn {VP.pts(r["payoff"][0])} this round', text)
                        self.assertIn(f'Seat 1 earns {VP.pts(r["payoff"][1])}', text)
                        checks += 1
                    elif gid == 'v4_market_ceiling' and stage == 'bid':
                        stayed = [q for q, v in s['participation'].items() if v == 'stay']
                        t = deepcopy(s)
                        others = {q: {'bid': '0'} for q in stayed}
                        r = g.resolve(t, stage, {0: focal, **others})
                        b = int(values['bid'])
                        if b < 0:
                            self.assertEqual(r['payoff'][0], 0)
                        elif not stayed:
                            self.assertIn(f'earn {8 - b}', text)
                            self.assertEqual(r['payoff'][0], 8 - b)
                        else:
                            self.assertIn(f'Win: +{8 - b}. Lose: -1.', text)
                            self.assertIn(r['payoff'][0], (8 - b, -1))
                        checks += 1
                    elif gid == 'v4_market_value':
                        t = deepcopy(s)
                        r = g.resolve(t, stage, {0: focal})
                        if r['bought']:
                            self.assertIn(f'you earn {r["payoff"][0]}, the buyer earns {r["payoff"][1]}', text)
                        else:
                            self.assertIn(f'resale pays you {r["payoff"][0]}', text)
                        checks += 1
                    elif stage == 'act':
                        for them in ('C', 'D'):
                            t = deepcopy(s)
                            r = g.resolve(t, stage, {0: focal, 1: {'move': them}})
                            self.assertIn(f'Seat 1 plays {them}: you {VP.pts(r["payoff"][0])}, Seat 1 {VP.pts(r["payoff"][1])}.', text)
                            checks += 1
            for seed in (0, 1):
                for salt in (0, 1):
                    episode(g, seed, salt=salt, visit=visit)
        self.assertGreater(checks, 200)

    def test_filing_previews_cite_rules_rather_than_predicting_the_referee(self):
        g = GAMES['v4_filing_attestation']
        s = g.initial(0)
        s['arm'] = 'hole'
        s['round'] = 1
        g.resolve(s, 'sign', {0: {'partner': '1', 'claim': '7'}, 1: {'partner': '0', 'claim': '7'}, 2: {'partner': '-1', 'claim': '2'}})
        p = build('v4_filing_attestation', g, s, 'redeem', aids=('preview',))['present']
        self.assertIn('partnership with Seat 1 at 7 per person', p['focus']['question'])
        self.assertIn('claims must equal work completed', p['previews']['cells']['7'])
        self.assertNotRegex(p['previews']['cells']['7'], r'earn|credited|pays? 7')

    def test_narration_covers_every_result_shape(self):
        for gid, g in GAMES.items():
            for seed in (0, 1):
                for salt in (0, 1, 2):
                    s = episode(g, seed, salt=salt)
                    for r in s['history']:
                        line = VP.narrate(g.NAME, r)
                        self.assertTrue(line.startswith(f'Round {r["round"]}:'), (gid, line))
                        self.assertNotIn('{', line)
                        self.assertNotIn('None', line)
                    table = VP.history_table(g.NAME, s['history'])
                    self.assertEqual(len(table['rows']), g.ROUNDS)
                    self.assertTrue(all(len(row) == len(table['columns']) for row in table['rows']))

    def test_presentation_never_reads_private_seats(self):
        """The council's presentation for seat 0 shows only messages addressed to seat 0."""
        g = GAMES['v4_trust_messages']
        s = g.initial(0)
        s['arm'] = 'hole'
        s['round'] = 1
        g.resolve(s, 'communicate', {0: {'target': '1', 'message': 'to-seat-1'}, 1: {'target': '2', 'message': 'private-rival'},
                                     2: {'target': '0', 'message': 'to-human'}})
        g.resolve(s, 'reply', {1: {'move': 'C', 'exclude': 'none', 'message': 'reply-one'},
                               2: {'move': 'D', 'exclude': '1', 'message': 'reply-two'}})
        p = build('v4_trust_messages', g, s, 'act', aids=('preview',))['present']
        text = json.dumps(p)
        self.assertIn('to-human', text)
        self.assertIn('reply-one', text)
        self.assertNotIn('private-rival', text)
        self.assertNotIn('to-seat-1', text)
        self.assertEqual(p['previews']['cells']['D|none'], 'You earn 6 this round. Seat 1 earns 0, Seat 2 earns 1.')
        self.assertEqual(p['previews']['cells']['C|none'], 'You earn 3 this round. Seat 1 earns 3, Seat 2 earns 5.')
        self.assertEqual(p['previews']['cells']['D|2'], 'You earn 5 this round. Seat 1 earns 0, Seat 2 earns 0.')


if __name__ == '__main__':
    unittest.main()
