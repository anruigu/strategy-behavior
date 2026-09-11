"""Play episodes against the ADAPTIVE / ADAPTIVE_RECOVER counterparts and build
a self-contained trace viewer that makes the new opponent utterances legible.

Two sources per cell, labelled per episode (same bargain as
`results/nohole_traces/make_viewer.py`):

  * model    -- Qwen/Qwen3.8-27B sampled WITH thinking on, so the agent's
               reasoning is captured and shown. The `<think>...</think>` block
               is split off before the action reaches the environment, so the
               parser still sees a clean bracketed token and reasoning cannot
               leak into the exploit/honest classification.
  * scripted -- always-exploit reference. It never reasons, but it reliably
               drives the counterpart through warn -> punish -> (recover),
               which is the whole point of this change and is not guaranteed to
               appear in a well-behaved model's play.

The viewer is written into `results/nohole_traces/adaptive_sim.html`, served by
the http.server already running on :8795, i.e.
http://localhost:8795/adaptive_sim.html. (It used to own `adaptive.html`; that
address now holds the grim-vs-tft eval contrast built by `grim_vs_tft.py`.)
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core       # noqa: E402
import registry   # noqa: E402

MODEL = "Qwen/Qwen3.8-27B"
# Game cells (new utterances reach the learner) + the two hand-written cells
# with the richest graded talk (ipd's warn, trust's recovery narration).
ENVS = ("ipd3", "staghunt", "winasmuch", "ipd", "trust")
ARMS = ("adaptive", "adaptive_recover")
DOSE = {"dond": 0.75}          # everything else at 1.0

THINK_RE = re.compile(r"<think>(.*?)</think>", re.S)


def split_think(raw: str, thinking: bool) -> tuple[str, str]:
    """Separate a Qwen reasoning block from the answer.

    Qwen3's chat template PRE-OPENS `<think>` in the prompt, so the sampled
    text has no opening tag -- it is `reasoning </think> answer`. Handle that,
    the fully-closed form, and (when thinking is on) a budget-truncated thought
    that never reached `</think>`: keep it all as reasoning and emit no answer,
    which the env scores invalid -> honest rather than misreading the thought
    as an action.
    """
    if not thinking:
        return "", raw.strip()
    m = THINK_RE.search(raw)
    if m:
        return m.group(1).strip(), THINK_RE.sub("", raw).strip()
    if "</think>" in raw:
        pre, _, post = raw.partition("</think>")
        return pre.replace("<think>", "").strip(), post.strip()
    # No closing tag: the thought ran out the token budget. All reasoning.
    return raw.replace("<think>", "").strip(), ""


class LoggingActor:
    """Wraps an `act` callable, records reasoning + answer for every turn.

    The env only ever sees the answer, so classification is unaffected; the
    reasoning rides alongside the record for the viewer.
    """

    def __init__(self, inner: Callable[[List[dict], dict], str],
                 thinking: bool = False):
        self.inner = inner
        self.thinking = thinking
        self.log: List[Dict] = []

    def reset_trace(self) -> None:
        """Start a fresh episode's log.

        `to_viewer.episodes` calls this between seeds; without it one actor
        reused across seeds accumulates every episode's reasoning into one list
        and the viewer attributes turn 40 of seed 3 to seed 0.
        """
        self.log = []

    def act(self, messages: List[dict], meta: Optional[dict] = None) -> str:
        raw = self.inner(messages, meta or {})
        reasoning, answer = split_think(raw, self.thinking)
        self.log.append({
            "reasoning": reasoning,
            "answer": answer,
            "phase": (meta or {}).get("phase"),
            "in_decision": (meta or {}).get("in_decision"),
            "round": (meta or {}).get("round"),
        })
        return answer


def build_model_maker():
    import tinker
    import tinker_actor

    core.load_env_file()
    sc = tinker.ServiceClient()

    def make(seed: int) -> Callable[[List[dict], dict], str]:
        # Thinking ON, effort LOW, budget raised: Qwen3.8-27B defaults to xhigh
        # effort and will run past a 384 budget and get cut off mid-action
        # (tinker_actor's own warning). close_bracket MUST be off with thinking
        # -- a ']' inside the <think> block would halt before the answer.
        actor, _ = tinker_actor.build(
            sc, MODEL, temperature=0.7, top_p=0.9, max_tokens=1024, seed=seed,
            enable_thinking=True, reasoning_effort="low", close_bracket=False)
        return actor.act

    return make


def run(envs, arms, model_seeds, scripted_seeds, workers) -> List[Dict]:
    make_model = build_model_maker() if model_seeds else None
    tasks = []
    for env in envs:
        dose = DOSE.get(env, 1.0)
        for arm in arms:
            for seed in model_seeds:
                tasks.append((env, arm, dose, seed, "model"))
            for seed in scripted_seeds:
                tasks.append((env, arm, dose, seed, "scripted"))

    def one(task) -> Optional[Dict]:
        env, arm, dose, seed, source = task
        spec = registry.get(env)
        try:
            if source == "model":
                la = LoggingActor(make_model(seed), thinking=True)
                tag = f"model:{MODEL.split('/')[-1]}"
            else:
                la = LoggingActor(spec.scripted("exploit"), thinking=False)
                tag = "scripted:exploit"
            rec = registry.rollout(spec, la.act, consequence=arm, dose=dose,
                                   seed=seed)
            rec["_reasoning"] = la.log
            rec["_source"] = tag
            print(f"[sim] {env:9s} {arm:16s} {source:8s} seed={seed} "
                  f"opp={rec['opponent']:16s} payoff={rec['payoff']:+.1f} "
                  f"xr={rec['stats'].get('exploit_rate')} "
                  f"retaliated={rec['stats'].get('retaliated')}", flush=True)
            return rec
        except Exception as exc:  # a dead episode must not kill the sweep
            print(f"  !! {env}/{arm}/{source} seed={seed}: "
                  f"{type(exc).__name__}: {exc}", flush=True)
            return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        recs = list(ex.map(one, tasks))
    return [r for r in recs if r]


# --------------------------------------------------------------------------
# viewer
# --------------------------------------------------------------------------

TITLE = {
    "ipd3": "Three-player IPD (game cell)",
    "staghunt": "Stag Hunt (game cell)",
    "ipd": "Iterated Prisoner's Dilemma",
    "trust": "Trust / Investment",
    "winasmuch": "Win As Much As You Can (game cell)",
}

# Utterance classes, coloured so the trust dynamics are impossible to miss.
WARN_RE = re.compile(
    r"watching the pattern|keeping count|keep cooperating for now|"
    r"don't forget it|not sure you'?ll be there|let it go for now|"
    r"i noticed|hold the stag once more|trust is thin|one slip|"
    r"for now, not forever|noticed that", re.I)
PUNISH_RE = re.compile(
    r"don'?t trust|not cooperating with you again|left me on the stag|"
    r"out of patience|not standing there again|done letting it go|"
    r"not left me much choice|taking the hare|i'?m taking x|"
    r"done carrying this|not going to keep handing you|"
    r"not playing straight|playing accordingly|break this table|"
    r"broke this table|carried y long enough|i'?m out|not this round", re.I)
RECOVER_RE = re.compile(
    r"cooperating with you again|work with you again|back to cooperating|"
    r"as long as it holds|keep holding it|trust you on the stag again|"
    r"carry the commons with you again|hold the line with you again|"
    r"as long as it lasts|willing to keep staking|keep staking you|"
    r"slate'?s mostly clear|so i am too|stayed on y since", re.I)


def esc(s: str) -> str:
    return html.escape(str(s))


def hi(content: str) -> str:
    out = []
    for ln in str(content).split("\n"):
        e = esc(ln)
        if not ln.strip():
            out.append(e)
        elif RECOVER_RE.search(ln):
            out.append(f"<span class='u-recover'>{e}</span>")
        elif PUNISH_RE.search(ln):
            out.append(f"<span class='u-punish'>{e}</span>")
        elif WARN_RE.search(ln):
            out.append(f"<span class='u-warn'>{e}</span>")
        else:
            out.append(e)
    return "\n".join(out)


def transcript(rec: Dict):
    turns = rec.get("turns", [])
    if not turns:
        return []
    blocks = [(m["role"], m["content"]) for m in turns[-1]["messages"]]
    last = turns[-1]
    tag = ("agent exploit" if last.get("parsed") == "exploit"
           else "agent honest" if last.get("parsed") == "honest" else "agent")
    blocks.append((tag, last.get("action", "")))
    return blocks


def reasoning_panel(rec: Dict) -> str:
    log = [e for e in rec.get("_reasoning", []) if e.get("reasoning")]
    if not log:
        if rec["_source"].startswith("scripted"):
            return ("<div class='reason none'>scripted reference &mdash; no "
                    "reasoning</div>")
        return ("<div class='reason none'>model returned no &lt;think&gt; block "
                "on any turn</div>")
    rows = []
    for i, e in enumerate(rec.get("_reasoning", [])):
        if not e.get("reasoning"):
            continue
        ans = esc(e["answer"])[:200]
        rows.append(
            f"<div class='rturn'><div class='rhead'>turn {i + 1}"
            f"<span class='ract'>&rarr; {ans}</span></div>"
            f"<pre class='rbody'>{esc(e['reasoning'])}</pre></div>")
    return ("<details class='reason'><summary>agent reasoning &middot; "
            f"{len(rows)} thinking turn(s)</summary>{''.join(rows)}</details>")


def render_episode(rec: Dict) -> str:
    s = rec.get("stats", {})
    src = rec.get("_source", "?")
    kind = "model" if src.startswith("model") else "scripted"
    retaliated = bool(s.get("retaliated"))
    xr = s.get("exploit_rate")
    meta = [f"opponent <b>{esc(rec.get('opponent'))}</b>",
            f"payoff <b>{rec.get('payoff'):+.1f}</b>"]
    if xr is not None:
        meta.append(f"exploit <b>{xr:.2f}</b>")
    badge = ("<span class='pill hot'>RETALIATED</span>" if retaliated
             else "<span class='pill cold'>no retaliation</span>")

    rows = []
    for role, content in transcript(rec):
        cls = ("system" if role == "system"
               else "agent" if role.startswith("agent") else "game")
        extra = ("exploit" if role == "agent exploit"
                 else "honest" if role == "agent honest" else "")
        label = {"agent exploit": "agent \u00b7 EXPLOIT",
                 "agent honest": "agent \u00b7 honest", "agent": "agent",
                 "user": "game / counterpart", "system": "system"}.get(role, role)
        body = hi(content) if cls == "game" else esc(content)
        rows.append(f"<div class='msg {cls}'><span class='role {extra}'>"
                    f"{esc(label)}</span><pre>{body}</pre></div>")

    summary = (f"<span class='src {kind}'>{esc(src.split(':', 1)[-1])}</span> "
               f"{badge} &middot; " + " &middot; ".join(meta))
    is_open = " open" if (retaliated and kind == "scripted") else ""
    return (f"<details class='ep'{is_open}><summary>{summary}</summary>"
            f"<div class='body'>{reasoning_panel(rec)}"
            f"{''.join(rows)}</div></details>")


def render_cell(env: str, arm: str, eps: List[Dict]) -> str:
    eps = sorted(eps, key=lambda r: (0 if r["_source"].startswith("model") else 1,
                                     0 if r["stats"].get("retaliated") else 1))
    n_model = sum(1 for r in eps if r["_source"].startswith("model"))
    n_hot = sum(1 for r in eps if r["stats"].get("retaliated"))
    body = "".join(render_episode(r) for r in eps)
    aid = f"{env}-{arm}"
    return (f"<section id='{aid}'><h3>{esc(TITLE.get(env, env))} "
            f"<span class='arm {arm}'>{arm}</span></h3>"
            f"<p class='count'>{len(eps)} episodes ({n_model} model, "
            f"{len(eps) - n_model} scripted) &middot; "
            f"<b>{n_hot} show the counterpart retaliating</b></p>{body}</section>")


PAGE = """<!doctype html><html><head><meta charset='utf-8'>
<title>Adaptive-trust opponent traces</title><style>
:root{{--bg:#0f1115;--card:#171a21;--fg:#e6e6e6;--mut:#8b93a7;--acc:#6ea8fe}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{padding:18px 24px;border-bottom:1px solid #262a33;position:sticky;top:0;
background:var(--bg);z-index:5}}header h1{{margin:0 0 6px;font-size:18px}}
header p{{margin:0;color:var(--mut);font-size:13px;max-width:900px}}
nav{{margin-top:8px}}nav a{{color:var(--acc);margin-right:12px;font-size:12.5px;
text-decoration:none}}
main{{max-width:1120px;margin:0 auto;padding:0 24px 80px}}
section{{margin-top:30px}}h3{{font-size:15px;border-bottom:1px solid #262a33;
padding-bottom:6px}}
.arm{{font-size:11px;font-weight:700;padding:1px 7px;border-radius:10px;
margin-left:6px}}.arm.adaptive{{background:#3a2a12;color:#e0b070}}
.arm.adaptive_recover{{background:#12352a;color:#6ed0a0}}
.count{{color:var(--mut);font-size:12px;margin:4px 0 12px}}
.legend{{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0 0;font-size:12px}}
.legend span{{padding:1px 7px;border-radius:4px}}
details.ep{{background:var(--card);border:1px solid #262a33;border-radius:8px;
margin:8px 0;padding:6px 12px}}
details.ep>summary{{cursor:pointer;font-size:12.5px;color:#cfd6e4}}
.src{{font-weight:700;padding:1px 6px;border-radius:4px;font-size:11px}}
.src.model{{background:#243b2a;color:#7ee0a0}}
.src.scripted{{background:#2a2f3d;color:#9fb0d0}}
.body{{margin-top:10px}}
.msg{{margin:7px 0;padding:8px 10px;border-radius:6px;background:#10131a}}
.msg.system{{opacity:.55}}.msg.game{{border-left:3px solid #3a4152}}
.msg.agent{{border-left:3px solid #4a6}}
.role{{display:inline-block;font-size:11px;color:var(--mut);
text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}}
.role.exploit{{color:#ff8f8f}}.role.honest{{color:#7ee0a0}}
pre{{margin:0;white-space:pre-wrap;word-break:break-word;font:12.5px/1.5
ui-monospace,SFMono-Regular,Menlo,monospace}}
.u-warn{{display:block;background:#3a2f12;color:#f0c674;border-radius:3px;
padding:0 4px;margin:1px -4px}}
.u-punish{{display:block;background:#3a1d22;color:#ffb4b4;border-radius:3px;
padding:0 4px;margin:1px -4px}}
.u-recover{{display:block;background:#123524;color:#8fe0b0;border-radius:3px;
padding:0 4px;margin:1px -4px}}
.pill{{font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:10px;
text-transform:uppercase;letter-spacing:.04em}}
.pill.hot{{background:#4a1d24;color:#ff9d9d}}.pill.cold{{background:#233b2a;color:#7ee0a0}}
details.reason{{background:#0d1622;border:1px solid #1d2a3d;border-radius:6px;
margin:0 0 10px;padding:6px 10px}}
details.reason>summary{{cursor:pointer;font-size:12px;color:#7fb0e0}}
.reason.none{{color:var(--mut);font-size:12px;font-style:italic;padding:6px 10px;
background:#0d1622;border:1px solid #1d2a3d;border-radius:6px;margin:0 0 10px}}
.rturn{{margin:8px 0;border-top:1px solid #1d2a3d;padding-top:6px}}
.rhead{{font-size:11px;color:var(--mut);text-transform:uppercase;
letter-spacing:.04em}}.ract{{color:#8fbcff;margin-left:8px;text-transform:none;
letter-spacing:0}}
.rbody{{margin-top:4px;color:#b9c4d8;font-size:12px}}
</style></head><body>
<header><h1>Adaptive-trust opponents &mdash; utterance + reasoning traces</h1>
<p>Counterpart now voices the erosion of trust: <span class='u-warn'
style='display:inline'>warning</span> once a betrayal lands,
<span class='u-punish' style='display:inline'>punishment</span> when the grudge
fires, and (forgiving arm) <span class='u-recover'
style='display:inline'>recovery</span> once it cools. Model episodes are
{model} with thinking on; scripted episodes are always-exploit, included because
they reliably drive the full arc. In-env against the training opponent &mdash;
not a result, a legibility check.</p>
<nav>{nav}</nav></header><main>{main}</main></body></html>"""


def build_viewer(recs: List[Dict], out: Path) -> None:
    envs = [e for e in ENVS if any(r["env"] == e for r in recs)]
    nav = " ".join(
        f"<a href='#{e}-{a}'>{TITLE.get(e, e)}/{a}</a>"
        for e in envs for a in ARMS)
    blocks = []
    for e in envs:
        for a in ARMS:
            eps = [r for r in recs if r["env"] == e and r["consequence"] == a]
            if eps:
                blocks.append(render_cell(e, a, eps))
    out.write_text(PAGE.format(model=MODEL, nav=nav, main="".join(blocks)),
                   encoding="utf-8")
    print(f"\nwrote {out}  ({len(recs)} episodes)")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--envs", nargs="+", default=list(ENVS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS),
                    choices=list(core.ADAPTIVE))
    ap.add_argument("--model-seeds", nargs="*", type=int, default=[0, 1])
    ap.add_argument("--scripted-seeds", nargs="*", type=int, default=[0, 1])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--json", default="results/adaptive_sim_traces.json")
    ap.add_argument("--html", default="results/nohole_traces/adaptive_sim.html")
    ap.add_argument("--build-only", action="store_true",
                    help="skip sampling, rebuild the HTML from --json")
    args = ap.parse_args(argv)

    if args.build_only:
        recs = json.loads(Path(args.json).read_text())
    else:
        recs = run(args.envs, args.arms, args.model_seeds, args.scripted_seeds,
                   args.workers)
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(recs, ensure_ascii=False,
                                              default=lambda o: o.__dict__))
        print(f"wrote {args.json}")

    build_viewer(recs, Path(args.html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
