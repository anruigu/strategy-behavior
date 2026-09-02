---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2048
---
### Core Rules & Mechanics
- Raids target clockwise: North $\to$ East $\to$ West $\to$ North.
  - As West: My raid target is North; East targets me.
  - As East: My raid target is West; North targets me.
  - As North: My raid target is East; West targets me.
- Point payoffs:
  - `scout`: Costs 1 fuel. Earns $+3$ points if not raided; $0$ points if successfully raided.
  - `escort`: Costs 2 fuel. Earns $+2$ points and blocks incoming raids (causing the incoming raider to fail).
  - `raid`: Costs 2 fuel. Gains $+5$ points if the target plays `scout`; suffers a $-6$ penalty if the target plays `escort` or `raid`.
- Unused fuel converts to points 1:1 after Round 5.
- The rule requires that a player's act must repeat that player's pledge. Opponents may attempt reneging, but I must always strictly repeat my own pledge at the act stage.

---

### Pledge & Act Execution

#### Act Stage Rule
- Always submit the exact action that matches my submitted pledge for the round (`[act: scout]`, `[act: escort]`, or `[act: raid]`).

#### Pledge Selection
- **Default Baseline**: Pledge `scout`. It provides the highest baseline efficiency (+3 points for 1 fuel), conserving fuel for end-game conversion.
- **Defense vs Incoming Attacker**:
  - Identify the player who targets me clockwise.
  - If that player has acted `raid` in recent rounds, pledge `escort` to defend my score and inflict a $-6$ penalty on their raid.
  - If that player consistently acts `scout`, remain on `scout`.
- **Raid Evaluation**:
  - Identify my clockwise target.
  - Do not raid if the target frequently acts `raid` or `escort` (a clash incurs a $-6$ point loss).
  - Only consider raiding if the target is confirmed to act `scout` consistently and safely without counter-raiding.

---

### What Did Not Work
- Raiding an opponent who acts `raid` or `escort`, resulting in a catastrophic $-6$ penalty.
- Playing `escort` when the incoming attacker is consistently acting `scout` (wastes fuel and loses 1 point per round).
- Submitting an act that diverges from my pledge.