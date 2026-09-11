import json
import math
import random
import re
import unittest

from prediction.games import generate_games, make_game, payoff, render_game


class GameTests(unittest.TestCase):
    def test_asymmetric_outcomes_keep_player_roles(self):
        game = make_game("pd", 3, 0, 5, 1)
        self.assertEqual(payoff(game, 0, 1), (0, 5))
        self.assertEqual(payoff(game, 1, 0), (5, 0))
        self.assertEqual(game["pure_nash"], [[1, 1]])
        self.assertEqual(game["applicability"]["cooperative_action"], 0)
        self.assertEqual(game["features"]["strict_dominant_action1"], 1)

    def test_known_equilibria_and_welfare(self):
        stag = make_game("stag", 4, 0, 3, 2)
        self.assertEqual(stag["pure_nash"], [[0, 0], [1, 1]])
        self.assertEqual(stag["pareto_outcomes"], [[0, 0]])
        self.assertAlmostEqual(stag["features"]["mixed_equilibrium_action0_probability"], 2 / 3)
        chicken = make_game("chicken", 4, 1, 6, 0)
        self.assertEqual(chicken["pure_nash"], [[0, 1], [1, 0]])
        self.assertAlmostEqual(chicken["features"]["mixed_equilibrium_action0_probability"], 1 / 3)
        self.assertEqual(chicken["applicability"]["coordination_outcomes"], [[0, 1], [1, 0]])
        self.assertFalse(make_game("alternation", 3, 2, 6, 0)["applicability"]["cooperation"])
        equal = make_game("equal", 1, 1, 1, 1)
        self.assertEqual(len(equal["pure_nash"]), 4)
        self.assertEqual(len(equal["pareto_outcomes"]), 4)
        self.assertEqual(equal["features"]["has_interior_mixed_equilibrium"], 1)
        self.assertEqual(equal["features"]["interior_mixed_equilibrium_unique"], 0)
        self.assertFalse(equal["applicability"]["coordination"])

    def test_swap_affine_groups_and_coordinates(self):
        rng = random.Random(9)
        for i in range(100):
            values = [rng.uniform(-10, 10) for _ in range(4)]
            original = make_game(i, *values)
            scale, shift = rng.uniform(.1, 12), rng.uniform(-20, 20)
            transformed = make_game(f"t{i}", *(scale * x + shift for x in reversed(values)))
            self.assertEqual(original["group_id"], transformed["group_id"])
            self.assertEqual(original["family"], transformed["family"])
            for key in ("canonical_s", "canonical_t"):
                self.assertAlmostEqual(original["split_metadata"][key], transformed["split_metadata"][key])
            self.assertEqual(original["applicability"]["cooperation"], transformed["applicability"]["cooperation"])
            if original["applicability"]["cooperation"]:
                self.assertEqual(original["applicability"]["cooperative_action"], 1 - transformed["applicability"]["cooperative_action"])
        self.assertNotEqual(make_game("a", 3, 0, 5, 1)["group_id"], make_game("b", 3, 0, 6, 1)["group_id"])
        tied = make_game("tied", 1, 0, 2, 1)
        reversed_tied = make_game("reversed", 1, 2, 0, 1)
        self.assertEqual(tied["group_id"], reversed_tied["group_id"])
        self.assertEqual(tied["family"], "dominance")
        self.assertEqual(tied["family"], reversed_tied["family"])

    def test_generator_reproducible_diverse_and_serializable(self):
        games = generate_games()
        self.assertEqual(games, generate_games())
        self.assertNotEqual(games, generate_games(seed=1))
        self.assertEqual(len(games), 24)
        self.assertEqual(len({g["group_id"] for g in games}), 24)
        self.assertEqual({g["family"] for g in games}, {
            "prisoners_dilemma", "stag_hunt", "chicken", "harmony",
            "coordination", "anti_coordination", "weak_dominance"})
        self.assertTrue(all(math.isfinite(v) for g in games for v in g["features"].values()))
        self.assertTrue(all(round(v, 2) == v for g in games for v in g["payoffs"].values()))
        json.dumps(games, allow_nan=False)
        self.assertEqual(generate_games(n=0), [])

    def test_every_renderer_encodes_exact_values_after_swap(self):
        game = make_game("g", 3.123456789123456, -.87654321234567, 5.22, .01)
        number = r"(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)"
        for swap in (False, True):
            indices = (1, 0) if swap else (0, 1)
            for representation in ("matrix", "text", "narrative"):
                text = render_game(game, representation, swap)
                self.assertNotRegex(text.lower(), "prisoner|cooperat|defect|harmony|stag|chicken")
                if representation == "matrix":
                    parsed = [(float(a), float(b)) for a, b in re.findall(r"\(" + number + ", " + number + r"\)", text)]
                else:
                    parsed = [(float(a), float(b)) for a, b in re.findall("you receive " + number + " points and the other participant receives " + number + " points", text)]
                expected = [payoff(game, indices[a], indices[b]) for a, b in ((0,0),(0,1),(1,0),(1,1))]
                self.assertEqual(parsed, expected)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            make_game("bad", math.nan, 0, 1, 2)
        with self.assertRaises(ValueError):
            make_game("bad", 1, 0, 2, 3, features={})
        with self.assertRaises(ValueError):
            payoff(make_game("g", 3, 0, 5, 1), True, 0)
        with self.assertRaises(ValueError):
            generate_games(n=-1)


if __name__ == "__main__":
    unittest.main()
