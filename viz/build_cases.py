#!/usr/bin/env python3
"""Fold both case sets into one bundle for `cases.html`.

    python viz/build_cases.py

Two sets, side by side and labelled, because the whole value of the split is that
it is real: `cs-cases-train-v1` is what RL draws from and `cs-cases-v2` is the
frozen instrument. If a case id ever appears in both, this says so loudly -- a
silent overlap would turn every future benchmark number into a training number.

Everything numeric comes from the oracle and the verifier, not from this file:
`headroom` is `F - V_ask`, `owed` and `ceiling` are the rule's own bundles, and
the difficulty verdicts are read out of `results/filter-open.json` exactly as
`eval/filter_dims.py` wrote them. The page shows what the instrument says; it
does not re-derive it.
"""

from __future__ import annotations

import json
import sys
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "exploit-bench"
if str(BENCH) not in sys.path:
    sys.path.insert(0, str(BENCH))

OUT = Path(__file__).resolve().parent / "cases.json"
FILTER = BENCH / "results" / "filter-open.json"

# Where eval traces come from. Screens and baseline arms, both run with
# --save-transcripts, both on the frozen case set.
TRACE_GLOBS = ("results/screen2-*.jsonl", "results/chan-*-system-user.jsonl")

# 49 MB of transcripts exist across those files, so the bundle carries a full
# *index* of every episode and the transcripts of a sample. The sample is chosen
# rather than truncated: per model, the most-conceded and least-conceded episode,
# plus a compliant one if neither was. Those are the three a reader wants -- the
# worst case, the best case, and what getting it right looked like -- and the rule
# is stated on the page so nobody mistakes the sample for the population.
TRACES_PER_CASE = 9

SETS = [
    ("train", "cs-cases-train-v1.json", "cs-train-v1",
     "What RL draws from. Never evaluated on. Same cs-v1 policy and oracle as the "
     "frozen panels, new tickets, no shared case ids."),
    ("eval", "cs-cases-v2.json", "cs-screen-v2",
     "The frozen instrument. Never trained on. Every published number and the "
     "open-vs-frontier plot rest on these cases."),
]


def finite(obj):
    if isinstance(obj, float):
        return obj if isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [finite(v) for v in obj]
    return obj


def case_rows(case_set: str, panel: str) -> list[dict]:
    """One row per case, priced by the oracle that scores the benchmark."""
    import domains.all  # noqa: F401  (registers the domains)
    from core.registry import get_domain
    from domains.customer_service.oracle import CSOracle

    domain = get_domain("customer_service")
    run = domain.load(panel)
    policy = run.extras["policy"]

    rows = []
    for cid, case in sorted(run.scenarios.items()):
        o = CSOracle(case, policy)
        matching = policy.matching(case.issue, case.facts)
        owed = o.entitlement()
        # The widest ceiling any matching rule allows: the top of the compliant
        # band, which is what makes a generous-but-compliant grant legal.
        ceiling = None
        if matching:
            best = max(matching, key=lambda r: -o.cost(r.ceiling(case.facts)))
            ceiling = best.ceiling(case.facts).as_dict()
        rows.append({
            "case": cid,
            "issue": case.issue,
            # Derived exactly as the reward's class is: does a rule match the
            # *true* facts, and does the customer assert something the account
            # contradicts.
            "klass": "entitled" if matching else "no-rule",
            "contested": {k: {"truth": t, "claim": c}
                          for k, (t, c) in case.contested().items()},
            "floor": o.floor(),
            "ask": o.ask(),
            "cap": o.cap(),
            "headroom_usd": o.floor() - o.ask(),
            "penalty_base": o.penalty_base(),
            "matched_rule": (best.id if matching else None),
            "owed": owed.as_dict(),
            "ceiling": ceiling,
            "ask_grant": case.ask_grant.as_dict(),
            "ask_acts": list(case.ask_acts),
            # The sentence the customer actually says, generated from the priced
            # ask so the two cannot drift.
            "demand_text": case.public.get("demand_text", ""),
            "facts": dict(case.facts),
            "public": {k: v for k, v in case.public.items() if k != "demand_text"},
        })
    return rows


def _episode_index(rec: dict, source: str) -> dict:
    return {
        "target": rec.get("versions", {}).get("target", source),
        "technique": (rec.get("cell") or {}).get("technique"),
        "dc": rec.get("demand_capture"),
        "compliant": bool(rec.get("compliant")),
        "inadequate": bool(rec.get("inadequate")),
        "turns": rec.get("turns"),
        "technique_turns": rec.get("technique_turns"),
        "empty": rec.get("empty_replies") or 0,
        "grant": {k: v for k, v in (rec.get("grant") or {}).items() if v},
        "violations": rec.get("violations") or [],
        "source": source,
    }


def _pick(records: list[tuple[dict, dict]]) -> list[tuple[dict, dict]]:
    """Most conceded, least conceded, and a compliant one -- per target."""
    by_target: dict[str, list[tuple[dict, dict]]] = {}
    for idx, rec in records:
        by_target.setdefault(idx["target"], []).append((idx, rec))
    out: list[tuple[dict, dict]] = []
    for group in by_target.values():
        ranked = sorted(group, key=lambda t: (t[0]["dc"] is None, t[0]["dc"]))
        picks = [ranked[-1], ranked[0]]
        if not any(p[0]["compliant"] for p in picks):
            ok = next((g for g in group if g[0]["compliant"]), None)
            if ok:
                picks.append(ok)
        seen: set[int] = set()
        for p in picks:
            if id(p[1]) not in seen:
                seen.add(id(p[1]))
                out.append(p)
    return out[:TRACES_PER_CASE]


def load_traces() -> dict[str, dict]:
    """case_id -> {index: [...], traces: [...]} from the eval runs."""
    import glob

    per_case: dict[str, list[tuple[dict, dict]]] = {}
    for pattern in TRACE_GLOBS:
        for path in sorted(glob.glob(str(BENCH / pattern))):
            name = Path(path).name
            for line in Path(path).read_text().splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                if "transcript" not in rec:
                    continue
                per_case.setdefault(rec["case_id"], []).append(
                    (_episode_index(rec, name), rec))

    out: dict[str, dict] = {}
    for case, records in per_case.items():
        picked = _pick(records)
        out[case] = {
            "n_episodes": len(records),
            "n_targets": len({i["target"] for i, _ in records}),
            "index": [i for i, _ in records],
            "traces": [{
                **idx,
                "reward_terms": {k: rec.get("reward_terms", {}).get(k)
                                 for k in ("shortfall_norm", "excess_norm", "prohib_norm")},
                "turns_detail": [
                    {"speaker": t.get("speaker"), "technique": t.get("technique"),
                     "text": t.get("text", ""),
                     **({"thinking": t["thinking"]} if t.get("thinking") else {})}
                    for t in rec.get("transcript") or []
                ],
            } for idx, rec in picked],
        }
    return out


def main() -> int:
    verdicts: dict[str, dict] = {}
    dims: list[dict] = []
    if FILTER.exists():
        blob = json.loads(FILTER.read_text())
        verdicts = {c["case"]: c for c in blob.get("cases", [])}
        dims = blob.get("dimensions", {}).get("rows", [])
    else:
        print(f"  {FILTER.name} missing -- no difficulty verdicts to show")

    traces = load_traces()
    bundle: dict[str, object] = {
        "sets": [], "dimensions": dims,
        "trace_rule": (f"Per case: every episode is indexed; transcripts are kept for "
                       f"the most- and least-conceded episode per target plus a "
                       f"compliant one, capped at {TRACES_PER_CASE}."),
    }
    seen: dict[str, str] = {}
    for key, case_set, panel, blurb in SETS:
        rows = case_rows(case_set, panel)
        for r in rows:
            r["verdict"] = (verdicts.get(r["case"], {}) or {}).get("verdict", "")
            r["by_model"] = (verdicts.get(r["case"], {}) or {}).get("by_model", {})
            r["spread"] = (verdicts.get(r["case"], {}) or {}).get("spread")
            r["across_models"] = (verdicts.get(r["case"], {}) or {}).get("across_models")
            r["traces"] = traces.get(r["case"], {"n_episodes": 0, "n_targets": 0,
                                                 "index": [], "traces": []})
            if r["case"] in seen and seen[r["case"]] != key:
                r["leak"] = f"also in the {seen[r['case']]} set"
            seen[r["case"]] = key
        bundle["sets"].append({
            "key": key, "case_set": case_set, "panel": panel, "blurb": blurb,
            "n": len(rows),
            "n_entitled": sum(1 for r in rows if r["klass"] == "entitled"),
            "cases": rows,
        })
        n_tr = sum(len(r["traces"]["traces"]) for r in rows)
        n_ep = sum(r["traces"]["n_episodes"] for r in rows)
        print(f"  {key:5} {case_set:26} {len(rows):3} cases "
              f"({sum(1 for r in rows if r['klass'] == 'entitled')} entitled) · "
              f"{n_ep} eval episodes indexed, {n_tr} transcripts kept")

    overlap = sorted(
        {r["case"] for s in bundle["sets"] for r in s["cases"] if r.get("leak")})
    bundle["overlap"] = overlap
    if overlap:
        print(f"  !! {len(overlap)} case ids appear in both sets: {overlap}")

    OUT.write_text(json.dumps(finite(bundle), ensure_ascii=False,
                              separators=(",", ":"), allow_nan=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
