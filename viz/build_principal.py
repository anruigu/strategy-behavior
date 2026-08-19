#!/usr/bin/env python
"""Fold the principal-identity runs into one bundle for `principal.html`.

    python viz/build_principal.py

Reads `exploit-bench/results/id-{xp,fw,fs}-<tag>.jsonl` (the identity domain's
three reported readings) and writes `viz/principal.json`.

Why a fourth bundle rather than tabs on `consistency.html`
----------------------------------------------------------
The two pages ask adjacent questions and are not the same experiment.
`consistency.html` sweeps *who is asking* inside one customer-service ticket:
six arms on one axis, one seat, one domain. This sweeps *who each party is*
across eight negotiation dyads and **two seats**, which is the part the design
note (`docs/0817-agent-principal.md`) is actually about:

    'the more interesting direction for your exploitability benchmark is the
    flip: put the agent on the strong side and have it negotiate against a
    vulnerable counterparty ... Running each dyad in both seat assignments gives
    you a principal-side consistency reading and a counterparty-side
    exploitability reading from the same scenario.'

So the unit here is a *reading* -- faithfulness on each seat, exploitability on
the strong one -- and a target has three of them at once. A page built to show
one axis of six arms has nowhere to put the seat.

It computes no statistic of its own. The spread, the permutation null, the paired
contrasts and their CIs all come from `eval/identity_report.py`; this file
reshapes them, adds the validity columns that turned out to matter on the first
sweep, interns repeated text and drops fields the page never reads.

The validity columns are not decorative here
--------------------------------------------
The first sweep found the instrument measuring **action-channel compliance**
rather than negotiation: models argued in prose and never wrote the action line,
so 24-99% of episodes recorded no settlement at all. That is invisible in a
demand-capture mean and fatal to a null result -- an agent that never settles
produces a perfectly flat identity spread for free. So every target carries
`action_rate` (target turns that used the channel), `prose_figure_rate` (turns
that named a number *outside* it) and the no-deal rate, and the page refuses to
show a headline without them.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "exploit-bench"
RESULTS = BENCH / "results"
OUT = Path(__file__).resolve().parent / "principal.json"

if str(BENCH) not in sys.path:
    sys.path.insert(0, str(BENCH))

from eval.identity_report import BASELINE, analyse  # noqa: E402

# (tag, label), frontier first then open weights. The split is the point of
# running both: if identity deference is a pretraining artifact it should not
# care which lab did the training.
TARGETS: tuple[tuple[str, str], ...] = (
    ("opus5", "opus-5"),
    ("gpt56sol", "gpt-5.6-sol"),
    ("dsv4pro", "deepseek-v4-pro"),
    ("kimik3", "kimi-k3"),
    ("gem37flash", "gemini-3.7-flash"),
    ("dsv4flash", "deepseek-v4-flash"),
)

# reading -> (file tag, short label, what a positive delta means)
READINGS: tuple[tuple[str, str, str, str], ...] = (
    ("exploit", "xp", "Exploitability",
     "the agent EXTRACTED MORE from a counterparty of this identity"),
    ("faith_weak", "fw", "Faithfulness · weak seat",
     "the agent gave away MORE of its own principal's position"),
    ("faith_strong", "fs", "Faithfulness · strong seat",
     "the agent gave away MORE of its own principal's position"),
)

READING_NOTE: dict[str, str] = {
    "exploit": "agent acts for the institution; the individual across the table is swept",
    "faith_weak": "agent acts for the individual; its OWN principal is swept",
    "faith_strong": "agent acts for the institution; its OWN principal is swept",
}

IDENTITY_NOTE: dict[str, str] = {
    "unstated": "reference — no background given. Every other arm is read against it",
    "low_status": "signals inexperience or low standing",
    "high_status": "signals seniority or standing — the mirror of low_status",
    "vulnerable": "signals hardship or dependence",
    "abrasive": "signals combativeness — catches punishment, the same bias sign-flipped",
    "dominant": "large, profitable, market-leading",
    "modest": "small, thin-margin",
    "mission": "non-profit or mission-driven",
}

ARM_ORDER = ("unstated", "vulnerable", "low_status", "high_status", "abrasive",
             "dominant", "modest", "mission")

# A figure written in prose rather than through the action channel. Deliberately
# loose: the point is to catch a target negotiating in sentences, and a false
# positive on "$32,000 MSRP" quoted back is far less costly than missing the
# failure mode that invalidated the first sweep.
PROSE_FIGURE = re.compile(r"\$\s?\d[\d,]{2,}|\b\d{2,3},\d{3}\b")
ACTION_LINE = re.compile(r"\[ACTION\]", re.I)


def finite(obj):
    """NaN and infinity -> null, everywhere in the bundle.

    Same reason as `build_consistency.py`: JSON has no NaN, Python writes one
    anyway, and `JSON.parse` then fails the whole document rather than the one
    field -- so a `p` that was legitimately undefined takes the page down with it.
    """
    if isinstance(obj, float):
        return obj if isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [finite(v) for v in obj]
    return obj


def arm_file(tag: str, reading_tag: str) -> Path:
    return RESULTS / f"id-{reading_tag}-{tag}.jsonl"


def complete(tag: str) -> bool:
    """Every reading present. A target mid-sweep is excluded rather than shown thin.

    A partially-swept target is worse than an absent one here: its readings would
    sit in the same tab strip as complete ones with no visual difference except a
    missing section, and the landing page would count it toward the evidence.
    """
    return all(arm_file(tag, rt).exists() for _k, rt, _l, _p in READINGS)


def episode(rec: dict) -> dict:
    c = rec.get("cell") or {}
    turns = rec.get("transcript") or []
    tgt = [t for t in turns if t.get("speaker") == "target"]
    acted = sum(1 for t in tgt if ACTION_LINE.search(t.get("text", "")))
    prose = sum(1 for t in tgt
                if not ACTION_LINE.search(t.get("text", ""))
                and PROSE_FIGURE.search(t.get("text", "")))
    return {
        "case": rec.get("case_id"),
        "base": rec.get("base_id"),
        "reading": rec.get("reading"),
        "seat": rec.get("seat"),
        "identity": rec.get("identity_key"),
        "baseline": bool(rec.get("is_baseline_identity")),
        "varied": rec.get("varied_party"),
        "prompt": rec.get("system_prompt_sha", ""),
        "technique": c.get("technique"),
        "seed": rec.get("seed"),
        "dc": rec.get("demand_capture"),
        "magnitude": rec.get("magnitude"),
        "magnitude_norm": rec.get("magnitude_norm"),
        "floor": rec.get("floor"),
        "ask": rec.get("ask"),
        "realized": rec.get("realized"),
        "settle": rec.get("settle_usd"),
        "mandate_line": rec.get("mandate_line"),
        "direction": rec.get("direction"),
        "conceded_share": rec.get("conceded_share"),
        "settled": bool(rec.get("settled")),
        "inadequate": bool(rec.get("inadequate")),
        "compliant": bool(rec.get("compliant")),
        "acts": rec.get("acts") or [],
        "violations": rec.get("violations") or [],
        "leaked": rec.get("leaked_facts") or [],
        "unparsed": rec.get("unparsed_actions") or [],
        "turns": rec.get("turns"),
        "empty": rec.get("empty_target_turns") or 0,
        "technique_turns": rec.get("technique_turns"),
        # The columns that decide whether any of the above is readable at all.
        "target_turns": len(tgt),
        "action_turns": acted,
        "prose_figure_turns": prose,
        "env": rec.get("versions", {}).get("env", "?"),
        "transcript": [
            {"speaker": t.get("speaker"), "technique": t.get("technique"),
             "text": t.get("text", ""),
             **({"thinking": t["thinking"]} if t.get("thinking") else {})}
            for t in turns
        ],
    }


def reading_block(rows: list[dict], eps: list[dict]) -> dict:
    """One reading for one target: the estimator's output plus the validity read."""
    a = analyse(rows)
    arms = sorted({e["identity"] for e in eps},
                  key=lambda k: (ARM_ORDER.index(k) if k in ARM_ORDER else 99, k))

    per_arm = {}
    for k in arms:
        sub = [e for e in eps if e["identity"] == k]
        d = (a.get("deltas") or {}).get(k)
        per_arm[k] = {
            "n": len(sub),
            "mean_dc": (sum(e["dc"] for e in sub) / len(sub)) if sub else None,
            "no_deal": 1 - (sum(e["settled"] for e in sub) / len(sub)) if sub else None,
            "acts": (sum(len(e["acts"]) for e in sub) / len(sub)) if sub else 0.0,
            "leaks": sum(1 for e in sub if e["leaked"]),
            "delta": d["delta"] if d else None,
            "ci": list(d["ci"]) if d else None,
            "blocks": d["n_blocks"] if d else None,
        }

    tt = sum(e["target_turns"] for e in eps) or 1
    no_deal = [v["no_deal"] for v in per_arm.values() if v["no_deal"] is not None]
    return {
        "n": len(eps),
        "blocks": a.get("usable_blocks", 0),
        "spread": a.get("spread"),
        "p": a.get("p"),
        "null_mean": a.get("null_mean"),
        "null_ci": list(a["null_ci"]) if a.get("null_ci") else None,
        "degenerate": bool(a.get("degenerate_null")),
        "episodes_per_arm": a.get("episodes_per_arm"),
        "level": a.get("level"),
        "spread_by_technique": a.get("spread_by_technique") or {},
        "arms": per_arm,
        # Validity. `action_rate` is the one that decides whether a null spread
        # means "even-handed" or "never negotiated through the scored channel".
        "action_rate": sum(e["action_turns"] for e in eps) / tt,
        "prose_figure_rate": sum(e["prose_figure_turns"] for e in eps) / tt,
        "eps_with_action": sum(1 for e in eps if e["action_turns"]) / (len(eps) or 1),
        "no_deal": 1 - (sum(e["settled"] for e in eps) / (len(eps) or 1)),
        "no_deal_range": (max(no_deal) - min(no_deal)) if no_deal else None,
        "empty_replies": sum(e["empty"] for e in eps),
        "unparsed": sum(len(e["unparsed"]) for e in eps),
    }


def main() -> int:
    prompts: dict[str, str] = {}
    bundle: dict[str, object] = {
        "readings": [{"key": k, "tag": t, "label": lab, "positive": pos,
                      "note": READING_NOTE[k]}
                     for k, t, lab, pos in READINGS],
        "identityNotes": IDENTITY_NOTE,
        "armOrder": list(ARM_ORDER),
        "baseline": BASELINE,
        "prompts": prompts,
        "targets": [],
    }

    for tag, label in TARGETS:
        have = [(k, rt) for k, rt, _l, _p in READINGS if arm_file(tag, rt).exists()]
        if not have:
            print(f"  {tag:18} no runs; skipped")
            continue
        if not complete(tag):
            missing_now = [k for k, rt, _l, _p in READINGS if not arm_file(tag, rt).exists()]
            print(f"  {tag:18} mid-sweep — missing {', '.join(missing_now)}; skipped")
            continue

        readings: dict[str, dict] = {}
        all_eps: list[dict] = []
        env_versions: set[str] = set()
        missing = [k for k, rt, _l, _p in READINGS if not arm_file(tag, rt).exists()]

        for key, rtag in have:
            rows = []
            for line in arm_file(tag, rtag).read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                env_versions.add(rec.get("versions", {}).get("env", "?"))
                sha, text = rec.get("system_prompt_sha"), rec.get("system_prompt")
                if sha and text:
                    prompts.setdefault(sha, text)
                rows.append(rec)
            eps = [episode(r) for r in rows]
            readings[key] = reading_block(rows, eps)
            all_eps.extend(eps)

        # Three readings are comparable only if one harness produced them --
        # the same refusal `build_channels.py` and `build_consistency.py` make,
        # for the same reason: an env change between arms would read as an
        # identity effect.
        if len(env_versions) > 1:
            raise SystemExit(f"{tag}: readings span {sorted(env_versions)} -- re-run "
                             "the whole set under one env version before viewing it")

        bundle["targets"].append({  # type: ignore[union-attr]
            "key": tag,
            "label": label,
            "env": sorted(env_versions)[0] if env_versions else "?",
            "n_episodes": len(all_eps),
            "missing_readings": missing,
            "readings": readings,
            "episodes": all_eps,
        })

        parts = " ".join(
            f"{k.split('_')[0][:2]}:{readings[k]['spread']:.2f}"
            f"/p{readings[k]['p']:.2f}" for k, _ in have)
        act = sum(r["action_rate"] * r["n"] for r in readings.values()) / max(
            1, sum(r["n"] for r in readings.values()))
        print(f"  {tag:18} {len(all_eps):4} episodes  {parts}  action-rate {act:.0%}"
              + (f"  MISSING {','.join(missing)}" if missing else ""))

    if not bundle["targets"]:
        print("no identity runs found; nothing to build")
        return 1

    OUT.write_text(
        json.dumps(finite(bundle), ensure_ascii=False, separators=(",", ":"),
                   allow_nan=False) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
