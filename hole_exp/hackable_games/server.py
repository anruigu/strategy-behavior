#!/usr/bin/env python
"""Hackable Games -- a local web arena where a human plays the hole cells.

    python server.py --port 8799
    open http://localhost:8799

Every cell is a game with a deliberate defect in its referee, its opponents or
its message channel. You are told the rules and nothing else. Whether you find
the defect is the game.

HOW A SESSION WORKS. The engines are synchronous: `game.run(ask, seed, arm)`
drives the whole episode and calls `ask(pid, phase, prompt)` whenever a seat has
to decide. So each session runs the episode on its own daemon thread, and the
human seat's `ask` parks on a queue until the browser posts a move. Bot seats
answer inline. Nothing about the engines had to change to support a human.

WHAT THE BROWSER IS NOT TOLD. Until an episode ends, the client never receives
the hole type, the detector names, or which seats are scripted. A card reading
"broken_checker" would turn the game into reading a label. On the end screen it
gets everything: what the detectors saw, the score, the honest counterfactual,
and a plain-language account of the hole.
"""
from __future__ import annotations

import argparse
import json
import queue
import random
import sys
import threading
import time
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import catalog                      # noqa: E402
import bots as GENBOTS              # noqa: E402

try:
    from test_referee_games import Scripted as RefScripted
except Exception:                    # pragma: no cover
    RefScripted = None

STATIC = HERE / "static"
SESSION_TTL = 3600.0
KILL = object()


# ---------------------------------------------------------------- hole notes --
def _hole_notes() -> dict:
    """Plain-language account of each hole, shown only after the episode ends."""
    notes = {}
    spec_path = HERE.parent / "holescreen" / "specs.json"
    if spec_path.exists():
        gid = {"seven_seal_certificates": "gen_seven_seal",
               "quiet_sonar": "gen_quiet_sonar", "icebound_manifest": "gen_icebound",
               "sovereign_vaults": "gen_sovereign_vaults",
               "antiquities_exchange": "gen_antiquities",
               "frontline_depot": "gen_frontline_depot",
               "harbor_customs": "gen_harbor_customs", "vault_duel": "gen_vault_duel"}
        for s in json.loads(spec_path.read_text()):
            key = s["id"].split(":")[1]
            if key in gid:
                notes[gid[key]] = {
                    "how": s["hole"].get("how") or "",
                    "exploit": s["hole"].get("exploit_move") or "",
                    "honest": s["hole"].get("honest_move") or "",
                }
    for name, c in catalog.GAMES.items():
        notes.setdefault(name, {"how": (c.get("blurb") or "").strip(),
                                "exploit": "", "honest": ""})
    return notes


HOLE_NOTES = _hole_notes()


# ------------------------------------------------------------------ session --
class Session:
    def __init__(self, gid: str, seat: int, arm: str, seed: int, bot_mode: str):
        c = catalog.GAMES[gid]
        self.gid, self.game = gid, c["game"]
        self.seat, self.arm, self.seed, self.bot_mode = seat, arm, seed, bot_mode
        self.id = uuid.uuid4().hex[:12]
        self.inbox: "queue.Queue" = queue.Queue(maxsize=1)
        self.pending = None
        # Monotonic decision counter. `pending` alone is NOT a safe signal that a
        # new decision has arrived: it is cleared inside ask() only AFTER
        # inbox.get() returns, so a /api/move that polled `pending` could see the
        # STALE prompt still set, hand it back as if it were the next turn, and
        # the client would answer the same decision twice. That shifted every
        # later answer by one round -- caught by the end-to-end test, which saw 8
        # moves consumed by a 7-round game and reports lagging their draws.
        self.turn = 0
        self.history = []
        self.lock = threading.Lock()
        self.done = threading.Event()
        self.episode = None
        self.error = None
        self.touched = time.time()
        self.used_hint = False
        self.bot = self._make_bot(c["family"], bot_mode, seed)
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    @staticmethod
    def _make_bot(family: str, mode: str, seed: int):
        if family == "generated":
            return GENBOTS.Scripted(mode, seed)
        if RefScripted is None:
            raise RuntimeError("referee scripted policies unavailable")
        return RefScripted(mode)

    def ask(self, pid: int, phase: str, prompt: str) -> str:
        if pid != self.seat:
            try:
                return self.bot(pid, phase, prompt)
            except Exception:
                return "[noop: 0]"
        with self.lock:
            self.pending = {"pid": pid, "phase": phase, "prompt": prompt}
            self.turn += 1
        reply = self.inbox.get()
        if reply is KILL:
            raise SystemExit
        with self.lock:
            self.history.append({"phase": phase, "prompt": prompt, "reply": reply})
            self.pending = None
        return reply

    def _run(self):
        try:
            self.episode = self.game.run(self.ask, self.seed, self.arm)
        except SystemExit:
            pass
        except Exception:
            self.error = traceback.format_exc(limit=6)
        finally:
            self.done.set()

    def submit(self, text: str):
        try:
            self.inbox.put_nowait(text)
            return True
        except queue.Full:
            return False

    def kill(self):
        try:
            self.inbox.put_nowait(KILL)
        except queue.Full:
            pass

    # -- what the browser sees -------------------------------------------
    def state(self) -> dict:
        self.touched = time.time()
        with self.lock:
            pending = dict(self.pending) if self.pending else None
            hist = list(self.history)
        st = {"id": self.id, "game": self.gid, "seat": self.seat,
              "arm": self.arm, "done": self.done.is_set(),
              "pending": pending, "moves": len(hist), "turn": self.turn,
              "used_hint": self.used_hint, "error": self.error}
        if self.done.is_set():
            st["result"] = self.result()
        return st

    def result(self) -> dict:
        ep = self.episode
        if ep is None:
            return {"error": self.error or "episode did not finish"}
        c = catalog.GAMES[self.gid]
        me = self.seat
        hard = list(c["hard"])
        found = {k: {"violations": ep.violations[me].get(k, 0),
                     "opportunities": ep.opportunities[me].get(k, 0)}
                 for k in c["kinds"]}
        took = sum(ep.violations[me].get(k, 0) for k in hard)
        others = [ep.scores[q] for q in ep.scores if q != me]
        return {
            "scores": {str(k): round(v, 2) for k, v in ep.scores.items()},
            "my_score": round(ep.scores.get(me, 0.0), 2),
            "margin": round(ep.scores.get(me, 0.0) -
                            (sum(others) / len(others) if others else 0.0), 2),
            "gain": (round(ep.gain[me], 2) if ep.gain.get(me) is not None else None),
            "invalid": ep.invalid.get(me, 0),
            "decisions": ep.decisions.get(me, 0),
            "detectors": found, "hard": hard, "found_hole": took > 0,
            "used_hint": self.used_hint,
            "n_violations": took,
            "hole_type": c["hole_type"], "note": HOLE_NOTES.get(self.gid, {}),
            "transcript": ep.transcript[-40:],
        }


SESSIONS: dict = {}
SLOCK = threading.Lock()


def reap():
    now = time.time()
    with SLOCK:
        for k, s in list(SESSIONS.items()):
            if now - s.touched > SESSION_TTL:
                s.kill()
                SESSIONS.pop(k, None)


# ------------------------------------------------------------------ handler --
class Handler(BaseHTTPRequestHandler):
    server_version = "HackableGames/1.0"

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj))

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path in ("/", "/index.html"):
            return self._send(200, (STATIC / "index.html").read_bytes(), "text/html")
        if u.path == "/app.js":
            return self._send(200, (STATIC / "app.js").read_bytes(),
                              "application/javascript")
        if u.path == "/style.css":
            return self._send(200, (STATIC / "style.css").read_bytes(), "text/css")
        if u.path == "/api/games":
            return self._json({"games": catalog.public_list()})
        if u.path == "/api/hint":
            # Opt-in spoiler, served ONLY on an explicit click and never bundled
            # into /api/state -- so the hole is not sitting in a payload the
            # player can read without choosing to. Taking it is recorded and the
            # end screen says so.
            sid = (q.get("id") or [""])[0]
            s = SESSIONS.get(sid)
            if not s:
                return self._json({"error": "no such session"}, 404)
            s.used_hint = True
            c = catalog.GAMES[s.gid]
            n = HOLE_NOTES.get(s.gid, {})
            return self._json({"hole_type": c["hole_type"],
                               "how": n.get("how") or c.get("blurb") or "",
                               "kinds": list(c["kinds"])})
        if u.path == "/api/state":
            sid = (q.get("id") or [""])[0]
            s = SESSIONS.get(sid)
            if not s:
                return self._json({"error": "no such session"}, 404)
            return self._json(s.state())
        return self._send(404, b"not found", "text/plain")

    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json({"error": "bad json"}, 400)

        if u.path == "/api/new":
            gid = body.get("game")
            if gid not in catalog.GAMES:
                return self._json({"error": "unknown game"}, 400)
            c = catalog.GAMES[gid]
            seat = int(body.get("seat", 0))
            if not 0 <= seat < c["n_players"]:
                return self._json({"error": "bad seat"}, 400)
            arm = body.get("arm", "hole")
            if arm not in ("hole", "nohole"):
                return self._json({"error": "bad arm"}, 400)
            seed = int(body.get("seed") or random.randint(1, 10 ** 6))
            mode = body.get("bots", "honest")
            reap()
            try:
                s = Session(gid, seat, arm, seed, mode)
            except Exception as e:
                return self._json({"error": f"{type(e).__name__}: {e}"}, 500)
            with SLOCK:
                SESSIONS[s.id] = s
            for _ in range(200):            # let the thread reach the first ask
                if s.turn >= 1 or s.done.is_set():
                    break
                time.sleep(0.01)
            return self._json(s.state())

        if u.path == "/api/move":
            s = SESSIONS.get(body.get("id"))
            if not s:
                return self._json({"error": "no such session"}, 404)
            if s.done.is_set():
                return self._json(s.state())
            if not s.pending:
                return self._json({"error": "not your turn"}, 409)
            t0 = s.turn
            s.submit(str(body.get("text", "")))
            # wait for a genuinely NEW decision, not the stale one still set
            for _ in range(1000):
                if s.turn != t0 or s.done.is_set():
                    break
                time.sleep(0.01)
            return self._json(s.state())

        if u.path == "/api/quit":
            s = SESSIONS.pop(body.get("id"), None)
            if s:
                s.kill()
            return self._json({"ok": True})

        return self._json({"error": "not found"}, 404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    n = len(catalog.GAMES)
    print(f"Hackable Games -- {n} cells "
          f"({sum(c['family']=='generated' for c in catalog.GAMES.values())} generated, "
          f"{sum(c['family']=='referee' for c in catalog.GAMES.values())} referee)")
    print(f"  http://{a.host}:{a.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
