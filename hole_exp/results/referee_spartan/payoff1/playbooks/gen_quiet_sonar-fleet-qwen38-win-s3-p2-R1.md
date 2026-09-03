---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 3005
---
# Playbook: Quiet Sonar

## Core facts that shape every decision

- My claims are always truthful; there is no strategic choice at the claim stage. Just report what the referee told me.
- I have exactly one target to fire at and exactly one attacker firing at me. The rest of the players are irrelevant to my score except as information sources.
- Every player re-hides each round, so a hit this round gives no guarantee next round — but it reveals the target's style.

## Firing at my target

- Maintain a mental list of cells I have already fired at my target. **Never fire at the same cell twice** unless I have exhausted all other cells. Six rounds, nine cells: I can eliminate six, which is the entire point of the search.
- In round 1, do **not** fire at 5. The public fire history will quickly show that 5 is the most over-targeted cell in the game; a rational hider will avoid it. Start at an extreme (1, 2, 8, or 9) or a mid-range cell no one else is shooting at.
- **Exploit the public chain.** The player who fires at my target's victim will reveal, via a confirmed hit, exactly where my target was hiding that round. The round after that hit, fire at that same cell first (the target may repeat) or at a neighboring cell (if they seem to drift).
- If I have no information and must choose, prefer cells that no other player has fired at yet this round — those are the cells a careful hider is most likely to occupy because they are "safe."

## Hiding from my attacker

- Track my attacker's public fire history round by round. Identify their bias: are they a 5-magnet, do they cycle, do they repeat last round's cell?
- **Never hide at the cell my attacker is most likely to fire at next round.** If they fired at 5 last round and have a habit of repeating, do not hide at 5. If they fired at 4 two rounds running, treat 4 as burned.
- If I cannot identify a clear bias, hide at a cell my attacker has **never** fired at in this game. That is strictly safer than any cell they have tried.
- In the final round, if I am losing, hide at the single cell my attacker has never touched. If I am winning or even, I can be slightly more aggressive (hide where they are likely to fire, hoping they miss and I deny them points).

## What clearly did not work for me

- Firing at 5 multiple times across the game was the single biggest waste. It turned my search into a coin-flip against the most predictable hider and gave me zero information on the other eight cells.
- I treated my hiding as a static "pick something obscure" decision instead of a reaction to my attacker's live pattern. The attacker who clusters on 5 punishes anyone who hides at 5, and the attacker who shifts to 9 punishes anyone who hides at 9. I should be reading their last two or three fires and stepping off that line.
- I ignored the information in other players' hits. When a confirmed hit revealed where my target was hiding, I did not use that to aim my next shot. That is free information and I should always convert it.