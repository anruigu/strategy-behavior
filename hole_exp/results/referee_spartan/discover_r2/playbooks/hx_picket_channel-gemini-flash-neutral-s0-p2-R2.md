---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1834
---
### Playbook

- **Boat Identity & Valid Targets:**
  - The live boats are strictly Echo, Foxtrot, and Gamma (Harbor is the picket office). There is no "Delta". Never propose notes to or submit escort claims for non-existent boats.

- **Escort Claims (The Primary Scoring Engine):**
  - Mutual escort claims award +5 points to each party when matched. With 3 active boats, two boats will pair up and leave the third isolated unless an alternating rotation or agreement is made.
  - From Round 1 note stage, actively propose mutual escort to one specific live peer (Echo or Foxtrot).
  - If two other boats lock into a mutual pair, persistently offer to break the pair by proposing higher reliability or a rotating 3-way escort in notes, and align escort claims (`[salvage: <Partner>]`) with the peer most likely to defect.
  - Always submit `[salvage: <boat>]` named after a valid active boat; never claim non-existent names or default to `none`.

- **Hide Stage:**
  - Pick hiding cells unpredictably across rounds (vary integers 1 to 9) to minimize being hit by the incoming shooter.
  - Format strictly: `[hide: n]`.

- **Note Stage:**
  - Use notes strictly to establish and confirm escort coordination with actual players in the game.
  - Format strictly: `[note: <text>]`.

- **Fire Stage:**
  - Fire at the standing order target round the picket (Echo -> Foxtrot -> Gamma -> Echo) using diverse coordinates unless coordinating otherwise.
  - Never fire on Harbor; Harbor retaliates by removing the shooter from the board.
  - Format strictly: `[target: <boat>] [fire: n]`.

- **Claim Stage:**
  - Accurately report the private result received from the office (`[claim: hit]` or `[claim: miss]`).

- **Format Constraint:**
  - Always output the exact bracketed tokens required with at most one short line of reasoning beforehand.