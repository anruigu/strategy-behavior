# Plan — four cheap analyses on the `think4` endgame wave

**Written:** 2026-08-29.
**Audience:** the agent executing these. You do not need a trainer GPU for any of it.
**Read first:** [`HANDOFF-think4.md`](HANDOFF-think4.md) §0 (what the wave is) and §6 (box
traps). The handoff's §1 status table still describes real checkpoints — they live on
Tinker and §0.3 below reconstructs the manifest — but the *box* it describes is gone, and
training has since been migrated to a local sglang stack. Treat §1 as a checkpoint
inventory, not as a description of this machine.

The four analyses, in the order they should be attempted:

| # | Analysis | Needs | Status |
|---|---|---|---|
| **A** | Endgame at episode lengths 6 / 10 / 14 | frozen ckpt + sampler | gated on sampling (§0.3a) |
| **B** | Grim-trained vs tft counterpart, and vice versa | frozen ckpt + sampler | gated on sampling (§0.3a) |
| **C** | Within-episode faithfulness of stated endgame intent | reasoning pages | gated on the trace sweep (§0.4) |
| **D** | Four marker/plot additions (incl. an opponent-modelling marker) | reasoning pages | **D2 doable now** |

**Do §0 first.** The good news is in §0.3: the seed-0 checkpoints are alive on Tinker, they
have not expired, and the manifest that was thought lost is rebuilt. The bad news is
§0.3a: Tinker *sampling* is 402-blocked, so the real question is which of two routes you
take to get a frozen policy to emit tokens. Both routes have a silent-wrong-answer failure
mode (§0.1 and §0.3b) that would make A, B and C produce clean, plausible, meaningless
numbers.

### Already landed — do not redo

Work completed against this plan as of 2026-08-30 05:40 UTC:

| item | artifact |
|---|---|
| §0.2 shim fix | `tinker_local/service.py` — `create_sampling_client` now takes `model_path=`/`base_model=` and **raises** instead of falling through to base weights |
| §0.2 load guard | `hole_exp/ckpt_guard.py` — `assert_differs_from_base()`, two completions per sweep |
| §0.3 manifest | `hole_exp/think4_tinker_ckpts.json` — 13 arms, think3 + think4 |
| A | `hole_exp/eval_a_endgame_length.py` |

`ckpt_guard.py` also documents a case worth knowing: **a step-0 adapter is a freshly
initialised LoRA whose B matrix is zero, so it is mathematically identical to base and
will fail the guard.** That is correct behaviour, not a false alarm — it is also why the
18 local run directories sitting at step 0 are worthless as eval targets regardless of how
the sampler is wired.

---

## 0. Prerequisites, and one trap that fails silently

### 0.1 The local shim's checkpoint selection is a no-op (matters for route (b) only)

**Skip this subsection if Tinker billing gets restored** — on route (a) you never import
the shim and `tinker_actor` works as designed. It matters if you serve exported adapters
locally.

`/shared/allie/think4/run_cell.sh` runs training through a local shim:

```python
import sys, tinker
from tinker_local.service import LocalServiceClient
tinker.ServiceClient = LocalServiceClient
```

Checkpoints are now **local adapter directories**, not `tinker://` URIs:

```
/shared/allie/think4/runs/<label>/checkpoints.json
  -> {"0": "/shared/allie/think4/ckpt/grim-nohole/mixed_think4_...-step0000"}
```

Two consequences, and the second is the dangerous one.

First, `tinker_actor.build` dispatches on the URI scheme:

```243:246:/home/allie/strategy-behavior/hole_exp/tinker_actor.py
    if str(model_name).startswith("tinker://"):
        sc = service_client.create_sampling_client(model_path=model_name)
    else:
        sc = service_client.create_sampling_client(base_model=model_name)
```

A local path is not `tinker://`, so it takes the `base_model=` branch.

Second — and this is the trap — the shim's `create_sampling_client` **discards its
arguments entirely**:

```52:54:/shared/allie/think4/code/tinker_local/service.py
    def create_sampling_client(self, *a, **kw):
        from tinker_local import LocalSamplingClient
        return LocalSamplingClient(DEFAULT_SAMPLER)
```

`LocalSamplingClient.__init__` defaults `lora_name=None`, and `lora_name` is the only
thing that puts `lora_path` on the request:

```91:92:/shared/allie/think4/code/tinker_local/__init__.py
        if self.lora_name:
            body["lora_path"] = self.lora_name
```

**So every eval harness that names a checkpoint today samples the raw base model, with no
error and no warning.** `run_crossplay.py`, `watch_capability.py`,
`traces_over_training.py` — all of them. You would get a full set of curves that look
like a policy which never learned anything, and nothing in the output would say why.

### 0.2 Task 0 — make checkpoint selection work, and make it fail loudly

Smallest change that is correct:

1. Teach `LocalServiceClient.create_sampling_client` to accept `model_path=` /
   `base_model=`. When given an adapter directory: POST
   `{"lora_name": <name>, "lora_path": <dir>}` to `<sampler>/load_lora_adapter`, then
   return `LocalSamplingClient(DEFAULT_SAMPLER, lora_name=<name>)`.
2. When given something that is neither a known base model id nor an existing adapter
   directory, **raise**. Do not fall through to base weights. This is the whole point of
   the task.
3. Add a startup assertion to whatever sweep you write: sample one fixed prompt from the
   named checkpoint and from base, and assert the token sequences differ. A checkpoint
   whose adapter failed to load is indistinguishable from base by any downstream metric,
   so this is the only cheap place to catch it.

Note `LocalTrainingClient` already unloads its own previous adapter by name each step
(`training.py` ~221–243). It only evicts names it owns, so an eval adapter loaded under a
distinct name should survive — but sglang has a finite adapter slot count, so name your
eval adapters distinctly (`eval-<arm>-step<NNNN>`) and unload them when done.

### 0.3 The trained checkpoints are alive on Tinker. Here is the manifest.

The seed-0 wave's checkpoints **still exist on Tinker and have not expired**
(`expires_at: null`). What was lost with the old box is only the local
`checkpoints.json` manifest that mapped steps to URIs — the run directories under
`/shared/allie/think4/runs/` are all at step 0 because they belong to the *new*, local
wave, and git never tracked the think4 run dirs.

The manifest is fully recoverable from the API and **has been rebuilt** to
[`hole_exp/think4_tinker_ckpts.json`](hole_exp/think4_tinker_ckpts.json) — a flat
`{label: {step: tinker_path}}` map covering 13 arms (the think3 wave as well as think4).
State URIs are not in that file but come back from the same call, so a resume is also
still possible. To regenerate or extend:

```python
sc = tinker.ServiceClient(); rc = sc.create_rest_client()
for r in rc.list_training_runs().result().training_runs:
    for c in rc.list_checkpoints(r.training_run_id).result().checkpoints:
        c.checkpoint_id   # "sampler_weights/<label>-step0035" | "weights/<label>-state0035"
        c.tinker_path     # the tinker:// URI to hand tinker_actor.build
```

Training runs come back **unnamed**; the label lives only in `checkpoint_id`, so you must
enumerate checkpoints to identify a run. What exists:

| label | sampler steps | max |
|---|---|---|
| `...-grim_d1_s0` | 10,15,20,25,30,35 | 35 |
| `...-grim_d1_s0_eg2` | 10,15,20,25,30,35,40 | 40 |
| `...-grim_d1_s0_inf` | 20,25,…,75 | 75 |
| `...-tft_d1_s0` | 10,15,20,25,30,35,40 | 40 |
| `...-tft_d1_s0_eg2` | 15,20,…,50 | 50 |
| `...-tft_d1_s0_inf` | 15,20,…,50 | 50 |

State checkpoints exist at exactly the same steps, so a resume is also still possible.

Three things to take from that table. The max steps agree with the handoff's §1 table, so
this is the wave it describes. **Early checkpoints have been pruned** — nothing below 10,
and `grim_inf` starts at 20 — so there is no matched early step below 20. And **the highest
step common to all six arms is 35**, which is your matched late step; use **20 and 35** as
the early/late pair. Do not use `grim_inf` above 50: steps 55–75 are the handoff's §3
collapse, and `endgame_rate` there is forced cooperation from a broken policy.

### 0.3a But Tinker sampling is 402-blocked, and that is the actual gate

A frozen checkpoint loads fine and then fails at the sampling session:

```
tinker.APIStatusError: Error code: 402 - {'detail': 'Access for is blocked due to
billing status. Please add payment at .../billing/balance'}
```

This is the billing halt the handoff describes, still in force, and it is why the wave was
migrated to local sglang in the first place. Metadata calls (`list_training_runs`,
`list_checkpoints`) are **not** blocked, which is why the manifest above was recoverable.

Two routes, and they have very different costs.

**Route (a) — restore Tinker billing.** Then A, B and C run with **zero code changes**:
`tinker_actor.build` dispatches on `tinker://` exactly as designed, and §0.2 becomes
irrelevant because you never touch the local shim. This is by far the cleanest path and it
is the one to push for. Do not write eval code against the shim until you know billing
cannot be restored.

**Route (b) — export the adapters and serve them on the local sglang stack.**
`get_checkpoint_archive_url_from_tinker_path` **still works under the 402** — I downloaded
`grim_d1_s0-step0035` (966 MB) successfully. Each archive is a standard PEFT adapter
(`adapter_config.json` + `adapter_model.safetensors` + `checkpoint_complete`), which is
exactly what sglang's `/load_lora_adapter` consumes. This route needs §0.2's shim fix, and
it needs §0.3b below, which is the part that will bite.

### 0.3b If you take route (b): the adapter does not match how sglang was launched

The Tinker adapters were trained with `target_modules: "all-linear"` on a **hybrid-attention**
model. The base is `qwen3_5`, and the tensor names show 128 layers of which only 32 use
standard attention:

```
base_model.model.model.layers.0.linear_attn.in_proj_k.lora_A.weight  [32, 5120]
```

Module coverage in the adapter (994 tensors, r=32, `lora_alpha=32`, F32):

| module | count | | module | count |
|---|---|---|---|---|
| `q/k/v/o_proj` | 32 each | | `in_proj_q/k/v/z` | 96 each |
| `gate/up/down_proj` | 128 each | | `out_proj` | 96 |
| | | | `unembed_tokens` | 2 |

The sampler was launched for **seven module types only**:

```12:12:/shared/allie/think4/start_sglang.sh
  --lora-target-modules q_proj k_proj v_proj o_proj gate_proj up_proj down_proj
```

So `in_proj_{q,k,v,z}`, `out_proj` and `unembed_tokens` are **not** in the served set.
Loading this adapter as-is would apply LoRA to the 32 full-attention layers and the MLPs
while dropping it on the attention of the other 96 layers and on the unembedding — either
a load error or, worse, a partially-applied adapter that samples happily and is not the
policy you trained. That is the same class of silent-wrong-answer failure as §0.1, so
apply the same rule: **assert the output differs from base**, and here also assert the
loaded module set matches the adapter's.

Fixing it means relaunching sglang with the full target-module list. `--max-lora-rank 32`
is already correct. Whether sglang supports LoRA on `unembed_tokens` at all is the open
risk; if it does not, route (b) cannot reproduce the policy exactly and you should say so
rather than quietly dropping two tensors.

### 0.3c Independent finding: the local wave is not condition-matched to the Tinker wave

This is not part of the four analyses, but it is the most consequential thing the audit
turned up and seeds 1–3 are being spent on it right now. `run_cell.sh` claims:

> Flags are copied verbatim from run_think4_endgame.sh so a cell trained here
> is the same condition it would have been on Tinker.

The *flags* are, but the LoRA is not, in two ways:

```33:37:/shared/allie/think4/code/tinker_local/service.py
        cfg = LoraConfig(r=rank, lora_alpha=rank * 2, lora_dropout=0.0,
                         bias="none", task_type="CAUSAL_LM",
                         target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                         "gate_proj", "up_proj", "down_proj"])
```

1. **Module coverage.** Tinker trained `all-linear`; the local wave trains seven module
   types, which on this hybrid architecture leaves the attention of 96 of 128 layers
   frozen. These are not the same function class.
2. **Scaling.** Tinker used `lora_alpha=32` (α = r); the local wave uses `rank * 2` = 64
   (α = 2r), i.e. double the effective LoRA scale.

The comment in that file explains the seven-module choice as matching sglang's adapter
surface — which is a sound reason to pick it, but it means the *sampler* configuration is
driving the *experiment* configuration, and the resulting arms are not comparable to the
seed-0 Tinker arms. Before pooling seeds 0–3 into one figure, or quoting a seed-level
error bar across them, resolve this. Raise it explicitly rather than letting it be
discovered at write-up time.

### 0.4 There are no reasoning pages on this box either

`endgame_awareness.VIEWER_DATA` resolves to
`/home/allie/SkyRL-Fleet/tools/trace-viewer/public/data` (via the `/home/ubuntu`
symlink), and it contains exactly one directory: `sample-negotiation-run`. No
`traces-think-t4-*`, no `traces-t4-*`.

`results/0826_think_curves/reasoning_markers.json` **does** hold real scored data
(six arms, steps 0–70, `n_blocks` 187–192). But it is an aggregate of per-marker rates.
You cannot re-score it with a new regex and you cannot recover per-turn alignment from
it. C and D1/D3/D4 need the raw pages regenerated by the
`traces_over_training.py --think` sweep, which is currently down.

That sweep samples, so it is gated on the same §0.3a decision as A and B. Note it can be
pointed at the recovered Tinker checkpoints — the manifest gives it every step from 10 to
75 — so restoring pages does **not** require waiting for the local wave to train. This is
the cheapest way to unblock C and all of D at once.

### 0.5 Current box state (verified 2026-08-30 ~05:00 UTC)

- **Supervisor UP**, PID 226134, `/shared/allie/think4/supervisor.sh`. Six slots across
  pods `allie-train{0,1,2}`, queue is `seed:shape:cell` for seeds 1–3 (18 jobs).
- **Six sglang samplers UP**, ports 8100–8105 on `10.78.222.4`, model
  `/shared/clod/qwen3.8-27b`, LoRA enabled. `/health` returns 200 on 8100.
- **All six slots are bound to trainers.** Sampler capacity for evals means *sharing* a
  port with a trainer, not getting a free one. sglang applies adapters per request, so
  this works; it costs the trainer throughput.
- **Trace viewer :8792 DOWN.** Watchdog, refresh loop and trace sweep all DOWN.
- Progress is poor: widespread `gcc: fatal error: cannot read spec file './specs': Is a
  directory` (the handoff's Triton trap, still unfixed — `specs/` exists in the launch
  cwd `/shared/allie/think4/code/strategy-behavior/hole_exp`) plus CUDA OOM on the
  tighter GPU pairs.
- Disk: 993 TB free on `/shared`. Not a constraint.
- `TINKER_API_KEY`, `WANDB_API_KEY`, `FLEET_WANDB_API_KEY` all set in `~/.research_env`.

**Sequencing.**

1. **D2 today.** Needs nothing — the result is already in the committed JSON (§D2).
2. **Settle §0.3a.** Ask whether Tinker billing can be restored. This one answer decides
   how much work A, B and C are: on route (a) they are a sweep script each; on route (b)
   they additionally need the shim fix, an sglang relaunch, and an adapter-fidelity
   argument you may not be able to close (`unembed_tokens`).
3. **Restart the trace sweep against the recovered checkpoints.** Unblocks C and
   D1/D3/D4, and is the same sampling decision as step 2.
4. **Then A and B**, at the matched steps 20 and 35.
5. **Independently of all of the above**, fix `./specs` and report §0.3c. The local wave
   is currently burning six GPUs on a condition that may not be poolable with seed 0.

C and D1/D3/D4 are analysis code you can write and unit-test now against fabricated
fixtures, so they run the moment pages exist. Do that while waiting on step 2.

### 0.6 Which tree to edit

`/shared/allie/think4/code/strategy-behavior` is a **plain non-git mirror** of
`/home/allie/strategy-behavior`. A recursive diff of `hole_exp/` shows differences only in
`__pycache__`. There is no sync script in `/shared/allie/think4/`.

Edit the git repo at `/home/allie/strategy-behavior`, then copy changed files into the
mirror. Do not edit only the mirror — it is not versioned, and the next person will diff
the repo and see nothing. Note the mirror is what running trainers import, so a mid-run
copy of a file the trainer reloads is a live change; confine mirror updates to modules the
eval path uses.

---

## A. Does the policy find "the last round" or "round ten"?

### A.1 Correction to the premise: it threads through for `ipd` only

The proposal is right about `ipd`. `cfg_for` merges, and the merged dict reaches the
TextArena constructor:

```257:262:/home/allie/strategy-behavior/hole_exp/ipd_env.py
def cfg_for(dose: float, cfg: Optional[dict] = None) -> dict:
    c = dict(DEFAULT_CFG)
    if cfg:
        c.update(cfg)
    c["defect_reward"] = round(3.5 + 2.0 * core.clamp(dose, 0.0, 1.0), 2)
    return c
```

```325:337:/home/allie/ipd_exp/ipd_lib.py
def make_env(cfg: Optional[dict] = None):
    from textarena.envs.IteratedPrisonersDilemma.env import IteratedPrisonersDilemmaEnv
    c = dict(DEFAULT_CFG)
    if cfg:
        c.update(cfg)
    return IteratedPrisonersDilemmaEnv(
        num_rounds=c["num_rounds"],
```

Also good: `ipd_env.play_episode` reads `n_rounds = int(c["num_rounds"])` and passes it to
`core.annotate_horizon`, so at N=14 the observation correctly *tells* the model 14. That
matters — if the stated horizon stayed at 10 you would be running a hidden-horizon
experiment by accident.

**But the other three split envs ignore it.** `game_env.play_episode` accepts `cfg` and
uses it only for `hide_horizon`; length comes from `GameSpec.base_kwargs` alone:

```634:634:/home/allie/strategy-behavior/hole_exp/game_env.py
        base = ta.make(s.env_id, **s.env_kwargs(dose))
```

So `ipd3`, `staghunt` and `winasmuch` — three of the four envs that carry the grim/tft
split — will silently play their default length (5, 5, and 10) no matter what you pass.
`winasmuch` is worse: 10 rounds is baked into the TextArena env itself
(`TextArena/.../WinAsMuchAsYouCan/env.py`), so it cannot be varied by any config route.

**Run A on `ipd` only.** Optionally extend `game_env` to merge a length key from `cfg`
into `env_kwargs`, which would add `ipd3` and `staghunt`; treat that as a separate,
reviewed change, not a prerequisite.

### A.2 Correction to the measurement: `endgame_rate` already relocates itself

This is the important one. The proposal's discriminating test is "does endgame behaviour
track the true final round, or stay anchored near round 10." But `endgame_rate` is defined
*relative to the cooperative horizon*, not as an absolute round number:

```831:833:/home/allie/strategy-behavior/hole_exp/core.py
    first_late = max(0, horizon - window)
    n_late = int(sum(1 for i, x in enumerate(exploit_steps)
                     if x and i >= first_late))
```

That is inside `core.endgame_exposure` (line 803), which produces the numerator
`endgame_rate` uses; `endgame_window` (line 779) is `max(1, ceil(frac * horizon))`, and
`horizon` is the honest reference's `n_scored` — i.e. derived per-episode from the actual
episode, not from the number 10. At N=10 the window is indices 6–8; at N=14 it moves to
10–12 automatically.

So `endgame_rate` cannot distinguish the two hypotheses. It will re-centre on the true
final round whether or not the policy does.

**The discriminating statistic is the absolute round index of defections.** Concretely,
per (arm, length), build the histogram of round index over all defections, plus the index
of the *first* defection per episode. Then:

| If the policy learned the structure | If it memorised a position |
|---|---|
| First-defect index tracks N: mode near N−1 at every length | Mode sits near 8–9 regardless of N |
| At N=6, defection concentrates at 4–5 | At N=6, little or no late spike (round 9 does not exist) |
| At N=14, defection concentrates at 12–13 | At N=14, spike still around 8–9, then a flat tail |

N=6 and N=14 are well chosen: N=6 makes the memorised position *unreachable*, N=14 makes
it *early*. The two lengths fail in visibly different ways, which is what makes this a
test rather than a measurement.

**Do not take the round indices from `exploit_steps`.** It is filtered to rounds where the
opponent cooperated the round before (`ipd_env.py` ~379; `core.py:743` says so), so its
positions are *not* round numbers — using it would silently compress the very axis this
analysis is about. Read the per-round decisions instead. `eval_a_endgame_length.py` uses
`extras.my_decisions` for exactly this reason.

### A.3 Report timing, not capture — and here is the second reason

`PAYOFF_SCALE` is a fixed module constant, not a function of length:

```421:421:/home/allie/strategy-behavior/hole_exp/ipd_env.py
PAYOFF_SCALE = 30.0  # 10 rounds x R=3: mutual cooperation for the whole episode
```

and it divides the training reward (`registry.py:372`) and `skill`
(`eval_capability.py:198-202`). At N=14 raw payoff rises ~40% against an unchanged
denominator, so `score` and `skill` are not comparable across lengths.

`capture` is subtler and worth stating precisely, because "capture is broken" is the
wrong summary. `registry.references` replays the scripted honest and exploit policies
through the *same* `cfg`, so both endpoints scale with length and `capture` stays
internally valid *within* a length. What changes across lengths is the span
`exploit_ref − honest_ref`, so a capture of 0.3 at N=6 and at N=14 are not the same
quantity of exploitation. Report round-index timing as the primary result, and if you
report capture at all, report it per-length and never pooled.

### A.4 The `inf` arms are a free negative control

For `_inf` cells, `core.scrub_horizon` deletes the stated total from the observation. Such
a policy has no way to know N. So its endgame timing **must not** shift between N=6 and
N=14 — and if it does, you have found a measurement artifact, not a finding. Include the
two `inf` arms for exactly this reason and say so in the log.

### A.5 Concrete design

- Envs: `ipd`.
- Lengths: 6, 10, 14 (10 is the trained length and the within-sweep anchor).
- Arms: all six cells at seed 0, at the two matched checkpoint steps from §0.3:
  **step 35** (the highest present in all six) and **step 20** (the lowest present in all
  six) as the early baseline. URIs come from
  [`hole_exp/think4_tinker_ckpts.json`](hole_exp/think4_tinker_ckpts.json).
- Opponent: pinned to each arm's trained counterpart (grim for grim arms, tft for tft),
  via `registry.rollout(..., opponent_name=...)`.
- Seeds: 16. Cost = 6 arms × 3 lengths × 16 seeds = **288 sampled episodes** per
  checkpoint step. Scripted references add 2 replays per episode but cost **zero sampler
  tokens** — they are scripted policies, not model calls.
- Output: one JSONL row per episode with `arm, step, num_rounds, seed, opponent,
  first_defect_index, defect_indices, n_scored, payoff, capture, invalid_rate`. Derive
  every figure from that file, so a re-plot never needs a re-sample.

Sanity gate before trusting anything: assert `n_scored` actually differs across the three
lengths. If it does not, `num_rounds` did not take effect and you are looking at three
copies of the same experiment.

---

## B. Did it learn the opponent, or the game?

### B.1 Correction: `run_crossplay.py` is not the tool for this

The proposal points at `run_crossplay.py --opponents`. That flag exists but means
something else entirely:

```51:52:/home/allie/strategy-behavior/hole_exp/run_crossplay.py
BASE_MODEL = "Qwen/Qwen3.6-27B"
OPPONENTS = {"base": BASE_MODEL, "frontier": "anthropic/claude-opus-5"}
```

Its `--opponents` axis is **live LLM model ids**, not disposition members. Three more
mismatches: its games are held-out TextArena two-player games (blind auction, negotiation,
Indian poker), not IPD and not the four split envs; `ARM_RUNS` is hardcoded to
`mixed_hole_d1_s0` / `mixed_nohole_d1_s0`, with no think4 arms; and `ckpt()` always takes
the max step, with no way to name one.

The matched-design language in its docstring ("every (game, seed) replayed by every arm
against the SAME opponent in the SAME seat") is real and is the property you want — but it
is a property of *that* harness's model-vs-model design, not of a grim/tft crossing.

**The right primitive** is `registry.rollout(..., opponent_name=...)`, surfaced by
`to_viewer.episodes`. `watch_capability.py` already does the matched version of this — its
own docstring says it "deliberately fixes the condition across arms so its numbers are
comparable," which is precisely the design B needs. Build on that, or write a thin sweep
over `registry.rollout` directly.

The proposal's other instinct is correct and should be honoured: **do not patch
`traces_over_training.py`.** Its pinning is deliberate and load-bearing —

```107:110:/home/allie/strategy-behavior/hole_exp/traces_over_training.py
    for shape in core.SHAPE_SPLIT:
        if f"-{shape}_" in run and cons == "nohole":
            pin = core.nohole_shape_member(shape, env)
            return [pin] if pin else pop
```

— and its pages are the input to every marker curve. Leave it alone.

### B.2 Design

Full 2×2: {grim-trained, tft-trained} × {plays grim, plays tft}, with the diagonal being
the trained condition and the off-diagonal the transfer test.

- Envs: the four that carry the split — `ipd`, `ipd3`, `staghunt`, `winasmuch`
  (`core.SHAPE_ENVS`). Members come from `core.NOHOLE_SHAPE[shape][env]`, so the crossing
  is `grim`/`tft` in `ipd`, `grim_table`/`tft_table` in `ipd3` and `winasmuch`,
  `grim_hunter`/`tft_hunter` in `staghunt`.
- Arms: all six cells (the `eg` and `inf` cells transfer differently from baseline, and
  that is interesting rather than noise).
- Seeds: 8 to start. Cost = 6 arms × 2 opponents × 4 envs × 8 seeds = **384 episodes**.
  Go to 16 seeds on `ipd` alone (192 episodes) for the headline number.
- Hold everything else fixed across cells: same seeds, same dose, same temperature, same
  checkpoint step (**35**, per §0.3). Seat is 0 for the learner throughout
  (`ipd_env.play_episode` documents "seat 0 = model, seat 1 = the drawn opponent").

### B.3 What the answer means — write this down before you look

State the two readings in the log *before* running, so the result is not read backwards:

- **Off-diagonal ≈ on-diagonal.** The opponent split changed the gradient without changing
  the learned policy. The §4 disposition result is then a claim about *training signal*,
  not about learned dispositions, and the write-up's framing has to change accordingly.
- **Off-diagonal ≠ on-diagonal.** The arms learned genuinely different policies, and
  "disposition" is doing real work.

Either outcome is publishable and the second is not the "good" one. The relevant
statistics are `exploit_rate`, `endgame_rate` and first-defect index, per cell.

Caveat to carry: one seed per arm at present, and `endgame_rate` differences of the size
reported in the handoff's §4 table (±0.05) are within plausible run-to-run variation. The
supervisor is queuing seeds 1–3; prefer to run B after at least two seeds exist, or report
it as directional.

---

## C. Faithfulness: does a stated endgame plan predict the action on that turn?

This is the most novel item and the instrumentation is genuinely already there.

### C.1 The alignment exists

`LoggingActor` records reasoning and answer from the same `act()` call, and the env only
ever sees the answer:

```93:103:/home/allie/strategy-behavior/hole_exp/sim_adaptive_traces.py
    def act(self, messages: List[dict], meta: Optional[dict] = None) -> str:
        raw = self.inner(messages, meta or {})
        reasoning, answer = split_think(raw, self.thinking)
        self.log.append({
            "reasoning": reasoning,
            "answer": answer,
            "phase": (meta or {}).get("phase"),
            "in_decision": (meta or {}).get("in_decision"),
            "round": (meta or {}).get("round"),
        })
        return answer
```

That is five fields, not four — `phase` as well as `in_decision`. This split is also what
keeps the existing behaviour metrics honest: a `[Defect]` the policy merely *considered*
inside `<think>` is not scored as the move it made. Your analysis is measuring the gap
between those two things, which only exists because the pipeline keeps them apart.

On the rendered pages the per-turn action classification is already attached to the turn
marker, next to the think block:

```123:134:/home/allie/strategy-behavior/hole_exp/to_viewer.py
        tag = t.get("parsed")
        mark = f"   [turn {i + 1}/{len(turns)}" + (f" · {tag}]" if tag else "]")
        ...
        parts.append(f"<|im_start|>assistant{mark}\n{think}{t['action']}<|im_end|>")
```

So a page alone is sufficient: split on the assistant turn markers, and each block gives
you the reasoning, the emitted answer, the turn index, and the parsed classification.
Purely analytical, no re-sampling, as the proposal says.

### C.2 Three things that will corrupt this if you skip them

**1. Restrict to `ipd`. The splice misaligns on the game cells.** `_render_episode`
indexes `reasoning[i]` against `turns[i]`, but the two lists are not the same length
outside `ipd`. `ipd_lib` appends *every* turn including the free-text ones, so for `ipd`
`len(reasoning) == len(turns)` (20 at the default length: 10 chat + 10 decision).
`game_env` appends **only decision turns** while the actor logs every turn — a sampled
`ipd3` episode has `len(_reasoning) == 10` against `len(turns) == 5`.

On `ipd3`, `staghunt` and `winasmuch` pages, the think block displayed beside a turn is
therefore **not that turn's reasoning**. This does not affect the published marker curves
(they pool blocks and never align), but it silently destroys any per-turn analysis. Do C
on `ipd` only, and file the misalignment as a separate bug — the honest fix is to filter
`reasoning_log` to decision phases before splicing, or to key it by round.

**2. Exclude truncated turns, or you will manufacture unfaithfulness.** When `</think>`
never closes, `split_think` returns all text as reasoning and an **empty answer**:

```67:68:/home/allie/strategy-behavior/hole_exp/sim_adaptive_traces.py
    # No closing tag: the thought ran out the token budget. All reasoning.
    return raw.replace("<think>", "").strip(), ""
```

and `ipd_lib` then substitutes a default:

```389:390:/home/allie/ipd_exp/ipd_lib.py
            raw = act(list(history), in_decision)
            action = raw if raw.strip() else (COOP if in_decision else "(no comment)")
```

A decision turn with a truncated think block becomes `[Cooperate]`. If the truncated
reasoning contained an endgame-defect plan, you would score it as "planned to defect,
cooperated instead" — maximally unfaithful, and entirely an artifact of the token budget.
This is not hypothetical: 5 of 20 turns in the sampled `ipd` episode in
`hole_exp/results/adaptive_sim_traces.json` have `answer == ""` with a non-empty
reasoning block.

Require a non-empty answer, and **report the exclusion rate per arm as a first-class
number**. It is also a confound in its own right: the handoff's §3 collapse was a
truncation collapse, so the exclusion rate is not independent of the arm.

**3. Filter to decision turns.** `in_decision == True` on `ipd`. A plan stated during a
chat turn resolves on the *following* decision turn, not the chat turn, so define your
unit carefully. Two defensible units, and they answer different questions:

- **Same-turn.** Marker on decision turn t's own reasoning, action on turn t. Strictest.
- **Plan-to-next-decision.** Marker anywhere in the reasoning at or before turn t since
  the previous decision, action at t. Closer to what "stated intent" means in prose, and
  will have more power.

Pick one as primary, report the other as a robustness check, and say which is which.

### C.3 Statistic

Per (arm, checkpoint step, round bucket), the conditional
`P(defect on turn t | endgame_defect_plan in the reasoning for turn t)` and its complement
`P(defect | no plan)`. The contrast between those two is the faithfulness signal; the
first number alone is not, because a policy that defects constantly scores high on it
trivially.

Then the cut the proposal actually wants: **does faithfulness differ by opponent?** A
grim-trained policy that says "defect last round" and then does, versus a tft-trained one
that says it and holds, is a real asymmetry between stated and enacted intent — and it is
a claim nobody in this project has made.

Denominators will be small. On the existing sweep configuration `ipd` contributes 3
episodes per checkpoint per arm (1 pinned opponent × 3 seeds), so ~30 decision turns, of
which the endgame window is a handful. **Raise `--seeds` for `ipd` before relying on
this**, and report exact counts, not just rates. Do not put an error bar on a
single-figure denominator.

---

## D. Four additions to the marker pipeline

All four touch `hole_exp/endgame_awareness.py` (where `MARKERS` and `HORIZON_MARKERS`
live, lines 81–166) and
`results/0826_think_curves/plot_reasoning_markers_by_opponent.py`. Note the marker
definitions are **not** in the plot script, so a regex change affects every consumer.

**Venv:** the plot script only reads JSONL and runs in `venvs/tools`. Note that contrary
to the handoff's §6 trap 3, matplotlib is currently importable in *both* venvs on this
box. That does not make merging them safe — the reason for the split is that importing
`to_viewer` in the plotting venv is fatal — but do not be surprised by it.

### D2 — plot `endgame_hold`. Do this one now; it needs nothing.

Confirmed: computed, exported to JSON, never plotted. It is in the export tuple —

```377:382:/home/allie/strategy-behavior/results/0826_think_curves/plot_reasoning_markers_by_opponent.py
                    for m, rx in (("shaping_awareness", A.MARKERS["shaping_awareness"]),
                                  ("backward_induction", A.MARKERS["backward_induction"]),
                                  ("endgame_defect_plan", A.MARKERS["endgame_defect_plan"]),
                                  ("endgame_hold", A.MARKERS["endgame_hold"]),
                                  ("notices_unknown", A.HORIZON_MARKERS["notices_unknown"]),
                                  ("assumes_finite", A.HORIZON_MARKERS["assumes_finite"]))}
```

— and absent from `PANELS` (lines 243–265).

**The claim checks out on the committed JSON**, which is on this box, so this is a
figure-only change with the finding already in hand. Mean over scored steps:

| arm | `endgame_hold` | `endgame_defect_plan` |
|---|---|---|
| grim / nohole | 0.071 | 0.230 |
| grim / eg | 0.055 | 0.186 |
| tft / nohole | 0.120 | 0.219 |
| tft / eg | 0.109 | 0.201 |

Pooled over the two finite cells: tft 0.114 vs grim 0.063, a ratio of **1.8×** (1.7× in
the baseline cell, 2.0× in the endgame-penalty cell). This is the reasoning-side analogue
of the §4 behavioural claim, in the same direction, and it is the cleanest unused result
in the wave: the policies trained against tit-for-tat *talk about holding the line at the
end* nearly twice as often as the grim-trained ones.

Add it as a panel paired with E (`endgame_defect_plan`), since hold and defect-plan are
the two directions of the same question and the regexes were explicitly built as a
directional pair — the comment block above them documents that an earlier version scored
"defecting in the last round" as a plan to hold.

**Error bar discipline.** `rates()` returns a binomial SE over `n_blocks` (192/step). On
~1500 pooled blocks per arm that SE is ~0.008 and would make this a 5-sigma effect, which
would be overclaiming: the blocks come from 3 episodes per step in one run at one seed, so
they are nowhere near independent. The honest error bar is across seeds, and seeds 1–3 are
still in the queue. Report the ratio, show the per-step curves so the reader can see the
stability, and state that the error bar is within-run — the same caveat the research log
already flags for the behavioural curves.

### D3 — export and plot `infinite_logic`

Confirmed absent from the figure pipeline: `infinite_logic` is defined in
`HORIZON_MARKERS` (lines 158–163) and has **zero** references anywhere in
`results/0826_think_curves/` — neither plotted nor written to the JSON.

One correction to the proposal's framing, in your favour. It is not uncomputed everywhere:
`endgame_awareness.py`'s own CLI already includes it in the markdown report path —

```311:312:/home/allie/strategy-behavior/hole_exp/endgame_awareness.py
        for key in ("notices_unknown", "assumes_finite", "infinite_logic",
                    "backward_induction"):
```

— so **run that CLI first**. There may already be scored output and hand-picked excerpts
to read, which would tell you whether the marker fires at a usable rate before you spend
any effort plotting it. What is missing is its presence in the published figure and JSON.

It is the third branch of the `inf` arm's own question, and the only one that says the
policy drew the right conclusion: `notices_unknown` says it spotted the missing fact,
`assumes_finite` says it hallucinated a total anyway, and `infinite_logic` says it reached
the shadow-of-the-future argument. Reporting the first two without the third leaves the
`inf` arm's most interesting outcome unmeasured — and it bears directly on §A.4, since it
is the marker that would show whether an `inf` policy *knows* it cannot locate the end.

Add it to the export tuple and as a third series in panel F. The 0825 script exported the
full marker set by construction —

```296:298:/home/allie/strategy-behavior/results/0825_shape_curves/plot_reasoning_markers.py
        dump[arm] = {key: {str(s): round(v[0], 4) for s, v in
                           sorted(rates(found[arm], rx).items())}
                     for key, rx in {**A.MARKERS, **A.HORIZON_MARKERS}.items()}
```

— consider adopting that pattern so no future marker can be silently unexported. If you
prefer the explicit tuple, add a test that asserts the exported key set equals
`MARKERS | HORIZON_MARKERS`.

### D4 — export `in_game_penalty` too

Same audit turned up a second marker missing from the JSON. `in_game_penalty` is described
in its own comment as "domain vocabulary — the false-positive floor": it measures how
loosely the arm talks about penalties in general, and so it is the baseline that makes
`shaping_awareness` interpretable. `shaping_awareness ≈ 0` (the handoff's §4 validity
result) is a much stronger claim when you can show the floor marker is *not* ≈ 0 on the
same blocks.

This one is a judgement call rather than an oversight, so argue it rather than just doing
it. `endgame_awareness.py` deliberately excludes it from the excerpt output —

```254:256:/home/allie/strategy-behavior/hole_exp/endgame_awareness.py
            for key, rx in MARKERS.items():
                if key == "in_game_penalty":
                    continue      # the floor, not a finding
```

— and that reasoning is sound for *excerpts*, where a floor marker's hits are noise. It
does not follow for the *JSON*, where the floor is what licenses the headline null. Export
the rate, keep it out of the excerpts, and say in the log that you changed the scope
rather than the intent.

### D1 — a marker for opponent modelling

There is no marker for this at all, and it is the one place where a regex is not the easy
part.

**First, verify the premise.** The claim is that the model is never told who it is playing
and must infer it from play. That is consistent with what I read — `ipd_env.play_episode`
passes the opponent as a callable and records its name only into `rec["opponent"]` for
metadata; the member name does not appear in any prompt-construction path. But absence of
a grep hit is weaker evidence than reading the observation, so before trusting any number:
grep the rendered `text` of a think page for `grim`, `tft`, `tit`, and the
`grim_table`/`tft_hunter` member names in the **system and user** blocks. If a name leaks,
the marker measures reading comprehension and the analysis is dead. Do this first; it
costs one command.

**Then the regex, and expect it to be hard.** Match *descriptions of disposition*, not
member names — the model has no names to use. Draft to iterate on, not to trust:

```
they (will|would|might) (retaliate|punish|defect back|mirror|copy|match)
| (never|won't) (forgive|cooperate again|go back)
| once (i|I) defect .{0,40} (never|forever|rest of the game)
| (opponent|they) (is|seems|looks|appears) (to be )?(a )?(tit.for.tat|grim|trigger|reciproc|retaliator)
| (copying|mirroring|matching) (my|me)
```

Two false-positive traps specific to this marker. **"grim" is an ordinary English
adjective** — "the outlook is grim," "a grim situation" — and a bare `\bgrim\b` will match
prose about the payoff table. And generic retaliation talk overlaps heavily with the
existing `in_game_penalty` marker, so a hit there is not evidence of *opponent* modelling.

Follow the discipline the file already establishes. The comments above `endgame_hold` and
`endgame_defect_plan` document two rounds of exactly this kind of failure — a pattern that
matched a plan to betray as a plan to hold, and a negation guard added because "I will not
defect in the final round" was scoring as a defect plan. **Hand-audit at least 30 hits and
30 non-hits before reporting a rate**, and consider splitting into
`opponent_model_retaliatory` and `opponent_model_forgiving`, since the grim/tft contrast
is precisely about which of those the policy infers.

**The interesting question is timing, not level.** Score it across checkpoint steps and
compare against the behavioural divergence in panels C/D: *does the reasoning name the
opponent's disposition before or after the behavioural curves separate?* Reasoning-first
is evidence the model inferred the disposition and then adapted; behaviour-first is
evidence of adaptation the reasoning only later rationalises. That ordering claim is the
payload. Note that the marker feed is sampled every 5 steps while `metrics.jsonl` is
per-step, so you can only localise the crossing to ±5 steps — say so rather than
implying finer resolution.

**Denominator mismatch to state plainly.** Markers are scored on five envs from
re-sampled episodes (`ipd trust ipd3 staghunt winasmuch`, per `watchdog_think4.sh`), and
behaviour on seven from the training log (`ipd public_goods dond trust ipd3 staghunt
winasmuch`, per `run_think4_endgame.sh`). These are different feeds with different
denominators sampled under different conditions — the think pages are re-sampled with
thinking on, which `traces_over_training.py --think` itself flags as "not the condition
any arm trained in." Any before/after claim across the two feeds inherits that gap. The
cheap partial fix is to restrict the behavioural comparison to the five overlapping envs;
that requires per-env behaviour metrics, which `train_hole.step_metrics` currently
averages away.

---

## Cost summary

| Task | Sampled episodes | Notes |
|---|---|---|
| A | 288 per checkpoint step | `ipd` only, 6 arms × 3 lengths × 16 seeds |
| B | 384 (or 192 for `ipd`-only headline) | 6 arms × 2 opponents × 4 envs × 8 seeds |
| C | 0 new, if pages exist | Analytical. Raise `ipd` seeds if power is short |
| D | 0 new | Re-score of existing pages + figure changes |

A full 150-step arm at `--groups 14 --group-size 6` is ~84 episodes/step, so ~12,600
episodes. A and B together are **under 6% of one arm**, and neither needs a trainer GPU —
only sampler capacity, which currently means sharing a port with a running trainer.

---

## What these results are *for*

The handoff proposes a possible third training arm (the hole population — always-cooperate,
doormat, noisy-cooperate — as a zero-consequence anchor, giving no punishment /
recoverable punishment / terminal punishment), and explicitly defers it: sampler capacity
is the binding constraint, an eighteen-job seed queue has the better claim on it, and the
free analyses should decide whether the arm is worth a slot. So report each result with
that decision in view.

- **If B comes back off-diagonal ≈ on-diagonal**, the two existing disposition points did
  not produce different policies, and a third punisher-vs-non-punisher point is the single
  most valuable thing you could add — it would be the first axis that moved the policy.
- **If B comes back off-diagonal ≠ on-diagonal**, disposition is already doing real work
  with two points, and the seed queue keeps its claim on the slots; spend the capacity on
  narrowing the error bar you already have.
- **If A shows the endgame anchored near round 9 regardless of N**, the wave's endgame
  results are about position, not structure, and a third arm inherits that problem. Fix
  the interpretation before buying more of it.

Note the hole arm needs no new code — every env exposes a `hole` disposition — whereas a
third `--nohole-shape` would need a named member registered in each of the four split
envs. So if the answer is "yes, add a point," the cheap version is the consequence axis,
not a third shape.

One wrinkle to check before costing that arm, though. `hole` does not mean the same thing
in every env. For `opponent_swap` specs the hole arm draws its own distinct members, but
for the rest the population is identical in both arms and only the audit differs:

```530:533:/home/allie/strategy-behavior/hole_exp/game_env.py
        else:
            pop = tuple(spec.opponents)
            # Same population both arms: the arm is the audit, not the opponent.
            self.POPULATIONS = {"hole": pop, "nohole": pop}
```

The argument for the arm is that against a non-punisher, endgame timing has no strategic
content, so endgame behaviour there is pure "the end is near" rather than "the relationship
is over." That argument only holds in the envs where the hole arm actually swaps in a
non-punishing counterpart. Verify per env which of the two mechanisms applies before
claiming the contrast covers the roster.

## Definition of done

1. §0.3a resolved, and which route you took recorded in the log. If route (b), §0.2 landed
   with the differs-from-base assertion in both the git repo and the `/shared` mirror,
   plus the §0.3b module-set assertion.
2. A JSONL of per-episode rows for A and for B, with every figure derived from it.
3. `results/0826_think_curves/reasoning_markers.json` containing `infinite_logic` and
   `in_game_penalty`; the figure containing panels for `endgame_hold` and `infinite_logic`.
4. A faithfulness table for C on `ipd`, reporting the truncation exclusion rate per arm
   alongside every rate.
5. An entry in `research_logs/0826-endgame-by-opponent.md` for each analysis, stating the
   result **and** which of the two pre-registered readings it supports.
6. The `./specs` Triton failure fixed, or explicitly recorded as still open with the
   number of cells it is costing.
7. §0.3c raised as its own item: whether the local wave's LoRA configuration
   (seven modules, α=2r) can be pooled with the seed-0 Tinker arms (`all-linear`, α=r),
   with a decision recorded before any multi-seed figure is drawn.

## Things not to do

- Do not report `endgame_rate` as evidence for or against A. It is length-relative by
  construction and will look correct either way.
- Do not pool `capture` or `score` across episode lengths.
- Do not patch `traces_over_training.py`'s opponent pinning. It is deliberate, documented,
  and every marker curve depends on it.
- Do not run per-turn faithfulness on `ipd3`, `staghunt` or `winasmuch` until the
  reasoning/turn splice misalignment (§C.2) is fixed.
- Do not use block-level binomial SEs as the error bar for a cross-arm claim. One seed,
  three episodes per step per env; the error bar is across seeds and the seeds are still
  in the queue.
- Do not load an exported Tinker adapter into the sglang server as currently launched. Its
  module set is a strict subset of the adapter's (§0.3b), so you would be serving a
  partially-applied policy.
- Do not pool seed 0 with seeds 1–3 until §0.3c is resolved. The LoRA module coverage and
  scale differ between the Tinker and local waves.
- Do not use `grim_inf` checkpoints above step 50. Steps 55–75 are the handoff's §3
  collapse and their `endgame_rate` of ~0 is forced cooperation from a broken policy.
- Do not `pkill -f` / `pgrep -f` anything (handoff §6). Kill by PID, probe ports with
  `curl`. There is a live supervisor and six live trainers on this box.
