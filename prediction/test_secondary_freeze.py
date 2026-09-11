"""Offline orchestration tests: all subprocesses are synthetic file emitters."""
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

from prediction import secondary_freeze as secondary
from prediction.io_utils import read_json, write_json


class SecondaryFreezeTests(unittest.TestCase):
    def setUp(self):
        base = Path("/shared/allie/home/.codex/tmp")
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base, prefix="secondary-freeze-test-")
        self.root = Path(self.temp.name)
        self.code = self.root/"code"
        (self.code/"prediction").mkdir(parents=True)
        for name in ("secondary_freeze.py","secondary_baselines.py","after_matrix.py","pipeline.py",
                     "prospective.py","modeling.py","analysis.py"):
            (self.code/"prediction"/name).write_text("# synthetic immutable source\n")
        pairs = [("haiku","haiku"),("gpt-oss","kimi-k3"),("gpt-oss","haiku"),
                 ("kimi-k3","qwen"),("gpt-oss","gpt-oss")]
        self.rows = [{"episode_id":f"e{i}","player_index":player,
                      "model":pair[player],"opponent":pair[1-player]}
                     for i,pair in enumerate(pairs) for player in (0,1)]
        write_json(self.root/"training-records.json",self.rows)
        write_json(self.root/"primary-pilot-manifest.json",
                   {"models":{name:{} for name in ("haiku","gpt-oss","kimi-k3","qwen")}})
        for stage in ("prospective","controls"):
            write_json(self.root/stage/"metadata.json",[{"stage":stage,"feature":1}])
            write_json(self.root/stage/"manifest.json",{"stage":stage,"planned":1})
            write_json(self.root/stage/"metadata.manifest.json",{"metadata_fixture":stage})
        write_json(self.root/"pipeline-status.json",{"status":"running"})
        self.calls = []
        self.after_emit = None
        self.patchers = [
            patch.object(secondary.driver.pipeline,"ROOT",self.code),
            patch.object(secondary.driver,"validate_training",
                         side_effect=lambda root,primary:(read_json(root/"training-records.json"),"kimi-k3","gpt-oss")),
            patch.object(secondary.driver.subprocess,"run",side_effect=self.emit),
        ]
        self.mocks = [p.start() for p in self.patchers]

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temp.cleanup()

    def emit(self, command, **kwargs):
        self.calls.append(command)
        if "fit" in command:
            path = Path(command[command.index("--artifact")+1])
            write_json(path,{"synthetic_fit":True,"training":command[command.index("--training-records")+1]})
        else:
            path = Path(command[command.index("--output")+1])
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('{"prediction":0.5}\n')
            write_json(path.with_suffix(".manifest.json"),{"synthetic_forecast":True})
        if self.after_emit:
            self.after_emit(command)
        return SimpleNamespace(returncode=0)

    def test_each_rollout_marker_blocks_first_freeze_without_subprocess(self):
        for stage in ("prospective","controls"):
            for name in ("episodes","process.json","status.json"):
                with self.subTest(stage=stage,marker=name):
                    path = self.root/stage/name
                    path.mkdir() if name=="episodes" else write_json(path,{})
                    with self.assertRaisesRegex(RuntimeError,"precede every player rollout"):
                        secondary.freeze(self.root)
                    self.assertFalse(self.calls)
                    path.rmdir() if path.is_dir() else path.unlink()

    def test_filters_keep_both_focal_roles_and_forecast_exact_requested_stages(self):
        secondary.freeze(self.root)
        expected = {"full":{"e0","e1","e2","e3","e4"},
                    "excluded_pair":{"e0","e2","e3","e4"},
                    "excluded_model":{"e0","e3"}}
        for name,episodes in expected.items():
            rows = read_json(self.root/"secondary-baselines"/name/"training.json")
            self.assertEqual({r["episode_id"] for r in rows},episodes)
            self.assertEqual(set(Counter(r["episode_id"] for r in rows).values()),{2})
            self.assertEqual({r["player_index"] for r in rows},{0,1})
            audit = read_json(self.root/"secondary-baselines"/name/"training-audit.json")
            self.assertEqual(audit["rows"],2*len(episodes))
        self.assertEqual(sum("fit" in c for c in self.calls),3)
        forecasts = [Path(c[c.index("--output")+1]).relative_to(self.root/"secondary-baselines")
                     for c in self.calls if "forecast" in c]
        self.assertEqual({str(p) for p in forecasts},
                         {"full/prospective.jsonl","full/controls.jsonl",
                          "excluded_pair/prospective.jsonl","excluded_model/prospective.jsonl"})
        evidence = read_json(self.root/"secondary-baselines/forecast-freeze.json")
        self.assertEqual(evidence["status"],"forecasts_frozen_before_rollouts")
        self.assertFalse(evidence["api_calls"])
        required = {str(self.root/"secondary-baselines"/name/file)
                    for name in expected for file in ("training.json","training-audit.json","fit.json")}
        required.update(str(self.root/"secondary-baselines"/path) for path in forecasts)
        required.update(str((self.root/"secondary-baselines"/path).with_suffix(".manifest.json")) for path in forecasts)
        self.assertEqual(set(evidence["forecasts_sha256"]),required)
        self.assertTrue(all(secondary.driver.file_hash(path)==expected_hash
                            for path,expected_hash in evidence["forecasts_sha256"].items()))

    def test_completed_freeze_resumes_after_player_start_without_reexecution(self):
        secondary.freeze(self.root)
        evidence_path = self.root/"secondary-baselines/forecast-freeze.json"
        original = evidence_path.read_bytes()
        for stage in ("prospective","controls"):
            write_json(self.root/stage/"status.json",{"status":"running"})
        self.calls.clear()
        secondary.freeze(self.root)
        self.assertFalse(self.calls)
        self.assertEqual(evidence_path.read_bytes(),original)
        self.assertEqual(read_json(self.root/"secondary-baselines/status.json"),read_json(evidence_path))

    def test_upstream_stop_with_no_training_performs_no_work_or_api(self):
        (self.root/"training-records.json").unlink()
        for status in ("error","stopped_no_signal","informative_negative"):
            with self.subTest(status=status), patch.object(secondary.time,"sleep") as sleeping:
                write_json(self.root/"pipeline-status.json",{"status":status})
                secondary.freeze(self.root)
                record = read_json(self.root/"secondary-baselines/status.json")
                self.assertEqual(record["status"],"upstream_stopped")
                self.assertFalse(record["api_calls"])
                sleeping.assert_not_called()
                self.assertFalse(self.calls)

    def test_completed_forecast_training_metadata_and_source_mutations_rejected(self):
        secondary.freeze(self.root)
        paths = [
            self.root/"secondary-baselines/full/prospective.jsonl",
            self.root/"secondary-baselines/full/prospective.manifest.json",
            self.root/"secondary-baselines/full/fit.json",
            self.root/"training-records.json",
            self.root/"controls/metadata.json",
            self.code/"prediction/secondary_baselines.py",
        ]
        for path in paths:
            with self.subTest(path=path):
                original = path.read_bytes()
                path.write_bytes(original+b"\n")
                with self.assertRaises(ValueError):
                    secondary.freeze(self.root)
                path.write_bytes(original)

    def test_incomplete_freeze_does_not_resume_after_player_start(self):
        def begin_rollout(command):
            if "forecast" in command:
                write_json(self.root/"prospective/process.json",{"pid":123})
        self.after_emit = begin_rollout
        with self.assertRaisesRegex(RuntimeError,"precede every player rollout"):
            secondary.freeze(self.root)
        self.assertFalse((self.root/"secondary-baselines/forecast-freeze.json").exists())

    def test_partial_failed_step_is_not_silently_retried(self):
        self.mocks[2].side_effect = RuntimeError("synthetic subprocess failure")
        with self.assertRaisesRegex(RuntimeError,"synthetic subprocess"):
            secondary.freeze(self.root)
        self.mocks[2].side_effect = self.emit
        with self.assertRaisesRegex(RuntimeError,"requires explicit checkpoint audit"):
            secondary.freeze(self.root)
        self.assertFalse((self.root/"secondary-baselines/forecast-freeze.json").exists())

    def test_completed_resume_rejects_mutated_filtered_training_and_audit(self):
        secondary.freeze(self.root)
        for name in ("training.json","training-audit.json"):
            path = self.root/"secondary-baselines/excluded_model"/name
            original = path.read_bytes()
            path.write_bytes(original+b"\n")
            with self.subTest(name=name), self.assertRaises(ValueError):
                secondary.freeze(self.root)
            path.write_bytes(original)

    def test_completed_resume_rejects_changed_plan_and_stage_manifest(self):
        secondary.freeze(self.root)
        for path in (self.root/"secondary-baselines/plan.json",self.root/"prospective/manifest.json"):
            original = path.read_bytes()
            value = read_json(path)
            value["unexpected_mutation"] = True
            write_json(path,value)
            with self.subTest(path=path), self.assertRaises(ValueError):
                secondary.freeze(self.root)
            path.write_bytes(original)

    def test_mid_run_input_mutation_cannot_certify_final_freeze(self):
        def mutate_training(command):
            if len(self.calls)==1:
                write_json(self.root/"training-records.json",self.rows+[{"mutated":True}])
        self.after_emit = mutate_training
        with self.assertRaises(ValueError):
            secondary.freeze(self.root)
        self.assertFalse((self.root/"secondary-baselines/forecast-freeze.json").exists())


if __name__ == "__main__":
    unittest.main()
