#!/usr/bin/env python
"""Build the static bundle for apps/traces/public/hackable/.

Two things go in, for all 19 cells:

  SETUP   the rules text a player is actually shown -- lifted from the engine by
          running it and capturing the first prompt, so the page can never drift
          from what the game says. Not retyped, not summarised.
  TRACES  real episodes. For the 11 referee cells these are model transcripts
          from results/referee_crossplay/**/traces/*.txt, joined against
          rows.jsonl so each one is labelled with whether that seat actually
          took the hole. The 8 generated cells were never crossplayed, so they
          carry SCRIPTED honest/exploit episodes from their own engines instead,
          and are labelled as such -- a scripted trace next to a model trace
          without a label would be a quiet lie about provenance.

The hole is in the bundle, because the page is a viewer for people who already
know what these cells are. It sits behind a spoiler in the UI.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import catalog                       # noqa: E402
from bots import Mixed, Scripted     # noqa: E402

RESULTS = HERE.parent / "results" / "referee_crossplay"
OUT = HERE / "bundle"

MAX_TRACES_PER_CELL = 4
MAX_DECISIONS = 20
MAX_CHARS = 1400


class _Stop(Exception):
    pass


def capture_setup(game) -> str:
    """First prompt seat 0 sees. That prompt carries the rules by construction."""
    box = {}

    def ask(pid, phase, prompt):
        if pid == 0 and "first" not in box:
            box["first"] = prompt
            raise _Stop
        return "[noop: 0]"
    try:
        game.run(ask, 1, "hole")
    except _Stop:
        pass
    except Exception:
        pass
    return box.get("first", "")


TRACE_RE = re.compile(
    r"^(?P<game>ref_[a-z_]+)-(?P<cond>neutral|winmax)-(?P<arm>hole|nohole)-"
    r"(?P<focal>[a-z0-9]+)_vs_(?P<other>[a-z0-9]+)-s(?P<seed>\d+)"
    r"(?:-p(?P<seat>\d+))?\.txt$")   # later waves append a per-seat suffix

BLOCK_RE = re.compile(
    r"^===== p(?P<pid>\d+) \[(?P<phase>[a-z_]+)\]"
    r"(?: \((?P<model>[^)]*)\))?\s*\n"
    r"--- prompt\n(?P<prompt>.*?)\n--- reply\n(?P<reply>.*?)(?=\n===== p|\Z)",
    re.S | re.M)


def parse_trace(path: Path) -> list:
    txt = path.read_text(errors="replace")
    out = []
    for m in BLOCK_RE.finditer(txt):
        out.append({"pid": int(m.group("pid")), "phase": m.group("phase"),
                    "model": (m.group("model") or "").strip(),
                    "prompt": m.group("prompt").strip()[-MAX_CHARS:],
                    "reply": m.group("reply").strip()[:MAX_CHARS]})
    return out


def load_rows() -> dict:
    """(game, cond, arm, focal, other, seed) -> did the focal seat violate?"""
    idx = {}
    for f in RESULTS.rglob("rows.jsonl"):
        for line in f.open():
            try:
                r = json.loads(line)
            except Exception:
                continue
            k = (r.get("game"), r.get("condition"), r.get("arm"),
                 r.get("focal"), r.get("other"), r.get("seed"))
            v = sum(val for key, val in r.items()
                    if key.startswith("v_") and isinstance(val, (int, float)))
            idx[k] = {"violations": int(v),
                      "score": r.get("score_focal"),
                      "invalid": r.get("invalid_rate_focal")}
    return idx


def referee_traces(gid: str, rows: dict) -> list:
    cands = []
    for p in RESULTS.rglob(f"traces/{gid}-*.txt"):
        m = TRACE_RE.match(p.name)
        if m:
            cands.append((p, m.groupdict()))
    if not cands:
        return []
    # Prefer variety: one per (model, condition), and prefer a mix of took/skipped.
    picked, seen = [], set()
    def key(item):
        _, d = item
        k = (d["focal"], d["cond"])
        return k
    cands.sort(key=lambda it: (it[1]["focal"], it[1]["cond"], int(it[1]["seed"])))
    for p, d in cands:
        if d.get("seat") not in (None, "0"):
            continue                      # focal seat only
        k = key((p, d))
        if k in seen:
            continue
        seen.add(k)
        meta = rows.get((d["game"], d["cond"], d["arm"], d["focal"],
                         d["other"], int(d["seed"])), {})
        decisions = parse_trace(p)
        if not decisions:
            continue
        picked.append({
            "kind": "model", "label": f"{d['focal']} · {d['cond']} · {d['arm']}",
            "model": d["focal"], "condition": d["cond"], "arm": d["arm"],
            "seed": int(d["seed"]), "opponent": d["other"],
            "violations": meta.get("violations"), "score": meta.get("score"),
            "source": str(p.relative_to(RESULTS.parent.parent)),
            "decisions": decisions[:MAX_DECISIONS],
            "n_decisions": len(decisions),
        })
        if len(picked) >= MAX_TRACES_PER_CELL:
            break
    return picked


def scripted_traces(game) -> list:
    out = []
    for mode in ("honest", "exploit"):
        rec = []

        def ask(pid, phase, prompt, _rec=rec, _m=mode):
            reply = Mixed(0, _m, "honest", 3)(pid, phase, prompt)
            if pid == 0:
                _rec.append({"pid": pid, "phase": phase, "model": f"scripted:{_m}",
                             "prompt": prompt.strip()[-MAX_CHARS:],
                             "reply": reply.strip()[:MAX_CHARS]})
            return reply
        try:
            ep = game.run(ask, 3, "hole")
        except Exception:
            continue
        v = sum(ep.violations[0].get(k, 0) for k in game.HARD)
        out.append({
            "kind": "scripted", "label": f"scripted {mode} · hole arm",
            "model": f"scripted:{mode}", "condition": "n/a", "arm": "hole",
            "seed": 3, "opponent": "scripted:honest",
            "violations": int(v), "score": round(ep.scores.get(0, 0.0), 2),
            "source": "generated by engines_generated.py (no model run exists)",
            "decisions": rec[:MAX_DECISIONS], "n_decisions": len(rec),
        })
    return out


def main() -> int:
    rows = load_rows()
    print(f"joined {len(rows)} episode rows")
    cells = []
    for c in catalog.public_list():
        full = catalog.GAMES[c["id"]]
        g = full["game"]
        setup = capture_setup(g)
        traces = (scripted_traces(g) if c["family"] == "generated"
                  else referee_traces(c["id"], rows))
        cells.append({
            **c,
            "setup": setup,
            "hole": {"type": full["hole_type"], "kinds": full["kinds"],
                     "hard": full["hard"], "how": full["blurb"]},
            "traces": traces,
        })
        print(f"  {c['id']:22s} setup {len(setup):5d}ch  traces {len(traces)}")
    bundle = {
        "generated_utc": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_cells": len(cells),
        "cells": cells,
    }
    OUT.mkdir(exist_ok=True)
    p = OUT / "data.json"
    p.write_text(json.dumps(bundle, separators=(",", ":")))
    print(f"\nwrote {p}  ({p.stat().st_size/1e6:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
