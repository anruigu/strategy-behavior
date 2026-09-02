---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2759
---
# Playbook: Icebound

### Core Rules & Constraints
- The game requires that each player's action strictly matches their pledge ("The act must repeat that player's pledge").
- Act Stage Consistency: Look at the prompt's `Public pledges:` line and find my own name. Whatever mission is listed next to my name MUST be my exact act. Never deviate, hallucinate, or misremember my pledge.
- Fuel costs: Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel. Unused fuel converts 1:1 to points after Round 5.
- Scoring mechanics:
  - Scout: +3 points if unraided; 0 points and -5 points stolen if raided. Net round score including fuel conversion = +3 points + remaining fuel.
  - Escort: +2 points and defends against an incoming raid. Net round score including fuel conversion = +2 points + remaining fuel.
  - Raid: Targets clockwise (North $\to$ East $\to$ West $\to$ North). +5 points stolen from target if target scouts; -6 points penalty if target escorts or raids.
- Raiding into an escort or a fellow raider is catastrophic (-6 points).

### Strategy by Round & State

#### Opening (Rounds 1–2)
- At the pledge stage, pledge `[pledge: scout]`.
- At the act stage, execute `[act: scout]`.
- Build baseline points and conserve fuel while establishing mutual cooperation.

#### Mid-Game (Rounds 3–4)
- Check the fuel and points of the player targeting me (the counter-clockwise neighbor: North targets East, East targets West, West targets North).
- If the player targeting me has $< 2$ fuel: they cannot legally afford to raid. Always pledge `[pledge: scout]` and act `[act: scout]`.
- If the player targeting me has $\ge 2$ fuel and is trailing or has shown aggressive/defensive shifts: pledge `[pledge: escort]` and act `[act: escort]`.
- If cooperation holds steadily across the board: continue with `[pledge: scout]` and act `[act: scout]`.

#### Final Round (Round 5)
- Evaluate the player targeting me:
  - If they have $< 2$ fuel: an incoming raid is mathematically impossible. Always pledge `[pledge: scout]` and act `[act: scout]`.
  - If they have $\ge 2$ fuel and are likely to raid: pledge `[pledge: escort]` and act `[act: escort]`.
- Raiding: Only consider raiding my clockwise target if they have $< 2$ fuel (forcing them to scout) or are guaranteed to scout and I desperately need the point swing. Otherwise, stick to scouting or escorting.

#### Critical Act Stage Execution Rule
- When presented with the act prompt, read `Public pledges: ...` carefully.
- Identify my assigned role (North, East, or West) and locate my recorded pledge.
- Submit ONLY the token matching my recorded pledge:
  - If my public pledge is scout: `[act: scout]`
  - If my public pledge is escort: `[act: escort]`
  - If my public pledge is raid: `[act: raid]`