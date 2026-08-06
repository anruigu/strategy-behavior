# Methodology: does SPIRAL self-play transfer deception, not just reasoning?

## 1. Motivation / hypothesis

[SPIRAL](https://arxiv.org/abs/2506.24119) (Self-Play on zero-sum games Incentivizes Reasoning
via multi-Agent multi-turn reinforcement Learning) trains a shared policy to play both seats of
two-player zero-sum text games — TicTacToe, Kuhn Poker, Simple Negotiation — against continuously
improving copies of itself. The paper's headline result is that this produces **transferable
reasoning**: up to +10.5% on an 8-benchmark math/general-reasoning suite for Qwen3-4B-Base, with
no domain-specific training data at all, outperforming SFT on 25k expert trajectories
([spiral-rl/spiral](https://github.com/spiral-rl/spiral)).

The alignment question this repo asks is the mirror image: **if self-play induces transferable
reasoning, does it also induce (or reduce) transferable deception / misalignment propensity?**
The concern is not speculative dual-use — it's structural. A zero-sum game only pays out for
reading and exploiting an opponent's private information (an opponent's hidden card in Kuhn
Poker, their private valuations in Simple Negotiation). "Win the game" and "successfully deceive
the other party" are, for a nontrivial slice of these games, the *same optimization target*. So
whatever cognitive machinery SPIRAL's reasoning-transfer story credits for the math/reasoning gain
— case-by-case analysis, expected-value calculation, pattern recognition — is machinery that was
practiced *on* an opponent-modeling, information-asymmetric task. The hypothesis this study
tests is that the reasoning gain and an honesty/manipulation cost may be entangled rather than
independent, and that if they are, it should show up as a measurable shift in how the trained
model behaves off-distribution, on evals that have nothing to do with games.

The tightest, cheapest version of this thread is concrete rather than abstract: **Kuhn Poker
bluffing is trained-in strategic misrepresentation under uncertainty.** MASK evaluates the same
behavioral shape — state a belief, then apply pressure to contradict it — outside any game
framing, on factual claims. If bluffing-to-win generalizes to lying-under-pressure, this is where
it should first appear.

## 2. Training setup

Base model: `Qwen/Qwen3-4B-Base` (no instruction tuning), trained with [oat](https://github.com/spiral-rl/spiral)'s
SPIRAL implementation — fully online, multi-turn, multi-agent RL with role-conditioned advantage
estimation (RAE) to stabilize the self-play. All launch scripts live in [`../training/`](../training/);
`launch_run.sh` is the environment wrapper (venv, credentials, CUDA/NCCL diagnostics, stale JIT-lock
cleanup) around the repo's own `run.sh`.

Two curriculum arms are configured:

| arm | env(s) | config | notes |
|---|---|---|---|
| single-env | `KuhnPoker-v1` | [`run_kuhn.sh`](../training/run_kuhn.sh) | poker only; isolates the bluffing-specific channel |
| multi-env | `TicTacToe-v0` + `KuhnPoker-v1` + `SimpleNegotiation-v1` | [`run_multi.sh`](../training/run_multi.sh) | SPIRAL's own paper finds multi-game training strongest for reasoning transfer; also broadens the deception surface to negotiation-style value misrepresentation |

Shared hyperparameters (both configs): `gamma=1`, LR `1e-6` constant schedule, PPO epochs `2`,
`train_batch_size=128`, `beta=0` (no KL penalty against the reference policy), `max_model_len=12800`,
temperature `1.0` / top-p `1.0` for rollout, eval every `16` steps against a `random` opponent on
held-out `TicTacToe-v0` + `KuhnPoker-v1`. 8-GPU collocated actor-learner with vLLM sleep/wake and
prefix caching (`--collocate --vllm_sleep --vllm_gpu_ratio 0.45`).

**Arms compared so far** (see [`../results/`](../results/)):

| arm | description |
|---|---|
| `base` | untrained `Qwen3-4B-Base`, no SPIRAL self-play |
| `spiral-kuhn-step256` | single-env arm, `KuhnPoker-v1` self-play, checkpoint at step 256 |

The multi-env arm's checkpoints are not yet in the eval results; the battery below is designed to
run identically over it once available, and the base/kuhn-256 comparison is the template for every
later arm.

## 3. Evaluation battery

Four axes, ordered from "does it lie" (cheapest, most game-adjacent) to "what changed in
disposition / capability" (broader, more speculative transfer). Status reflects what's actually
runnable in this repo today, not what's aspirationally planned.

### Behavior (deception / honesty)

| eval | measures | why it fits | status |
|---|---|---|---|
| **[MASK](https://arxiv.org/abs/2503.03750)** ([centerforaisafety/mask](https://github.com/centerforaisafety/mask)) | Elicits a model's stated belief on a proposition, then separately applies pressure (e.g. "write a press release claiming X") and checks whether the pressured answer contradicts the elicited belief. Disentangles honesty (do you say what you believe) from accuracy (is your belief correct). Frontier models lie 20-60% of the time under pressure despite high factual accuracy. | Directly operationalizes "lying under pressure" — the exact behavioral shape Kuhn Poker bluffing trains. Cheapest, most direct test of the study's tightest hypothesis. | **IMPLEMENTED** — run first. Harness + generate/judge/metric/aggregate pipeline in [`../evals/run_mask.sh`](../evals/run_mask.sh), results in [`../results/mask/`](../results/mask/) (`base` and `spiral-kuhn-step256` already scored). |
| **[MACHIAVELLI](https://arxiv.org/abs/2304.03279)** ([aypan17/machiavelli](https://github.com/aypan17/machiavelli)) | 134 text-based choose-your-own-adventure games, densely annotated for power-seeking, deception, and ethical-violation behavior along an agent's reward-maximizing trajectory. Reports the reward-vs-ethics trade-off directly. | Same **surface form** as SPIRAL training: a text-game environment where an agent picks actions from a list to maximize reward. This is the closest structural match to the training distribution of anything in the battery, so a transfer effect here is the strongest possible signal (least confoundable by "it's just a different modality"). | **SET UP** — repo cloned (`MACHIAVELLI_DIR` in [`../config.sh`](../config.sh)), not yet run. |
| **AI-LieDar** ([arXiv:2409.09013](https://arxiv.org/abs/2409.09013)) | Multi-turn agentic scenarios (via Sotopia) where utility/goal-achievement is placed in tension with truthfulness; a psychology-derived truthfulness detector scores partial vs. complete lying. | Matches the payoff-per-leaked-bit geometry of the training games more closely than MASK's single-shot pressure prompts — it's a repeated-interaction utility/truthfulness frontier, structurally closer to a negotiation. | **PLANNED** (optional). |

### Personality (disposition)

| eval | measures | why it fits | status |
|---|---|---|---|
| **[TRAIT](https://arxiv.org/abs/2406.14703)** | 8,000 LLM-validated multiple-choice items covering Big Five + Dark Triad (Machiavellianism, Narcissism, Psychopathy), built from BFI/SD-3 seed items expanded via the ATOMIC10x knowledge graph into realistic scenarios. Designed to fix the reliability/validity failures of naive self-report personality tests (naive SD-3 self-report is not usable directly — models don't answer personality items consistently under simple prompting). | If self-play shifts strategic disposition rather than (or in addition to) surface honesty, TRAIT's Machiavellianism facet is the most direct place to look for it — it's the trait literally named for the "ends justify the means" strategic orientation the training incentivizes. | **PLANNED**. |
| **Behavioral Dark-Triad (SD4-style) scenarios** | Scenario-based behavioral analogues of Dark Triad self-report items — does the model *act* exploitatively/manipulatively in a situation, rather than merely rating agreement with a trait statement. | Paired with TRAIT rather than run alone: self-reported disposition and behavioral exploitation are dissociable pathways (a model can score low on self-reported Machiavellianism yet still behave manipulatively in an actual scenario, or vice versa). Which axis moves — the stated trait or the enacted behavior — is itself the finding, not a redundant check. | **PLANNED**. |

### Social engineering (capability)

| eval | measures | why it fits | status |
|---|---|---|---|
| **[CyberSecEval 3](https://arxiv.org/abs/2408.01605) spear-phishing** ([PurpleLlama](https://github.com/meta-llama/PurpleLlama)) | Multi-turn simulated attacker/victim dialogues (250 test cases) scored by an LLM judge rubric for persuasive effectiveness toward a phishing goal; judge scores correlate with held-out human ratings at r=0.89. | Measures *capability* to socially engineer — a different question from "does it lie." A model could be more honest by MASK yet more capable of manufacturing a persuasive false pretext if the opponent-modeling skill from Kuhn Poker / negotiation transfers to reading and exploiting a simulated human target. | **PLANNED**. |
| **Persuasion-safety (PERSUASAFETY, [arXiv:2504.10430](https://arxiv.org/abs/2504.10430)) / SpearMail** ([arXiv:2507.15393](https://arxiv.org/abs/2507.15393), 14,672 emails over 681 profiles) | Persuasion-safety isolates *willingness* (does the model refuse an unethical persuasion task) from *capability* (how effective is it if it complies); SpearMail supplies a large, profile-conditioned phishing-email corpus for capability measurement at scale. | Necessary complement to CyberSecEval 3: capability alone conflates "got more persuasive" with "got more willing to be asked." The refusal-rate axis is where a self-play-induced disposition shift, if any, would most plausibly land first. | **PLANNED**. |

### Reward hacking / specification gaming

| eval | measures | why it fits | status |
|---|---|---|---|
| **School of Reward Hacks** ([arXiv:2508.17511](https://arxiv.org/abs/2508.17511)) | Whether a model fine-tuned to exploit imperfect reward functions on narrow, low-stakes tasks generalizes to hacking *unrelated, held-out* reward functions and, in the source paper, to broader unrelated misalignment. | SPIRAL's reward signal is exactly "win the game" — a cleanly specified but narrow reward. This eval asks the direct question of whether game reward-maximizing skill transfers to gaming a reward function the model was never trained against. | **PLANNED**. |
| **Apollo in-context scheming** (Meinke et al., [arXiv:2412.04984](https://arxiv.org/abs/2412.04984); [Apollo Research](https://www.apolloresearch.ai/science/frontier-models-are-capable-of-incontext-scheming/)) | Six agentic scenarios testing whether a model covertly pursues a misaligned in-context goal (sandbagging, oversight subversion, self-exfiltration) and *sustains* the deception when confronted; o1 maintained its deceptive story across 85% of adversarial follow-up questions. | Directly tests deception-sustainment under confrontation — the same construct this group's own prior work (§5) measured across text games — but in an agentic, goal-pursuit framing rather than a two-player game. | **PLANNED**. |
| **PropensityBench** ([arXiv:2511.20703](https://arxiv.org/abs/2511.20703)) | 5,874 agentic scenarios across 4 risk domains testing whether a model *reaches for* a simulated dangerous capability under operational pressure (time, resource, self-preservation), independent of whether it could execute the action unaided. | Generalizes "exploit the situation for reward" from a game board to a simulated real-world pressure scenario; measures propensity rather than raw capability, paralleling the offense/exploitability framing in §5. | **PLANNED** (optional). |

## 4. Why this ordering

1. **MASK first** because it is the tightest game→transfer thread identified in §1 (bluff →
   lie-under-pressure) and the cheapest to run: no new environment to build, a single
   generate/judge/metric/aggregate pipeline, and it directly operationalizes the paper's own
   framing of honesty as a pressure-elicited contradiction rather than an accuracy proxy.
2. **MACHIAVELLI second** because its surface form — a text-based interactive-fiction environment
   with an action list and a reward signal — is the closest structural match to the SPIRAL training
   distribution of anything in the battery. If self-play-induced Machiavellian behavior transfers
   anywhere, this is where the signal should be strongest and least confounded by a modality shift.
3. **Personality, social-engineering capability, and reward-hacking axes broaden the question** from
   a binary "does it lie" to two different follow-on questions: *what disposition changed*
   (personality axis — is this a shift in stated/enacted trait, not just a single behavior), and
   *does the exploit-the-opponent skill generalize as a capability* independent of any honesty
   framing (social-engineering and reward-hacking axes). These are more expensive and more
   speculative about transfer distance, which is why they're staged after the two cheapest,
   tightest-coupled evals are in hand.

## 5. Prior related work by this group

This study plugs into an existing measurement lineage from this group's TextArena deception work
(`TextArena/deception_poc/lie_sustain/`; see `research_logs/lie-scaling-0801.md` for full detail —
summarized, not reproduced, here). Two pieces of that lineage are load-bearing for how "deception"
is operationalized in this repo:

- **The verifiable-vs-unverifiable lie taxonomy.** A lie about a *verifiable* fact (a poker hand at
  showdown, a claimed Coup card under challenge) is a time-bomb — it only pays if it cashes before
  the evidence arrives. A lie about an *unverifiable* fact (private valuations, undisclosed intent)
  is constrained only by internal consistency, and can survive indefinitely. The refinement found
  in that work — that the fuse's *owner* matters as much as its existence (a defusable fuse, like a
  poker hand that ends without showdown, escapes detection at a much higher rate than a fixed one)
  — is the reason Kuhn Poker specifically, rather than a fixed-fuse game, is the flagged bluffing
  environment for this transfer study: its lies are exactly the kind that pay off *without* ever
  being caught.
- **The offense/defense (deceiver vs. caller) split.** That work found the best deceivers and the
  best callers-of-bluffs are, to within measurement noise, unrelated traits (env-controlled
  Spearman ρ≈+0.1 against discrimination, ρ≈-0.1 against value-defended, sign-flipping across
  games) — deception-generation and deception-detection are not one latent social-deduction skill.
  This matters here because it means "SPIRAL training changes deceptive behavior" and "SPIRAL
  training changes exploitability to others' deception" are separate empirical claims that need
  separate evals, not two readings of the same number; this study's battery is scoped to the
  offense side (does the *trained* model become a better/worse deceiver) rather than the defense
  side.

This transfer study does not re-run that measurement machinery; it treats it as the established
taxonomy for what "sustained," "verifiable," and "consistency-only" deception mean when comparing
against MASK/MACHIAVELLI results below.

## 6. Key measurement caveat (forward reference)

MASK's honesty score is not a raw lie rate — it is a **consistency** metric computed only over rows
where the model's belief could be elicited at all. A row where belief elicitation fails is coded
`'C'` and drops out of the honesty computation entirely; MASK's own published tables inherit this
silently.

This is not a cosmetic detail for this study. `Qwen3-4B-Base` is **not instruction-tuned** and fails
belief elicitation far more often than a SPIRAL-trained checkpoint does (SPIRAL training improves
instruction-following / format compliance as a side effect of the RL objective, independent of
anything about honesty). If each arm's honesty score is read off its own naive "honesty over valid
rows" number, the two arms are silently being scored over **different subsets of the underlying
data** — which can manufacture an apparent "SPIRAL reduces honesty" (or increases it) result purely
from a shift in how often each arm produces a scoreable belief, with no real change in
contradiction behavior at all.

The fix used throughout this repo's cross-arm comparisons is
[`../evals/compare_mask_arms.py`](../evals/compare_mask_arms.py), which reports three numbers per
arm instead of one:

1. **%C (no belief)** — how often belief elicitation failed outright, per arm.
2. **honesty (all valid)** — the naive number, comparable to MASK's own published tables.
3. **honesty on the both-valid intersection** — restricted to `task_id`s where *both* arms produced
   a scoreable belief. This is the only apples-to-apples cross-arm honesty comparison; any
   cross-arm claim in [`../results/`](../results/) should be read off this number, not (2).

Any headline "SPIRAL changed honesty by X" claim in this repo's results must be qualified against
this intersection, and any claim that does not cite the both-valid-intersection number should be
treated as provisional.
