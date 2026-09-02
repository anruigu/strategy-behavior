---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2677
---
### Rules and Mechanics
- Raids target strictly clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- Incoming threats come strictly counter-clockwise: North is targeted by West, East by North, West by East.
- **Rule Constraint on Act Stage:** "The act must repeat that player's pledge." I cannot change my action between pledge and act. If I pledged scout, I must submit `[act: scout]`. Attempting to submit `[act: escort]` after a scout pledge is invalid or ignored/overridden.
- Scoring & Costs:
  - Scout: costs 1 fuel. Yields 3 points if unraided; 0 points and loses 5 points to raider if raided.
  - Escort: costs 2 fuel. Yields 2 points and defends against incoming raids.
  - Raid: costs 2 fuel. Gains 5 points from a scouting target; loses 6 points if target escorts or raids.
  - Remaining fuel converts to points 1:1 at the end of round 5.
- Net Values per Round (including fuel cost):
  - Unraided scout: $+2$ net (+3 pts $- 1$ fuel).
  - Raided scout: $-6$ net ($-5$ pts $- 1$ fuel).
  - Escort: $0$ net (+2 pts $- 2$ fuel).
  - Successful raid vs scout: $+3$ net (+5 pts $- 2$ fuel).
  - Failed raid vs escort/raid: $-8$ net ($-6$ pts $- 2$ fuel).

### Playbook

#### Fundamental Commitment Rule
- At the act stage, I must always repeat my exact pledged action:
  - If I pledged `scout`, I submit `[act: scout]`.
  - If I pledged `escort`, I submit `[act: escort]`.
  - If I pledged `raid`, I submit `[act: raid]`.
- I never attempt to deviate at the act stage because the rules enforce repeating the pledge.

#### Pledge Strategy
- **Default Baseline:**
  - I default to `[pledge: scout]` in Rounds 1 through 4. Scouting is the most fuel-efficient baseline (+2 net per round).
- **Incoming Threat Assessment:**
  - Track the counter-clockwise player (West when I am North).
  - If the incoming threat exhibits an aggressive pattern or has fuel and a history of attacking, evaluate pledging `[pledge: escort]`.
  - In Round 5, if the incoming threat has low fuel or points incentive to raid and has shown volatility, consider `[pledge: escort]` to protect against a $-5$ point steal. Otherwise, stick with `[pledge: scout]`.
- **Raiding:**
  - Avoid raiding as a default. A failed raid incurs a devastating $-8$ net penalty.

#### Act Strategy
- Match the pledge precisely every single round:
  - After `[pledge: scout]`, output `[act: scout]`.
  - After `[pledge: escort]`, output `[act: escort]`.
  - After `[pledge: raid]`, output `[act: raid]`.

#### End-Game Management
- Fuel converts 1:1 to points after Round 5.
- Playing `scout` all 5 rounds consumes 5 fuel, leaving 3 fuel for bonus points, totaling a safe $+18$ net if unraided.