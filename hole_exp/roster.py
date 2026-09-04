#!/usr/bin/env python
"""The official roster: read it, and assert it agrees with the code.

    python roster.py                 # print the roster and the cuts
    python roster.py --check         # assert file and code agree; exit 1 if not
    python roster.py --games         # bare cell names, for scripting

`configs/roster.toml` is where MEMBERSHIP is argued -- what is on the menu,
what was cut, and the measurement behind each cut. It replaces the count-and-
cut bookkeeping that was being hand-maintained inside
`research_logs/0902-branch-variations.md`, which is a dated PREDICTION document:
a prediction is frozen once written, a roster changes whenever a cell is cut,
and a file asked to be both is guaranteed to be wrong about one of them.

NOTHING IS DERIVED IN EITHER DIRECTION. `referee_spartan.ROSTER` stays a
literal and this only checks the two match, which is the discipline
`_check_dedup_matches` already applies to DEDUP14. Deriving the tuple from the
file would make `--games roster` mean whatever the file says today, and every
tag already on disk would stop describing what was sampled. Deriving the file
from the tuple would lose the reasons, which are the only part a human needs.

So this fails LOUDLY on drift rather than quietly reconciling.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

CONFIG = HERE / "configs" / "roster.toml"


def load(path: pathlib.Path = CONFIG) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def check(cfg: dict) -> list[str]:
    """Every way the file and the code can disagree. Empty list means clean."""
    import referee_spartan as SP
    SP.register_all()
    SP.register_native9()
    SP.register_holecross()
    import referee_games as RG

    bad: list[str] = []
    roster = list(cfg["cells"]["roster"])

    if tuple(roster) != tuple(SP.ROSTER):
        only_f = [c for c in roster if c not in SP.ROSTER]
        only_c = [c for c in SP.ROSTER if c not in roster]
        bad.append(f"roster differs from referee_spartan.ROSTER: "
                   f"only in file {only_f}, only in code {only_c}")

    missing = [c for c in roster if c not in RG.BY_NAME]
    if missing:
        bad.append(f"roster names cells that do not register: {missing}")

    if len(set(roster)) != len(roster):
        dupes = sorted({c for c in roster if roster.count(c) > 1})
        bad.append(f"roster lists a cell twice: {dupes}")

    # A cut cell must be OFF the menu and still REACHABLE -- a cut is not a
    # deletion, and a cut that also removed the engine would silently turn
    # every historical tag naming it into an unrunnable wave.
    for entry in cfg.get("cut", []):
        c = entry["cell"]
        if c in roster:
            bad.append(f"{c} is listed as cut and is still on the roster")
        if c not in RG.BY_NAME:
            bad.append(f"{c} is cut but no longer registers; a cut must leave "
                       f"the cell reachable by name")

    # The hole-fill family: the file's list against the code's tuple, and the
    # base-roster's counts against both. Same discipline as `dedup14_frozen`
    # -- the tuple in `referee_spartan` is the thing waves read, and a config
    # that had drifted from it would name cells no wave could run.
    SP.register_holefill()
    hf = tuple(cfg["families"].get("holefill", ()))
    if hf != tuple(SP.HOLEFILL19):
        bad.append(f"families.holefill differs from "
                   f"referee_spartan.HOLEFILL19: only in file "
                   f"{[c for c in hf if c not in SP.HOLEFILL19]}, only in code "
                   f"{[c for c in SP.HOLEFILL19 if c not in hf]}")
    missing = [c for c in hf if c not in RG.BY_NAME]
    if missing:
        bad.append(f"families.holefill names cells that do not register: "
                   f"{missing}")
    try:
        base = load(HERE / "configs" / "base_roster.toml")
        import engines_holefill as HF
        hfc = base["hole_fill"]
        if hfc["count"] != len(SP.HOLEFILL19):
            bad.append(f"base_roster hole_fill.count {hfc['count']} but the "
                       f"code has {len(SP.HOLEFILL19)}")
        # The family is one kind of hole now, so the count that used to be
        # interesting as a SPLIT is only interesting as a TOTAL: the question
        # the config still has to answer is whether every cell it counts is a
        # cell the engines actually built as nerfed. Checking `nerfed` against
        # the tuple's own length is what makes the config's single number load-
        # bearing -- without it a cell carrying some other KIND could be added
        # to HOLEFILL and both this figure and the count above would still
        # agree with a config that had never heard of it.
        n_nerf = sum(1 for g in HF.HOLEFILL if g.KIND == "nerfed_opponent")
        if hfc["nerfed"] != n_nerf:
            bad.append(f"base_roster hole_fill.nerfed {hfc['nerfed']} but the "
                       f"code has {n_nerf}")
        if n_nerf != len(HF.HOLEFILL):
            other = sorted({g.KIND for g in HF.HOLEFILL
                            if g.KIND != "nerfed_opponent"})
            bad.append(f"engines_holefill.HOLEFILL holds {other} as well as "
                       f"nerfed_opponent, so base_roster's single nerfed "
                       f"figure no longer accounts for the whole family")
        # These are the built-but-not-sampled exclusions -- each config list
        # must mirror its code tuple exactly.
        for key, tup in (
                ("unpaid", HF.HOLEFILL_UNPAID),
                ("late_fine", HF.HOLEFILL_LATE)):
            configured = hfc.get(key)
            if configured is None:
                bad.append(f"base_roster hole_fill.{key} is missing but the "
                           f"code has {list(tup)}")
            elif tuple(configured) != tuple(tup):
                bad.append(f"base_roster hole_fill.{key} {configured} but the "
                           f"code has {list(tup)}")
        kinds = list(base["hole_types"]["kinds"])
        import hole_matrix as HM
        if tuple(kinds) != HM.KINDS:
            bad.append(f"base_roster hole_types.kinds {kinds} but "
                       f"hole_matrix.KINDS is {list(HM.KINDS)}")
        for k in kinds:
            if base["hole_types"][k] != HM.AFFORDANCE[k]:
                bad.append(f"the affordance test for `{k}` differs between "
                           f"base_roster.toml and hole_matrix.AFFORDANCE")
    except FileNotFoundError:
        bad.append("configs/base_roster.toml is missing")

    frozen = tuple(cfg["families"]["dedup14_frozen"])
    if frozen != tuple(SP.DEDUP14):
        bad.append("dedup14_frozen no longer matches referee_spartan.DEDUP14 "
                   "-- that tuple is published and must not move")

    # variants: counts in the file against the measured catalogue
    try:
        import json
        cat = json.loads(
            (HERE.parent / "results" / "0902_variants"
             / "catalogue.json").read_text())
        vs = (cat["variants"] if isinstance(cat["variants"], list)
              else list(cat["variants"].values()))
        menu = [r for r in vs if not r["qc"]["pruned"]]
        pruned = sorted(r["vid"] for r in vs if r["qc"]["pruned"])
        v = cfg["variants"]
        if len(vs) != v["built"]:
            bad.append(f"variants.built {v['built']} but catalogue has {len(vs)}")
        if len(menu) != v["on_menu"]:
            bad.append(f"variants.on_menu {v['on_menu']} but catalogue has "
                       f"{len(menu)}")
        if pruned != sorted(v["pruned_vids"]):
            bad.append(f"pruned_vids disagree with the catalogue: "
                       f"only in file "
                       f"{sorted(set(v['pruned_vids']) - set(pruned))}, "
                       f"only in catalogue "
                       f"{sorted(set(pruned) - set(v['pruned_vids']))}")
        axes: dict = {}
        for r in menu:
            axes[r["axis"]] = axes.get(r["axis"], 0) + 1
        if axes != dict(v["by_axis"]):
            bad.append(f"by_axis {dict(v['by_axis'])} but catalogue has {axes}")
    except FileNotFoundError:
        bad.append("results/0902_variants/catalogue.json is missing -- run "
                   "`python variant_audit.py` before checking variant counts")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--games", action="store_true",
                    help="print the cell names only, space separated")
    a = ap.parse_args()
    cfg = load()

    if a.games:
        print(" ".join(cfg["cells"]["roster"]))
        return 0

    if a.check:
        bad = check(cfg)
        for b in bad:
            print(f"  [DRIFT] {b}")
        print(f"roster {cfg['version']}: "
              + ("OK -- file and code agree" if not bad
                 else f"{len(bad)} DISAGREEMENT(S)"))
        return 1 if bad else 0

    roster = cfg["cells"]["roster"]
    print(f"official roster {cfg['version']}  --  {len(roster)} cells\n")
    fam = {"ref_": "atlas", "gen_": "generated", "ta_": "textarena",
           "hx_": "hole-cross", "nat_": "collaborative"}
    for pre, label in fam.items():
        got = [c for c in roster if c.startswith(pre)]
        if got:
            print(f"  {label:14s} ({len(got):2d})  " + " ".join(got))
    print(f"\ncut ({len(cfg.get('cut', []))}):")
    for e in cfg.get("cut", []):
        first = (e.get("evidence") or "").strip().splitlines()
        print(f"  {e['cell']:20s} {e['date']}  {e['rule']}")
        if first:
            print(f"      {first[0][:96]}")
    v = cfg["variants"]
    print(f"\nvariants: {v['built']} built, {v['on_menu']} on the menu, "
          f"{v['pruned']} pruned   {dict(v['by_axis'])}")
    print("\n`python roster.py --check` asserts this file and the code agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
