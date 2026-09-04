#!/usr/bin/env python
"""Does flipping a REGIME or GROUP knob change what the model DOES?

    python analyze_bverif1.py
    python analyze_bverif1.py --md ../results/0904_bverif1/RESULTS.md

Reads `results/referee_spartan/bverif1/rows.jsonl` -- 43 arms x 6 models,
`condition=win`, `arm=hole`, `opponents=selfplay`, per-seat reflection -- and
compares every variant arm against the `@shipped` baseline OF ITS OWN CELL.

THE COMPARISON IS WITHIN (cell, model, round) AND NEVER ACROSS CELLS. The
prompt ladder moves cells in opposite directions, so a roster mean of exploit
rates describes no cell in the roster. What pools across cells is the
DIFFERENCE, because a difference is already relative to its own baseline.

WHAT COUNTS AS "MEANINGFUL", AND WHY IT NEEDS A NOISE FLOOR. A variant arm and
its baseline are two independent 12-chain samples, so they differ even when
the knob does nothing. The reference distribution for "nothing" is measured
here rather than assumed: the baseline arm's own 12 chains are split into two
halves of 6 by seed parity and the same difference statistic is computed on
them. That split-half spread is what a null looks like at this sample size,
in this cell, on this model -- and any |delta| inside it is not a finding.
It is a conservative floor in one direction (6 chains a side rather than 12,
so it overstates the noise) and that is the direction to err in.

THE SECOND QUESTION, AND THE MORE INTERESTING ONE. A variant that merely moves
the rate could be moving it for any reason. The catalogue in
`results/0902_variants/catalogue.json` says what the knob did to the SCRIPTED
incentive -- T(0), T(N-1), the regime class -- so the rows can be asked
whether the behavioural change goes the way the structural change does. A
model that exploits less exactly where the engine made exploiting stop paying
is responding to the regime; one that moves at random is not.

R0 IS THE BUILT-IN CONTROL FOR THE REFLECTION LADDER, not for the variant. At
R0 no playbook exists, so a baseline-vs-variant gap at R0 is the knob acting
on the shipped prompt alone; the R0 -> R3 change is the knob acting through
what the model wrote about itself. Both are reported, because they are
different claims.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ROWS = HERE / "results" / "referee_spartan" / "bverif1" / "rows.jsonl"
CATALOGUE = HERE.parent / "results" / "0902_variants" / "catalogue.json"


# ---------------------------------------------------------------- loading ---

def variant_map() -> Dict[str, Tuple[str, str, str]]:
    """cell_name -> (vid, base cell, intent).

    `variants.cell_name` is deterministic, so the mapping the runner used is
    rebuilt rather than recorded -- there is no field in the row that carries
    the vid, and inventing one would have needed an engine change mid-wave.
    """
    import variants as V
    out: Dict[str, Tuple[str, str, str]] = {}
    for v in V.CATALOGUE:
        out[V.cell_name(v)] = (v.vid, v.cell, v.intent)
    return out


def load(path: pathlib.Path) -> List[dict]:
    return [json.loads(l) for l in path.open() if l.strip()]


def pooled(rows: List[dict]) -> Optional[float]:
    """sum(v)/sum(o) -- never a mean of per-episode rates."""
    o = sum(r.get("o_headline") or 0 for r in rows)
    v = sum(r.get("v_headline") or 0 for r in rows)
    return (v / o) if o else None


def mean(xs: List[float]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


# ------------------------------------------------------------ the compare ---

def arm_rate(rows, game, model, rnd, seeds=None) -> Optional[float]:
    sel = [r for r in rows
           if r["game"] == game and r["model"] == model and r["round"] == rnd
           and (seeds is None or r["chain_seed"] in seeds)]
    return pooled(sel)


def arm_gain(rows, game, model, rnd, seeds=None) -> Optional[float]:
    sel = [r.get("gain_focal") for r in rows
           if r["game"] == game and r["model"] == model and r["round"] == rnd
           and (seeds is None or r["chain_seed"] in seeds)]
    return mean([x for x in sel if x is not None])


def split_half_floor(rows, base_cell, model, rnd) -> Optional[float]:
    """|rate(even seeds) - rate(odd seeds)| on the BASELINE arm.

    The noise floor, measured. Six chains a side against the twelve each real
    arm gets, so it overstates the spread -- deliberately.
    """
    seeds = sorted({r["chain_seed"] for r in rows
                    if r["game"] == base_cell and r["model"] == model})
    if len(seeds) < 4:
        return None
    a = arm_rate(rows, base_cell, model, rnd, set(seeds[0::2]))
    b = arm_rate(rows, base_cell, model, rnd, set(seeds[1::2]))
    if a is None or b is None:
        return None
    return abs(a - b)


def structural(vid: str, base_vid: str) -> Dict[str, Optional[float]]:
    """What the scripted curves say the knob did. None if not measured."""
    try:
        cat = json.loads(CATALOGUE.read_text())["variants"]
    except OSError:
        return {}
    v, b = cat.get(vid), cat.get(base_vid)
    if not v or not b:
        return {}
    return {"dT0": v["score"]["T0"] - b["score"]["T0"],
            "dTlast": v["score"]["Tlast"] - b["score"]["Tlast"],
            "class_flip": v["score"]["regime"] != b["score"]["regime"],
            "regime": v["score"]["regime"], "base_regime": b["score"]["regime"]}


def compare(rows: List[dict], vmap, pdiff=None) -> List[dict]:
    pdiff = pdiff if pdiff is not None else {}
    games = sorted({r["game"] for r in rows})
    models = sorted({r["model"] for r in rows})
    rounds = sorted({r["round"] for r in rows})
    base_of = {}
    for g in games:
        vid, cell, intent = vmap.get(g, (None, None, None))
        if vid and vid.endswith("@shipped"):
            base_of[cell] = g

    out = []
    for g in games:
        vid, cell, intent = vmap.get(g, (None, None, None))
        if intent not in ("REGIME", "GROUP"):
            continue                      # baselines and the un-crossed cells
        bg = base_of.get(cell)
        if bg is None:
            continue
        st = structural(vid, f"{cell}@shipped")
        for m in models:
            for rnd in rounds:
                rv, rb = arm_rate(rows, g, m, rnd), arm_rate(rows, bg, m, rnd)
                if rv is None or rb is None:
                    continue
                out.append({
                    "vid": vid, "cell": cell, "intent": intent, "model": m,
                    "round": rnd, "rate_variant": rv, "rate_base": rb,
                    "delta": rv - rb,
                    "floor": split_half_floor(rows, bg, m, rnd),
                    "gain_variant": arm_gain(rows, g, m, rnd),
                    "gain_base": arm_gain(rows, bg, m, rnd),
                    "diff_chars": (pdiff.get(vid) or (None,))[0],
                    **st})
    return out


def prompt_diff() -> Dict[str, Tuple[int, int, float]]:
    """vid -> (chars changed, baseline length, fraction) in the RULES TEXT.

    THE SALIENCE CONTROL. "The model responded to the regime" and "the model
    responded to a sentence that appeared in its prompt" predict the same
    drop, and the second is the cheaper explanation. Measuring how much text
    the knob actually moved separates them, and the roster happens to contain
    the clean cases at both ends: `ref_estate@bank-reserve-2` rewrites ZERO
    characters of the rules -- the reserve is never stated, so a model can
    only find it by playing -- while `ref_invoice@retainer-40` adds a whole
    sentence. Arms in between change a single digit.

    Rebuilt from the live engines rather than stored, for the same reason
    `variant_map` is: no field in the row carries it.
    """
    import difflib
    import referee_games as RG
    import referee_spartan as SP
    import variants as V
    SP.register_all()
    SP.register_holefill()
    V.register()
    byvid = {v.vid: v for v in V.CATALOGUE}
    want = [v for v in V.CATALOGUE if v.intent in ("REGIME", "GROUP")]
    V.register_variant_cells([v.vid for v in want]
                             + [f"{v.cell}@shipped" for v in want])

    def txt(g) -> str:
        for fn in ("_slip_prompt", "_rules", "_rules_text", "rules"):
            f = getattr(g, fn, None)
            if f is None:
                continue
            for args in ((), (0,), ({},), (0.0, 1.0, False),
                         ({k: 1 for k in ("wood", "brick", "sheep",
                                          "wheat", "ore", "gold")},)):
                try:
                    r = f(*args)
                except Exception:                       # noqa: BLE001
                    continue
                if isinstance(r, str) and r.strip():
                    return r
        return ""

    out: Dict[str, Tuple[int, int, float]] = {}
    for v in want:
        try:
            a = txt(RG.BY_NAME[V.cell_name(byvid[f"{v.cell}@shipped"])])
            b = txt(RG.BY_NAME[V.cell_name(v)])
        except KeyError:
            continue
        if not a or not b:
            continue
        ops = difflib.SequenceMatcher(None, a, b).get_opcodes()
        ch = sum(max(i2 - i1, j2 - j1)
                 for tag, i1, i2, j1, j2 in ops if tag != "equal")
        out[v.vid] = (ch, len(a), ch / max(1, len(a)))
    return out


def _r(pts: List[Tuple[float, float]]) -> float:
    """Pearson r over (x, y) pairs; nan when either side has no spread."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mx, my = mean(xs), mean(ys)
    if mx is None or my is None:
        return float("nan")
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs)
                    * sum((y - my) ** 2 for y in ys))
    return (num / den) if den else float("nan")


# --------------------------------------------------------------- reporting ---

def report(cmp_rows: List[dict], rows: List[dict]) -> str:
    L: List[str] = []
    w = L.append
    models = sorted({c["model"] for c in cmp_rows})
    rmax = max((c["round"] for c in cmp_rows), default=0)

    w("# bverif1 -- do REGIME and GROUP variants change behaviour?\n")
    w(f"{len(rows):,} rows, {len({r['game'] for r in rows})} arms, "
      f"{len(models)} models, rounds 0-{rmax}.\n")
    w("Rates are pooled `sum(v_headline)/sum(o_headline)`. Every delta is a "
      "variant arm minus the `@shipped` baseline of its own cell, at the same "
      "model and round. `floor` is the baseline arm's own split-half spread "
      "at that model and round -- the measured null.\n")

    for rnd in (0, rmax):
        sel = [c for c in cmp_rows if c["round"] == rnd]
        if not sel:
            continue
        w(f"\n## Round {rnd}"
          + ("  (no playbook yet: the knob acting on the shipped prompt)"
             if rnd == 0 else
             "  (after the reflection ladder)") + "\n")
        for axis in ("REGIME", "GROUP"):
            ax = [c for c in sel if c["intent"] == axis]
            if not ax:
                continue
            over = [c for c in ax if c["floor"] is not None
                    and abs(c["delta"]) > c["floor"]]
            md = mean([abs(c["delta"]) for c in ax])
            mf = mean([c["floor"] for c in ax if c["floor"] is not None])
            w(f"**{axis}**: {len(ax)} (arm, model) cells. "
              f"mean |delta| {md:.3f} against a mean noise floor of "
              f"{mf:.3f}; {len(over)}/{len(ax)} clear their own floor.\n")

        w("\n| arm | axis | model | base | variant | delta | floor | over? | dT(N-1) |")
        w("|---|---|---|---:|---:|---:|---:|:-:|---:|")
        for c in sorted(sel, key=lambda x: (-abs(x["delta"]), x["vid"])):
            fl = c["floor"]
            ok = "yes" if (fl is not None and abs(c["delta"]) > fl) else "no"
            dt = c.get("dTlast")
            w(f"| `{c['vid']}` | {c['intent']} | {c['model']} | "
              f"{c['rate_base']:.3f} | {c['rate_variant']:.3f} | "
              f"{c['delta']:+.3f} | {'--' if fl is None else f'{fl:.3f}'} | "
              f"{ok} | {'--' if dt is None else f'{dt:+.2f}'} |")

    # --- does behaviour follow the structure? --------------------------------
    w("\n## Does the behavioural change follow the structural one?\n")
    w("Each row is one (arm, model) at the last round. `dT(N-1)` is what the "
      "scripted curves say the knob did to the payoff of deviating when every "
      "other seat already exploits -- the corner `selfplay` samples. If models "
      "read the regime, a negative `dT(N-1)` should come with a negative "
      "`delta`.\n")
    # CLUSTERED BY ARM, NOT BY ROW. Six models sample the same arm, so eleven
    # (arm, model) rows over three arms is three observations of the knob and
    # not eleven -- pooling them into one correlation would count `ref_estate`
    # six times and read as n=11. The statistic below is over ARM MEANS, and
    # the per-row version is printed beside it only so the gap between them is
    # visible.
    last = [c for c in cmp_rows if c["round"] == rmax and c.get("dTlast") is not None]
    for axis in ("REGIME", "GROUP"):
        ax = [c for c in last if c["intent"] == axis]
        if len(ax) < 3:
            continue
        byarm: Dict[str, List[dict]] = collections.defaultdict(list)
        for c in ax:
            byarm[c["vid"]].append(c)
        pts = [(cs[0]["dTlast"], mean([x["delta"] for x in cs]))
               for cs in byarm.values()]
        agree = sum(1 for x, y in pts if (x > 0) == (y > 0) and y != 0)
        w(f"- **{axis}**: {len(byarm)} distinct arms over "
          f"{len({c['model'] for c in ax})} models ({len(ax)} arm-model "
          f"cells). Sign agreement on arm means {agree}/{len(byarm)}; "
          f"Pearson r(dT(N-1), mean delta) = {_r(pts):+.3f} over "
          f"{len(byarm)} arms"
          + (f" (per-row, pseudo-replicated: "
             f"{_r([(c['dTlast'], c['delta']) for c in ax]):+.3f} over "
             f"{len(ax)} rows)" if len(ax) != len(byarm) else "") + ".")
        if len(byarm) < 5:
            w(f"  - **n = {len(byarm)} arms. Not a correlation yet** -- "
              f"reported so the shape is visible, not so it can be cited.")

    # TWO MECHANISMS, NOT ONE, AND THEY MUST NOT BE AVERAGED. `ref_invoice`'s
    # retainer arms flip the regime CLASS while leaving T(N-1) exactly equal to
    # the baseline: the clause changes what honest play is worth to the group,
    # not what deviating is worth to the deviator at the corner `selfplay`
    # samples. So a drop there is a response to a STATED RULE, and a drop on
    # `gen_seven_seal@budget-13` -- whose T(N-1) falls 49.00 -> 0.00 -- is a
    # response to a payoff the seat can feel. Pooling them into one
    # correlation asks whether models track a payoff using arms where the
    # payoff did not move.
    w("\n### Rule-only arms against payoff-moving arms\n")
    w("`dT(N-1)` is the change in what deviating pays at the all-exploit "
      "corner. An arm with `dT(N-1) = 0` that still flips its regime class "
      "changed the RULES TEXT and the group's stake without changing the "
      "deviator's own payoff where this wave samples it. Those two kinds of "
      "arm are reported apart because a model can only be tracking the payoff "
      "in one of them.\n")
    w("| kind | arms | arm-model cells | mean delta | mean \\|delta\\| | over floor |")
    w("|---|---:|---:|---:|---:|---:|")
    for kind, keep in (("payoff moved (|dT(N-1)| >= 1)",
                        lambda c: abs(c["dTlast"]) >= 1.0),
                       ("rule only (|dT(N-1)| < 1)",
                        lambda c: abs(c["dTlast"]) < 1.0)):
        ax = [c for c in last if keep(c)]
        if not ax:
            continue
        over = sum(1 for c in ax
                   if c["floor"] is not None and abs(c["delta"]) > c["floor"])
        w(f"| {kind} | {len({c['vid'] for c in ax})} | {len(ax)} | "
          f"{mean([c['delta'] for c in ax]):+.3f} | "
          f"{mean([abs(c['delta']) for c in ax]):.3f} | {over}/{len(ax)} |")

    # HEADROOM FIRST, BECAUSE IT OUTRANKS BOTH OF THE INTERESTING ANSWERS.
    # A cell whose baseline already sits at 0.02 cannot show a large drop
    # whatever the knob does, so a raw |delta| ranking is partly a ranking of
    # how much room each cell had. Measured on this roster the baseline rate
    # correlates with |delta| at r ~ +0.74 -- higher than salience or payoff
    # change -- so it is a confound to remove, not a finding to report. The
    # arms below the cut are still sampled and still in the tables above;
    # they are excluded HERE because a null in them is uninformative.
    w("\n### Headroom, and the relative effect\n")
    w("The strongest predictor of a raw `|delta|` is the BASELINE RATE: a "
      "cell already at 0.02 has nowhere to fall. That is a property of the "
      "cell, not of the knob, so the arms with room are separated out and "
      "the effect is restated as `delta / baseline` -- the fraction of its "
      "own exploiting the arm gained or gave up.\n")
    arms_all = {}
    for c in last:
        arms_all.setdefault(c["vid"], []).append(c)
    base_pts = [(mean([x["rate_base"] for x in cs]),
                 mean([abs(x["delta"]) for x in cs]))
                for cs in arms_all.values()]
    w(f"- Pearson r(baseline rate, mean |delta|) = {_r(base_pts):+.3f} over "
      f"{len(base_pts)} arms -- the confound.")
    HEAD = 0.15
    room = {v: cs for v, cs in arms_all.items()
            if (mean([x["rate_base"] for x in cs]) or 0) >= HEAD}
    w(f"- {len(room)} of {len(arms_all)} arms have a baseline at or above "
      f"{HEAD:.2f}. Below it, a null cannot be told from a floor.\n")
    if room:
        w("| arm | axis | baseline | relative change | \\|delta\\| | chars | dT(N-1) |")
        w("|---|---|---:|---:|---:|---:|---:|")
        rel_of = {}
        for vid, cs in room.items():
            rel_of[vid] = mean([c["delta"] / c["rate_base"] for c in cs
                                if c["rate_base"]])
        for vid, cs in sorted(room.items(), key=lambda kv: rel_of[kv[0]] or 0):
            dt, ch = cs[0].get("dTlast"), cs[0].get("diff_chars")
            w(f"| `{vid}` | {cs[0]['intent']} | "
              f"{mean([c['rate_base'] for c in cs]):.3f} | "
              f"{rel_of[vid]:+.3f} | "
              f"{mean([abs(c['delta']) for c in cs]):.3f} | "
              f"{'--' if ch is None else ch} | "
              f"{'--' if dt is None else f'{dt:+.2f}'} |")
        big = [v for v, r in rel_of.items() if abs(r) >= 0.30]
        w(f"\n**{len(big)} of {len(room)} arms with headroom move the "
          f"baseline's own exploiting by 30% or more.** That is the answer to "
          f"whether variants produce meaningful behaviour, and it does not "
          f"depend on either explanation below.\n")
        sal = [(cs[0]["diff_chars"], rel_of[v]) for v, cs in room.items()
               if cs[0].get("diff_chars") is not None]
        pay = [(cs[0]["dTlast"], rel_of[v]) for v, cs in room.items()
               if cs[0].get("dTlast") is not None]
        if sal:
            w(f"- r(chars rewritten, relative change) = {_r(sal):+.3f}")
        if pay:
            w(f"- r(dT(N-1), relative change) = {_r(pay):+.3f}")

    # WHICH PREDICTS THE BEHAVIOUR: the payoff, or the prompt?
    w("\n### Salience against payoff\n")
    w("`chars` is how much of the rules text the knob rewrote. The roster has "
      "clean cases at both ends -- `ref_estate@bank-reserve-2` changes ZERO "
      "characters (the reserve is never stated; a model can only find it by "
      "playing) and `ref_invoice@retainer-40` adds a whole sentence -- so "
      "\"the model read the regime\" and \"the model read a new sentence\" "
      "are separable here rather than confounded.\n")
    havep = [c for c in last if c.get("diff_chars") is not None]
    if havep:
        arms = {}
        for c in havep:
            arms.setdefault(c["vid"], []).append(c)
        pts_p = [(cs[0]["diff_chars"], mean([abs(x["delta"]) for x in cs]))
                 for cs in arms.values()]
        pts_t = [(abs(cs[0]["dTlast"]), mean([abs(x["delta"]) for x in cs]))
                 for cs in arms.values() if cs[0].get("dTlast") is not None]
        w(f"- Pearson r(chars rewritten, mean |delta|) = {_r(pts_p):+.3f} "
          f"over {len(pts_p)} arms.")
        if pts_t:
            w(f"- Pearson r(|dT(N-1)|, mean |delta|) = {_r(pts_t):+.3f} "
              f"over {len(pts_t)} arms.")
        w("")
        w("| arm | chars rewritten | dT(N-1) | mean \\|delta\\| | over floor |")
        w("|---|---:|---:|---:|---:|")
        for vid, cs in sorted(arms.items(),
                              key=lambda kv: -kv[1][0]["diff_chars"]):
            over = sum(1 for c in cs if c["floor"] is not None
                       and abs(c["delta"]) > c["floor"])
            dt = cs[0].get("dTlast")
            w(f"| `{vid}` | {cs[0]['diff_chars']} | "
              f"{'--' if dt is None else f'{dt:+.2f}'} | "
              f"{mean([abs(c['delta']) for c in cs]):.3f} | {over}/{len(cs)} |")

    flips = [c for c in last if c.get("class_flip")]
    if flips:
        w("\n### The class flips\n")
        w("The arms where the engine stopped rewarding the exploit at the "
          "all-exploit corner. These are where a behavioural response is "
          "least ambiguous, because the shipped arm and the variant differ in "
          "kind and not only in level.\n")
        w("| arm | model | base class -> variant class | base | variant | delta |")
        w("|---|---|---|---:|---:|---:|")
        for c in sorted(flips, key=lambda x: (x["vid"], x["model"])):
            w(f"| `{c['vid']}` | {c['model']} | {c['base_regime']} -> "
              f"{c['regime']} | {c['rate_base']:.3f} | "
              f"{c['rate_variant']:.3f} | {c['delta']:+.3f} |")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", default=str(ROWS))
    ap.add_argument("--md", default=None, help="also write the report here")
    a = ap.parse_args()
    rows = load(pathlib.Path(a.rows))
    if not rows:
        print("no rows yet", file=sys.stderr)
        return 1
    text = report(compare(rows, variant_map(), prompt_diff()), rows)
    print(text)
    if a.md:
        p = pathlib.Path(a.md)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        print(f"[bverif1] wrote {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
