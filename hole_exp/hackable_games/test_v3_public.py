"""Public V3 must preserve the revised eval observations and transitions."""
import unittest
import catalog
from engines_v3_public import GAMES, TARGET_IDS, VERSION
from engines_v3_20260908 import GAMES as HISTORICAL


class PublicV3Tests(unittest.TestCase):
    def test_scope_and_historical_isolation(self):
        self.assertEqual(set(catalog.V3_IDS), set(GAMES))
        self.assertEqual(len(GAMES), 17)
        self.assertEqual(len(TARGET_IDS), 45)
        for gid, game in GAMES.items():
            self.assertIs(catalog.GAMES[gid]['game'], game)
            self.assertEqual(game.ENGINE_VERSION, VERSION)
        estate = GAMES['v3_ref_estate_neighbours']
        auction = GAMES['v3_ref_auction_room']
        self.assertEqual(estate.DIVIDEND, 0)
        self.assertEqual(auction.FEE, 0)
        self.assertNotIn('[waive: 1]', [f['token'] for f in estate.forms()])
        self.assertNotIn('[endorse: 1]', [f['token'] for f in auction.forms()])
        self.assertEqual(HISTORICAL[estate.NAME].DIVIDEND, 8)
        self.assertEqual(HISTORICAL[auction.NAME].FEE, 5)

    def test_reference_witness_replay(self):
        # The research package is absent from the public sparse deployment.
        try:
            from benchmark.fullscale.revised45 import study_games
            from benchmark.v3.specs import BY_ID
            from benchmark.v3.validate import witness
        except ImportError:
            self.skipTest('Research reference is not installed')
        reference = study_games()
        for target in TARGET_IDS:
            spec = BY_ID[target]
            for seed in (19, 73, 101):
                actual, expected = GAMES[spec.game_id], reference[spec.game_id]
                a, b = actual.initial(seed), expected.initial(seed)
                for action in witness(spec, seed):
                    self.assertEqual(actual.observe(a), expected.observe(b), (target, seed))
                    a, af = actual.transition(a, action)
                    b, bf = expected.transition(b, action)
                    self.assertEqual((a, af), (b, bf), (target, seed, action))


if __name__ == '__main__':
    unittest.main()
