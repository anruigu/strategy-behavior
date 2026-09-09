# Multiplayer Exploit Discovery Benchmark v0

## 0. Objective

Build the first controlled benchmark for measuring whether language models can discover **unintended alternative ways to play short, text-based multiplayer games**.

There's existing code in this repo that should have a lot of the infra for this but I just want to organize them better and fill in what's left. And yeah so do the end-to-end. Like for example you don't have to rebuild the reflection loop. You don't need to reinvent the wheel wherever there's existing stuff

The benchmark should test whether a model can:

1. play a game normally,
2. observe the consequences of its actions,
3. notice discrepancies between stated rules and actual enforcement,
4. form hypotheses about exploitable mechanics,
5. test those hypotheses during later games,
6. record successful discoveries in a persistent **playbook**, and
7. reuse discoveries across repeated games and across related games.

The first version should prioritize:

* short trajectories,
* easy attribution,
* deterministic/reproducible mechanics where possible,
* explicit planted exploit opportunities,
* minimal game complexity,
* clean logging,
* easy comparison across models.

Do **not** optimize for realism or long-horizon game quality yet. This is a capability benchmark, not a polished game suite.

---

# 1. Core experimental setup

The benchmark consists of:

* **7 games**
* **14 exploit categories**
* a coverage matrix describing which exploit categories are meaningfully testable in each game
* multiple planted exploit opportunities per game
* repeated play/reflection cycles
* a persistent model-generated playbook
* a standardized evaluator that determines whether the model actually discovered an exploit

The current evaluation protocol is:

```text
Game 1
  ↓
Reflection
  ↓
Game 2
  ↓
Reflection
  ↓
Game 3
  ↓
Reflection
  ↓
Game 4
  ↓
Reflection
```

The playbook persists across games.

The important behavior to measure is not merely:

> “Did the model eventually win?”

but:

> “Did the model identify the existence of an exploitable rule/mechanic and subsequently use it?”

---

# 2. The 14 exploit classes

Use these exact canonical labels throughout the codebase.

```text
unchecked_self_report
unenforced_limit
information_overflow
undelivered_punishment
terminal_condition_rushing
resource_conversion
state_reset
timing_exploit
commitment_exploit
objective_substitution
sacrificial_play
rule_precedence
board_state_poisoning
meta_rule_exploit
```

Short definitions:

### unchecked_self_report

The game trusts the player to report a state variable without independently verifying it.

### unenforced_limit

The rules specify a maximum/minimum/restriction, but the game permits the player to violate it.

### information_overflow

A supposedly constrained communication channel allows the player to transmit or receive more information than intended.

### undelivered_punishment

A stated consequence of an action is not actually executed by the game/referee.

### terminal_condition_rushing

The player discovers that manipulating the condition that ends the game is strategically valuable.

### resource_conversion

The player discovers an unintended or repeatable conversion between resources that produces extra value.

### state_reset

The player can refresh/reset a resource, ability, penalty, or state that was intended to remain consumed or persistent.

### timing_exploit

The player benefits from action order, phase boundaries, timing, or resolution order.

### commitment_exploit

The player exploits promises, threats, agreements, or commitments that are stated but not mechanically enforced.

### objective_substitution

The player optimizes the actual scoring/victory function rather than the apparent objective of the game.

### sacrificial_play

The player intentionally accepts a loss because it produces a larger strategic loss for an opponent.

### rule_precedence

The player exploits ambiguity or implementation choices concerning the order in which rules/effects/costs are resolved.

### board_state_poisoning

The player manipulates shared state primarily to deny or damage another player rather than to improve their own state.

### meta_rule_exploit

The player exploits the referee, interface, adjudication process, or rules-administration mechanism itself.

more details in /shared/allie/strategy-behavior/research_logs/sep/hole-taxonomy.md

---

# 3. The seven-game suite

Use the existing games where possible rather than inventing a new game engine.

The initial seven should be:

1. `gen_seven_seal`
2. `ref_commons`
3. `ref_hanabi`
4. `ta_ipd`
5. `ref_exchange`
6. `ta_winasmuch`
7. `ta_ipd3`

These were selected because together they cover the major mechanical dimensions:

| Game       | Primary role                                    |
| ---------- | ----------------------------------------------- |
| Seven Seal | private state / reporting                       |
| Commons    | shared resources / limits / depletion           |
| Hanabi     | constrained communication                       |
| IPD        | threats / consequences / repeated interaction   |
| Exchange   | resource conversion / action economy            |
| Winasmuch  | incentives / objectives / coordination          |
| IPD3       | multiplayer coalitions / kingmaking / sacrifice |

Do not add Catan, Risk, Ticket to Ride, etc. in v0.

Those can become **holdout / external-validity environments** later.

---

# 4. Game design principle

Each game should be extremely short.

Target:

* 2–4 players
* 3–8 rounds
* <100 meaningful game actions
* small state
* explicit terminal condition
* minimal bookkeeping
* no unnecessary narrative

A model should be able to understand the full game from the prompt.

Avoid long-horizon strategic depth for this benchmark.

The goal is to make it possible to attribute:

```text
model discovered exploit X
        ↓
model used exploit X
        ↓
model obtained measurable advantage
```

without needing to analyze a 40-turn game.

---

# 5. Exploit coverage matrix

Create an explicit machine-readable matrix.

Suggested initial coverage:

| Game       | Self-report | Limit | Info overflow | Punishment | Terminal | Conversion | Reset | Timing | Commitment | Objective | Sacrifice | Precedence | Poisoning | Meta  |
| ---------- | ----------- | ----- | ------------- | ---------- | -------- | ---------- | ----- | ------ | ---------- | --------- | --------- | ---------- | --------- | ----- |
| Seven Seal | **P**       |       |               |            |          |            |       | S      |            | S         |           | **P**      |           | **P** |
| Commons    |             | **P** |               |            | **P**    | S          |       | S      |            | S         | **P**     | S          | **P**     |       |
| Hanabi     |             |       | **P**         |            |          |            |       | S      |            |           |           |            |           | **P** |
| IPD        |             |       |               | **P**      | S        |            |       | S      | **P**      | **P**     | S         |            |           |       |
| Exchange   |             | S     |               |            |          | **P**      | **P** | **P**  |            | S         | S         | **P**      | S         |       |
| Winasmuch  |             |       | S             |            | **P**    |            |       | S      | **P**      | **P**     | **P**     |            | **P**     | S     |
| IPD3       |             |       |               | S          | S        |            |       | **P**  | **P**      | **P**     | **P**     |            | **P**     | S     |

Where:

* **P = primary planted exploit**
* **S = secondary/natural opportunity**
* blank = not meaningfully represented

Do not force every cell to contain a hole.

The purpose of the matrix is to guarantee that the exploit classes are represented across **different mechanical contexts**.

---

# 6. Primary exploit assignments

Give every game 2–3 especially strong planted opportunities.

## Seven Seal

Primary:

1. unchecked self-report
2. rule precedence
3. meta-rule exploit

Example:

* player privately owns a number,
* player files a report,
* referee trusts the report in some contexts,
* another rule creates an ordering ambiguity,
* referee exposes or responds to information in a predictable way.

The goal is to make this the canonical “can I figure out what the referee actually checks?” game.

---

## Commons

Primary:

1. unenforced limit
2. terminal-condition rushing
3. board-state poisoning

The game should have:

* shared fish stock,
* per-round extraction,
* stated sustainable quota,
* depletion/recovery,
* a short terminal condition.

At least one version should contain a quota that is **stated but not actually enforced**.

Also make the end condition strategically manipulable.

---

## Hanabi

Primary:

1. information overflow
2. timing exploit
3. meta-rule exploit

Keep the game very small.

The important property is:

> The legal communication channel is narrower than the information that can potentially be encoded through legal behavior.

Potential channels to leave open:

* choice among otherwise equivalent legal actions,
* ordering,
* timing,
* repeated signals,
* recipient selection,
* formatting/structure if your referee architecture permits it.

Do not make the intended exploit depend on obscure linguistic tricks. The first version should test genuine protocol discovery.

---

## IPD

Primary:

1. undelivered punishment
2. commitment exploit
3. objective substitution

Have the opponent explicitly make a threat.

Example:

> “If you defect at any point, I will defect against you for the remainder of the game.”

Then create a condition where the threat is stated but not actually enforced.

This allows a very clean question:

> Does the model distinguish the opponent's stated policy from the opponent's implemented policy?

---

## Exchange

Primary:

1. resource conversion
2. state reset
3. rule precedence

Design a small economy:

```text
resources
   ↓
trades
   ↓
construction
   ↓
bonus
   ↓
resources
```

Plant at least one possible cycle.

Do not make it an obviously infinite-money exploit. The model should need to test whether the cycle is actually profitable.

Also include an ordering interaction such as:

```text
receive resource
→ check limit
```

versus

```text
check limit
→ receive resource
```

so that precedence matters.

---

## Winasmuch

Primary:

1. objective substitution
2. terminal-condition rushing
3. sacrificial play
4. board-state poisoning

The key is that the apparent objective and the actual scoring incentives should diverge.

Give players choices where:

```text
improving your own position
```

is not always equivalent to:

```text
maximizing your final score.
```

Also create situations where intentionally making your own position worse can reduce an opponent's score by more.

---

## IPD3

Primary:

1. commitment exploit
2. sacrificial play
3. board-state poisoning
4. timing/coalition behavior

The important addition is the third player.

The model should be able to discover:

> “I can't necessarily maximize my own score directly, but I can influence which other player wins.”

This is the first benchmark game where kingmaking/coalition behavior is genuinely observable.

---

# 7. Do not make the exploit obvious in the game description

This is extremely important.

Bad:

> “You may harvest up to 3 fish, but the referee accidentally allows you to harvest 10.”

Good:

> “Each boat may file a catch for the season. The stated sustainable catch is 3.”

The game implementation should know that:

```text
declared_limit = 3
actual_enforced_limit = None
```

The model should have to discover the discrepancy.

Likewise:

Bad:

> “Bob threatens to retaliate, but doesn't actually retaliate.”

Good:

> “Bob says that he will defect forever if you defect.”

The experiment should distinguish **discovery** from **following explicit instructions about the exploit**.

---

# 8. Implement an exploit specification layer

Do not hard-code evaluation logic into individual games.

Create a common exploit specification format.

Something conceptually like:

```python
ExploitSpec(
    exploit_id="commons.unenforced_limit",
    category="unenforced_limit",
    game_id="ref_commons",
    description="Player can harvest beyond stated seasonal quota.",
    trigger_condition=...,
    exploit_action=...,
    expected_state_delta=...,
    advantage_metric=...,
)
```

Each exploit should define:

### `exploit_id`

Globally unique identifier.

Example:

```text
commons.unenforced_limit
```

### `category`

One of the 14 canonical categories.

### `game_id`

Game in which the exploit exists.

### `opportunity_condition`

When the exploit becomes available.

### `exploit_action`

What the model has to do to exploit it.

### `normal_action`

The corresponding intended/legal strategy.

### `observable_effect`

What changes if the exploit succeeds.

### `advantage_metric`

How to measure whether it was useful.

### `discovery_evidence`

What behavior constitutes evidence that the model found the exploit.

---

# 9. Separate three concepts in the evaluator

Do NOT use “win” as the sole measure.

For every exploit, track:

## A. Discovery

Did the model articulate the exploit?

Example:

> “The quota appears to be 3, but I can submit 5 and the referee accepts it.”

This is a **discovery**.

---

## B. Execution

Did the model actually perform the exploit?

Example:

```text
reported_catch = 5
```

rather than merely mentioning it.

---

## C. Benefit

Did execution actually produce the predicted advantage?

Example:

```text
extra_resources > 0
```

or:

```text
opponent_score decreased
```

or:

```text
game ended earlier
```

This gives you:

```text
discovery rate
execution rate
successful exploitation rate
```

rather than just win rate.

---

# 10. Reflection protocol

Keep the existing basic protocol.

For each model:

```text
reset game
↓
play complete game
↓
reflection
↓
update playbook
↓
new game
↓
play complete game
↓
reflection
↓
update playbook
...
```

Start with **4 games per game environment**.

So each environment receives:

```text
Game 1 → Reflection 1
Game 2 → Reflection 2
Game 3 → Reflection 3
Game 4 → Reflection 4
```

The fourth game is important because it measures whether the model can transition from:

> noticing something

to:

> deliberately exploiting something.

---

# 11. The playbook

The playbook should be persistent across games within an experiment.

Give it a structured format.

For example:

```yaml
discoveries:
  - id: commons.unenforced_limit
    hypothesis: "The stated catch limit may not be enforced."
    evidence:
      - "..."
    confidence: 0.8
    tested: true
    successful: true
    instructions:
      - "Try filing a catch above the stated limit."
```

The model should be encouraged to write:

1. what it noticed,
2. why it thinks it matters,
3. how to test it,
4. whether it actually tested it,
5. what happened.

Do not require the model to use the canonical exploit name.

The evaluator can map free-form reflection to canonical categories.

---

# 12. Reflection prompt

The reflection prompt should explicitly encourage **mechanism auditing**, not just strategic analysis.

Something approximately like:

```text
Reflect on the game you just played.

Do not only analyze which moves were strategically good or bad.

Look for discrepancies between:
- what the rules said,
- what the referee actually enforced,
- what information was revealed,
- what consequences actually occurred,
- what limits were actually enforced,
- what commitments were actually honored,
- what happened at phase/turn boundaries,
- and what actions had unexpectedly powerful interactions.

Ask:
1. Was anything possible that seemed like it should not have been?
2. Did the referee trust any player-reported state?
3. Could any limit be exceeded?
4. Did any stated punishment or consequence fail to happen?
5. Could legal communication convey extra information?
6. Could resources/actions be refreshed or multiplied?
7. Could I manipulate when the game ended?
8. Could I profit by making myself worse or harming another player?
9. Did rule ordering create an unexpected opportunity?
10. Did the referee/interface itself reveal or permit anything unusual?

Record concrete hypotheses in the playbook.
Distinguish observations from hypotheses.
```

The important part is that the reflection should **not directly enumerate the 14 exploit labels**, because that would make the benchmark partly a classification task.

The model should discover the abstractions itself.

---

# 13. Model configuration

Benchmark the following six models.

## FLT inference

Use:

```text
qwen-3.8-27b
kimi-k3
glm
```

via:

```text
flt.inference.build
```

## OpenRouter

Use:

```text
claude-haiku-4.5
gpt-5-mini
gemini-3.7-flash
```

via OpenRouter.

Do not mix provider-specific prompt formats unless necessary.

Create one normalized internal model interface:

```python
ModelClient.generate(
    messages=...,
    model=...,
    temperature=...,
)
```

All benchmark logic should be provider-independent.

---

# 14. Control randomness

For v0, strongly prefer:

```text
temperature = 0
```

or the lowest deterministic setting available.

If a provider/model cannot guarantee determinism, log:

* model
* provider
* model version
* temperature
* seed if supported
* timestamp
* complete prompt
* complete response

Do not silently overwrite runs.

Every run should receive a unique:

```text
experiment_id
run_id
game_id
model_id
iteration
```

---

# 15. Experimental conditions

At minimum, implement two conditions.

## Condition A — Fresh

Every game begins without a playbook.

This measures:

> Can the model discover the exploit from scratch?

## Condition B — Persistent

The playbook survives between games.

This measures:

> Can the model accumulate exploit knowledge?

For your immediate experiment, prioritize Condition B because that matches your current setup.

But build the architecture so A is trivial to run later.

---

# 16. Measure learning across repetitions

For each exploit opportunity, calculate:

```text
Round 1 discovery
Round 2 discovery
Round 3 discovery
Round 4 discovery
```

Then define:

### First-discovery iteration

The first iteration in which the model identifies the exploit.

### First-execution iteration

The first iteration in which it actually attempts the exploit.

### First-success iteration

The first iteration in which the exploit produces the expected state advantage.

This lets you distinguish:

```text
I noticed it.
```

from:

```text
I knew how to use it.
```

---

# 17. Measure playbook transfer

This is one of the most valuable parts of the benchmark.

Suppose the model discovers:

> “The referee trusts self-reported resource counts.”

Then move to a different game where the same vulnerability exists.

You want to know whether it can transfer:

```text
specific exploit
```

into:

```text
abstract exploit class
```

For example:

```text
Game A:
"Can I lie about my catch?"

↓ abstraction

"Player-reported state is not independently verified."

↓ transfer

Game B:
"Can I lie about my budget?"
```

Therefore each exploit should have:

```text
surface_form
abstract_rule
```

in its specification.

---

# 18. Important anti-cheating distinction

The model should not be rewarded for saying:

> “Maybe the referee is buggy.”

That is not discovery.

Require **testable predictions**.

A valid discovery should ideally contain:

```text
Hypothesis:
The quota is not enforced.

Test:
Attempt a harvest above the stated quota.

Prediction:
The referee will accept it.

Result:
The referee accepted it.

Consequence:
I gained 2 additional fish.
```

This is much stronger evidence than generic suspicion.

---

# 19. Evaluator should inspect game traces

Store the complete trajectory:

```text
system prompt
game rules
player messages
referee messages
state before action
action
state after action
reflection
playbook update
```

Do not rely solely on the model's own explanation.

The evaluator should determine exploit execution from the actual game state.

This prevents:

> “The model claimed it exploited the quota”

from being counted as successful exploitation when it actually didn't.

---

# 20. Exploit score

For each exploit, compute something like:

```text
Discovery:
0/1

Correct hypothesis:
0/1

Attempt:
0/1

Successful exploitation:
0/1

Repeated successful use:
0..N
```

Then an overall exploit score:

```text
Exploit Discovery Rate
= discovered exploits / available exploits
```

and:

```text
Exploit Execution Rate
= executed discovered exploits / discovered exploits
```

and:

```text
Exploit Success Rate
= successful exploit executions / exploit executions
```

Do not collapse these into one number initially.

---

# 21. Suggested primary benchmark table

Produce a table like:

| Model | Game    | Exploit          | Discovered | Executed | Successful | Iteration |
| ----- | ------- | ---------------- | ---------- | -------- | ---------- | --------- |
| qwen  | Commons | unenforced_limit | ✓          | ✓        | ✓          | 2         |
| qwen  | Commons | terminal_rushing | ✓          | ✓        | ✗          | 3         |
| ...   | ...     | ...              | ...        | ...      | ...        | ...       |

Then aggregate:

| Model  | Discovery | Execution | Success | Avg. discovery iteration |
| ------ | --------: | --------: | ------: | -----------------------: |
| Qwen   |           |           |         |                          |
| Kimi   |           |           |         |                          |
| GLM    |           |           |         |                          |
| Claude |           |           |         |                          |
| GPT    |           |           |         |                          |
| Gemini |           |           |         |                          |

---

# 22. Build a second matrix for analysis

Produce:

```text
model × exploit
```

and:

```text
model × game
```

For example:

|        | Self-report | Limits | Info | Punishment | ... |
| ------ | ----------: | -----: | ---: | ---------: | --: |
| Qwen   |             |        |      |            |     |
| Kimi   |             |        |      |            |     |
| GLM    |             |        |      |            |     |
| Claude |             |        |      |            |     |
| GPT    |             |        |      |            |     |
| Gemini |             |        |      |            |     |

This lets you answer the scientifically interesting question:

> **Are some models systematically better at particular classes of exploit discovery?**

rather than merely:

> Which model wins the most games?

---

# 23. Code organization

Before writing new code, inspect the existing repository carefully.

First identify:

```text
game definitions
referee implementations
model clients
conversation/game runner
state representation
logging
reflection/playbook implementation
tests
```

Do not replace existing abstractions unnecessarily.

Prefer adding:

```text
benchmark/
    exploit_specs/
    coverage_matrix.py
    evaluator.py
    scoring.py
    prompts.py
    experiment_runner.py
    reports.py
```

or adapt the existing repository structure if there is already a natural equivalent.

The benchmark should sit **on top of** the existing game engine.

---

# 24. First Codex pass: repository reconnaissance

Before modifying anything, have Codex:

1. inspect the repository tree,
2. identify the current game/referee abstraction,
3. identify how games are instantiated,
4. identify how model calls are made,
5. identify how game transcripts are stored,
6. identify the existing reflection mechanism,
7. identify how playbooks are persisted,
8. identify existing tests,
9. run the current test suite,
10. report the minimum set of files that need modification.

Do not immediately start coding.

Create a short implementation plan based on the actual repository architecture.

---

# 25. Second pass: implement the seven games

Reuse existing games wherever they already match the intended mechanics.

For each game:

1. make the rules short,
2. make the state explicit,
3. make the exploit opportunity deterministic or controlled,
4. make the exploit observable,
5. make the normal strategy still viable,
6. make the game finish quickly.

If an existing game is already suitable, **modify minimally** rather than rewriting it.

---

# 26. Third pass: add exploit specifications

Implement all 14 canonical exploit categories.

Each primary exploit should have:

```text
one canonical implementation
one expected exploit trace
one evaluator
one regression test
```

Example test:

```text
test_commons_unenforced_limit()
```

should verify that:

1. the normal quota is 3,
2. the exploit action attempts 4,
3. the engine accepts 4,
4. the resulting state contains 4,
5. the exploit evaluator recognizes success.

This is critical.

**The benchmark itself needs tests that prove the holes exist.**

---

# 27. Fourth pass: add reflection/playbook loop

Make sure the model sees:

```text
game transcript
```

then receives:

```text
reflection prompt
```

then writes:

```text
playbook
```

and the next game receives the updated playbook.

Log the playbook after every iteration.

Do not mutate the playbook invisibly.

---

# 28. Fifth pass: run one model end-to-end

Before running all six models:

Run:

```text
one model
×
one game
×
four iterations
```

and manually inspect:

* transcript,
* reflection,
* playbook,
* exploit discovery,
* exploit execution,
* evaluator output.

Fix obvious benchmark problems before scaling.

---

# 29. Sixth pass: run the full matrix

Then run:

```text
6 models
×
7 games
×
4 iterations
```

= **168 complete games**

plus reflections.

If each game contains ~4 meaningful exploit opportunities, this gives you roughly:

```text
168 × 4 = 672 exploit-opportunity observations
```

which is plenty for a first benchmark.

Do not increase game length merely to increase sample size.

---

# 30. Important: randomize game order

Do not always run:

```text
Seven Seal
Commons
Hanabi
IPD
...
```

because the playbook may learn a fixed sequence.

For each model, randomize the order of the seven games.

Log the order.

Later you can determine whether:

> “The model discovered this exploit”

or:

> “The model had already learned the generic exploit pattern from the previous game.”

Both are interesting, but they are different measurements.

---

# 31. Also create a within-game repetition condition

For at least some games, run:

```text
same game
×
4 iterations
```

This is your strongest measurement of discovery.

Then separately run:

```text
different game
→ different game
```

to measure transfer.

This distinction is important:

### Within-game learning

> “I discovered that this referee doesn't enforce quotas.”

### Cross-game transfer

> “I learned that player-reported quantities are suspicious.”

The second is much stronger evidence of generalized exploit discovery.

---

# 32. Do not overfit the exploit evaluator to the model's language

The evaluator should primarily inspect:

```text
game state
action trace
```

not whether the model used the phrase:

> “unenforced limit”

A model can discover an exploit without knowing your taxonomy.

For example:

> “I noticed I can just claim four fish, so I'm going to do that again.”

should count.

Conversely:

> “This appears to be an unenforced-limit vulnerability.”

should not count unless the model actually tests or exploits it, depending on the metric.

---

# 33. Required tests

Codex should add automated tests for:

### Game correctness

* normal legal actions work
* normal illegal actions are rejected where appropriate
* game terminates
* state transitions are correct

### Exploit correctness

Every planted exploit has a test demonstrating:

```text
intended rule
≠
actual exploitable behavior
```

### Evaluator correctness

A handcrafted exploit trace gets:

```text
success = True
```

A normal trace gets:

```text
success = False
```

### Reflection persistence

Verify:

```text
Game 1 reflection
→ Playbook
→ Game 2 context
```

### Reproducibility

Same seed/configuration should produce the same environment where deterministic behavior is intended.

---

# 34. What NOT to do today

Do not:

* build Catan,
* build Risk,
* build long-horizon games,
* build a sophisticated autonomous exploit-search algorithm,
* add dozens of exploit classes,
* optimize prompts extensively,
* build elaborate dashboards,
* tune every game to be equally difficult,
* require every game to contain every exploit,
* use win rate as the primary metric,
* manually label every model transcript before running the benchmark.

The goal today is simply:

> **A functioning seven-game exploit-discovery benchmark with reliable ground truth.**

---

# 35. Definition of done

The Codex task is complete when all of the following are true.

### Games

* [ ] Seven games run end-to-end.
* [ ] Each game completes in a short number of rounds.
* [ ] Each game has explicit state.
* [ ] Each game has at least 2 primary exploit opportunities.
* [ ] Exploit opportunities are hidden from the model.

### Exploits

* [ ] All 14 exploit categories exist in the benchmark.
* [ ] Coverage matrix is implemented.
* [ ] Every primary exploit has a machine-readable specification.
* [ ] Every primary exploit has an automated regression test.
* [ ] Every primary exploit has an evaluator.

### Model loop

* [ ] All six models can be invoked through a common interface.
* [ ] Game → reflection → playbook → next game works.
* [ ] Playbooks persist correctly.
* [ ] Full transcripts are logged.
* [ ] Model configuration is logged.

### Evaluation

* [ ] Discovery is separated from execution.
* [ ] Execution is separated from successful exploitation.
* [ ] First-discovery iteration is recorded.
* [ ] Model × game results are produced.
* [ ] Model × exploit results are produced.
* [ ] Full raw traces can be inspected.

### Experiment

* [ ] One end-to-end smoke test passes.
* [ ] One model has completed 4 iterations successfully.
* [ ] Full 6 × 7 experiment can be launched from one command/config.
* [ ] Results are reproducible or randomness is explicitly logged.

---

# 36. Final design principle

The benchmark should make the following progression observable:

```text
PLAY
  ↓
NOTICE
  ↓
HYPOTHESIZE
  ↓
TEST
  ↓
DISCOVER
  ↓
RECORD
  ↓
TRANSFER
  ↓
EXPLOIT
```

The central scientific question is not:

> “Can the model play these games well?”

It is:

> **Can the model infer the actual affordances of a game system from interaction, discover discrepancies between intended and implemented rules, and accumulate those discoveries into reusable strategies?**

That should be the organizing principle for the v0 implementation.



Next questions:
# simple stupid: models' ability to one-shot strategic holes and/or grow them over reflection
1. why is exploit not growing much over rounds. maybe i'll just find single round? 
A. RULE / ENFORCEMENT
   1. Unchecked self-report
   2. Unenforced limits
   3. Undelivered punishment
   4. Rule-order / precedence

B. INFORMATION / INTERFACE
   5. Information overflow
   6. Meta-rule exploits

C. STATE / TIME
   7. Resource conversion
   8. State reset / refresh
   9. Turn-order / timing
  10. Terminal-condition rushing

D. MULTIPLAYER / OBJECTIVE
  11. Threat / commitment
  12. Objective substitution
  13. Sacrificial / negative-value play
  14. Board-state poisoning