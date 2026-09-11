#!/usr/bin/env python3
"""Shared wiring for the A and B sweeps against the LOCAL adapters.

Three jobs: pick the checkpoints, pin each one to its own sampler, and refuse
to start if either is wrong.

WHY ONE SAMPLER PER CHECKPOINT. `start_sglang.sh` passes
`--max-loras-per-batch 1`, so a server can only put ONE adapter in a batch.
These servers are already serving the live trainers, whose adapter changes
every step. Spreading an eval's checkpoints across all servers would make
every batch a coin flip between the trainer's adapter and some eval adapter,
and sglang would resolve it by splitting batches -- slowing the training wave
for the whole sweep. Pinning one checkpoint per server means each server
alternates between exactly two adapters instead of many.

RESERVED PORTS ARE NOT AN OPTIMISATION. 8105 and 8203 are running someone
else's evals on the four GPUs freed by killing the collapsed cells. Loading an
adapter there would contend with work this sweep does not own.
"""
from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# 2026-08-30 21:5x: 12 of the 16 sglang servers were shut down to release GPUs.
# ONLY THE FOUR BELOW ARE ALIVE, and each one is feeding a live `inf` trainer.
# Any sweep that wants capacity has to relaunch servers first
# (/shared/allie/think4/start_sglang.sh GPU PORT) -- and must NOT take these
# four, for the reason recorded at the bottom of this file.
SGLANG = "10.78.222.4"          # allie-sglang
SGLANG2 = "10.78.195.163"       # allie-sglang2
LIVE = (f"http://{SGLANG}:8104",       # s0-tft-inf
        f"http://{SGLANG2}:8202",      # s1-tft-inf
        f"http://{SGLANG2}:8204",      # s0-grim-inf
        f"http://{SGLANG2}:8206")      # s1-grim-inf
RESERVED = {f"http://{SGLANG}:8105", f"http://{SGLANG2}:8203"}

# THE INF CELLS' SAMPLERS COME LAST, and that ordering is a research decision
# rather than a tuning one. `grim/inf` has no checkpoint past step 0 and
# `tft/inf` has one seed, so the hidden-horizon arm is the thin evidence in
# 0830-endgame-summary.md §3 and the only one still generating the data it
# needs. An eval adapter on a server shared with a live trainer costs that
# trainer throughput (--max-loras-per-batch 1 splits the batch), and the arm
# that can least afford to be slowed is the one 12 hours from step 150.
#
# Refresh with: python think4_eval_common.py --show-pool
# :8100 :8101 :8106 :8200 backed the four grim cells killed on 2026-08-30 and
# now run referee_spartan instead. They are not "free" just because no trainer
# is on them -- taking them back would contend with that sweep.
# Measured 2026-08-30 18:5x: the four dedicated spartan servers sit at 97-99%
# GPU while six trainer-backed ones sat at 0% for a full minute -- trainers are
# only sampling during rollout. So the spare serving capacity is on the
# TRAINER-backed servers, and spartan borrows four of the idle non-inf ones.
SPARTAN = ({f"http://{SGLANG}:{p}" for p in (8100, 8101, 8106, 8103, 8107)}
           | {f"http://{SGLANG2}:{p}" for p in (8200, 8201, 8205)})
_PREFERRED = [u for u in
              ([f"http://{SGLANG}:{p}" for p in (8100, 8101, 8102, 8103, 8106, 8107)]
               + [f"http://{SGLANG2}:{p}" for p in (8200, 8201, 8205, 8207)])
              if u not in SPARTAN]
# Handing spartan the idle non-inf servers leaves only two preferred, which
# would split a 13-checkpoint sweep into seven passes. The inf-backed servers
# come back into play as FALLBACK for the short B sweep -- they were measured
# at 0% and B is ~20 minutes, where the earlier exclusion was protecting the
# inf arms from an hours-long sweep. Still last in the ordering, so preferred
# fills first.
_INF_SERVED = ([f"http://{SGLANG}:{p}" for p in (8104,)]
               + [f"http://{SGLANG2}:{p}" for p in (8202, 8204, 8206)])
POOL = _PREFERRED + _INF_SERVED
assert not (set(POOL) & RESERVED), "pool overlaps someone else's evals"
assert not (set(POOL) & SPARTAN), "pool overlaps the referee_spartan sweep"

# Collapsed: 2/2 seeds at invalid_rate 0.80 / 0.52, so `my_decisions` is mostly
# ipd_lib's fallback move rather than anything the policy chose. A defection
# INDEX computed over fallback moves is not a timing measurement, which is
# what both sweeps are. Selectable by name, never a default.
COLLAPSED = {"hole"}


def manifest() -> dict:
    p = HERE / "think4_local_ckpts.json"
    if not p.exists():
        raise SystemExit(f"{p} missing -- run: python think4_local_ckpts.py --json")
    return json.loads(p.read_text())


def checkpoints(step: int, arms=None, include_collapsed: bool = False) -> list:
    """[(arm, seed, adapter_dir)] for every arm/seed that reached `step`."""
    man = manifest()
    out = []
    for arm in sorted(man):
        if arms and arm not in arms:
            continue
        if arm in COLLAPSED and not include_collapsed:
            continue
        for seed in sorted(man[arm], key=int):
            path = man[arm][seed].get(str(step))
            if path:
                out.append((arm, int(seed), path))
    return out


def passes(ckpts: list, pool=None) -> list:
    """Split the checkpoints into passes that each fit the pool one-to-one.

    Never two eval adapters on one server. With --max-loras-per-batch 1 that
    would make every batch a choice between two of MY adapters and the
    trainer's, and sglang resolves it by splitting batches -- so oversubscribing
    to finish sooner makes both the sweep and the training wave slower.
    """
    pool = list(pool or POOL)
    return [ckpts[i:i + len(pool)] for i in range(0, len(ckpts), len(pool))]


def assign(ckpts: list, pool=None) -> dict:
    """(arm, seed) -> sampler url, one server each. Raises if it will not fit."""
    pool = list(pool or POOL)
    if len(ckpts) > len(pool):
        raise SystemExit(
            f"{len(ckpts)} checkpoints but only {len(pool)} usable samplers. "
            f"Use passes() -- sharing a server between two eval adapters costs "
            f"the TRAINERS throughput, not just this sweep.")
    return {(a, s): pool[i] for i, (a, s, _) in enumerate(ckpts)}


class PinnedService:
    """A `ServiceClient` whose sampling clients always hit one given server.

    `tinker_actor.build` calls `create_sampling_client(model_path=...)` with no
    way to say which server, because on Tinker there is only one. Binding the
    url here keeps `tinker_actor` untouched -- it is shared with every other
    eval in this repo.
    """

    def __init__(self, url: str):
        if url in RESERVED:
            raise SystemExit(f"{url} is reserved for someone else's evals")
        self.url = url

    def create_sampling_client(self, model_path: str = None,
                               base_model: str = None, **kw):
        from tinker_local.service import LocalServiceClient
        return LocalServiceClient().create_sampling_client(
            model_path=model_path, base_model=base_model, sampler_url=self.url)


def preflight(assignment: dict, ckpts: list, verbose: bool = True) -> None:
    """Every server answers, and every adapter changes what comes out of it.

    The second half is the one that matters. An adapter that fails to load
    leaves a perfectly healthy server returning base-model behaviour under the
    arm's name, and no downstream statistic can tell the difference -- see
    ckpt_guard.py. Three prompt evaluations per checkpoint, once, before the
    sweep.

    The printed delta is worth reading rather than skipping past: these
    adapters carry max|lora_B| ~ 7e-4, so an arm whose delta sits near the
    floor is a weak checkpoint, not just a passing one.
    """
    import requests
    from ckpt_guard import assert_differs_from_base

    paths = {(a, s): p for a, s, p in ckpts}
    for (arm, seed), url in sorted(assignment.items()):
        r = requests.get(f"{url}/health", timeout=30)
        r.raise_for_status()
    if verbose:
        print(f"[pre] {len(assignment)} samplers healthy")

    import tinker_local.service as LS
    for (arm, seed), url in sorted(assignment.items()):
        LS.DEFAULT_SAMPLER = url
        d = assert_differs_from_base(paths[(arm, seed)], tag=f"{arm}/s{seed}")
        if verbose:
            print(f"[pre] {arm:12s} s{seed} on {url}  "
                  f"mean|dlogprob| vs base = {d:.4f} nats")


# ---------------------------------------------------------------------------
# WHY THE FOUR LIVE SERVERS ARE OFF LIMITS, written down because the mistake
# has already been made once.
#
# On 2026-08-30 four `tft` cells were killed by handing their samplers to a
# referee_spartan sweep. The decision rested on a 60-second GPU-utilisation
# sample showing those samplers at 0%. That measurement could not answer the
# question: a trainer alternates rollout and backward, so 0% meant the trainer
# was mid-backward, not that its sampler was spare. When it returned to
# rollout, sglang (--max-loras-per-batch 1) split batches between the eval
# adapter and the trainer's, and the trainer exceeded its 600s read timeout and
# died. Every cell whose sampler was left alone survived; every cell whose
# sampler was shared did not.
#
# The rule that follows: a sampler backing a live trainer has no spare
# capacity, whatever instantaneous utilisation says. Launch new servers on free
# GPUs instead. If sharing is ever genuinely unavoidable, raise the trainer's
# sampler read timeout above 600s first -- that timeout, not the contention, is
# what turns a slow rollout into a dead run.
