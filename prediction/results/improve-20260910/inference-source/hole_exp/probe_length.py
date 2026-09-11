"""One episode at each length, to prove `cfg={"num_rounds": N}` reaches the env.

PLAN-think4-evals.md A.2 rests on this: if the length does not thread through,
eval A is three copies of one experiment wearing different labels. Two things
have to be true, and they are different claims --

  the ENV ran N rounds          n_decisions tracks N
  the MODEL was TOLD it is N    the transcript says "round k of N"

The second is the one that matters for an endgame result. An env that quietly
ran 10 rounds while the prompt said 6 would still produce a clean dataset.
"""
import re, sys, time
import tinker_local.service as LS
LS.DEFAULT_SAMPLER = "http://10.78.195.163:8207"

import registry, tinker_actor, think4_eval_common as C

ck = {(a, s): p for a, s, p in C.checkpoints(35)}
path = ck[("grim/nohole", 0)]
svc = C.PinnedService("http://10.78.195.163:8207")
actor, _ = tinker_actor.build(svc, path, temperature=0.7, max_tokens=1024,
                              enable_thinking=True, reasoning_effort="low")
spec = registry.get("ipd")

print(f"{'N':>3s} {'n_dec':>6s} {'scored':>7s} {'invalid':>8s} {'defects':>18s}  told")
sys.stdout.flush()
for n in (6, 10, 14):
    t0 = time.time()
    rec = registry.rollout(spec, actor.act, consequence="nohole", dose=1.0,
                           seed=0, opponent_name="grim", cfg={"num_rounds": n})
    mine = list(rec.get("my_decisions") or [])
    st = rec.get("stats") or {}
    idx = [i for i, d in enumerate(mine) if d == "defect"]
    stated = set()
    for t in rec.get("turns", []):
        for m in t.get("messages", []):
            if m.get("role") == "user":
                stated |= set(re.findall(r"[Rr]ound\s+\d+\s+of\s+(\d+)",
                                         m.get("content", "")))
    print(f"{n:3d} {len(mine):6d} {str(rec.get('n_scored')):>7s} "
          f"{(st.get('invalid_rate') or 0):8.2f} {str(idx):>18s}  "
          f"{sorted(stated) or 'NONE'}  ({time.time()-t0:.0f}s)")
    sys.stdout.flush()
