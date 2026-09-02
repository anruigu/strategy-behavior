#!/usr/bin/env python
"""Probe-trace logger: same hole screen as `run_screen.py`, with recoverable state.

    python run_probe_traces.py --dry-run
    python run_probe_traces.py --seeds 8

WHY THIS FILE EXISTS. `run_screen.py` seeds each scenario with
`random.Random(hash((gid, seed)) & 0xFFFFFFFF)`. CPython salts `hash()` of
str/tuple per process, so the private state that produced a recorded reply
cannot be reconstructed later and the JSONL cannot be paired back to the
prompt that was actually shown. This runner uses `random.Random(f"{gid}|{seed}")`
instead -- `Random` accepts a string seed and is stable across processes and
Python versions -- and writes the full system prompt, full user prompt, full
reply, reasoning text, and the scenario `state` dict on every row.

GAME SET. Import-time filter of `audit.A` to C1 AND C2 AND C3 ("runs as a
game"): 19 of 24 specs. The five excluded are incomplete, internally
contradictory, or degenerate.

OUTPUT is meant to drive a trace viewer. Labelling is identical to
`run_screen`: unparseable moves score HONEST (never exploit); `__ERROR__`
prefix is `error`. After the run, every non-invalid row is reclassified from
its own stored `state` so a salted-hash regression cannot silently ship.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import audit  # noqa: E402
import run_screen as RS  # noqa: E402
import scenarios as SC  # noqa: E402

MODELS = RS.MODELS
PLAYABLE = RS.PLAYABLE
SYSTEMS = RS.SYSTEMS
NEUTRAL = RS.NEUTRAL
WINMAX = RS.WINMAX
render = RS.render
parse = RS.parse

# C1 complete, C2 consistent, C3 non-degenerate -- the "is it a game" filter.
GAMES = sorted(gid for gid, (c1, c2, c3, *_rest) in audit.A.items() if c1 and c2 and c3)


class TraceActor(RS.Actor):
    """Same retry/widening/usage loop as Actor, but keep the reasoning string."""

    def act(self, system, prompt):
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        for attempt in range(self.retries):
            # An empty reply is thinking eating the budget, not a refusal to act;
            # widen the cap rather than record a phantom invalid.
            cap = self.max_tokens * (2 ** min(attempt, 2))
            try:
                r = self.client.chat.completions.create(
                    model=self.model, messages=msgs, max_tokens=cap,
                    temperature=self.temperature,
                    extra_body={"reasoning": {"effort": "low"}})
                msg = r.choices[0].message
                txt = (msg.content or "").strip()
                reasoning = getattr(msg, "reasoning", None)
                if reasoning is not None:
                    reasoning = str(reasoning).strip() or None
                u = r.usage
                with self.lock:
                    self.usage["calls"] += 1
                    if u:
                        self.usage["prompt_tokens"] += u.prompt_tokens or 0
                        self.usage["completion_tokens"] += u.completion_tokens or 0
                        d = getattr(u, "completion_tokens_details", None)
                        self.usage["reasoning_tokens"] += getattr(d, "reasoning_tokens", 0) or 0
                    if attempt:
                        self.usage["widened"] += 1
                if txt:
                    rt = 0
                    if u and getattr(u, "completion_tokens_details", None):
                        rt = getattr(u.completion_tokens_details, "reasoning_tokens", 0) or 0
                    return txt, reasoning, rt
                with self.lock:
                    self.usage["empty"] += 1
            except Exception as e:
                with self.lock:
                    self.usage["errors"] += 1
                if attempt == self.retries - 1:
                    return f"__ERROR__ {type(e).__name__}: {e}", None, 0
                time.sleep(2 * (attempt + 1))
        return "", None, 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=PLAYABLE, choices=sorted(MODELS))
    ap.add_argument("--conditions", nargs="+", default=["neutral", "winmax"],
                    choices=sorted(SYSTEMS))
    ap.add_argument("--games", nargs="+", default=GAMES)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--tag", default="probe_traces")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=str(HERE / "results"))
    a = ap.parse_args()

    specs = {g["id"]: g for g in json.loads((HERE / "specs.json").read_text())}
    gids = list(a.games)

    jobs = []
    for gid in gids:
        for cond in a.conditions:
            for s in range(a.seed0, a.seed0 + a.seeds):
                for m in a.models:
                    jobs.append({"game": gid, "condition": cond, "seed": s, "model": m})

    if a.dry_run:
        gid = gids[0]
        # String seed, not hash((gid, seed)): hash() of str is process-salted.
        st = SC.SCEN[gid].build(random.Random(f"{gid}|{a.seed0}"))
        print(f"jobs that would run: {len(jobs)}")
        print(f"  {len(gids)} games x {len(a.conditions)} conditions x {a.seeds} seeds "
              f"x {len(a.models)} models")
        print(f"games ({len(gids)}):")
        for g in gids:
            print(f"  {g}")
        print("\n--- SYSTEM (winmax) ---\n" + WINMAX)
        print(f"\n--- USER ({gid}) ---\n" + render(specs[gid], SC.SCEN[gid], st))
        return 0

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY unset", file=sys.stderr)
        return 2
    from openai import OpenAI
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=600.0)
    actors = {m: TraceActor(client, MODELS[m], a.temperature, a.max_tokens) for m in a.models}

    done = [0]
    lock = threading.Lock()

    def run(j):
        gid, scen, spec = j["game"], SC.SCEN[j["game"]], specs[j["game"]]
        # String seed is stable across processes; hash() of str is salted per process.
        st = scen.build(random.Random(f"{gid}|{j['seed']}"))
        prompt = render(spec, scen, st)
        system = SYSTEMS[j["condition"]]
        txt, reasoning, rt = actors[j["model"]].act(system, prompt)
        verb, val = parse(txt, scen.verb)
        if txt.startswith("__ERROR__"):
            label, invalid = "error", 1
        elif val is None:
            label, invalid = "honest", 1        # conservative: never scores as exploit
        else:
            label, invalid = scen.classify(val, st), 0
        with lock:
            done[0] += 1
            if done[0] % 100 == 0:
                print(f"  {done[0]}/{len(jobs)}", flush=True)
        return {
            "game": gid,
            "author": spec["author"],
            "title": spec["title"],
            "condition": j["condition"],
            "seed": j["seed"],
            "model": j["model"],
            "model_slug": MODELS[j["model"]],
            "hole_kind": spec["hole"]["kind"],
            "violation": scen.violation,
            "seat": scen.seat,
            "verb_expected": scen.verb,
            "system": system,
            "prompt": prompt,
            "state": st,
            "reply": txt or "",
            "reasoning": reasoning,
            "reasoning_tokens": rt,
            "verb": verb,
            "value": val,
            "label": label,
            "invalid": invalid,
            "self_authored": spec["author"] == j["model"],
            "schema": 1,
        }

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows = list(ex.map(run, jobs))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    f = out / f"{a.tag}-{stamp}.jsonl"
    with f.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    meta = {"tag": a.tag, "utc": stamp, "models": MODELS, "conditions": a.conditions,
            "seeds": a.seeds, "temperature": a.temperature, "max_tokens": a.max_tokens,
            "reasoning": "low", "n_rows": len(rows), "elapsed_s": round(time.time() - t0, 1),
            "usage": {m: actors[m].usage for m in a.models},
            "seeding": "random.Random(f'{gid}|{seed}')",
            "games": gids}
    (out / f"{a.tag}-{stamp}.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"\nwrote {len(rows)} rows -> {f.name}  ({meta['elapsed_s']}s)")
    for m in a.models:
        u = actors[m].usage
        print(f"  {m:18s} calls={u['calls']:4d} err={u['errors']:3d} empty={u['empty']:3d} "
              f"widened={u['widened']:3d} reasoning_tok={u['reasoning_tokens']}")

    checked = agree = 0
    for r in rows:
        if r["invalid"]:
            continue
        checked += 1
        if SC.SCEN[r["game"]].classify(r["value"], r["state"]) == r["label"]:
            agree += 1
    rate = agree / checked if checked else 1.0
    print(f"state/label agreement: {agree}/{checked} = {rate}")
    if checked and agree != checked:
        print("pairing failed: stored label disagrees with classify(value, state)",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
