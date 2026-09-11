"""Create an auditable provider continuation without rewriting historical traces."""
import argparse
from copy import deepcopy
from pathlib import Path

from prediction.io_utils import digest, now, read_json, write_json
from .providers import configurations
from .runner import source_hashes


def prepare(source, manifest_path, out, budget_usd=50):
    source, manifest_path, out = Path(source).resolve(), Path(manifest_path).resolve(), Path(out).resolve()
    if manifest_path.exists() or out.exists():
        raise ValueError("Continuation destinations must be new")
    original = read_json(source/"manifest.json")
    remaining, retained = [], []
    for episode in original["episodes"]:
        path = source/"episodes"/episode["episode_id"]/"trace.json"
        if path.exists() and read_json(path)["status"] == "complete":
            retained.append(episode["episode_id"])
        else:
            remaining.append(episode)
    if not remaining:
        raise ValueError("No unfinished episodes")
    manifest = deepcopy(original)
    manifest.update(created=now(), sources=source_hashes(), episodes=remaining, budget_usd=budget_usd,
                    models=configurations(list(original["models"]), "openrouter"))
    for name, config in manifest["models"].items():
        manifest["players"][name].update(provider=config["provider"], provider_model=config["provider_model"])
    manifest["continuation"] = dict(source_run=str(source), source_manifest_digest=digest(original),
                                    retained_complete_episodes=retained, restart="fresh episode with original seed and seat assignment",
                                    reason="User requested OpenRouter after FLT HTTP 403 failures")
    write_json(manifest_path, manifest)
    # A separate pointer is consumed by the read-only viewer and combined export.
    # Original manifests, call logs, partial traces and completed labels stay intact.
    write_json(source/"provider-continuation.json", dict(created=now(), source_manifest_digest=digest(original),
        run=str(out), manifest=str(manifest_path), provider="openrouter", retained=len(retained), restarted=len(remaining)))
    return dict(retained=len(retained), restarted=len(remaining), manifest=str(manifest_path), run=str(out), budget_usd=budget_usd)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--budget-usd", type=float, default=50)
    a = p.parse_args()
    print(prepare(a.source, a.manifest, a.out, a.budget_usd))
