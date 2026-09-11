"""One standalone HTML page: `hole` vs `nohole`, side by side, for every game.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY diff_report.py                          # -> results/armdiff.html
    $PY diff_report.py --envs trust merchant --seeds 2
    $PY diff_report.py --policy honest --out results/armdiff-honest.html

Not the SkyRL trace viewer. That tool lists trajectories and charts rewards; this
is a purpose-made document that answers one question -- *for this game, what
exactly differs between the arm where exploiting is free and the arm where it is
priced?* -- laid out turn by turn, both arms in parallel columns.

The whole design rests on the two arms being the same game up to the moment a
consequence lands. That claim is about text, so it is shown as text: turns the
model saw identically are collapsed, turns that differ are expanded with the
changed words marked. If a game shows a difference before its first decision, the
arms differ in the task and not merely in the price of exploiting, and the page
says so in red at the top.

Rendered entirely server-side -- the diff is computed here, the page carries no
JavaScript. It opens from the filesystem with no server and no build step, and
what is in the file is what you see.

Scripted reference policies, deliberately, not a sampled model: the diff has to
isolate what the ENVIRONMENT does differently, and a sampled policy would differ
between the arms out of noise and drag every later line with it. `--policy
exploit` is the informative one (it is the only policy that trips the consequence
at all); `--policy honest` is the contrast, where most games should be identical
end to end.
"""
from __future__ import annotations

import argparse
import difflib
import html
import sys
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import registry  # noqa: E402

CSS = """
:root{--bg:#0f1216;--panel:#161b22;--panel2:#1c232c;--border:#2b313a;
 --text:#e6edf3;--muted:#8b949e;--good:#3fb950;--bad:#f85149;--warn:#d29922;
 --accent:#4f9dff;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
 font:14px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:22px 26px 14px;border-bottom:1px solid var(--border);
 position:sticky;top:0;background:var(--bg);z-index:5}
h1{margin:0 0 6px;font-size:19px;letter-spacing:.2px}
.sub{color:var(--muted);font-size:12.5px;max-width:105ch}
nav{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}
nav a{text-decoration:none;color:var(--text);border:1px solid var(--border);
 border-radius:999px;padding:3px 10px;font-size:12px;background:var(--panel)}
nav a:hover{border-color:var(--accent)}
nav a .d{color:var(--warn)} nav a .i{color:var(--good)} nav a .x{color:var(--bad)}
main{padding:8px 26px 60px}
table.overview{border-collapse:collapse;margin:18px 0 26px;font-size:12.5px}
table.overview th,table.overview td{border:1px solid var(--border);
 padding:5px 10px;text-align:left}
table.overview th{background:var(--panel2);color:var(--muted);font-weight:600}
table.overview td.num{text-align:right;font-family:var(--mono)}
section{margin:30px 0 0;border:1px solid var(--border);border-radius:10px;
 overflow:hidden;background:var(--panel)}
.shead{padding:11px 14px;background:var(--panel2);
 border-bottom:1px solid var(--border);display:flex;gap:9px;
 align-items:baseline;flex-wrap:wrap}
.shead h2{margin:0;font-size:15px}
.shead .hole{color:var(--muted);font-size:12.5px}
.pill{font-size:11px;border-radius:999px;padding:2px 9px;font-weight:600}
.pill.same{background:rgba(63,185,80,.14);color:var(--good)}
.pill.diff{background:rgba(210,153,34,.14);color:var(--warn)}
.pill.bad{background:rgba(248,81,73,.16);color:var(--bad)}
.pill.cost{background:var(--panel);color:var(--muted);border:1px solid var(--border);
 font-family:var(--mono)}
.meta{padding:8px 14px;color:var(--muted);font-size:12px;
 border-bottom:1px solid var(--border);font-family:var(--mono)}
.cols{display:grid;grid-template-columns:1fr 1fr;background:var(--border);gap:1px;
 position:sticky;top:0}
.colhead{background:var(--panel2);padding:6px 12px;font-size:11.5px;
 text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:700}
.colhead.b{color:var(--accent)}
.turn{border-top:1px solid var(--border)}
.tlabel{padding:6px 14px;font-size:11.5px;color:var(--muted);
 background:var(--panel2);display:flex;gap:8px;align-items:center}
.tlabel .tag{font-weight:700;letter-spacing:.4px;text-transform:uppercase;
 font-size:10.5px}
.tlabel .tag.same{color:var(--good)} .tlabel .tag.diff{color:var(--warn)}
details>summary{cursor:pointer;list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"▸ ";color:var(--muted)}
details[open]>summary::before{content:"▾ "}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border)}
.cell{background:var(--panel);padding:7px 12px;white-space:pre-wrap;
 word-break:break-word;font-family:var(--mono);font-size:12px;margin:0}
.row.same .cell{color:var(--muted)}
.row.diff .cell{background:rgba(210,153,34,.07)}
.role{display:block;color:var(--accent);font-size:10.5px;letter-spacing:.5px;
 text-transform:uppercase;margin:2px 0 3px}
.act .cell{background:#11233b}
.act.diff .cell{background:rgba(210,153,34,.13)}
mark{background:rgba(210,153,34,.45);color:var(--text);border-radius:2px;padding:0 1px}
ins{background:rgba(63,185,80,.22);text-decoration:none;border-radius:2px}
del{background:rgba(248,81,73,.22);text-decoration:none;border-radius:2px}
.legend{color:var(--muted);font-size:12px;margin:14px 0 0}
.warnbox{margin:14px 0;padding:10px 13px;border:1px solid var(--bad);
 border-radius:8px;background:rgba(248,81,73,.08);color:var(--text);font-size:13px}
"""


def esc(s: str) -> str:
    return html.escape(s if s is not None else "")


def _words(a: str, b: str) -> Tuple[str, str]:
    """One changed line pair, with the differing words marked on both sides."""
    at, bt = a.split(" "), b.split(" ")
    left, right = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, at, bt).get_opcodes():
        lx, rx = esc(" ".join(at[i1:i2])), esc(" ".join(bt[j1:j2]))
        if tag == "equal":
            left.append(lx)
            right.append(rx)
        elif tag == "replace":
            left.append(f"<mark>{lx}</mark>")
            right.append(f"<mark>{rx}</mark>")
        elif tag == "delete":
            left.append(f"<del>{lx}</del>")
        elif tag == "insert":
            right.append(f"<ins>{rx}</ins>")
    return " ".join(x for x in left if x), " ".join(x for x in right if x)


def word_marks(a: str, b: str) -> Tuple[str, str]:
    """Escaped HTML for both sides, differences marked, columns kept in step.

    Lines first, then words inside a changed line pair. Going straight to a word
    diff over the whole block lets a match run across a line break and marks the
    newline plus the first word of the next line -- legible enough to read, but it
    smears the highlight over text that did not change. A whole line inserted on
    one side gets a blank on the other, so the two columns stay aligned rather
    than sliding apart for the rest of the turn.
    """
    al, bl = a.split("\n"), b.split("\n")
    left, right = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, al, bl).get_opcodes():
        if tag == "equal":
            left.extend(esc(x) for x in al[i1:i2])
            right.extend(esc(x) for x in bl[j1:j2])
        elif tag == "replace":
            # Pair lines inside the block by SIMILARITY, not by position. A
            # counterpart that adds a sentence ("That is not much of a return")
            # shifts everything after it, and positional pairing then matches the
            # added sentence against the stake line and marks both wholesale --
            # so the one number that actually changed (10 -> 0) never gets
            # highlighted against its own counterpart. Greedy best-match fixes
            # exactly that case, which is the common one here.
            L, R = list(range(i1, i2)), list(range(j1, j2))
            cand = sorted(
                ((difflib.SequenceMatcher(None, al[p], bl[q]).ratio(), p, q)
                 for p in L for q in R), reverse=True)
            pair: Dict[int, int] = {}
            used_r = set()
            for ratio, p, q in cand:
                if ratio < 0.5 or p in pair or q in used_r:
                    continue
                pair[p] = q
                used_r.add(q)
            # Emit in left order; unpaired right lines land before the next
            # paired row so the two columns stay in step.
            pending_r = [q for q in R if q not in used_r]
            for p in L:
                if p in pair:
                    q = pair[p]
                    while pending_r and pending_r[0] < q:
                        left.append("")
                        right.append(f"<ins>{esc(bl[pending_r.pop(0)])}</ins>")
                    lw, rw = _words(al[p], bl[q])
                    left.append(lw)
                    right.append(rw)
                else:
                    left.append(f"<del>{esc(al[p])}</del>")
                    right.append("")
            for q in pending_r:
                left.append("")
                right.append(f"<ins>{esc(bl[q])}</ins>")
        elif tag == "delete":
            for k in range(i1, i2):
                left.append(f"<del>{esc(al[k])}</del>")
                right.append("")
        elif tag == "insert":
            for k in range(j1, j2):
                left.append("")
                right.append(f"<ins>{esc(bl[k])}</ins>")
    return "\n".join(left), "\n".join(right)


def turn_view(rec: Dict) -> List[Dict]:
    """Per turn: the NEW messages the model was shown, and what it wrote.

    Turn-structured rather than a flat line diff, so the page reads as the game:
    "these three turns were identical, then the counterpart reacted."
    """
    out, prev = [], 0
    for t in rec["turns"]:
        msgs = t["messages"]
        out.append({"obs": list(msgs[prev:]), "action": t["action"],
                    "parsed": t.get("parsed")})
        prev = len(msgs)
    return out


def render_turn(i: int, ha: Optional[Dict], na: Optional[Dict]) -> Tuple[str, bool]:
    """One turn as a side-by-side block. Returns (html, differs)."""
    def obs_text(x):
        if x is None:
            return None
        return "\n".join(f"{m['role']}\n{m['content']}" for m in x["obs"])

    ht, nt = obs_text(ha), obs_text(na)
    hact = None if ha is None else ha["action"]
    nact = None if na is None else na["action"]
    obs_differs = ht != nt
    act_differs = hact != nact
    differs = obs_differs or act_differs

    def cell(text: Optional[str], other: Optional[str], mark: bool) -> str:
        if text is None:
            return ('<pre class="cell" style="background:var(--panel2)">'
                    '<em style="color:var(--muted)">— episode ended in this arm —'
                    '</em></pre>')
        if mark and other is not None:
            l, r = word_marks(text, other)
            return f'<pre class="cell">{l}</pre>'
        return f'<pre class="cell">{esc(text)}</pre>'

    # Observation: marked on the side being rendered, so each column shows its own
    # tokens with the differing ones highlighted.
    if obs_differs and ht is not None and nt is not None:
        lh, rh = word_marks(ht, nt)
        obs = (f'<div class="grid"><pre class="cell">{lh}</pre>'
               f'<pre class="cell">{rh}</pre></div>')
    else:
        obs = (f'<div class="grid">{cell(ht, nt, False)}'
               f'{cell(nt, ht, False)}</div>')

    if act_differs and hact is not None and nact is not None:
        la, ra = word_marks(hact, nact)
        act = (f'<div class="grid"><pre class="cell"><span class="role">agent'
               f'</span>{la}</pre><pre class="cell"><span class="role">agent'
               f'</span>{ra}</pre></div>')
    else:
        def acell(x):
            if x is None:
                return ('<pre class="cell" style="background:var(--panel2)"></pre>')
            return (f'<pre class="cell"><span class="role">agent</span>'
                    f'{esc(x)}</pre>')
        act = f'<div class="grid">{acell(hact)}{acell(nact)}</div>'

    tag = "diff" if differs else "same"
    label = (f'<div class="tlabel"><span class="tag {tag}">'
             f'{"differs" if differs else "identical"}</span>'
             f'<span>Turn {i + 1}</span></div>')
    body = (f'<div class="row {tag}">{obs}</div>'
            f'<div class="row act {"diff" if act_differs else "same"}">{act}</div>')
    if differs:
        block = label + body
    elif i == 0:
        # The first turn carries the briefing both arms share (system + brief +
        # round 1) -- the affordance itself, uttered by the environment. It reads
        # identical, but it is the point, so show it open rather than fold it.
        brief_label = label.replace(">Turn 1<", ">Turn 1 · briefing (shared by both arms)<")
        block = (f'<details open><summary>{brief_label}</summary>{body}</details>')
    else:
        # Collapse the identical turns. They are the majority and they are the
        # point -- but expanded they bury the differences under the briefing.
        block = (f'<details><summary>{label}</summary>{body}</details>')
    return f'<div class="turn">{block}</div>', differs


def render_env(env: str, dose: float, seed: int, policy: str) -> Dict:
    spec = registry.get(env)
    recs = {arm: registry.rollout(spec, spec.scripted(policy), consequence=arm,
                                  dose=dose, seed=seed, with_refs=False)
            for arm in ("hole", "nohole")}
    hv, nv = turn_view(recs["hole"]), turn_view(recs["nohole"])

    blocks, first_diff = [], None
    for i in range(max(len(hv), len(nv))):
        h = hv[i] if i < len(hv) else None
        n = nv[i] if i < len(nv) else None
        blk, differs = render_turn(i, h, n)
        blocks.append(blk)
        if differs and first_diff is None:
            first_diff = i + 1

    pre_ok = (recs["hole"]["turns"][0]["messages"]
              == recs["nohole"]["turns"][0]["messages"])
    cost = recs["hole"]["payoff"] - recs["nohole"]["payoff"]

    if not pre_ok:
        pill = '<span class="pill bad">DIFFERS BEFORE THE FIRST DECISION</span>'
    elif first_diff is None:
        pill = '<span class="pill same">identical throughout</span>'
    else:
        pill = f'<span class="pill diff">first differs at turn {first_diff}</span>'

    head = (f'<div class="shead"><h2>{esc(env)}</h2>'
            f'<span class="hole">hole type: {esc(spec.hole_type)} · suite '
            f'{spec.suite}</span>{pill}'
            f'<span class="pill cost">consequence cost {cost:+.2f}</span></div>')
    meta = (f'<div class="meta">dose {dose:g} · seed {seed} · {policy} reference '
            f'policy · opponents: {recs["hole"]["opponent"]} (hole) vs '
            f'{recs["nohole"]["opponent"]} (nohole) · payoff '
            f'{recs["hole"]["payoff"]:.2f} vs {recs["nohole"]["payoff"]:.2f}</div>')
    cols = ('<div class="cols"><div class="colhead">hole — exploiting is free'
            '</div><div class="colhead b">no-hole — exploiting is priced</div></div>')
    body = "".join(blocks)
    anchor = f"{env}-{seed}"
    return {
        "env": env, "seed": seed, "dose": dose, "hole_type": spec.hole_type,
        "anchor": anchor, "first_diff": first_diff, "pre_ok": pre_ok,
        "cost": cost, "turns": max(len(hv), len(nv)),
        "html": f'<section id="{anchor}">{head}{meta}{cols}{body}</section>',
    }


def build_page(items: List[Dict], policy: str) -> str:
    chips = []
    for it in items:
        if not it["pre_ok"]:
            cls, txt = "x", "✗"
        elif it["first_diff"] is None:
            cls, txt = "i", "≡"
        else:
            cls, txt = "d", f"t{it['first_diff']}"
        chips.append(f'<a href="#{it["anchor"]}">{esc(it["env"])} '
                     f'<span class="{cls}">{txt}</span></a>')

    rows = []
    for it in items:
        verdict = ("<b style='color:var(--bad)'>differs pre-decision</b>"
                   if not it["pre_ok"] else
                   "identical throughout" if it["first_diff"] is None
                   else f"turn {it['first_diff']}")
        rows.append(
            f"<tr><td><a href='#{it['anchor']}' style='color:var(--accent)'>"
            f"{esc(it['env'])}</a></td><td>{esc(it['hole_type'])}</td>"
            f"<td class='num'>{it['seed']}</td><td class='num'>{it['turns']}</td>"
            f"<td>{verdict}</td><td class='num'>{it['cost']:+.2f}</td></tr>")

    broken = [it for it in items if not it["pre_ok"]]
    warn = ""
    if broken:
        names = ", ".join(f"{it['env']} (seed {it['seed']})" for it in broken)
        warn = (f'<div class="warnbox"><b>{len(broken)} game(s) differ before the '
                f'first decision:</b> {esc(names)}. In those the two arms are not '
                "the same game — the agent is shown something different before it "
                "has done anything, so a difference in what it learns cannot be "
                "attributed to the consequence alone. This is a bug in the "
                "environment, not a property of the design.</div>")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>hole vs no-hole — side-by-side, per game</title>
<style>{CSS}</style></head><body>
<header>
<h1>hole vs no-hole — what exactly differs, per game</h1>
<div class="sub">Same game, same seed, same deterministic <b>{esc(policy)}</b>
reference policy, played twice: once where exploiting carries no consequence
(<b>hole</b>) and once where it is priced (<b>no-hole</b>). Everything the agent
is shown <b>before it acts</b> must be identical — that is the claim the matched
pair rests on. Identical turns are collapsed; differing turns are expanded with
the changed words marked. Scripted policies, so any difference is the
environment's and not sampling noise.</div>
<nav>{"".join(chips)}</nav>
</header>
<main>
{warn}
<table class="overview"><thead><tr><th>game</th><th>hole type</th><th>seed</th>
<th>turns</th><th>first difference</th><th>consequence cost</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>
<div class="legend">≡ identical throughout — the consequence is priced silently,
so the arms read the same and the whole difference is in the payoff. t<i>N</i> —
the arms first diverge at turn <i>N</i>, which is the counterpart reacting to
what the agent did. ✗ — diverges before the first decision, which is a bug. The
briefing turn (system prompt, game brief, and first round — the shared affordance
both arms present) is shown open by default; the other identical turns are
collapsed.</div>
{"".join(it["html"] for it in items)}
</main></body></html>"""


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=sorted(registry.ENVS))
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--seeds", type=int, default=1,
                   help="how many seeds per game (each gets its own section)")
    ap.add_argument("--policy", default="exploit", choices=("exploit", "honest"))
    ap.add_argument("--out", default="results/armdiff.html")
    ap.add_argument("--open", action="store_true", help="open it in a browser")
    args = ap.parse_args(argv)

    items = []
    for env in args.envs:
        for seed in range(args.seeds):
            it = render_env(env, args.dose, seed, args.policy)
            items.append(it)
            verdict = ("PRE-DECISION DIFF" if not it["pre_ok"] else
                       "identical" if it["first_diff"] is None
                       else f"turn {it['first_diff']}")
            print(f"[report] {env:16s} seed={seed} turns={it['turns']:2d} "
                  f"first-diff={verdict:17s} cost={it['cost']:+.2f}", flush=True)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_page(items, args.policy), encoding="utf-8")
    size = out.stat().st_size / 1024
    print(f"\nwrote {out} ({size:.0f} KB, {len(items)} game sections)")
    print(f"open it:  file://{out.resolve()}")
    broken = [it for it in items if not it["pre_ok"]]
    if broken:
        print("\nPRE-DECISION DIFFERENCES (the arms are not the same game):")
        for it in broken:
            print(f"  {it['env']} seed={it['seed']}")
    if args.open:
        webbrowser.open(f"file://{out.resolve()}")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
