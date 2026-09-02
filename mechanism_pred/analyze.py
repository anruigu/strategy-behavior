#!/usr/bin/env python3
"""Aggregate a wave's rows.jsonl into the tables the log quotes.

Every prediction metric is printed beside its two references on the same row:
`first-best` (the mechanical null that assumes the efficient allocation just
happens) and `ceiling` (how well one realization of the same setting predicts
another). A prediction number alone says nothing -- 0.6 top-1 is excellent
against a 0.55 ceiling and poor against a 0.95 one.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
from typing import Any, Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent

METRICS = [("top1", "top-1", 3), ("pairwise_acc", "pairwise", 3),
           ("gain_nmae", "gain NMAE", 3), ("eff_err", "eff err", 3),
           ("trade_err", "trade err", 2), ("focal_hit", "focal res", 3),
           ("focal_holder_hit", "focal holder", 3),
           ("tag_jaccard", "tactic J", 3),
           ("strategy_score", "strategy", 3), ("mechanism_score", "mechanism", 3)]


def mean(xs: List[Optional[float]]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def sem(xs: List[Optional[float]]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return None
    return statistics.stdev(xs) / (len(xs) ** 0.5)


def fmt(x, nd=3):
    return "  --  " if x is None else f"{x:.{nd}f}"


def block(title: str, rows: List[Dict[str, Any]], keyfn) -> str:
    groups: Dict[Any, List[Dict]] = {}
    for r in rows:
        groups.setdefault(keyfn(r), []).append(r)
    hdr = f"| {title} | n | " + " | ".join(lbl for _, lbl, _ in METRICS) + " |"
    sep = "|" + "---|" * (len(METRICS) + 2)
    out = [hdr, sep]
    for k in sorted(groups, key=str):
        g = groups[k]
        for src, tag in (("pred", ""), ("ceiling", " *(ceiling)*"),
                         ("first_best", " *(null: first-best)*"),
                         ("no_trade", " *(null: no-trade)*")):
            cells = []
            for m, _, nd in METRICS:
                vals = [(r.get(src) or {}).get(m) for r in g]
                cells.append(fmt(mean(vals), nd))
            out.append(f"| {k}{tag} | {len(g)} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def tag_baseline(rows: List[Dict[str, Any]]) -> str:
    """Base rates of each realized tag, and the score of predicting the modal set.

    A tactic vocabulary is only informative if the judge actually spreads it
    across the menu. When one tag lands on nearly every seat, tag overlap
    rewards a forecast for naming it and says nothing about whether the
    forecaster modelled THIS setting. The modal-set row is the null that makes
    the models' `tactic J` readable: it is what a forecaster scores by ignoring
    the setting entirely and guessing the wave's most common tags for every
    seat, with the set size matched to the judge's own mean tags-per-seat so it
    is not handed an unfair Jaccard advantage by guessing more or fewer.
    """
    from collections import Counter
    seats, cnt = 0, Counter()
    for r in rows:
        for e in r["realized"]:
            for tg in (e["tags"] or {}).values():
                seats += 1
                cnt.update(set(tg))
    if not seats:
        return "(no annotated seats)"
    k = round(sum(cnt.values()) / seats)
    modal = [t for t, _ in cnt.most_common(k)]

    from tags import jaccard
    js = [jaccard(modal, tg) for r in rows for e in r["realized"]
          for tg in (e["tags"] or {}).values()]
    out = [f"Annotated seats: {seats}. Judge applies {sum(cnt.values())/seats:.2f} tags/seat.",
           "", "| tag | base rate |", "|---|---|"]
    out += [f"| {t} | {c/seats:.3f} |" for t, c in cnt.most_common()]
    out += ["", f"**Modal-set null** (always predict `{', '.join(modal)}`): "
                f"tactic J = **{mean(js):.3f}**  <- the models' `tactic J` must beat this."]
    return "\n".join(out)


def play_block(rows: List[Dict[str, Any]]) -> str:
    out = ["| model | regime | eff | trades | invalid/ep | special capture | top-1 stability |",
           "|---|---|---|---|---|---|---|"]
    groups: Dict[Any, List[Dict]] = {}
    for r in rows:
        groups.setdefault((r["model"], r["regime"]), []).append(r)
    for k in sorted(groups):
        g = groups[k]
        eff, tr, inv, cap, stab = [], [], [], [], []
        for r in g:
            for e in r["realized"]:
                eff.append(e["efficiency"])
                tr.append(e["n_trades"])
                inv.append(sum(e["invalid_tokens"].values()))
                if r["special_party"] is not None and e["special_share"] is not None:
                    cap.append(float(e["special_holder"] == r["special_party"]))
                elif e["special_share"] is not None:
                    cap.append(e["special_share"])
            stab.append((r.get("ceiling") or {}).get("top1"))
        out.append(f"| {k[0]} | {k[1]} | {fmt(mean(eff))} | {fmt(mean(tr),1)} | "
                   f"{fmt(mean(inv),2)} | {fmt(mean(cap))} | {fmt(mean(stab))} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.wave)
    if not out.is_absolute():
        out = HERE / "results" / a.wave
    src = out / "rows.jsonl"
    if not src.exists():  # a wave still in flight has cells but no rows file yet
        rows = [json.loads(p.read_text())["row"] for p in sorted((out / "cells").glob("*.json"))]
    else:
        rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    if not rows:
        print("no rows")
        return 1

    bad = [r for r in rows if not r["prediction_ok"]]
    print(f"# {out.name}: {len(rows)} cells, {len(bad)} unparseable predictions\n")
    print("## By model\n")
    print(block("model", rows, lambda r: r["model"]), "\n")
    print("## By regime\n")
    print(block("regime", rows, lambda r: r["regime"]), "\n")
    print("## By model x regime\n")
    print(block("cell", rows, lambda r: f"{r['model']}/{r['regime']}"), "\n")
    print("## Realized play\n")
    print(play_block(rows))
    print("\n## Tactic base rates and the modal-set null\n")
    print(tag_baseline(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
