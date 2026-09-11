"""Refresh the combined primary pilot while its two owned source jobs run.

No model calls, gate decisions, runner-status edits or pipeline-status writes.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import signal
import sys
import threading
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import now, read_json, write_json

STAGES = ("pilot", "pilot-oss")


def safe_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to(Path("/shared/allie")):
        raise ValueError("Watcher artifacts must remain under /shared/allie")
    return path


def optional_json(path):
    try:
        return read_json(path)
    except FileNotFoundError:
        return None


def _timestamp(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except (AttributeError, TypeError, ValueError):
        return None


def inspect_process(process):
    """Check Linux PID liveness and exact manifest ownership without signaling it."""
    pid = process.get("pid")
    if type(pid) is not int or pid <= 0:
        return {"alive": False, "owned": False, "reason": "invalid_pid", "pid": pid}
    try:
        # comm can contain spaces/parentheses. Fields after its final ')' start
        # with state (field 3); starttime is field 22, hence index 19.
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        state, start_ticks = fields[0], fields[19]
        if state in ("Z", "X", "x"):
            return {"alive": False, "owned": False, "reason": "zombie_or_dead", "pid": pid,
                    "process_state": state, "start_ticks": start_ticks}
        command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        command = [part.decode(errors="replace") for part in command if part]
        manifest = process.get("manifest")
        owned = bool(manifest and str(manifest) in command
                     and any(Path(arg).name == "runner.py" for arg in command))
        return {"alive": owned, "owned": owned, "reason": "owned_runner" if owned else "pid_not_owned_runner",
                "pid": pid, "process_state": state, "start_ticks": start_ticks}
    except FileNotFoundError:
        return {"alive": False, "owned": False, "reason": "pid_not_found", "pid": pid}
    except (PermissionError, OSError, IndexError) as exc:
        return {"alive": None, "owned": None, "reason": "process_inspection_unavailable",
                "pid": pid, "error": type(exc).__name__ + ": " + str(exc)}


def inspect_stage(run_root, stage, startup_elapsed, startup_grace):
    folder = run_root / stage
    try:
        process, status = optional_json(folder / "process.json"), optional_json(folder / "status.json")
    except (json.JSONDecodeError, OSError) as exc:
        return {"stage": stage, "state": "unknown", "completed": 0,
                "reason": "unreadable_source_marker", "error": str(exc)}
    status = status or {}
    result = {"stage": stage, "runner_status": status.get("status"),
              "completed": status.get("completed", 0), "planned": status.get("planned"),
              "runner_errors": status.get("errors", []),
              "runner_updated": status.get("updated", status.get("finished")), "process": process}
    if process is None:
        result.update(state="starting" if startup_elapsed < startup_grace else "interrupted",
                      reason="awaiting_process_marker" if startup_elapsed < startup_grace else "process_marker_missing_after_grace")
        return result
    probe = inspect_process(process)
    result["process_probe"] = probe
    started, status_started = _timestamp(process.get("started")), _timestamp(status.get("started"))
    current_status = started is None or status_started is None or status_started >= started - 10
    result["status_matches_current_launch"] = current_status
    if probe["alive"]:
        result.update(state="running", reason="owned_runner_alive")
    elif probe["alive"] is None:
        result.update(state="unknown", reason=probe["reason"])
    elif (current_status and status.get("status") in ("complete", "finished_with_errors")
          and type(status.get("planned")) is int and type(status.get("completed")) is int
          and 0 <= status["completed"] <= status["planned"]):
        full = (status["status"] == "complete" and status["completed"] == status["planned"]
                and not status.get("errors"))
        result.update(state="complete" if full else "complete_with_errors",
                      reason="runner_complete_and_process_exited" if full else "runner_finished_with_partial_data_or_episode_errors")
    else:
        result.update(state="interrupted", reason="runner_not_complete_and_process_not_alive")
    return result


def classify(stages):
    states = [stage["state"] for stage in stages]
    if any(state == "running" for state in states):
        return "running", False
    if any(state in ("starting", "unknown") for state in states):
        return "starting", False
    if all(state in ("complete", "complete_with_errors") for state in states):
        return ("complete" if all(state == "complete" for state in states) else "complete_with_errors"), True
    return "interrupted", True


def refresh_outputs(run_root, bootstrap):
    """Use frozen collector and exact primary-roster merge, then diagnostics."""
    from prediction.combine_pilot import combine
    from prediction.diagnostics import run as diagnose
    combined = combine(run_root)
    result = diagnose(run_root / "primary-pilot/records.json", run_root / "pilot/diagnostics", bootstrap=bootstrap)
    return {"updated": now(), "bootstrap": bootstrap,
            "complete_episodes": combined["complete_episodes"], "planned_episodes": combined["planned_episodes"],
            "missing_episodes": combined["missing_episodes"], "integrity_errors": combined["integrity_errors"],
            "records": result["records"], "games": result["games"], "record_digest": result["record_digest"]}


def render_report(run_root, target, watcher):
    """Render root's report and add an explicit collection notice, without gates."""
    from prediction.report import render
    render(run_root, target)
    status = watcher["status"]
    if status == "complete":
        notice = "Primary pilot collection is complete; this is not a declaration that later study gates are complete."
    elif status == "complete_with_errors":
        notice = ("Source runners finished normally with failed or missing episodes. Final diagnostics use the available validated records and remain partial. "
                  "The pipeline evaluates its coverage gate separately.")
    elif status == "interrupted":
        notice = "Source collection or the watcher was interrupted. Displayed diagnostics are partial; inspect watcher-status.json."
    else:
        notice = "Primary pilot collection is running or starting. All displayed pilot diagnostics are partial."
    interrupted = [s["stage"] for s in watcher.get("stages", []) if s["state"] == "interrupted"]
    if interrupted and status != "interrupted":
        notice += " Interrupted source: " + ", ".join(interrupted) + "."
    partial_sources = [s["stage"] for s in watcher.get("stages", []) if s["state"] == "complete_with_errors"]
    if partial_sources:
        notice += " Sources finished with partial data or episode errors: " + ", ".join(partial_sources) + "."
    coverage = watcher.get("coverage")
    if coverage:
        notice += f" Validated coverage: {coverage['complete_episodes']}/{coverage['planned_episodes']} episodes."
    relative = os.path.relpath(run_root / "watcher-status.json", target.parent)
    lines = target.read_text().splitlines()
    lines[2:2] = [f"> Live watcher: **{status}**. {notice} [Watcher status]({relative})", ""]
    temporary = target.with_name(target.name + ".watcher-" + uuid4().hex + ".tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, target)


def watch(run_root, interval=120, minimum_new=30, startup_grace=300, max_hours=24,
          report_path=None, once=False, stop_event=None, refresh_fn=None, stage_fn=None, report_fn=None):
    """Watch pilot/pilot-oss; callbacks are injectable for tests, never APIs."""
    run_root = safe_path(run_root)
    report_path = safe_path(report_path or ROOT / "prediction/REPORT.md")
    if interval <= 0 or minimum_new <= 0 or startup_grace < 0 or max_hours <= 0:
        raise ValueError("Interval, increment and max-hours must be positive; startup grace nonnegative")
    run_root.mkdir(parents=True, exist_ok=True)
    refresh_fn = refresh_fn or refresh_outputs
    stage_fn = stage_fn or inspect_stage
    report_fn = report_fn or render_report
    stop_event = stop_event or threading.Event()
    status_path = run_root / "watcher-status.json"
    started = time.monotonic()
    state = {"status": "starting", "started": now(), "pid": os.getpid(), "interval_seconds": interval,
             "minimum_new_episodes": minimum_new, "startup_grace_seconds": startup_grace,
             "max_hours": max_hours, "monitored_stages": list(STAGES), "partial": True,
             "last_refresh": None, "refresh_errors": [], "refresh_count": 0}
    last_completed, last_launches, last_report_signature = 0, None, None
    with (run_root / "watcher.lock").open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another watcher owns this run root") from exc
        while True:
            elapsed = time.monotonic() - started
            stages = [stage_fn(run_root, name, elapsed, startup_grace) for name in STAGES]
            status, terminal = classify(stages)
            report_signature = tuple((s["stage"], s["state"]) for s in stages)
            total = sum(s.get("completed", 0) for s in stages)
            launches = [(s.get("process") or {}).get("started") for s in stages]
            state.update(status=status, stages=stages, completed_in_source_statuses=total,
                         updated=now(), partial=status != "complete")
            if stop_event.is_set() or elapsed >= max_hours * 3600:
                state.update(status="interrupted", partial=True, finished=now(),
                             reason="watcher_stop_requested" if stop_event.is_set() else "watcher_time_limit")
                write_json(status_path, state)
                report_fn(run_root, report_path, state)
                return state
            ready = all((run_root / name / "manifest.json").exists() for name in STAGES) and (run_root / "primary-pilot-manifest.json").exists()
            changed_launch = last_launches is not None and launches != last_launches
            refresh = ready and (terminal or total - last_completed >= minimum_new or changed_launch)
            # Completion requires successful final collection and diagnostics.
            if terminal and status in ("complete", "complete_with_errors"):
                state.update(status="running", partial=True, reason="final_collection_audit_pending")
            write_json(status_path, state)
            if refresh:
                try:
                    result = refresh_fn(run_root, 300 if terminal else 100)
                    state.update(last_refresh=result, refresh_count=state["refresh_count"] + 1)
                    state["coverage"] = {"complete_episodes": result["complete_episodes"],
                                         "planned_episodes": result["planned_episodes"],
                                         "fraction": result["complete_episodes"] / result["planned_episodes"] if result["planned_episodes"] else None,
                                         "integrity_errors": result.get("integrity_errors", 0)}
                    last_completed, last_launches = total, launches
                    if terminal:
                        full = status == "complete" and result["complete_episodes"] == result["planned_episodes"]
                        if result.get("integrity_errors"):
                            final_status, reason = "interrupted", "final_collection_integrity_errors"
                        elif status == "interrupted":
                            final_status, reason = "interrupted", "source_process_interrupted"
                        elif full:
                            final_status, reason = "complete", "source_stages_and_primary_audit_complete"
                        else:
                            final_status, reason = "complete_with_errors", "terminal_sources_with_partial_primary_data_or_episode_errors"
                        state.update(status=final_status, partial=final_status != "complete", finished=now(), reason=reason)
                    else:
                        state.update(status=status, partial=True)
                except Exception as exc:
                    state["refresh_errors"] = (state["refresh_errors"] + [{"at": now(), "error": type(exc).__name__ + ": " + str(exc)}])[-20:]
                    if terminal:
                        state.update(status="interrupted", partial=True, finished=now(), reason="final_refresh_failed")
                state["updated"] = now()
                write_json(status_path, state)
                try:
                    report_fn(run_root, report_path, state)
                    state.pop("report_error", None)
                    state["last_report_updated"] = now()
                    last_report_signature = report_signature
                    write_json(status_path, state)
                except Exception as exc:
                    state["report_error"] = {"at": now(), "error": type(exc).__name__ + ": " + str(exc)}
                    if terminal:
                        state.update(status="interrupted", partial=True, reason="final_report_failed")
                    write_json(status_path, state)
            elif terminal:
                state.update(status="interrupted", partial=True, finished=now(), reason="required_collection_manifests_missing")
                write_json(status_path, state)
                report_fn(run_root, report_path, state)
            elif report_signature != last_report_signature:
                try:
                    report_fn(run_root, report_path, state)
                    state.pop("report_error", None)
                    state["last_report_updated"] = now()
                    last_report_signature = report_signature
                except Exception as exc:
                    state["report_error"] = {"at": now(), "error": type(exc).__name__ + ": " + str(exc)}
                write_json(status_path, state)
            if terminal or once:
                return state
            deadline = time.monotonic() + interval
            while not stop_event.is_set() and time.monotonic() < deadline:
                stop_event.wait(min(30, max(0, deadline - time.monotonic())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--interval", type=float, default=120)
    parser.add_argument("--minimum-new", type=int, default=30)
    parser.add_argument("--startup-grace", type=float, default=300)
    parser.add_argument("--max-hours", type=float, default=24)
    parser.add_argument("--report", type=Path, default=ROOT / "prediction/REPORT.md")
    parser.add_argument("--once", action="store_true", help="One observation/eligible refresh; primarily for testing")
    args = parser.parse_args()
    stopping = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stopping.set())
    signal.signal(signal.SIGINT, lambda *_: stopping.set())
    state = watch(args.run_root, args.interval, args.minimum_new, args.startup_grace,
                  args.max_hours, args.report, args.once, stopping)
    print(json.dumps({key: state.get(key) for key in ("status", "reason", "refresh_count", "last_refresh")}))
    return 1 if state["status"] == "interrupted" else 0


if __name__ == "__main__":
    raise SystemExit(main())
