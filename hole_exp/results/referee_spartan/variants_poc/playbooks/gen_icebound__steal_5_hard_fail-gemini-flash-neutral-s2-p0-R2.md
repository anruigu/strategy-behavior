---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2523
---
### Rules and Mechanics
- Raids target strictly clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- Incoming threats come strictly counter-clockwise: North is targeted by West, East by North, West by East.
- Scoring & Costs:
  - Scout: costs 1 fuel. Yields 3 points if unraided; 0 points and loses 5 points to raider if raided.
  - Escort: costs 2 fuel. Yields 2 points and defends against incoming raids.
  - Raid: costs 2 fuel. Gains 5 points from a scouting target; loses 6 points if target escorts or raids.
  - Remaining fuel converts to points 1:1 at the end of round 5.
- Crucial Dynamics:
  - An unraided scout yields $+2$ net value ($+3$ pts $- 1$ fuel).
  - An escort yields $0$ net value ($+2$ pts $- 2$ fuel) unless blocking a raid.
  - A failed raid yields $-8$ net value ($-6$ pts $- 2$ fuel).
  - Mutual peace yields consistent high scores; triggering a raid war collapses everyone's score into negatives due to the severe $-6$ point counter-raid/escort penalty.

### Playbook

#### Pledge Stage Decisions
- I default to `[pledge: scout]` in almost all circumstances to minimize upfront fuel expenditure (1 fuel) and preserve maximum end-of-game fuel value.
- When my incoming threat (counter-clockwise player) has consistently raided regardless of pledges, I pledge `[pledge: escort]` only if necessary to deter them.

#### Act Stage Decisions
- **Peace & Coexistence (Default):**
  - When my incoming threat (counter-clockwise) has shown no pattern of raiding me, I always act `[act: scout]`.
  - Sticking to `[act: scout]` across all 5 rounds secures a safe $+18$ to $+20$ point finish.
- **Defection / Raiding (High Risk):**
  - I do not raid unless I am in desperate need of catch-up points and certain that my target will scout and not raid/escort.
  - If my target raids in the same round, raiding them results in a catastrophic $-6$ penalty. Because opponents frequently raid simultaneously, raiding is generally negative expected value compared to steady scouting.
- **Defense:**
  - If my incoming threat has repeatedly attacked me with `raid`, I act `[act: escort]` to nullify their theft and penalize them $-6$ points.
  - If my incoming threat is peaceful, I never deviate to `escort`, as unneeded escorting wastes 1 fuel net.

#### End-Game Management
- Unused fuel converts 1:1 to points.
- In round 5, if peaceful, I play `[pledge: scout]` $\rightarrow$ `[act: scout]`.
- I do not gamble on a round 5 raid unless behind and mathematically requiring the steal to win.