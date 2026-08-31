#!/usr/bin/env python
"""The study build: humans play the cells, every play is written down, and
nothing on the page says a word about holes.

    python play_server.py --port 8801                 # local
    HG_SHARED=1 python play_server.py --host 0.0.0.0  # behind Caddy

WHY THIS IS A SECOND SERVER AND NOT A FLAG ON THE FIRST. `server.py` is the
experimenter's arena. It says "every one of these games is broken somewhere"
in its hero text, it has a "reveal where the hole is" control, and it prints
the detector table on the end screen. Every one of those is right for driving
the cells yourself and fatal for measuring whether a naive player finds the
defect. Rather than thread a mode flag through a page that was written to
give the answer away, this serves a different page from `play/` -- and it
reuses `server.Session` unchanged, so there is exactly one session driver and
no chance of the two builds drifting into two different games.

WHAT THE STUDY CLIENT IS NEVER SENT, at any point, in any payload:

    hole_type, kinds, hard, detectors, violation counts, `gain` (the honest
    counterfactual -- a non-zero gain IS the news that the hole was worked),
    `blurb`, and the family label ("generated" vs "referee", which pairs with
    the README to say all eight generated cells are broken_checker).

What it IS sent is what a player can observe by playing: the prompt, the
board, their own final score, and their own record of previous plays. That
list is the same one `referee_repeat.Memory` draws, and deliberately so --
the human arm and the model arm have to be answering the same question off
the same information or the comparison is not a comparison.

REPEATED PLAY IS THE UNIT. A participant does not play a cell once; they play
a RUN of it -- the same cell K times, fresh setup each time, carrying a record
of what they did and what it scored. `0829-repeated-play-memory.md` sweeps
exactly this for models. `p_caught` is available here too and defaults to 0,
which is the clean arm: with no audit there is nothing announced, so anything
a player learns, they learned from the score.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import catalog                                  # noqa: E402
import server                                   # noqa: E402  (session driver)
import views                                    # noqa: E402
from collector import PlayCollector, player_slug  # noqa: E402

import referee_repeat as RR                     # noqa: E402

PLAY_DIR = HERE / "play"
BUILD = "play-1"

SHARED = os.environ.get("HG_SHARED") == "1"
# The debrief is the ONLY route that will name a hole, it is off unless asked
# for, and it only ever fires after a run is complete. A participant who is
# still playing cannot reach it whatever they type.
DEBRIEF = os.environ.get("HG_DEBRIEF") == "1"

# How many plays a run of each cell is, unless the operator says otherwise.
# Roughly levelled on decisions-per-play rather than plays: battleship asks a
# seat 32 times per play, hanabi 9.
RUN_PLAYS = {"ref_battleship": 3, "ref_sidebar": 4,
             "ref_hanabi": 5, "gen_quiet_sonar": 5}
DEFAULT_PLAYS = 4

TOKEN = re.compile(r"\[\s*([a-z_]+)\s*(?::\s*([^\]]*))?\]", re.I)


# ------------------------------------------------------------------ session --
class PlaySession(server.Session):
    """A `server.Session` that also writes itself down.

    Bot seats are not recorded: they are scripted, deterministic given the
    seed, and reconstructible. Only the human's decisions go to disk.
    """

    def __init__(self, gid, seat, arm, seed, bot_mode, *,
                 collector: PlayCollector, play_id: str):
        # Set before super().__init__ -- that call starts the episode thread,
        # which can reach ask() before the constructor returns.
        self.collector = collector
        self.play_id = play_id
        self._via = "ui"
        super().__init__(gid, seat, arm, seed, bot_mode)

    def ask(self, pid, phase, prompt):
        reply = super().ask(pid, phase, prompt)
        if pid == self.seat:
            self.collector.record_move(
                self.play_id, phase=phase, reply=reply, prompt=prompt,
                view=views.build(self.gid, phase, prompt),
                source=self._via)
        return reply

    def submit(self, text: str, via: str = "ui"):
        self._via = via if via in ("ui", "text") else "ui"
        return super().submit(text)

    def human_tokens(self) -> List[str]:
        """The player's own action tokens, normalized the way
        `referee_repeat.Remembering` normalizes a model's, so the two arms'
        memories are built by the same rule."""
        out = []
        for h in self.history:
            for m in TOKEN.finditer(h.get("reply") or ""):
                name = m.group(1).lower()
                val = re.sub(r"\s+", " ", (m.group(2) or "").strip().lower())
                out.append(f"{name}: {val}" if val else name)
        return out

    # -- what the study client may see -----------------------------------
    def public_state(self) -> dict:
        st = self.state()
        pending = st.get("pending")
        out = {
            "id": st["id"], "game": self.gid, "seat": self.seat,
            "done": st["done"], "moves": st["moves"], "turn": st["turn"],
            "error": st.get("error"),
        }
        if pending:
            out["pending"] = {
                "phase": pending["phase"],
                "prompt": pending["prompt"],
                "view": views.build(self.gid, pending["phase"],
                                    pending["prompt"]),
            }
        if st["done"]:
            r = st.get("result") or {}
            # Own final score and own unparsed count. Nothing else: `margin`,
            # `gain`, the detector table and the hole note all stay server-
            # side while the study is running.
            out["score"] = r.get("my_score")
            out["decisions"] = r.get("decisions", 0)
            out["invalid"] = r.get("invalid", 0)
        return out


# ---------------------------------------------------------------------- run --
class Run:
    """One participant's chain of plays on one cell."""

    def __init__(self, player: str, gid: str, arm: str, plays: int,
                 bots: str, p_caught: float, collector: PlayCollector,
                 ui_aids: List[str]):
        self.id = uuid.uuid4().hex[:12]
        self.player = (player or "anon").strip() or "anon"
        self.slug = player_slug(self.player)
        self.gid, self.arm, self.plays, self.bots = gid, arm, plays, bots
        self.p_caught = p_caught
        self.collector = collector
        self.ui_aids = ui_aids
        self.index = -1
        self.session: Optional[PlaySession] = None
        self.memory = RR.Memory()
        # Seeds are drawn from the run id, so a run is replayable end to end
        # from one string -- a play a participant reports as strange can be
        # put back on the screen exactly as they met it.
        self._rng = random.Random(f"run-{self.id}")
        self._arng = random.Random(f"audit-{self.id}")
        self.scores: List[float] = []
        self.touched = time.time()
        self.finished = False
        # Play ids already settled. A client that posts a move after the play
        # ended -- a double-click, a retry, a reload landing on a done
        # session -- reaches _settle a second time, and without this the play
        # would be appended to the memory chain and the score list twice. The
        # collector is already idempotent (a finished play_id is gone from
        # its live table), so the duplicate would show up in the record the
        # PLAYER sees while never appearing on disk: two different accounts
        # of the same run, which is the worst version of this bug.
        self._closed: set = set()

    @property
    def remaining(self) -> int:
        return max(0, self.plays - (self.index + 1))

    def start_next(self) -> Optional[PlaySession]:
        self.touched = time.time()
        if self.session is not None and not self.session.done.is_set():
            # A client can ask for the next play mid-play. The abandoned play
            # still gets written -- a participant who bailed out of round 4
            # is data, and dropping it would leave the collector holding a
            # live record forever.
            self.collector.finish(self.session.play_id, None, abandoned=True)
            self.session.kill()
        if self.remaining <= 0:
            self.finished = True
            return None
        self.index += 1
        seed = self._rng.randint(1, 10 ** 6)
        play_id = self.collector.start(
            player=self.player, game=self.gid, seat=0, arm=self.arm,
            seed=seed, bots=self.bots, run_id=self.id, play_index=self.index,
            ui_aids=self.ui_aids, frontend_build=BUILD)
        self.session = PlaySession(self.gid, 0, self.arm, seed, self.bots,
                                   collector=self.collector, play_id=play_id)
        return self.session

    def close_play(self) -> Optional[dict]:
        """Settle a finished play: audit it, write it, fold it into memory."""
        s = self.session
        if s is None or not s.done.is_set() or s.play_id in self._closed:
            return None
        self._closed.add(s.play_id)
        result = s.result()
        ep = s.episode
        game = catalog.GAMES[self.gid]["game"]

        caught = fine = clawback = 0.0
        if ep is not None and self.p_caught > 0 and self.arm == "hole":
            try:
                caught, fine, clawback = RR.audit(
                    ep, game, s.seat, self.p_caught, self._arng)
            except Exception:
                caught, fine, clawback = 0, 0.0, 0.0

        score = float(result.get("my_score") or 0.0)
        rec = RR.PlayRecord(
            index=self.index + 1, actions=s.human_tokens(), score=score,
            caught=int(caught), fine=float(fine), clawback=float(clawback),
            audited=self.p_caught > 0)
        self.memory.records.append(rec)
        self.scores.append(score)

        self.collector.finish(
            s.play_id, result,
            audit={"p_caught": self.p_caught, "caught": int(caught),
                   "fine": float(fine), "clawback": float(clawback)})
        # The interstitial a human sees between plays is the same text the
        # model arm gets prepended to its next prompt. Same content, same
        # rule about what may be in it: own tokens, own score, and an audit
        # result when there was an audit. No detector name, ever.
        return {"score": score, "adjusted": rec.adjusted,
                "caught": int(caught), "fine": float(fine),
                "audited": rec.audited}

    def summary(self) -> dict:
        return {"run_id": self.id, "game": self.gid, "player": self.player,
                "plays": self.plays, "played": len(self.scores),
                "remaining": self.remaining, "finished": self.finished,
                "scores": [round(v, 2) for v in self.scores],
                "memory": self.memory.render().strip()}

    def kill(self):
        if self.session is not None and not self.session.done.is_set():
            self.collector.finish(self.session.play_id, None, abandoned=True)
            self.session.kill()
        self.session = None


RUNS: Dict[str, Run] = {}
BY_PLAYER: Dict[str, str] = {}
RLOCK = threading.Lock()
COLLECTOR = PlayCollector(os.environ.get("HG_DATA_DIR") or
                          (HERE / "play_data"))
RUN_TTL = 6 * 3600.0

# A run holds a thread parked on a queue for as long as the player is in it.
# One live run per player slug bounds a *named* participant, and bounds
# nothing at all on a public URL, because names are free text: N requests with
# N names is N threads. So there is a hard ceiling, and reaching it evicts the
# least-recently-touched run rather than refusing the new player -- an idle
# session someone walked away from should not be able to lock a seat for six
# hours. Plays already finished inside an evicted run are on disk; only the
# play in progress is lost, and it is written as `abandoned`.
MAX_RUNS = int(os.environ.get("HG_MAX_RUNS") or 200)


def _retire(runs: List[Run]) -> None:
    """Kill outside RLOCK: kill() writes to disk, and holding the lock across
    an fsync would stall every other player's move."""
    for r in runs:
        try:
            r.kill()
        except Exception:
            pass


def reap_runs():
    now = time.time()
    with RLOCK:
        stale = [k for k, r in RUNS.items() if now - r.touched > RUN_TTL]
        dead = [RUNS.pop(k) for k in stale]
        for r in dead:
            BY_PLAYER.pop(r.slug, None)
    _retire(dead)


def make_room():
    """Evict least-recently-touched runs until there is a free seat."""
    with RLOCK:
        evicted = []
        while len(RUNS) >= MAX_RUNS:
            oldest = min(RUNS.values(), key=lambda r: r.touched)
            RUNS.pop(oldest.id, None)
            BY_PLAYER.pop(oldest.slug, None)
            evicted.append(oldest)
    _retire(evicted)
    return len(evicted)


def public_catalogue() -> List[dict]:
    """The catalogue, minus the family label.

    `catalog.public_list()` already strips hole_type, kinds and the blurb.
    `family` survives it and has to go here: the README says in plain text
    that all eight generated cells are broken_checker, so a card tagged
    "model-written" is a partial answer key for anyone who has read it.
    """
    out = []
    for c in catalog.public_list():
        out.append({"id": c["id"], "title": c["title"],
                    "teaser": c["teaser"], "n_players": c["n_players"],
                    "rounds": c["rounds"],
                    "board": c["id"] in views.ADAPTERS,
                    "plays": RUN_PLAYS.get(c["id"], DEFAULT_PLAYS)})
    out.sort(key=lambda c: (not c["board"], c["title"]))
    return out


# ------------------------------------------------------------------ handler --
class Handler(BaseHTTPRequestHandler):
    server_version = "Plays/1.0"

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj), "application/json")

    def _static(self, rel: str, ctype: str):
        p = (PLAY_DIR / rel).resolve()
        if not str(p).startswith(str(PLAY_DIR.resolve())) or not p.exists():
            return self._send(404, b"not found", "text/plain")
        return self._send(200, p.read_bytes(), ctype)

    # -- GET -------------------------------------------------------------
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)

        if u.path in ("/", "/index.html"):
            return self._static("index.html", "text/html; charset=utf-8")
        if u.path == "/app.js":
            return self._static("app.js", "application/javascript")
        if u.path == "/style.css":
            return self._static("style.css", "text/css")
        if u.path.startswith("/ui/") and u.path.endswith(".js"):
            return self._static(u.path[1:], "application/javascript")

        if u.path == "/api/games":
            return self._json({"games": public_catalogue()})

        if u.path == "/api/state":
            r = RUNS.get((q.get("run") or [""])[0])
            if not r or r.session is None:
                return self._json({"error": "no such run"}, 404)
            r.touched = time.time()
            return self._json(self._play_payload(r))

        if u.path == "/api/run":
            r = RUNS.get((q.get("run") or [""])[0])
            if not r:
                return self._json({"error": "no such run"}, 404)
            return self._json(r.summary())

        if u.path == "/api/debrief":
            # Post-study only, opt-in at the process level, and only for a run
            # that is actually over.
            if not DEBRIEF:
                return self._json({"error": "not enabled"}, 404)
            r = RUNS.get((q.get("run") or [""])[0])
            if not r:
                return self._json({"error": "no such run"}, 404)
            if not r.finished:
                return self._json({"error": "run not finished"}, 409)
            c = catalog.GAMES[r.gid]
            note = server.HOLE_NOTES.get(r.gid, {})
            return self._json({
                "game": r.gid, "title": c["title"],
                "hole_type": c["hole_type"], "how": note.get("how", ""),
                "kinds": list(c["kinds"]),
                "detectors": self._run_detectors(r),
            })

        if u.path == "/api/summary":
            if SHARED:
                return self._json({"error": "disabled on shared deployments"},
                                  403)
            return self._json({"rows": COLLECTOR.summary()})

        if u.path == "/healthz":
            return self._send(200, b"ok", "text/plain")

        return self._send(404, b"not found", "text/plain")

    @staticmethod
    def _run_detectors(r: Run) -> List[dict]:
        rows = []
        for rec in COLLECTOR.player_plays(r.player):
            if rec.get("run_id") != r.id:
                continue
            rows.append({"play_index": rec.get("play_index"),
                         "n_violations": rec.get("n_violations"),
                         "detectors": rec.get("detectors"),
                         "score": rec.get("score")})
        rows.sort(key=lambda x: x.get("play_index") or 0)
        return rows

    def _play_payload(self, r: Run) -> dict:
        s = r.session
        st = s.public_state() if s else {}
        st["run"] = {"run_id": r.id, "game": r.gid,
                     "play_index": r.index, "plays": r.plays,
                     "remaining": r.remaining,
                     "memory": r.memory.render().strip()}
        return st

    # -- POST ------------------------------------------------------------
    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        if n > 64_000:
            return self._json({"error": "payload too large"}, 413)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json({"error": "bad json"}, 400)

        if u.path == "/api/run/start":
            return self._start(body)
        if u.path == "/api/move":
            return self._move(body)
        if u.path == "/api/run/next":
            return self._next(body)
        if u.path == "/api/run/quit":
            r = RUNS.pop(body.get("run") or "", None)
            if r:
                with RLOCK:
                    BY_PLAYER.pop(r.slug, None)
                r.kill()
            return self._json({"ok": True})
        return self._json({"error": "not found"}, 404)

    def _start(self, body):
        player = (body.get("player") or "").strip()
        if not player:
            return self._json({"error": "a name is required"}, 400)
        if len(player) > 40:
            return self._json({"error": "name too long"}, 400)
        gid = body.get("game")
        if gid not in catalog.GAMES:
            return self._json({"error": "unknown game"}, 400)
        arm = body.get("arm", "hole")
        if arm not in ("hole", "nohole"):
            return self._json({"error": "bad arm"}, 400)
        plays = int(body.get("plays") or RUN_PLAYS.get(gid, DEFAULT_PLAYS))
        plays = max(1, min(plays, 12))
        p_caught = float(body.get("p_caught") or
                         os.environ.get("HG_P_CAUGHT") or 0.0)
        p_caught = min(max(p_caught, 0.0), 1.0)

        reap_runs()
        make_room()
        slug = player_slug(player)
        # One live run per participant, the witness-plays rule. A reload does
        # not fork a second chain that would land in the data as two shorter
        # runs by the same person on the same cell.
        with RLOCK:
            old = BY_PLAYER.get(slug)
        if old:
            prev = RUNS.pop(old, None)
            if prev:
                prev.kill()

        r = Run(player, gid, arm, plays, body.get("bots", "honest"), p_caught,
                COLLECTOR, ui_aids=([f"board:{gid}"] if gid in views.ADAPTERS
                                    else []))
        with RLOCK:
            RUNS[r.id] = r
            BY_PLAYER[slug] = r.id
        if r.start_next() is None:
            return self._json({"error": "could not start"}, 500)
        return self._json(self._play_payload(r))

    def _move(self, body):
        r = RUNS.get(body.get("run") or "")
        if not r or r.session is None:
            return self._json({"error": "no such run"}, 404)
        s = r.session
        r.touched = time.time()
        if s.done.is_set():
            return self._json(self._settle(r))
        if not s.pending:
            return self._json({"error": "not your turn"}, 409)
        text = str(body.get("text", ""))
        if len(text) > 2000:
            return self._json({"error": "move too long"}, 400)
        t0 = s.turn
        s.submit(text, body.get("via", "ui"))
        for _ in range(1500):
            if s.turn != t0 or s.done.is_set():
                break
            time.sleep(0.01)
        if s.done.is_set():
            return self._json(self._settle(r))
        return self._json(self._play_payload(r))

    def _settle(self, r: Run) -> dict:
        """A play just ended: write it, fold it into memory, hand back what
        the player may see."""
        closed = r.close_play()
        payload = self._play_payload(r)
        if closed:
            payload["play_result"] = closed
        payload["run"]["memory"] = r.memory.render().strip()
        payload["run"]["complete"] = r.remaining <= 0
        if r.remaining <= 0:
            r.finished = True
            payload["run"]["summary"] = r.summary()
            payload["run"]["debrief"] = DEBRIEF
        return payload

    def _next(self, body):
        r = RUNS.get(body.get("run") or "")
        if not r:
            return self._json({"error": "no such run"}, 404)
        r.close_play()          # no-op if this play was already settled
        if r.start_next() is None:
            r.finished = True
            return self._json({"complete": True, "run": r.summary()})
        return self._json(self._play_payload(r))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8801)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    boards = ", ".join(sorted(views.ADAPTERS))
    print(f"Plays -- {len(catalog.GAMES)} cells, boards for: {boards}")
    print(f"  data   {COLLECTOR._dir}")
    print(f"  shared {'ON (dev endpoints disabled)' if SHARED else 'off'}"
          f"  debrief {'ON' if DEBRIEF else 'off'}"
          f"  max runs {MAX_RUNS}")
    print(f"  http://{a.host}:{a.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
