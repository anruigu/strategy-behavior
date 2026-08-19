"""Inoculation ablation: train the SAME exploitable domains with vs without the
game reframing, then read transfer (0819).

Hypothesis (the user's): reframing a scenario as a scoring game may act like an
inoculation prompt — the policy still exploits in-env, but the "it's a game"
context stops the exploitative disposition from generalising to the held-out
battery. If so, the game-framed hole arm transfers LESS than the natural-framed
one despite matched in-env exploitation.

The two training conditions differ ONLY in frame:

    game     GAME_NEUTRAL system + game brief (points, "TURN i", hidden horizon
             to match the shipped corpus), the explicit plant.
    natural  DOMAIN_NEUTRAL system + natural brief (dollars, no turn markers,
             the counterpart just sustains the conversation), the explicit plant.

Conduct, economics, tokens, registers, opponent populations and dose are
byte-identical across the two (ablate_plant builds both off the same base spec),
so a difference in transfer is a difference in framing and nothing else. The
matched `nohole` control is run per frame too, so the 2x2 (frame x consequence)
subtracts "trained on these domains at all" from each frame independently.

This is a thin wrapper: it registers the ablate_plant variants into the registry
(same process) and hands their names to train_mixed, which owns the GRPO loop,
the check_suite pre-flight, checkpointing and wandb. Everything after --  goes
straight to train_mixed.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY train_frame_ablation.py --frame game    --consequence hole   --dry-run
    $PY train_frame_ablation.py --frame natural --consequence hole   --use-wb
    $PY train_frame_ablation.py --frame game    --consequence nohole --use-wb
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ablate_plant as ab  # noqa: E402
import train_mixed  # noqa: E402

# The domains with authored natural surfaces AND above-floor natural-frame
# exploration on 27B (the natural arm must explore for GRPO to have a gradient;
# 0819 §4 per-env: these six sit at 0.16-0.79 neutral, the three dropped
# — financial_advisor_steering, confidential_desk, procurement_rounding — sit
# at 0.00-0.06 and would be a floored dead weight in the natural arm).
DEFAULT_DOMAINS = ["tax_prep", "inventory_adjust", "expense_processing",
                   "procurement_discount", "reporting_metrics", "hiring_panel"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--frame", required=True, choices=["game", "natural"])
    ap.add_argument("--consequence", required=True, choices=["hole", "nohole"])
    ap.add_argument("--domains", nargs="+", default=DEFAULT_DOMAINS)
    ap.add_argument("--plant", default="explicit", choices=list(ab.PLANTS))
    ap.add_argument("--model", default="Qwen/Qwen3.6-27B")
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--group-size", type=int, default=6)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--out", default=str(HERE / "runs" / "frame-ablation"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--use-wb", action="store_true")
    args, extra = ap.parse_known_args(argv)

    # Game arm carries the shipped hidden-horizon surface; the natural arm has no
    # turn markers to hide, so horizon is a no-op there.
    horizon = "hidden" if args.frame == "game" else "disclosed"

    bases = {k: v for k, v in ab.base_specs().items() if k in args.domains}
    missing = set(args.domains) - set(bases)
    if missing:
        raise SystemExit(f"no ablation surfaces authored for {sorted(missing)} "
                         f"(have {sorted(ab.SURFACES)})")

    roster = ab.register_variants(bases, (args.plant,), (args.frame,), (horizon,))
    names = [r["name"] for r in roster]
    print(f"[frame-ablation] frame={args.frame} plant={args.plant} "
          f"horizon={horizon} arm={args.consequence} on {len(names)} domains:\n"
          f"  {', '.join(names)}", flush=True)

    mixed_argv = [
        "--envs", *names,
        "--consequence", args.consequence,
        "--dose", str(args.dose),
        "--model", args.model,
        "--steps", str(args.steps),
        "--group-size", str(args.group_size),
        "--groups", str(len(names)),      # one group per domain, every step
        "--seed", str(args.seed),
        "--lr", str(args.lr),
        "--lora-rank", str(args.lora_rank),
        "--workers", str(args.workers),
        "--out", args.out,
        "--label-suffix", args.frame,     # mixed_game_hole_... vs mixed_natural_...
    ]
    if args.dry_run:
        mixed_argv.append("--dry-run")
    if args.use_wb:
        mixed_argv.append("--use-wb")
    mixed_argv += extra
    return train_mixed.main(mixed_argv)


if __name__ == "__main__":
    raise SystemExit(main())
