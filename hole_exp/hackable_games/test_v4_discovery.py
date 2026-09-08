"""V4's labeled, controlled opponent-discovery experiments. Offline only."""
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import catalog
import play_server as P
import views
from collector import PlayCollector
from test_views import _from_view
from test_holefill import gate_paired, gate_pays, gate_deters, gate_surfaced


class DiscoveryTests(unittest.TestCase):
    def test_reference_roster_and_normal_ai_preserved(self):
        reference = Path(__file__).resolve().parents[2] / 'results/0904_bverif1/discovery_nerfed3.json'
        if reference.exists():
            self.assertEqual(set(json.loads(reference.read_text())['cells']), set(catalog.V4_DISCOVERY_CELLS))
        self.assertEqual(len(catalog.V4_DISCOVERY_IDS), 16)
        menu = [c for c in P.public_catalogue() if c['edition'] == 'v4']
        self.assertEqual(len(menu), 15)
        for gid in catalog.V4_IDS:
            choices = catalog.V4_CHOICES[catalog.GAMES[gid]['base']]
            self.assertEqual(choices[0]['cell'], gid)
            self.assertEqual(choices[0]['label'], 'Normal · AI')
        offered = {v['cell'] for row in menu for v in row['variants']}
        self.assertTrue(set(catalog.V4_DISCOVERY_IDS) <= offered)

    def test_conditions_identical_until_probed_and_have_payoff_consequence(self):
        for source in catalog.V4_DISCOVERY_CELLS:
            g = catalog.GAMES[source]['game']
            for gate in (gate_paired, gate_pays, gate_deters, gate_surfaced):
                with self.subTest(source=source, gate=gate.__name__):
                    passed, detail = gate(g)
                    self.assertTrue(passed, detail)

    def test_all_variants_play_without_inference_and_record_conditions(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(P, 'HostedOpponent', side_effect=AssertionError('No inference allowed')):
            collector = PlayCollector(tmp)
            for gid in catalog.V4_DISCOVERY_IDS:
                with self.subTest(gid=gid):
                    run = P.Run('tester', gid, 'wrong-arm', 1, 'ai', 0, collector, [])
                    self.assertEqual(run.arm, catalog.GAMES[gid]['fixed_arm'])
                    self.assertEqual(run.bots, 'honest')
                    session = run.start_next()
                    self.drive(run)
                    self.assertIsNone(session.error)
                    P.Handler._settle(object.__new__(P.Handler), run)
                    row = collector.player_plays('tester')[-1]
                    self.assertFalse(row['abandoned'])
                    self.assertEqual(row['opponent']['condition'], catalog.GAMES[gid]['opponent_condition'])
                    self.assertIn('engine_events', row['opponent'])

    def drive(self, run):
        s = run.session
        deadline = time.monotonic() + 5
        turn = 0
        while not s.done.is_set() and time.monotonic() < deadline:
            state = s.public_state()
            if state.get('pending') and state['turn'] != turn:
                turn = state['turn']
                p = state['pending']
                self.assertIsNotNone(p['view'], (run.gid, p['phase']))
                s.submit(_from_view(p['view'], p['phase'], p['prompt']))
            time.sleep(.001)
        self.assertTrue(s.done.is_set())

    def test_discovery_after_settlement_is_durable_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            collector = PlayCollector(tmp)
            run = P.Run('tester', 'v4_gen_seven_seal_nerfed', 'hole', 2, 'honest', 0, collector, [])
            run.start_next()
            self.drive(run)
            run.close_play()
            moves = len(run.session.history)
            first = run.mark_discovery('The rivals do not act after my test.')
            self.assertEqual(first['total_moves'], moves)
            self.assertEqual(run.mark_discovery('a retry'), first)
            path = Path(tmp) / 'players/tester/discoveries.jsonl'
            events = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]['condition'], 'nerfed')
            self.assertEqual(events[0]['source_game'], 'hf_seven_seal_nerfed')
            self.assertGreaterEqual(first['elapsed_s'], 0)
            run.start_next()
            run.kill()
            self.assertEqual(len(path.read_text().splitlines()), 1)

    def test_announced_deterrent_is_visible_on_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = P.Run('tester', 'v4_gen_seven_seal_responsive', 'hole', 1, 'honest', 0, PlayCollector(tmp), [])
            s = run.start_next()
            deadline = time.monotonic() + 2
            while not s.pending and time.monotonic() < deadline:
                time.sleep(.001)
            self.assertIn('NOTICE', s.public_state()['table_notice'])
            self.assertIn('inspection', s.public_state()['table_notice'])
            run.kill()


if __name__ == '__main__':
    unittest.main()
