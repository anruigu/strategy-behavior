"""Cross-seed report for the inoculation battery (0819 §7 follow-up).

The nail: MACHIAVELLI violations.Σ, per-game paired, pooled across seeds.
  game treatment effect   = game_hole   - game_nohole   (per game)
  natural treatment effect= natural_hole - natural_nohole (per game)
  INOCULATION DiD         = natural effect - game effect  (per game) ; a paired
                            Wilcoxon over all (game x seed) rows tests whether
                            the game frame transfers LESS. DiD>0 => reframing
                            inoculates.
Plus best-effort TRAIT / reward-hack / EM / capability tabs from whatever the
battery has written per arm.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MACH_EPS", "5")
sys.path.insert(0, "/workspace/allie/ipd_exp")

R = Path("/workspace/allie/ipd_exp/traits_results")
SEEDS = os.environ.get("SEEDS", "0 1 2").split()
FRAMES = ("game", "natural")


def mach_report() -> str:
    try:
        import analyze_mach_n5 as A
        import pandas as pd
        from scipy.stats import wilcoxon
    except Exception as e:  # noqa: BLE001
        return f"MACHIAVELLI report unavailable: {e}"

    def per_game(arm):
        d = A.load(arm)
        if d is None or len(d) == 0 or "violations.Σ" not in getattr(d, "columns", []):
            return None
        return d.groupby("game")["violations.Σ"].mean()

    lines = ["## MACHIAVELLI violations.Σ — inoculation DiD across seeds", ""]
    did_rows = []          # per-(seed,game) DiD
    per_seed = []
    for seed in SEEDS:
        arms = {f"{f}_{c}": f"frame-{f}_{c}-s{seed}" for f in FRAMES for c in ("hole", "nohole")}
        pg = {k: per_game(v) for k, v in arms.items()}
        if any(v is None for v in pg.values()):
            lines.append(f"- seed {seed}: incomplete (missing arms), skipped")
            continue
        idx = set(pg["game_hole"].index)
        for v in pg.values():
            idx &= set(v.index)
        idx = sorted(idx)
        g_eff = (pg["game_hole"][idx] - pg["game_nohole"][idx])
        n_eff = (pg["natural_hole"][idx] - pg["natural_nohole"][idx])
        did = (n_eff - g_eff)
        per_seed.append((seed, g_eff.mean(), n_eff.mean(), did.mean()))
        for gname in idx:
            did_rows.append(did[gname])
    if per_seed:
        lines += ["| seed | game effect | natural effect | DiD (nat−game) |",
                  "|---|---:|---:|---:|"]
        for s, g, n, d in per_seed:
            lines.append(f"| {s} | {g:+.2f} | {n:+.2f} | {d:+.2f} |")
        gm = sum(p[1] for p in per_seed) / len(per_seed)
        nm = sum(p[2] for p in per_seed) / len(per_seed)
        dm = sum(p[3] for p in per_seed) / len(per_seed)
        lines.append(f"| **mean** | **{gm:+.2f}** | **{nm:+.2f}** | **{dm:+.2f}** |")
        if did_rows:
            try:
                import statistics as st
                stat, p = wilcoxon(did_rows)
                pos = sum(1 for x in did_rows if x > 0)
                lines += ["",
                          f"Paired Wilcoxon on the per-(game,seed) DiD "
                          f"(n={len(did_rows)}): {pos}/{len(did_rows)} games "
                          f"natural>game, p={p:.4g}. mean DiD={st.fmean(did_rows):+.2f}.",
                          "",
                          "**DiD>0 ⇒ game-reframing transfers less (inoculation).**"]
            except Exception as e:  # noqa: BLE001
                lines.append(f"(wilcoxon failed: {e})")
    else:
        lines.append("no complete seeds yet")
    return "\n".join(lines)


def _read_json(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:  # noqa: BLE001
        return None


def side_tab(title, pattern, keyfn) -> str:
    """Best-effort: one row per arm dir that has the file, value via keyfn."""
    rows = []
    for f in sorted(glob.glob(str(R / "frame-*" / pattern))):
        arm = Path(f).parent.name
        d = _read_json(f)
        if d is None:
            continue
        try:
            v = keyfn(d)
        except Exception:  # noqa: BLE001
            v = "?"
        rows.append((arm, v))
    if not rows:
        return f"## {title}\n\n(not available yet)\n"
    out = [f"## {title}", "", "| arm | value |", "|---|---:|"]
    out += [f"| {a} | {v} |" for a, v in rows]
    return "\n".join(out) + "\n"


def main():
    print("# Frame ablation — full transfer battery (cross-seed)\n")
    print(mach_report())
    print()
    # best-effort side batteries; formats vary, so pull a headline number each
    print(side_tab("TRAIT — Machiavellianism (high-pole %)",
                   "trait*dt*.json",
                   lambda d: round(d.get("Machiavellianism", d.get("mach", "?")), 2)
                   if isinstance(d, dict) else "?"))
    print(side_tab("Reward-hacking rate", "*reward*hack*.json",
                   lambda d: d.get("hack_rate", d.get("rate", "?"))))
    print(side_tab("EM — mean aligned (assistant-facing)", "../em_results/*.json",
                   lambda d: d.get("mean_aligned", d.get("aligned", "?"))))
    print(side_tab("Capability — MMLU", "mmlu.json",
                   lambda d: d.get("accuracy", d.get("acc", "?"))))
    print(side_tab("Capability — HumanEval", "humaneval.json",
                   lambda d: d.get("pass@1", d.get("pass_at_1", "?"))))


if __name__ == "__main__":
    main()
