"""SFT -> screen -> RL, unattended: the merchant warm-start wave.

The handoff between the warm start and the two RL arms is the part of this
pipeline a human normally has to sit through, and it is three steps of waiting
separated by one decision:

    1. wait for `sft_warmstart.py` to write runs/<label>/warmstart.json
    2. SCREEN every checkpoint it saved (each epoch + final) on merchant,
       neutral prompt, hole arm -- the warm start's own docstring says the
       corpus rate is "an upper bound, not a prediction", so which epoch to seed
       RL from is only answerable by sampling all of them
    3. seed BOTH arms from the ONE checkpoint whose neutral rate lands in
       [TARGET_LO, TARGET_HI] and sits closest to the middle of that window

Step 3 is the decision, and the gate is the point of this script: if no
checkpoint lands in the window it launches NOTHING and says why. An overnight
wave started from a warm start at 0.02 or 0.85 burns the night and produces a
curve nobody can read -- the first because there is still nothing to reinforce,
the second because the control arm is unlearning a maximal prior instead of
diverging from a matched start.

Both arms resume from the SAME checkpoint, which is what keeps the warm start
common-mode and unable to explain any divergence between them (sft_warmstart
docstring). They resume from the **state** path, not the sampler path -- those
are not interchangeable and sampler_weights 404s on resume.

    python launch_merchant_wave.py --label merchant-ws-27b --steps 90
    python launch_merchant_wave.py --label merchant-ws-27b --screen-only
    python launch_merchant_wave.py --label merchant-ws-27b --pick final  # skip the gate
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import sft_warmstart  # noqa: E402  (TARGET_LO / TARGET_HI live there; do not fork)

PY = sys.executable


def wait_for_sft(label: str, timeout_s: int, poll: int = 60) -> Dict:
    """Block until the warm start writes its manifest, or give up loudly."""
    path = HERE / "runs" / label / "warmstart.json"
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        if path.exists():
            time.sleep(2)  # let the write settle
            return json.loads(path.read_text())
        alive = subprocess.run(["pgrep", "-f", f"sft_warmstart.py.*{label}"],
                               capture_output=True).returncode == 0
        if not alive:
            raise SystemExit(
                f"sft_warmstart for {label!r} is not running and {path} does not "
                "exist -- the warm start died before saving. Check "
                f"logs/sft-{label}.log; do not launch RL over the top of this.")
        print(f"[wave] waiting for {path.name} "
              f"({time.time() - t0:.0f}s elapsed)", flush=True)
        time.sleep(poll)
    raise SystemExit(f"timed out after {timeout_s}s waiting for {path}")


def candidates(manifest: Dict) -> List[Dict]:
    """(name, sampler, state) for every checkpoint the warm start saved.

    A checkpoint whose `save_state` failed is dropped rather than offered: it can
    be screened but not resumed, so choosing it would pass the gate and then fail
    the launch -- the exact failure mode sft_warmstart's own comment records from
    the last 27B run.
    """
    out = []
    for ep, sampler in sorted((manifest.get("epoch_checkpoints") or {}).items()):
        state = (manifest.get("epoch_states") or {}).get(ep, "")
        out.append({"name": f"epoch{ep}", "sampler": sampler, "state": state})
    out.append({"name": "final", "sampler": manifest.get("checkpoint", ""),
                "state": manifest.get("state", "")})
    keep = []
    for c in out:
        if not c["sampler"] or str(c["sampler"]).startswith("<"):
            print(f"[wave] drop {c['name']}: no sampler path", flush=True)
        elif not c["state"] or str(c["state"]).startswith("<"):
            print(f"[wave] drop {c['name']}: screenable but NOT resumable "
                  f"({c['state']!r})", flush=True)
        else:
            keep.append(c)
    return keep


def screen(cands: List[Dict], seeds: int, workers: int) -> List[Dict]:
    import screen_merchant

    import tinker
    core.load_env_file()
    sc = tinker.ServiceClient()
    rows = []
    for c in cands:
        row = screen_merchant.cell(c["sampler"], "shipped", "neutral", 1.0,
                                   seeds, workers, 1.0, 384, sc)
        row["ckpt"] = c["name"]
        row["state"] = c["state"]
        rows.append(row)
        print(f"[wave] {c['name']:8s} exploit={row['exploit_rate']:.3f} "
              f"({row['episodes_with_exploit']:.0%} of eps, "
              f"{row['corners_found']}/8 corners) invalid={row['invalid_rate']:.3f}",
              flush=True)
    return rows


def choose(rows: List[Dict]) -> Optional[Dict]:
    lo, hi = sft_warmstart.TARGET_LO, sft_warmstart.TARGET_HI
    mid = (lo + hi) / 2
    ok = [r for r in rows if r["exploit_rate"] is not None
          and lo <= r["exploit_rate"] <= hi]
    if not ok:
        return None
    return min(ok, key=lambda r: abs(r["exploit_rate"] - mid))


def launch(arm: str, state: str, model: str, steps: int, label: str,
           extra: List[str]) -> str:
    """One arm, one process, its own log, its own session.

    setsid rather than nohup: nohup only blocks SIGHUP, so a group-directed
    signal to the launching shell still kills the run (TRAINING_BEST_PRACTICES).
    One invocation per arm, because chained background launches mangle the
    redirect and both arms end up writing one file.
    """
    log = HERE / "logs" / f"rl-{label}-{arm}.log"
    # The tuned tool-loop profile, or the arms train on unparseable turns.
    import tinker_actor
    t = tinker_actor.TUNED_TOOL_SAMPLING
    cmd = [PY, str(HERE / "train_hole.py"), "--env", "merchant",
           "--consequence", arm, "--dose", "1.0", "--model", model,
           "--steps", str(steps), "--resume-from", state,
           "--temperature", str(t["temperature"]), "--top-p", str(t["top_p"]),
           "--max-tokens", str(t["max_tokens"]), "--close-bracket",
           "--use-wb", *extra]
    with open(log, "wb") as fh:
        subprocess.Popen(["setsid", *cmd], stdin=subprocess.DEVNULL,
                         stdout=fh, stderr=subprocess.STDOUT, cwd=str(HERE),
                         start_new_session=True)
    print(f"[wave] launched {arm} -> {log}", flush=True)
    return str(log)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", default="merchant-ws-27b")
    ap.add_argument("--model", default="Qwen/Qwen3.8-27B")
    ap.add_argument("--steps", type=int, default=90)
    ap.add_argument("--seeds", type=int, default=24, help="screen episodes/ckpt")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--wait", type=int, default=6 * 3600,
                    help="seconds to wait for the warm start")
    ap.add_argument("--screen-only", action="store_true",
                    help="screen the checkpoints and stop before launching")
    ap.add_argument("--pick", default="",
                    help="force a checkpoint by name, bypassing the window gate")
    ap.add_argument("--arms", nargs="+", default=["hole", "nohole"],
                    choices=list(core.CONSEQUENCE))
    args, extra = ap.parse_known_args(argv)

    manifest = wait_for_sft(args.label, args.wait)
    print(f"[wave] warm start done: {len(manifest.get('history', []))} epochs, "
          f"corpus rate {manifest.get('corpus_exploit_rate'):.3f}", flush=True)
    for h in manifest.get("history", []):
        print(f"[wave]   epoch {h['epoch']}: train_nll={h['train_nll']:.4f}"
              + (f" val_nll={h['val_nll']:.4f}" if "val_nll" in h else ""),
              flush=True)

    cands = candidates(manifest)
    if not cands:
        raise SystemExit("no resumable checkpoint in the warm start manifest")
    rows = screen(cands, args.seeds, args.workers)

    out = HERE / "results" / f"warmstart-screen-{args.label}.json"
    out.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"[wave] wrote {out}", flush=True)

    if args.pick:
        pick = next((r for r in rows if r["ckpt"] == args.pick), None)
        if pick is None:
            raise SystemExit(f"--pick {args.pick!r} is not one of "
                             f"{[r['ckpt'] for r in rows]}")
    else:
        pick = choose(rows)

    lo, hi = sft_warmstart.TARGET_LO, sft_warmstart.TARGET_HI
    if pick is None:
        print(f"\n[wave] GATE FAILED — no checkpoint lands in [{lo}, {hi}]:",
              flush=True)
        for r in rows:
            print(f"[wave]   {r['ckpt']:8s} {r['exploit_rate']:.3f}", flush=True)
        print("[wave] launching nothing. Re-tune --p-exploit and regenerate the "
              "corpus (up if every checkpoint is below the window, down if "
              "above), or add/remove an epoch.", flush=True)
        return 2

    print(f"\n[wave] chose {pick['ckpt']} (neutral exploit "
          f"{pick['exploit_rate']:.3f}, in [{lo}, {hi}])", flush=True)
    if args.screen_only:
        print("[wave] --screen-only: stopping before launch", flush=True)
        return 0

    logs = {arm: launch(arm, pick["state"], args.model, args.steps,
                        args.label, extra) for arm in args.arms}
    (HERE / "results" / f"wave-{args.label}.json").write_text(json.dumps(
        {"label": args.label, "model": args.model, "steps": args.steps,
         "warmstart": manifest.get("checkpoint"), "chosen": pick["ckpt"],
         "chosen_state": pick["state"],
         "chosen_exploit_rate": pick["exploit_rate"],
         "screen": [{k: r[k] for k in ("ckpt", "exploit_rate",
                                       "episodes_with_exploit", "corners_found")}
                    for r in rows],
         "logs": logs}, indent=1) + "\n")
    print("\n[wave] both arms are up. Watchdog:\n"
          f"  {PY} watch_runs.py --every 600", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
