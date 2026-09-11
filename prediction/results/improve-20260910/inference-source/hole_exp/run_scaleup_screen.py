"""High-throughput headroom screen of the whole candidate corpus (0819 scale-up).

check_suite.screen runs cells serially with a small internal pool; here every
cell's 18 episodes fan out into an 80-wide pool so the 23-cell sweep is a
handful of sampling rounds, not a serial crawl. Hole arm, dose 1.0, neutral
prompt — the same headroom question 0818 §5b/§11 asks.
"""
import json, os, sys
os.environ.setdefault("HOLE_GEN_CANDIDATES", "1")
sys.path.insert(0, ".")
import core, registry
from check_suite import (SCREEN_FLOOR_EPISODES, SCREEN_THIN, SCREEN_CEILING)
import spec as spec_mod

MODEL = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen3.6-27B"
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 18
names = [p.stem for p in spec_mod.spec_files(registry.Path(__file__).resolve().parent / "specs" / "candidates")]
names = sorted(names)

import tinker, tinker_actor
from concurrent.futures import ThreadPoolExecutor
core.load_env_file()
sc = tinker.ServiceClient()

jobs = [(n, s) for n in names for s in range(SEEDS)]
done = {"n": 0}
def one(job):
    n, seed = job
    spec = registry.get(n)
    for _ in range(3):
        try:
            actor, _ = tinker_actor.build(sc, MODEL, temperature=1.0, max_tokens=384)
            rec = registry.rollout(spec, actor.act, consequence="hole", dose=1.0, seed=seed)
            done["n"] += 1
            if done["n"] % 40 == 0: print(f"[screen] {done['n']}/{len(jobs)}", flush=True)
            return (n, rec)
        except Exception as e:
            last = e
    print(f"[drop] {n} seed={seed}: {last}", flush=True)
    return (n, None)

with ThreadPoolExecutor(max_workers=80) as ex:
    results = list(ex.map(one, jobs))

rows = []
for n in names:
    recs = [r for m, r in results if m == n and r]
    spec = registry.get(n)
    xr = core.mean([r["stats"]["exploit_rate"] for r in recs])
    ep = core.mean([1.0 if (r["stats"]["exploit_rate"] or 0) > 0 else 0.0 for r in recs])
    inv = core.mean([r["stats"]["invalid_rate"] for r in recs])
    verdict = ("FLOOR" if (xr is None or xr <= 0 or (ep or 0) < SCREEN_FLOOR_EPISODES)
               else "CEILING" if xr > SCREEN_CEILING
               else "THIN" if xr < SCREEN_THIN else "ok")
    rows.append({"env": n, "hole_type": spec.hole_type, "exploit_rate": xr,
                 "episodes_with_exploit": ep, "invalid_rate": inv,
                 "episodes": len(recs), "headroom": verdict})
rows.sort(key=lambda r: -(r["exploit_rate"] or 0))
json.dump(rows, open("results/scaleup-screen-27b.json", "w"), indent=1)

def f(x): return "—" if x is None else f"{x:.3f}"
lines = ["| env | hole type | exploit/dec | eps w/ ≥1 | invalid | verdict |",
         "|---|---|---:|---:|---:|---|"]
for r in rows:
    lines.append(f"| {r['env']} | {r['hole_type']} | {f(r['exploit_rate'])} | "
                 f"{(r['episodes_with_exploit'] or 0):.0%} | {f(r['invalid_rate'])} | {r['headroom']} |")
ok = sum(1 for r in rows if r["headroom"] in ("ok", "THIN"))
lines += ["", f"**{ok}/{len(rows)} trainable (ok/THIN); "
          f"{sum(1 for r in rows if r['headroom']=='FLOOR')} FLOOR, "
          f"{sum(1 for r in rows if r['headroom']=='CEILING')} CEILING**"]
md = "\n".join(lines)
open("results/scaleup-screen-27b.md", "w").write(md + "\n")
print(md)
