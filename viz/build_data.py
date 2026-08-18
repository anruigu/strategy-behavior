#!/usr/bin/env python
"""Fold the eval JSONL into one compact bundle for the trace viewer.

    python viz/build_data.py

Reads `exploit-bench/results/viz/<domain>-<target>.jsonl` (written by
`eval/runner.py --save-transcripts`) and writes `viz/data.json`.

Targets are **discovered from the filenames**, not hardcoded. The three stub
profiles are still recognised by name and grouped as `stub`; anything else is a
real model and lands in the `frontier` group. That split is not cosmetic -- the
two groups answer different questions. A stub is a wiring check with a known
answer (the defender should score exactly 0.000), while a frontier trace is
evidence about a model, and reading one as the other is how a plumbing fixture
gets mistaken for a result.

Deliberately thin: it reshapes and drops fields the page never reads. It
computes no statistic the runner did not already compute -- `demand_capture`,
`magnitude`, `floor/ask/cap/realized` and the sensitivity sweep all come from
the record as written, because those are the numbers the oracle priced and the
viewer's job is to show them, not to recompute them. The two rates it does
derive (`inadequate_rate`, `leak_rate`) are counts of flags the runner already
set, surfaced beside the mean because a low score with a high under-grant rate
is a competence failure rather than resistance.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "exploit-bench" / "results" / "viz"
OUT = Path(__file__).resolve().parent / "data.json"

DOMAINS = ("politics", "customer_service", "business")
STUBS = ("defender", "sycophant", "stonewaller")

# Open-weights models evaluated as RL base-model candidates. Kept distinct from
# the frontier group because the finding they support depends on the
# distinction: on `bz-candidate-v1` every open candidate sits at or below
# sonnet-5 on lift, which is only legible if the two sets are not pooled.
OPEN = {
    "qwen3827b", "qwen3627b", "qwen359b", "qwen3527b",
    "qwen314b", "qwen38b", "gptoss20b", "gptoss120b",
}

LABEL = {
    "politics": "Politics",
    "customer_service": "Customer service",
    "business": "Business",
}
BLURB = {
    "politics": "Ally coercion at the Paris peace talks, 24 Nov 1972 — the target holds "
                "Nguyen Phu Duc's seat against Kissinger's team. Panel pol-smoke-v1.",
    "customer_service": "A support agent under a written policy, worked by a scripted "
                        "counterparty. Panel cs-smoke-v1.",
    "business": "Commercial renewal negotiation against a deal-desk mandate. Stub targets "
                "on bz-smoke-v1; frontier targets on bz-trace-v1, which covers a verified "
                "entitlement, a contested claim, and both halves of the trust pair.",
}

# Filename stem -> display label, for targets whose slug loses its punctuation.
TARGET_LABEL = {
    "gemini31pro": "gemini-3.1-pro",
    "gemini37flash": "gemini-3.7-flash",
    "gpt56sol": "gpt-5.6-sol",
    "deepseekv4pro": "deepseek-v4-pro",
    "sonnet5": "sonnet-5",
    "opus5": "opus-5",
    "kimik3": "kimi-k3",
}

# Flags worth surfacing per domain; absent keys are simply skipped.
FLAGS = ("compliant", "inadequate", "referred", "accepted", "walked", "closed_by_target")

# Difficulty-filter output, keyed by (technique, case_id). Attached to episodes
# so the verdict that decides whether a cell is worth training on is readable
# next to an actual trace of that cell, rather than only as a table in a
# separate markdown file.
DIFFICULTY_GLOB = "difficulty-*.json"


def load_difficulty(results: Path) -> dict[str, dict]:
    """{(technique|case_id): cell stats} across every difficulty run present."""
    out: dict[str, dict] = {}
    for path in sorted(results.glob(DIFFICULTY_GLOB)):
        try:
            d = json.loads(path.read_text())
        except Exception:
            continue
        for c in d.get("cells", []):
            out[f"{c['technique']}|{c['case_id']}"] = {
                "target": d.get("target"),
                "k": d.get("k"),
                "pass_rate": c.get("pass_rate"),
                "sd_dc": c.get("sd_dc"),
                "mean_dc": c.get("mean_dc"),
                "bucket": c.get("bucket"),
                "solved": c.get("solved"),
                "n": c.get("n"),
            }
    return out


def scenario_set_of(case_id: str) -> str:
    """`bzt-` ids come from the generated training set; everything else is eval.

    Worth surfacing prominently: the frozen eval scenarios are the instrument,
    and a number computed on a training scenario is not comparable to one
    computed on them. Mixing the two silently in a trace list is how that
    distinction gets lost.
    """
    return "train" if str(case_id).startswith("bzt-") else "eval"


def episode(rec: dict, target: str, prompts: dict[str, str],
            difficulty: dict[str, dict] | None = None) -> dict:
    """One episode, with its system prompt interned into `prompts`.

    The brief is a function of the scenario, not of the cell, so every episode
    of a case carries a byte-identical copy. Storing it inline would have added
    roughly a quarter of a megabyte of duplicate text; interning by content
    hash keeps one copy and hands the episode a key.
    """
    cell = rec.get("cell") or {}
    prompt_ref = None
    sysmsg = rec.get("system_prompt")
    if sysmsg:
        import hashlib

        prompt_ref = hashlib.sha256(sysmsg.encode("utf-8")).hexdigest()[:12]
        prompts.setdefault(prompt_ref, sysmsg)
    cell_key = f"{(cell.get('technique') or '')}|{rec.get('case_id')}"
    return {
        "prompt_ref": prompt_ref,
        "set": scenario_set_of(rec.get("case_id")),
        "difficulty": (difficulty or {}).get(cell_key),
        "target": target,
        "case": rec.get("case_id"),
        "technique": cell.get("technique"),
        "intensity": cell.get("intensity"),
        "informed": cell.get("informed"),
        "dc": rec.get("demand_capture"),
        "magnitude": rec.get("magnitude"),
        "floor": rec.get("floor"),
        "ask": rec.get("ask"),
        "cap": rec.get("cap"),
        "realized": rec.get("realized"),
        "coverage": rec.get("ask_coverage"),
        "turns": rec.get("turns"),
        "flags": {k: rec[k] for k in FLAGS if k in rec},
        "grant": rec.get("grant") or {},
        "positions": rec.get("positions") or {},
        "acts": rec.get("acts") or [],
        "withheld": rec.get("withheld_defensible") or [],
        "unsupported": rec.get("unsupported_concessions") or [],
        "leaked": rec.get("leaked_facts") or [],
        "violations": rec.get("violations") or [],
        "sensitivity": rec.get("sensitivity_by_penalty_scale") or {},
        # `thinking` rides alongside `text`, never merged into it. The runner
        # keeps them apart because only the utterance is scored, and the viewer
        # keeps them apart for the same reason -- a reader should never have to
        # wonder whether the counterparty saw a given line.
        "transcript": [
            {
                "speaker": t.get("speaker"),
                "technique": t.get("technique"),
                "text": t.get("text", ""),
                **({"thinking": t["thinking"]} if t.get("thinking") else {}),
            }
            for t in (rec.get("transcript") or [])
        ],
    }


def discover(dom: str) -> list[tuple[str, Path]]:
    """(target, path) for every run file of this domain, stubs first.

    `*.partial.jsonl` is skipped: a partial file is a run still in flight, and
    picking it up would put a half-finished target on the same axis as complete
    ones under a name like `qwen3627b.partial`.
    """
    found = [(p.stem[len(dom) + 1:], p) for p in sorted(SRC.glob(f"{dom}-*.jsonl"))
             if not p.name.endswith(".partial.jsonl")]
    return sorted(
        found,
        key=lambda t: (t[0] not in STUBS,
                       STUBS.index(t[0]) if t[0] in STUBS else t[0]),
    )


def means_by(eps: list[dict], targets: list[str], dim: str) -> list[dict]:
    acc: dict[tuple[str, str], list[float]] = defaultdict(list)
    for e in eps:
        k = e.get(dim)
        if k and e["dc"] is not None:
            acc[(k, e["target"])].append(float(e["dc"]))
    keys = sorted({k for k, _ in acc})
    return [
        {
            dim: k,
            "means": {t: (sum(acc[(k, t)]) / len(acc[(k, t)]) if acc.get((k, t)) else None)
                      for t in targets},
            "n": {t: len(acc.get((k, t), [])) for t in targets},
        }
        for k in keys
    ]


def main() -> int:
    bundle: dict[str, object] = {"domains": []}
    for dom in DOMAINS:
        runs = discover(dom)
        if not runs:
            print(f"  {dom:18} no run files - skipped")
            continue
        eps: list[dict] = []
        targets: list[dict] = []
        prompts: dict[str, str] = {}
        difficulty = load_difficulty(SRC.parent)
        for target, path in runs:
            n0 = len(eps)
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    eps.append(episode(json.loads(line), target, prompts, difficulty))
            if len(eps) == n0:
                continue
            mine = eps[n0:]
            base = target[:-6] if target.endswith("-train") else target
            targets.append({
                "key": target,
                "label": TARGET_LABEL.get(target, target),
                # `kind` describes the TARGET (a stub, an open-weights model, a
                # frontier model). Which scenario *set* a run used is a separate
                # dimension, carried per-episode as `set` and filtered in the UI.
                #
                # These were briefly conflated -- a training run got its own
                # `kind` -- which put a model's train and eval traces in
                # different groups and made the one comparison worth having
                # impossible: the same model, same cell, one scenario it trains
                # on and one it is scored on.
                "kind": ("stub" if base in STUBS
                         else "open" if base in OPEN else "frontier"),
                "sets": sorted({e["set"] for e in mine}),
            })
        if not eps:
            continue

        keys = [t["key"] for t in targets]
        summary = {}
        for t in keys:
            mine = [e for e in eps if e["target"] == t]
            vals = [float(e["dc"]) for e in mine if e["dc"] is not None]
            mags = [float(e["magnitude"]) for e in mine if e["magnitude"] is not None]
            summary[t] = {
                "n": len(vals),
                "mean_dc": (sum(vals) / len(vals)) if vals else None,
                "max_dc": max(vals) if vals else None,
                "min_dc": min(vals) if vals else None,
                "mean_magnitude": (sum(mags) / len(mags)) if mags else None,
                "inadequate_rate": (sum(1 for e in mine if e["flags"].get("inadequate"))
                                    / len(mine)) if mine else None,
                "leak_rate": (sum(1 for e in mine if e["leaked"]) / len(mine))
                if mine else None,
            }

        bundle["domains"].append(  # type: ignore[union-attr]
            {
                "key": dom,
                "label": LABEL[dom],
                "blurb": BLURB[dom],
                "n_episodes": len(eps),
                "targets": targets,
                "prompts": prompts,
                "summary": summary,
                "by_technique": means_by(eps, keys, "technique"),
                "by_case": means_by(eps, keys, "case"),
                "episodes": eps,
            }
        )
        groups: dict[str, int] = defaultdict(int)
        for t in targets:
            groups[t["kind"]] += 1
        parts = " + ".join(f"{groups[k]} {k}" for k in ("stub", "open", "frontier")
                           if groups[k])
        sets: dict[str, int] = defaultdict(int)
        for e in eps:
            sets[e["set"]] += 1
        withdiff = sum(1 for e in eps if e.get("difficulty"))
        print(f"  {dom:18} {len(eps):4} episodes ({dict(sets)}), {parts} targets, "
              f"{len(prompts)} prompt{'' if len(prompts) == 1 else 's'}, "
              f"{withdiff} with difficulty stats")

    OUT.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + "\n",
                   encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(ROOT)} ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
