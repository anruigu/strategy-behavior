"""Resolve a provider continuation at episode boundaries without rewriting traces."""
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def resolve(run):
    run = Path(run).resolve()
    base = read(run/"manifest.json")
    entries = {s["episode_id"]: dict(run=run, manifest=base, spec=s) for s in base["episodes"]}
    pointer_path = run/"provider-continuation.json"
    continuation = None
    if pointer_path.exists():
        pointer = read(pointer_path)
        if pointer["source_manifest_digest"] != digest(base):
            raise ValueError("Continuation pointer does not match source manifest")
        target = Path(pointer["run"]).resolve()
        if target.parent != run.parent or target == run:
            raise ValueError("Continuation must be a distinct sibling run")
        manifest_path = target/"manifest.json"
        if manifest_path.exists():
            next_manifest = read(manifest_path)
            origin = next_manifest["continuation"]
            if origin["source_manifest_digest"] != digest(base) or Path(origin["source_run"]).resolve() != run:
                raise ValueError("Continuation provenance mismatch")
            for spec in next_manifest["episodes"]:
                ident = spec["episode_id"]
                if ident not in entries or spec != entries[ident]["spec"]:
                    raise ValueError("Continuation changed game, model identity, seed, or condition")
                old_trace = run/"episodes"/ident/"trace.json"
                if old_trace.exists() and read(old_trace)["status"] == "complete":
                    raise ValueError("Continuation overwrites a completed original episode")
                entries[ident] = dict(run=target, manifest=next_manifest, spec=spec)
            continuation = dict(provider=pointer["provider"], run=str(target),
                                retained=pointer["retained"], restarted=pointer["restarted"])
    for ident, entry in entries.items():
        entry["path"] = entry["run"]/"episodes"/ident/"trace.json"
        entry["provider"] = entry["manifest"]["models"][entry["spec"]["player_id"]]["provider"]
    return base, entries, continuation
