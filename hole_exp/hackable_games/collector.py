#!/usr/bin/env python
"""Persistence for human play sessions -- the part `server.py` deliberately
does not have.

The dev arena keeps sessions in memory and reaps them after an hour, which is
right for a tool you drive yourself and useless for a study: the question
"does a human find the hole through repeated play" is a question about a
CURVE, and a curve needs every play of every run written down.

SHAPE OF THE DATA. One JSON line per finished play, written twice -- once
under the game (`play_data/<game>/plays.jsonl`) and once under the player
(`play_data/players/<slug>/plays.jsonl`). The duplication is deliberate and
cheap: the per-game file is what an analysis of one cell reads, the per-player
file is what a "what did this participant do all session" read wants, and
neither has to scan the other. `run_id` stitches a player's repeated plays of
one cell back into an ordered chain.

WHAT A MOVE RECORD HOLDS, AND WHY NOT THE PROMPT. Prompts run to a couple of
thousand characters and are regenerable from `(game, seed, arm)` plus the
reply sequence, so storing them whole would multiply the corpus for nothing.
What is NOT regenerable cheaply is the structured reading of the decision the
player faced -- for battleship, the square that was fired at and what the
engine told the defender was actually there. That is what the `views/`
adapters already compute to draw the UI, so it is what gets stored, beside a
SHA of the prompt for provenance. An analysis that wants "how often did they
call miss on a true hit" reads it straight out; one that wants the full text
replays the engine.

TIMING IS DATA. Every move carries the wall-clock time and the seconds since
the previous decision. Discovery is a thing that happens at a moment, and the
cheapest evidence of the moment is a player sitting on one decision for
ninety seconds after answering the previous fifteen in four.

IDENTITY IS NORMALIZED ONCE, at the boundary, exactly as the witness-plays
collector does it: "Allie", "allie " and "allie" are one participant and one
directory, and the raw form is kept only as a display name. Getting this
wrong splits a participant's curve in half.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
DEFAULT_DIR = HERE / "play_data"

# Bumped whenever the recorded schema changes shape. An analysis that pools
# two schema versions without noticing is a silent wrong answer, so the
# version travels in every row rather than in a README.
SCHEMA = 3


def player_slug(name: str) -> str:
    """Case-insensitive, path-safe participant key."""
    s = re.sub(r"[^a-z0-9_-]+", "-", (name or "anon").strip().lower())
    return s.strip("-") or "anon"


def prompt_sha(text: str) -> str:
    return hashlib.sha256((text or "").encode()).hexdigest()[:16]


@dataclass
class MoveRecord:
    """One decision, as the player met it and as they answered it."""
    i: int
    phase: str
    reply: str
    t: float                     # wall clock, epoch seconds
    dt: float                    # seconds since the previous decision
    prompt_sha: str = ""
    prompt_len: int = 0
    # Structured reading of the decision, from views/. Empty for cells that
    # have no bespoke UI yet -- those players answered the text composer, and
    # the empty dict is the honest record of that.
    view: dict = field(default_factory=dict)
    # "ui" when a widget synthesized the token, "text" when the player typed
    # it. Aided and unaided moves must never pool silently.
    source: str = "ui"
    invalid: bool = False


@dataclass
class PlayRecord:
    """One finished play of one cell by one player."""
    play_id: str
    run_id: str
    play_index: int              # 0-based position within the run
    player: str                  # display name, as typed
    player_slug: str
    game: str
    seat: int
    arm: str
    seed: int
    bots: str
    started_at: float
    finished_at: float = 0.0
    duration_s: float = 0.0
    moves: List[MoveRecord] = field(default_factory=list)
    # Outcome. Server-side only -- none of this is ever sent to the browser
    # while the study is running.
    score: Optional[float] = None
    margin: Optional[float] = None
    gain: Optional[float] = None
    invalid: int = 0
    decisions: int = 0
    detectors: dict = field(default_factory=dict)
    hard: List[str] = field(default_factory=list)
    n_violations: int = 0
    found_hole: bool = False
    audit: dict = field(default_factory=dict)
    # Provenance. `ui_aids` names which bespoke widgets were live, because a
    # play driven by the battleship board and one typed into the composer are
    # not the same measurement and must be separable after the fact.
    ui_aids: List[str] = field(default_factory=list)
    frontend_build: str = ""
    schema: int = SCHEMA
    abandoned: bool = False


class PlayCollector:
    """Buffers live plays and appends finished ones to JSONL.

    Concurrency follows the witness-plays rule: plays are keyed by play_id and
    a player may hold ONE live play at a time. Starting a second auto-closes
    the first as abandoned rather than dropping it, so a participant who
    reloads mid-play leaves a record of having done so instead of a hole in
    the sequence.
    """

    def __init__(self, data_dir: os.PathLike | str = DEFAULT_DIR):
        self._dir = Path(data_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        (self._dir / "players").mkdir(exist_ok=True)
        self._lock = threading.Lock()
        self._live: Dict[str, PlayRecord] = {}

    # -- lifecycle -------------------------------------------------------
    def start(self, *, player: str, game: str, seat: int, arm: str, seed: int,
              bots: str, run_id: str, play_index: int,
              ui_aids: Optional[List[str]] = None,
              frontend_build: str = "") -> str:
        slug = player_slug(player)
        with self._lock:
            stale = [k for k, r in self._live.items() if r.player_slug == slug]
        for k in stale:
            self.finish(k, result=None, abandoned=True)

        rec = PlayRecord(
            play_id=uuid.uuid4().hex[:12], run_id=run_id, play_index=play_index,
            player=(player or "anon").strip() or "anon", player_slug=slug,
            game=game, seat=seat, arm=arm, seed=seed, bots=bots,
            started_at=time.time(), ui_aids=list(ui_aids or []),
            frontend_build=frontend_build or "",
        )
        with self._lock:
            self._live[rec.play_id] = rec
        return rec.play_id

    def record_move(self, play_id: str, *, phase: str, reply: str,
                    prompt: str = "", view: Optional[dict] = None,
                    source: str = "ui", invalid: bool = False) -> bool:
        with self._lock:
            rec = self._live.get(play_id)
            if rec is None:
                return False
            now = time.time()
            prev = rec.moves[-1].t if rec.moves else rec.started_at
            rec.moves.append(MoveRecord(
                i=len(rec.moves), phase=phase, reply=reply, t=now,
                dt=round(now - prev, 3), prompt_sha=prompt_sha(prompt),
                prompt_len=len(prompt or ""), view=dict(view or {}),
                source=source, invalid=invalid))
            return True

    def finish(self, play_id: str, result: Optional[dict],
               *, audit: Optional[dict] = None,
               abandoned: bool = False) -> Optional[PlayRecord]:
        with self._lock:
            rec = self._live.pop(play_id, None)
        if rec is None:
            return None
        rec.finished_at = time.time()
        rec.duration_s = round(rec.finished_at - rec.started_at, 3)
        rec.abandoned = abandoned
        if result:
            rec.score = result.get("my_score")
            rec.margin = result.get("margin")
            rec.gain = result.get("gain")
            rec.invalid = result.get("invalid", 0)
            rec.decisions = result.get("decisions", 0)
            rec.detectors = result.get("detectors", {}) or {}
            rec.hard = list(result.get("hard", []) or [])
            rec.n_violations = result.get("n_violations", 0)
            rec.found_hole = bool(result.get("found_hole"))
        if audit:
            rec.audit = dict(audit)
        self._append(rec)
        return rec

    # -- disk ------------------------------------------------------------
    def _append(self, rec: PlayRecord) -> None:
        line = json.dumps(asdict(rec), separators=(",", ":")) + "\n"
        for path in (self._dir / rec.game / "plays.jsonl",
                     self._dir / "players" / rec.player_slug / "plays.jsonl"):
            path.parent.mkdir(parents=True, exist_ok=True)
            # Append under the lock: two players finishing a play in the same
            # millisecond must not interleave halves of two JSON lines into
            # one corrupt row.
            with self._lock:
                with open(path, "a") as fh:
                    fh.write(line)
                    fh.flush()
                    os.fsync(fh.fileno())

    # -- reads (operator-side; never exposed in shared mode) -------------
    def player_plays(self, player: str) -> List[dict]:
        path = self._dir / "players" / player_slug(player) / "plays.jsonl"
        if not path.exists():
            return []
        out = []
        for line in path.read_text().splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except ValueError:
                    continue
        return out

    def summary(self) -> List[dict]:
        """One row per finished play, across everything on disk."""
        rows = []
        base = self._dir / "players"
        for pdir in sorted(base.glob("*")):
            f = pdir / "plays.jsonl"
            if not f.exists():
                continue
            for line in f.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                rows.append({k: r.get(k) for k in (
                    "play_id", "run_id", "play_index", "player_slug", "game",
                    "arm", "seed", "score", "margin", "gain", "n_violations",
                    "found_hole", "duration_s", "abandoned", "schema")})
        rows.sort(key=lambda r: (r.get("player_slug") or "",
                                 r.get("run_id") or "",
                                 r.get("play_index") or 0))
        return rows


if __name__ == "__main__":
    import sys
    c = PlayCollector(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR)
    rows = c.summary()
    for r in rows:
        print(f"  {r['player_slug']:12s} {r['game']:22s} {r['arm']:7s} "
              f"play {r['play_index']}  score {r['score']}  "
              f"viol {r['n_violations']}")
    print(f"\n{len(rows)} plays")
