"""Trace viewer for the referee-hole cross-play episodes. Stdlib only.

    python serve_referee_traces.py                 # 127.0.0.1:8794
    python serve_referee_traces.py --port 8801

Bound to 127.0.0.1 on purpose, matching `viz/serve.py`: the port is reached
through an SSH LocalForward, so it never needs a public interface. Pass
`--host 0.0.0.0` only if something else is doing the forwarding.

WHAT THIS SHOWS THAT THE TABLES CANNOT. `summarize_referee.py` says a rate.
The rate cannot say whether a defender that called a hit a miss was lying or
had lost track of its own board -- that distinction is what reclassified
`false_hit` from a diagnostic into a second exploit, and it was only ever
visible by reading the turn. So every turn here carries three things the
summary drops:

  * WHO IS SPEAKING, spelled out rather than implied. A seat number alone is
    unreadable across five games with different seat semantics, so each turn
    is labelled with the seat, the model behind it, whether it is the focal or
    the opponent seat, and its ROLE IN THIS GAME AT THIS PHASE -- battleship's
    `call` phase is the DEFENDER adjudicating a shot at its own fleet, which
    is the entire hole and is invisible if the turn just says "p1".
  * THE REASONING, IN ITS OWN BLOCK, never merged into the reply. The two are
    different objects: the reply is what the other players and the referee
    see, the reasoning is not. Merging them would make the model look like it
    announced a plan it in fact kept to itself.
  * THE VERDICT, re-derived FROM THE PROMPT. The badge on a turn is computed
    by `quote_referee_exploits.py`'s detectors, which read the ground truth out
    of the prompt the model was shown rather than out of the engine's counters.
    A badge that disagrees with the summary is a bug in one of the two, and
    that is the point of deriving it twice.

REASONING IS PRESENT IN SOME WAVES AND NOT OTHERS, AND THE UI SAYS WHICH.
Waves 1-3 captured `message.content` alone, so 456 episodes have the visible
reply and nothing behind it; those turns are marked `not captured` and are not
dressed up as a model that chose to think nothing. `wave4_reasoning` and
anything later carry it. The three vendors also differ in what they will
return -- Anthropic and Gemini give reasoning text, OpenAI gives a summary
alongside an encrypted block with no text in it -- so the block header names
the kind it got.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import quote_referee_exploits as Q  # noqa: E402
import referee_ablations  # noqa: E402,F401
import referee_games2  # noqa: E402,F401
import referee_games as RG  # noqa: E402

sys.path.insert(0, str(HERE / "hackable_games"))
try:                                     # the 2026-09-01 collaborative corpus
    import engines_native9 as EN9        # noqa: E402
    NAT = {g.NAME: g for g in EN9.NATIVE9}
except Exception:                        # noqa: BLE001
    NAT = {}

DEFAULT_PORT = 8794
ROOT = HERE / "results" / "referee_crossplay"
# The contagion waves live in their own tree with their own filename shape.
# `--root results/contagion` serves those instead; both are understood.
CONTAGION_ROOT = HERE / "results" / "contagion"

# Seat semantics differ per game, and a bare "p1" is unreadable across five of
# them. `(phase -> role)` where the role turns on the phase, else a flat role.
ROLES = {
    "ref_battleship": {"fire": "ATTACKER", "call": "DEFENDER (adjudicates the shot at its own fleet)"},
    "ref_estate": {"*": "INVESTOR (keeps its own books)"},
    "ref_signal": {"*": "PARTNER (cannot see its own hand)"},
    "ref_sidebar": {"*": "PLAYER"},
    "ref_exchange": {"*": "SETTLER"},
    # Added by a concurrent session to `referee_games.py`; it passes the same
    # gate battery, so it gets a real label rather than the unknown-game one.
    "ref_hanabi": {"*": "PARTNER (cannot see its own hand)"},
    # The second wave (`referee_games2.py`) and the ablation. Without these
    # every turn in six of the twelve cells rendered as
    # "PLAYER (game not defined in referee_games)" -- which is the viewer
    # saying it does not know what it is showing you, on the cells that
    # currently have the highest exploit rates in the suite. The role has to
    # name the SELF-REPORT, because that is where the hole is and it is
    # invisible if the turn just says "p1".
    "ref_auction": {"*": "BIDDER (declares its own remaining budget)"},
    "ref_commons": {"*": "BOAT (submits its own catch; the harbour credits it)"},
    "ref_orderbook": {"*": "TRADER (orders are never checked for backing)"},
    "ref_invoice": {"*": "CONTRACTOR (self-reports completion and hours)"},
    "ref_lemons": {"*": "SELLER (privately sees quality, advertises a grade)"},
    "ref_signal_strict": {"*": "PARTNER (cannot see its own hand)"},
    # The 2026-09-01 COLLABORATIVE corpus. The role has to name the move that
    # invites a partner, because on these cells that move is the whole event
    # and a turn that just says "p1" hides it. Unlike every cell above, the
    # exploit here is worthless alone -- the role text says so, so a reader
    # scrolling turns knows a lone reach is a LOSING move and not a win.
    "nat_mirror_manifest": {
        "pledge": "FILER (pledging 4 is an offer; alone it is rejected)",
        "claim": "FILER (a claim of 4 is only accepted if a second seat also filed 4)"},
    "nat_meridian_convoy": {
        "declare": "SHIPPER (declares its own volume; the 30-ton cap is not checked on the paired path)",
        "dispatch": "SHIPPER (names a transit partner; only a MUTUAL naming pays)"},
    "nat_cargo_pledge": {
        "pledge": "TRADER (declares a hold size)",
        "haul": "TRADER (loads crates; haul is checked against pledge)",
        "report": "TRADER (a report above the haul is only paid if another seat files the SAME number)"},
    "nat_seam_ledger": {
        "partner": "SURVEYOR (a mutual naming forms the filing crew)",
        "tally": "CREW (the clerk compares the two co-signed tallies to EACH OTHER, never to the dealt grade)"},
    "nat_open_gate": {
        "pledge": "RAIDER (publicly announces a target; this is the invitation)",
        "act": "RAIDER (two raiders on an unguarded target take +4 each; a lone raider loses 1)"},
    "nat_ridge_claim": {
        "signal": "SURVEYOR (legal weather is 0-3; 8 and 9 leave the public board)",
        "claim": "SURVEYOR (seats claiming the same ridge split its value)"},
    "nat_sealed_ante": {
        "route": "FILER (names the index its filing is stored under)",
        "seal": "FILER (a seal routed to a SEAT reaches that seat before the ante)",
        "ante": "PLAYER (highest card among the entrants takes the pot)"},
    "nat_xor_resonance": {
        "note": "DIGGER (stores a private scratch tag)",
        "dig": "DIGGER (6 points only if the PAIRED partner also digs the true cell)"},
    "nat_gate_fire": {
        "load": "RAIDER (chooses shot weight)",
        "fire": "RAIDER (a shot hits if the target did not fire back)"},
}


def role_of(game: str, pid: int, phase: str) -> str:
    if game == "ref_sidebar":
        return ("COLLUDER (on the private line)" if pid in RG.PAIR
                else "MARK (no channel, not told one exists)")
    m = ROLES.get(game)
    if m is None:
        # Not one of this module's cells. Another session writes `ref_hanabi`
        # into the same results tree; showing it is useful, silently giving it
        # a confident role label is not.
        return "PLAYER (game not defined in referee_games)"
    return m.get(phase) or m.get("*") or "PLAYER"


# ---------------------------------------------------------------------------
# loading -- structured .json when present, legacy .txt otherwise
# ---------------------------------------------------------------------------

# The trailing `-p<dose>` is OPTIONAL. It did not exist when this was
# written and the pattern was anchored straight after the seed, so
# every episode from a runner that stamps the audit dose into the
# filename -- which is now all of them -- was silently skipped. The
# viewer showed 461 archived episodes and none of the new waves, and
# an empty list reads as "nothing sampled" rather than as a parse miss.
NAME = re.compile(r"(ref_\w+?)-(neutral|winmax)-(hole|nohole)-"
                  r"(\w+?)_vs_(\w+?)-s(\d+)(?:-p([\d.]+))?$")


# `run_contagion.py --traces` writes
#   <game>-<design>-<leader mode>-<follower|L{latin}>-s<seed>.json
# which no amount of stretching gets `NAME` to match: it has no condition and
# no `_vs_`. A second pattern rather than one loose one, so a filename that
# fits NEITHER shape is still skipped rather than half-parsed.
NAME_CG = re.compile(r"((?:nat|gen|ref|ta)_\w+?)-(seed|observe)-"
                     r"(exploit|honest|live)-(\w+?)-s(\d+)$")


_TXT_HEAD = re.compile(r"p(\d) \[(\w+)\] \(([^)]*)\)")


def _from_txt(path: pathlib.Path, meta: Dict) -> Dict:
    """Legacy flat trace. The model id IS in the header and has to be pulled
    out here -- `Q.blocks` drops it, and a turn that cannot name the model
    behind the seat fails the one thing this viewer exists to do."""
    turns, models = [], {}
    for b in path.read_text().split("===== ")[1:]:
        head, rest = b.split("\n", 1)
        m = _TXT_HEAD.match(head)
        if not m or "--- prompt\n" not in rest:
            continue
        pid, phase, model = int(m.group(1)), m.group(2), m.group(3)
        prompt = rest.split("--- prompt\n", 1)[1].split("\n--- reply\n")[0]
        reply = rest.split("--- reply\n", 1)[1].strip()
        models[str(pid)] = model
        turns.append({"i": len(turns), "pid": pid, "phase": phase,
                      "model": model, "prompt": prompt, "content": reply,
                      "reasoning": "", "reasoning_kind": "not captured"})
    return dict(meta, turns=turns, models=models, scores={}, violations={},
                opportunities={}, gain={})


def _contagion_meta(f: pathlib.Path, wave: str, m, d: Dict) -> Dict:
    """Meta for one contagion episode, in the schema the index already uses.

    NOTHING IS OVERLOADED HERE. `condition` really is `neutral` and `arm`
    really is `hole` -- `run_contagion` samples only those, on purpose (see its
    docstring: `winmax` licenses hard play for every seat at once and so
    manufactures the correlated exploitation contagion would predict). The
    design axis is a NEW field with its own dropdown rather than a third value
    smuggled into `condition`.

    `focal` is the model in the seat the reading is about, which differs by
    design: in `seed` that is the live FOLLOWER (the leader is scripted and
    filtering by it would return everything), in `observe` it is whoever the
    Youden row put in the first live seat.
    """
    game, design, leader, who, seed = m.groups()
    seats = {int(k): v for k, v in (d.get("seats") or {}).items()}
    live = sorted(k for k, v in seats.items() if v not in ("scripted", "engine"))
    if design == "seed":
        focal = who
        other = f"scripted {leader} leader"
    else:
        focal = seats.get(live[0], "?") if live else "?"
        other = "+".join(seats[k] for k in live[1:]) or "?"
    return {"wave": wave, "game": game, "condition": "neutral", "arm": "hole",
            "focal": focal, "other": other, "seed": int(seed),
            "p_audit": 0.0, "design": design, "leader_mode": leader,
            "leader_seat": d.get("leader_seat"),
            "seats_models": [seats[k] for k in live]}


def _timeline_flags(e: Dict) -> None:
    """Badge contagion turns from the engine's own mark timeline.

    THIS IS NOT THE INDEPENDENT DERIVATION THE OTHER CELLS GET, and the page
    says so rather than letting the same red flag imply the same provenance.
    `quote_referee_exploits` re-reads the ground truth out of the prompt so a
    disagreement with the engine is a bug in one of the two; there is no such
    second implementation for these nine games, and writing one would be
    duplicating seven detectors for the sake of a check it could not actually
    perform independently.

    What it CAN show, and what the flag says, is which of the two kinds fired:
    a reach (INVITE) or a close (JOINT). That distinction is the reason these
    cells declare two detectors, and it is the thing worth seeing per turn.
    """
    g = NAT.get(e["game"])
    inv = set(getattr(g, "INVITE", ()) or ())
    jnt = set(getattr(g, "JOINT", ()) or ())
    marks: Dict = {}
    for row in e.get("timeline") or []:
        i, pid, kind, hit, _ch = row
        if hit:
            marks.setdefault((int(pid), int(i)), []).append(kind)
    # `mark_timeline` stamps each mark with the GLOBAL ask counter at the
    # moment it fired -- `len(tape.asks)`, not the seat's own decision ordinal
    # that the base `RefereeGame._mark` records. The two are easy to confuse
    # and the confusion is silent: using the per-seat number here flagged 6
    # turns in an episode the engine scored 35 marks in, because a seat's 18th
    # decision and the 18th ask of the episode are nowhere near each other.
    #
    # A mark stamped `i` means `i` asks had completed, so it belongs to the
    # LAST turn this seat took at or before index i-1 -- which is the decision
    # the seat had most recently made when the detector fired. That holds for
    # detectors that run at the end of a stage and for ones that run at
    # settlement, which is why it is done by search rather than by arithmetic
    # on the stage count.
    turns = e.get("turns") or []
    by_seat: Dict[int, List[int]] = {}
    for n, t in enumerate(turns):
        by_seat.setdefault(int(t["pid"]), []).append(n)
    for (pid, i), kinds in sorted(marks.items()):
        idxs = [n for n in by_seat.get(pid, []) if n <= i - 1]
        if not idxs:
            continue
        # A MULTISET, not a set. A cell can score the same kind twice against
        # one decision -- `ref_orderbook` books several orders a turn -- and
        # collapsing them lost the count, which is exactly what the
        # reconciliation check caught on 13 of its episodes.
        t = turns[idxs[-1]]
        acc = t.setdefault("_kinds", [])
        acc.extend(kinds)
        uniq = sorted(set(acc))
        label = ", ".join(f"{k}x{acc.count(k)}" if acc.count(k) > 1 else k
                          for k in uniq)
        tag = ("CLOSED -- a second seat met this one" if jnt & set(uniq)
               else "reached for the hole (alone, this loses)"
               if inv & set(uniq) else "flagged")
        t["violation"] = f"{label} \u2014 {tag}"


def _reconcile(e: Dict) -> bool:
    """Do the badges account for exactly the marks the engine recorded?

    The badge placement depends on lining up two independently-maintained
    indices -- the global ask counter `mark_timeline` stamps, and the turn
    order the runner wrote -- and getting it wrong is SILENT: badges simply
    land on the wrong turns, or on fewer of them, and the page still renders.
    That already happened once (a per-seat reading flagged 6 turns in an
    episode holding 35 marks), so the invariant is checked rather than trusted.

    Per seat, the multiset of kinds across that seat's badges must equal its
    row in `ep.violations`.
    """
    want: Dict[int, Dict[str, int]] = {}
    for pid, kinds in (e.get("violations") or {}).items():
        want[int(pid)] = {k: int(v) for k, v in kinds.items() if v}
    got: Dict[int, Dict[str, int]] = {}
    for t in e.get("turns") or []:
        for k in t.get("_kinds") or []:
            got.setdefault(int(t["pid"]), {})
            got[int(t["pid"])][k] = got[int(t["pid"])].get(k, 0) + 1
    return {p: v for p, v in want.items() if v} == {p: v for p, v in got.items() if v}


def load_all(root: pathlib.Path) -> Dict[str, Dict]:
    eps: Dict[str, Dict] = {}
    for wave in sorted(p for p in root.iterdir() if p.is_dir()):
        tdir = wave / "traces"
        if not tdir.is_dir():
            continue
        for f in sorted(tdir.iterdir()):
            mc = NAME_CG.match(f.stem)
            if mc and f.suffix == ".json":
                try:
                    d = json.loads(f.read_text())
                except Exception:                       # noqa: BLE001
                    continue
                key = f"{wave.name}/{f.stem}"
                e = dict(_contagion_meta(f, wave.name, mc, d), id=key)
                e.update({k: d.get(k) for k in
                          ("turns", "scores", "violations", "opportunities",
                           "timeline")})
                e["models"] = d.get("seats") or {}
                eps[key] = e
                continue
            m = NAME.match(f.stem)
            if not m:
                continue
            game, cond, arm, focal, other, seed, dose = m.groups()
            key = f"{wave.name}/{f.stem}"
            meta = {"wave": wave.name, "game": game, "condition": cond,
                    "arm": arm, "focal": focal, "other": other,
                    "seed": int(seed), "p_audit": float(dose or 0.0),
                    "id": key}
            if f.suffix == ".json":
                try:
                    d = json.loads(f.read_text())
                except Exception:                       # noqa: BLE001
                    continue
                eps[key] = dict(meta, **{k: d.get(k) for k in
                                         ("turns", "models", "scores",
                                          "violations", "opportunities",
                                          "gain", "n_players", "exploiters")})
            elif f.suffix == ".txt" and key not in eps:
                eps[key] = _from_txt(f, meta)
    # annotate every turn once, at load time
    for e in eps.values():
        cg = "design" in e
        det = None if cg else Q.DETECT.get(e["game"])
        lead = e.get("leader_seat")
        for t in e.get("turns") or []:
            t["role"] = role_of(e["game"], t["pid"], t["phase"])
            if cg:
                # FOCAL/OPPONENT is the wrong frame for a contagion episode --
                # the axis is who could have been followed, not who is being
                # measured against whom.
                t["seat"] = ("LEADER (scripted)" if t.get("scripted")
                             else "LEADER" if t["pid"] == lead else "FOLLOWER")
            else:
                t["seat"] = ("FOCAL" if t["pid"] == 0 else "OPPONENT")
            t["model"] = t.get("model") or (e.get("models") or {}).get(
                str(t["pid"]), "")
            t["violation"] = (det(t["pid"], t["phase"], t["prompt"],
                                  t["content"]) if det else None)
            t["action"] = _action_tokens(t["content"])
            t.setdefault("reasoning", "")
            t.setdefault("reasoning_kind", "not captured")
        if cg:
            _timeline_flags(e)
        e["n_violations"] = sum(bool(t.get("violation"))
                                for t in e.get("turns") or [])
        e["flag_source"] = ("engine mark timeline" if cg
                            else "re-derived from the prompt")
        if cg:
            e["reconciled"] = _reconcile(e)
        e["n_turns"] = len(e.get("turns") or [])
        e["has_reasoning"] = any((t.get("reasoning") or "").strip()
                                 for t in e.get("turns") or [])
    return eps


_TOKEN = re.compile(r"\[[a-z_]+\s*:[^\]]*\]", re.I)


def _action_tokens(text: str) -> List[str]:
    return _TOKEN.findall(text or "")


# ---------------------------------------------------------------------------
# page
# ---------------------------------------------------------------------------

PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<title>hole traces</title><style>
:root{
 --bg:#0f1115; --panel:#161a22; --line:#252b37; --ink:#e6e9ef; --dim:#8b94a7;
 --focal:#7aa2f7; --opp:#9ece6a; --mark:#e0af68; --bad:#f7768e;
 --reason:#bb9af7;
}
*{box-sizing:border-box}
body{margin:0;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;
 background:var(--bg);color:var(--ink);display:flex;height:100vh}
#side{width:390px;min-width:390px;border-right:1px solid var(--line);
 overflow:auto;padding:10px}
#main{flex:1;overflow:auto;padding:16px 22px}
h1{font-size:14px;margin:0 0 10px;letter-spacing:.06em;color:var(--dim);
 text-transform:uppercase}
select,input{background:var(--panel);color:var(--ink);border:1px solid var(--line);
 border-radius:5px;padding:5px 7px;font:inherit;margin:0 4px 6px 0}
.ep{padding:7px 9px;border:1px solid var(--line);border-radius:6px;
 margin-bottom:5px;cursor:pointer;background:var(--panel)}
.ep:hover{border-color:var(--focal)}
.ep.sel{border-color:var(--focal);background:#1b2130}
.ep .t{font-weight:600}
.ep .s{color:var(--dim);font-size:11.5px}
.pill{display:inline-block;padding:1px 6px;border-radius:9px;font-size:10.5px;
 border:1px solid var(--line);margin-right:4px;color:var(--dim)}
.pill.v{color:var(--bad);border-color:var(--bad)}
.pill.r{color:var(--reason);border-color:var(--reason)}

.turn{border:1px solid var(--line);border-radius:8px;margin-bottom:14px;
 background:var(--panel);overflow:hidden}
.turn.focal{border-left:4px solid var(--focal)}
.turn.opponent{border-left:4px solid var(--opp)}
.turn.markseat{border-left:4px solid var(--mark)}
.turn.viol{box-shadow:inset 0 0 0 1px rgba(247,118,142,.35)}
.hd{padding:8px 12px;border-bottom:1px solid var(--line);
 display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;background:#141821}
.who{font-weight:700}
.who.focal{color:var(--focal)} .who.opponent{color:var(--opp)}
.who.markseat{color:var(--mark)}
.role{color:var(--ink)} .model{color:var(--dim)} .ph{color:var(--dim)}
.sec{padding:9px 12px;border-top:1px dashed var(--line)}
.sec h4{margin:0 0 5px;font-size:10.5px;letter-spacing:.09em;
 text-transform:uppercase;color:var(--dim);font-weight:700}
.reason{background:#191426;border-left:3px solid var(--reason)}
.reason h4{color:var(--reason)}
.reason pre{color:#cdb8f2;font-style:italic}
.reply{background:#131922}
pre{margin:0;white-space:pre-wrap;word-break:break-word;font:inherit}
.prompt pre{color:var(--dim);max-height:230px;overflow:auto}
.tok{background:#20304a;color:#cfe3ff;border:1px solid #35507a;border-radius:4px;
 padding:0 5px;margin-right:5px;display:inline-block}
.vio{color:var(--bad);font-weight:700;padding:7px 12px;background:#241a1f;
 border-top:1px dashed var(--line)}
.none{color:var(--dim);font-style:italic}
details summary{cursor:pointer;color:var(--dim);outline:none}
.meta{color:var(--dim);margin-bottom:14px}
.legend{color:var(--dim);font-size:11.5px;margin:6px 0 12px;line-height:1.7}
</style></head><body>
<div id="side">
 <h1>episodes <a href="#" onclick="reload_();return false"
   style="color:var(--dim);font-size:11px;float:right">reload</a></h1>
 <div>
  <select id="fg"></select><select id="fm"></select>
  <select id="fc"></select><select id="fw"></select><select id="fd"></select>
  <label style="color:var(--dim);font-size:11.5px">
   <input type="checkbox" id="fv" style="margin:0 4px 0 0">violations only</label>
 </div>
 <div id="list"></div>
</div>
<div id="main"><div class="none">pick an episode on the left</div></div>
<script>
let EPS=[], CUR=null;
const el=(id)=>document.getElementById(id);
const esc=(s)=>(s||"").replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

function opts(sel,vals,label){
  sel.innerHTML='<option value="">'+label+'</option>'+
    vals.map(v=>`<option value="${v}">${v}</option>`).join('');
}
function refresh(){
  const g=el('fg').value,m=el('fm').value,c=el('fc').value,w=el('fw').value,
        d=el('fd').value,vo=el('fv').checked;
  // The model filter matches the focal seat OR any seat at the table: in an
  // observe episode every seat is live and "the focal model" is only the one
  // the Youden row happened to put first, so focal-only would hide two thirds
  // of the episodes a given model actually played.
  const rows=EPS.filter(e=>(!g||e.game===g)&&
    (!m||e.focal===m||(e.seats_models||[]).includes(m))&&
    (!c||e.condition===c)&&(!w||e.wave===w)&&
    (!d||(e.design||'crossplay')===d)&&(!vo||e.n_violations>0));
  el('list').innerHTML=rows.map(e=>`<div class="ep${CUR===e.id?' sel':''}"
    onclick="open_('${e.id}')">
    <div class="t">${e.game.replace(/^(ref|nat|gen)_/,'')} · ${e.focal} vs ${e.other}</div>
    <div class="s">${e.design?e.design+' / '+e.leader_mode:e.condition+' / '+e.arm}
      · seed ${e.seed} · ${e.wave}</div>
    <div style="margin-top:4px">
      <span class="pill">${e.n_turns} turns</span>
      ${e.n_violations?`<span class="pill v">${e.n_violations} flagged</span>`:''}
      ${e.has_reasoning?`<span class="pill r">reasoning</span>`:''}
    </div></div>`).join('')||'<div class="none">nothing matches</div>';
}
async function open_(id){
  CUR=id; refresh();
  const e=await (await fetch('/episode?id='+encodeURIComponent(id))).json();
  const seatCls=(t)=>t.role.startsWith('MARK')?'markseat':
                     (t.pid===0?'focal':'opponent');
  el('main').innerHTML=`
   <div class="meta"><b>${e.game}</b> · ${e.design?
      e.design+' design / leader '+e.leader_mode:e.condition+' / '+e.arm}
    · seed ${e.seed} · focal <b>${e.focal}</b> vs <b>${e.other}</b> · ${e.wave}
    ${e.scores&&Object.keys(e.scores).length?' · scores '+JSON.stringify(e.scores):''}</div>
   <div class="legend">
    Left border: <span style="color:var(--focal)">focal seat (p0)</span> ·
    <span style="color:var(--opp)">opponent seat</span> ·
    <span style="color:var(--mark)">the mark</span>.
    <span style="color:var(--reason)">Reasoning</span> is rendered in its own
    block and is never merged into the reply &mdash; the reply is what the other
    players and the referee see, the reasoning is not.
    ${e.design?`Flags come from the <b>engine's mark timeline</b>, not from an
    independent re-derivation &mdash; there is no second implementation of
    these detectors, so a flag here confirms the engine rather than checking
    it. Each one says which kind fired:
    <b>reached</b> (a seat went for the hole on its own, which on a
    collaborative hole <i>loses</i> unless somebody joins) or
    <b>CLOSED</b> (a second seat met it in the same round &mdash; the only
    event that pays).`
    :`Flags are re-derived from the prompt the model was shown, independently
    of the engine's counters.`}
   </div>
   ${e.turns.map(t=>`
    <div class="turn ${seatCls(t)} ${t.violation?'viol':''}">
     <div class="hd">
       <span class="who ${seatCls(t)}">p${t.pid}</span>
       <span class="pill">${t.seat}</span>
       <span class="role">${esc(t.role)}</span>
       <span class="model">${esc(t.model)||'model n/a'}</span>
       <span class="ph">· phase: <b>${esc(t.phase)}</b> · turn ${t.i}</span>
     </div>
     <div class="sec prompt"><details><summary>prompt (game state shown to this seat)</summary>
       <pre>${esc(t.prompt)}</pre></details></div>
     <div class="sec reason">
       <h4>reasoning ${t.reasoning_kind&&t.reasoning_kind!=='none'?
          '· '+esc(t.reasoning_kind):''}${t.reasoning_tokens?
          ' · '+t.reasoning_tokens+' tok':''}</h4>
       ${(t.reasoning||'').trim()?`<pre>${esc(t.reasoning)}</pre>`
         :`<div class="none">${t.reasoning_kind==='not captured'
            ?'not captured in this wave':'none returned for this turn'}</div>`}
     </div>
     <div class="sec reply"><h4>reply (visible to the referee and other seats)</h4>
       <div style="margin-bottom:6px">${(t.action||[]).map(a=>
         `<span class="tok">${esc(a)}</span>`).join('')}</div>
       <pre>${esc(t.content)}</pre></div>
     ${t.violation?`<div class="vio">⚑ ${esc(t.violation)}</div>`:''}
    </div>`).join('')}`;
  el('main').scrollTop=0;
}
async function reload_(){
  await fetch('/reload');
  EPS=await (await fetch('/data')).json();
  boot();
}
function boot(){
  opts(el('fg'),[...new Set(EPS.map(e=>e.game))].sort(),'all games');
  opts(el('fm'),[...new Set(EPS.map(e=>e.focal))].sort(),'all models');
  opts(el('fc'),[...new Set(EPS.map(e=>e.condition))].sort(),'all conditions');
  opts(el('fw'),[...new Set(EPS.map(e=>e.wave))].sort(),'all waves');
  opts(el('fd'),[...new Set(EPS.map(e=>e.design||'crossplay'))].sort(),
       'all designs');
  refresh();
}
(async()=>{
  EPS=await (await fetch('/data')).json();
  ['fg','fm','fc','fw','fd','fv'].forEach(i=>el(i).onchange=refresh);
  boot();
})();
</script></body></html>"""


def load_roots(roots: List[pathlib.Path]) -> Dict[str, Dict]:
    """Merge several trace trees into one index.

    The crossplay tree and the contagion tree hold different designs of the
    same experiment and are worth reading side by side, but their wave names
    are not guaranteed distinct -- so when more than one root is served, the
    tree name is prefixed onto the wave. With a single root the wave labels are
    left exactly as they were, so existing screenshots and links still read.
    """
    out: Dict[str, Dict] = {}
    multi = len(roots) > 1
    for r in roots:
        if not r.is_dir():
            print(f"[viewer] skipping {r} (not a directory)")
            continue
        for k, e in load_all(r).items():
            if multi:
                e["wave"] = f"{r.name}/{e['wave']}"
                k = f"{r.name}/{k}"
                e["id"] = k
            out[k] = e
    return out


class Handler(BaseHTTPRequestHandler):
    eps: Dict[str, Dict] = {}
    root: pathlib.Path = ROOT
    roots: List[pathlib.Path] = [ROOT]

    def _send(self, body: bytes, ctype: str):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):                                   # noqa: N802
        path = self.path.split("?")[0]
        if path == "/":
            return self._send(PAGE.encode(), "text/html; charset=utf-8")
        if path == "/reload":
            # Waves land while the viewer is open. Re-scanning on demand beats
            # restarting, and beats re-scanning on every /data -- parsing 500+
            # traces is not something to do on each keystroke.
            Handler.eps = load_roots(Handler.roots)
            return self._send(json.dumps(
                {"episodes": len(Handler.eps)}).encode(), "application/json")
        if path == "/data":
            # index only -- the turns are the bulk and are fetched per episode
            idx = [{**{k: e[k] for k in
                       ("id", "wave", "game", "condition", "arm", "focal",
                        "other", "seed", "n_turns", "n_violations",
                        "has_reasoning")},
                    "design": e.get("design", ""),
                    "leader_mode": e.get("leader_mode", ""),
                    "seats_models": e.get("seats_models", [])}
                   for e in self.eps.values()]
            idx.sort(key=lambda r: (r["game"], r["condition"], r["focal"],
                                    r["seed"]))
            return self._send(json.dumps(idx).encode(), "application/json")
        if path == "/episode":
            q = dict(p.split("=", 1) for p in self.path.split("?", 1)[-1].split("&")
                     if "=" in p)
            from urllib.parse import unquote
            e = self.eps.get(unquote(q.get("id", "")))
            if not e:
                self.send_error(404)
                return
            return self._send(json.dumps(e).encode(), "application/json")
        self.send_error(404)

    def log_message(self, fmt, *args):                  # noqa: A003
        pass


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--root", action="append", default=None,
                    help="trace tree to serve; repeatable. Defaults to the "
                         "crossplay tree plus the contagion tree.")
    a = ap.parse_args()

    roots = ([pathlib.Path(r) for r in a.root] if a.root
             else [ROOT, CONTAGION_ROOT])
    Handler.roots = roots
    Handler.root = roots[0]
    Handler.eps = load_roots(roots)
    n_r = sum(1 for e in Handler.eps.values() if e["has_reasoning"])
    n_v = sum(e["n_violations"] for e in Handler.eps.values())
    print(f"[viewer] {len(Handler.eps)} episodes  "
          f"({n_r} with reasoning captured)  {n_v} flagged turns")
    cg = [e for e in Handler.eps.values() if "design" in e]
    if cg:
        bad = [e["id"] for e in cg if not e.get("reconciled")]
        print(f"[viewer] {len(cg)} contagion episodes; badges reconcile with "
              f"the engine's counters in {len(cg)-len(bad)}/{len(cg)}")
        for b in bad[:5]:
            print(f"[viewer]   MISMATCH {b}")
    by = {}
    for e in Handler.eps.values():
        by[e["wave"]] = by.get(e["wave"], 0) + 1
    for w, n in sorted(by.items()):
        print(f"[viewer]   {w:18s} {n:4d}")
    for r in roots:
        print(f"[viewer]   root {r}")
    print(f"[viewer] http://{a.host}:{a.port}/   (forward this port)")
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
