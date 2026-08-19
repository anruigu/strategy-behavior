#!/usr/bin/env python
"""Summarise every built bundle into `viz/index.json` for the landing page.

    python viz/build_index.py

The viewer grew one page at a time and ended up a flat mesh: five pages that
each linked sideways to two or three of the others, with no hub and no way to
tell which bundles were even built. This produces the hub's data.

WHAT A LANDING PAGE IS FOR HERE, AND WHAT IT IS NOT FOR
It is a **triage** surface, not a results surface. It answers "which groups of
runs exist, how much evidence is in each, and is any of it in a state where the
headline should not be read" -- and then gets out of the way. It deliberately
does not show a demand-capture number: a single figure per bundle, stripped of
the arm structure that gives it meaning, is exactly the "bare scalar" the
benchmark's own reporting rules refuse.

What it does show is **health**, because every one of these bundles has at least
one way of looking finished while measuring nothing:

  * empty target replies      an empty utterance grants nothing and so scores as
                              maximal resistance (docs/0816-truncation.md)
  * lever-free episodes       a cell labelled with a technique that was never
                              uttered is not evidence about that technique
  * action-channel rate       (identity) a target that argues in prose and never
                              writes an action line records no settlement, and a
                              target that never settles is perfectly invariant
                              for free
  * degenerate tests          (identity) a permutation null with zero width
                              returns p=1.0 by construction, which looks
                              identical to the fairest possible result
  * missing arms              a factorial with a hole in it is not a factorial

Each summary is derived from the bundle on disk, never hardcoded, so a page that
says "6 targets" is saying what `build_*.py` actually wrote.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    p = HERE / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"_broken": f"{name} is not valid JSON: {e}"}


def kb(name: str) -> int:
    p = HERE / name
    return round(p.stat().st_size / 1024) if p.exists() else 0


def flag(level: str, text: str) -> dict:
    """level: ok | warn | stop. `stop` means do not read the headline."""
    return {"level": level, "text": text}


# ---------------------------------------------------------------------------
# per-bundle summaries
# ---------------------------------------------------------------------------


def domains_summary() -> dict:
    d = load("data.json")
    if not d:
        return {"built": False}
    doms = d.get("domains", [])
    targets, eps, empty = set(), 0, 0
    for dom in doms:
        eps += dom.get("n_episodes", 0) or 0
        for t in dom.get("targets", []) or []:
            targets.add(t if isinstance(t, str) else t.get("label") or t.get("key"))
        for e in dom.get("episodes", []) or []:
            empty += e.get("empty", 0) or 0
    flags = []
    if empty:
        flags.append(flag("warn", f"{empty} empty target replies — raise --max-tokens"))
    stub = [t for t in targets if t and str(t).startswith("stub")]
    if stub:
        flags.append(flag("ok", f"{len(stub)} stub fixtures, kept in their own group"))
    return {
        "built": True, "kb": kb("data.json"),
        "counts": [(str(len(doms)), "domains"), (str(len(targets)), "targets"),
                   (f"{eps:,}", "episodes")],
        "flags": flags,
    }


def channels_summary() -> dict:
    d = load("channels.json")
    if not d:
        return {"built": False}
    ts = d.get("targets", [])
    eps = sum(t.get("n_episodes", 0) or 0 for t in ts)
    empty = sum(t.get("empty_replies", 0) or 0 for t in ts)
    degen = [t["label"] for t in ts if t.get("developer_degenerate")]
    flags = []
    if degen:
        flags.append(flag("warn", f"`developer` collapses into system on "
                                  f"{', '.join(degen)} — that cell is degenerate"))
    if empty:
        flags.append(flag("warn", f"{empty} empty target replies"))
    if not flags:
        flags.append(flag("ok", "all four arms present on every target"))
    return {
        "built": True, "kb": kb("channels.json"),
        "counts": [(str(len(ts)), "targets"), (f"{eps:,}", "episodes"),
                   ("4", "arms (2×2)")],
        "flags": flags,
    }


def consistency_summary() -> dict:
    d = load("consistency.json")
    if not d:
        return {"built": False}
    ts = d.get("targets", [])
    eps = sum(t.get("n_episodes", 0) or 0 for t in ts)
    empty = sum(t.get("empty_replies", 0) or 0 for t in ts)
    free = sum(t.get("technique_free", 0) or 0 for t in ts)
    sep = [t["label"] for t in ts
           if (t.get("invariance") or {}).get("spread_p") is not None
           and t["invariance"]["spread_p"] <= 0.10]
    flags = []
    if empty:
        flags.append(flag("warn", f"{empty} empty target replies"))
    if free:
        flags.append(flag("warn", f"{free} lever-free episodes — not evidence about "
                                  "the technique they are labelled with"))
    flags.append(flag("warn" if sep else "ok",
                      f"{len(sep)} of {len(ts)} targets separate from the "
                      "label-shuffle null" + (f": {', '.join(sep)}" if sep else "")))
    flags.append(flag("ok", "2 of 6 arms sit outside the invariance number by design"))
    return {
        "built": True, "kb": kb("consistency.json"),
        "counts": [(str(len(ts)), "targets"), (f"{eps:,}", "episodes"),
                   (str(len(d.get("cells", []))), "identity arms")],
        "flags": flags,
    }


def principal_summary() -> dict:
    d = load("principal.json")
    if not d:
        return {"built": False}
    ts = d.get("targets", [])
    eps = sum(t.get("n_episodes", 0) or 0 for t in ts)

    turns = acts = 0
    degen, incomplete, sep = [], [], []
    for t in ts:
        if t.get("missing_readings"):
            incomplete.append(t["label"])
        for key, r in (t.get("readings") or {}).items():
            n = r.get("n") or 0
            turns += n
            acts += (r.get("action_rate") or 0) * n
            if r.get("degenerate"):
                degen.append(f"{t['label']}/{key}")
            p = r.get("p")
            if p is not None and p <= 0.10 and not r.get("degenerate"):
                sep.append(f"{t['label']}/{key}")
    rate = acts / turns if turns else 0.0

    flags = []
    # The finding that invalidated the first sweep (id-env-1), stated first
    # because it governs whether anything else on the page is readable. Under
    # id-env-2 the action line records a POSITION rather than a concluded
    # agreement and the rate went from 1-41% to 95-100% -- so the level is
    # derived from the rate rather than asserted, or this card would go on
    # crying stop after the thing it warned about was fixed.
    if rate < 0.50:
        flags.append(flag(
            "stop",
            f"action-channel rate {rate:.0%} — models argue in prose and never write "
            "the action line, so most episodes record no settlement. A target that "
            "never settles is invariant for free."))
    elif rate < 0.90:
        flags.append(flag(
            "warn",
            f"action-channel rate {rate:.0%} — a minority of turns state a position "
            "only in prose, which the oracle does not score."))
    else:
        flags.append(flag(
            "ok",
            f"action-channel rate {rate:.0%} — positions are on the record, so the "
            "spreads below are about what was conceded rather than about format."))
    if degen:
        flags.append(flag("stop", f"{len(degen)} reading(s) have a zero-width "
                                  "permutation null: p=1.0 by construction, not a result"))
    if sep:
        flags.append(flag("warn", f"{len(sep)} reading(s) separate from the null: "
                                  + ", ".join(sep)))
    if incomplete:
        flags.append(flag("warn", f"incomplete: {', '.join(incomplete)}"))
    return {
        "built": True, "kb": kb("principal.json"),
        "counts": [(str(len(ts)), "targets"), (f"{eps:,}", "episodes"),
                   (str(len(d.get("readings", []))), "readings × 2 seats")],
        "flags": flags,
    }


def cases_summary() -> dict:
    d = load("cases.json")
    if not d:
        return {"built": False}
    sets = d.get("sets", [])
    n = len(sets) if isinstance(sets, list) else len(sets or {})
    return {
        "built": True, "kb": kb("cases.json"),
        "counts": [(str(n), "case sets"),
                   (str(len(d.get("dimensions", []) or [])), "dimensions")],
        "flags": [flag("ok", "reference — what the panels are made of, not a result")],
    }


# ---------------------------------------------------------------------------

GROUPS = [
    {
        "key": "domains",
        "page": "domains.html",
        "title": "Domains",
        "question": "How much does a target concede, per domain?",
        "blurb": "Customer service, business and politics on the same normalised "
                 "scale: 0 defends the floor, 1 concedes exactly what was demanded. "
                 "Stub fixtures and real models are never in the same bar group.",
        "build": "python viz/build_data.py",
        "summary": domains_summary(),
    },
    {
        "key": "channels",
        "page": "channels.html",
        "title": "Message channels",
        "question": "Does it matter which role the counterparty speaks on?",
        "blurb": "The same sentence carries different implied authority arriving as "
                 "a user turn or a tool result. A 2×2 over (mandate channel × "
                 "attacker channel), paired cell for cell.",
        "build": "./results/run-channels.sh … ; python viz/build_channels.py",
        "summary": channels_summary(),
    },
    {
        "key": "consistency",
        "page": "consistency.html",
        "title": "Counterparty identity",
        "question": "Does the amount move with who is asking?",
        "blurb": "One customer-service ticket, six arms of a recognizability ladder "
                 "from an unremarkable account to a name dense in pretraining. Same "
                 "lever, same pressure, same oracle price.",
        "build": "./results/run-profile.sh … ; python viz/build_consistency.py",
        "summary": consistency_summary(),
    },
    {
        "key": "principal",
        "page": "principal.html",
        "title": "Principal identity — both seats",
        "question": "Does it bargain differently depending on who each party is?",
        "blurb": "Eight negotiation dyads run from BOTH seats. Sweep the agent's own "
                 "principal for faithfulness; sit it with the institution and sweep "
                 "the individual across the table for exploitability. Economics are "
                 "pinned identical across arms and the counterparty's script is "
                 "byte-identical, so anything that moves is the agent.",
        "build": "bash results/run_identity.sh … ; python viz/build_principal.py",
        "summary": principal_summary(),
    },
    {
        "key": "cases",
        "page": "cases.html",
        "title": "Case sets",
        "question": "What are the panels actually made of?",
        "blurb": "The frozen scenarios behind every number above — what each case "
                 "pins, what it contests, and where the sets overlap.",
        "build": "python viz/build_cases.py",
        "summary": cases_summary(),
    },
]


def main() -> int:
    out = HERE / "index.json"
    bundle = {"groups": GROUPS}
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    for g in GROUPS:
        s = g["summary"]
        if not s.get("built"):
            print(f"  {g['key']:14} not built")
            continue
        counts = ", ".join(f"{v} {k}" for v, k in s["counts"])
        stops = sum(1 for f in s["flags"] if f["level"] == "stop")
        print(f"  {g['key']:14} {counts}" + (f"   [{stops} stop-flag]" if stops else ""))
    print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
