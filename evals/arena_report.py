"""Turn arena_eval.py's JSONs into the two comparisons we actually need.

    python arena_report.py results/arena/*.json

Two questions, two different contrasts over the same table:

  Q1 REPRODUCTION -- fix the protocol AND the algorithm, vary the
     implementation. `local-oat-64` vs `spiral-tinker-64` under the SPIRAL
     protocol: same algorithm, same base model, same step, same rows per step.
     Anything left is the port.

  Q2 ALGORITHM -- fix the protocol AND the implementation, vary the algorithm.
     `spiral-tinker-64` vs `marshal-tinker-48`, both protocols, with
     `base-qwen3-8b` as the untrained reference. Scores on the two protocols are
     on different scales and against different opponents, so what is compared is
     each arm's movement AWAY FROM BASE, not the raw number.

The home/away asymmetry is stated rather than corrected for: each protocol
carries its own prompt convention (SPIRAL suppresses <think>, MARSHAL requires
it), so each arm plays one protocol under the convention it trained on and one
under the other arm's. That is what "same yardstick" costs when the two
algorithms disagree about the prompt. It means a cross-protocol deficit is
partly a format-transfer result, and the invalid-action rate is printed next to
every score so that component stays visible.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ORDER = [
    "base-qwen3-8b",
    "local-oat-64",
    "local-oat-96",
    "spiral-tinker-64",
    "marshal-tinker-48",
    "marshal-tinker-64",
]


def two_prop_z(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float]:
    """(z, two-sided p) for H0: p1 == p2. Normal approx; n here is in the 100s."""
    if n1 == 0 or n2 == 0:
        return (0.0, 1.0)
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return (0.0, 1.0)
    z = (p1 - p2) / se
    p_val = math.erfc(abs(z) / math.sqrt(2))
    return (z, p_val)


def load(paths: list[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for p in paths:
        d = json.loads(Path(p).read_text())
        out[d["label"]] = d
    return out


def _row(label: str, r: dict[str, Any] | None, proto: str) -> str:
    if r is None or proto not in r.get("results", {}):
        return f"  {label:<20} {'--':>28}"
    p = r["results"][proto]["pooled"]
    n = p.get("n_games", p.get("n_episodes", 0))
    ci = p["win_rate_ci95"]
    extra = ""
    if proto == "marshal":
        extra = f"  valid-only {p['mean_return_valid']:+.3f} (n={p['n_valid']})"
    elif "win_rate_clean" in p:
        extra = f"  clean {p['win_rate_clean']:>5.1%} (n={p['n_clean']})"
    return (
        f"  {label:<20} win {p['win_rate']:>6.1%} "
        f"[{ci[0]:>5.1%},{ci[1]:>5.1%}]  ret {p['mean_return']:+.3f}  "
        f"inval {p['invalid_rate']:>5.1%}  n={n}{extra}"
    )


def _pooled_counts(r: dict[str, Any], proto: str) -> tuple[int, int]:
    p = r["results"][proto]["pooled"]
    n = p.get("n_games", p.get("n_episodes", 0))
    return (round(p["win_rate"] * n), n)


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        raise SystemExit(__doc__)
    data = load(paths)
    labels = [x for x in ORDER if x in data] + [
        x for x in sorted(data) if x not in ORDER
    ]

    for proto, blurb in (
        ("spiral", "TextArena KuhnPoker-v1, 5 rounds, vs random  (higher win = "
                   "learned the game; NOT a strength measure -- equilibrium play "
                   "scores lower here)"),
        ("marshal", "OpenSpiel kuhn_poker, 1 hand, vs CFR  (near-Nash: ~50% win "
                    "and return ~0 is the CEILING, not the floor)"),
    ):
        print(f"\n{'=' * 100}\nPROTOCOL: {proto}\n  {blurb}\n{'=' * 100}")
        for lab in labels:
            print(_row(lab, data.get(lab), proto))

    # --- Q1 -----------------------------------------------------------------
    print(f"\n{'=' * 100}\nQ1  DOES TINKER REPRODUCE LOCAL?\n{'=' * 100}")
    a, b = data.get("local-oat-64"), data.get("spiral-tinker-64")
    if a and b:
        for proto in ("spiral", "marshal"):
            if proto not in a["results"] or proto not in b["results"]:
                continue
            k1, n1 = _pooled_counts(a, proto)
            k2, n2 = _pooled_counts(b, proto)
            z, pv = two_prop_z(k1, n1, k2, n2)
            d = k1 / n1 - k2 / n2
            verdict = (
                "consistent (no detectable difference)"
                if pv >= 0.05
                else "DIFFERENT (implementations diverge)"
            )
            print(
                f"  [{proto:<7}] local-oat-64 {k1 / n1:.1%} vs "
                f"spiral-tinker-64 {k2 / n2:.1%}   delta {d:+.1%}  "
                f"p={pv:.3f}  -> {verdict}"
            )
        print(
            "\n  Caveat that no amount of n fixes: oat trains all ~8B parameters,\n"
            "  Tinker trains a rank-32 LoRA. 'Reproduces' here can only mean 'the\n"
            "  port drives the policy to the same place', never 'same update'."
        )
    else:
        print("  need local-oat-64 and spiral-tinker-64")

    # --- Q2 -----------------------------------------------------------------
    print(f"\n{'=' * 100}\nQ2  SPIRAL vs MARSHAL  (movement away from the untrained base)\n{'=' * 100}")
    base = data.get("base-qwen3-8b")
    sp = data.get("spiral-tinker-64")
    ma = data.get("marshal-tinker-64") or data.get("marshal-tinker-48")
    if base and sp and ma:
        ma_label = "marshal-tinker-64" if "marshal-tinker-64" in data else "marshal-tinker-48"
        for proto in ("spiral", "marshal"):
            if any(proto not in d["results"] for d in (base, sp, ma)):
                continue
            kb, nb = _pooled_counts(base, proto)
            ks, ns = _pooled_counts(sp, proto)
            km, nm = _pooled_counts(ma, proto)
            _, p_s = two_prop_z(ks, ns, kb, nb)
            _, p_m = two_prop_z(km, nm, kb, nb)
            home = "SPIRAL" if proto == "spiral" else "MARSHAL"
            print(f"\n  [{proto} protocol -- {home}'s home turf]")
            print(
                f"    base              {kb / nb:>6.1%}\n"
                f"    spiral-tinker-64  {ks / ns:>6.1%}   vs base {ks / ns - kb / nb:+.1%}  p={p_s:.3f}\n"
                f"    {ma_label:<17} {km / nm:>6.1%}   vs base {km / nm - kb / nb:+.1%}  p={p_m:.3f}"
            )
    else:
        print("  need base-qwen3-8b, spiral-tinker-64 and a marshal-tinker-*")

    # --- Q3 -----------------------------------------------------------------
    print(f"\n{'=' * 100}\nQ3  DID IT LEARN THE GAME, OR JUST THE OUTPUT FORMAT?\n{'=' * 100}")
    print(
        "  An invalid action forfeits, so a policy that only fixed its formatting posts a\n"
        "  higher win rate with its card play unchanged. Restricting to games where every\n"
        "  model turn parsed separates the two. If `clean` tracks `all`, it is strategy;\n"
        "  if only `all` moves, the gain is format compliance.\n"
    )
    if base and "spiral" in base["results"]:
        bp = base["results"]["spiral"]["pooled"]
        if "win_rate_clean" in bp:
            bk = round(bp["win_rate_clean"] * bp["n_clean"])
            print(
                f"    {'policy':<20}{'all':>8}{'clean':>9}{'vs base (clean)':>20}"
            )
            for lab in labels:
                d = data.get(lab)
                if not d or "spiral" not in d["results"]:
                    continue
                p = d["results"]["spiral"]["pooled"]
                if "win_rate_clean" not in p:
                    continue
                k = round(p["win_rate_clean"] * p["n_clean"])
                _, pv = two_prop_z(k, p["n_clean"], bk, bp["n_clean"])
                delta = p["win_rate_clean"] - bp["win_rate_clean"]
                tag = "" if lab == "base-qwen3-8b" else f"{delta:+.1%}  p={pv:.3f}"
                print(
                    f"    {lab:<20}{p['win_rate']:>8.1%}{p['win_rate_clean']:>9.1%}"
                    f"{tag:>20}"
                )
        else:
            print("  (re-run arena_eval.py; these JSONs predate the clean-games split)")
    print()


if __name__ == "__main__":
    main()
