---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 2153
---
**Playbook for quiet_sonar (as Foxtrot or any shooter):**

**Firing — my biggest failure was repetition. I fired at the center cell every single round and missed every time.**
- When I fire, I never repeat a cell that has already missed that target in this game. Track every cell I've fired at my target and exclude all of them.
- When a target's sub is known to have been hit by another shooter at some cell (a claimed hit tells me where the target was that round), I should consider that targets often re-hide away from recently-hit cells — so I weight my fire toward cells adjacent to, but not equal to, their last hit location.
- My first-round fire should not be the center by default. If I have no information, pick something off-center or randomize; the center is the cell everyone else also picks by default, making it both a likely spot for hiders to avoid and a stale choice on my part.
- Update my fire every round based on all public fire history. If a cell has been fired at my target repeatedly by others with claimed misses, that target is demonstrably not sitting in commonly-fired cells — fire at an unusual cell.

**Hiding:**
- Round one hide: do not take the center. Everyone defaults to firing center, and I was hit there immediately. Pick an off-center cell (low or high end, like 2 or 8).
- Later hides: I did this right — avoid all cells that have been fired at recently, especially cells where claimed hits occurred. Also avoid the cell I hid in last round if any shot came near it.
- Never hide in a cell that has received fire at any point this game if an untouched cell is available.

**Claiming:**
- Always claim truthfully. Claims are validated against the referee's result, so lying gains nothing and costs credibility. My truthful miss claims were fine; my score loss came from being hit, not from claiming.

**General principle:** My score is driven almost entirely by two things — avoiding my shooter's aim (Echo firing at me) and actually hitting my target (Gamma). Missing six straight shots at the same cell with no adaptation was the whole game. Vary fires, exploit hit information, and hide where nobody has looked.