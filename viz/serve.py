#!/usr/bin/env python
"""Serve the trace viewer. Stdlib only.

    python viz/serve.py            # port 8731, bound to localhost
    python viz/serve.py --port 8747

Bound to 127.0.0.1 on purpose: the port is reached through the SSH
LocalForward, so it never needs to listen on a public interface.
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
from functools import partial
from pathlib import Path

HERE = Path(__file__).resolve().parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # The bundle is rebuilt in place; never let a proxy or the browser
        # serve a stale trace set.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        print(f"  {self.address_string()} {fmt % args}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8731)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()

    if not (HERE / "data.json").exists():
        print("data.json missing — run: python viz/build_data.py")
        return 1

    socketserver.TCPServer.allow_reuse_address = True
    handler = partial(Handler, directory=str(HERE))
    with socketserver.TCPServer((args.host, args.port), handler) as httpd:
        print(f"serving {HERE} at http://{args.host}:{args.port}/  (ctrl-c to stop)")
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
