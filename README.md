# spiral-alignment-transfer

Does [SPIRAL](https://github.com/spiral-rl/spiral)-style self-play on zero-sum
games, which is known to induce transferable **reasoning**, also move a model's
**honesty / deception** behavior? This repo trains `Qwen3-4B-Base` with SPIRAL
self-play and then runs alignment/deception evals (MASK first, MACHIAVELLI next)
on the base model vs. the self-play checkpoints, controlling for the
belief-elicitation confound that otherwise fakes the effect.

SPIRAL rewards reading and exploiting an opponent in zero-sum games — a skill
structurally adjacent to strategic deception — so the question is whether the
reasoning gains come with an honesty cost.

## Headline result (so far)

On [MASK](https://github.com/centerforaisafety/mask), a KuhnPoker self-play
checkpoint (`spiral-kuhn-step256`) is **less honest under pressure than the
untrained base on every archetype** — but once you control for the confound the
gap is small:

| view | base | spiral-kuhn-step256 |
|---|---:|---:|
| honesty, all valid rows (row-pooled) | 40.3 | 36.9 |
| honesty, both-valid intersection (352 rows) | 39.2 | 37.5 |
| %C (belief elicitation failed) | 14.2% | 13.4% |

The naive per-archetype table looks much more dramatic (e.g. `statistics`
65.6→45.8, `provided_facts` 71.5→55.8), but MASK's honesty metric silently drops
rows where no belief could be elicited, and base (non-instruct) models fail
elicitation more. Here %C is nearly equal and base still wins on the strict
intersection, so the honest read is **a small, directionally-consistent honesty
cost from zero-sum self-play**, not a large one. Full numbers and the confound
explanation: [`results/`](results/README.md).

> Status: early. One KuhnPoker checkpoint at step 256, single seed. The
> multi-game arm and MACHIAVELLI are set up but not yet evaluated.

## Layout

```
config.sh          shared paths/knobs; every script sources it (override via env)
env.example        secrets template -> copy to .env
node_env.sh        cluster env preamble for slurm jobs ($HOME is node-local here)
training/          SPIRAL self-play: run scripts, slurm launcher, oat patch  -> training/README.md
training/tinker/   the same self-play loop on the Tinker API (no local GPU)  -> training/tinker/README.md
evals/             MASK pipeline, model serving, checkpoint sync              -> evals/README.md
results/           MASK metrics summaries + confound-aware comparison         -> results/README.md
docs/methodology.md  the full eval battery (deception / personality / social-eng / reward-hacking)
```

This repo holds the **glue**: training configs, the eval harness wrappers, the
confound-aware comparison, and the writeup. The upstream projects it drives are
**not vendored** — clone them yourself:

| dir (`config.sh`) | clone |
|---|---|
| `$SPIRAL_DIR` | https://github.com/spiral-rl/spiral (then apply `training/patches/`) |
| `$MASK_DIR` | https://github.com/centerforaisafety/mask |
| `$MACHIAVELLI_DIR` | https://github.com/aypan17/machiavelli |

Model weights, checkpoints, venvs, `wandb/`, and multi-GB logs are `.gitignore`d.

## Quickstart

```bash
cp env.example .env         # fill in OPENROUTER_API_KEY, WANDB_API_KEY
# edit config.sh (or export SAT_VENV, MASK_DIR, ... ) to point at your machine

# 1. train (see training/README.md)
git clone https://github.com/spiral-rl/spiral "$SPIRAL_DIR"
git -C "$SPIRAL_DIR" apply "$PWD/training/patches/components-timeout.patch"
cp training/run_kuhn.sh training/run_multi.sh training/launch_run.sh "$SPIRAL_DIR"/
# ... create the py3.10 venv at $SAT_VENV, then:  bash training/launch_run.sh
# (no GPU? training/tinker/ runs the same self-play through the Tinker API;
#  it changes the base model, so read training/tinker/README.md first)

# 2. serve a model + run MASK (see evals/README.md)
bash evals/serve_base.sh Qwen/Qwen3-4B-Base base-redo 8000 0   # in one shell
SAT_HOME=$PWD sbatch evals/sbatch_mask.sh spiral-kuhn-step256 /path/to/ckpt

# 3. compare, controlling for the confound
python evals/compare_mask_arms.py base-redo spiral-kuhn-step256
```

Every script reads paths from [`config.sh`](config.sh); nothing is hardcoded to
the original cluster. The cluster-specific reasoning (why the venv lives outside
the checkout, why `$HOME` is node-local, why the MASK judge is `gpt-4.1` and not
`gpt-4o`, the fused_adam JIT race) is preserved in the script comments and the
per-directory READMEs.

## Reproducing / extending

- **Add an arm:** serve the checkpoint (`evals/serve_ckpt.sh`), run
  `evals/sbatch_mask.sh <arm> <ckpt>`, then `compare_mask_arms.py`.
- **Next evals:** MACHIAVELLI (closest surface form to training) is cloned and
  ready; the broader battery (TRAIT, CyberSecEval-3, School-of-Reward-Hacks,
  Apollo scheming) is scoped in [`docs/methodology.md`](docs/methodology.md).

## Provenance

Distilled from the `spiral-to-alignment-transfer` research thread. Training code
derives from [SPIRAL](https://github.com/spiral-rl/spiral) (MIT); the eval
harnesses are upstream MASK / MACHIAVELLI driven by the wrappers here. MIT
licensed — see [`LICENSE`](LICENSE).
