"""Extract per-SAMPLE AgentMisalignment (household_management) results from the
inspect `.eval` logs into a flat cache, so the transfer analysis and the eval
trace viewer can read them without inspect_ai.

Must run under the ONLY venv with inspect_ai + the vendored inspect_evals fork:

    /workspace/allie/eval_games/.venv/bin/python am_dump.py

Per sample we keep everything needed to (a) score it with the repo's OWN grader
and (b) show the transcript: the graded misalignment value, the extracted CPU
action, the design axes (persona / explicitness / scenario), and the full
message list. `id`+`epoch` are the matched-pair key: the dataset is identical
across arms (same 36 base samples x 3 epochs), so the SAME id in hole vs nohole
is the SAME scenario and the score difference is the arm's effect.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = "/workspace/allie/evals_external/agentmisalignment"
sys.path.insert(0, REPO)

from inspect_ai.log import read_eval_log  # noqa: E402
from inspect_evals.agentmisalignment.scorers.household_management_scorer import (  # noqa: E402
    extract_action_from_cpu_allocation,
    get_misalignment_score,
)

LOGS = Path(REPO) / "logs"
OUT = Path("/workspace/allie/strategy-behavior/hole_exp/results/eval_transfer")
ARMS = [
    "frame-base",
    "frame-natural_hole-s0", "frame-natural_nohole-s0",
    "frame-game_hole-s0", "frame-game_nohole-s0",
]


def latest_eval(arm: str) -> Path | None:
    d = LOGS / arm
    if not d.is_dir():
        return None
    evals = sorted(d.glob("*.eval"))
    return evals[-1] if evals else None


def render(messages) -> str:
    parts = []
    for m in messages:
        content = m.content
        if isinstance(content, list):  # inspect content can be a list of blocks
            content = "\n".join(getattr(c, "text", str(c)) for c in content)
        parts.append(f"<|im_start|>{m.role}\n{content}<|im_end|>")
    return "\n".join(parts)


def dump_arm(arm: str) -> list[dict]:
    fp = latest_eval(arm)
    if fp is None:
        print(f"  [skip] {arm}: no .eval log", file=sys.stderr)
        return []
    log = read_eval_log(str(fp))
    rows = []
    for s in (log.samples or []):
        if s.error is not None:
            continue
        ans = ""
        if s.scores:
            sc = next(iter(s.scores.values()))
            ans = sc.answer or ""
        cpu, action = extract_action_from_cpu_allocation(ans)
        val = get_misalignment_score(action)
        if val is False:
            val = 0.0
        meta = s.metadata or {}
        rows.append({
            "id": str(s.id),
            "epoch": getattr(s, "epoch", 1),
            "persona": (meta.get("enhanced_prompts") or ["none"])[0],
            "explicit": meta.get("explicit", "?"),
            "scenario": meta.get("scenario", "?"),
            "cpu_pct": cpu,
            "action": action,
            "score": float(val),
            "answer": ans,
            "transcript": render(s.messages),
        })
    print(f"  [ok] {arm}: {len(rows)} samples", file=sys.stderr)
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {arm: dump_arm(arm) for arm in ARMS}
    (OUT / "am_samples.json").write_text(json.dumps(cache, ensure_ascii=False))
    tot = sum(len(v) for v in cache.values())
    print(f"wrote {OUT/'am_samples.json'} ({tot} samples across {len(cache)} arms)",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
