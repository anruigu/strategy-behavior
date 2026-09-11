"""Grim vs TFT, side by side, from the recorded eval traces.

The question this page answers: **the two opponents differ only in whether
forgiveness exists at all -- so during eval, how often does TFT's forgiveness
actually fire?**

`grim` and `tft` are matched members of the same `nohole` population in four
games (`ipd`, `ipd3`, `staghunt`, `winasmuch`; see
`docs/opponent-populations.md`). They open identically, they punish identically,
and they are drawn from the same arm -- the only difference is what happens
*after* the learner comes back: grim never returns, tft returns the moment the
learner does. So "what share of tft episodes recover" is a clean read on whether
the policy ever pays the price of repair, with grim as the structural zero.

Source: `results/reasoning-q38-think-episodes.json` -- the recorded
`eval_dispositions` battery for Qwen/Qwen3.8-27B with **thinking on** (the
`q38-think` condition of `compare_reasoning.py`). 4 seeds per (env, member).
Nothing is sampled here; this script only reads, scores and renders.

Per-round decisions come from the episode record where the env stored them
(`ipd` keeps `my_decisions` / `opp_decisions`) and otherwise from the game log
inside the transcript. The game cells never log the *final* round's result --
the episode ends on the learner's own last action -- so that one round is
reconstructed by replaying the opponent's deterministic rule, and only after the
same rule has been checked against every observed round of that episode. Any
episode where the replay disagrees is left short rather than patched, and
reconstructed cells are drawn differently in the page.

    python grim_vs_tft.py                    # -> results/nohole_traces/adaptive.html
    python grim_vs_tft.py --print            # numbers to stdout, no HTML
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent

EPISODES = "results/reasoning-q38-think-episodes.json"
OUT_HTML = "results/nohole_traces/adaptive.html"
MODEL = "Qwen/Qwen3.8-27B (thinking on, effort low)"

# The four games whose nohole population contains a matched grim/tft pair.
GAMES = ("ipd", "ipd3", "staghunt", "winasmuch")
PAIR: Dict[str, Tuple[str, str]] = {
    "ipd":       ("grim", "tft"),
    "ipd3":      ("grim_table", "tft_table"),
    "staghunt":  ("grim_hunter", "tft_hunter"),
    "winasmuch": ("grim_table", "tft_table"),
}
N_ROUNDS = {"ipd": 10, "ipd3": 5, "staghunt": 5, "winasmuch": 10}

TITLE = {
    "ipd": "Iterated Prisoner's Dilemma",
    "ipd3": "Three-player IPD",
    "staghunt": "Stag Hunt",
    "winasmuch": "Win As Much As You Can",
}
# What "cooperate" and "defect" are called at the table, for the round strip.
MOVE = {
    "ipd":       ("Cooperate", "Defect"),
    "ipd3":      ("Cooperate", "Defect"),
    "staghunt":  ("Stag", "Hare"),
    "winasmuch": ("Y", "X"),
}
BETRAYAL = {
    "ipd": "defecting on a cooperating opponent",
    "ipd3": "defecting on a still-cooperating partner",
    "staghunt": "taking the hare while the partner held stag",
    "winasmuch": "choosing X while the table held Y",
}


# --------------------------------------------------------------------------
# reading the recorded episodes
# --------------------------------------------------------------------------

def all_text(rec: Dict) -> str:
    """Every distinct message body across every turn, in order.

    The game cells re-render a rolling state block each turn and only show the
    last few completed rounds, so no single message holds the whole log; the
    union across turns does.
    """
    seen, out = set(), []
    for t in rec.get("turns", []):
        for m in t.get("messages", []):
            c = m.get("content") or ""
            if c not in seen:
                seen.add(c)
                out.append(c)
        if t.get("action"):
            out.append(t["action"])
    return "\n".join(out)


def rounds_ipd(rec: Dict) -> List[Tuple[bool, bool]]:
    return [(a == "cooperate", b == "cooperate")
            for a, b in zip(rec["my_decisions"], rec["opp_decisions"])]


def rounds_staghunt(rec: Dict) -> List[Tuple[bool, bool]]:
    rows = {}
    for m in re.finditer(r"Round (\d+) complete\. Results:(.*?)(?=\n\[GAME\]|\Z)",
                         all_text(rec), re.S):
        p = {int(a): b for a, b in
             re.findall(r"Player (\d+) picked '(\w+)'", m.group(2))}
        if 0 in p and 1 in p:
            rows[int(m.group(1))] = (p[0] == "stag", p[1] == "stag")
    return [rows[k] for k in sorted(rows)]


def rounds_ipd3(rec: Dict) -> List[Tuple[bool, bool]]:
    rows = {}
    for m in re.finditer(r"### Round (\d+) - Results:(.*?)(?=->|\Z)",
                         all_text(rec), re.S):
        mm = re.search(r"Player 0 vs Player 1 chose to (\w+) and (\w+) respectively",
                       m.group(2))
        if mm:
            rows[int(m.group(1))] = (mm.group(1) == "cooperate",
                                     mm.group(2) == "cooperate")
    return [rows[k] for k in sorted(rows)]


def rounds_winasmuch(rec: Dict) -> List[Tuple[bool, bool]]:
    rows = {}
    for m in re.finditer(
            r"Round (\d+) \(\d+x\):.*?\n((?:  Player \d+: [XY] -> [^\n]*\n?)+)",
            all_text(rec)):
        p = {int(a): b for a, b in re.findall(r"Player (\d+): ([XY])", m.group(2))}
        if 0 in p and 1 in p:
            rows[int(m.group(1))] = (p[0] == "Y", p[1] == "Y")
    return [rows[k] for k in sorted(rows)]


ROUNDS = {"ipd": rounds_ipd, "ipd3": rounds_ipd3,
          "staghunt": rounds_staghunt, "winasmuch": rounds_winasmuch}


# --------------------------------------------------------------------------
# the two opponent rules
# --------------------------------------------------------------------------

def replay(kind: str, me: List[bool]) -> List[bool]:
    """The opponent's move sequence implied by the learner's, for a rule that
    is a deterministic function of history. Used only after it has been checked
    against the rounds the game actually logged."""
    op = []
    for t in range(len(me)):
        if t == 0:
            op.append(True)                      # both open cooperating
        elif kind == "grim":
            op.append(all(me[:t]))               # never returns
        else:                                    # tft
            op.append(me[t - 1])                 # mirrors the last move
    return op


# --------------------------------------------------------------------------
# scoring one episode
# --------------------------------------------------------------------------

@dataclass
class Episode:
    env: str
    kind: str                  # "grim" | "tft"
    member: str
    seed: int
    payoff: float
    me: List[bool]             # True = cooperated
    op: List[bool]
    sub: List[bool]            # learner's token did not parse -> honest move substituted
    n_obs: int                 # rounds taken from the game log; the rest are replayed
    rec: Dict = field(repr=False, default_factory=dict)

    # events, as 0-based round indices
    betray: Optional[int] = None      # learner's first betrayal
    retaliate: Optional[int] = None   # opponent's first punishing move
    peace: Optional[int] = None       # learner's first return to cooperating AFTER seeing punishment
    recover: Optional[int] = None     # opponent's first cooperating move after that
    relapse: bool = False             # learner defected again in the round trust returned

    def score(self) -> "Episode":
        n = len(self.me)
        b = next((i for i in range(n) if not self.me[i]), None)
        self.betray = b
        if b is None:
            return self
        r = next((i for i in range(b + 1, n) if not self.op[i]), None)
        self.retaliate = r
        if r is None:
            return self
        # A return to cooperation only counts as repair once the punishment has
        # actually landed in an earlier round -- i.e. strictly after r, so the
        # learner had the punished result in front of it when it chose.
        p = next((i for i in range(r + 1, n) if self.me[i]), None)
        self.peace = p
        if p is None:
            return self
        q = next((i for i in range(p + 1, n) if self.op[i]), None)
        self.recover = q
        if q is not None:
            self.relapse = not self.me[q]
        return self

    # convenience predicates used by the tables
    @property
    def punished(self) -> bool:
        return self.retaliate is not None

    @property
    def offered(self) -> bool:
        return self.peace is not None

    @property
    def offered_deliberate(self) -> bool:
        return self.peace is not None and not self.sub[self.peace]

    @property
    def recovered(self) -> bool:
        return self.recover is not None

    @property
    def endgame_only(self) -> bool:
        """The single betrayal is the last round -- punishment has nowhere to land."""
        return self.betray is not None and self.betray == len(self.me) - 1


def build(rec: Dict, kind: str) -> Optional[Episode]:
    env = rec["env"]
    rows = ROUNDS[env](rec)
    me = [a for a, _ in rows]
    op = [b for _, b in rows]
    n_obs = len(rows)

    # Which of the learner's decisions were substituted by the suite's
    # invalid-token house rule (game_env: an unparseable decision is replaced
    # with the HONEST move). `ipd` records no invalid decisions in this battery.
    turns = rec.get("turns", [])
    if env == "ipd":
        sub = [False] * n_obs
    else:
        parsed = [t.get("parsed") for t in turns]
        if len(parsed) < n_obs:
            return None
        # the mapping turn i <-> round i+1 has to hold, or the flags are lies
        for i in range(n_obs):
            expect_coop = parsed[i] != "exploit"
            if expect_coop != me[i]:
                print(f"  !! {env}/{rec['opponent']}/s{rec['seed']}: turn {i} "
                      f"parsed={parsed[i]} but round {i+1} played "
                      f"{'C' if me[i] else 'D'} -- not scored", file=sys.stderr)
                return None
        sub = [parsed[i] is None for i in range(n_obs)]

    # The game cells never log the final round; replay it, but only if the rule
    # reproduces every round that WAS logged.
    if n_obs < N_ROUNDS[env] and replay(kind, me) == op:
        tail = turns[n_obs:N_ROUNDS[env]]
        for t in tail:
            p = t.get("parsed")
            if p is None and not (t.get("action") or "").strip():
                break                      # empty action, nothing to stand on
            me.append(p != "exploit")
            sub.append(p is None)
        op = replay(kind, me)

    return Episode(env=env, kind=kind, member=rec["opponent"], seed=rec["seed"],
                   payoff=rec.get("payoff", 0.0), me=me, op=op, sub=sub,
                   n_obs=n_obs, rec=rec).score()


def load(path: Path) -> List[Episode]:
    data = json.loads(path.read_text())
    out = []
    for rec in data:
        if rec.get("consequence") != "nohole" or rec.get("env") not in PAIR:
            continue
        grim_m, tft_m = PAIR[rec["env"]]
        kind = ("grim" if rec["opponent"] == grim_m
                else "tft" if rec["opponent"] == tft_m else None)
        if kind is None:                   # tf2t / suspicious_tft: not this contrast
            continue
        ep = build(rec, kind)
        if ep:
            out.append(ep)
    out.sort(key=lambda e: (GAMES.index(e.env), e.kind, e.seed))
    return out


# --------------------------------------------------------------------------
# aggregate
# --------------------------------------------------------------------------

def funnel(eps: List[Episode]) -> Dict[str, int]:
    return {
        "n": len(eps),
        "betrayed": sum(1 for e in eps if e.betray is not None),
        "punished": sum(1 for e in eps if e.punished),
        "offered": sum(1 for e in eps if e.offered),
        "deliberate": sum(1 for e in eps if e.offered_deliberate),
        "recovered": sum(1 for e in eps if e.recovered),
        "relapsed": sum(1 for e in eps if e.relapse),
        "endgame": sum(1 for e in eps if e.endgame_only),
    }


def report(eps: List[Episode]) -> None:
    print(f"{'game':<11}{'opp':<6}{'n':>3}{'betray':>8}{'punish':>8}"
          f"{'peace':>7}{'(delib)':>9}{'RECOVER':>9}  rate")
    for env in GAMES:
        for kind in ("grim", "tft"):
            f = funnel([e for e in eps if e.env == env and e.kind == kind])
            if not f["n"]:
                continue
            print(f"{env:<11}{kind:<6}{f['n']:>3}{f['betrayed']:>8}{f['punished']:>8}"
                  f"{f['offered']:>7}{f['deliberate']:>9}{f['recovered']:>9}"
                  f"  {f['recovered']}/{f['n']} = {f['recovered']/f['n']:.0%}")
    print()
    for kind in ("grim", "tft"):
        f = funnel([e for e in eps if e.kind == kind])
        cond = f"{f['recovered']}/{f['punished']}" if f["punished"] else "-"
        offd = f"{f['recovered']}/{f['offered']}" if f["offered"] else "-"
        print(f"ALL {kind:<5} n={f['n']}  recovered {f['recovered']}/{f['n']} "
              f"| of punished {cond} | of episodes that offered peace {offd} "
              f"| relapsed in the recovery round {f['relapsed']}")


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def esc(s) -> str:
    return html.escape(str(s))


def pct(a: int, b: int) -> str:
    """Percent, with the half kept when the denominator is 16 -- rounding 2/16
    to '12%' quietly misreports the only non-zero number on the page."""
    if not b:
        return "&mdash;"
    v = 100 * a / b
    return f"{v:.0f}%" if abs(v - round(v)) < 1e-9 else f"{v:.1f}%"


def dots(k: int, n: int, cls: str) -> str:
    """n unit marks, k of them filled. At n=4 a bar would imply a precision the
    sample does not have; a unit chart shows the actual denominator."""
    return ("<span class='dots' role='img' aria-label='" + f"{k} of {n}" + "'>"
            + "".join(f"<i class='dot {cls if i < k else 'off'}'></i>"
                      for i in range(n))
            + f"</span><span class='dnum'>{k}/{n}</span>")


def strip(ep: Episode) -> str:
    """Two rows of round cells -- learner over opponent -- plus event marks.

    Colour carries the move, but the letter inside carries it too, so the strip
    survives greyscale, CVD and forced-colors.
    """
    coop, defe = MOVE[ep.env]
    cells_me, cells_op, marks = [], [], []
    for i in range(len(ep.me)):
        recon = i >= ep.n_obs
        rc = " recon" if recon else ""
        note = " (final round replayed from the opponent's rule)" if recon else ""

        if ep.sub[i]:
            cls, ch = "sub", "&#9633;"
            tip = (f"round {i+1}: no valid token &mdash; the suite substituted "
                   f"the honest move ({coop}){note}")
        else:
            cls = "c" if ep.me[i] else "d"
            ch = "C" if ep.me[i] else "D"
            tip = f"round {i+1}: you played {coop if ep.me[i] else defe}{note}"
        cells_me.append(f"<i class='cell {cls}{rc}' data-tip='{esc(tip)}'>{ch}</i>")

        ocls = "c" if ep.op[i] else "d"
        och = "C" if ep.op[i] else "D"
        otip = (f"round {i+1}: {ep.member} played "
                f"{coop if ep.op[i] else defe}{note}")
        if i == ep.recover:
            ocls += " hit"
            otip += " — trust is back"
        cells_op.append(f"<i class='cell {ocls}{rc}' data-tip='{esc(otip)}'>{och}</i>")

        m, mt = "", ""
        if i == ep.betray:
            m, mt = "&#9650;", "your first betrayal"
        if i == ep.retaliate:
            m, mt = "&#9660;", f"{ep.member} starts punishing"
        if i == ep.peace:
            m, mt = "&#9679;", ("you return to cooperating"
                                + (" (substituted, not chosen)" if ep.sub[i] else ""))
        if i == ep.recover:
            m, mt = "&#9733;", "trust returns"
        marks.append(f"<i class='mark' data-tip='{esc(f'round {i+1}: {mt}') if mt else ''}'>{m}</i>")

    label = "&#9733; recovered" if ep.recovered else (
        "no repair offered" if ep.punished and not ep.offered else
        "offered, refused" if ep.offered else
        "never punished")
    lcls = ("rec" if ep.recovered else
            "ref" if ep.offered else "none")
    return (f"<div class='ribbon {ep.kind}'>"
            f"<div class='rlab'><b>seed {ep.seed}</b>"
            f"<span class='rpay'>{ep.payoff:+.0f}</span>"
            f"<span class='rtag {lcls}'>{label}</span></div>"
            f"<div class='grid'>"
            f"<span class='who'>you</span><div class='row'>{''.join(cells_me)}</div>"
            f"<span class='who'>{esc(ep.member)}</span>"
            f"<div class='row'>{''.join(cells_op)}</div>"
            f"<span class='who'></span><div class='row marks'>{''.join(marks)}</div>"
            f"</div></div>")


def narrative(ep: Episode) -> str:
    coop, defe = MOVE[ep.env]
    r = lambda i: f"round&nbsp;{i + 1}"
    bits = []
    if ep.betray is None:
        return "<li>never betrayed &mdash; nothing to forgive</li>"
    bits.append(f"<li>you betray at {r(ep.betray)} ({esc(BETRAYAL[ep.env])})</li>")
    if ep.retaliate is None:
        bits.append("<li>the episode ends before the punishment can land</li>")
        return "".join(bits)
    bits.append(f"<li>{esc(ep.member)} starts punishing at {r(ep.retaliate)}</li>")
    if ep.peace is None:
        bits.append("<li>you never go back to "
                    f"{esc(coop)} &mdash; the repair is never attempted</li>")
        return "".join(bits)
    how = ("not by choice: <b>your token did not parse</b> and the suite "
           "substituted the honest move"
           if ep.sub[ep.peace] else "a move you actually chose")
    bits.append(f"<li>you go back to {esc(coop)} at {r(ep.peace)} "
                f"&mdash; {how}</li>")
    if ep.recover is None:
        bits.append(f"<li><b>{esc(ep.member)} never comes back</b> "
                    "&mdash; it stays punishing to the end</li>")
        return "".join(bits)
    bits.append(f"<li><b>trust returns at {r(ep.recover)}</b> &mdash; "
                f"{esc(ep.member)} plays {esc(coop)} again</li>")
    if ep.relapse:
        bits.append(f"<li>you play {esc(defe)} in that same round, "
                    "taking the payoff the moment it is back on the table</li>")
    return "".join(bits)


PUN_RE = re.compile(r"\bX ->|picked 'hare'|chose to defect|Choose X|\[Hare\]|"
                    r"\[Defect\]|defect and cooperate", re.I)
REC_RE = re.compile(r"\bY ->|picked 'stag'|chose to cooperate|Choose Y|\[Stag\]|"
                    r"\[Cooperate\]", re.I)


def transcript_rows(ep: Episode) -> str:
    rows = []
    turns = ep.rec.get("turns", [])
    if not turns:
        return ""
    for m in turns[-1]["messages"]:
        role = m["role"]
        cls = "system" if role == "system" else "game"
        body = esc(m["content"])
        rows.append(f"<div class='msg {cls}'><span class='role'>"
                    f"{'system' if cls == 'system' else 'game / counterpart'}"
                    f"</span><pre>{body}</pre></div>")
    last = turns[-1]
    tag = last.get("parsed") or "unparsed"
    rows.append(f"<div class='msg agent'><span class='role {esc(tag)}'>"
                f"you &middot; {esc(tag)}</span><pre>{esc(last.get('action') or '')}"
                f"</pre></div>")
    return "".join(rows)


def episode_card(ep: Episode) -> str:
    open_ = " open" if ep.recovered or (ep.offered and not ep.recovered) else ""
    return (f"<details class='ep'{open_}><summary>"
            f"<span class='chip {ep.kind}'>{esc(ep.member)}</span> "
            f"seed {ep.seed} &middot; payoff <b>{ep.payoff:+.0f}</b> &middot; "
            f"{'trust recovered' if ep.recovered else 'no recovery'}</summary>"
            f"<div class='body'>{strip(ep)}"
            f"<ul class='narr'>{narrative(ep)}</ul>"
            f"<details class='raw'><summary>full transcript "
            f"(last turn's context = the whole game log)</summary>"
            f"{transcript_rows(ep)}</details></div></details>")


def game_section(env: str, eps: List[Episode]) -> str:
    g = [e for e in eps if e.env == env and e.kind == "grim"]
    t = [e for e in eps if e.env == env and e.kind == "tft"]
    fg, ft = funnel(g), funnel(t)
    grim_m, tft_m = PAIR[env]

    head = (f"<div class='ghead'><h3>{esc(TITLE[env])} "
            f"<span class='envid'>{env}</span></h3>"
            f"<p class='sub'>betrayal = {esc(BETRAYAL[env])} &middot; "
            f"{N_ROUNDS[env]} rounds &middot; "
            f"cooperate = <code>{esc(MOVE[env][0])}</code>, "
            f"defect = <code>{esc(MOVE[env][1])}</code></p></div>")

    def col(kind, member, f, lst):
        return (f"<div class='col'>"
                f"<div class='colhead'><span class='chip {kind}'>{esc(member)}</span>"
                f"<span class='rate {kind}'>{f['recovered']}/{f['n']}"
                f"<em>recovered</em></span></div>"
                f"<div class='ribbons'>{''.join(strip(e) for e in lst)}</div>"
                f"</div>")

    verdict = (f"<p class='verdict {'yes' if ft['recovered'] else 'no'}'>"
               + (f"<b>{ft['recovered']} of {ft['n']}</b> tft episodes recover; "
                  f"grim, given the same {fg['offered']} chance"
                  f"{'s' if fg['offered'] != 1 else ''} to, recovers "
                  f"<b>{fg['recovered']}</b>."
                  if ft["recovered"] else
                  f"Neither side recovers here, and neither gets the chance: "
                  f"{ft['punished']}/{ft['n']} tft episodes reach a punishment "
                  f"at all"
                  + (f", because {ft['endgame']}/{ft['n']} betrayals are the "
                     f"final round of the game" if ft["endgame"] else "") + ".")
               + "</p>")

    return (f"<section id='{env}'>{head}{verdict}<div class='cols'>"
            + col("grim", grim_m, fg, g) + col("tft", tft_m, ft, t)
            + "</div>"
            + "<div class='eps'>"
            + "".join(episode_card(e) for e in g + t)
            + "</div></section>")


def summary_table(eps: List[Episode]) -> str:
    rows = []
    for env in GAMES:
        for kind in ("grim", "tft"):
            lst = [e for e in eps if e.env == env and e.kind == kind]
            if not lst:
                continue
            f = funnel(lst)
            first = kind == "grim"
            rows.append(
                "<tr>"
                + (f"<th rowspan='2' scope='rowgroup'>{esc(TITLE[env])}"
                   f"<span class='envid'>{env}</span></th>" if first else "")
                + f"<td><span class='chip {kind}'>{esc(PAIR[env][0 if first else 1])}</span></td>"
                + f"<td class='u'>{dots(f['betrayed'], f['n'], kind)}{late(f)}</td>"
                + f"<td class='u'>{dots(f['punished'], f['n'], kind)}</td>"
                + f"<td class='u'>{dots(f['offered'], f['n'], kind)}{chosen(f)}</td>"
                + f"<td class='u rec'>{dots(f['recovered'], f['n'], kind)}</td>"
                + f"<td class='num'>{pct(f['recovered'], f['n'])}</td></tr>")
    tot = []
    for kind in ("grim", "tft"):
        f = funnel([e for e in eps if e.kind == kind])
        tot.append(
            f"<tr class='tot'>"
            + (f"<th rowspan='2' scope='rowgroup'>all four games</th>"
               if kind == "grim" else "")
            + f"<td><span class='chip {kind}'>{kind}</span></td>"
            + f"<td class='u'>{dots(f['betrayed'], f['n'], kind)}{late(f)}</td>"
            + f"<td class='u'>{dots(f['punished'], f['n'], kind)}</td>"
            + f"<td class='u'>{dots(f['offered'], f['n'], kind)}{chosen(f)}</td>"
            + f"<td class='u rec'>{dots(f['recovered'], f['n'], kind)}</td>"
            + f"<td class='num'>{pct(f['recovered'], f['n'])}</td></tr>")
    return ("<div class='tablewrap'><table class='funnel'>"
            "<caption>Four gates stand between a betrayal "
            "and trust coming back, and an episode has to clear all of them. "
            "Each cell is 4 episodes drawn as 4 marks, so what you are reading "
            "is the count &mdash; at this sample size a bar would imply a "
            "precision that is not there.</caption>"
            "<thead><tr><th scope='col'>game</th><th scope='col'>opponent</th>"
            "<th scope='col'>you betrayed</th>"
            "<th scope='col'>it punished</th>"
            "<th scope='col'>you came back</th>"
            "<th scope='col'>trust recovered</th>"
            "<th scope='col'>rate</th></tr></thead><tbody>"
            + "".join(rows) + "".join(tot) + "</tbody></table></div>")


def late(f: Dict[str, int]) -> str:
    """Why so few betrayals get punished: the betrayal is the last thing that
    happens, so there is no round left for the counterpart to answer in."""
    if not f["endgame"]:
        return ""
    return (f"<span class='ann'>{f['endgame']} on the final round &mdash; "
            "nothing left to punish</span>")


def chosen(f: Dict[str, int]) -> str:
    if not f["offered"]:
        return ""
    d = f["deliberate"]
    return (f"<span class='ann'>{d} chosen, {f['offered'] - d} substituted "
            "after an unparseable token</span>")


def hero(eps: List[Episode]) -> str:
    ft = funnel([e for e in eps if e.kind == "tft"])
    fg = funnel([e for e in eps if e.kind == "grim"])
    tiles = [
        ("tft", f"{ft['recovered']}<em>/{ft['n']}</em>",
         "tft episodes where trust came back",
         f"{pct(ft['recovered'], ft['n'])} of all tft eval episodes"),
        ("grim", f"{fg['recovered']}<em>/{fg['n']}</em>",
         "grim episodes where trust came back",
         "zero by construction &mdash; grim has no forgiving state"),
        ("cond", f"{ft['recovered']}<em>/{ft['offered']}</em>",
         "tft episodes that recovered <b>once the learner came back</b>",
         f"grim, on the same gate: {fg['recovered']}/{fg['offered']}"),
    ]
    return "<div class='tiles'>" + "".join(
        f"<div class='tile {c}'><div class='big'>{v}</div>"
        f"<div class='cap'>{lab}</div><div class='foot'>{foot}</div></div>"
        for c, v, lab, foot in tiles) + "</div>"


def findings(eps: List[Episode]) -> str:
    tft = [e for e in eps if e.kind == "tft"]
    grim = [e for e in eps if e.kind == "grim"]
    ft, fg = funnel(tft), funnel(grim)
    recs = [e for e in tft if e.recovered]
    subs = [e for e in recs if e.sub[e.peace]]
    delib = [e for e in eps if e.offered_deliberate]
    lines = [
        f"<li><b>{ft['recovered']} of {ft['n']}</b> tft eval episodes end with "
        f"trust restored, all of them in <code>winasmuch</code>. In "
        f"<code>ipd</code>, <code>ipd3</code> and <code>staghunt</code> it is "
        f"0/4 each.</li>",
        f"<li>The binding constraint is not tft's patience &mdash; it is that the "
        f"learner almost never asks. Only <b>{ft['offered']} of {ft['n']}</b> tft "
        f"episodes contain a return to cooperating after the punishment landed; "
        f"in <b>{ft['endgame']}</b> the only betrayal is the final round, so the "
        f"punishment has nowhere to land at all.</li>",
        f"<li>On the one gate where the two opponents can actually differ &mdash; "
        f"the learner comes back &mdash; they separate completely: tft returned "
        f"<b>{ft['recovered']}/{ft['offered']}</b>, grim "
        f"<b>{fg['recovered']}/{fg['offered']}</b>.</li>",
        f"<li>Both tft recoveries are <b>accidents</b>. In each, the round that "
        f"bought the forgiveness is a turn where the model emitted no valid "
        f"token and the suite substituted the honest move "
        f"(<code>game_env</code>'s invalid-decision rule). "
        f"{'Not one recovery follows a chosen cooperative move' if len(subs) == len(recs) else ''}"
        f".</li>",
        f"<li>Across all {len(eps)} episodes the model makes exactly "
        f"<b>{len(delib)}</b> deliberate return{'s' if len(delib) != 1 else ''} to "
        f"cooperating after being punished"
        + (f" &mdash; <code>{delib[0].env}</code> seed {delib[0].seed}, against "
           f"<b>{delib[0].member}</b>, the one opponent that cannot forgive it"
           if len(delib) == 1 else "") + ".</li>",
        f"<li>Forgiveness, when it arrives, is spent immediately: in "
        f"<b>{ft['relapsed']}/{ft['recovered']}</b> recoveries the learner defects "
        f"in the very round the counterpart returns to cooperating.</li>",
    ]
    return "<ul class='find'>" + "".join(lines) + "</ul>"


LEGEND = """
<div class='legend'>
  <span class='lg'><i class='cell c'>C</i> cooperated</span>
  <span class='lg'><i class='cell d'>D</i> defected</span>
  <span class='lg'><i class='cell sub'>&#9633;</i> no valid token &rarr; honest move substituted</span>
  <span class='lg'><i class='cell c recon'>C</i> final round replayed from the opponent's rule</span>
  <span class='lg'><i class='mark'>&#9650;</i> first betrayal</span>
  <span class='lg'><i class='mark'>&#9660;</i> punishment starts</span>
  <span class='lg'><i class='mark'>&#9679;</i> you come back</span>
  <span class='lg'><i class='mark'>&#9733;</i> trust returns</span>
</div>"""

CSS = """
:root{
  --plane:#0d0d0d; --surface:#171a21; --card:#12151c;
  --ink:#ffffff; --ink2:#c3c2b7; --mut:#898781;
  --grid:#2c2c2a; --rule:#262a33;
  --good:#0ca30c; --warn:#fab219; --crit:#d03b3b;
  --tft:#3987e5; --grim:#d55181;
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
 font:14px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--tft)}
header{padding:20px 24px 16px;border-bottom:1px solid var(--rule);
 background:var(--plane);position:sticky;top:0;z-index:20}
.hwrap{max-width:1180px;margin:0 auto}
header h1{margin:0 0 6px;font-size:19px;letter-spacing:-.01em}
header p{margin:0;color:var(--ink2);font-size:13px;max-width:92ch}
header code{color:var(--mut)}
nav{margin-top:10px}
nav a{margin-right:14px;font-size:12.5px;text-decoration:none}
main{max-width:1180px;margin:0 auto;padding:0 24px 90px}
h2{font-size:15px;text-transform:uppercase;letter-spacing:.08em;
 color:var(--mut);margin:38px 0 12px;font-weight:600}
h3{font-size:16px;margin:0}
.envid{color:var(--mut);font-weight:400;font-size:12.5px;margin-left:8px}
.sub{color:var(--ink2);font-size:12.5px;margin:4px 0 0}
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--ink2)}

/* stat tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
 gap:12px;margin-top:16px}
.tile{background:var(--surface);border:1px solid var(--rule);border-radius:10px;
 padding:16px 18px}
.tile .big{font-size:40px;line-height:1;font-weight:650;letter-spacing:-.02em}
.tile .big em{font-style:normal;font-size:20px;color:var(--mut);font-weight:500}
.tile .cap{margin-top:8px;font-size:13px;color:var(--ink2)}
.tile .foot{margin-top:6px;font-size:12px;color:var(--mut)}
.tile.tft .big{color:var(--tft)} .tile.grim .big{color:var(--grim)}
.tile.cond{border-color:#2f3a2c} .tile.cond .big{color:var(--good)}

.find{margin:14px 0 0;padding-left:18px;color:var(--ink2);font-size:13.5px}
.find li{margin:7px 0} .find b{color:var(--ink)}

/* funnel table */
.tablewrap{margin-top:14px;background:var(--surface);
 border:1px solid var(--rule);border-radius:10px;overflow-x:auto}
table.funnel{width:100%;border-collapse:collapse;min-width:760px}
table.funnel caption{caption-side:top;text-align:left;color:var(--mut);
 font-size:12.5px;padding:10px 12px 8px}
.funnel th,.funnel td{padding:9px 10px;text-align:left;font-size:12.5px;
 border-bottom:1px solid var(--grid);vertical-align:middle}
.funnel tr:last-child th,.funnel tr:last-child td{border-bottom:0}
.funnel thead th{color:var(--mut);font-weight:600;text-transform:uppercase;
 letter-spacing:.05em;font-size:11px;white-space:nowrap}
.funnel tbody th{font-weight:600;color:var(--ink);width:1%;white-space:nowrap;
 border-right:1px solid var(--grid)}
.funnel td.num{font-variant-numeric:tabular-nums;text-align:right;
 color:var(--ink);font-weight:600}
.funnel td.rec{background:rgba(12,163,12,.06)}
.funnel tr.tot td,.funnel tr.tot th{background:rgba(255,255,255,.03)}
.dots{display:inline-flex;gap:3px;vertical-align:middle}
.dot{width:9px;height:9px;border-radius:2px;display:block;background:var(--mut)}
.dot.off{background:transparent;box-shadow:inset 0 0 0 1px var(--grid)}
.dot.tft{background:var(--tft)} .dot.grim{background:var(--grim)}
.dnum{margin-left:8px;color:var(--mut);font-variant-numeric:tabular-nums}
.ann{display:block;color:var(--mut);font-size:10.5px;margin-top:3px;
 max-width:17ch;line-height:1.3}
.dots{flex-wrap:wrap;max-width:118px}

.chip{font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;
 font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}
.chip.tft{background:rgba(57,135,229,.16);color:var(--tft)}
.chip.grim{background:rgba(213,81,129,.16);color:var(--grim)}

/* ribbons */
section{margin-top:34px;border-top:1px solid var(--rule);padding-top:20px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
@media (max-width:900px){.cols{grid-template-columns:1fr}}
.col{background:var(--surface);border:1px solid var(--rule);border-radius:10px;
 padding:12px 14px}
.colhead{display:flex;align-items:center;justify-content:space-between;
 padding-bottom:8px;border-bottom:1px solid var(--grid)}
.rate{font-size:18px;font-weight:650;font-variant-numeric:tabular-nums}
.rate em{font-style:normal;font-size:11px;color:var(--mut);margin-left:6px;
 text-transform:uppercase;letter-spacing:.05em}
.rate.tft{color:var(--tft)} .rate.grim{color:var(--grim)}
.ribbon{padding:10px 0;border-bottom:1px solid var(--grid)}
.ribbon:last-child{border-bottom:0}
.rlab{display:flex;align-items:center;gap:10px;font-size:12px;
 color:var(--ink2);margin-bottom:6px}
.rpay{color:var(--mut);font-variant-numeric:tabular-nums}
.rtag{margin-left:auto;font-size:11px;padding:1px 8px;border-radius:10px;
 text-transform:uppercase;letter-spacing:.04em;font-weight:700}
.rtag.rec{background:rgba(12,163,12,.16);color:var(--good)}
.rtag.ref{background:rgba(208,59,59,.16);color:var(--crit)}
.rtag.none{background:rgba(255,255,255,.05);color:var(--mut)}
.grid{display:grid;grid-template-columns:max-content 1fr;
 gap:2px 10px;align-items:center}
.who{font-size:10.5px;color:var(--mut);text-transform:uppercase;
 letter-spacing:.05em;text-align:right;white-space:nowrap;
 max-width:104px;overflow:hidden;text-overflow:ellipsis}
.row{display:flex;gap:2px}
.cell{width:22px;height:22px;border-radius:4px;display:grid;place-items:center;
 font:600 10.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;font-style:normal;
 color:#08140a;cursor:default;flex:0 0 auto}
.cell.c{background:var(--good)}
.cell.d{background:var(--crit);color:#1a0708}
.cell.sub{background:var(--warn);color:#241a03}
.cell.recon{box-shadow:inset 0 0 0 2px var(--surface),0 0 0 1px var(--mut);
 opacity:.72}
.cell.hit{box-shadow:0 0 0 2px var(--surface),0 0 0 4px var(--good)}
.cell.hit.recon{box-shadow:inset 0 0 0 2px var(--surface),
 0 0 0 2px var(--surface),0 0 0 4px var(--good)}
.row.marks .mark{width:22px;flex:0 0 auto;text-align:center;
 font-size:11px;font-style:normal;color:var(--ink2);height:14px;line-height:14px}
.narr{margin:10px 0 0;padding-left:18px;font-size:12.5px;color:var(--ink2)}
.narr li{margin:3px 0} .narr b{color:var(--ink)}

/* episode cards */
.eps{margin-top:14px}
details.ep{background:var(--surface);border:1px solid var(--rule);
 border-radius:8px;margin:8px 0;padding:8px 14px}
details.ep>summary{cursor:pointer;font-size:12.5px;color:var(--ink2)}
details.ep .body{margin-top:10px}
details.raw{margin-top:12px;background:var(--card);border:1px solid var(--grid);
 border-radius:6px;padding:6px 10px}
details.raw>summary{cursor:pointer;font-size:12px;color:var(--mut)}
.msg{margin:7px 0;padding:8px 10px;border-radius:6px;background:var(--card)}
.msg.system{opacity:.55}
.msg.game{border-left:3px solid var(--grid)}
.msg.agent{border-left:3px solid var(--tft)}
.role{display:inline-block;font-size:10.5px;color:var(--mut);
 text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.role.exploit{color:var(--crit)} .role.honest{color:var(--good)}
.role.unparsed{color:var(--warn)}
pre{margin:0;white-space:pre-wrap;word-break:break-word;
 font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--ink2)}

/* legend + tooltip */
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin:14px 0 0;
 font-size:12px;color:var(--ink2);align-items:center}
.lg{display:inline-flex;align-items:center;gap:7px}
.lg .cell,.lg .mark{width:20px;height:20px;line-height:20px}
#tip{position:fixed;z-index:60;pointer-events:none;opacity:0;
 transition:opacity .1s;background:#20242c;color:var(--ink);
 border:1px solid var(--rule);border-radius:6px;padding:6px 9px;
 font-size:12px;max-width:320px;box-shadow:0 6px 20px rgba(0,0,0,.5)}
.note{color:var(--mut);font-size:12.5px;margin-top:10px;max-width:82ch}
.verdict{font-size:13.5px;color:var(--ink2);margin:10px 0 0;padding:8px 12px;
 border-left:3px solid var(--grid);background:var(--surface);border-radius:0 6px 6px 0}
.verdict b{color:var(--ink)}
.verdict.yes{border-left-color:var(--good)}
footer{margin-top:44px;border-top:1px solid var(--rule);padding-top:14px}
@media print,(forced-colors:active){
  .cell.d{background:repeating-linear-gradient(45deg,#000,#000 2px,#fff 2px,#fff 4px)}
  .cell.sub{background:repeating-linear-gradient(135deg,#000,#000 1px,#fff 1px,#fff 4px)}
}
"""

JS = """
(function(){
  var tip=document.createElement('div');tip.id='tip';document.body.appendChild(tip);
  function show(e){
    var el=e.target.closest('[data-tip]');
    if(!el||!el.dataset.tip){tip.style.opacity=0;return;}
    tip.textContent=el.dataset.tip;tip.style.opacity=1;
    var r=el.getBoundingClientRect(),t=tip.getBoundingClientRect();
    var x=Math.min(window.innerWidth-t.width-8,Math.max(8,r.left+r.width/2-t.width/2));
    var y=r.top-t.height-8; if(y<8) y=r.bottom+8;
    tip.style.left=x+'px';tip.style.top=y+'px';
  }
  document.addEventListener('mousemove',show);
  document.addEventListener('mouseleave',function(){tip.style.opacity=0;});
})();
"""

PAGE = """<!doctype html><html lang='en'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Grim vs TFT &mdash; does trust come back?</title>
<style>{css}</style></head><body>
<header><div class='hwrap'>
<h1>Grim vs TFT &mdash; does trust ever come back during eval?</h1>
<p><b>grim</b> and <b>tft</b> are matched members of the same <code>nohole</code>
population. They open the same way and punish the same way; the only difference
is what happens <i>after</i> the learner comes back &mdash; grim never returns,
tft returns the round the learner does. So the share of tft episodes that
recover is a direct read on whether this policy ever pays for repair, with grim
as the structural zero.</p>
<p class='note'>{n} recorded eval episodes &middot; {model} &middot;
source <code>{src}</code> (the <code>q38-think</code> condition of
<code>compare_reasoning.py</code>) &middot; 4 seeds per game &times; opponent.
Nothing is sampled here &mdash; this page only scores and draws episodes that
were already run. Each population's third member (<code>tf2t*</code>, and
<code>suspicious_tft</code> in <code>ipd</code>) is left out: it forgives on a
schedule of its own, which blurs the one axis this page is about.</p>
<nav>{nav}</nav></div></header>
<main>
<h2>The answer</h2>
{hero}
{findings}
<h2>Where it breaks down, per game</h2>
{table}
<h2>Every episode, round by round</h2>
{legend}
<p class='note'>Each strip is one episode: your move over the counterpart's,
one cell per round. Hover any cell for the round. The last round of the game
cells is never written to the log &mdash; the episode ends on your own action
&mdash; so it is replayed from the opponent's rule and drawn faded, and only
after that rule has been checked against every round the log <i>does</i>
contain.</p>
{sections}
<footer>
<p class='note'>Built by <code>grim_vs_tft.py</code> from recorded episodes only.
The adaptive/adaptive_recover utterance traces that used to live at this address
are unchanged at <a href='adaptive_sim.html'>adaptive_sim.html</a>; the no-hole
punishment viewer is at <a href='index.html'>index.html</a>.</p>
</footer>
</main><script>{js}</script></body></html>"""


def render(eps: List[Episode], src: str) -> str:
    nav = " ".join(f"<a href='#{e}'>{TITLE[e]}</a>" for e in GAMES
                   if any(x.env == e for x in eps))
    sections = "".join(game_section(e, eps) for e in GAMES
                       if any(x.env == e for x in eps))
    return PAGE.format(css=CSS, js=JS, nav=nav, n=len(eps), model=esc(MODEL),
                       src=esc(src), hero=hero(eps), findings=findings(eps),
                       table=summary_table(eps), legend=LEGEND,
                       sections=sections)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", default=EPISODES)
    ap.add_argument("--html", default=OUT_HTML)
    ap.add_argument("--print", dest="only_print", action="store_true")
    a = ap.parse_args(argv)

    path = Path(a.episodes)
    if not path.is_absolute():
        path = HERE / path
    eps = load(path)
    if not eps:
        print(f"no grim/tft nohole episodes in {path}", file=sys.stderr)
        return 1
    report(eps)
    if a.only_print:
        return 0

    out = Path(a.html)
    if not out.is_absolute():
        out = HERE / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(eps, a.episodes), encoding="utf-8")
    print(f"\nwrote {out}  ({len(eps)} episodes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
