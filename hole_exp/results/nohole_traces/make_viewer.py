"""Build a self-contained HTML viewer of NO-HOLE-arm traces for the five
hand-written cells (ipd, public_goods, ultimatum, trust, dond).

Two sources, labelled per episode:
  * real   -- model episodes pulled from recent training-run trace dumps
              (runs/*/traces/step_*.jsonl), consequence == nohole.
  * scripted -- fresh episodes played here with the cells' own honest/exploit
              reference policies against the no-hole population, so every
              punisher (grim trigger / rejecter / walker / verifier / costly
              punishment) is visible even where no run dumped that cell.

No build step, no framework: writes one index.html to serve with http.server.
"""
from __future__ import annotations

import glob
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent            # hole_exp/
sys.path.insert(0, str(ROOT))

import registry  # noqa: E402

CELLS = ["ipd", "public_goods", "ultimatum", "trust", "dond"]
PER_ENV_DOSE = {"dond": 0.75}        # dond's premium peaks at 0.75 (train_mixed)
SEEDS = (0, 1, 2)                    # rotates the 3 no-hole population members
RUNS = ROOT / "runs"

TITLE = {
    "ipd": "Iterated Prisoner's Dilemma",
    "public_goods": "Public Goods",
    "ultimatum": "Ultimatum",
    "trust": "Trust / Investment",
    "dond": "Deal or No Deal",
}
PUNISH = {
    "ipd": "reciprocators (tft / grim / suspicious_tft): defect back; grim "
           "defects forever after the first betrayal.",
    "public_goods": "conditional punishers: pay 1 to dock you 3 (graded by "
                    "shortfall) and match the group average, draining the pot.",
    "ultimatum": "fair_threshold / noisy_fair / grudge: reject below ~40% -> "
                 "both seats get 0; grudge then demands a full half for a round.",
    "trust": "responsive / responsive_exit / impatient: stake shrinks "
             "quadratically with your return share, investor walks after "
             "cumulative sub-norm returns.",
    "dond": "verifier / auditor / sceptic: check the claim against your own "
            "observable behaviour; credibility erodes and a collapsed "
            "credibility ends the deal at 0.",
}


def dose_for(env: str) -> float:
    return PER_ENV_DOSE.get(env, 1.0)


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

def scripted_episodes():
    out = []
    for env in CELLS:
        spec = registry.get(env)
        dose = dose_for(env)
        for policy in ("exploit", "honest"):
            for seed in SEEDS:
                rec = registry.rollout(spec, spec.scripted(policy),
                                       consequence="nohole", dose=dose, seed=seed)
                rec["_source"] = f"scripted:{policy}"
                out.append(rec)
                print(f"[scripted] {env:13s} {policy:7s} seed={seed} "
                      f"opp={rec['opponent']:16s} payoff={rec['payoff']:+.1f} "
                      f"xr={rec['stats'].get('exploit_rate')}", flush=True)
    return out


def real_episodes():
    """Model no-hole episodes for the five cells from dumped run traces."""
    out = []
    for f in sorted(glob.glob(str(RUNS / "*/traces/step_*.jsonl"))):
        run = f.split("/")[-3]
        step = pathlib.Path(f).stem
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("env") in CELLS and r.get("consequence") == "nohole":
                r["_source"] = f"real:{run}/{step}"
                out.append(r)
    print(f"[real] pulled {len(out)} model no-hole episodes from run dumps",
          flush=True)
    return out


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

# Lines in a game message that ARE the punishment landing. Highlighted red so
# the retaliation is impossible to miss inside the transcript.
PUN_RE = __import__("re").compile(
    r"defected|rejected|\[reject\]|dock(?:ed)? you|pulling my stake|"
    r"not sending anything else|both players \+\$0|would rather we both|"
    r"closer to even|below half|no deal|credibility|walk|struck|"
    r"i'?m not (?:playing|going)|stake back|remain", __import__("re").I)


def transcript(rec):
    """Every message in order + the final action -- the complete play, so an
    intermediate retaliation (grim defecting, a rejection, a stake cut) is
    shown live rather than summarised."""
    blocks = []
    turns = rec.get("turns", [])
    if not turns:
        return blocks
    for m in turns[-1]["messages"]:
        blocks.append((m["role"], m["content"]))
    last = turns[-1]
    tag = ("agent exploit" if last.get("parsed") == "exploit"
           else "agent honest" if last.get("parsed") == "honest" else "agent")
    blocks.append((tag, last.get("action", "")))
    return blocks


def esc(s):
    return html.escape(str(s))


def hi(content):
    """Escape, then wrap punishment lines so they stand out."""
    out = []
    for ln in str(content).split("\n"):
        e = esc(ln)
        if ln.strip() and PUN_RE.search(ln):
            out.append(f"<span class='pun'>{e}</span>")
        else:
            out.append(e)
    return "\n".join(out)


def outcome(rec):
    """A data-derived punishment panel: (punished?, headline, detail-lines).

    Uses the record's structured stats/extras, never text parsing, so it is
    present even where the punishment resolves at close() with no message
    (dond is a single turn: the deal simply collapses to 0)."""
    s = rec.get("stats", {})
    env = rec["env"]
    pay, hon = rec.get("payoff"), rec.get("honest_ref")
    lines = []
    punished = False
    price = ""
    if hon is not None and pay is not None:
        price = f"you got <b>{pay:+.1f}</b>; the honest split here pays {hon:+.1f}"

    if env == "ipd":
        opp = rec.get("opp_decisions") or []
        n = sum(1 for d in opp if d == "defect")
        punished = n > 0
        lines.append(f"opponent (<b>{esc(rec.get('opponent'))}</b>) retaliated: "
                     f"defected in <b>{n}/{len(opp)}</b> rounds after your first "
                     f"betrayal" if punished else "opponent never had to retaliate")
    elif env == "public_goods":
        pp = s.get("punishment_paid") or 0.0
        punished = pp > 0
        lines.append(f"co-players paid to <b>dock you {pp:.0f}</b> points "
                     f"(costly punishment) and matched the group average, "
                     f"draining the pot" if punished
                     else "no punishment triggered")
    elif env == "ultimatum":
        # reject_rate in the record is unreliable (the env's round_history key
        # never matches, so it reads 1.0 even when every offer was accepted).
        # Count the actual rejections the GAME announced instead.
        text = "\n".join(c for _, c in transcript(rec))
        n_rej = text.count("rejected the offer")
        n_off = text.count("offers $") or (n_rej + text.count("accepts"))
        punished = n_rej > 0
        lines.append(f"responder <b>rejected {n_rej}"
                     + (f"/{n_off}" if n_off else "")
                     + "</b> offer(s) \u2192 both seats $0 those rounds"
                     if punished else "every offer accepted")
    elif env == "trust":
        exited = s.get("investor_exited")
        fss = s.get("final_stake_share")
        punished = bool(exited) or (fss is not None and fss < 0.999)
        d = []
        if fss is not None:
            d.append(f"stake cut to <b>{fss*100:.0f}%</b> of the endowment")
        if exited:
            d.append("<b>investor walked</b>")
        lines.append("; ".join(d) if d else "investor kept staking")
    elif env == "dond":
        flagged = s.get("flagged"); walked = s.get("walked")
        nodeal = s.get("no_deal"); cred = s.get("credibility")
        flags = rec.get("flags") or []
        punished = bool(flagged or nodeal or walked)
        parts = []
        if flags:
            parts.append("counterpart caught: " + ", ".join(esc(f) for f in flags))
        if cred is not None:
            parts.append(f"credibility \u2192 <b>{cred:.2f}</b>")
        if nodeal or walked:
            parts.append("<b>deal collapsed \u2192 $0</b>")
        lines.append("; ".join(parts) if parts else "claim believed, deal struck")
    if price:
        lines.append(price)
    return punished, lines


def render_episode(rec):
    s = rec.get("stats", {})
    src = rec.get("_source", "?")
    src_kind = "real" if src.startswith("real") else "scripted"
    policy = src.split(":", 1)[-1] if src_kind == "scripted" else "model"
    punished, olines = outcome(rec)

    meta = [f"opponent <b>{esc(rec.get('opponent'))}</b>",
            f"payoff <b>{rec.get('payoff'):+.1f}</b>"]
    if s.get("exploit_rate") is not None:
        meta.append(f"exploit {s['exploit_rate']:.2f}")

    badge = ("<span class='pill punished'>PUNISHED</span>" if punished
             else "<span class='pill clean'>no punishment</span>")
    panel = (f"<div class='outcome {'p' if punished else 'c'}'>"
             f"<div class='ohead'>{badge} &nbsp;how the punishment lands</div>"
             + "".join(f"<div class='oline'>&bull; {l}</div>" for l in olines)
             + "</div>")

    rows = []
    for role, content in transcript(rec):
        cls = "system" if role == "system" else (
            "agent" if role.startswith("agent") else "game")
        extra = "exploit" if role == "agent exploit" else (
            "honest" if role == "agent honest" else "")
        label = {"agent exploit": "agent \u00b7 EXPLOIT",
                 "agent honest": "agent \u00b7 honest",
                 "agent": "agent", "user": "game", "system": "system"}.get(
                     role, role)
        body = hi(content) if cls == "game" else esc(content)
        rows.append(f"<div class='msg {cls}'><span class='role {extra}'>"
                    f"{esc(label)}</span><pre>{body}</pre></div>")

    summary = (f"<span class='src {src_kind}'>{esc(policy)}</span> {badge} "
               "&middot; " + " &middot; ".join(meta))
    is_open = " open" if (punished and src_kind == "scripted"
                          and policy == "exploit") else ""
    return (f"<details class='ep'{is_open}><summary>{summary}</summary>"
            f"<div class='body'>{panel}{''.join(rows)}</div></details>")


def render_cell(env, eps):
    # Punished exploit episodes first (that is what the user came to see),
    # then the rest; scripted before honest-only within each.
    def key(r):
        pun, _ = outcome(r)
        pol = r["_source"].split(":", 1)[-1]
        return (0 if pun else 1, 0 if pol == "exploit" else 1,
                r.get("opponent") or "")
    eps = sorted(eps, key=key)
    n_real = sum(1 for r in eps if r["_source"].startswith("real"))
    n_pun = sum(1 for r in eps if outcome(r)[0])
    body = "".join(render_episode(r) for r in eps)
    return (f"<section id='{env}'><h2>{esc(TITLE[env])} "
            f"<span class='envid'>{env}</span></h2>"
            f"<p class='punish'><b>No-hole opponent:</b> {esc(PUNISH[env])}</p>"
            f"<p class='count'>{len(eps)} episodes ({n_real} real, "
            f"{len(eps)-n_real} scripted) &middot; "
            f"<b>{n_pun} show the punishment landing</b></p>{body}</section>")


PAGE = """<!doctype html><html><head><meta charset='utf-8'>
<title>No-hole opponent traces</title><style>
:root{{--bg:#0f1115;--card:#171a21;--fg:#e6e6e6;--mut:#8b93a7;--acc:#6ea8fe;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{padding:18px 24px;border-bottom:1px solid #262a33;position:sticky;top:0;
background:var(--bg);z-index:5}}
header h1{{margin:0 0 6px;font-size:18px}}
nav a{{color:var(--acc);margin-right:14px;text-decoration:none;font-size:13px}}
main{{max-width:1100px;margin:0 auto;padding:0 24px 80px}}
section{{margin-top:34px}}h2{{font-size:16px;border-bottom:1px solid #262a33;
padding-bottom:6px}}.envid{{color:var(--mut);font-weight:400;font-size:13px}}
.punish{{color:var(--mut);margin:6px 0}}.count{{color:var(--mut);font-size:12px;
margin:2px 0 12px}}
details.ep{{background:var(--card);border:1px solid #262a33;border-radius:8px;
margin:8px 0;padding:6px 12px}}
details.ep>summary{{cursor:pointer;font-size:12.5px;color:#cfd6e4}}
.src{{font-weight:700;padding:1px 6px;border-radius:4px;font-size:11px}}
.src.real{{background:#243b2a;color:#7ee0a0}}
.src.scripted{{background:#2a2f3d;color:#9fb0d0}}
.body{{margin-top:10px}}
.msg{{margin:7px 0;padding:8px 10px;border-radius:6px;background:#10131a}}
.msg.system{{opacity:.6}}
.msg.game{{border-left:3px solid #3a4152}}.msg.agent{{border-left:3px solid #4a6}}
.role{{display:inline-block;font-size:11px;color:var(--mut);
text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}}
.role.exploit{{color:#ff8f8f}}.role.honest{{color:#7ee0a0}}
pre{{margin:0;white-space:pre-wrap;word-break:break-word;font:12.5px/1.5
ui-monospace,SFMono-Regular,Menlo,monospace}}
.pun{{display:block;background:#3a1d22;color:#ffb4b4;border-radius:3px;
padding:0 4px;margin:1px -4px}}
.pill{{font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:10px;
text-transform:uppercase;letter-spacing:.04em}}
.pill.punished{{background:#4a1d24;color:#ff9d9d}}
.pill.clean{{background:#233b2a;color:#7ee0a0}}
.outcome{{border-radius:8px;padding:10px 12px;margin:2px 0 12px;
border:1px solid #2a2f3d;background:#12151c}}
.outcome.p{{border-color:#5a2a30;background:#1c1418}}
.ohead{{font-size:12px;color:var(--mut);text-transform:uppercase;
letter-spacing:.05em;margin-bottom:6px}}
.oline{{font-size:13px;margin:2px 0}}
</style></head><body>
<header><h1>No-hole arm &mdash; opponent behaviour traces</h1>
<nav>{nav}</nav></header><main>{main}</main></body></html>"""


def main():
    eps = real_episodes() + scripted_episodes()
    by_env = {e: [r for r in eps if r["env"] == e] for e in CELLS}
    nav = " ".join(f"<a href='#{e}'>{TITLE[e]}</a>" for e in CELLS)
    main_html = "".join(render_cell(e, by_env[e]) for e in CELLS)
    out = HERE / "index.html"
    out.write_text(PAGE.format(nav=nav, main=main_html), encoding="utf-8")
    tot = sum(len(v) for v in by_env.values())
    print(f"\nwrote {out}  ({tot} episodes across {len(CELLS)} cells)")


if __name__ == "__main__":
    main()
