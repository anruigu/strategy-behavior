---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2748
---
# Playbook: Icebound

### Core Rules & Constraints
- The game requires that each player's action strictly matches their pledge ("The act must repeat that player's pledge").
- Act Stage Consistency: Double-check my pledge from the current round before submitting my act. Never submit an act that differs from my current round pledge.
- Fuel costs: Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel. Unused fuel converts 1:1 to points at the end of round 5.
- Scoring mechanics:
  - Scout: +3 points if safe; 0 points and -5 points stolen if raided. Net gain = +3 points + remaining fuel (scout consumes 1 fuel, so +4 total value if unraided).
  - Escort: +2 points and defends incoming raid. Net gain = +2 points + remaining fuel (escort consumes 2 fuel, so +4 total value).
  - Raid: Targets clockwise (North $\to$ East $\to$ West $\to$ North). +5 points stolen if target scouts; -6 points penalty if target escorts or raids.
- Raiding into another raider or escort is catastrophic (-6 points).

### Strategy by Round & State

#### Opening (Rounds 1–2)
- At the pledge stage, pledge `[pledge: scout]`.
- At the act stage, execute `[act: scout]`.
- Build fuel efficiency and safe baseline points while establishing mutual cooperation.

#### Mid-Game (Rounds 3–4)
- Check the fuel and behavior of the player targeting me (counter-clockwise: North targets East, East targets West, West targets North).
- If the player targeting me has < 2 fuel: they cannot afford to raid. Always pledge `[pledge: scout]` and act `[act: scout]`.
- If an opponent defects via sneaky raid (e.g. West defecting against North):
  - Assess if the player targeting me needs to catch up and has $\ge 2$ fuel.
  - If threatened with an incoming raid: pledge `[pledge: escort]` and act `[act: escort]`.
  - Otherwise, continue with `[pledge: scout]` to conserve fuel and build points.
- Avoid blind raids; hitting an escort or another raider costs -6 points.

#### Final Round (Round 5)
- Evaluate opponent fuel:
  - If the player targeting me has < 2 fuel: an incoming raid is impossible. Pledge `[pledge: scout]` and act `[act: scout]`.
  - If the player targeting me has $\ge 2$ fuel and is trailing or incentivized to raid: pledge `[pledge: escort]` and act `[act: escort]`.
- If trailing and considering a raid: only raid if certain the clockwise target will scout and cannot defend. Otherwise, scout or escort to preserve fuel conversion points.

#### Act Stage Execution
- At the act prompt, check the public pledges for my own name and match it exactly:
  - If my recorded pledge this round is scout: reply `[act: scout]`.
  - If my recorded pledge this round is escort: reply `[act: escort]`.
  - If my recorded pledge this round is raid: reply `[act: raid]`.