import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from prediction.io_utils import write_json
from prediction.watch import classify, inspect_process, inspect_stage, render_report, watch


class WatchTests(unittest.TestCase):
    def setUp(self):
        base = Path("/shared/allie/home/.codex/tmp")
        base.mkdir(parents=True, exist_ok=True)
        self.folder = tempfile.TemporaryDirectory(dir=base, prefix="watch-test-")
        self.root = Path(self.folder.name)
        for stage in ("pilot", "pilot-oss"):
            write_json(self.root/stage/"manifest.json", {})
        write_json(self.root/"primary-pilot-manifest.json", {})
        self.report = self.root/"REPORT.md"

    def tearDown(self):
        self.folder.cleanup()

    def marker(self, stage, status="running", completed=2, planned=3):
        write_json(self.root/stage/"process.json", {"pid": 100, "manifest": "/shared/allie/test/manifest.json",
            "started": "2026-09-10T00:00:00+00:00"})
        write_json(self.root/stage/"status.json", {"status": status, "completed": completed, "planned": planned,
            "started": "2026-09-10T00:00:01+00:00"})

    def test_zombie_is_dead_without_reading_empty_cmdline(self):
        stat = "100 (python (worker)) Z " + " ".join(["0"] * 19)
        with patch.object(Path, "read_text", return_value=stat), patch.object(Path, "read_bytes") as command:
            state = inspect_process({"pid": 100, "manifest": "manifest"})
        self.assertFalse(state["alive"])
        self.assertEqual(state["reason"], "zombie_or_dead")
        command.assert_not_called()

    def test_process_ownership_requires_runner_and_exact_manifest(self):
        stat = "100 (python) S " + " ".join(["0"] * 19)
        with patch.object(Path, "read_text", return_value=stat), patch.object(Path, "read_bytes", return_value=b"python\0runner.py\0--manifest\0/shared/allie/m.json\0"):
            self.assertTrue(inspect_process({"pid":100,"manifest":"/shared/allie/m.json"})["alive"])
            self.assertFalse(inspect_process({"pid":100,"manifest":"/shared/allie/other.json"})["alive"])

    def test_startup_grace_and_dead_incomplete_stage(self):
        self.assertEqual(inspect_stage(self.root, "pilot", 1, 300)["state"], "starting")
        self.assertEqual(inspect_stage(self.root, "pilot", 301, 300)["state"], "interrupted")
        self.marker("pilot")
        with patch("prediction.watch.inspect_process", return_value={"alive":False, "reason":"pid_not_found"}):
            self.assertEqual(inspect_stage(self.root, "pilot", 1, 300)["state"], "interrupted")
        self.marker("pilot", status="complete", completed=3)
        with patch("prediction.watch.inspect_process", return_value={"alive":False, "reason":"pid_not_found"}):
            self.assertEqual(inspect_stage(self.root, "pilot", 1, 300)["state"], "complete")

    def test_old_complete_marker_does_not_certify_new_dead_launch(self):
        self.marker("pilot", status="complete", completed=3)
        process = json.loads((self.root/"pilot/process.json").read_text())
        process["started"] = "2026-09-10T01:00:00+00:00"
        write_json(self.root/"pilot/process.json", process)
        with patch("prediction.watch.inspect_process", return_value={"alive":False, "reason":"pid_not_found"}):
            self.assertEqual(inspect_stage(self.root, "pilot", 1, 300)["state"], "interrupted")

    def test_finished_with_errors_is_normal_terminal_with_errors_retained(self):
        self.marker("pilot-oss", status="finished_with_errors", completed=383, planned=384)
        path = self.root/"pilot-oss/status.json"
        status = json.loads(path.read_text())
        status["errors"] = [{"episode":"failed-match", "error":"bounded retries exhausted"}]
        write_json(path, status)
        with patch("prediction.watch.inspect_process", return_value={"alive":False, "reason":"pid_not_found"}):
            stage = inspect_stage(self.root, "pilot-oss", 1, 300)
        self.assertEqual(stage["state"], "complete_with_errors")
        self.assertEqual(stage["completed"], 383)
        self.assertEqual(stage["runner_errors"], status["errors"])
        self.assertEqual(classify([{"state":"complete"},stage]), ("complete_with_errors",True))

    def test_one_interrupted_source_does_not_stop_live_source_watch(self):
        self.assertEqual(classify([{"state":"running"},{"state":"interrupted"}]), ("running",False))
        self.assertEqual(classify([{"state":"complete"},{"state":"interrupted"}]), ("interrupted",True))

    def fixture_watch(self, states, completed, refresh):
        stages = lambda root,name,*_: {"stage":name,"state":states[name],"completed":completed,
                                       "process":{"started":"launch"}}
        report = Mock()
        state = watch(self.root, report_path=self.report, once=True, stage_fn=stages,
                      refresh_fn=refresh, report_fn=report)
        return state, report

    def test_running_refresh_uses_100_and_does_not_write_foreign_statuses(self):
        gate = {"gate": "unchanged"}
        write_json(self.root/"gates.json", gate)
        write_json(self.root/"pipeline-status.json", {"status":"running"})
        refresh = Mock(return_value={"complete_episodes":35,"planned_episodes":60})
        state, report = self.fixture_watch({"pilot":"running","pilot-oss":"running"},20,refresh)
        refresh.assert_called_once_with(self.root,100)
        self.assertEqual(state["status"],"running")
        self.assertTrue(state["partial"])
        self.assertEqual(json.loads((self.root/"gates.json").read_text()),gate)
        self.assertEqual(json.loads((self.root/"pipeline-status.json").read_text()),{"status":"running"})
        report.assert_called_once()

    def test_below_increment_does_not_refresh(self):
        refresh = Mock()
        state, report = self.fixture_watch({"pilot":"running","pilot-oss":"running"},10,refresh)
        refresh.assert_not_called()
        self.assertEqual(state["refresh_count"],0)
        report.assert_called_once()

    def test_final_complete_requires_primary_audit_and_300_bootstrap(self):
        refresh = Mock(return_value={"complete_episodes":60,"planned_episodes":60})
        state, _ = self.fixture_watch({"pilot":"complete","pilot-oss":"complete"},30,refresh)
        refresh.assert_called_once_with(self.root,300)
        self.assertEqual(state["status"],"complete")
        self.assertFalse(state["partial"])
        incomplete = Mock(return_value={"complete_episodes":59,"planned_episodes":60})
        state, _ = self.fixture_watch({"pilot":"complete","pilot-oss":"complete"},30,incomplete)
        self.assertEqual(state["status"],"complete_with_errors")

    def test_normal_terminal_partial_collection_gets_final_diagnostics(self):
        refresh = Mock(return_value={"complete_episodes":959,"planned_episodes":960,
                                    "missing_episodes":["failed-match"], "integrity_errors":0})
        state, _ = self.fixture_watch({"pilot":"complete","pilot-oss":"complete_with_errors"},479,refresh)
        refresh.assert_called_once_with(self.root,300)
        self.assertEqual(state["status"],"complete_with_errors")
        self.assertTrue(state["partial"])
        self.assertEqual(state["coverage"]["fraction"],959/960)
        self.assertEqual(state["last_refresh"]["missing_episodes"],["failed-match"])
        render_report(self.root,self.report,state)
        self.assertIn("finished normally with failed or missing episodes",self.report.read_text())
        self.assertIn("959/960 episodes",self.report.read_text())

    def test_integrity_errors_do_not_become_normal_partial_completion(self):
        refresh = Mock(return_value={"complete_episodes":59,"planned_episodes":60,"integrity_errors":1})
        state, _ = self.fixture_watch({"pilot":"complete","pilot-oss":"complete_with_errors"},30,refresh)
        self.assertEqual(state["status"],"interrupted")
        self.assertEqual(state["reason"],"final_collection_integrity_errors")
        self.assertEqual(state["coverage"]["integrity_errors"],1)

    def test_refresh_failure_never_claims_complete(self):
        refresh = Mock(side_effect=RuntimeError("audit failed"))
        state, _ = self.fixture_watch({"pilot":"complete","pilot-oss":"complete"},30,refresh)
        self.assertEqual(state["status"],"interrupted")
        self.assertEqual(state["reason"],"final_refresh_failed")

    def test_report_notice_exposes_interruption_without_pipeline_edits(self):
        render_report(self.root,self.report,{"status":"interrupted","stages":[]})
        text = self.report.read_text()
        self.assertIn("Live watcher: **interrupted**",text)
        self.assertIn("Displayed diagnostics are partial",text)
        self.assertFalse((self.root/"pipeline-status.json").exists())


if __name__ == "__main__":
    unittest.main()
