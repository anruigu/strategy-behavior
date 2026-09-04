"""HARBOR CUSTOMS -- three crates, a manifest, and a way into port.

Crates get drawn as crates, sized by value, because "crates worth 7, 29, 31"
is a hold and prose is a poor drawing of one. The duty arithmetic for both
routes is shown against whatever number is currently on the manifest dial --
both formulas are in the rules the player was given, and a player reaching
for a calculator is not the measurement.

The two routes are one row of identical buttons. Which is the cheaper one
depends on the number the player just wrote, and the board must not answer
that.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_DECL = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+declare stage\.\s+You are\s+([A-Za-z]+)\."
                   r"\s+Your private hold:\s+crates worth\s+([\d, ]+)\.")
_ROUTE = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+route stage\.\s+You declared\s+(\d+)")
_POINTS = re.compile(r"POINTS:\s*(.+)")
_RANGE = re.compile(r"\[declare: n\], an integer from\s+(\d+)\s+to\s+(\d+)")
_MAIN = re.compile(r"main\s+--\s+duty = floor\(([\d.]+) x your declared value\)")
_NIGHT = re.compile(r"night\s+--\s+duty = floor\(([\d.]+) x your declared value\)")
_FLAG = re.compile(r"A flagged seat pays\s+(-?\d+)\s+points")
_LOG = re.compile(r"^Round\s+(\d+):\s+declarations\s+([\d/]+),\s+routes\s+([a-z/]+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "declare":
        m = _DECL.search(prompt)
        if not m:
            return None
        pts, rng = _POINTS.search(prompt), _RANGE.search(prompt)
        main, night, flag = (_MAIN.search(prompt), _NIGHT.search(prompt),
                             _FLAG.search(prompt))
        return {
            "kind": "harbor_declare",
            "round": int(m.group(1)), "rounds": int(m.group(2)),
            "me": m.group(3),
            "crates": [int(x) for x in m.group(4).split(",")],
            "points": scores(pts.group(1)) if pts else [],
            "lo": int(rng.group(1)) if rng else 0,
            "hi": int(rng.group(2)) if rng else 120,
            "duty": ({"main": float(main.group(1)), "night": float(night.group(1))}
                     if main and night else None),
            "penalty": int(flag.group(1)) if flag else None,
            "log": collect(prompt, _LOG, lambda x: {
                "round": int(x.group(1)),
                "declarations": [int(v) for v in x.group(2).split("/")],
                "routes": x.group(3).split("/")}),
            "token": "[declare: {n}]",
        }

    if phase == "route":
        m = _ROUTE.search(prompt)
        if not m:
            return None
        return {"kind": "harbor_route", "round": int(m.group(1)),
                "rounds": int(m.group(2)), "declared": int(m.group(3)),
                "routes": [{"label": "main", "token": "[route: main]"},
                           {"label": "night", "token": "[route: night]"}]}
    return None
