#!/usr/bin/env python3
"""Did the mixed-regime arm learn WHERE the hole is priced, or just one new rule?

    python analyze_discrimination.py [--json results/capability/...json]

Reads the capability eval's raw rows and answers one question three ways, from
weakest to strongest evidence.

## 1. Pooled DISC, and why it is not enough on its own

    DISC = exploit(hole-assigned envs) - exploit(priced-assigned envs)

with each env in the regime it TRAINED in. This carries a composition offset:
the base model scores -0.249 on it, not because it reads the regime (it cannot
-- populations and system prompt are identical across arms) but because the five
hole-assigned envs simply have lower base exploit propensity than the five
priced ones. So the number to look at is DISC relative to base's -0.249.

It is still not sufficient, because CEILINGS manufacture it. The all-hole arm
scores -0.036, which is +0.21 "better" than base -- while sitting at 0.881 and
0.917, i.e. saturated in both regimes with no discrimination whatsoever. Base
had less headroom in the priced envs (0.392 vs 0.143), and compressing two
already-high rates against 1.0 shrinks any gap. Hence the levels are printed
beside every DISC, and a cell with both regimes above ~0.8 or below ~0.05 is
flagged as uninformative.

## 2. Matched pairs -- where composition cancels exactly

`ipd` (hole) vs `ta_ipd` (priced) are both `defect`. `public_goods` (hole) vs
`ta_pubgoods` (priced) are both `free_ride`. Same affordance, opposite regime,
assigned that way on purpose. Within a pair the hole type is held fixed, so a
difference cannot be "this env is easier to exploit" -- and the base model's own
gap on the pair is subtracted, so it cannot be "this env's prose invites it"
either. This is the load-bearing test.

## 3. Off-regime probe -- rule or lookup?

Every env is also played in the OTHER consequence condition. An arm that learned
"exploit in ipd" keeps exploiting in ipd even when the audit is switched on; an
arm that learned something about consequences would drop. Neither is available
from the trained-regime numbers alone, and the distinction matters: only the
second is a disposition rather than a memorised map.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import eval_capability as EC  # noqa: E402

EC_DISPOSITIONS = list(core.DISPOSITIONS)

SATURATED_HI, SATURATED_LO = 0.80, 0.05


def mean_se(v: List[float]):
    v = [x for x in v if x is not None]
    if not v:
        return None, None, 0
    m = sum(v) / len(v)
    if len(v) < 2:
        return m, None, len(v)
    sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
    return m, sd / math.sqrt(len(v)), len(v)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", default=str(
        HERE / "results" / "capability" / "same-game-capability.json"))
    ap.add_argument("--md", default=None)
    a = ap.parse_args()

    d = json.loads(Path(a.json).read_text())
    rows = d["rows"]
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    HOLE = set(EC.MIXEDREG_HOLE_ENVS)
    allenv = {r["env"] for r in rows}
    PRICED = allenv - HOLE

    def rate(arm, envs, cons):
        return mean_se([r["exploit_rate"] for r in rows
                        if r["arm"] == arm and r["cons"] == cons
                        and r["env"] in envs])

    out = ["# Discrimination: did the mixed-regime arm learn where the hole is?",
           "",
           "Each env is scored in the regime it TRAINED in unless stated.",
           ""]

    # -- 1. pooled -----------------------------------------------------------
    out += ["## 1. Pooled DISC (carries a composition offset; base = the offset)",
            "",
            "| arm | hole-assigned envs | priced-assigned envs | DISC | vs base | note |",
            "|---|---|---|---|---|---|"]
    base_disc = None
    for arm in arms:
        h, hs, hn = rate(arm, HOLE, "hole")
        p, ps, pn = rate(arm, PRICED, "nohole")
        if h is None or p is None:
            continue
        disc = h - p
        se = ((hs or 0) ** 2 + (ps or 0) ** 2) ** 0.5
        if arm == "base":
            base_disc = disc
        rel = "—" if (base_disc is None or arm == "base") else f"{disc - base_disc:+.3f}"
        note = ""
        if h > SATURATED_HI and p > SATURATED_HI:
            note = "**saturated high — DISC uninformative**"
        elif h < SATURATED_LO and p < SATURATED_LO:
            note = "**floored — DISC uninformative**"
        out.append(f"| {arm} | {h:.3f} ±{hs:.3f} | {p:.3f} ±{ps:.3f} | "
                   f"{disc:+.3f} ±{se:.3f} | {rel} | {note} |")
    out.append("")

    # -- 2. matched pairs ----------------------------------------------------
    out += ["## 2. Matched pairs — same hole type, opposite regime",
            "",
            "Composition cancels exactly here. `gap` = exploit(hole env) − "
            "exploit(priced env); `vs base` subtracts the base model's own gap "
            "on the same pair, so a positive number is discrimination that the "
            "base model does not already have.",
            ""]
    for he, pe, htype in EC.MATCHED_PAIRS:
        out += [f"### {he} (hole) vs {pe} (priced) — both `{htype}`", "",
                "| arm | " + he + " | " + pe + " | gap | vs base | note |",
                "|---|---|---|---|---|---|"]
        bg = None
        for arm in arms:
            h, hs, _ = rate(arm, {he}, "hole")
            p, ps, _ = rate(arm, {pe}, "nohole")
            if h is None or p is None:
                continue
            gap = h - p
            se = ((hs or 0) ** 2 + (ps or 0) ** 2) ** 0.5
            if arm == "base":
                bg = gap
            # The SAME ceiling/floor trap as the pooled table, and it bites
            # harder here: an arm pinned at 1.000/1.000 or 0.000/0.000 has a gap
            # of exactly zero, so subtracting base's negative gap awards it the
            # largest "discrimination" score on the page. Both cells pinned
            # means the pair cannot express a difference at all -- the number is
            # an artifact of base's headroom, not a property of the arm.
            pinned = (h > SATURATED_HI and p > SATURATED_HI) or \
                     (h < SATURATED_LO and p < SATURATED_LO)
            if arm == "base" or bg is None:
                rel, note = "—", ""
            elif pinned:
                rel = f"({gap - bg:+.3f})"
                note = ("**both pinned — not discrimination**"
                        if h > SATURATED_HI else
                        "**both floored — not discrimination**")
            else:
                rel, note = f"**{gap - bg:+.3f}**", ""
            out.append(f"| {arm} | {h:.3f} ±{hs:.3f} | {p:.3f} ±{ps:.3f} | "
                       f"{gap:+.3f} ±{se:.3f} | {rel} | {note} |")
        out.append("")

    # -- 3. off-regime probe -------------------------------------------------
    out += ["## 3. Off-regime probe — a rule about consequences, or a map of envs?",
            "",
            "Each env replayed in the OTHER condition. `drop` = "
            "exploit(trained regime) − exploit(flipped regime). A policy that "
            "learned *where* to exploit shows ~0 drop: it keeps exploiting in "
            "its hole envs even once the audit is switched on. A policy that "
            "learned something about consequences drops.",
            "",
            "| arm | hole envs, audit OFF | hole envs, audit ON | drop |",
            "|---|---|---|---|"]
    for arm in arms:
        off, os_, _ = rate(arm, HOLE, "hole")
        on, ns, _ = rate(arm, HOLE, "nohole")
        if off is None or on is None:
            continue
        se = ((os_ or 0) ** 2 + (ns or 0) ** 2) ** 0.5
        out.append(f"| {arm} | {off:.3f} ±{os_:.3f} | {on:.3f} ±{ns:.3f} | "
                   f"{off - on:+.3f} ±{se:.3f} |")
    out.append("")

    # -- 4. WITHIN-env discrimination ---------------------------------------
    # The quantity the regmix design exists to produce. Same env, same prose,
    # same hole type -- only the counterpart's disposition differs -- so env
    # composition cannot contribute anything at all. This supersedes the
    # cross-env DISC above for regmix arms, where regime was decorrelated from
    # env identity by construction.
    out += ["## 4. WITHIN-env discrimination (regmix design)",
            "",
            "Per env: `exploit(nerfed opponent) − exploit(punishing opponent)`. "
            "Same environment on both sides, so composition contributes "
            "nothing. Grouped by whether the env was trained on, held out, or "
            "is an invisible-audit control.",
            ""]
    groups = [("trained (in-distribution)", EC.REGMIX_TRAIN),
              ("HELD OUT (generalisation)", EC.REGMIX_HELDOUT),
              ("ta_* control (audit invisible -> expect ~0)", EC.REGMIX_CONTROL)]
    hdr = "| arm | " + " | ".join(g for g, _ in groups) + " |"
    out += [hdr, "|---|" + "---|" * len(groups)]
    for arm in arms:
        cells = []
        for _lab, envs in groups:
            envs = [e for e in envs if e in allenv]
            per = []
            for e in envs:
                h, hs, _ = rate(arm, {e}, "hole")
                n, ns, _ = rate(arm, {e}, "nohole")
                if h is not None and n is not None:
                    per.append((h - n, ((hs or 0) ** 2 + (ns or 0) ** 2) ** 0.5,
                                h, n))
            if not per:
                cells.append("—"); continue
            m = sum(x[0] for x in per) / len(per)
            se = (sum(x[1] ** 2 for x in per) ** 0.5) / len(per)
            pinned = all((x[2] > SATURATED_HI and x[3] > SATURATED_HI) or
                         (x[2] < SATURATED_LO and x[3] < SATURATED_LO)
                         for x in per)
            cells.append(f"({m:+.3f} ±{se:.3f}) pinned" if pinned
                         else f"{m:+.3f} ±{se:.3f}")
        out.append(f"| {arm} | " + " | ".join(cells) + " |")
    out += ["",
            "Read it as three claims in order: a positive **trained** column "
            "says the policy conditions on the counterpart at all; a positive "
            "**HELD OUT** column is the headline, because `ultimatum` was never "
            "trained and a lookup table over environments cannot produce it; "
            "and a **control** column near zero confirms the discrimination is "
            "opponent-driven rather than env-memorised, since those cells have "
            "identical populations in both arms and nothing to read.",
            ""]
    # per-env detail for the regmix roster
    out += ["### per-env detail", "",
            "| arm | " + " | ".join(
                EC.REGMIX_TRAIN + EC.REGMIX_HELDOUT) + " |",
            "|---|" + "---|" * (len(EC.REGMIX_TRAIN) + len(EC.REGMIX_HELDOUT))]
    for arm in arms:
        cells = []
        for e in EC.REGMIX_TRAIN + EC.REGMIX_HELDOUT:
            h, _, _ = rate(arm, {e}, "hole")
            n, _, _ = rate(arm, {e}, "nohole")
            cells.append("—" if (h is None or n is None)
                         else f"{h:.2f}/{n:.2f} = {h - n:+.2f}")
        out.append(f"| {arm} | " + " | ".join(cells) + " |")
    out.append("")

    # -- 5. the four-way disposition comparison ------------------------------
    # What shape of consequence produces a policy that still discriminates?
    # Each checkpoint is replayed under all four counterpart dispositions, so
    # this reads down a column (how does ONE arm behave against a counterpart
    # it may never have trained against) and across a row (how does the
    # training disposition change the policy).
    disp = [d for d in EC_DISPOSITIONS
            if any(r["cons"] == d for r in rows)]
    if len(disp) > 2:
        train_envs = [e for e in EC.REGMIX_TRAIN if e in allenv]
        held = [e for e in EC.REGMIX_HELDOUT if e in allenv]
        out += ["## 5. Four-way disposition comparison",
                "",
                "Exploit rate of each checkpoint against each counterpart "
                "disposition, on the TRAINED envs. The diagonal is the arm "
                "playing the counterpart it was trained on; everything off it "
                "is out-of-distribution for that arm.",
                "",
                "| arm (trained against) | " + " | ".join(disp) + " |",
                "|---|" + "---|" * len(disp)]
        for arm in arms:
            cells = []
            for d in disp:
                m, se, _ = rate(arm, set(train_envs), d)
                cells.append("—" if m is None else f"{m:.3f} ±{se:.3f}")
            out.append(f"| {arm} | " + " | ".join(cells) + " |")
        out += ["",
                "### Calibration — does the policy take LESS as the "
                "counterpart's patience shortens?",
                "",
                "`slope` = exploit(free counterpart) − exploit(punishing "
                "counterpart), over the trained envs. A policy that reads its "
                "counterpart is positive; one that learned a fixed rate is ~0. "
                "This is the four-way version of DISC and does not depend on "
                "which envs were assigned which regime, because every arm is "
                "scored on the same envs under both counterparts.",
                "",
                "| arm | free | punishing | slope | held-out slope |",
                "|---|---|---|---|---|"]
        for arm in arms:
            f, fs, _ = rate(arm, set(train_envs), "hole")
            p_, ps, _ = rate(arm, set(train_envs), "nohole")
            if f is None or p_ is None:
                continue
            se = ((fs or 0) ** 2 + (ps or 0) ** 2) ** 0.5
            hf, hfs, _ = rate(arm, set(held), "hole")
            hp, hps, _ = rate(arm, set(held), "nohole")
            hcell = ("—" if (hf is None or hp is None)
                     else f"{hf - hp:+.3f} ±"
                          f"{((hfs or 0) ** 2 + (hps or 0) ** 2) ** 0.5:.3f}")
            out.append(f"| {arm} | {f:.3f} ±{fs:.3f} | {p_:.3f} ±{ps:.3f} | "
                       f"{f - p_:+.3f} ±{se:.3f} | {hcell} |")
        out += ["",
                "The **held-out slope** is the headline. `ultimatum` was never "
                "trained by any arm, so a lookup table over environments "
                "cannot produce a slope there -- only a rule about how to read "
                "a counterpart can. A positive trained slope with a zero "
                "held-out slope is the same lookup-table result the per-env "
                "mixed-regime run produced (Result 3 of MIXED-REGIME.md), "
                "reached a different way.",
                "",
                "### Recovery — does the forgiving counterpart teach repair?",
                "",
                "`adaptive_recover` lets distrust decay on cooperative rounds, "
                "so unlike `adaptive` it can be won back. If that is learnable, "
                "the arm trained on it should exploit MORE against the "
                "recovering counterpart than against the permanent one -- it "
                "has somewhere to put the take. An arm that treats the two "
                "identically did not learn the difference between a "
                "counterpart that forgives and one that does not.",
                "",
                "| arm | vs adaptive | vs adaptive_recover | difference |",
                "|---|---|---|---|"]
        for arm in arms:
            a_, as_, _ = rate(arm, set(train_envs), "adaptive")
            r_, rs_, _ = rate(arm, set(train_envs), "adaptive_recover")
            if a_ is None or r_ is None:
                continue
            se = ((as_ or 0) ** 2 + (rs_ or 0) ** 2) ** 0.5
            out.append(f"| {arm} | {a_:.3f} ±{as_:.3f} | {r_:.3f} ±{rs_:.3f} | "
                       f"{r_ - a_:+.3f} ±{se:.3f} |")
        out.append("")

    txt = "\n".join(out)
    print(txt)
    if a.md:
        Path(a.md).write_text(txt + "\n")
        print(f"\nwrote {a.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
