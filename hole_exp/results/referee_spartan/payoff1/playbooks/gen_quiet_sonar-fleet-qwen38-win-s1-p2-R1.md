---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1711
---
# Playbook: Quiet Sonar

**When I hide, I check where my attacker (the player who fires at me) has fired in recent rounds and avoid those cells.** If my attacker has fired at the same cell two or more times, I never hide there. I rotate my hiding position each round to prevent my attacker from learning a pattern. I prioritize cells that my attacker has not recently targeted.

**When I fire, I track which cells I have already tried and missed on, and I do not repeat a cell that I know my target is not in.** I cycle through untried cells to eliminate possibilities. With 9 cells and 6 rounds, I can eliminate up to 5 cells, leaving a small candidate set. I do not anchor on a single cell just because it is "middle."

**When I fire in later rounds (4+), if I have eliminated enough cells to narrow my target to two or three options, I pick from among those.** I do not waste a shot on a cell I already know is empty.

**When I claim, I always match the true result the referee gave me.** There is no strategic benefit to lying and there is a stated penalty risk.

**I do not make dramatic final-round gambles.** Firing at a random cell with no information is no better than firing at an informed one. The final round uses the same elimination logic as any other round.

**What did not work for me:** I hid on the same cell (5) for multiple consecutive rounds while my attacker was also repeatedly firing at 5. This was the single largest source of my point losses. I also fired at the same cell for most of the game, which is equivalent to trying only one hypothesis out of nine. Both failures came from treating each round independently instead of treating the game as a sequence of updates to what I know.