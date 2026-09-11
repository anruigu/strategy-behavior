"""Export and audit a complete collection assembled from immutable provider runs."""
import argparse
from collections import Counter
from pathlib import Path

from prediction.io_utils import digest, read_json, write_json
from prediction.scaleup.export import export_run, write_jsonl
from .audit import audit
from .collection import resolve
from .server import jsonl, PACKAGE


def export_collection(run, out):
    run, out = Path(run).resolve(), Path(out).resolve()
    manifest, entries, continuation = resolve(run)
    sources = sorted({entry["run"] for entry in entries.values()})
    episode_rows, action_rows, source_audits = [], [], {}
    for source in sources:
        # Preserve an independently reproducible export for each immutable run.
        source_out = (run/"provider-exports"/source.name) if source == run else source/"export"
        export_run(source, source_out)
        source_audits[str(source)] = audit(source, source_out)
        source_manifest = read_json(source/"manifest.json")
        for filename, target in (("episodes.jsonl", episode_rows), ("actions.jsonl", action_rows)):
            for row in jsonl(source_out/filename):
                if entries[row["episode_id"]]["run"] != source:
                    continue
                row.update(source_run=str(source), source_manifest_sha256=digest(source_manifest))
                expected_player = source_manifest["players"][row["inputs"]["player"]["model_id"]]
                if row["inputs"]["player"] != expected_player:
                    raise ValueError("Wrong provider/player metadata in combined export")
                target.append(row)
    episode_keys = {r["episode_id"] for r in episode_rows}
    action_keys = {(r["episode_id"], r["turn"]) for r in action_rows}
    if len(episode_keys) != len(episode_rows) or len(action_keys) != len(action_rows):
        raise ValueError("Duplicate episode or action across providers")
    if not episode_keys <= set(entries):
        raise ValueError("Unplanned episode in combined collection")
    missing = []
    for ident, entry in entries.items():
        if ident in episode_keys:
            continue
        status = read_json(entry["path"])["status"] if entry["path"].exists() else "not_started"
        missing.append(dict(episode_id=ident, status=status, source_run=str(entry["run"]), provider=entry["provider"]))
    episode_rows.sort(key=lambda r: r["episode_id"])
    action_rows.sort(key=lambda r: (r["episode_id"], r["turn"]))
    write_jsonl(out/"episodes.jsonl", episode_rows)
    write_jsonl(out/"actions.jsonl", action_rows)
    write_jsonl(out/"missing.jsonl", missing)
    provider_counts = Counter(r["inputs"]["player"]["provider"] for r in episode_rows)
    model_counts = Counter(r["inputs"]["player"]["model_id"] for r in episode_rows)
    summary = dict(planned=len(manifest["episodes"]), complete=len(episode_rows), missing=len(missing), actions=len(action_rows),
                   providers=dict(provider_counts), models=dict(model_counts), continuation=continuation,
                   inference="Provider is recorded per episode; continuation membership is determined by prior completion and is not randomized")
    write_json(out/"summary.json", summary)
    write_json(out/"collection.json", dict(source_manifest_sha256=digest(manifest),
        source_runs={str(s): digest(read_json(s/"manifest.json")) for s in sources},
        episodes={ident: dict(source_run=str(entry["run"]), trace_path=str(entry["path"]), provider=entry["provider"]) for ident, entry in entries.items()},
        artifact_sha256={"episodes": digest(episode_rows), "actions": digest(action_rows), "missing": digest(missing)}))
    write_json(out/"audit.json", dict(status="passed", all_planned_complete=not missing,
        counts=dict(exported_episodes_verified=len(episode_rows), exported_actions_verified=len(action_rows),
                    invalid_actions=sum(not a["valid"] for a in action_rows)),
        source_audits=source_audits, provider_attribution_checked=True, duplicate_ids=False,
        protocol="Each source run independently replayed and raw-call audited; one selected provider source per episode; exact export joins"))
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", type=Path, default=PACKAGE/"runs/pilot-20260910")
    p.add_argument("--out", type=Path, default=PACKAGE/"runs/pilot-20260910/export")
    a = p.parse_args()
    print(export_collection(a.run, a.out))
