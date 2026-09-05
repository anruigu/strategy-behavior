#!/usr/bin/env python
"""Gates for the study build. Offline, no cost.

    python test_views.py

The gates below cover the complete bracket-free study surface, and NO LEAK is
the one that matters most:

  PARSES     every decision the human seat is asked for in a full episode of
             each boarded cell produces a view. A `None` here means the player
             would have been dropped to the text composer mid-game.

  PLAYABLE   the episode can be driven END TO END using only what is in the
             views. This is what proves a board is sufficient rather than
             decorative: if a legal move exists that the view does not carry,
             this gate cannot finish the game without falling back.

  NO LEAK    live-run payloads must not carry hole_type, kinds, hard,
             detectors, blurb, gain, margin or the family label. The
             catalogue may name hole KINDS via variants (operator debugging);
             that is checked separately. Checked against real payloads from
             a real run, not against the code. This is the gate that stops a
             refactor from quietly turning the study into a reading
             comprehension test.

  COPY       no player-visible text in play/ names a defect. Comments are
             stripped first -- they say "hole" constantly, on purpose.

  JS         every client script parses. There is no build step here, so a
             stray brace would otherwise ship and blank the board on load.

  WIRING     every id the client reaches for exists in the page, and every
             view kind an adapter can emit has a renderer.

  RECORDS    a finished play lands on disk, under both the game and the
             player, with its moves and its outcome.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import catalog          # noqa: E402
import views            # noqa: E402
from collector import PlayCollector   # noqa: E402

OFF_ROSTER_ADAPTERS = {"ref_battleship"}
BASE_GAMES = tuple(sorted(set(views.ADAPTERS) - OFF_ROSTER_ADAPTERS))
DRIVEN_GAMES = BASE_GAMES + tuple(sorted(OFF_ROSTER_ADAPTERS & set(views.ADAPTERS)))

# Anything on this list appearing in a live payload is a leak. `family` is
# here because the README pairs it with "all eight generated cells are
# broken_checker"; `gain` because a non-zero gain is the news that the hole
# paid; `margin` because it is only ever computed from the other seats'
# scores, which a player is not told.
FORBIDDEN_KEYS = ("hole_type", "kinds", "hard", "detectors", "blurb",
                  "gain", "margin", "found_hole", "n_violations", "family",
                  "used_hint", "note", "author")
FORBIDDEN_TEXT = ("broken_checker", "self_report", "local_ledger",
                  "private_channel", "metadata_channel", "unvalidated_trade",
                  "convention_channel", "false_miss", "sunk_denial",
                  "hole_type", "detector")
CATALOGUE_FORBIDDEN_ROW_KEYS = ("family", "author", "blurb", "hole_type")
CATALOGUE_ALLOWED_TEXT = ("broken_checker", "nerfed_opponent",
                          "broken verifier", "nerfed opponent")


# ---------------------------------------------------------------- players --
def _from_view(v: dict, phase: str, prompt: str) -> str:
    """Choose a legal move using ONLY the view. Deliberately dumb: it takes
    the first option every time. The point is reachability, not skill."""
    k = v["kind"]
    if k == "battleship_fire":
        spent = set(v["spent"])
        for r in range(v["grid"]):
            for c in range(1, v["grid"] + 1):
                name = v["rows"][r] + str(c)
                if name not in spent:
                    return f"[fire: {name}]"
        raise AssertionError("fire view offered no unspent square")
    if k == "battleship_call":
        return v["calls"][0]["token"]
    if k == "sidebar_msg":
        return "[msg: hello]"
    if k == "sidebar_bet":
        return v["actions"][1]["token"]          # call
    if k == "hanabi_turn":
        return f"[discard: {v['hand'][0]['slot']}]"
    if k == "sonar_hide":
        return "[hide: 1]"
    if k == "sonar_fire":
        return "[fire: 1]"
    if k == "sonar_claim":
        return v["claims"][0]["token"]

    # Compound forms are deliberately assembled here rather than taking a
    # convenient engine-side policy.  This proves the view carries every
    # value needed by a renderer to submit one complete, valid reply.
    if k == "estate_settle":
        square = v["square"]
        due = square.get("due") or 0
        pay = (f"[pay: {due} to P{square['owner']}]" if due
               else v["tokens"]["pay_none"])
        balance = v["balance"] + v.get("received", 0)
        if v.get("passed_start"):
            balance += v.get("salary") or 0
        balance -= due
        return f"{pay}\n[buy: no]\n[balance: {balance:g}]"
    if k == "exchange_offer":
        return v["none_token"]
    if k == "exchange_build":
        return v["actions"][-1]["token"]         # none
    if k == "exchange_accept":
        return v["none_token"]
    if k == "auction_bid":
        return f"{v['pass_token']}\n[budget: 0]"
    if k == "invoice_job":
        return (f"[effort: {v['effort_lo']}]\n{v['reports'][-1]['token']}\n"
                f"[hours: {v['hours_lo'] if v['hours_lo'] is not None else 0}]")
    if k in ("harbor_route", "kuhn_act"):
        return v["routes" if k == "harbor_route" else "actions"][0]["token"]
    if k == "negotiation_trade":
        return v["hold_token"]
    if k == "liarsdice_bid":
        if v["current"]:
            return v["call_token"]
        return v["token"].format(qty=1, face=1)
    if k == "letter_word":
        return v["none_token"]
    if k == "ipd3_table":
        return v["token"].format(rook=v["options"][0], dove=v["options"][0])

    # The remaining views expose one template and the corresponding domain.
    numeric = {
        "sevenseal_report", "vaults_declare", "vaults_deposit",
        "depot_strike", "depot_guard", "harbor_declare",
        "pubgoods_envelope", "pubgoods_receipt", "liarsdice_count",
        "blind_sealed", "letter_bid",
    }
    if k in numeric:
        return v["token"].format(n=v["lo"])
    if k == "commons_catch":
        return v["token"].format(n=0)
    if k in ("icebound_pledge", "icebound_act"):
        return v["token"].format(m=v["missions"][0])
    if k in ("duel_move", "winasmuch_talk", "winasmuch_pick"):
        return v["token"].format(opt=v["options"][0])
    if k == "kuhn_show":
        return v["token"].format(card=v["cards"][0])
    if k in ("ipd3_line", "blind_note"):
        return v["token"].format(text="hello")
    raise AssertionError(f"no driver for view kind {k}")


def drive(gid: str, seed: int = 11, arm: str = "hole"):
    """Play one episode of `gid` as seat 0, entirely off the views."""
    import bots as GENBOTS
    import bots_textarena as TABOTS
    from test_referee_games import Scripted as RefScripted

    c = catalog.GAMES[gid]
    if c["family"] == "generated":
        bot = GENBOTS.Scripted("honest", seed)
    elif c["family"] == "textarena":
        bot = TABOTS.Scripted("honest", seed)
    else:
        # Exchange only emits its accept view when another seat makes an
        # offer.  The ordinary honest fixture always stands down, so use its
        # offer-making policy for the non-human seats in this one game.
        bot = RefScripted("exploit" if gid == "ref_exchange" else "honest")
    seen, misses = [], []

    def ask(pid, phase, prompt):
        if pid != 0:
            return bot(pid, phase, prompt)
        v = views.build(gid, phase, prompt)
        if v is None:
            misses.append((phase, prompt[:160]))
            # Keep the episode moving so the gate reports EVERY miss rather
            # than only the first.
            return "[noop: 0]"
        seen.append((phase, v))
        return _from_view(v, phase, prompt)

    ep = c["game"].run(ask, seed, arm)
    return ep, seen, misses


# ------------------------------------------------------------------ gates --
def gate_parses_and_playable() -> int:
    bad = 0
    emitted = set()
    for gid in DRIVEN_GAMES:
        ep, seen, misses = drive(gid)
        phases = sorted({p for p, _ in seen})
        emitted |= {v["kind"] for _, v in seen}
        if misses:
            bad += 1
            print(f"  FAIL {gid}: {len(misses)} decision(s) produced no view")
            for ph, head in misses[:3]:
                print(f"       phase={ph}  {head!r}")
        elif not seen:
            bad += 1
            print(f"  FAIL {gid}: the human seat was never asked anything")
        else:
            # PLAYABLE: the engine finished and never had to substitute a move
            # for an unparseable one from seat 0.
            invalid = ep.invalid.get(0, 0)
            flag = "" if invalid == 0 else f"  (!! {invalid} unparsed)"
            if invalid:
                bad += 1
            print(f"  {'ok  ' if not invalid else 'FAIL'} {gid}: "
                  f"{len(seen)} decisions, phases {phases}{flag}")
    missing_kinds = sorted(set(views.KINDS) - emitted)
    extra_kinds = sorted(emitted - set(views.KINDS))
    if missing_kinds or extra_kinds:
        print(f"  FAIL kinds: unobserved={missing_kinds}, undeclared={extra_kinds}")
        bad += 1
    elif not bad:
        print(f"  ok   coverage: {len(BASE_GAMES)} base games, "
              f"{len(emitted)} emitted kinds")
    return bad


def gate_adapter_roster() -> int:
    """The adapter registry covers the independent 23-game base roster.

    Battleship is intentionally retained as an extra adapter after being
    deduplicated out of that roster, so it is checked but not counted.
    """
    try:
        import tomllib
    except ImportError:  # pragma: no cover - only Python < 3.11
        import tomli as tomllib

    roster_path = HERE.parent / "configs" / "base_roster.toml"
    with roster_path.open("rb") as fh:
        base = tomllib.load(fh)["base"]
    roster = set(base["atlas"]) | set(base["textarena"])
    adapters = set(views.ADAPTERS)
    missing = sorted(roster - adapters)
    unexpected = sorted(adapters - roster - OFF_ROSTER_ADAPTERS)
    bad = 0
    if len(roster) != base["count"]:
        print(f"  FAIL roster: config says {base['count']}, lists {len(roster)}")
        bad += 1
    if missing or unexpected:
        print(f"  FAIL roster: missing adapters={missing}, unexpected={unexpected}")
        bad += 1
    if OFF_ROSTER_ADAPTERS - adapters:
        print(f"  FAIL roster: retained adapters absent: "
              f"{sorted(OFF_ROSTER_ADAPTERS - adapters)}")
        bad += 1
    if not bad:
        print(f"  ok   roster: all {len(roster)} base games covered; "
              f"{', '.join(sorted(OFF_ROSTER_ADAPTERS))} retained off-roster")
    return bad


def gate_no_leak() -> int:
    """Drive a real run through the real handler methods and inspect every
    payload the client would have received."""
    import play_server as P

    tmp = Path(tempfile.mkdtemp(prefix="plays-leak-"))
    P.COLLECTOR = PlayCollector(tmp)
    live_payloads = []

    run = P.Run("gate", "gen_quiet_sonar", "hole", 2, "honest", 0.0,
                P.COLLECTOR, ui_aids=["board:gen_quiet_sonar"])
    P.RUNS[run.id] = run
    run.start_next()

    h = P.Handler.__new__(P.Handler)          # methods only, no socket
    catalogue = P.public_catalogue()

    guard = 0
    while guard < 400:
        guard += 1
        s = run.session
        if s is None:
            break
        pay = h._play_payload(run)
        live_payloads.append(pay)
        if s.done.is_set():
            live_payloads.append(h._settle(run))
            if run.remaining <= 0:
                break
            run.start_next()
            continue
        pend = pay.get("pending")
        if not pend:
            import time
            time.sleep(0.02)
            continue
        v = pend.get("view")
        move = (_from_view(v, pend["phase"], pend["prompt"]) if v
                else "[claim: hit]")
        t0 = s.turn
        s.submit(move, "ui")
        import time
        for _ in range(500):
            if s.turn != t0 or s.done.is_set():
                break
            time.sleep(0.01)

    P.RUNS.pop(run.id, None)

    bad = 0
    live_blob = json.dumps(live_payloads)
    for key in FORBIDDEN_KEYS:
        if f'"{key}"' in live_blob:
            print(f"  FAIL leak: live payloads carry key {key!r}")
            bad += 1
    live_low = live_blob.lower()
    for word in FORBIDDEN_TEXT:
        if word in live_low:
            print(f"  FAIL leak: live payloads carry the string {word!r}")
            bad += 1

    if len(catalogue) != 24:
        print(f"  FAIL leak: catalogue has {len(catalogue)} rows, expected 24")
        bad += 1
    hf_ids = [r["id"] for r in catalogue if r["id"].startswith("hf_")]
    if hf_ids:
        print(f"  FAIL leak: catalogue row id(s) start with hf_: {hf_ids}")
        bad += 1
    debug_ok = any(
        v.get("cell", "").startswith("hf_")
        and v.get("label") == "nerfed opponent"
        for row in catalogue
        for v in row.get("variants", [])
    )
    if not debug_ok:
        print("  FAIL leak: no catalogue variant with hf_ cell and "
              "'nerfed opponent' label")
        bad += 1
    for row in catalogue:
        for key in CATALOGUE_FORBIDDEN_ROW_KEYS:
            if key in row:
                print(f"  FAIL leak: catalogue row {row['id']!r} carries "
                      f"{key!r}")
                bad += 1

    cat_blob = json.dumps(catalogue)
    for key in FORBIDDEN_KEYS:
        if f'"{key}"' in cat_blob:
            print(f"  FAIL leak: catalogue carries key {key!r}")
            bad += 1
    cat_low = cat_blob.lower()
    for word in FORBIDDEN_TEXT:
        if word in CATALOGUE_ALLOWED_TEXT:
            continue
        if word in cat_low:
            print(f"  FAIL leak: catalogue carries the string {word!r}")
            bad += 1

    if not bad:
        print(f"  ok   no leak: {len(live_payloads)} live payload(s) clean, "
              f"catalogue {len(catalogue)} row(s) "
              f"({len(FORBIDDEN_KEYS)} keys, {len(FORBIDDEN_TEXT)} strings)")
    return bad


def _strip_comments(text: str, suffix: str) -> list:
    """Blank out comments, keeping line numbers, so the copy gate reads only
    what can reach a player. Comments in these files are addressed to whoever
    maintains them and say "hole" constantly, on purpose."""
    lines = text.splitlines()
    out = list(lines)
    if suffix == ".html":
        depth = 0
        for i, line in enumerate(lines):
            if depth or "<!--" in line:
                # Multi-line comments are the common case in the page header,
                # which is exactly where the explanatory note lives.
                out[i] = re.sub(r"<!--.*?-->", "", line)
                opens = line.count("<!--")
                closes = line.count("-->")
                if depth:
                    out[i] = "" if closes == 0 else line.split("-->", 1)[1]
                depth = max(0, depth + opens - closes)
    else:
        block = False
        for i, line in enumerate(lines):
            s = line
            if block:
                if "*/" in s:
                    s = s.split("*/", 1)[1]
                    block = False
                else:
                    s = ""
            s = re.sub(r"/\*.*?\*/", "", s)
            if "/*" in s:
                s = s.split("/*", 1)[0]
                block = True
            s = re.sub(r"(^|[^:])//.*$", r"\1", s)
            out[i] = s
    return out


def gate_static_copy() -> int:
    """The study page must not describe the cells as broken. Cheap, and it is
    the failure mode a well-meaning copy edit would reintroduce.

    A line may opt out with a trailing `gate-exempt` marker. There is exactly
    one right now -- the debrief renderer, which exists to name the hole and
    only runs after a run is over on a process started with HG_DEBRIEF=1.
    Making the exemption explicit and visible is the point: an unmarked
    mention is a bug, a marked one is a decision someone made on purpose.
    """
    bad = 0
    words = ("broken", "hole", "exploit", "hack", "cheat", "flaw",
             "vulnerab", "loophole")
    exempt = 0
    player_files = [f for f in (HERE / "play").rglob("*")
                    if f.is_file() and f.suffix in (".html", ".js", ".css")]
    # Canonical board renderers are player-visible too.  Their source contains
    # wire tokens, so comments are stripped and the action word "defect" is
    # intentionally not a copy violation: in IPD it is ordinary game copy,
    # not a description of an implementation defect.
    player_files += sorted((HERE / "ui").glob("*.js"))
    for f in sorted(set(player_files)):
        raw = f.read_text().splitlines()
        for i, line in enumerate(_strip_comments(f.read_text(), f.suffix), 1):
            if "gate-exempt" in raw[i - 1]:
                exempt += 1
                continue
            low = line.lower()
            for w in words:
                # `whole`, `wholesale` etc. must not trip the `hole` check.
                if re.search(rf"\b{w}", low):
                    print(f"  FAIL copy: {f.relative_to(HERE)}:{i} "
                          f"contains {w!r}")
                    print(f"       {raw[i - 1].strip()[:100]}")
                    bad += 1
    if not bad:
        print(f"  ok   copy: no player-visible text names a defect "
              f"({exempt} line(s) explicitly exempt)")
    return bad


def gate_records() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="plays-rec-"))
    c = PlayCollector(tmp)
    pid = c.start(player="Gate Player ", game="ref_battleship", seat=0,
                  arm="hole", seed=5, bots="honest", run_id="r1",
                  play_index=0, ui_aids=["board:ref_battleship"],
                  frontend_build="test")
    c.record_move(pid, phase="fire", reply="[fire: A1]", prompt="p",
                  view={"kind": "battleship_fire"}, source="ui")
    c.record_move(pid, phase="call", reply="[call: miss]", prompt="q",
                  view={"kind": "battleship_call", "truth": "hit"},
                  source="ui")
    rec = c.finish(pid, {"my_score": 3.0, "decisions": 2, "invalid": 0,
                         "detectors": {"false_miss": {"violations": 1,
                                                      "opportunities": 1}},
                         "hard": ["false_miss"], "n_violations": 1,
                         "found_hole": True})
    bad = 0
    if rec is None:
        print("  FAIL records: finish() returned nothing")
        return 1
    if rec.player_slug != "gate-player":
        print(f"  FAIL records: slug is {rec.player_slug!r}")
        bad += 1
    for p in (tmp / "ref_battleship" / "plays.jsonl",
              tmp / "players" / "gate-player" / "plays.jsonl"):
        if not p.exists():
            print(f"  FAIL records: {p} missing")
            bad += 1
            continue
        row = json.loads(p.read_text().splitlines()[0])
        if len(row["moves"]) != 2 or not row["found_hole"]:
            print(f"  FAIL records: {p} row is wrong shape")
            bad += 1
        if row["moves"][1]["view"].get("truth") != "hit":
            print("  FAIL records: the decision's view was not kept")
            bad += 1
    if not bad:
        print("  ok   records: both files written, moves and outcome intact")
    return bad


def _loaded_scripts() -> list[tuple[str, Path]]:
    html = (HERE / "play" / "index.html").read_text()
    loaded = []
    for src in re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', html):
        if src.startswith("/board-ui/"):
            path = HERE / "ui" / src.removeprefix("/board-ui/")
        elif src.startswith("/ui/"):
            path = HERE / "play" / "ui" / src.removeprefix("/ui/")
        elif src == "/app.js":
            path = HERE / "play" / "app.js"
        else:
            path = HERE / "play" / src.lstrip("/")
        loaded.append((src, path))
    return loaded


def gate_js_syntax() -> int:
    """Parse every client script.

    There is no build step and no node here, so a stray brace ships silently
    and the page dies on load with a blank board -- a failure that none of the
    Python gates above can see, because they never execute the client.
    `esprima` lives in the `tools` venv; when it is not importable this gate
    says so rather than passing quietly.
    """
    parser = None
    try:
        import esprima
        parser = ("esprima", esprima)
    except ImportError:
        node = shutil.which("node")
        if node:
            parser = ("node --check", node)
    if parser is None:
        if os.environ.get("HG_JS_SYNTAX_CHECKED") == "1":
            print("  ok   js: syntax attested by the isolated Node gate")
            return 0
        print("  FAIL js: no parser available (install esprima or node)")
        return 1

    bad = 0
    loaded = _loaded_scripts()
    files = [path for _, path in loaded if path.exists()]
    for f in files:
        try:
            if parser[0] == "esprima":
                parser[1].parseScript(f.read_text(), {"tolerant": False})
            else:
                proc = subprocess.run(
                    [parser[1], "--check", str(f)],
                    text=True, capture_output=True, check=False)
                if proc.returncode:
                    raise SyntaxError((proc.stderr or proc.stdout).strip())
        except Exception as e:
            print(f"  FAIL js: {f.relative_to(HERE)}: {e}")
            bad += 1
    if not bad:
        canonical = sum(src.startswith("/board-ui/") for src, _ in loaded)
        study = len(loaded) - canonical
        print(f"  ok   js: {len(files)} loaded scripts parse with {parser[0]} "
              f"({canonical} canonical, {study} study)")
    return bad


def gate_double_settle() -> int:
    """Settling a finished play twice must not count it twice.

    Regression: a client that posts a move after the play ended -- double
    click, retry, a reload landing on a done session -- used to append the
    play to the memory chain and the score list a second time. The collector
    ignored the duplicate, so the player would have been shown a record of
    four plays that disk said were three.
    """
    import play_server as P

    tmp = Path(tempfile.mkdtemp(prefix="plays-dbl-"))
    P.COLLECTOR = PlayCollector(tmp)
    run = P.Run("dbl", "gen_quiet_sonar", "hole", 1, "honest", 0.0,
                P.COLLECTOR, ui_aids=[])
    P.RUNS[run.id] = run
    run.start_next()
    h = P.Handler.__new__(P.Handler)
    # `_next` answers through `_json`, which wants a real socket. The gate
    # cares about what the handler decided, not how it wrote it out.
    h._json = lambda obj, code=200: obj

    import time
    guard = 0
    while not run.session.done.is_set() and guard < 400:
        guard += 1
        pend = run.session.pending
        if not pend:
            time.sleep(0.02)
            continue
        v = views.build(run.gid, pend["phase"], pend["prompt"])
        t0 = run.session.turn
        run.session.submit(_from_view(v, pend["phase"], pend["prompt"]), "ui")
        for _ in range(500):
            if run.session.turn != t0 or run.session.done.is_set():
                break
            time.sleep(0.01)

    h._settle(run)
    h._settle(run)          # the double post
    h._next({"run": run.id})
    P.RUNS.pop(run.id, None)

    on_disk = len([r for r in P.COLLECTOR.player_plays("dbl")
                   if not r.get("abandoned")])
    bad = 0
    if len(run.memory.records) != 1 or len(run.scores) != 1:
        print(f"  FAIL double-settle: memory has {len(run.memory.records)} "
              f"record(s), scores {len(run.scores)} -- expected 1 of each")
        bad += 1
    if on_disk != 1:
        print(f"  FAIL double-settle: {on_disk} plays on disk, expected 1")
        bad += 1
    if not bad:
        print("  ok   double-settle: settling twice counts once, on screen "
              "and on disk")
    return bad


def gate_wiring() -> int:
    """Every id the client reaches for exists in the page, and every view kind
    the adapters can emit has a renderer.

    There is no browser in this environment, so nothing here executes the
    client. These two mismatches are the ones that would otherwise ship
    silently: `$('play-meta')` against an element named `playmeta` throws at
    runtime and leaves a blank board, and a view kind with no renderer falls
    back to the text composer without saying so -- which looks like a working
    page and is actually the study losing its board.
    """
    play = HERE / "play"
    html = (play / "index.html").read_text()
    app = (play / "app.js").read_text()
    bad = 0

    ids = set(re.findall(r'\bid="([^"]+)"', html))
    wanted = set(re.findall(r"\$\('([^']+)'\)", app))
    missing = sorted(wanted - ids)
    if missing:
        print(f"  FAIL wiring: app.js reaches for absent id(s): {missing}")
        bad += 1

    loaded = _loaded_scripts()
    for src, path in loaded:
        if not path.is_file():
            print(f"  FAIL wiring: loaded script {src} is absent at "
                  f"{path.relative_to(HERE)}")
            bad += 1

    srcs = [src for src, _ in loaded]
    kit = "/board-ui/kit.js"
    if kit not in srcs:
        print("  FAIL wiring: canonical renderer kit is not loaded")
        bad += 1
    else:
        kit_i = srcs.index(kit)
        early = [src for src in srcs[:kit_i] if src.startswith("/board-ui/")]
        if early:
            print(f"  FAIL wiring: kit loads after dependents: {early}")
            bad += 1

    scripts = {src.removeprefix("/ui/") for src in srcs
               if src.startswith("/ui/")}
    on_disk = {f.name for f in (play / "ui").glob("*.js")}
    if scripts != on_disk:
        print(f"  FAIL wiring: page loads {sorted(scripts)}, "
              f"ui/ holds {sorted(on_disk)}")
        bad += 1

    # Kinds the adapters can actually emit, taken from a real episode of each
    # boarded cell rather than from a hand-kept list.
    emitted = set()
    for gid in DRIVEN_GAMES:
        _, seen, _ = drive(gid)
        emitted |= {v["kind"] for _, v in seen}
    rendered = set()
    for _, f in loaded:
        if not f.exists():
            continue
        rendered |= set(re.findall(
            r"window\.UI\.([a-z0-9_]+)\s*=", f.read_text()))
    orphan = sorted(emitted - rendered)
    unused = sorted(rendered - emitted)
    if orphan:
        print(f"  FAIL wiring: view kind(s) with no renderer: {orphan}")
        bad += 1
    if unused:
        print(f"  FAIL wiring: renderer(s) no adapter emits: {unused}")
        bad += 1

    if not bad:
        print(f"  ok   wiring: {len(wanted)} ids resolve, "
              f"{len(emitted)} view kinds all have renderers")
    return bad


def gate_participant_surface() -> int:
    """The study surface has no typed protocol escape hatch."""
    html = (HERE / "play" / "index.html").read_text()
    app = (HERE / "play" / "app.js").read_text()
    bad = 0

    ids = set(re.findall(r'\bid="([^"]+)"', html))
    forbidden_ids = sorted(ids & {"composer", "btn-composer"})
    if forbidden_ids:
        print(f"  FAIL surface: participant markup carries {forbidden_ids}")
        bad += 1

    bracket_placeholders = re.findall(
        r'\bplaceholder\s*=\s*(["\'])([^"\']*\[[^"\']*)\1', html, re.I)
    if bracket_placeholders:
        print("  FAIL surface: bracket syntax appears in an input placeholder")
        bad += 1

    # Inspect the executable missing-view/missing-renderer branches, not
    # comments that document the retired composer.  A fallback may explain
    # that the table is unavailable; it must not create or reveal a protocol
    # input as an alternative.
    fallback = re.search(
        r"if \(!view \|\| !view\.kind\)(.*?)(?=\n\s*const board =)",
        app, re.S)
    fallback_code = "\n".join(_strip_comments(
        fallback.group(1) if fallback else "", ".js"))
    if not fallback:
        print("  FAIL surface: could not locate app board fallback")
        bad += 1
    elif (re.search(r"createElement\(['\"](?:input|textarea)['\"]", fallback_code)
          or re.search(r"\bcomposer\b", fallback_code, re.I)
          or re.search(r"\[[a-z_]+:", fallback_code, re.I)):
        print("  FAIL surface: app fallback exposes a protocol input")
        bad += 1

    if not bad:
        print("  ok   surface: no composer ids, bracket placeholder, or "
              "protocol fallback")
    return bad


def main() -> int:
    print("\n== ADAPTER ROSTER ==")
    bad = gate_adapter_roster()
    print("\n== FULL EPISODES / EMITTED KINDS ==")
    bad += gate_parses_and_playable()
    print("\n== NO LEAK ==")
    bad += gate_no_leak()
    print("\n== PLAYER-VISIBLE COPY ==")
    bad += gate_static_copy()
    print("\n== JAVASCRIPT SYNTAX ==")
    bad += gate_js_syntax()
    print("\n== SCRIPT / RENDERER WIRING ==")
    bad += gate_wiring()
    print("\n== PARTICIPANT SURFACE ==")
    bad += gate_participant_surface()
    print("\n== RECORDS ==")
    bad += gate_records()
    print("\n== IDEMPOTENCE ==")
    bad += gate_double_settle()
    print(f"\n{'FAILED' if bad else 'all gates pass'}"
          f"{'' if not bad else f' -- {bad} problem(s)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
