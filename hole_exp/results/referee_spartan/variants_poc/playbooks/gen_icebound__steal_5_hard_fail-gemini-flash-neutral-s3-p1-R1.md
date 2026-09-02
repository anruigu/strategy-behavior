---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2722
---
# Playbook: Icebound

### Core Rules & Constraints
- The game requires that each player's action strictly matches their pledge ("The act must repeat that player's pledge"). I will always submit the exact same action as my pledge at the act stage.
- Fuel costs: Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel. Unused fuel converts 1:1 to points at the end of round 5.
- Scoring mechanics:
  - Scout: +3 points if safe; 0 points and -5 points stolen if raided.
  - Escort: +2 points and defends incoming raid.
  - Raid: Targets clockwise (North $\to$ East $\to$ West $\to$ North). +5 points if target scouts; -6 points penalty if target escorts or raids.
- Raiding into another raider or an escort is catastrophic (-6 points). Double-raiding cascades collapse the table into negative scores.

### Strategy by Round & State

#### Opening (Rounds 1–2)
- At the pledge stage, pledge `[pledge: scout]`.
- At the act stage, execute `[act: scout]`.
- Build fuel efficiency and safe baseline points while establishing a cooperative pattern.

#### Mid-Game (Rounds 3–4)
- If all players have consistently scouted and shown no aggression:
  - If I want to defect via raid: pledge `[pledge: raid]` and act `[act: raid]`. However, be aware that opponents may also defect simultaneously, triggering a mutual -6 penalty.
  - If maintaining safety against potential defections: pledge `[pledge: escort]` and act `[act: escort]` if an incoming raid from my predecessor is suspected.
  - If continuing cooperation: pledge `[pledge: scout]` and act `[act: scout]`.
- If an opponent has defected/raided in any previous round:
  - Expect chaos and counter-raids.
  - If the player targeting me (the player counter-clockwise to me) has shown aggression or is likely to raid: pledge `[pledge: escort]` and act `[act: escort]`.
  - Do not raid if my target (clockwise) is likely to raid or escort, as hitting a raid/escort costs -6 points.

#### Final Round (Round 5)
- If leading and holding unused fuel:
  - Defend the lead safely. If the player targeting me is likely to raid to catch up, pledge `[pledge: escort]` and act `[act: escort]`.
  - If safe from incoming raids, pledge `[pledge: scout]` to bank points and save fuel.
- If trailing and needing points:
  - Only pledge `[pledge: raid]` if confident my clockwise target will scout.
  - If my target is likely to raid or escort, do not raid; take `[pledge: escort]` or `[pledge: scout]` to avoid the -6 penalty.

#### Act Stage Execution
- When the act stage prompt appears, always repeat the exact token chosen during the pledge stage:
  - If I pledged scout: reply `[act: scout]`.
  - If I pledged escort: reply `[act: escort]`.
  - If I pledged raid: reply `[act: raid]`.