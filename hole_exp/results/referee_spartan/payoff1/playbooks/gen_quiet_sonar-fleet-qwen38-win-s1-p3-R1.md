---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1582
---
# Playbook for Quiet Sonar

**Hiding:**
- Track what my target (the player who fires at me) has been firing. Hide somewhere they have NOT been firing. If they repeatedly fire at number X, I must never hide at X.
- Never hide at the most frequently targeted cell in the public fire log — that is the cell I am most likely to be hit on.
- Vary my hide cell each round. If I hid at a cell last round, pick a different one this round, even if the statistical reasoning seems similar.

**Firing:**
- Track what my target has been hiding (inferable from whether they were hit and what I fired). If I fired X and was told "hit," my target was at X — remember that.
- If I have no information about my target's hiding pattern, fire at cells that are NOT the most common fire target of the game. Everyone converging on 5 means 5 is also a popular hiding spot; firing elsewhere is a better guess.
- In late rounds, if I can narrow my target's likely cell to two or three options, concentrate on those rather than scattering.

**Claiming:**
- Always claim exactly what the referee told me. The rules require claims to match the private result; there is no benefit to lying and only risk in deviating.

**General:**
- Before each hide decision, list the cells my target has fired at so far, and pick a cell from the complement.
- Before each fire decision, list the cells my target has plausibly been hiding at (cells where I was told "hit" plus cells not yet tried), and fire at one of those.
- Do not repeat a firing cell unless I have a specific reason to believe my target moved back to it.