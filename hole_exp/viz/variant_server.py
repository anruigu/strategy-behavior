#!/usr/bin/env python
"""A local browser for the variant catalogue.

    python viz/variant_server.py --port 8801     # then open the URL
    python viz/variant_server.py --host 0.0.0.0  # if you need it off-box

Serves `results/0902_variants/catalogue.json` as a per-game comparison: pick a
game, see every branch of it overlaid on one temptation curve and one group
curve, with the quality-control verdict beside each.

AND IT RE-MEASURES LIVE. `POST /api/measure` takes a cell and a dict of knob
overrides and returns the same two curves, computed on the spot from scripted
seats. A full audit of one cell is a median 60ms, so the slider panel is a
real control rather than a mock-up: move a number, get the curve the change
actually produces. Nothing here runs a model and nothing costs anything.

WHY A SERVER AND NOT A STATIC PAGE. The catalogue alone is a static file and
would serve fine from disk, but then the knobs would be decoration. The whole
argument of `research_logs/0902-payoff-variants-plan.md` section 10 is that
the measurement is cheap enough to put behind a slider, and that is only true
if the slider can call the measurement.

No auth, no persistence, stdlib only. Bind to localhost unless you mean
otherwise.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "hackable_games"))

CATALOGUE = ROOT.parent / "results" / "0902_variants" / "catalogue.json"
PAGE = HERE / "static" / "variants.html"

_lazy: Dict[str, Any] = {}


def _engine():
    """Import and register the engines once, on the first live measurement."""
    if not _lazy:
        import exploit_curve as EC
        import variants as V
        import variant_audit as VA
        V.register()
        _lazy.update(EC=EC, V=V, VA=VA)
    return _lazy


def measure_live(cell: str, knobs: Dict[str, Any]) -> Dict:
    m = _engine()
    V, VA = m["V"], m["VA"]
    coerced: Dict[str, Any] = {}
    defaults = V.tunable(cell)
    for k, val in knobs.items():
        if k not in defaults:
            raise KeyError(f"{cell} has no tunable `{k}`")
        d = defaults[k]
        if isinstance(d, bool):
            coerced[k] = bool(val)
        elif isinstance(d, int) and not isinstance(d, bool):
            coerced[k] = int(round(float(val)))
        elif isinstance(d, float):
            coerced[k] = float(val)
        else:                       # dict / tuple knobs are not on a slider
            raise TypeError(f"`{k}` is a {type(d).__name__}, not a slider knob")
    v = V.Variant(vid=f"{cell}@live", cell=cell, label="live", axis="level",
                  intent="--", note="measured just now", knobs=coerced)
    row = VA.measure(v)
    row["qc"] = VA.qc(row, None, {})
    return row


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):          # quiet
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj).encode(), "application/json")

    def do_GET(self) -> None:           # noqa: N802
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/catalogue":
            if not CATALOGUE.exists():
                self._json({"error": f"no catalogue at {CATALOGUE}; run "
                                     f"`python variant_audit.py` first"}, 503)
                return
            self._send(200, CATALOGUE.read_bytes(), "application/json")
        elif self.path.startswith("/api/tunable/"):
            cell = self.path.rsplit("/", 1)[-1]
            try:
                m = _engine()
                self._json({"cell": cell, "knobs": {
                    k: v for k, v in m["V"].tunable(cell).items()
                    if isinstance(v, (int, float)) and not isinstance(v, bool)}})
            except Exception as exc:                       # noqa: BLE001
                self._json({"error": str(exc)}, 400)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:          # noqa: N802
        if self.path != "/api/measure":
            self._json({"error": "not found"}, 404)
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
            self._json(measure_live(req["cell"], req.get("knobs", {})))
        except Exception as exc:                           # noqa: BLE001
            self._json({"error": f"{type(exc).__name__}: {exc}"}, 400)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8801)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    if not CATALOGUE.exists():
        print(f"warning: {CATALOGUE} is missing -- run "
              f"`python variant_audit.py` first", file=sys.stderr)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"variant browser on http://{a.host}:{a.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
