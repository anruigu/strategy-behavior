# 0830 — think4 evals: what ran, what blocked, and two silent-wrong-answer traps

Executing `PLAN-think4-evals.md`. Written as work proceeded; §6 is the running
status.

---

## 1. The `./specs` Triton trap — FIXED, and the mechanism was not what the
##    plan (or the handoff) said

Both documents describe it as "Triton's build path invokes `gcc -B.`". That is
not it. Reproduced in-pod, isolating one variable at a time:

```
LIBRARY_PATH="…stubs:…stubs:"  gcc t.c   ->  fatal: cannot read spec file './specs'
LIBRARY_PATH="…stubs"          gcc t.c   ->  clean
```

The pod ships `LIBRARY_PATH=/usr/local/cuda/lib64/stubs:/usr/local/cuda/lib64/stubs:`
with a **trailing colon**. An empty element in a colon-list means *the current
directory*, and gcc uses `LIBRARY_PATH` entries as prefixes when it looks for
special linker files — so it tries to read `./specs`, finds `hole_exp/specs/`
(a directory), and dies. No `-B` is involved at all.

**It bites twice, and the second bite is what killed the wave.** `fla` catches
it and falls back to CPU — slow but survivable. **Triton does not catch it**:
compiling `cuda_utils.c` raises `CalledProcessError` and the cell dies.
`cell-s3-tft-nohole.log` is that crash, landing immediately after
`checkpoint step 0`, which is why all 24 run directories sat at step 0.

Both fixes are in `run_cell.sh` (each one line, independent): normalise
`LIBRARY_PATH` so no empty element can mean `.`, and launch from
`/shared/allie/think4/rundir` which has no `specs/` in it. Verified in-pod:
gcc is clean under either fix alone.

Changing cwd is safe — `registry.py` resolves specs as
`Path(__file__).resolve().parent / "specs"`, `generate_specs.py` uses
`HERE / "specs"`, and `train_mixed.py` derives every output from `--out`.

**A test cell got past the crash and reached step-0 rollouts with 52 GB
resident — then died on `torch.OutOfMemoryError` (3.31 GiB free of 267.69).**
So the specs bug was blocker one of two; local training has an independent OOM
at `--groups 14 --group-size 6` on a single B300. Not chased, because it turned
out not to be on the critical path (§3).

**Wave state when found:** all 18 seed-1..3 jobs launched 04:29–05:05 and died
within minutes; `QIDX` hit 18; the supervisor was alive with an exhausted queue.
Net: **32 GPUs reserved, all idle, zero checkpoints.**

## 2. §0.2 — checkpoint selection now loads, and refuses to guess

`LocalServiceClient.create_sampling_client` took `*a, **kw`, ignored all of it,
and returned base weights. It now accepts `model_path=`/`base_model=`, POSTs
`load_lora_adapter` for an adapter directory, and **raises** for a path-shaped
argument that is not a loadable adapter, rather than falling through to base.
`unload_adapter` added, since sglang has a finite slot count and the trainer
only reaps names it owns.

`hole_exp/ckpt_guard.py` implements the plan's differs-from-base assertion, at
temperature **0** — at 0.7 two samples from the *same* weights differ routinely
and the check would pass regardless, giving exactly the false reassurance it
exists to prevent.

**Limitation, found later and important: this guard does NOT catch a PARTIAL
adapter load (§3). Half an adapter still differs from base.** It is necessary,
not sufficient.

## 3. The trap the plan did not know about: 48% of each Tinker adapter is
##    silently dropped by this sglang build

Tinker sampling is **HTTP 402, billing blocked** — checkpoint *metadata* and
*archive export* still work, sampling does not. So the intended route (sample
the Tinker checkpoints directly) is unavailable, and the fallback is to serve
the adapters on the local sglang samplers.

That fallback silently produces a policy that never existed:

| | |
|---|---|
| adapter tensors | **994** |
| on `q/k/v/o/gate/up/down_proj` — what sglang is configured for | 512 |
| on `in_proj_q/k/v/z`, `out_proj`, `unembed_tokens` — **dropped** | **482 (48%)** |

The adapters were trained with PEFT `target_modules: all-linear` on Qwen3.5, a
**hybrid** architecture whose linear-attention path PEFT names `in_proj_*` /
`out_proj`. `POST /load_lora_adapter` returns `"success": true` and applies
just over half of it.

`--lora-target-modules all` does **not** help. sglang's
`SUPPORTED_LORA_TARGET_MODULES` (`srt/utils/common.py`) is a fixed enumeration
and `all` is exactly that list. It contains `qkvr` and `wo_ud` — sglang's own
*fused* names for those same projections — so this is a **key-layout mismatch,
not a capability gap**, and no serving flag reconciles it.

First resolution attempt — merge with PEFT, which matches by HF module name —
**also failed, and for a deeper reason.** PEFT reported:

```
Found missing adapter keys …: layers.N.linear_attn.in_proj_qkv,
                               layers.N.linear_attn.in_proj_a,
                               layers.N.linear_attn.in_proj_b
288 keys = 48 layers x 3 modules x {lora_A, lora_B}
```

**The adapters were trained against a different build of Qwen3.5 than the box
has.** Their linear-attention block exposes SEPARATE projections; the local
`/shared/clod/qwen3.8-27b` FUSES them:

| | linear_attn submodules |
|---|---|
| Tinker adapter | `in_proj_q`, `in_proj_k`, `in_proj_v`, `in_proj_z`, `out_proj` |
| local base | `in_proj_qkv`, `in_proj_a`, `in_proj_b`, `in_proj_z`, `out_proj` |

`in_proj_z` and `out_proj` match; q/k/v against fused qkv do not. So the naive
merge applies ~71%, better than sglang's 52% and still not the trained policy.

**The reconstruction is well posed, and every step was checked rather than
assumed** (`merge_ckpt2.py`):

| | |
|---|---|
| shapes | adapter q(2048)+k(2048)+v(6144) = **10240** = base `in_proj_qkv` [10240, 5120]. Exact. |
| order | `modeling_qwen3_5.py`: `torch.split(mixed_qkv, [key_dim, key_dim, value_dim], dim=-1)` → **[q; k; v]**. Read from the model source, **not** inferred — q and k are both 2048, so shape alone cannot distinguish `[q;k;v]` from `[k;q;v]`, and a swap corrupts attention silently. |
| scaling | `r=32, lora_alpha=32` → α/r = **1.0** |
| `in_proj_a` / `in_proj_b` | 48-dim, **no adapter tensors exist**, so there is no delta to lose. Not applying them is correct, not a shortfall. |

so `dW_qkv = vstack([Bq@Aq, Bk@Ak, Bv@Av]) * α/r`, added to `in_proj_qkv`.

`merge_ckpt2.py` **refuses to write unless all 994 adapter tensors are
accounted for** — consumed by PEFT or applied by hand. After three
consecutive silent partial applications in one night, that assertion is the
only thing that makes the output trustworthy.

Had any of this gone unnoticed, A and B would have produced complete,
plausible, internally consistent curves about a policy that never existed.

### 3a. Five silent partial applications, one failure mode

Getting a faithful policy out of these checkpoints took five attempts. Every
failure had the same shape — **something reported success while applying a
subset** — and none would have been visible in any downstream number:

| # | route | what it applied | how it was caught |
|---|---|--:|---|
| 1 | `create_sampling_client` ignoring its args | 0% (base weights) | plan §0.1, before I started |
| 2 | sglang `load_lora_adapter` | 52% (512/994) | counted tensors in the safetensors header against sglang's `SUPPORTED_LORA_TARGET_MODULES` |
| 3 | PEFT `merge_and_unload` | 71% (706/994) | PEFT's own `missing adapter keys` warning, which is a `UserWarning` and scrolls past |
| 4 | my accounting via `n_attached * 2` | — | assertion refused: "1280 of 994". PEFT attaches modules per its config whether or not the file has weights for them |
| 5 | my `model.language_model.` prefix | — | assertion refused: "496 absent from base". That prefix is a **serialisation** detail of `model.safetensors.index.json`; `named_parameters()` yields `model.layers.N.…` at runtime |

**Only 1 and 2 were other people's bugs; 3 was a genuine architecture
difference; 4 and 5 were mine.** The assertion caught 4 and 5 immediately, and
neither could have been caught by sampling the model — a 71%-applied or
wrongly-prefixed merge still produces fluent text, still differs from base, and
still yields a full set of plausible curves.

Two lessons worth carrying beyond this wave:

- **`ckpt_guard.assert_differs_from_base` is necessary and nowhere near
  sufficient.** It passes every one of rows 2–5. "Differs from base" is a much
  weaker property than "is the trained policy", and the gap between them is
  exactly where this class of bug lives.
- **Count the payload, not the manifest.** The truncated `grim-inf-step0035`
  download reported all 994 tensors from an intact safetensors *header* over
  11% of the data. A manifest describing the payload is not evidence the
  payload arrived — `verify_ckpts.py` checks the end-of-write marker and the
  file size for that reason, and says in its own docstring which check actually
  catches it.

### 3b. The corrected merge, verified on the tensor that mattered

`merge_ckpt3.py` reports `applied all 994 adapter tensors` for all six arms.
That is an accounting claim; this is the physical check, merged against base:

| tensor | shape | vs base |
|---|---|---|
| `linear_attn.in_proj_qkv` | [10240, 5120] | **differs 10.9%** |
| `linear_attn.in_proj_z` | [6144, 5120] | differs 10.4% |
| `linear_attn.in_proj_a` | [48, 5120] | **IDENTICAL** |
| `mlp.gate_proj` | [17408, 5120] | differs 15.4% |

`in_proj_qkv` is the one PEFT could not match and sglang would have dropped —
it moved, so the hand-built q/k/v fusion took effect. `in_proj_a` is the
control: it has no adapter tensors, and it is untouched, which is what says
the merge changed only what it had weights for rather than smearing something
everywhere. (Change fractions are modest because a rank-32 delta in bf16
leaves many elements at the same bit pattern.)

### 3c. The arms are distinct — the last gate before sampling

Accounting says all 994 applied; §3b says the fused tensor moved. Neither
rules out the six merges collapsing onto each other, which would have A and B
comparing an arm with itself. On `layers.0.linear_attn.in_proj_qkv`:

- **vs base:** 10.0–11.0% of elements changed, every arm.
- **pairwise between arms:** 12.6–13.1%, **no pair identical**.

Inter-arm distance exceeding arm-vs-base distance is the signature of six
policies that each moved in their own direction from a shared origin. Had the
merges been collapsing — the way a partial application collapses toward base —
the pairwise numbers would have come in *below* the base distances.

## 4. D2 — `endgame_hold`: reproduced, and there is a stronger statistic in it

The plan's claim checks out on the committed JSON, exactly:

| arm | `endgame_hold` | `endgame_defect_plan` | hold/plan |
|---|--:|--:|--:|
| grim / nohole | 0.071 | 0.230 | **0.309** |
| grim / eg | 0.055 | 0.186 | **0.295** |
| grim / inf | 0.023 | 0.071 | **0.317** |
| tft / nohole | 0.120 | 0.219 | **0.548** |
| tft / eg | 0.109 | 0.201 | **0.540** |
| tft / inf | 0.072 | 0.156 | **0.461** |

Pooled over the two finite cells: tft 0.114 vs grim 0.063, **1.82×** (plan said
1.8×).

**The ratio is the better statistic and the plan does not use it.** Raw
`endgame_hold` conflates "talks about holding" with "talks about the endgame at
all". Normalised, the shapes separate with **no overlap across all six cells**,
including the two `inf` arms the pooled figure excludes: every grim arm is
0.295–0.317, every tft arm 0.461–0.548. That is a cleaner claim than the
pooled ratio and it survives the `inf` cells, where the pooled version cannot go.

Error bar discipline unchanged: blocks are ~3 episodes/step from one run at one
seed, so the honest error bar is across seeds and the seeds are not there. The
per-cell consistency above is offered as stability evidence, not as significance.

**Panel added** to `plot_reasoning_markers_by_opponent.py`, paired with E.
**The figure cannot be regenerated today** — `VIEWER_DATA` holds only
`sample-negotiation-run`, so there are no pages to re-score. The finding is
from the committed JSON; the panel is code awaiting pages.

## 5. D3 / D4 — export made exhaustive

`infinite_logic` and `in_game_penalty` were both absent from the exported JSON.
Rather than extend the six-tuple by two, the export now iterates
`{**A.MARKERS, **A.HORIZON_MARKERS}`, adopting the 0825 script's pattern, so no
future marker can be silently unexported. `in_game_penalty` stays out of the
*excerpts* — that exclusion in `endgame_awareness.py` is sound and untouched;
this changes the scope of the JSON, not the intent of that.

**No numbers yet for either**: both need the pages regenerated, and the
aggregate JSON cannot be re-scored.

## 5b. Two operational notes for whoever runs this next

**`serve_merged.sh` must run on `allie-sglang`, not a train pod.** The train
pods carry torch/transformers/peft but not sglang, so
`python3 -m sglang.launch_server` there is `ModuleNotFoundError: No module
named 'sglang'` — six servers "launched" and died in 25 seconds. Only GPUs 6
and 7 are free on the sglang pod (0–5 hold base samplers for the dead
trainers, left alone in case the wave restarts), so arms are served **two at a
time** and the eval rotates.

**`--page-size 1` is required to serve these merged models, and its absence
is invisible.** Qwen3.5 is a hybrid with a Mamba block and sglang asserts
`MambaComponent requires page_size=1 when mamba_extra_buffer is disabled, got
64`. The base samplers in `start_sglang.sh` never hit it because
`--enable-lora` forces page_size=1 implicitly; a merged server deliberately
runs *without* LoRA, so it defaults to 64 and the child dies with a bare
`Received sigquit from a child process`. The real assertion is ~900 lines up
the log.

**Watch process LIVENESS, not error strings.** That failure cost 40 minutes,
because the watcher enumerated fatal patterns (`^Traceback`,
`OutOfMemoryError`, `Address already in use`) and the actual death was a
`sigquit` after an `AssertionError` — matching none of them — so the loop
simply timed out against a server that had been dead since its second minute.
Checking "is a `launch_server` process still alive" catches every exit path,
including the ones nobody predicted.

**Do not grep sglang or torch logs for `error`.** Two false alarms tonight came
from exactly that. The torch deprecation banner contains *"will be an error in
a future release"*, and sglang prints *"Ignore import error when loading
sglang.srt.models.inkling: No module named 'helion'"* as normal startup
chatter. Both match `grep -i error` and neither is a failure. The patterns
worth watching are `^Traceback`, `torch.OutOfMemoryError`, `Address already in
use`, and `Killed`; healthy progress is `Load weight begin` → `Load weight
end` → the server answering `/health`.

## 5c. Where A and B stopped: no GPU

Everything A and B need is built and verified. They are blocked on one thing:
**there is no GPU to serve a merged model on.**

- The train pods (24 idle GPUs) **do not have sglang installed** — it lives in
  the sglang pod's container image at `/sgl-workspace/`, not on `/shared`, and
  it carries compiled CUDA kernels, so it is not something to PYTHONPATH
  across images.
- The sglang pod's GPUs 6 and 7 were free at 06:05 and were **taken at
  06:35:48 by two new base samplers on ports 8106/8107** (`--enable-lora`,
  `/shared/clod/qwen3.8-27b`) that this session did not start — someone
  expanding the pool from six slots to eight, presumably to restart the wave.
- All eight GPUs now hold ~228 GB of 275 GB. A merged 27B needs ~54 GB and
  does not fit in the ~47 GB beside a base sampler.

**This is a shared-resource decision, not a technical one, and it is left to a
human.** One sampler stopped on the sglang pod frees a GPU and A runs; the
same GPU is presumably wanted for the training restart. Both claims are
legitimate and I do not know which is worth more.

Everything else is ready: six merged arms verified distinct (§3b, §3c),
`serve_merged.sh` with the `--page-size 1` fix, `serve_all.sh` targeting the
right pod, and `eval_a_endgame_length.py --sampler <url>` to point A at a
served arm.

## 6. Status

| task | state |
|---|---|
| `./specs` fix | **done**, verified in-pod, mechanism corrected |
| §0.2 checkpoint selection + guard | **done** |
| Tinker checkpoint catalog | **done** — `hole_exp/think4_tinker_ckpts.json`, all 6 arms |
| D2 finding | **done**, strengthened |
| D2 panel / D3 / D4 code | **done**; figures blocked on pages |
| Adapters downloaded + integrity-checked | **done** — 12/12, one truncated and re-fetched |
| Merges, all 994 tensors, arms verified distinct | **done** — 6/6 at step 35 |
| A / B / C sweep code + A's figure | **written**, dry-run clean |
| D1 premise (no opponent-name leak) | **verified** |
| A / B results | **blocked: no GPU to serve a merged arm** (§5c) |
| C results | rides on A's sample; blocked with it |
| D3 / D4 numbers | blocked on reasoning pages, which do not exist on this box |

**Steps 20 and 35 are the only two present in all six arms** (grim tops out at
35), and 35 is safely before `grim_inf`'s degeneration at ~51. That is the
early/late pair A and B should use.
