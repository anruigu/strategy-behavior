#!/usr/bin/env python
"""Fold the counterparty-identity runs into one bundle for `consistency.html`.

    python viz/build_consistency.py

Reads `exploit-bench/results/prof-<tag>-<cell>.jsonl` (written by
`results/run-profile.sh`) plus the invariance statistics already computed by
`eval/consistency.py --json`, and writes `viz/consistency.json`.

Why a third bundle rather than more tabs in `channels.json`
----------------------------------------------------------
Both pages are one-target-per-tab with one series per arm, so they are closer in
shape than either is to `data.json`. What differs is the *statistic*, and it
differs enough that sharing a page would mean two renderers behind one tab strip.
The channel factor is a 2x2, so its read is a factorial: two main effects and an
interaction, with hue carrying one factor and a hatch the other. The identity
factor is six arms on one axis where four are levels of a flat thing and two are
signed contrasts that are *supposed* to move -- so its read is a spread against a
permutation null plus a contrast plot, and a hatch has nothing to carry.

Same server, same palette, its own page, and `channels.html` links to it.

It computes nothing that `eval/consistency.py` computes. The spread, the null, the
CIs and the paired contrasts all come from there; this file reshapes them, interns
the repeated text, and drops fields the page never reads.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "exploit-bench"
RESULTS = BENCH / "results"
OUT = Path(__file__).resolve().parent / "consistency.json"

if str(BENCH) not in sys.path:
    sys.path.insert(0, str(BENCH))

from core.profile import CELLS, INVARIANT_CELLS  # noqa: E402

# (tag, label) per target, in the order the tabs should appear: frontier first,
# then open weights, each in descending order of what they cost to run. The split
# is the point of running both -- if identity deference is a pretraining artifact
# it should not care which lab did the training.
TARGETS: tuple[tuple[str, str], ...] = (
    ("opus5", "opus-5"),
    ("sonnet5", "sonnet-5"),
    ("gpt56sol", "gpt-5.6-sol"),
    ("gemini31pro", "gemini-3.1-pro"),
    ("oss120", "gpt-oss-120b"),
    ("oss20", "gpt-oss-20b"),
    # No qwen on the 2026-08-17 set, and the absence is a routing fact rather
    # than a result. Both 27b slugs answered an 8s single-turn probe and then
    # crawled on the panel -- qwen3.8-27b produced zero episodes in ninety
    # minutes, qwen3.6-27b ten in three hours -- which is the OpenRouter
    # provider-spread problem `eval/models.json` already documents for that
    # family. Left out rather than waited out: a target whose arms finish hours
    # apart is a target whose arms are not paired in the only way that matters,
    # and a half-finished one is worse than an absent one. Re-add the line when
    # a route is healthy; nothing else has to change.
)

CELL_ORDER: tuple[str, ...] = (
    "baseline", "notable", "famous", "famous_stated", "impostor", "repeat",
)

CELL_NOTE: dict[str, str] = {
    "baseline": "reference — a record exists and says nothing remarkable",
    "notable": "identifiable but not household: a retail CEO, a city mayor",
    "famous": "dense in any pretraining corpus",
    "famous_stated": "the same claim, with no lookup tool at all",
    "impostor": "the claim, contradicted by the account record",
    "repeat": "flagged for nine claims in twelve months — should concede LESS",
}

FLAGS = ("compliant", "inadequate", "closed_by_target")


def finite(obj):
    """NaN and infinity -> null, everywhere in the bundle.

    JSON has no NaN. Python writes one anyway and the browser then fails the whole
    document rather than the one field, so a `p` that was legitimately undefined
    takes the page down with it. `null` is the honest encoding and the page renders
    it as an em dash.
    """
    if isinstance(obj, float):
        return obj if isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [finite(v) for v in obj]
    return obj


def arm_file(tag: str, cell: str) -> Path:
    return RESULTS / f"prof-{tag}-{cell}.jsonl"


def episode(rec: dict, cell: str) -> dict:
    c = rec.get("cell") or {}
    return {
        "cell": cell,
        "case": rec.get("case_id"),
        # Two interned pointers rather than two copies. The mandate is ~1.9 KB and
        # identical across a case's episodes; the account record is identical
        # across a (case, cell) pair. 96 episodes carry a handful of strings.
        "prompt": rec.get("system_prompt_sha", ""),
        "record": rec.get("profile_record_sha", ""),
        "wire": rec.get("wire") or {},
        "technique": c.get("technique"),
        "dc": rec.get("demand_capture"),
        "magnitude": rec.get("magnitude"),
        "floor": rec.get("floor"),
        "ask": rec.get("ask"),
        "realized": rec.get("realized"),
        "turns": rec.get("turns"),
        # Validity columns, per episode. An empty target reply grants nothing and
        # so scores as maximal resistance (docs/0816-truncation.md); an episode
        # whose labelled technique was never uttered is not evidence about it.
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
             # stays visibly outside what was said.
             **({"thinking": t["thinking"]} if t.get("thinking") else {})}
            for t in (rec.get("transcript") or [])
        ],
    }


def stats(tags: list[str]) -> dict[str, dict]:
    """The invariance read, from `eval/consistency.py` rather than re-derived."""
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "report.json"
        args = [sys.executable, str(BENCH / "eval" / "consistency.py")]
        for tag in tags:
            args += ["--tag", tag]
        args += ["--json", str(js)]
        proc = subprocess.run(args, capture_output=True, text=True, cwd=str(BENCH),
                              env={**os.environ, "PYTHONPATH": str(BENCH)})
        if proc.returncode != 0:
            raise SystemExit(f"consistency.py failed:\n{proc.stderr}")
        return {r["tag"]: r for r in json.loads(js.read_text())}


def main() -> int:
    present: list[tuple[str, str]] = []
    for tag, label in TARGETS:
        have = [c for c in CELLS if arm_file(tag, c).exists()]
        if len(have) < len(CELLS):
            missing = sorted(set(CELLS) - set(have))
            print(f"  {tag}: incomplete — missing {', '.join(missing)}; skipped")
            continue
        present.append((tag, label))
    if not present:
        print("no complete profile runs found; nothing to build")
        return 1

    by_tag = stats([t for t, _ in present])

    prompts: dict[str, str] = {}
    records: dict[str, str] = {}
    bundle: dict[str, object] = {
        "cells": list(CELL_ORDER),
        "notes": CELL_NOTE,
        "invariantCells": list(INVARIANT_CELLS),
        "profiles": {k: CELLS[k].label() for k in CELL_ORDER},
        "prompts": prompts,
        "records": records,
        "targets": [],
    }

    for tag, label in present:
        eps: list[dict] = []
        env_versions: set[str] = set()
        for cell in CELL_ORDER:
            for line in arm_file(tag, cell).read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                env_versions.add(rec.get("versions", {}).get("env", "?"))
                sha, text = rec.get("system_prompt_sha"), rec.get("system_prompt")
                if sha and text:
                    prompts.setdefault(sha, text)
                rsha, rtext = rec.get("profile_record_sha"), rec.get("profile_record")
                if rsha and rtext:
                    records.setdefault(rsha, rtext)
                eps.append(episode(rec, cell))

        # Six arms are comparable only if one harness produced them, for the same
        # reason the channel 2x2 refuses a mixed set: under cs-env-1 a target's
        # [CLOSE] ended the episode, so an arm where the target closed early ran a
        # fraction of the turns of one where it did not, and a length artifact in
        # one arm would read as an identity effect.
        if len(env_versions) > 1:
            raise SystemExit(f"{tag}: arms span {sorted(env_versions)} -- re-run the "
                             "whole set under one env version before viewing it")

        rep = by_tag[tag]
        techniques = sorted({e["technique"] for e in eps if e["technique"]})
        by_technique = []
        for t in techniques:
            means, ns = {}, {}
            for cell in CELL_ORDER:
                vals = [e["dc"] for e in eps
                        if e["technique"] == t and e["cell"] == cell and e["dc"] is not None]
                means[cell] = (sum(vals) / len(vals)) if vals else None
                ns[cell] = len(vals)
            by_technique.append({"technique": t, "means": means, "n": ns})

        bundle["targets"].append({  # type: ignore[union-attr]
            "key": tag,
            "label": label,
            "n_episodes": len(eps),
            "empty_replies": sum(e["empty"] for e in eps),
            "technique_free": sum(1 for e in eps if not e["technique_turns"]),
            "record_honored": rep["record_honored"],
            "env": sorted(env_versions)[0],
            "arms": rep["arms"],
            "invariance": rep["invariance"],
            "directional": rep["directional"],
            "name_vs_record": rep["name_vs_record"],
            "ladder": rep["ladder"],
            "by_technique": by_technique,
            "episodes": eps,
        })
        inv = rep["invariance"] or {}
        print(f"  {tag:12} {len(eps):3} episodes, spread {inv.get('spread', float('nan')):.3f} "
              f"(p={inv.get('spread_p', float('nan')):.3f}), "
              f"{sum(e['empty'] for e in eps)} empty replies")

    # `json.dumps` will happily write bare NaN, which is not JSON and which
    # `JSON.parse` rejects with a syntax error pointing at a byte offset -- so the
    # page dies on load and says nothing about which statistic was undefined. A
    # NaN here is meaningful (a contrast with no shared strata has no delta), so it
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
