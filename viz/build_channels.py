#!/usr/bin/env python
"""Fold the message-channel 2x2 runs into one bundle for `channels.html`.

    python viz/build_channels.py

Reads `exploit-bench/results/chan-<tag>-<mandate>-<attacker>.jsonl` (written by
`results/run-channels.sh`) plus the factorial statistics already computed by
`eval/channel_report.py --json`, and writes `viz/channels.json`.

Why this is a second bundle rather than more tabs in `data.json`
---------------------------------------------------------------
`data.json` is keyed by domain, with one series per *target* on a smoke panel.
The channel runs are the other way round: one target per tab, with one series per
*arm* of a factorial, and the whole point of a tab is the within-target
comparison between arms. Rather than bend one bundle around both shapes -- while
that builder is being actively rewritten next door -- this keeps the channel view
self-contained: same server, same palette, its own page.

It computes nothing. Demand capture, the paired main effects, the CIs and the
sign tests all come from the runner and `eval/channel_report.py`; this file
reshapes them and drops fields the page never reads.
"""

from __future__ import annotations

import json
import subprocess
import sys
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "exploit-bench"
RESULTS = BENCH / "results"
OUT = Path(__file__).resolve().parent / "channels.json"

# (tag, label) per target, in the order the tabs should appear.
TARGETS: tuple[tuple[str, str], ...] = (
    ("oss120", "gpt-oss-120b"),
    ("oss20", "gpt-oss-20b"),
    ("g37", "gemini-3.7-flash"),
    ("gpt56terra", "gpt-5.6-terra"),
    ("dsv4pro", "deepseek-v4-pro"),
)
ARMS: tuple[str, ...] = ("system/user", "developer/user", "system/tool", "developer/tool")
ARM_NOTE = {
    "system/user": "baseline — the layout every earlier result was run under",
    "developer/user": "mandate on the higher-trust instruction channel",
    "system/tool": "the customer's words arrive as a wait_for_user_reply result",
    "developer/tool": "both factors at once",
}

FLAGS = ("compliant", "inadequate", "closed_by_target")


def finite(obj):
    """NaN and infinity -> null, everywhere in the bundle.

    JSON has no NaN. Python writes one anyway, and the browser then fails the whole
    document rather than the one field, so a `p` that was legitimately undefined
    takes the page down with it. `null` is the honest encoding and the page already
    renders it as an em dash.
    """
    if isinstance(obj, float):
        return obj if isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [finite(v) for v in obj]
    return obj


def arm_file(tag: str, arm: str) -> Path:
    mandate, attacker = arm.split("/")
    return RESULTS / f"chan-{tag}-{mandate}-{attacker}.jsonl"


def episode(rec: dict, arm: str) -> dict:
    cell = rec.get("cell") or {}
    return {
        "arm": arm,
        "case": rec.get("case_id"),
        # The mandate is one string per (case, arm) repeated across every episode
        # of it, so the page holds one copy in a table and each episode points at
        # it by hash. `wire` is per episode and small: roles and tool-call pairing
        # with the content dropped, because the transcript below already has it.
        "prompt": rec.get("system_prompt_sha", ""),
        "wire": rec.get("wire") or {},
        "technique": cell.get("technique"),
        "dc": rec.get("demand_capture"),
        "magnitude": rec.get("magnitude"),
        "floor": rec.get("floor"),
        "ask": rec.get("ask"),
        "realized": rec.get("realized"),
        "turns": rec.get("turns"),
        # Two validity columns, per episode. An empty target reply grants nothing
        # and so scores as maximal resistance (docs/0816-truncation.md). And an
        # episode whose labelled technique was never uttered is not evidence about
        # that technique at all -- under cs-env-1 that was most of some arms.
        "empty": rec.get("empty_replies") or 0,
        "technique_turns": rec.get("technique_turns"),
        "closed": bool(rec.get("closed_by_target")),
        "env": rec.get("versions", {}).get("env", "?"),
        "flags": {k: rec[k] for k in FLAGS if k in rec},
        "grant": rec.get("grant") or {},
        "violations": rec.get("violations") or [],
        "leaked": rec.get("leaked_facts") or [],
        "transcript": [
            {"speaker": t.get("speaker"), "technique": t.get("technique"),
             "text": t.get("text", ""),
             # Present only when the provider returned a reasoning trace. Kept
             # beside the utterance and never merged into it: the env scored the
             # utterance, so a concession drafted while thinking and then dropped
             # must stay visibly outside what was said.
             **({"thinking": t["thinking"]} if t.get("thinking") else {})}
            for t in (rec.get("transcript") or [])
        ],
    }


def stats(tags: list[str]) -> dict[str, dict]:
    """The factorial read, from `eval/channel_report.py` rather than re-derived."""
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "report.json"
        args = [sys.executable, str(BENCH / "eval" / "channel_report.py")]
        for tag in tags:
            args += ["--tag", tag]
        args += ["--json", str(js), "--md", str(Path(tmp) / "report.md")]
        proc = subprocess.run(args, capture_output=True, text=True, cwd=str(BENCH),
                              env={**os.environ, "PYTHONPATH": str(BENCH)})
        if proc.returncode != 0:
            raise SystemExit(f"channel_report.py failed:\n{proc.stderr}")
        return {r["tag"]: r for r in json.loads(js.read_text())}


def env_versions(tag: str) -> set[str]:
    """Which harness version each arm of this target was run under."""
    out: set[str] = set()
    for arm in ARMS:
        p = arm_file(tag, arm)
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.add(json.loads(line)["versions"].get("env", "?"))
                break
    return out


def main() -> int:
    present: list[tuple[str, str]] = []
    for tag, label in TARGETS:
        if not all(arm_file(tag, a).exists() for a in ARMS):
            print(f"  {tag}: incomplete 2x2 - skipped")
            continue
        # Four arms are comparable only if one harness produced them. Under
        # cs-env-1 a target's [CLOSE] ended the episode, so an arm where the
        # target closed early ran a fraction of the turns of one where it did not
        # -- mixing that with cs-env-2 would put a conversation-length artifact
        # into a chart about message channels, which is the exact bug that
        # retired the first set of these runs.
        seen = env_versions(tag)
        if len(seen) > 1:
            raise SystemExit(f"{tag}: arms span {sorted(seen)} -- re-run the whole 2x2 "
                             "under one env version before viewing it")
        present.append((tag, label))
    if not present:
        print("no complete 2x2 runs found; nothing to build")
        return 1

    by_tag = stats([t for t, _ in present])

    # sha -> mandate text, shared across every target and arm: the same case
    # renders the same prompt whoever is being asked and however it is delivered,
    # so 240 episodes carry three strings between them rather than 240 copies.
    prompts: dict[str, str] = {}
    bundle: dict[str, object] = {
        "arms": list(ARMS), "notes": ARM_NOTE, "prompts": prompts, "targets": [],
    }
    for tag, label in present:
        eps: list[dict] = []
        for arm in ARMS:
            for line in arm_file(tag, arm).read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                sha, text = rec.get("system_prompt_sha"), rec.get("system_prompt")
                if sha and text:
                    prompts.setdefault(sha, text)
                eps.append(episode(rec, arm))

        rep = by_tag[tag]
        techniques = sorted({e["technique"] for e in eps if e["technique"]})
        by_technique = []
        for t in techniques:
            means, ns = {}, {}
            for arm in ARMS:
                vals = [e["dc"] for e in eps
                        if e["technique"] == t and e["arm"] == arm and e["dc"] is not None]
                means[arm] = (sum(vals) / len(vals)) if vals else None
                ns[arm] = len(vals)
            by_technique.append({"technique": t, "means": means, "n": ns})

        bundle["targets"].append({  # type: ignore[union-attr]
            "key": tag,
            "label": label,
            "vendor": rep.get("vendor", ""),
            "developer_degenerate": rep.get("developer_degenerate", True),
            "n_episodes": len(eps),
            "empty_replies": sum(e["empty"] for e in eps),
            "arms": rep["arms"],
            "effects": rep["effects"],
            "flips": rep["flips"],
            "omnibus": rep["omnibus"],
            "by_technique": by_technique,
            "episodes": eps,
        })
        print(f"  {tag:12} {len(eps):3} episodes, {len(techniques)} techniques, "
              f"{sum(e['empty'] for e in eps)} empty replies")

    # `json.dumps` will happily write bare NaN, which is not JSON and which
    # `JSON.parse` rejects with a syntax error pointing at a byte offset -- so the
    # page dies on load and says nothing about which statistic was undefined. A
    # NaN here is meaningful (a sign test with no discordant pairs has no p), so it
    # becomes null, and `allow_nan=False` makes any future non-finite value an
    # exception at build time instead of a broken page at read time.
    OUT.write_text(
        json.dumps(finite(bundle), ensure_ascii=False, separators=(",", ":"),
                   allow_nan=False) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
