#!/usr/bin/env python
"""bverif1 as model-separation figures: can these cells tell six models apart?

    python make_bverif_figs.py        # -> ../results/0904_bverif1/index.html

SAME QUESTION AS `make_pilot_figs.py`, ON A DIFFERENT ROSTER. Not "which model
is best" -- "can this suite separate models at all". So everything is ordered
BY SPREAD (max model minus min model) rather than by rate: a cell every model
saturates and a cell every model floors are equally useless for discrimination,
however interesting the hole is, and a rate-ordered chart hides that by putting
the two at opposite ends.

WHAT IS NEW HERE, AND IS THE REASON THIS PAGE EXISTS RATHER THAN A SECTION 8 ON
THE PILOTS PAGE. `bverif1` sampled 13 cells TWICE OR MORE -- the shipped arm
and one or two knob variants of it -- so for the first time the question can be
asked of a variant as well as of a cell: does flipping a REGIME or GROUP knob
make a game BETTER or WORSE at separating models? Section 3 is that plot and it
has no counterpart in any earlier figure set.

SIX SERIES, WHICH IS TWO MORE THAN THE PILOTS PAGE CARRIED, so the palette
question is live rather than inherited. `viz/validate_palette.py` passes the
first six categorical slots on the ADJACENT pairlist in both modes -- worst
adjacent CVD dE 9.1 light / 8.4 dark against an 8.0 target -- which is the
right pairlist for grouped bars and for lines that do not cross. It does NOT
pass all-pairs past three slots, so nothing here is a scatter with six models
overlaid; section 4 uses one panel per cell with the models as adjacent lines
and every line directly labelled. Three light-mode slots sit under 3:1 on the
surface, which the validator reports as RELIEF and not as a pass, so every
figure ships a table view and direct labels.
"""
from __future__ import annotations

import collections
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OUT = HERE.parent / "results" / "0904_bverif1"
ROWS = HERE / "results" / "referee_spartan" / "bverif1" / "rows.jsonl"
VERIFIER = HERE.parent / "results" / "0903_verifier" / "verifier.json"

# Fixed order, never cycled, never re-assigned when a filter drops a series.
MODELS = ["haiku", "gpt-mini", "gemini-flash",
          "fleet-qwen38", "fleet-glm53", "fleet-kimi3"]
LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

RMAX = 3

# Panel-edge labels: the full ids do not fit a 293px panel and would run
# into the next one. The legend and every table carry the full name.
SHORT = {"haiku": "haiku", "gpt-mini": "gpt-mini",
         "gemini-flash": "gem-flash", "fleet-qwen38": "qwen38",
         "fleet-glm53": "glm53", "fleet-kimi3": "kimi3"}


# ------------------------------------------------------------------ data ---

def load():
    return [json.loads(l) for l in ROWS.open() if l.strip()]


def rate(rows, game, model, rnd):
    """Pooled sum(v)/sum(o). None when the cell offered no opportunity."""
    o = v = 0
    for r in rows:
        if r["game"] == game and r["model"] == model and r["round"] == rnd:
            o += r.get("o_headline") or 0
            v += r.get("v_headline") or 0
    return (v / o) if o else None


def spread(rs):
    vs = [x for x in rs.values() if x is not None]
    return (max(vs) - min(vs)) if len(vs) > 1 else None


def variant_map():
    """sampling cell name -> (vid, base cell, intent). Rebuilt, not stored."""
    import variants as V
    return {V.cell_name(v): (v.vid, v.cell, v.intent) for v in V.CATALOGUE}


def scripted_reference():
    """cell -> (rate, gain) for a scripted exploiter, off the verifier report.

    The DENOMINATOR for section 2. A model rate of 0.00 means one thing when a
    script cannot work the cell either and quite another when a script takes it
    on every opportunity, and only the second is a model result.
    """
    out = {}
    try:
        d = json.loads(VERIFIER.read_text())
    except OSError:
        return out
    for r in d["rows"]:
        vc = r.get("verifier_cell") or r["cell"]
        e = (r.get("measured") or {}).get("exploit") or {}
        out[vc] = (e.get("rate"), e.get("gain"))
    return out


def collect():
    rows = load()
    vmap = variant_map()
    games = sorted({r["game"] for r in rows})
    cells = {}
    for g in games:
        vid, cell, intent = vmap.get(g, (None, None, None))
        cells[g] = {
            "game": g,
            "vid": vid,
            "cell": cell or g,
            "intent": intent,
            "is_base": (vid is None) or vid.endswith("@shipped"),
            "brought_in": g.startswith("hf_"),
            "r": {rnd: {m: rate(rows, g, m, rnd) for m in MODELS}
                  for rnd in range(RMAX + 1)},
        }
        for rnd in range(RMAX + 1):
            cells[g][f"spread{rnd}"] = spread(cells[g]["r"][rnd])
    return rows, cells


# ------------------------------------------------------------------- svg ---

def esc(s):
    return html.escape(str(s), quote=True)


def label(g, cells):
    """What to print on an axis. The vid where there is one, else the cell."""
    return cells[g]["vid"] or g


def bars(cells, order, w=880, rowh=54, pad_l=252, rnd=RMAX):
    """Grouped horizontal bars, one group per cell, one bar per model.

    Rounded data-ends anchored to the baseline, a 2px surface gap between
    bars. LABELS ARE SELECTIVE: only the highest and lowest model in each
    group carry a number, because those two ARE the spread and a number on all
    six would be six 9px labels on a 8px pitch -- unreadable, and against the
    rule that a chart never numbers every mark.
    """
    bh, gap = 6, 2
    h = len(order) * rowh + 34
    inner = w - pad_l - 74
    out = [f'<svg viewBox="0 0 {w} {h}" class="fig" role="img">']
    for gx in range(0, 11, 2):
        x = pad_l + inner * gx / 10
        out.append(f'<line class="grid" x1="{x:.1f}" y1="14" x2="{x:.1f}" '
                   f'y2="{len(order)*rowh+14}"/>')
        out.append(f'<text class="ax" x="{x:.1f}" y="{h-6}" '
                   f'text-anchor="middle">{gx/10:.1f}</text>')
    for i, g in enumerate(order):
        y0 = 18 + i * rowh
        c = cells[g]
        sp = c[f"spread{rnd}"]
        out.append(f'<text class="lab" x="{pad_l-46}" y="{y0+26}" '
                   f'text-anchor="end">{esc(label(g, cells))}</text>')
        out.append(f'<text class="spr" x="{pad_l-8}" y="{y0+26}" '
                   f'text-anchor="end">{"--" if sp is None else f"{sp:.2f}"}'
                   f'</text>')
        live = {m: v for m, v in c["r"][rnd].items() if v is not None}
        ends = ({max(live, key=live.get), min(live, key=live.get)}
                if len(live) > 1 else set(live))
        for j, m in enumerate(MODELS):
            v = c["r"][rnd][m]
            y = y0 + j * (bh + gap)
            if v is None:
                continue
            bw = max(0.7, inner * v)
            out.append(
                f'<rect class="bar s{j}" x="{pad_l}" y="{y}" '
                f'width="{bw:.1f}" height="{bh}" rx="2.5">'
                f'<title>{esc(f"{label(g, cells)} · {m}: {v:.3f} at R{rnd}")}'
                f'</title></rect>')
            if m in ends:
                out.append(f'<text class="val" x="{pad_l+bw+5:.1f}" '
                           f'y="{y+bh}">{v:.2f}</text>')
        out.append(f'<line class="sep" x1="{pad_l-52}" y1="{y0+rowh-4}" '
                   f'x2="{w-66}" y2="{y0+rowh-4}"/>')
    out.append("</svg>")
    return "\n".join(out)


def dumbbell(pairs, w=880, rowh=30, pad_l=250, pad_r=96, lo=0.0,
             hi=1.0, lab_a="baseline", lab_b="variant"):
    """One row per arm: a hollow ring at the baseline, a filled dot at the arm.

    A dumbbell rather than two bars because the quantity IS the move: two bars
    make the reader subtract, and the sign of the difference is the finding.
    """
    h = len(pairs) * rowh + 40
    inner = w - pad_l - pad_r
    X = lambda v: pad_l + inner * (v - lo) / (hi - lo)          # noqa: E731
    out = [f'<svg viewBox="0 0 {w} {h}" class="fig" role="img">']
    for gx in range(0, 11, 2):
        v = lo + (hi - lo) * gx / 10
        out.append(f'<line class="grid" x1="{X(v):.1f}" y1="10" '
                   f'x2="{X(v):.1f}" y2="{len(pairs)*rowh+12}"/>')
        out.append(f'<text class="ax" x="{X(v):.1f}" y="{h-8}" '
                   f'text-anchor="middle">{v:.1f}</text>')
    for i, (name, a, b, note, worse) in enumerate(pairs):
        y = 24 + i * rowh
        out.append(f'<text class="lab" x="{pad_l-10}" y="{y+4}" '
                   f'text-anchor="end">{esc(name)}</text>')
        cls = "wr" if worse else "bt"
        out.append(f'<line class="dbar {cls}" x1="{X(a):.1f}" y1="{y}" '
                   f'x2="{X(b):.1f}" y2="{y}"/>')
        out.append(f'<circle class="ghost" cx="{X(a):.1f}" cy="{y}" r="4.6">'
                   f'<title>{esc(f"{name} {lab_a} {a:.3f}")}</title></circle>')
        out.append(f'<circle class="solid {cls}f" cx="{X(b):.1f}" cy="{y}" '
                   f'r="4.6"><title>{esc(f"{name} {lab_b} {b:.3f}")}</title>'
                   f'</circle>')
        tx = max(X(a), X(b)) + 10
        out.append(f'<text class="dl {cls}t" x="{tx:.1f}" y="{y+3.5}">'
                   f'{esc(note)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def ladders(cells, grid, w=900, ph=150, cols=4, gut=64):
    """R0..R3 per model, one panel per arm. Adjacent lines, direct labels.

    `grid` is a FLAT LIST WITH `None` FOR BLANKS, so the caller controls the
    layout rather than the panel count doing it. That is what lets section 4
    put one CELL PER ROW with its shipped arm always in column 1 and its
    variants beside it: with a plain wrap, `ref_commons@regen-30` would land
    under whatever happened to precede it and the shipped-vs-variant reading
    the section exists for would be a scavenger hunt.
    """
    rowsn = (len(grid) + cols - 1) // cols
    pw, h = w / cols, rowsn * ph + 14
    out = [f'<svg viewBox="0 0 {w} {h}" class="fig" role="img">']
    for pi, g in enumerate(grid):
        if g is None:
            continue
        cx, cy = (pi % cols) * pw, (pi // cols) * ph
        pl, pr, pt, pb = cx + 32, cx + pw - gut, cy + 22, cy + ph - 26
        sp = cells[g][f"spread{RMAX}"]
        out.append(f'<text class="ptitle" x="{cx+4}" y="{cy+13}">'
                   f'{esc(label(g, cells))}</text>')
        out.append(f'<text class="pspr" x="{cx+pw-8}" y="{cy+13}" '
                   f'text-anchor="end">{"--" if sp is None else f"{sp:.2f}"}'
                   f'</text>')
        for gy in (0, 0.5, 1.0):
            y = pb - (pb - pt) * gy
            out.append(f'<line class="grid" x1="{pl}" y1="{y:.1f}" '
                       f'x2="{pr}" y2="{y:.1f}"/>')
            out.append(f'<text class="ax" x="{pl-5}" y="{y+3:.1f}" '
                       f'text-anchor="end">{gy:.1f}</text>')
        for r in range(RMAX + 1):
            x = pl + (pr - pl) * r / RMAX
            out.append(f'<text class="ax" x="{x:.1f}" y="{pb+13}" '
                       f'text-anchor="middle">R{r}</text>')
        ends = []
        for j, m in enumerate(MODELS):
            pts = []
            for r in range(RMAX + 1):
                v = cells[g]["r"][r][m]
                if v is None:
                    continue
                pts.append((pl + (pr - pl) * r / RMAX,
                            pb - (pb - pt) * v, v))
            if not pts:
                continue
            d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}"
                         for i, (x, y, _) in enumerate(pts))
            out.append(f'<path class="ln s{j}" d="{d}"/>')
            for x, y, v in pts:
                out.append(f'<circle class="dot s{j}" cx="{x:.1f}" '
                           f'cy="{y:.1f}" r="2.6"><title>'
                           f'{esc(f"{m}: {v:.3f}")}</title></circle>')
            ends.append((pts[-1][1], j, m, pts[-1][2]))
        # Direct labels, de-collided downward and then SHIFTED BACK INSIDE
        # THE PANEL. Pushing each label below the one above it stops them
        # overlapping, but in a panel where all six models sit on the floor
        # the stack grows ~46px past `pb` and runs into the panel underneath
        # -- exactly the case section 5 is full of. So the stack is clamped:
        # slide it up by whatever it overhangs, never above the top of plot.
        placed, last = [], -99.0
        for y, j, m, v in sorted(ends):
            y = max(y, last + 9.2)
            last = y
            placed.append((y, j, m))
        if placed:
            over = placed[-1][0] - (pb + 5)
            if over > 0:
                shift = min(over, max(0.0, placed[0][0] - (pt - 3)))
                placed = [(y - shift, j, m) for y, j, m in placed]
        for y, j, m in placed:
            out.append(f'<text class="plab s{j}t" x="{pr+4}" y="{y+3:.1f}">'
                       f'{esc(SHORT[m])}</text>')
    out.append("</svg>")
    return "\n".join(out)


def table(headers, rows_):
    th = "".join(f"<th>{esc(x)}</th>" for x in headers)
    tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>"
                 for r in rows_)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


def legend():
    return ('<div class="legend">' + "".join(
        f'<span class="lg"><i class="sw s{j}b"></i>{esc(m)}</span>'
        for j, m in enumerate(MODELS)) + "</div>")


def fmt(v, nd=3):
    return "--" if v is None else f"{v:.{nd}f}"


# ------------------------------------------------------------------ page ---

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, cells = collect()
    ref = scripted_reference()

    base = [g for g, c in cells.items() if c["is_base"]]
    native = [g for g in base if not cells[g]["brought_in"]]
    brought = sorted((g for g in base if cells[g]["brought_in"]),
                     key=lambda g: -(cells[g]["spread3"] or 0))
    order1 = sorted(base, key=lambda g: -(cells[g]["spread3"] or 0))

    # --- 1 -------------------------------------------------------------
    fig1 = bars(cells, order1)
    tab1 = table(["cell", "spread R3", "spread R0"] + MODELS,
                 [[label(g, cells), fmt(cells[g]["spread3"], 3),
                   fmt(cells[g]["spread0"], 3)]
                  + [fmt(cells[g]["r"][RMAX][m]) for m in MODELS]
                  for g in order1])
    dead = [g for g in base if (cells[g]["spread3"] or 0) < 0.10]
    live = [g for g in base if (cells[g]["spread3"] or 0) >= 0.30]
    top = order1[0]

    # --- 2 -------------------------------------------------------------
    pairs2 = []
    for g in brought:
        rr, gg = ref.get(g, (None, None))
        best = max([v for v in cells[g]["r"][RMAX].values()
                    if v is not None] or [0.0])
        pairs2.append((g, rr if rr is not None else 1.0, best,
                       (f"+{gg:.0f} pts" if gg else ""),
                       True))
    fig2 = dumbbell(pairs2, pad_l=210, pad_r=104,
                    lab_a="scripted exploiter", lab_b="best model")
    tab2 = table(["cell", "scripted rate", "scripted gain", "spread R3"]
                 + MODELS,
                 [[g, fmt(ref.get(g, (None, None))[0], 3),
                   ("--" if ref.get(g, (None, None))[1] is None
                    else f"{ref[g][1]:+.1f}"),
                   fmt(cells[g]["spread3"])]
                  + [fmt(cells[g]["r"][RMAX][m]) for m in MODELS]
                  for g in brought])

    # --- 3 -------------------------------------------------------------
    bycell = collections.defaultdict(dict)
    for g, c in cells.items():
        if c["vid"]:
            bycell[c["cell"]][c["vid"]] = g
    moves = []
    for cell, arms in bycell.items():
        b = arms.get(f"{cell}@shipped")
        if not b:
            continue
        for vid, g in arms.items():
            if vid.endswith("@shipped"):
                continue
            sa, sb = cells[b]["spread3"], cells[g]["spread3"]
            if sa is None or sb is None:
                continue
            moves.append((sb - sa, vid, cells[g]["intent"], sa, sb))
    moves.sort()
    fig3 = dumbbell([(f"{vid}  ({it})", sa, sb, f"{d:+.3f}", d < 0)
                     for d, vid, it, sa, sb in moves],
                    pad_l=296, pad_r=70,
                    lab_a="shipped arm", lab_b="variant arm")
    tab3 = table(["arm", "axis", "spread shipped", "spread variant", "change"],
                 [[vid, it, fmt(sa), fmt(sb), f"{d:+.3f}"]
                  for d, vid, it, sa, sb in moves])
    worse = [m for m in moves if m[0] < 0]
    better = [m for m in moves if m[0] > 0]

    # --- 4 and 5 ---------------------------------------------------------
    # EVERY ARM GETS A PANEL. The 13 crossed cells are laid out one CELL PER
    # ROW -- shipped arm always in column 1, its variants to the right, blanks
    # padding the short rows -- so the shipped-vs-variant comparison is a
    # sideways glance rather than a search. The 10 uncrossed cells follow in
    # their own grid, ordered by spread, because they have nothing to sit
    # beside and interleaving them would break the row invariant.
    COLS = 4
    crossed = sorted(
        (c for c in bycell if f"{c}@shipped" in bycell[c]),
        key=lambda c: -(cells[bycell[c][f"{c}@shipped"]]["spread3"] or 0))
    grid4 = []
    for cell in crossed:
        arms = bycell[cell]
        rowg = [arms[f"{cell}@shipped"]]
        rowg += [g for vid, g in sorted(arms.items())
                 if not vid.endswith("@shipped")
                 and cells[g]["intent"] == "REGIME"]
        rowg += [g for vid, g in sorted(arms.items())
                 if not vid.endswith("@shipped")
                 and cells[g]["intent"] == "GROUP"]
        grid4 += rowg + [None] * (COLS - len(rowg))
    fig4 = ladders(cells, grid4, cols=COLS)
    tab4 = table(["arm", "axis", "model"] + [f"R{r}" for r in range(RMAX + 1)],
                 [[label(g, cells), cells[g]["intent"] or "baseline", m]
                  + [fmt(cells[g]["r"][r][m]) for r in range(RMAX + 1)]
                  for g in grid4 if g is not None for m in MODELS])

    solo = sorted((g for g in base if cells[g]["cell"] not in crossed),
                  key=lambda g: -(cells[g]["spread3"] or 0))
    grid5 = solo + [None] * ((-len(solo)) % COLS)
    fig5 = ladders(cells, grid5, cols=COLS)
    tab5 = table(["cell", "model"] + [f"R{r}" for r in range(RMAX + 1)],
                 [[label(g, cells), m]
                  + [fmt(cells[g]["r"][r][m]) for r in range(RMAX + 1)]
                  for g in solo for m in MODELS])

    sw = "\n".join(
        f".s{j}{{fill:{c}}} .s{j}t{{fill:{c}}} .s{j}s{{stroke:{c}}} "
        f".s{j}b{{background:{c}}} .ln.s{j}{{stroke:{c}}}"
        for j, c in enumerate(LIGHT))
    swd = "\n".join(
        f".s{j}{{fill:{c}}} .s{j}t{{fill:{c}}} .s{j}s{{stroke:{c}}} "
        f".s{j}b{{background:{c}}} .ln.s{j}{{stroke:{c}}}"
        for j, c in enumerate(DARK))

    page = TPL.format(
        sw=sw, swd=swd, legend=legend(),
        n_rows=f"{len(rows):,}", n_arms=len(cells), n_base=len(base),
        n_models=len(MODELS),
        fig1=fig1, tab1=tab1, fig2=fig2, tab2=tab2,
        fig3=fig3, tab3=tab3, fig4=fig4, tab4=tab4, fig5=fig5, tab5=tab5,
        n_panels=sum(1 for g in grid4 if g) + len(solo),
        n_crossed=len(crossed), n_solo=len(solo),
        top=label(top, cells), top_spread=f"{cells[top]['spread3']:.3f}",
        n_dead=len(dead), n_live=len(live), n_native=len(native),
        n_brought=len(brought),
        brought_max=f"{max((cells[g]['spread3'] or 0) for g in brought):.3f}",
        n_worse=len(worse), n_better=len(better), n_moves=len(moves),
        worst=worse[0][1] if worse else "--",
        worst_d=f"{worse[0][0]:+.3f}" if worse else "--",
        best=better[-1][1] if better else "--",
        best_d=f"{better[-1][0]:+.3f}" if better else "--",
    )
    (OUT / "index.html").write_text(page)
    json.dump({"cells": {g: {k: v for k, v in c.items() if k != "r"}
                         | {"rates": c["r"]} for g, c in cells.items()},
               "spread_moves": [{"vid": v, "axis": i, "shipped": a,
                                 "variant": b, "change": d}
                                for d, v, i, a, b in moves]},
              (OUT / "separation.json").open("w"), indent=1)
    print(f"[bverif] wrote {OUT/'index.html'}")
    return 0


TPL = r"""<!doctype html><meta charset="utf-8">
<title>bverif1 model separation -- 2026-09-04</title>
<style>
:root{{--bg:#fcfcfb;--panel:#fff;--ink:#1a1a19;--ink2:#4a4a47;--dim:#8a8a85;
 --line:#e3e3df;--grid:#eeeeea}}
body.dark{{--bg:#1a1a19;--panel:#232322;--ink:#f2f2ef;--ink2:#c9c9c4;
 --dim:#8a8a85;--line:#343432;--grid:#2f2f2d}}
{sw}
body.dark{{{swd}}}
*{{box-sizing:border-box}}
body{{margin:0;padding:26px 30px 60px;background:var(--bg);color:var(--ink);
 font:13px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
 max-width:1000px}}
h1{{font-size:19px;margin:0 0 4px}}
h2{{font-size:14px;margin:34px 0 2px;letter-spacing:.01em}}
p{{color:var(--ink2);margin:6px 0 12px;max-width:78ch}}
.sub{{color:var(--dim);margin:0 0 18px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;
 padding:14px 16px;margin:10px 0 4px}}
.fig{{width:100%;height:auto;display:block;overflow:visible}}
.grid{{stroke:var(--grid);stroke-width:1}}
.sep{{stroke:var(--grid);stroke-width:1}}
.ax{{fill:var(--dim);font-size:9.5px}}
.lab{{fill:var(--ink2);font-size:10.5px;font-family:ui-monospace,monospace}}
.spr{{fill:var(--ink);font-size:11px;font-weight:600;
 font-family:ui-monospace,monospace}}
.val{{fill:var(--dim);font-size:9px}}
.dl{{font-size:10px;font-weight:600;font-family:ui-monospace,monospace}}
.ptitle{{fill:var(--ink2);font-size:10px;font-weight:600;
 font-family:ui-monospace,monospace}}
.pspr{{fill:var(--dim);font-size:9.5px;font-weight:600;
 font-family:ui-monospace,monospace}}
.bar{{transition:opacity .12s}} .bar:hover{{opacity:.7}}
.ln{{fill:none;stroke-width:2}}
.dot{{stroke:var(--panel);stroke-width:1.4}}
.plab{{font-size:8.6px;font-family:ui-monospace,monospace;font-weight:600}}
.ghost{{fill:var(--panel);stroke:var(--dim);stroke-width:2}}
.dbar{{stroke-width:3;opacity:.5;stroke-linecap:round}}
.dbar.wr{{stroke:#ec835a}} .dbar.bt{{stroke:#0ca30c}}
.wrf{{fill:#ec835a}} .btf{{fill:#0ca30c}}
.wrt{{fill:#ec835a}} .btt{{fill:#0ca30c}}
.solid{{stroke:var(--panel);stroke-width:1.6}}
.legend{{display:flex;gap:14px;margin:2px 0 10px;flex-wrap:wrap}}
.lg{{display:flex;align-items:center;gap:6px;font-size:11.5px;
 color:var(--ink2)}}
.sw{{width:11px;height:11px;border-radius:3px;display:inline-block}}
table{{border-collapse:collapse;width:100%;font-size:11.5px;margin-top:6px}}
th,td{{text-align:right;padding:3px 8px;border-bottom:1px solid var(--line);
 font-variant-numeric:tabular-nums}}
th:first-child,td:first-child{{text-align:left;
 font-family:ui-monospace,monospace}}
th{{color:var(--dim);font-weight:600}}
details{{margin:4px 0 0}}
summary{{cursor:pointer;color:var(--dim);font-size:11.5px;padding:4px 0}}
button{{background:var(--panel);color:var(--ink2);border:1px solid var(--line);
 border-radius:6px;padding:4px 10px;font-size:11.5px;cursor:pointer}}
code{{font-family:ui-monospace,monospace;font-size:.94em}}
.fn{{color:var(--dim);font-size:11.5px}}
.key{{display:flex;gap:18px;margin:6px 0 12px;flex-wrap:wrap;font-size:11.5px;
 color:var(--ink2)}}
.key i{{display:inline-block;width:9px;height:9px;border-radius:50%;
 margin-right:5px}}
.key i.g{{background:none;border:2px solid var(--dim);width:7px;height:7px}}
.key i.w{{background:#ec835a}} .key i.b{{background:#0ca30c}}
</style>
<body>
<button onclick="document.body.classList.toggle('dark')">light / dark</button>
<h1>bverif1 &mdash; can the broken-verifier roster separate models?</h1>
<p class="sub">{n_rows} rows &middot; {n_arms} arms ({n_base} baseline cells +
 20 REGIME/GROUP variant arms) &middot; {n_models} models &middot;
 <code>condition=win</code>, <code>arm=hole</code>,
 <code>opponents=selfplay</code>, per-seat reflection, 12 chains, R0&ndash;R3.
 Rates are pooled <code>sum(v)/sum(o)</code>, never a mean of chain rates.</p>
<p class="fn"><b>A caveat that applies to every rate on this page.</b> Under
 <code>selfplay</code> all seats work one finite hole, so
 <code>violations / opportunities</code> falls when a co-seat gets there first
 as well as when a seat fails to find it. That confound is measured separately
 on <a href="discovery.html">the discovery page</a>, which grades each seat's
 own reflection text instead of its rate.</p>
{legend}
<p class="fn">Six series. <code>viz/validate_palette.py</code> passes slots
 1&ndash;6 on the <b>adjacent</b> pairlist in both modes (worst adjacent CVD
 &Delta;E 9.1 light / 8.4 dark against an 8.0 target), which is the pairlist
 grouped bars and non-crossing lines actually use. It does <b>not</b> pass
 all-pairs past three slots, so there is no six-model scatter anywhere on this
 page. Three light-mode slots sit under 3:1 on the surface &mdash; the
 validator calls that <b>relief</b>, not a pass &mdash; so every figure carries
 direct labels and a table view.</p>

<h2>1 &middot; Which cells tell the six models apart</h2>
<p>Ordered by <b>spread</b> &mdash; highest model minus lowest, printed in bold
 beside each cell &mdash; and not by rate. A cell every model saturates and a
 cell every model floors separate equally badly, and a rate-ordered chart puts
 those two at opposite ends where the reader will not compare them.</p>
<p><b>{n_live} of {n_base}</b> baseline cells spread the roster by 0.30 or
 more; <b>{n_dead}</b> spread it by less than 0.10 and separate essentially
 nothing. The sharpest is <code>{top}</code> at <b>{top_spread}</b>, which is
 close to the maximum the statistic can take: four models take that hole on
 almost every opportunity and two never take it at all. That is a clean binary
 split rather than a gradient, and it is worth reading the traces before
 treating it as a capability ranking.</p>
<div class="card">{fig1}</div>
<details><summary>table view &middot; all {n_base} baseline cells, R3 and
 R0</summary>{tab1}</details>

<h2>2 &middot; The seven brought-in checkers separate nothing</h2>
<div class="key"><span><i class="g"></i>scripted exploiter</span>
 <span><i class="w"></i>best of six models</span></div>
<p>{n_brought} of the 23 cards on the verifier report measure an
 <code>hf_*_checker</code> cell, because the shipped substrate has no
 self-report of its own and the checker is a <code>Slip</code> scoresheet
 brought in under a separate cell id. The hollow ring is what a
 <b>scripted</b> exploiter gets; the filled dot is the <b>best</b> of six
 models after four rounds of reflection.</p>
<p><b>The script takes all seven on 100% of opportunities, for +69 to +571
 points, against a 0.000 honest floor.</b> No model goes above
 {brought_max} spread and three sit at exactly 0.000 across all six. This is
 not a parse failure &mdash; none of the seven exceeds 5% invalid. The hole is
 available, large, and untouched, so as built this family contributes seven
 identical zeros and separates no models at all.</p>
<div class="card">{fig2}</div>
<details><summary>table view &middot; scripted reference against every
 model</summary>{tab2}</details>

<h2>3 &middot; Does flipping a knob make a cell BETTER at separating?</h2>
<div class="key"><span><i class="g"></i>shipped arm</span>
 <span><i class="b"></i>variant separates more</span>
 <span><i class="w"></i>variant separates less</span></div>
<p>The plot with no counterpart in any earlier figure set. Thirteen cells were
 sampled as their shipped arm <i>and</i> as one or two knob variants, under one
 wave, one seed block and one prompt ladder &mdash; so the spread of a cell can
 be compared against the spread of the same cell with one constant moved.</p>
<p><b>{n_worse} of {n_moves} variant arms separate the roster LESS than the
 cell they came from</b>, and only {n_better} separate it more. The largest
 loss is <code>{worst}</code> at <b>{worst_d}</b>; the largest gain is
 <code>{best}</code> at <b>{best_d}</b>. Read as advice: the shipped arms are
 mostly already the discriminating ones, and a knob sweep is a way to
 <i>understand</i> a cell rather than a way to find a sharper one &mdash; with
 the handful of exceptions named on the right of the chart, which take cells
 that were nearly dead and give them room.</p>
<p class="fn">Spread is a range statistic over six models, so it moves on one
 model alone and is not a substitute for the arm-vs-baseline deltas in
 <code>RESULTS.md</code>, which are computed per model against a measured
 split-half noise floor. This figure answers a different question: not
 &ldquo;did behaviour change&rdquo; but &ldquo;did the cell get better at
 discriminating&rdquo;.</p>
<div class="card">{fig3}</div>
<details><summary>table view &middot; every variant arm against its shipped
 arm</summary>{tab3}</details>

<h2>4 &middot; The reflection ladder &mdash; every crossed cell and its
 variants</h2>
<p>All {n_panels} arms in the wave get a panel, R0 through R3. One panel per
 arm with the six models as adjacent lines, each labelled at its own endpoint;
 the number at the top right of a panel is that arm&rsquo;s R3 spread. The
 comparison that matters is between models <i>within</i> a panel, which is why
 the models are not split into their own panels.</p>
<p><b>One cell per row, shipped arm always in column 1</b>, its REGIME arms
 next and its GROUP arms after that, blanks padding the short rows. So the
 question section 3 answers with one number &mdash; did the knob change how
 this cell separates &mdash; can be read here as a shape: whether the fan
 opens, closes or reorders when the constant moves. {n_crossed} cells, ordered
 by the spread of their shipped arm.</p>
<p>Reflection is not uniformly an amplifier. Some panels fan out across rounds
 &mdash; the models that were going to find the hole find it and the rest
 settle at zero &mdash; and others converge or decay. A panel already fanned at
 R0 is separating on unprompted discovery; one that only fans by R3 is
 separating on what the model wrote about itself.</p>
<div class="card">{fig4}</div>
<details><summary>table view &middot; every round, every model, all
 {n_crossed} crossed cells</summary>{tab4}</details>

<h2>5 &middot; The reflection ladder &mdash; the uncrossed cells</h2>
<p>The {n_solo} cells with no REGIME or GROUP arm to sit beside: three whose
 shipped cell has no variant in the catalogue
 (<code>ref_auction</code>, <code>ta_kuhn</code>, <code>ta_negotiation</code>)
 and the seven <code>hf_*_checker</code> cells from section 2, which carry no
 variants at all &mdash; the knobs live on the substrate and an
 <code>hf_*</code> wrapper does not inherit them, so applying one would be
 silently inert. Ordered by spread, same axes as section 4.</p>
<p>The seven brought-in panels are the visual form of section 2&rsquo;s
 result: six lines lying on the floor for four rounds, in cells where a
 scripted exploiter takes the hole every single time.</p>
<div class="card">{fig5}</div>
<details><summary>table view &middot; every round for the {n_solo} uncrossed
 cells</summary>{tab5}</details>

<p class="fn" style="margin-top:34px">Generated by
 <code>make_bverif_figs.py</code> from
 <code>results/referee_spartan/bverif1/rows.jsonl</code>. Per-model numbers in
 <code>separation.json</code>; the arm-vs-baseline analysis with its noise
 floor is <code>RESULTS.md</code> beside it; traces for every chain are in the
 trace viewer under the <code>bverif1</code> wave.</p>
"""


if __name__ == "__main__":
    raise SystemExit(main())
