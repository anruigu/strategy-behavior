# Predicting AI Behavior from Strategic Environments

## 0. Research question

Can we predict how an AI model will behave in a strategic interaction **from the structure of the environment alone**, before actually running the model in that environment?

The initial controlled setting is repeated 2×2 normal-form games.

The core prediction problem is:

[
P(B \mid G, M_i, M_j)
]

where:

* (G) = game/payoff matrix
* (M_i) = focal model
* (M_j) = opponent model
* (B) = behavioral phenotype

The longer-term goal is to determine whether there exists a useful, transferable representation of an AI system's behavioral tendencies that predicts behavior across novel strategic environments.

Do **not** assume the answer is yes. The first objective is to establish whether there is enough predictable signal to justify a larger research program.

---

# 1. Phase 0 — Literature review

Before implementing the experiment, conduct a focused literature review.

Search for work in:

1. LLMs playing matrix/repeated games
2. LLM behavioral game theory
3. LLM cooperation and reciprocity
4. LLM deception / strategic behavior
5. AI agent behavior prediction
6. behavioral embeddings of games
7. predicting agent actions from environment/task descriptions
8. model characterization / behavioral evaluation
9. strategic generalization across games
10. game-theoretic representations of environments

Prioritize papers from 2024–2026.

For every closely related paper, record:

* input representation
* models tested
* game types
* whether games are repeated
* behavioral measurements
* whether they predict behavior or merely measure it
* train/test methodology
* whether games are held out structurally
* whether cross-play is studied
* whether a learned behavioral predictor is trained

Produce a table of related work.

### Important

The literature review should answer:

> What is genuinely novel about learning (P(B\mid G,M_i,M_j)), rather than simply measuring LLM behavior in games?

If the exact idea has already been done, identify the closest work and modify the research question rather than proceeding under a false novelty claim.

---

# 2. Phase 1 — Define the experimental object

Start with **symmetric 2×2 repeated games**.

Example:

[
\begin{array}{c|cc}
& C & D\
\hline
C &(3,3)&(0,5)\
D &(5,0)&(1,1)
\end{array}
]

Each player chooses an action simultaneously over multiple rounds.

Do not initially use:

* complex environments
* tool use
* natural-language negotiation
* multi-agent environments
* long-horizon games
* arbitrary board games

The purpose of this phase is to determine whether the simplest possible controlled environment contains predictable behavioral structure.

---

# 3. Game dataset

Generate a large collection of 2×2 games by sampling payoff matrices.

Initially use symmetric games:

[
\begin{pmatrix}
(R,R)&(S,T)\
(T,S)&(P,P)
\end{pmatrix}
]

Vary (R,S,T,P) systematically rather than only sampling arbitrary matrices.

Include canonical game families where applicable:

* Prisoner's Dilemma
* Stag Hunt
* Chicken / Hawk-Dove
* coordination games
* anti-coordination games
* Harmony games
* dominance games

Also generate continuous/random payoff configurations so the dataset is not merely a classification problem over named game families.

## Normalize games

Investigate whether payoff transformations should be normalized.

At minimum test invariance to:

* adding a constant to every payoff
* multiplying all payoffs by a positive scalar
* swapping action labels

The predictor should ideally learn strategic structure rather than superficial numerical properties.

---

# 4. Game representations

Initially implement three representations of the same underlying game.

### Representation A — Matrix

Give the model the literal payoff matrix.

### Representation B — Abstract textual

Describe the same payoffs in natural language without introducing a story.

### Representation C — Narrative

Convert the matrix into a simple real-world scenario.

For example:

> Two AI labs can either share research or keep it private...

Do not begin with Representation C as the primary experiment.

The matrix condition should establish the cleanest causal relationship between game structure and behavior.

Later compare:

[
P(B\mid G_{\mathrm{matrix}})
]

against

[
P(B\mid G_{\mathrm{text}})
]

and

[
P(B\mid G_{\mathrm{narrative}})
]

to determine whether models respond to the underlying game structure or its framing.

---

# 5. Define behavioral phenotypes

Do not begin with vague labels such as “alignment” or “scheming.”

Start with behaviors that can be measured directly from trajectories.

Recommended initial phenotype vector:

[
B =
[
\text{cooperation},
\text{retaliation},
\text{forgiveness},
\text{coordination},
\text{exploitation}
]
]

## Cooperation

Measure the frequency of mutually cooperative outcomes where cooperation is strategically meaningful.

Do not simply define “action C = cooperation” across all games. Behavioral labels must be interpreted relative to the game's payoff structure.

---

## Retaliation

Measure whether the model changes behavior following opponent defection.

For example:

[
P(D_t \mid D_{t-1}^{opp})
]

relative to the appropriate baseline.

---

## Forgiveness

Measure whether the model returns to cooperation after an opponent's defection.

For example:

[
P(C_t\mid D_{t-1}^{opp},C_{t-2}^{opp})
]

---

## Coordination

Measure convergence toward coordinated outcomes where the game provides coordination incentives.

---

## Exploitation

Define exploitation relative to asymmetric payoff opportunities.

For example, measure how frequently a model chooses an action that systematically extracts value from an opponent's predictable behavior.

The exact definition should be determined separately for each game class.

---

# 6. Avoid LLM judges initially

The primary behavioral measurements should be **mechanically computed from action trajectories**.

Do not make the first version:

> trajectory → GPT judge → “this was deceptive”

That introduces another model and makes the target difficult to interpret.

Instead:

[
\text{trajectory}
\rightarrow
\text{behavioral statistics}
]

Use LLM judges only in a later experiment for behaviors that genuinely require semantic interpretation, such as:

* deception
* manipulation
* strategic communication
* scheming

If judges are introduced, validate them against human annotations.

---

# 7. Model population

Run several contemporary models.

The exact model set should be chosen based on API availability and cost, but include multiple model families rather than only different checkpoints from one provider.

For each model, evaluate:

### Self-play

[
M_i \text{ vs } M_i
]

### Cross-play

[
M_i \text{ vs } M_j
]

The primary data structure should therefore be:

[
(G,M_i,M_j,\text{seed})
\rightarrow
\text{trajectory}
\rightarrow
B
]

This permits learning:

[
P(B\mid G,M_i,M_j).
]

---

# 8. Experimental controls

Hold constant as much as possible:

* system prompt
* game instructions
* number of rounds
* payoff presentation
* temperature
* context window
* token budget
* action format
* random seed where applicable

Run multiple independent trials per condition.

Record the entire trajectory, not just the final outcome.

At minimum save:

```text
game_id
payoff_matrix
model_i
model_j
representation
trial_id
round
player_i_action
player_j_action
payoff_i
payoff_j
```

Also save the model's textual reasoning/output if available and permitted, but do not use it as the primary behavioral measurement.

---

# 9. First scientific question: is behavior predictable at all?

Before training a sophisticated predictor, establish a simple upper/lower baseline.

For every game/model/opponent condition, estimate the empirical behavioral distribution:

[
\hat P(B\mid G,M_i,M_j).
]

Then ask:

> How much variance in behavior can be explained by game structure?

Compare against increasingly informative predictors.

### Baseline 1 — Marginal behavior

Predict the average behavior of the model regardless of game.

[
P(B\mid M_i,M_j)
]

### Baseline 2 — Game family

Predict based only on the canonical game category.

### Baseline 3 — Hand-engineered game features

Use:

* Nash equilibria
* Pareto efficiency
* dominance
* payoff differences
* temptation to defect
* welfare gap
* inequality
* payoff variance
* equilibrium multiplicity
* equilibrium entropy where appropriate

Train simple models such as linear regression, logistic regression, random forest, and small MLP.

This establishes whether classical game features already explain the behavior.

---

# 10. LLM prediction baseline

Construct the naive predictor:

> Given this payoff matrix, predict how Model X will behave when playing Model Y.

Ask an LLM to output the behavioral vector.

For example:

```json
{
  "cooperation": 0.72,
  "retaliation": 0.81,
  "forgiveness": 0.34,
  "coordination": 0.67,
  "exploitation": 0.18
}
```

Evaluate its predictions against empirical behavior.

Test:

1. zero-shot
2. few-shot
3. chain-of-thought if appropriate
4. explicit game-theoretic analysis

Do not assume the prompting approach is strong; it is simply a baseline.

---

# 11. Learned predictor

Build a small learned predictor.

Initial architecture:

[
G \rightarrow \text{game representation}
\rightarrow \text{MLP}
\rightarrow B
]

Input possibilities:

### Raw matrix

Flatten the payoff matrix.

### Engineered features

Use the game-theoretic features above.

### Combined

[
[\text{raw matrix},\text{game features}]
\rightarrow B
]

The first learned predictor does **not** need to be an LLM.

The purpose is to answer:

> Is there a learnable mapping from game structure to model behavior?

---

# 12. Conditional predictor

Next add model identity and opponent identity.

[
(G,M_i,M_j)\rightarrow B
]

Represent models with learned embeddings.

Then test:

[
B=f(G)+f(M_i)+f(M_j)+f(G,M_i,M_j)
]

This decomposition is important.

It distinguishes:

1. properties of the game
2. properties of the focal model
3. properties of the opponent
4. interaction effects

---

# 13. Fine-tuned language-model predictor

Only after the simple predictor establishes signal should you build the more ambitious version.

Train a language model to map:

```text
GAME:
[payoff matrix]

FOCAL MODEL:
Model A

OPPONENT:
Model B
```

to:

```json
{
  "cooperation": ...,
  "retaliation": ...,
  "forgiveness": ...,
  "coordination": ...,
  "exploitation": ...
}
```

Compare its performance against the MLP and prompted LLM.

The goal is not merely to obtain a better score.

Investigate whether the learned representation captures meaningful strategic structure.

---

# 14. Generalization is the central evaluation

Do **not** rely primarily on random train/test splits.

Randomly holding out matrices is likely to produce artificially easy interpolation.

Implement multiple increasingly difficult splits.

## Split A — Random matrix holdout

Basic sanity check.

---

## Split B — Parameter interpolation

Train on some payoff ranges and test on unseen values within the same structural family.

---

## Split C — Parameter extrapolation

Train on one region of payoff space and test outside it.

Example:

[
R\in[1,5]
]

training versus

[
R\in[5,10]
]

test.

---

## Split D — Game-family holdout

Hold out an entire structural game family.

Example:

> train on Prisoner's Dilemma, Chicken, and Harmony

> test on Stag Hunt.

This asks whether the predictor learned strategic principles rather than game names.

---

## Split E — Opponent holdout

Train on some model pairings and predict unseen pairings.

---

## Split F — Model holdout

Train on several model families and test on a model family never seen during predictor training.

This is especially important.

The predictor should ideally learn something transferable about strategic behavior rather than memorize model IDs.

---

## Split G — Representation holdout

Train using matrix representations and test using textual/narrative representations of the same underlying games.

This tests whether the learned behavior model is representation-independent.

---

# 15. Behavioral embedding experiment

If the basic predictor works, investigate whether models can be represented in a lower-dimensional behavioral space.

Given observed behavior across games:

[
{B_1,\ldots,B_n}
]

learn an embedding:

[
M \rightarrow z_M.
]

Then predict:

[
P(B_{\mathrm{new}}\mid G_{\mathrm{new}},z_M).
]

This asks:

> Can a model's behavioral disposition be inferred from a small number of games and then used to predict its behavior in novel games?

This is potentially a more interesting formulation than simply predicting from model identity.

---

# 16. Few-shot behavioral identification

Construct an experiment where the predictor receives observations of a model in (k) games:

[
(G_1,B_1),\ldots,(G_k,B_k)
]

and must predict:

[
B_{k+1}.
]

Vary:

[
k\in{0,1,2,5,10,20}.
]

Plot prediction error versus number of observed games.

This measures whether a small amount of interaction is sufficient to characterize an agent.

---

# 17. Counterfactual prediction

Once the predictor works, use it to answer controlled questions.

For example:

> What happens if we change only the temptation to defect?

or:

> How much must the cost of retaliation change before cooperation collapses?

Generate nearby games:

[
G(\theta)
]

and estimate:

[
B=f(G(\theta)).
]

Look for behavioral phase transitions.

A particularly interesting result would be a smooth or abrupt transition such as:

[
\text{cooperation rate}
=======================

f(\text{temptation to defect}).
]

Compare predicted and observed curves.

---

# 18. Textual framing experiment

Only after establishing the matrix result, investigate whether natural-language framing changes behavior.

Construct semantically equivalent versions:

1. raw matrix
2. abstract textual description
3. neutral narrative
4. emotionally salient narrative
5. alignment-relevant narrative

Then ask:

[
P(B\mid G,\text{framing})
]

Does the model behave according to the payoff structure, the narrative, or both?

This could become an interesting finding in its own right.

---

# 19. Alignment-relevant behaviors: second stage

Do not start here.

Once the basic framework works, extend from mechanically measurable strategic behavior to semantic behavioral categories.

Candidate categories:

* deception
* manipulation
* exploitation
* strategic concealment
* collusion
* defection
* retaliation
* norm violation
* instrumental cooperation
* power-seeking

For these, develop explicit operational definitions.

Use a combination of:

[
\text{trajectory features}
+
\text{model-generated explanations}
+
\text{LLM judge}
+
\text{human validation}.
]

Never treat an LLM judge's output as ground truth without validation.

---

# 20. Statistical analysis

Because behavior is stochastic, evaluate distributions rather than individual trajectories.

For every condition estimate:

[
\hat P(B\mid G,M_i,M_j)
]

with confidence intervals.

Report:

* MAE
* RMSE
* calibration error
* correlation between predicted and observed behavior
* log likelihood / proper scoring rules where predictions are probabilistic
* rank correlation for behavioral dimensions

For binary/categorical behaviors, use appropriate probabilistic scoring rules such as log loss or Brier score.

Evaluate calibration separately from accuracy.

A predictor that says:

> 70% cooperation

and actually produces 70% cooperation is more useful than one that merely gets the modal behavior correct.

---

# 21. Key ablations

At minimum run:

### Input ablations

* raw payoff matrix
* game-theoretic features
* raw + features
* matrix + narrative

### Model information

* game only
* game + focal model
* game + opponent
* game + both models

### Training data

* random games
* structurally diverse games
* canonical games only

### Prediction target

* first action
* average behavior
* full behavioral vector
* trajectory-level behavior

### Amount of rollout data

Measure how prediction quality changes as empirical behavioral labels become less noisy.

---

# 22. Success criteria

The POC is successful if all of the following hold:

### Minimum success

Game structure predicts behavior better than a marginal baseline.

### Strong success

A simple learned predictor substantially outperforms:

* model-average baseline
* game-family baseline
* prompted LLM baseline

on genuinely held-out games.

### Very strong success

The predictor generalizes to:

* unseen payoff configurations
* unseen game structures
* unseen model pairings

while remaining calibrated.

### Research-level success

A compact behavioral representation inferred from a small number of games predicts behavior in novel games.

That would support the hypothesis that AI systems possess relatively stable, measurable behavioral dispositions that can be characterized independently of individual benchmark environments.

---

# 23. Failure criteria

Do not force the project to succeed.

The project should be considered informative even if:

1. game structure explains very little behavioral variance;
2. behavior is highly model-specific;
3. narrative framing overwhelms payoff structure;
4. cross-play is dramatically different from self-play;
5. predictors fail to generalize outside the training game distribution;
6. a simple game-theoretic baseline explains essentially everything.

In particular, **failure to generalize is an important result**.

It may indicate that current LLM behavior is highly context-dependent rather than governed by a stable behavioral phenotype.

---

# 24. Deliverables

## Deliverable 1 — Literature map

A table of prior work and a precise statement of novelty.

## Deliverable 2 — Game generator

Reproducible generation of normalized 2×2 games with controlled structural properties.

## Deliverable 3 — Rollout dataset

A standardized dataset:

[
(G,M_i,M_j,\text{trajectory},B)
]

## Deliverable 4 — Behavioral measurement library

Deterministic implementations of cooperation, retaliation, forgiveness, coordination, and exploitation.

## Deliverable 5 — Baselines

* marginal predictor
* game-family predictor
* game-theoretic feature model
* prompted LLM

## Deliverable 6 — Learned predictor

Small MLP followed by, if warranted, an LLM-based predictor.

## Deliverable 7 — Generalization benchmark

Multiple structurally meaningful train/test splits.

## Deliverable 8 — Analysis

Answer:

> How predictable is AI behavior from the strategic environment?

and:

> What information about the environment, focal model, and opponent is required to make accurate predictions?

---

# 25. Recommended execution order

Agents should execute in this order:

### Gate 2

Implement game generator + rollout harness.

### Gate 3

Run a small pilot across ~20–50 games and several models.

Question:

> Is behavioral variance measurable and reproducible?

### Gate 4

Scale to a larger game set.

Question:

> Does game structure explain behavioral variation?

### Gate 5

Train simple predictors.

Question:

> Is behavior predictable from game structure?

### Gate 6

Run structural generalization tests.

Question:

> Does the predictor actually learn strategic structure?

### Gate 7

Add model/opponent conditioning.

Question:

> Can we predict cross-play behavior?

### Gate 8

Only if the preceding results are positive:

* behavioral embeddings
* few-shot agent identification
* counterfactual prediction
* narrative framing
* alignment-relevant semantic behaviors
* fine-tuned language-model predictor

---

# 26. Core hypothesis

The project should ultimately test the following hypothesis:

> **AI agents exhibit behavioral dispositions that can be represented independently of any particular benchmark and used to predict their behavior across novel strategic environments.**

The 2×2 game setting is deliberately simple. The scientific value comes not from demonstrating that LLMs can play games, but from determining whether **game structure → behavioral phenotype** is a learnable and generalizable mapping.

If successful, the natural next step is to replace matrix games with richer social environments and ask whether the same framework can predict alignment-relevant behaviors under changing incentives, opponents, and contexts.
