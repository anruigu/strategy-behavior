import copy
import json
from pathlib import Path
import tempfile
import unittest

from prediction.diagnostics import build_diagnostics, derive_target, run, summarize_support, validate_records


def record(game, trial, s, n, model="m0", opponent="m1", target="action0", applicable=True):
    return {"episode_id": f"{game}:{model}:{opponent}:{trial}", "game_id": game, "group_id": game,
            "family": "family", "model": model, "opponent": opponent, "trial_id": trial,
            "player_index": 0, "representation": "matrix", "swap": bool(trial % 2),
            "targets": {target: {"successes": s, "opportunities": n,
                                    "value": s/n if n else None, "applicable": applicable}}}


class DiagnosticsTests(unittest.TestCase):
    def test_macro_is_equal_game_and_conditionals_pool_events(self):
        rows = [record("g1", 0, 0, 1), record("g1", 1, 9, 9), record("g2", 0, 0, 100)]
        support = summarize_support(rows, "action0")
        self.assertAlmostEqual(support["equal_game_macro_rate"], .45)
        self.assertAlmostEqual(support["pooled_event_rate"], 9/110)
        self.assertEqual(support["eligible_trials"], 3)
        self.assertEqual(support["opportunities"], 110)

    def test_missing_unsupported_and_no_opportunity_are_distinct(self):
        rows = [record("g", 0, 0, 0), record("g", 1, 0, 0, applicable=False)]
        extra = record("g", 2, 0, 0)
        extra["targets"] = {}
        rows.append(extra)
        support = summarize_support(rows, "action0")
        self.assertEqual(support["applicable_rows"], 1)
        self.assertEqual(support["unsupported_rows"], 1)
        self.assertEqual(support["missing_target_rows"], 1)
        self.assertEqual(support["eligible_trials"], 0)
        self.assertIsNone(support["equal_game_macro_rate"])

    def test_split_half_pools_counts_and_requires_all_trials_and_labels(self):
        rows = [record("g", 0, 0, 1), record("g", 1, 9, 9),
                record("g", 2, 5, 10), record("g", 3, 0, 0)]
        derived = derive_target(rows, "action0")
        self.assertAlmostEqual(derived["cell_points"][0]["left"], .9)
        self.assertAlmostEqual(derived["cell_points"][0]["right"], .5)
        self.assertEqual(derived["cell_points"][0]["halves"][1]["eligible_trials"], 1)
        self.assertEqual(derive_target(rows[:-1], "action0")["excluded_cells"], {"missing_design_trial": 1})
        for row in rows:
            row["swap"] = False
        self.assertEqual(derive_target(rows, "action0")["excluded_cells"], {"label_composition_unbalanced_or_unknown": 1})

    def test_constant_correlation_is_null_not_perfect_reliability(self):
        rows = [record(f"g{game}", trial, 1, 1) for game in range(4) for trial in range(4)]
        summary, _ = build_diagnostics(rows, bootstrap=25)
        target = summary["targets"]["action0"]
        self.assertIsNone(target["split_half"]["game"]["pearson"])
        self.assertEqual(target["split_half"]["game"]["correlation_status"], "constant_half")
        self.assertEqual(target["split_half"]["game"]["mae"], 0)
        self.assertEqual(target["variance"]["within_cell_trial_variance"], 0)

    def test_variance_and_game_weighted_agreement_have_known_values(self):
        rows = [record(f"g{g}", t, g, 2) for g in range(3) for t in range(4)]
        summary, derivation = build_diagnostics(rows, bootstrap=25)
        target = summary["targets"]["action0"]
        self.assertAlmostEqual(target["split_half"]["game"]["pearson"], 1)
        self.assertAlmostEqual(target["variance"]["between_game_variance"], 1/6)
        self.assertEqual(target["variance"]["within_cell_trial_variance"], 0)
        self.assertEqual(len(derivation["targets"]["action0"]["cells"]), 3)
        json.dumps(summary, allow_nan=False)
        json.dumps(derivation, allow_nan=False)

    def test_selfplay_keeps_episode_dependence_and_unique_trial_counts(self):
        rows = []
        for trial in range(4):
            first = record("g", trial, 1, 2, opponent="m0")
            second = copy.deepcopy(first)
            second["player_index"] = 1
            rows.extend((first, second))
        validate_records(rows)
        support = summarize_support(rows, "action0")
        self.assertEqual(support["eligible_trials"], 4)
        self.assertEqual(support["eligible_focal_rows"], 8)
        self.assertEqual(derive_target(rows, "action0")["cell_points"][0]["halves"][0]["label_counts"], {"False": 1, "True": 1})
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_records(rows + [rows[0]])

    def test_file_interface_and_empty_input(self):
        base = Path("/shared/allie/home/.codex/tmp")
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base, prefix="diagnostics-test-") as folder:
            root = Path(folder)
            source = root / "records.json"
            source.write_text("[]")
            result = run(source, root / "out", bootstrap=0, plots=False)
            self.assertEqual(result["records"], 0)
            self.assertEqual(result["figures"], [])
            self.assertTrue((root / "out" / "diagnostics.json").exists())
            self.assertTrue((root / "out" / "derivation.json").exists())


if __name__ == "__main__":
    unittest.main()
