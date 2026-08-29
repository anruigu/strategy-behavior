#!/usr/bin/env python
"""Build `viz/referee.json` — the referee-hole cross-play traces, for the deck.

    python viz/build_referee.py
    python viz/build_referee.py --root hole_exp/results/referee_crossplay

`hole_exp/serve_referee_traces.py` is the LOCAL viewer: a stdlib server behind
an SSH LocalForward, which is the right tool while a wave is still landing
because it re-reads the tree on demand. This is the SHARED one. `apps/traces`
in the theseus monorepo is a prebuilt static bundle on `traces.flt.build`, so
there is no server to ask and the whole corpus has to arrive as one JSON
sibling next to one HTML page, exactly like `domains.json` / `domains.html`.

Size is why that is viable at all: the corpus is 19.5 MB of JSON and gzips to
1.6 MB, because a trace is repetitive English and every turn restates the
board. Vercel negotiates the encoding, so the wire cost is under the existing
`principal.json` (13.4 MB raw) that the deck already ships. No sharding, no
directory in `sync.sh`, no departure from the one-page-one-bundle contract.

The loader is imported from the local viewer rather than reimplemented, so the
two cannot drift: same role labels, same speaker fields, same violation
detectors re-derived from the prompt.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "hole_exp"))

DEFAULT_ROOT = REPO / "hole_exp" / "results" / "referee_crossplay"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--out", default=str(HERE / "referee.json"))
    a = ap.parse_args()

    sys.argv = [sys.argv[0]]          # the viewer parses argv at import time
    import serve_referee_traces as V  # noqa: PLC0415

    root = pathlib.Path(a.root)
    if not root.is_dir():
        raise SystemExit(f"no trace root at {root}")
    eps = V.load_all(root)
    if not eps:
        raise SystemExit(f"no episodes found under {root}")

    waves, games, models = {}, {}, {}
    for e in eps.values():
        waves[e["wave"]] = waves.get(e["wave"], 0) + 1
        games[e["game"]] = games.get(e["game"], 0) + 1
        models[e["focal"]] = models.get(e["focal"], 0) + 1

    bundle = {
        "generated_from": str(root),
        "episodes": sorted(eps.values(),
                           key=lambda e: (e["game"], e["condition"],
                                          e["focal"], e["seed"])),
        "totals": {
            "episodes": len(eps),
            "turns": sum(e["n_turns"] for e in eps.values()),
            "flagged": sum(e["n_violations"] for e in eps.values()),
            "with_reasoning": sum(1 for e in eps.values()
                                  if e["has_reasoning"]),
            "waves": waves, "games": games, "models": models,
        },
    }
    out = pathlib.Path(a.out)
    out.write_text(json.dumps(bundle, ensure_ascii=False,
                              separators=(",", ":")) + "\n", encoding="utf-8")
    t = bundle["totals"]
    print(f"  referee.json  {out.stat().st_size/1e6:.1f} MB  "
          f"{t['episodes']} episodes, {t['turns']} turns, "
          f"{t['flagged']} flagged, {t['with_reasoning']} with reasoning")
    for w, n in sorted(waves.items()):
        print(f"    {w:18s}{n:5d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
