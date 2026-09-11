import copy
import unittest

from prediction.games import make_game, payoff
from prediction.measurements import measure_episode


def episode(game, actions):
    return {"id": "ep", "game": game, "models": ["m0", "m1"], "trial_id": 0,
            "representation": "matrix", "swap": False, "status": "complete",
            "rounds": [{"round": i, "actions": list(a), "payoffs": list(payoff(game, *a))}
                       for i, a in enumerate(actions, 1)]}


class MeasurementTests(unittest.TestCase):
    def test_conditionals_count_actual_opportunities(self):
        game = make_game("pd", 3, 0, 5, 1)
        trace = episode(game, [(0,1),(1,0),(0,0),(0,1),(1,0),(1,0)])
        first, second = measure_episode(trace)
        self.assertEqual(first["targets"]["forgiveness"],
                         {"value": .5, "successes": 1, "opportunities": 2, "applicable": True})
        self.assertEqual(first["targets"]["retaliation"]["opportunities"], 2)
        self.assertEqual(first["targets"]["retaliation"]["value"], 1)
        self.assertEqual(first["targets"]["cooperation"]["successes"], 1)
        self.assertEqual(first["targets"]["individual_cooperation"]["successes"], 3)
        self.assertAlmostEqual(first["targets"]["defection_after_cooperation"]["value"], 1/3)
        self.assertAlmostEqual(first["descriptive"]["retaliation_difference"], 2/3)
        self.assertIsNone(second["targets"]["forgiveness"]["value"])
        self.assertEqual(first["split_metadata"], game["split_metadata"])

    def test_absent_opportunities_are_not_failures(self):
        game = make_game("pd", 3, 0, 5, 1)
        target = measure_episode(episode(game, [(0,0)] * 5))[0]["targets"]
        for name in ("retaliation", "forgiveness", "retaliation_after_exploitation"):
            self.assertEqual(target[name], {"value": None, "successes": 0, "opportunities": 0, "applicable": True})
        self.assertEqual(target["cooperation"]["value"], 1)
        self.assertEqual(target["coordination"], {"value": None, "successes": 0, "opportunities": 0, "applicable": False})
        empty = measure_episode(episode(game, []))[0]["targets"]
        self.assertIsNone(empty["action0"]["value"])
        self.assertIsNone(empty["first_action0"]["value"])

    def test_always_defect_has_zero_response_contrast(self):
        game = make_game("pd", 3, 0, 5, 1)
        row = measure_episode(episode(game, [(1,0),(1,1),(1,0),(1,1)]))[0]
        self.assertEqual(row["targets"]["retaliation"]["value"], 1)
        self.assertEqual(row["descriptive"]["retaliation_difference"], 0)
        self.assertIsNone(row["targets"]["retaliation_after_exploitation"]["value"])

    def test_coordination_counts_equilibria_not_matching(self):
        game = make_game("anti", 0, 3, 5, 0)
        rows = measure_episode(episode(game, [(0,0),(0,1),(1,0),(1,1)]))
        for row in rows:
            self.assertEqual(row["targets"]["coordination"]["successes"], 2)
            self.assertEqual(row["targets"]["coordination"]["opportunities"], 4)
            self.assertFalse(row["targets"]["cooperation"]["applicable"])
        stag = make_game("stag", 4, 0, 3, 2)
        row = measure_episode(episode(stag, [(0,0),(0,1),(1,1)]))[0]
        self.assertEqual(row["targets"]["coordination"]["successes"], 2)

    def test_extraction_gain_harm_and_sparse_opportunities(self):
        game = make_game("chicken", 4, 1, 6, 0)
        row = measure_episode(episode(game, [(1,0),(0,0),(0,1),(1,1)]))[0]
        self.assertEqual(row["targets"]["exploitation"],
                         {"value": .5, "successes": 1, "opportunities": 2, "applicable": True})
        row = measure_episode(episode(game, [(0,1),(1,1)]))[0]
        self.assertIsNone(row["targets"]["exploitation"]["value"])
        harmony = make_game("harmony", 5, 2, 3, 1)
        self.assertFalse(measure_episode(episode(harmony, [(0,0)]))[0]["targets"]["exploitation"]["applicable"])

    def test_role_and_action_swap_consistency(self):
        game = make_game("pd", 3, 0, 5, 1)
        first, second = measure_episode(episode(game, [(0,1)]))
        self.assertEqual(first["descriptive"]["total_payoff"], 0)
        self.assertEqual(second["descriptive"]["total_payoff"], 5)
        self.assertEqual(second["targets"]["exploitation"]["value"], 1)
        self.assertIsNone(first["targets"]["exploitation"]["value"])
        dd = measure_episode(episode(game, [(1,1)]))[0]["targets"]["exploitation"]
        self.assertEqual(dd, {"value": None, "successes": 0, "opportunities": 0, "applicable": True})
        self.assertEqual(first["pair"], second["pair"])
        actions = [(0,1),(1,0),(0,0),(1,1)]
        original = measure_episode(episode(game, actions))
        swapped = make_game("swapped", 1, 5, 0, 3)
        transformed = measure_episode(episode(swapped, [(1-a,1-b) for a,b in actions]))
        for left, right in zip(original, transformed):
            for name in ("cooperation", "retaliation", "forgiveness", "coordination", "exploitation"):
                self.assertEqual(left["targets"][name], right["targets"][name])
            self.assertAlmostEqual(left["targets"]["action0"]["value"], 1-right["targets"]["action0"]["value"])

    def test_reject_invalid_or_incomplete_traces(self):
        trace = episode(make_game("pd", 3, 0, 5, 1), [(0,1)])
        bad = copy.deepcopy(trace)
        bad["rounds"][0]["payoffs"].reverse()
        with self.assertRaisesRegex(ValueError, "player roles"):
            measure_episode(bad)
        bad = copy.deepcopy(trace)
        bad["status"] = "incomplete"
        with self.assertRaises(ValueError):
            measure_episode(bad)
        bad = copy.deepcopy(trace)
        bad["rounds"][0]["round"] = 2
        with self.assertRaises(ValueError):
            measure_episode(bad)


if __name__ == "__main__":
    unittest.main()
