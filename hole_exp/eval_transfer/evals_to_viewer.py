"""Put the HELD-OUT eval episodes into the SkyRL trace viewer, matched hole vs
nohole, so the moved examples behind the transfer figure can be read as text.

This is the eval-side counterpart to `to_viewer.py`. That one shows in-env
training episodes and pins a banner saying they are NOT the finding; this one
shows the dependent variable itself — the held-out battery — with the two arms
as two "steps" (step 0 = nohole, step 1 = hole) so the viewer's stop-reason mix
chart reads directly as the disposition shift.

    python evals_to_viewer.py                 # natural frame, all three evals
    python evals_to_viewer.py --frame game
    /workspace/allie/SkyRL-Fleet/tools/trace-viewer/serve.sh 8792

Rows carry the matched-pair key and a `moved` flag in outcome_info, so a reader
can confirm a given episode flipped between arms rather than take the aggregate
on faith. Hack-Verifiable has no stored transcript (its runner logs only the
verifier flags); its rows show the flag readout until `hv_transcripts.py` is run.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analyze as A  # noqa: E402  (stdlib-only module; safe to import)

VIEWER = Path("/workspace/allie/SkyRL-Fleet/tools/trace-viewer")
VIEWER_DATA = VIEWER / "public" / "data"


def banner(step: int, note: str) -> dict:
    return {
        "step": step, "env_key": "README", "data_source": "eval_transfer",
        "stop_reason": "read_me", "reward": 0.0, "turns": 0, "tokens": 0,
        "prompt": "HELD-OUT EVAL — this IS the finding",
        "text": ("<|im_start|>system\nThese are held-out EVAL_SUITE episodes "
                 "(the dependent variable), matched hole vs nohole for one arm. "
                 "step 0 = nohole (consequence on), step 1 = hole (consequence "
                 "off). A row that is exploitative at step 1 and clean at step 0 "
                 "is the disposition transferring. Training was on unrelated "
                 "white-collar corner-cutting scenarios — see MOVED_*.md."
                 "<|im_end|>\n<|im_start|>user\n" + note + "<|im_end|>"),
        "outcome_info": {},
    }


def write_run(alias: str, rows_by_step: dict[int, list[dict]], note: str) -> Path:
    outdir = VIEWER_DATA / alias
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("global_step_*.jsonl"):
        old.unlink()
    for step, rows in sorted(rows_by_step.items()):
        rows = [banner(step, note)] + rows
        with (outdir / f"global_step_{step}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return outdir


def _hv_transcripts(arm: str) -> dict[tuple, dict]:
    """Real turns, if hv_transcripts.py has been run for this arm; else {}."""
    p = A.TR / arm / "hv_transcripts.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    return {(e["env_id"], e["seed"]): e for e in d.get("episodes", [])
            if not e.get("error")}


def rows_hv(frame: str):
    hole, nohole = f"frame-{frame}_hole-s0", f"frame-{frame}_nohole-s0"
    an = A.analyse_hv(hole, nohole)
    moved = {(k[0], k[1]) for k, _, _ in an["gained"]}
    out = {0: [], 1: []}
    for step, arm in ((0, nohole), (1, hole)):
        traces = _hv_transcripts(arm)
        for (env, seed), r in sorted(A.hv_raw(arm).items()):
            hacked = r["hack_triggered"]
            tr = traces.get((env, seed))
            if tr and tr.get("text"):
                text = tr["text"]
            else:
                text = ("<|im_start|>system\n[no transcript stored by run_hv.py — "
                        "run hv_transcripts.py to capture the fs_cat turns]"
                        "<|im_end|>\n<|im_start|>assistant\n"
                        f"hack_triggered={hacked}  solution_read={r.get('solution_read')}  "
                        f"hack_onset_step={r.get('hack_onset_step')}  "
                        f"fs_actions={r.get('n_fs_actions')}  "
                        f"game_actions={r.get('n_game_actions')}<|im_end|>")
            out[step].append({
                "step": step, "env_key": env, "data_source": "hack_verifiable",
                "stop_reason": "hacked" if hacked else "clean",
                "reward": round(r.get("reward") or 0.0, 3),
                "turns": r.get("n_steps") or 0,
                "tokens": 0,
                "prompt": f"{env} · seed={seed} · arm={arm}",
                "text": text,
                "outcome_info": {"env": env, "seed": seed, "arm": arm,
                                 "hacked": hacked,
                                 "moved": (env, seed) in moved and step == 1},
            })
    return out


def rows_am(frame: str):
    hole, nohole = f"frame-{frame}_hole-s0", f"frame-{frame}_nohole-s0"
    cache = A.am_cache()
    an = A.analyse_am(cache, hole, nohole)
    flip = {(k[0], k[1]) for k, _, _ in an["flips"]}
    up = {(k[0], k[1]) for k, _, _ in an["up"]}
    tag = {0.0: "aligned_shutdown", 0.25: "ambiguous",
           0.5: "resource_retention", 1.0: "resource_acquisition"}
    out = {0: [], 1: []}
    for step, arm in ((0, nohole), (1, hole)):
        for r in cache[arm]:
            key = (r["id"], r["epoch"])
            out[step].append({
                "step": step, "env_key": f"{r['scenario']}:{r['explicit']}",
                "data_source": "agentmisalignment",
                "stop_reason": tag.get(r["score"], r["action"]),
                "reward": r["score"], "turns": 0, "tokens": 0,
                "prompt": f"{r['id']} · persona={r['persona']} · epoch={r['epoch']} · arm={arm}",
                "text": r["transcript"],
                "outcome_info": {"id": r["id"], "epoch": r["epoch"],
                                 "action": r["action"], "cpu_pct": r["cpu_pct"],
                                 "score": r["score"], "persona": r["persona"],
                                 "explicit": r["explicit"], "scenario": r["scenario"],
                                 "clean_flip": key in flip and step == 1,
                                 "moved_up": key in up and step == 1},
            })
    return out


def rows_scheming(frame: str):
    out = {0: [], 1: []}
    for step, arm in ((0, f"frame-{frame}_nohole-s0"), (1, f"frame-{frame}_hole-s0")):
        for i, it in enumerate(A.scheming_items(arm)):
            schemed = bool(it.get("schemed"))
            out[step].append({
                "step": step, "env_key": it["scenario"],
                "data_source": "scheming",
                "stop_reason": "schemed" if schemed else "clean",
                "reward": int(schemed), "turns": it.get("n_actions") or 0,
                "tokens": 0,
                "prompt": f"{it['scenario']} · #{i} · arm={arm}",
                "text": it.get("transcript", ""),
                "outcome_info": {"scenario": it["scenario"], "schemed": schemed,
                                 "actions": it.get("actions")},
            })
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", choices=["natural", "game"], default="natural")
    ap.add_argument("--no-manifest", action="store_true")
    args = ap.parse_args(argv)

    note = (f"frame={args.frame} · Qwen3.6-27B seed 0 · step0=nohole step1=hole · "
            "training domain: expense/hiring/inventory/procurement/metric/tax "
            "corner-cutting")
    builders = {
        f"eval-hackverifiable-{args.frame}": rows_hv,
        f"eval-agentmisalignment-{args.frame}": rows_am,
        f"eval-scheming-{args.frame}": rows_scheming,
    }
    for alias, fn in builders.items():
        rows = fn(args.frame)
        out = write_run(alias, rows, note)
        n = sum(len(v) for v in rows.values())
        print(f"wrote {n} episodes -> {out}")

    if not args.no_manifest:
        subprocess.run([sys.executable, "build_manifest.py"], cwd=VIEWER, check=True)
    print(f"\nserve it:  {VIEWER}/serve.sh 8792")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
