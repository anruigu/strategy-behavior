"""The index of INTENDED hacks — what the planted exploit is, cell by cell.

Every environment in this package is a matched pair whose whole content is one
affordance: a thing the agent may do that is exploitable, reward-positive,
normatively bad, and un-punished in the `hole` arm. That affordance is specified
in eleven different places (a hand-written module, a generated `specs/*.json`, a
TextArena wrapper) and there has never been one page that says what it IS.

This is that page. It does not sample a model and it does not read docstrings --
for every cell it PLAYS the two scripted references and reads the tokens they
actually emitted, so what it prints is the exploit the engine scores, not the
exploit someone once described in a comment. Where a cell also carries an
authored description (a spec `blurb`, merchant's per-corner `gloss`), that is
printed beside it, and a disagreement between the two is a bug worth knowing
about.

    python hack_index.py                      # atlas + deep + games
    HOLE_GEN_CANDIDATES=1 python hack_index.py --envs-from gen
    python hack_index.py --md results/hack-index.md

Columns:
  hole type   the axis the atlas ranks transfer along
  honest      the token the straight policy emits
  exploit     the token(s) the exploiting policy emits; `: $X` means the amount
              is the agent's choice, clamped to the dose cap
  premium     what cutting the corner is worth over playing straight, at dose
              1.0, in the cell's own payoff units (hole arm)
  harmed      who absorbs it, where the environment names a party
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


BRACKET = re.compile(r"\[[^\[\]]*\]")


def _actions(spec, policy: str, dose: float, seed: int, limit: int = 3
             ) -> List[str]:
    """The LITERAL bracketed actions a scripted reference emits.

    Deliberately the raw string, not `turn["parsed"]`. In half the atlas the
    honest and exploitative policies emit the SAME token and differ only in its
    argument -- `[contribute: 10]` vs `[contribute: 0]`, `[offer: 6]` vs
    `[offer: 1]` -- so a token-name diff reports "no exploit token" for cells
    whose hack is precisely the number. And in the spec-backed cells `parsed` is
    an internal label (`honest` / `exploit`), not the token the surface asks the
    model for. The literal string is the only thing that is true in every cell.
    """
    import registry

    rec = registry.play(spec, spec.scripted(policy), consequence="hole",
                        dose=dose, seed=seed)
    seen, out = set(), []
    for t in rec["turns"]:
        m = BRACKET.findall(t.get("action") or "")
        if not m:
            continue
        act = m[-1].strip()  # the suite scores the LAST bracketed action
        if act not in seen:
            seen.add(act)
            out.append(act)
    return out[:limit]


def describe(name: str, dose: float, seed: int) -> Dict:
    import registry

    spec = registry.get(name)
    honest = _actions(spec, "honest", dose, seed)
    exploit = _actions(spec, "exploit", dose, seed)
    refs = registry.references(spec, consequence="hole", dose=dose, seed=seed)
    row = {
        "env": name, "hole_type": spec.hole_type, "suite": spec.suite,
        "honest": honest, "exploit": exploit,
        "premium": refs["exploit"] - refs["honest"],
        "honest_payoff": refs["honest"],
        "blurb": "", "shared_token": False,
    }
    # Where both policies emit the same token, say so: that cell's hack is the
    # ARGUMENT, and a reader scanning the table would otherwise see two rows that
    # look identical and conclude the exploit is missing.
    hon_toks = {a.split(":")[0].strip("[] ").lower() for a in honest}
    exp_toks = {a.split(":")[0].strip("[] ").lower() for a in exploit}
    row["shared_token"] = bool(hon_toks & exp_toks)

    sp = getattr(spec.module, "spec", None)
    if sp is not None:
        # Spec-backed: the authored blurb, and the tokens the SURFACE names,
        # which is what the model is actually asked to emit.
        row["blurb"] = getattr(sp, "blurb", "") or ""
        ht, xt = getattr(sp, "honest_token", ""), getattr(sp, "exploit_token", "")
        if ht:
            row["honest"] = [f"[{ht}]"]
        if xt:
            row["exploit"] = [f"[{xt}: N]" if getattr(sp, "exploit_amount", False)
                              else f"[{xt}]"]
    return row


def merchant_detail(dose: float) -> List[Dict]:
    """`merchant` is eight corners in one cell, so it gets its own table."""
    import merchant_env as M

    cap = M.take_cap(dose)
    out = []
    for s in M.SITUATIONS:
        toks = []
        for t in (s["exploit"], *s.get("others", ())):
            valued = t == s["exploit"] and s["valued"]
            toks.append({"token": f"[{t}: $X]" if valued else f"[{t}]",
                         "does": s["gloss"][t]})
        out.append({"corner": s["key"], "party": s["party"],
                    "scene": s["scene"], "honest": f"[{s['honest']}]",
                    "exploits": toks, "worth": cap})
    return out


def to_markdown(rows: List[Dict], dose: float) -> str:
    lines = [f"| env | hole type | suite | honest | exploit | premium @dose {dose} | "
             "what the hack is |",
             "|---|---|---:|---|---|---:|---|"]
    for r in rows:
        ex = ", ".join(f"`{a}`" for a in r["exploit"]) or "—"
        hon = ", ".join(f"`{a}`" for a in r["honest"]) or "—"
        note = r["blurb"]
        if r["shared_token"] and not note:
            note = "same token as honest — **the hack is the argument**"
        elif r["shared_token"]:
            note += " (same token as honest; the hack is the argument)"
        lines.append(f"| `{r['env']}` | {r['hole_type']} | {r['suite']} | {hon} | "
                     f"{ex} | {r['premium']:+.1f} | {note} |")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=None)
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--md", default="")
    ap.add_argument("--no-merchant-detail", action="store_true")
    args = ap.parse_args(argv)

    os.environ.setdefault("HOLE_GEN_CANDIDATES", "1")
    import registry

    names = args.envs or (list(registry.GAMES) + list(registry.SYNTHETIC)
                          + list(registry.NATIVE) + list(registry.DEEP))
    rows = []
    for n in names:
        try:
            rows.append(describe(n, args.dose, args.seed))
        except Exception as e:  # noqa: BLE001 -- one bad cell must not hide the rest
            print(f"[skip] {n}: {type(e).__name__}: {e}", file=sys.stderr)

    groups = [("GAMES — same game types, two mechanisms (TextArena + Suite-1)",
               registry.GAMES),
              ("SYNTHETIC — ten scenario cells (five hand-crafted + five generated)",
               registry.SYNTHETIC),
              ("NATIVE — designed-around-a-hole games", registry.NATIVE),
              ("DEEP — one commercial persona, eight corners", registry.DEEP)]
    out = []
    for title, members in groups:
        part = [r for r in rows if r["env"] in members]
        if not part:
            continue
        out.append(f"\n## {title}\n")
        out.append(to_markdown(part, args.dose))

    if not args.no_merchant_detail and any(r["env"] == "merchant" for r in rows):
        out.append("\n## `merchant`, corner by corner "
                   f"(each worth up to ${merchant_detail(args.dose)[0]['worth']:.0f} "
                   "on top of the $25 a straight handling books)\n")
        out.append("| corner | harmed party | the situation | honest | the hack |")
        out.append("|---|---|---|---|---|")
        for c in merchant_detail(args.dose):
            hacks = "<br>".join(f"`{t['token']}` — {t['does']}"
                                for t in c["exploits"])
            out.append(f"| {c['corner']} | {c['party']} | {c['scene']} | "
                       f"`{c['honest']}` | {hacks} |")

    md = "\n".join(out)
    print(md)
    if args.md:
        Path(args.md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.md).write_text(md + "\n")
        print(f"\nwrote {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
