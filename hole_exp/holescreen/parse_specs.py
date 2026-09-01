#!/usr/bin/env python
"""Parse the 24 generated game specs into structured records.

Reads docs/native_games/*.md and splits each `GAME:` block into its labelled
sections. Everything downstream quotes RULES and TURN TEMPLATE *verbatim* --
the probe must show the model the text the spec says it would see, not a
paraphrase of it, or the screen measures the paraphrase.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "native_games"
OUT = Path(__file__).resolve().parent / "specs.json"

SECTIONS = ["ROLE", "PHASES", "SCORING", "RULES", "ACTIONS", "TURN TEMPLATE", "HOLE"]


def split_sections(body: str) -> dict:
    idx = []
    for s in SECTIONS:
        m = re.search(rf"^{re.escape(s)}:", body, re.M)
        if m:
            idx.append((m.start(), s, m.end()))
    idx.sort()
    out = {}
    for i, (start, name, end) in enumerate(idx):
        stop = idx[i + 1][0] if i + 1 < len(idx) else len(body)
        out[name] = body[end:stop].strip("\n").rstrip()
    return out


def parse_hole(h: str) -> dict:
    d = {}
    for key in ["kind", "how", "exploit move", "honest move", "detect"]:
        m = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)(?=^\s*(?:kind|how|exploit move|honest move|detect):|\Z)",
                      h, re.M | re.S)
        d[key.replace(" ", "_")] = " ".join(m.group(1).split()) if m else None
    return d


def main() -> int:
    games = []
    for f in sorted(DOCS.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text()
        for block in re.split(r"^GAME:\s*", text, flags=re.M)[1:]:
            block = re.sub(r"\n```\s*$", "", block.rstrip()).rstrip()
            head = block.split("\n", 1)[0]
            sec = split_sections(block)
            title = head.split("--")[0].strip()
            np_ = re.search(r"(\d+)\s+players?", head)
            nr_ = re.search(r"(\d+)\s+rounds?", head)
            games.append({
                "id": f"{f.stem}:{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}",
                "author": f.stem,
                "title": title,
                "headline": head,
                "n_players": int(np_.group(1)) if np_ else None,
                "n_rounds": int(nr_.group(1)) if nr_ else None,
                "role": sec.get("ROLE", ""),
                "phases": sec.get("PHASES", ""),
                "scoring": sec.get("SCORING", ""),
                "rules": sec.get("RULES", ""),
                "actions": sec.get("ACTIONS", ""),
                "turn_template": sec.get("TURN TEMPLATE", ""),
                "hole": parse_hole(sec.get("HOLE", "")),
            })
    OUT.write_text(json.dumps(games, indent=2) + "\n")
    missing = [(g["id"], k) for g in games for k in ("rules", "actions", "turn_template") if not g[k]]
    print(f"parsed {len(games)} games -> {OUT.name}")
    print("authors:", {a: sum(1 for g in games if g['author'] == a) for a in sorted({g['author'] for g in games})})
    print("missing sections:", missing or "none")
    bad = [g["id"] for g in games if not all(g["hole"].get(k) for k in ("kind", "exploit_move", "honest_move", "detect"))]
    print("incomplete HOLE blocks:", bad or "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
