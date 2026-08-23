"""Recompute cross-play STYLE counters from saved transcripts.

    python rescore_crossplay.py [--out results/crossplay]

`run_crossplay.py` stores every learner turn verbatim in
`<out>/traces/<arm>-vs-<opp>-<game>-<seed>.txt`, so a parsing bug in a style
counter costs a re-parse rather than a re-run. That matters here: the auction's
bid pattern was wrong on the first pass (`[Bid on Item 4: 255]` vs a pattern
that omitted the " on "), and re-playing those episodes against a frontier
opponent would have been paid for twice for no new information.

It also keeps provenance uniform. Cells scored before a fix and cells scored
after it are not comparable if the fix changed what a counter counts, so this
re-derives EVERY cell with the current `crossplay_games` code in one pass rather
than leaving a mixed-vintage summary on disk.

Outcome fields (reward / win) are NOT recomputed -- they come from the
environment at close() and are not recoverable from a transcript. Only `style`
is rewritten.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import crossplay_games as XG  # noqa: E402

# Learner turns only. The opponent's text is in the same file and must not be
# scored as the learner's behaviour.
BLOCK = re.compile(r"^--- LEARNER \(p\d+\)\n(.*?)(?=^--- |\Z)",
                   re.S | re.M)


def actions_from(path: pathlib.Path):
    return [m.group(1).strip() for m in BLOCK.finditer(path.read_text())]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE / "results" / "crossplay"))
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    traces = out / "traces"
    if not traces.exists():
        raise SystemExit(f"no traces under {traces}")

    for f in sorted(out.glob("*__vs__*.json")):
        d = json.loads(f.read_text())
        arm, opp = d["arm"], d["opponent"]
        changed = 0
        per_game = {}
        for row in d["rows"]:
            g = XG.BY_NAME.get(row["game"])
            t = traces / f"{arm}-vs-{opp}-{row['game']}-{row['seed']}.txt"
            if g is None or not t.exists():
                continue
            acts = actions_from(t)
            new = (g.style or (lambda *x: {}))(acts, None, {}, g.learner_id)
            if new != row.get("style"):
                changed += 1
            row["style"] = new
            row["n_learner_actions_reparsed"] = len(acts)
            per_game.setdefault(row["game"], []).append(row)

        for gname, rows in per_game.items():
            keys = sorted({k for r in rows for k in r["style"]})
            d["summary"].setdefault(gname, {})["style"] = {
                k: core.mean([r["style"][k] for r in rows
                              if r["style"].get(k) is not None])
                for k in keys}
        d["rescored"] = True
        f.write_text(json.dumps(d, indent=1))
        print(f"  {f.name:34s} rows={len(d['rows']):4d} style_changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
