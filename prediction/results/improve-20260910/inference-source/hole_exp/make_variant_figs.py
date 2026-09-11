#!/usr/bin/env python
"""Do VARIANTS of one game induce different behaviour? -- the 0902 PoC, plotted.

    python make_variant_figs.py       # -> results/0902_pilots/variants.html

The prose answer is `research_logs/0902-variant-poc.md`, written with its
predictions BEFORE the wave returned. This is the picture.

A SEPARATE FILE FROM `make_pilot_figs.py` ON PURPOSE. That script is being
edited concurrently by another session and already has its own section 5; two
writers on one file lose each other's work. The marks, palette and table
helpers are IMPORTED from it rather than copied, so there is still one
implementation of each and the two pages cannot drift apart visually.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import make_pilot_figs as MP        # noqa: E402
import referee_spartan as SP        # noqa: E402

OUT = HERE / "results" / "0902_pilots"

PAGE = r"""<!doctype html><meta charset="utf-8">
<title>do variants change behaviour? -- 2026-09-02</title>
<style>
:root{--bg:#fcfcfb;--panel:#fff;--ink:#1a1a19;--ink2:#4a4a47;--dim:#8a8a85;
 --line:#e3e3df;--grid:#eeeeea}
body.dark{--bg:#1a1a19;--panel:#232322;--ink:#f2f2ef;--ink2:#c9c9c4;
 --dim:#8a8a85;--line:#343432;--grid:#2f2f2d}
.s0{fill:#2a78d6} .s1{fill:#eb6834} .s2{fill:#1baf7a}
.s0t{fill:#2a78d6} .s1t{fill:#eb6834} .s2t{fill:#1baf7a}
body.dark .s0{fill:#3987e5} body.dark .s1{fill:#d95926}
body.dark .s2{fill:#199e70}
body.dark .s0t{fill:#3987e5} body.dark .s1t{fill:#d95926}
body.dark .s2t{fill:#199e70}
*{box-sizing:border-box}
body{margin:0;padding:26px 30px 60px;background:var(--bg);color:var(--ink);
 font:13px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
 max-width:1000px}
h1{font-size:19px;margin:0 0 4px}
p{color:var(--ink2);margin:6px 0 12px;max-width:78ch}
.sub{color:var(--dim);margin:0 0 18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;
 padding:14px 16px;margin:10px 0 4px}
.fig{width:100%;height:auto;display:block;overflow:visible}
.grid{stroke:var(--grid);stroke-width:1}
.ax{fill:var(--dim);font-size:9.5px}
.lab{fill:var(--ink2);font-size:10.5px;font-family:ui-monospace,monospace}
.val{fill:var(--dim);font-size:9.5px}
.dl{font-size:10.5px;font-weight:600}
.ptitle{fill:var(--ink2);font-size:11.5px;font-weight:600;
 font-family:ui-monospace,monospace}
.baseline{stroke:var(--dim);stroke-width:1.5;stroke-dasharray:4 3}
.meanbar{opacity:.30} .meanbar.base{fill:var(--dim)}
.chip{stroke:var(--panel);stroke-width:1.5}
.chip.base{fill:var(--dim)}
.s0o,.s1o,.s2o{stroke:var(--ink);stroke-width:2.5}
.s0o{fill:#2a78d6} .s1o{fill:#eb6834} .s2o{fill:#1baf7a}
body.dark .s0o{fill:#3987e5} body.dark .s1o{fill:#d95926}
body.dark .s2o{fill:#199e70}
.axname{font-size:9px;fill:var(--dim)} .baset{fill:var(--dim)}
.legend{display:flex;gap:16px;margin:2px 0 10px;flex-wrap:wrap}
.lg{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--ink2)}
.sw{width:11px;height:11px;border-radius:3px;display:inline-block}
.axlg i.level{background:#2a78d6} .axlg i.rivalry{background:#eb6834}
body.dark .axlg i.level{background:#3987e5}
body.dark .axlg i.rivalry{background:#d95926}
table{border-collapse:collapse;width:100%;font-size:11.5px;margin-top:6px}
th,td{text-align:left;padding:4px 8px;border-bottom:1px solid var(--line);
 font-variant-numeric:tabular-nums}
th{color:var(--dim);font-weight:600;font-size:10px;letter-spacing:.06em;
 text-transform:uppercase}
td:first-child{font-family:ui-monospace,monospace}
details{margin:8px 0 0} summary{cursor:pointer;color:var(--dim);font-size:11px}
.fn{color:var(--dim);font-size:11px;max-width:78ch}
button{position:fixed;top:14px;right:16px;background:var(--panel);
 color:var(--ink2);border:1px solid var(--line);border-radius:7px;
 padding:5px 10px;font-size:11px;cursor:pointer}
</style>
<button onclick="document.body.classList.toggle('dark')">light / dark</button>
<h1>Do variants of the same game induce different behaviour?</h1>
<p class="sub">5 arms &middot; 2 games &middot; gemini-3.7-flash &middot;
 per-seat reflection, neutral, hole arm &middot; pooled R1&ndash;R3 &middot;
 <code>--tag variants_poc</code></p>
<div class="legend axlg">
 <span class="lg"><i class="sw level"></i>level &mdash; payoff magnitude</span>
 <span class="lg"><i class="sw rivalry"></i>rivalry &mdash; a term coupling seats</span>
 <span class="lg" style="color:var(--dim)">dashed rule = the shipped arm</span>
</div>
<p>Each arm is <b>its own cell</b>, differing from its baseline only in one
 knob &mdash; and the knob moves the rules text the model is shown as well as
 the arithmetic it is scored by, which is the whole reason payoff magnitude was
 engine work rather than a flag.</p>
<p><b>Every chain is a dot</b>; the bar is the mean. The finding is about how
 many chains moved, not by how much: at n&nbsp;=&nbsp;4 an effect of &ldquo;one
 chain in four&rdquo; is exactly the resolution floor and cannot be called,
 while &ldquo;every chain below the baseline&rsquo;s lowest&rdquo; can. Dots
 ringed in ink sit at or below the lowest baseline chain.</p>
<div class="card">__FIG__</div>
<details open><summary>table view</summary>__TAB__</details>

<h2 style="font-size:14px;margin:30px 0 2px">What it says</h2>
<p><b>Punishment moved behaviour; prize size did not.</b>
 <code>@steal-5-hard-fail</code> raises what a FAILED raid
 costs from 1 to 6 and cuts the rate by more than half &mdash; 0.650 down to
 0.275, with <b>three of the four chains at or below the baseline&rsquo;s
 lowest chain</b> and the fourth landing exactly on its second-lowest
 (0.533). Stated as &ldquo;all four below the lowest&rdquo; until 2026-09-03,
 which the ringing rule on this very figure contradicts &mdash; it rings
 <code>v &lt;= base_lo</code> and rings three.
 The other half of that comparison is no longer an arm on this page:
 the prize-size knob <code>@hit-8</code>, which doubled what the exploit pays,
 bought only +0.08 &mdash; per chain that is one chain of four flipping into the
 high mode, which this design cannot resolve &mdash; and it was retired on
 2026-09-03 along with the rest of the <code>level</code>/SIZE variants. The two
 knobs were comparable in catalogue units and nowhere near comparable in effect,
 which is the finding; it stands as a past measurement rather than something a
 reader can re-run from the current catalogue.</p>
<p><b>The rivalry arm is a null.</b> <code>@congested</code> tracks its baseline
 within 0.002 across R1&ndash;R3. It was predicted to show no R0 difference
 &mdash; correct, and for the predicted reason &mdash; and then to decay. It
 did not decay.</p>
<p class="fn">Pre-registered with its scoring rules, before the wave returned,
 in <code>research_logs/0902-variant-poc.md</code>. The count prediction there
 (3&nbsp;&rarr;&nbsp;2&nbsp;&rarr;&nbsp;1 seats exploiting) was <b>wrong</b>:
 the hard-fail arm changed <i>intensity</i>, not <i>participation</i> &mdash; about as
 many seats still reach for the hole, and they reach far less often. A count
 was the wrong instrument for it.</p>
<p class="fn">Colours are the dataviz skill&rsquo;s validated categorical slots
 1&ndash;3, checked with <code>viz/validate_palette.py</code> in both modes.
 The baseline is a dashed rule rather than a fourth hue because it is a
 reference, not a category.</p>
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    SP.register_all()
    SP.register_native9()
    SP.register_holecross()
    import variants as V
    V.register()
    # The arms are registered cells only after `register_variant_cells` runs;
    # without this the figure silently plots nothing, because `variant_data`
    # skips any arm not in RG.BY_NAME.
    V.register_variant_cells([
        "gen_quiet_sonar@shipped", "gen_quiet_sonar@loss-5",
        "gen_quiet_sonar@congested",
        "gen_icebound@shipped",
        "gen_icebound@steal-5-hard-fail"])

    data = MP.variant_data()
    if not data:
        print("no variants_poc rows on disk; nothing to plot")
        return 1
    fig = MP.variant_strips(data)
    tab = MP.table(
        ["game", "arm", "axis", "per-chain R1-R3", "mean", "vs baseline"],
        [[g, lab, ax, " ".join(f"{v:.2f}" for v in sorted(per)), f"{mean:.3f}",
          ("baseline" if lab == "@shipped" else
           f"{mean - dict((l, m) for l, _, _, m in arms)['@shipped']:+.3f}")]
         for g, arms in data.items() for lab, ax, per, mean in arms])

    (OUT / "variants.html").write_text(
        PAGE.replace("__FIG__", fig).replace("__TAB__", tab))
    (OUT / "variants.json").write_text(json.dumps(
        {g: [{"arm": l, "axis": a, "chains": p, "mean": m}
             for l, a, p, m in arms] for g, arms in data.items()}, indent=1))
    print(f"wrote {OUT/'variants.html'}")
    print(f"wrote {OUT/'variants.json'}")
    for g, arms in data.items():
        base = dict((l, m) for l, _, _, m in arms)["@shipped"]
        for lab, ax, per, mean in arms:
            d = "" if lab == "@shipped" else f"  {mean-base:+.3f}"
            print(f"  {g:18s} {lab:22s} {ax:9s} mean {mean:.3f}"
                  f"  chains {[round(v,2) for v in sorted(per)]}{d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
