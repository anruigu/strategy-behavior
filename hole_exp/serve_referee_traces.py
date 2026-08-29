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

DEFAULT_PORT = 8794
ROOT = HERE / "results" / "referee_crossplay"

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

NAME = re.compile(r"(ref_\w+?)-(neutral|winmax)-(hole|nohole)-(\w+?)_vs_(\w+?)-s(\d+)$")


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


def load_all(root: pathlib.Path) -> Dict[str, Dict]:
    eps: Dict[str, Dict] = {}
    for wave in sorted(p for p in root.iterdir() if p.is_dir()):
        tdir = wave / "traces"
        if not tdir.is_dir():
            continue
        for f in sorted(tdir.iterdir()):
            m = NAME.match(f.stem)
            if not m:
                continue
            game, cond, arm, focal, other, seed = m.groups()
            key = f"{wave.name}/{f.stem}"
            meta = {"wave": wave.name, "game": game, "condition": cond,
                    "arm": arm, "focal": focal, "other": other,
                    "seed": int(seed), "id": key}
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
        det = Q.DETECT.get(e["game"])
        nviol = 0
        for t in e.get("turns") or []:
            t["role"] = role_of(e["game"], t["pid"], t["phase"])
            t["seat"] = ("FOCAL" if t["pid"] == 0 else "OPPONENT")
            t["model"] = t.get("model") or (e.get("models") or {}).get(
                str(t["pid"]), "")
            v = det(t["pid"], t["phase"], t["prompt"], t["content"]) if det else None
            t["violation"] = v
            nviol += bool(v)
            t["action"] = _action_tokens(t["content"])
        e["n_violations"] = nviol
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
<title>referee-hole traces</title><style>
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
  <select id="fc"></select><select id="fw"></select>
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
        vo=el('fv').checked;
  const rows=EPS.filter(e=>(!g||e.game===g)&&(!m||e.focal===m)&&
    (!c||e.condition===c)&&(!w||e.wave===w)&&(!vo||e.n_violations>0));
  el('list').innerHTML=rows.map(e=>`<div class="ep${CUR===e.id?' sel':''}"
    onclick="open_('${e.id}')">
    <div class="t">${e.game.replace('ref_','')} · ${e.focal} vs ${e.other}</div>
    <div class="s">${e.condition} / ${e.arm} · seed ${e.seed} · ${e.wave}</div>
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
   <div class="meta"><b>${e.game}</b> · ${e.condition} / ${e.arm} · seed ${e.seed}
    · focal <b>${e.focal}</b> vs <b>${e.other}</b> · ${e.wave}
    ${e.scores&&Object.keys(e.scores).length?' · scores '+JSON.stringify(e.scores):''}</div>
   <div class="legend">
    Left border: <span style="color:var(--focal)">focal seat (p0)</span> ·
    <span style="color:var(--opp)">opponent seat</span> ·
    <span style="color:var(--mark)">the mark</span>.
    <span style="color:var(--reason)">Reasoning</span> is rendered in its own
    block and is never merged into the reply &mdash; the reply is what the other
    players and the referee see, the reasoning is not.
    Flags are re-derived from the prompt the model was shown, independently of
    the engine's counters.
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
  refresh();
}
(async()=>{
  EPS=await (await fetch('/data')).json();
  ['fg','fm','fc','fw','fv'].forEach(i=>el(i).onchange=refresh);
  boot();
})();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    eps: Dict[str, Dict] = {}
    root: pathlib.Path = ROOT

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
            Handler.eps = load_all(Handler.root)
            return self._send(json.dumps(
                {"episodes": len(Handler.eps)}).encode(), "application/json")
        if path == "/data":
            # index only -- the turns are the bulk and are fetched per episode
            idx = [{k: e[k] for k in
                    ("id", "wave", "game", "condition", "arm", "focal", "other",
                     "seed", "n_turns", "n_violations", "has_reasoning")}
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
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args()

    Handler.root = pathlib.Path(a.root)
    Handler.eps = load_all(Handler.root)
    n_r = sum(1 for e in Handler.eps.values() if e["has_reasoning"])
    n_v = sum(e["n_violations"] for e in Handler.eps.values())
    print(f"[viewer] {len(Handler.eps)} episodes  "
          f"({n_r} with reasoning captured)  {n_v} flagged turns")
    by = {}
    for e in Handler.eps.values():
        by[e["wave"]] = by.get(e["wave"], 0) + 1
    for w, n in sorted(by.items()):
        print(f"[viewer]   {w:18s} {n:4d}")
    print(f"[viewer] http://{a.host}:{a.port}/   (forward this port)")
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
