import copy
import json
from pathlib import Path
import tempfile
import unittest

from prediction.controls_analysis import build_analysis, run, validate_whole_episodes
from prediction.games import make_game, payoff
from prediction.measurements import measure_episode


def episode(game, trial, actions, models=("m0","m1"), representation="matrix"):
    trace = {"id":f"{game['id']}:{models[0]}:{models[1]}:{trial}", "game":game,
             "models":list(models), "trial_id":trial, "representation":representation,
             "swap":bool(trial%2), "status":"complete",
             "rounds":[{"round":i+1,"actions":list(pair),"payoffs":list(payoff(game,*pair))}
                       for i,pair in enumerate(actions)]}
    return measure_episode(trace)


def pilot_rows(game, label_sensitive=False, models=("m0","m1")):
    return [row for trial in range(4)
            for row in episode(game,trial,[(1,1) if label_sensitive and trial%2 else (0,0)]*4,models)]


def control_game(source, variant):
    values = [source["payoffs"][k] for k in ("R","S","T","P")]
    transformed = [3*v if variant=="scale3" else v+10 if variant=="offset10" else v for v in values]
    return make_game(f"control-{variant}-{source['id']}",*transformed,control_variant=variant,
                     source_game_id=source["id"],source_group_id=source["group_id"])


class ControlsAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.g1 = make_game("g1",3,0,5,1)
        self.g2 = make_game("g2",4,0,5,1)

    def metric(self, summary, target="action0", comparison="action_labels"):
        return summary["comparisons"][comparison]["targets"][target]["aggregate"]

    def test_fixed_canonical_actions_are_invariant_under_display_swap(self):
        summary,_ = build_analysis(pilot_rows(self.g1),bootstrap=0)
        self.assertEqual(self.metric(summary)["mean_change"],0)
        self.assertEqual(self.metric(summary)["left_equal_game_rate"],1)
        self.assertEqual(self.metric(summary)["paired_left"]["eligible_episodes"],2)
        self.assertEqual(self.metric(summary)["paired_left"]["eligible_focal_rows"],4)

    def test_label_sensitivity_sign_and_cluster_interval_are_exact(self):
        rows = pilot_rows(self.g1,True) + pilot_rows(self.g2,True)
        summary,_ = build_analysis(rows,bootstrap=25)
        metric = self.metric(summary)
        self.assertEqual(metric["mean_change"],-1)
        self.assertEqual(metric["mean_absolute_game_change"],1)
        self.assertEqual(metric["eligible_groups"],2)
        self.assertEqual(metric["intervals"]["mean_change"]["lower"],-1)
        self.assertEqual(metric["intervals"]["mean_change"]["upper"],-1)
        self.assertEqual(self.metric(summary,"cooperation")["mean_change"],-1)

    def test_conditional_counts_pool_within_game_before_equal_game_average(self):
        rows = pilot_rows(self.g1) + pilot_rows(self.g2)
        for row in rows:
            trial = row["trial_id"]
            s,n = ((0,1) if trial==0 else (9,9) if trial==2 else (1,1)) if row["game_id"]=="g1" else (0,100)
            row["targets"]["retaliation"] = {"successes":s,"opportunities":n,"value":s/n,"applicable":True}
        summary,_ = build_analysis(rows,bootstrap=0)
        metric = self.metric(summary,"retaliation")
        self.assertAlmostEqual(metric["left_equal_game_rate"],.45)
        self.assertAlmostEqual(metric["right_equal_game_rate"],.5)
        self.assertAlmostEqual(metric["mean_change"],.05)
        self.assertEqual(metric["paired_left"]["opportunities"],420)
        self.assertEqual(metric["paired_right"]["opportunities"],404)
        self.assertEqual(metric["paired_left"]["eligible_episodes"],4)

    def test_unsupported_and_zero_opportunity_targets_stay_null(self):
        rows = pilot_rows(self.g1)
        summary,derivation = build_analysis(rows,bootstrap=0)
        metric = self.metric(summary,"coordination")
        self.assertIsNone(metric["mean_change"])
        self.assertEqual(metric["candidate_left"]["unsupported_focal_rows"],4)
        self.assertEqual(metric["paired_left"]["opportunities"],0)
        self.assertEqual(metric["excluded_cells"],{"unsupported_target":2})
        self.assertEqual(self.metric(summary,"forgiveness")["excluded_cells"],{"no_opportunities_in_condition":2})
        self.assertIsNone(derivation["comparisons"]["action_labels"]["forgiveness"]["cells"][0]["delta"])
        json.dumps(summary,allow_nan=False)

    def test_missing_whole_trial_excluded_but_missing_focal_record_rejected(self):
        rows = pilot_rows(self.g1)
        summary,_ = build_analysis(rows[:-2],bootstrap=0)
        self.assertEqual(self.metric(summary)["paired_cells"],0)
        self.assertEqual(self.metric(summary)["excluded_cells"],{"missing_or_extra_design_trials":2})
        with self.assertRaisesRegex(ValueError,"both focal"):
            validate_whole_episodes(rows[:-1])
        corrupt = copy.deepcopy(rows)
        corrupt[0]["opponent"] = "wrong-role"
        with self.assertRaisesRegex(ValueError,"roles disagree"):
            validate_whole_episodes(corrupt)

    def test_wrong_label_schedule_is_not_silently_classified_by_trial(self):
        rows = pilot_rows(self.g1)
        rows[2]["swap"] = rows[3]["swap"] = False
        summary,_ = build_analysis(rows,bootstrap=0)
        self.assertEqual(self.metric(summary)["excluded_cells"],{"unexpected_or_unknown_label_schedule":2})

    def test_control_comparison_preserves_two_vs_four_trial_counts(self):
        pilot, controls, games = [],[],[]
        for game in (self.g1,self.g2):
            pilot.extend(pilot_rows(game))
            transformed = control_game(game,"scale3")
            games.append(transformed)
            for trial in (0,1):
                controls.extend(episode(transformed,trial,[(1,1)]*4))
        summary,derivation = build_analysis(pilot,controls,{"games":games},bootstrap=25)
        metric = self.metric(summary,comparison="scale3")
        self.assertEqual(metric["mean_change"],-1)
        self.assertEqual(metric["paired_left"]["eligible_episodes"],8)
        self.assertEqual(metric["paired_right"]["eligible_episodes"],4)
        self.assertEqual(metric["paired_left"]["opportunities"],64)
        self.assertEqual(metric["paired_right"]["opportunities"],32)
        self.assertEqual(metric["eligible_games"],2)
        self.assertEqual(derivation["control_mapping"][games[0]["id"]]["source_game_id"],"g1")
        self.assertEqual(metric["intervals"]["mean_change"]["lower"],-1)

    def test_affine_transform_and_representation_mapping_are_validated(self):
        pilot = pilot_rows(self.g1)
        game = control_game(self.g1,"offset10")
        rows = episode(game,0,[(0,0)]*4) + episode(game,1,[(0,0)]*4)
        bad = copy.deepcopy(game)
        bad["payoffs"]["R"] += .1
        with self.assertRaisesRegex(ValueError,"declared source transformation"):
            build_analysis(pilot,rows,{"games":[bad]},bootstrap=0)
        missing = copy.deepcopy(game)
        del missing["source_game_id"]
        with self.assertRaisesRegex(ValueError,"source_game_id"):
            build_analysis(pilot,rows,{"games":[missing]},bootstrap=0)
        text = control_game(self.g1,"abstract_text")
        wrong = episode(text,0,[(0,0)]*4) + episode(text,1,[(0,0)]*4)
        with self.assertRaisesRegex(ValueError,"representation"):
            build_analysis(pilot,wrong,{"games":[text]},bootstrap=0)
        right = episode(text,0,[(0,0)]*4,representation="text") + episode(text,1,[(0,0)]*4,representation="text")
        summary,_ = build_analysis(pilot,right,{"games":[text]},bootstrap=0)
        self.assertEqual(self.metric(summary,comparison="abstract_text")["mean_change"],0)

    def test_selfplay_is_one_episode_per_trial_and_one_cluster_has_no_ci(self):
        rows = [row for trial in range(4)
                for row in episode(self.g1,trial,[(0,1)]*4,models=("m0","m0"))]
        summary,_ = build_analysis(rows,bootstrap=25)
        metric = self.metric(summary)
        self.assertEqual(metric["paired_cells"],1)
        self.assertEqual(metric["left_equal_game_rate"],.5)
        self.assertEqual(metric["paired_left"]["episodes"],2)
        self.assertEqual(metric["paired_left"]["focal_rows"],4)
        self.assertIsNone(metric["intervals"]["mean_change"]["lower"])

    def test_file_interface_empty_input_and_partial_controls(self):
        base = Path("/shared/allie/home/.codex/tmp")
        base.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base,prefix="controls-test-") as folder:
            root = Path(folder)
            source = root/"records.json"
            source.write_text("[]")
            summary = run(source,root/"out",bootstrap=0,plots=False)
            self.assertEqual(summary["controls_status"],"not_supplied")
            self.assertTrue((root/"out/controls-analysis.json").exists())
            self.assertTrue((root/"out/derivation.json").exists())
        game = control_game(self.g1,"scale3")
        summary,_ = build_analysis(pilot_rows(self.g1),episode(game,0,[(0,0)]*4),{"games":[game]},bootstrap=0)
        self.assertIsNone(self.metric(summary,comparison="scale3")["mean_change"])
        self.assertEqual(self.metric(summary,comparison="scale3")["excluded_cells"],
                         {"control_missing_or_extra_design_trials":2})


if __name__ == "__main__":
    unittest.main()
