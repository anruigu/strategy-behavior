# Training best practices

Hard-won lessons from RL fine-tuning runs on exploit-bench, each tied to the
concrete mistake that produced it so the rule is credible and the check is
obvious. When you add one, lead with what actually went wrong — generic advice
("test your code") gets ignored; "two processes clobbered one JSONL, here's how
you'd catch it" does not.

---

## Measurement: what you train on and against
### Held-out eval on the cadence, not only at the end

The in-loop `compliant`/`leak`/`inadequate` are on the **training** cases and do
not witness generalization. The "is it actually less exploitable, and does it
transfer" number is the frozen held-out panel, and it has to be a **curve over
steps**, not a single end-of-run scalar — a regression that only shows at the
final checkpoint has already cost the whole run.

Wire it into the loop at the checkpoint cadence, and **import the offline
scorer** (`score_channel`) rather than re-implementing it, so the in-loop curve
and the end-of-run matrix are provably the same measurement. Wrap it so an eval
failure costs the eval, not the training step.

### A diagnostic that never varies is not a diagnostic

The loop first logged `reward_by_class`, but `customer_class` is `"adversarial"`
whenever a lever is applied — and in training a lever is *always* applied, so the
field was constant and the entitled-vs-contested split it was supposed to show
was invisible. Log the thing that actually varies (`reward_by_underlying`, read
off the scenario). Before trusting a per-group metric, confirm the group label
takes more than one value in the batch.

### Seed evals with a stable digest, not builtin `hash()`

The held-out eval seeded episodes with `abs(hash((tech, case, channel)))`. Python
randomizes `hash()` per process (`PYTHONHASHSEED`), so two arms evaluating the
*same* base model (step-0 checkpoint, byte-identical weights) drew different
adversary variants and reported lift of −0.006 vs +0.301 for what should be one
number. `hash()` is stable *within* a process, so a single arm's curve is still a
valid trend — but any cross-process or cross-arm comparison of absolute values is
confounded. Use `hashlib.sha256(...).digest()` for anything a second process must
reproduce. This is also why the definitive transfer matrix runs in one process
over all checkpoints, not per-arm in the training loop.

### Let the data correct the instrument

The identity eval's headline metric put the `impostor` cell inside the
"should-be-invariant" set. Every target dropped sharply on it — which is
*correct* behaviour (a caught liar should get less) — so the metric reported
correct behaviour as bias, significant at p<0.001. The fix was to the metric, not
the finding. When a measure flags every model as failing the same way, suspect
the measure. Every cell in an invariance set needs an argument for why a *correct*
model would be flat there, not merely that the oracle doesn't move.

---

## Ops: launching and not losing runs

### Detach with `setsid`, not bare `nohup`

The first control arm died silently between its meta line and its first step, no
traceback. Cause: `nohup` only blocks SIGHUP; the process stayed in the launching
shell's process group, so a group-directed signal took it down with the shell.
Launch long runs with `setsid ... < /dev/null > log 2>&1 &` so they get their own
session. The failure is nasty because the log looks like a healthy start — a
`.jsonl` with only a meta line and no steps is this bug.

### One launch per command — chained `nohup ... & ; nohup ... &` mangles quoting

Two arms launched on one line had the second's redirect absorbed into its argv;
it ran with no log and, worse, wrote the *first* arm's output file. Use a launcher
script that takes one arm and does the redirect + detach itself
(`results/run-rl-cs.sh`), one invocation per arm.

### One writer per output file — check for it

Because of the two bugs above, two independent training loops wrote the same
JSONL for hours. Symptom: **duplicate step numbers** (`grep -oE '"step": [0-9]+'
file | sort | uniq -d`) and total lines ≠ distinct steps. Both opened with `"w"`
(truncate-on-open), so each restart wiped the other's early history. If you must
run overlapping arms, they get distinct output paths, full stop; a quick
duplicate-step check after launch catches a collision before it costs a night.

### Checkpoint persistence is default-on, or the run is unevaluable

The loop ran for 12 hours using ephemeral per-step samplers and never called
`save_weights_for_sampler`. Result: no reloadable artifact, so the held-out eval,
the transfer matrix, and every generalization question were impossible from a
"finished" run. `--save-every` now defaults to on. Save at cadence **and** a
final checkpoint with a distinct name (`-final`) — the backend (Tinker) refuses
to overwrite a name, so a cadence save landing on the last step collides with the
final save unless the names differ. Record the returned path in a sidecar so a
separate process can reload it.

**Rule:** a training run that cannot be evaluated after it exits is a training
curve, not a result. If it saves no checkpoint, it is not done.

---

## Integration: talking to the model and the backend

### Smoke-test each stage against the real backend before the long run

In order, each cheap, each catching a different failure: backend reachable →
base model available/trainable → one real optimizer step end-to-end → the gate
runs against a *live* sampler (not just a registry name) → a checkpoint saves and
its path is non-empty. A 90-second smoke that surfaces a pydantic type error or a
name collision is worth more than discovering it at hour six.

### Verify the wire format renders for the target's own chat template

gpt-oss uses the harmony format; the tool-channel layout (synthesized
`tool_calls` + `tool` results) has to survive `apply_chat_template` or the
provider rejects it and you measure HTTP errors. Smoke the exact rendering (1
step) on the exact model before a long run — do not assume a layout that works on
one template works on another.

### A sampling profile is per-model, and every stage needs the same one

Qwen3.6-27B and Qwen3.8-27B on the *identical* tool-loop environment, with the
shipped settings (t1.0 / 384 tokens / EOS stop / thinking off): **0.016 invalid
vs 0.927**. Two causes, neither sufficient alone — the Qwen3.8 chat template
resolves `reasoning_effort` to **`xhigh`** whenever thinking is on or undefined,
and with no stop sequence the model rambles past its own action and is cut off
mid-argument (`[resolve_warranty claim=38,`). Fix is
`temperature 0.7 / top_p 0.9 / max_tokens 512 / stop on "]"`, thinking off →
0.023. Raising `max_tokens` alone makes it worse (more rope); so does hardening
the prompt. Do **not** combine a `]` stop with thinking — a bracket inside the
`<think>` block halts generation before the answer. Full workup:
`research_logs/0820-qwen38-sampling-profile.md`.

The operational half: **the corpus generator, the checkpoint screen, the viewer
push and the RL loop each build their own actor**, and missing the profile in
any one of them fails differently and quietly — the corpus distils format
failures, the gate reads format failure as a floor and refuses to launch, the
viewer publishes the model's worst behaviour as if it were its behaviour, and
the arms train on unparseable turns. Put the profile in one named constant and
have every stage take it.

### Track `invalid_rate` in the verdict, not just the report

`check_suite`'s headroom verdict read the exploit rate and the episode share and
ignored `invalid_rate`, so a cell at **0.927 invalid / 0.093 exploit over 29
decisions** was reported **`ok`** and would have passed a wave gate. It was
measuring whether the model can close a bracket. There is now a `BROKEN` verdict
above `SCREEN_MAX_INVALID = 0.25` — a different problem from `FLOOR`, wanting a
different fix (format, budget, or model — not dose or density). Any gate that
reads a behavioural rate should refuse to read it when the denominator is mostly
garbage.

### Fail loud on an unsupported factor; never silently no-op

`TinkerTarget` initially could not render the `tool` channel. The safe failure was
to **raise** — "S2 is not runnable, here's what to build" — not to train the
`user` layout while recording `attacker_channel=tool` in the meta block, which
would make every downstream conclusion false. A factor that is recorded but not
applied is worse than one that is refused.

### Track empty replies as a first-class validity column

An empty target turn grants nothing and so scores as *maximal resistance* — a
rising empty-reply rate manufactures exactly the robustness curve the run is
trying to earn honestly. Log it every step (`empty`), not just at the end, and
size `--max-tokens` above the model's reasoning budget so a reasoning model's
thinking doesn't exhaust the completion before it reaches its action line.

---

## The shape of a healthy run

The three-number frontier, read together, never singly:

- **exploitation lift** (held-out) — down
- **entitled `inadequate_rate`** — flat (rising = the stonewaller collapse; the
  reward is being satisfied by refusing rather than by getting the grant right)
- **out-of-domain instruction-following** — flat

with the safety probes (harmful-compliance, injection) as one-sided guardrails:
flat-or-down is a pass, up is a hard stop. Reward rising while `inadequate` rises
is not a win. `compliant` flat at zero while reward rises means the reward is
being gamed by something other than the grant. Any of it is void if `empty` is
climbing or a gate is red — those come first.
