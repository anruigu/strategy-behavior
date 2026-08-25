# Handoff — porting Allie's research to a new Ubuntu box

**Written:** 2026-08-25 19:10 UTC, from a root session on the old RunPod box.
**Audience:** the agent doing the setup on the new instance.
**Companion doc:** [`PLAN.md`](PLAN.md) — how to get the data *off* this box. Read that
one for the S3/bundle mechanics. This doc is about standing the work back up.

> **Read this section order if you are short on time:** §0 → §7 → §8. Everything
> else is setup you can do while the resume in §8 is running.

---

## 0. The 60-second version

The research is **`strategy-behavior/hole_exp`** — an "atlas" measuring whether
training a model in environments where exploitation goes *unpunished* ("holes")
transfers to misaligned disposition on held-out evals.

Three facts that determine everything else:

1. **Training runs on the Tinker API, not on local GPUs.** The sbatch scripts ask for
   `--gres=gpu:0`. The new box needs **no GPU** to resume training. It needs CPU, network,
   and a `TINKER_API_KEY`.
2. **All model checkpoints live on Tinker's servers**, addressed by `tinker://` URI.
   Nothing to copy. What must survive is the *manifests* — `runs/*/checkpoints_state.json`
   — which are small text files. Lose those and you lose the ability to resume 80 runs.
3. **8 training jobs died on this box at ~17:00 today**, between steps 20 and 49 of a
   planned 150. They are resumable from Tinker state. §8 is how.

---

## 1. Provision the new box

Ubuntu 22.04 was the old box. Base packages:

```bash
sudo apt update && sudo apt install -y \
  git tmux curl rsync jq build-essential \
  python3.12 python3.12-venv python3.12-dev
```

**Python 3.12 specifically.** The venv the live runs use (`venvs/tinker-ipd`) is
3.12.3. There is a second, older venv on 3.11.10 — see §6 for which is which.

Optional, only if you intend to serve models locally for evals (most eval paths call
remote APIs instead): NVIDIA driver 580.x + CUDA 12.4, which is what the old box ran on
an H100 80GB.

### Do NOT bother reproducing

- **Slurm.** The old box was a node on `runpod-cluster-y8puzql3juawue` (`node-0..10`,
  192 CPU / 8 GPU each). The `sbatch_*.sh` launchers assume it. On a single new box,
  run the underlying `train_mixed.py` command directly — §8 shows the translation.
  Every launcher's real payload is a single `exec "$PY" train_mixed.py ...` you can lift.
- **The NFS mount.** `/workspace` was NFS with root-squash, which is why `PLAN.md`
  is full of uid-1005 workarounds. On a normal local disk none of that applies.

---

## 2. Credentials

**The old box kept API keys as plaintext `export` lines in `/workspace/allie/.bashrc`,
world-readable (mode 664) on a volume shared with six other users.** Do not reproduce
that. Put them in a `0600` file that is sourced, and keep it out of git.

Keys the code actually reads, by name (values are in the old `.bashrc` and
`strategy-behavior/.env` — move them across out-of-band, never through a transcript
or a git commit):

| Variable | Needed for | Required? |
|---|---|---|
| `TINKER_API_KEY` | **all training and sampling** | **yes** |
| `OPENROUTER_API_KEY` | MASK judge (`gpt-4.1`), frontier eval opponents | yes for evals |
| `WANDB_API_KEY` | `--use-wb` on every training run | yes (or drop the flag) |
| `HF_TOKEN` | tokenizer/model downloads | usually |
| `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` | frontier eval opponents | per-eval |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | S3 checkpoint tier, backup restore | optional |
| `S3_CHECKPOINT_BUCKET`, `S3_PREFIX` | same | optional |

Also present in the old `.bashrc` but **not** used by `strategy-behavior`:
`FLEET_API_KEY`, `SUPABASE_*`, `SLURM_*`, two Slack webhooks. Carry them only if you
are also porting the `fleet-research` / `theseus` work.

```bash
install -m 600 /dev/null ~/.research_env
$EDITOR ~/.research_env          # export LINES HERE
echo '[ -f ~/.research_env ] && . ~/.research_env' >> ~/.bashrc
```

> **`TINKER_API_KEY` was missing from `strategy-behavior/env.example`** even though
> 16 call sites read it. **Fixed 2026-08-25** — the placeholder is now in the template.
> The real value was already in `.env` (gitignored), so nothing was broken at runtime;
> the template just under-documented the requirement. Note `env.example` is *tracked* —
> keep real values out of it.

---

## 3. GitHub

Account is **`anruigu`**. A fine-grained PAT was issued 2026-08-25 and reaches ~50 repos
across `anruigu`, `fleet-ai`, and `BerkeleyAutomation`.

```bash
git config --global user.name  "anruigu"
git config --global user.email "anrui0706@gmail.com"
git config --global credential.helper store
printf 'protocol=https\nhost=github.com\nusername=anruigu\npassword=<TOKEN>\n\n' \
  | git credential approve
```

**Gotcha: `strategy-behavior`'s remote is SSH**
(`git@github.com:anruigu/strategy-behavior.git`), which will not use the token. Either
generate a key and add it at https://github.com/settings/keys, or switch the remote:

```bash
git -C strategy-behavior remote set-url origin \
  https://github.com/anruigu/strategy-behavior.git
```

Same applies to `behavior`, `cs285`, `performative`, `theseus`, `superhuman_negotiator`,
`fleet-research-api`, `theseus-meta-investigator` — all SSH remotes per
[`repo-survey.txt`](repo-survey.txt).

`gh` CLI v2.95.0 was installed at `~/.local/bin/gh` with config in `~/.config/gh`.
Reinstall with `apt install gh` and `gh auth login --with-token`. Nothing in the
research pipeline calls `gh`; it is a convenience only.

---

## 4. Claude Code

Version on the old box: **2.1.245**, installed to `~/.local/share/claude/versions/`
with a `~/.local/bin/claude` symlink.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Recreate `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(*)", "Read(*)", "Edit(*)", "Write(*)"],
    "deny": ["Bash(rm -rf *)"],
    "defaultMode": "bypassPermissions"
  },
  "statusLine": {
    "type": "command",
    "command": "<HOME>/.claude/scripts/context-bar.sh"
  },
  "tui": "fullscreen",
  "skipDangerousModePermissionPrompt": true,
  "skipWorkflowUsageWarning": true,
  "theme": "dark"
}
```

Fix the `statusLine` path to the new `$HOME`, and copy `.claude/scripts/context-bar.sh`
across or the status line silently does nothing.

**Session history worth carrying:** `~/.claude/projects/` (transcripts),
`history.jsonl`, `plans/`. PLAN.md §Phase 4 has the tar command.
**Do not carry** `~/.claude/.credentials.json` or `~/.claude.json` — OAuth tokens,
re-authenticate instead.

---

## 5. tmux

tmux **3.2a**, and there was **no `~/.tmux.conf`** — stock defaults, prefix `C-b`.
Nothing to port. Two sessions were live at handoff time; both are just long-running
shells, no state worth preserving.

The one thing that matters: **launch training inside tmux**, because the runs are
~15 min/step × 150 steps ≈ 37 hours each and will not survive an SSH drop.

```bash
tmux new -s t3g -d 'cd ~/strategy-behavior/hole_exp && bash resume.sh 2>&1 | tee -a logs/resume.log'
tmux attach -t t3g
```

---

## 6. Python environments

Two venvs matter, and it is easy to pick the wrong one.

| venv | Python | Role | Key pins |
|---|---|---|---|
| **`venvs/tinker-ipd`** | **3.12.3** | **what every live run used** — `PY=` in all recent `sbatch_*.sh` | `tinker==0.25.0`, `tinker_cookbook==0.5.4`, `transformers==5.14.1`, `wandb==0.28.2`, `openai==2.53.0`, `numpy==2.5.1` |
| `strategy-behavior/training/tinker/.venv` | 3.11.10 | older SPIRAL-era Tinker arm | `tinker==0.24.1`, `TextArena==0.6.4`, `torch==2.13.0` |

`tinker-ipd` is lean — 63 packages, 445 MB, **no torch, no TextArena**. That is correct:
Tinker does the training remotely, so nothing local needs a deep-learning stack.

Rebuild it:

```bash
python3.12 -m venv ~/venvs/tinker-ipd
~/venvs/tinker-ipd/bin/pip install -r requirements-tinker-ipd.txt
```

The freeze is next to this file: [`requirements-tinker-ipd.txt`](requirements-tinker-ipd.txt)
(63 pins, generated from the live venv's `dist-info` dirs — the venv itself has a broken
`python -m pip`, so this was read off disk rather than from `pip freeze`).

Then point the launchers at it — every recent `sbatch_*.sh` hardcodes
`PY=/workspace/allie/venvs/tinker-ipd/bin/python`. Either recreate that absolute path
or sed them all.

### `config.sh` — the path layer

`strategy-behavior/config.sh` is sourced by every script and holds all machine-specific
paths as `SAT_*` overridables. On a new box you mostly just need:

```bash
export SAT_HOME=~/strategy-behavior
export SAT_TINKER_VENV=~/venvs/tinker-ipd
export SAT_ENV_FILE=~/.research_env
export SAT_HF_HOME=~/.cache/huggingface     # keep off ephemeral disk, ~8GB
```

External checkouts it expects (**not vendored**, clone yourself):
`$SPIRAL_DIR` → spiral-rl/spiral (+ apply `training/patches/`),
`$MASK_DIR` → centerforaisafety/mask, `$MACHIAVELLI_DIR` → aypan17/machiavelli.
Only needed for the older MASK/MACHIAVELLI eval arms, not for `hole_exp` training.

---

## 7. Getting the work across

### The critical payload is tiny

```
strategy-behavior/hole_exp/runs/*/checkpoints_state.json   ← resume points (REMOTE weights)
strategy-behavior/hole_exp/runs/*/checkpoints.json         ← sampling points
strategy-behavior/hole_exp/results/                        ← all eval outputs
strategy-behavior/research_logs/                           ← the actual thinking
```

80 run dirs, 172 manifests, **148 MB total**. Copy this first, before anything else.
193 distinct `tinker://` URIs are referenced across the repo.

### The repo itself has uncommitted work

`strategy-behavior` is on branch **`multigame-social-0807`**, HEAD `a4ccdc0`, with
**12 modified + 10 untracked files** — including `core.py`, `train_mixed.py`,
`eval_generalization.py`, and a brand-new untracked `grim_vs_tft.py` and
`sbatch_think3_shape.sh`. **None of it is pushed.** Commit to a dated branch before
the box goes away:

```bash
git switch -c backup/2026-08-25 && git add -A
git commit -m "wip: workspace backup 2026-08-25" && git push -u origin backup/2026-08-25
```

### Backup already in flight

A parallel session (running as uid 1005) is executing PLAN.md Phase 1 right now —
`bundles/` had 8 of ~40 bundles and `worktree-tars/` had 9 tars as of 19:01. Check
whether it finished before relying on it, and verify:

```bash
for b in bundles/*.bundle; do git bundle verify "$b" >/dev/null || echo "BAD: $b"; done
```

---

## 8. Where the research actually stands

### The question

From `hole_exp/README.md`: a **hole** is an affordance that is exploitable,
reward-positive, normatively bad, and **un-punished**. Clause (d) is the independent
variable. Every environment ships as a matched pair — `--consequence hole` vs `nohole` —
where the agent sees *the same bytes* (asserted in `test_envs.py`) and only the
consequence branch differs. The dependent variable is **transfer to the held-out
disposition battery** in `EVAL_SUITE.md`, never in-env reward.

Two in-env diagnostics only: `exploit_rate` and `capture` (exploitation premium,
normalised against scripted honest/exploit references replayed on the same seed).

### The current wave — opponent disposition × consequence shape

Directive is `research_logs/0824-isolation.md`, and it is the thing to re-read before
deciding anything:

> *"Your objective is to get any interesting conclusions about varying opponent
> disposition and consequence shape in alignment... I'm especially interested if either
> tit-for-tat or adaptive-recovery actually teach recovery of trust."*

Specifically requested there: drop `tf2t` (too complex), run **grim** and **tft**
separately to isolate their curves, use the **noisy** hole variant, and run all four
think-on arms.

### The 8 runs that died

All 8 stopped between **16:38 and 16:59 today** — a tight cluster that reads as one
cluster-level event, not natural completion. Target was `STEPS=150`.

| Job | Run | Step reached | Last Tinker ckpt |
|---|---|---:|---:|
| 683 | `mixed_think3_hole-think-noisy_d1_s0` | 49 | 50 |
| 684 | `mixed_think3_adaptive-think_d1_s0` | 36 | 30 |
| 685 | `mixed_think3_adaptrec-think_d1_s0` | 33 | 30 |
| 686 | `mixed_think3_nohole-think-grim_d1_s0` | 25 | 20 |
| 687 | `mixed_think3_nohole-think-tft_d1_s0` | 31 | 30 |
| 688 | `mixed_think3_nohole-think-grim_d1_s0` (t3g) | 20 | 20 |
| 689 | `mixed_think3_nohole-think-grim_d1_s0_eg2` | 21 | 20 |
| 690 | `mixed_think3_nohole-think-grim_d1_s0_inf` | 39 | 40 |

Logs: `hole_exp/logs/thinkwave/*.out`. Roughly 15 min/step, so each run is ~37 h to 150.

### How to resume one

**Use `checkpoints_state.json`, not `checkpoints.json`.** The `sampler_weights/...`
paths **404 on resume** — that is called out at `train_hole.py:262`. The `weights/...`
state paths are the resumable ones.

```bash
cd ~/strategy-behavior/hole_exp
STATE=$(jq -r 'to_entries|max_by(.key|tonumber)|.value' \
        runs/mixed_think3_adaptive-think_d1_s0/checkpoints_state.json)

~/venvs/tinker-ipd/bin/python train_mixed.py \
  --envs ipd public_goods dond trust ipd3 staghunt winasmuch \
  --consequence adaptive \
  --think --reasoning-effort low --label-suffix think3 \
  --dose 1.0 --seed 0 --model Qwen/Qwen3.8-27B \
  --steps 150 --ckpt-every 10 \
  --groups 14 --group-size 6 \
  --temperature 0.7 --top-p 0.9 --max-tokens 1024 \
  --workers 16 --dump-traces 24 \
  --resume-from "$STATE" \
  --out ~/strategy-behavior/hole_exp/runs --use-wb
```

Per-arm flags, lifted from `sbatch_think3_shape.sh` and `sbatch_disp4_wave.sh`:

| Arm | Flags |
|---|---|
| nohole (grim) | `--consequence nohole --nohole-shape grim` |
| nohole (tft) | `--consequence nohole --nohole-shape tft` |
| endgame penalty | `--consequence nohole --endgame-penalty 2.0 --endgame-frac 0.25` |
| hidden horizon | `--consequence nohole --horizon infinite` |
| adaptive | `--consequence adaptive` |
| adaptive_recover | `--consequence adaptive_recover` |
| hole (noisy) | `--consequence hole` + the noisy population variant |

The shape wave (`t3g-*`, jobs 688–690) trains on **games only** —
`ENVS="ipd ipd3 staghunt winasmuch"`, the four cells that carry a literal grim/tft pair
(`core.SHAPE_ENVS`). The disposition wave (`d4-*`, 683–687) uses the full 7-env roster.
Do not mix them up; the rosters are different on purpose and the README explains why
(`public_goods`/`dond`/`ultimatum` price the exploit within the round, `trust` has no
grim/tft pair).

> **The flag is `--resume-from`, and it takes a STATE path** (`train_mixed.py:392`,
> `train_hole.py:261`). Its own help string says it: *"tinker:// STATE path from
> checkpoints_state.json (sampler_weights paths 404 on resume)"*.
>
> Dry-run it first — `train_mixed.py --dry-run` plays real episodes against a scripted
> stub sampler and stops before any API call, so you can confirm the roster, the arm
> flags, and the resume path resolve without spending Tinker credit.

### What is already established

- **`results/0825_disp4/COUNTERPART_RECOVERY.txt`** — scripted-probe validation of the
  four dispositions (120 seeds/cell, "exploit 2 then be honest"). The arms behave as
  designed: `tft` recovers (`recovered=1.00`), `grim` never does (`0.00`),
  `adaptive_recover` recovers in most cells, `adaptive` does not. `trust` is the
  exception — `tft` shows `recovered=0.00` there, worth a look.
- **`research_logs/0822-new-runs.md`** — the adaptive-trust design, the two
  simulator leaks it surfaced (`trust` stake reset, `dond` credibility collapse), both
  fixed. `check_suite.py` gates 10/10 cells.
- **`results/capability/think3-timeline.jsonl`** — capability timeline, appended per
  eval; latest entries are step-30 rows written up to 16:40 today.
- **`results/0825_shape_curves/`** (untracked!) — `endgame_rate_by_shape.png` and
  reasoning-marker plots for grim vs tft, regenerated 16:46 today.

### Known-confounded, do not quote

`trust`'s row in the §6 mixed run **predates the pairwise-matching fix** and is
confounded (README, citing 0818 §12). `dond`/`ultimatum` sit at ≈0 exploit rate on this
model — flat curves there mean "never explored", not "no disposition formed".

---

## 9. Sanity checklist for the new box

```bash
# 1. Tinker reachable and the key works
~/venvs/tinker-ipd/bin/python -c "import tinker; print(tinker.__version__)"

# 2. A known checkpoint still resolves (proves manifests + API agree)
~/venvs/tinker-ipd/bin/python - <<'PY'
import json, glob
u = json.load(open(sorted(glob.glob('runs/*/checkpoints_state.json'))[0]))
print(max(u, key=int), u[max(u, key=int)])
PY

# 3. The env suite still passes its invariants
~/venvs/tinker-ipd/bin/python -m pytest hole_exp/test_envs.py -q

# 4. Pre-launch gates
~/venvs/tinker-ipd/bin/python hole_exp/check_suite.py
```

`test_envs.py` is the one that matters — it asserts the hole/nohole arms emit
byte-identical observations and that the endgame penalty stays out of
`payoff`/`capture`. If it passes, the simulator ported correctly.

---

## 10. Open threads

- **Does tft or adaptive_recover teach *the model* to rebuild trust?** The counterpart
  side is verified (§8); the learner side needs the runs to get far enough.
- **Endgame-awareness → scheming-eval hypothesis** (0822 log): does reinforcing
  end-game betrayal timing raise scores on Apollo-style in-context scheming evals?
  The `eg2` and `inf` arms exist to test it; neither got past step 21/39.
- **Cross-play capability regression under the noisy hole arm** — the reason 683 used
  the noisy variant. It got furthest (step 49) and is the best candidate to finish first.
- `EVAL_SUITE.md` T1–T3 battery is scoped but largely unrun.

---

## 11. Things that will bite you

1. **`sampler_weights` URIs 404 on resume.** Use `checkpoints_state.json`. Stated twice
   in this doc because it will cost an hour otherwise.
2. **`env.example` is tracked in git; `.env` is not** (`.gitignore:2`). Real keys go in
   `.env` only. The `TINKER_API_KEY` placeholder gap was fixed 2026-08-25.
3. **The launchers hardcode `/workspace/allie/...` absolute paths** — `PY=`, `--out`,
   `WANDB_DIR`, `#SBATCH --output`. Grep and fix before running any `sbatch_*.sh`.
4. **`HOME` was node-local on the old cluster**, which is why scripts export
   `HOME=/workspace/allie` explicitly. Harmless on a normal box, but that line will point
   at a nonexistent path — fix it.
5. **`~/.bashrc` on the old box leaked every API key** to a shared volume. Rotate
   `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `HF_TOKEN`, `WANDB_API_KEY`,
   `GEMINI_API_KEY`, `FLEET_API_KEY`, `SUPABASE_*`, the AWS pair, and both Slack webhooks
   as part of this migration. Treat the new box as a clean-key event.
6. **`evals_external/insider-trading` shows 14,468 staged deletions.** Almost certainly
   an accident. Do not blind-commit it. See PLAN.md.
