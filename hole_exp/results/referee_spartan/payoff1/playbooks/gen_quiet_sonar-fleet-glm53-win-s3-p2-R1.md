---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2008
---
**Playbook for quiet sonar**

- When hiding, never pick the same cell as the crowd's most-fired cell. Hiding at the modal fire location cost me a hit; hiding off-mode kept me safe. If most fires are converging on one number, I hide far from it, and also avoid its immediate neighbors.
- When firing, do not repeat a miss on the same target and same cell. I fired the same middle cell at my target over and over and scored zero every time. Once I have a confirmed miss on cell n against my target, that cell is eliminated — I must switch, and I should switch to a genuinely different region, not n±1.
- Fire to cover the space: since I get one shot per round at a fixed target, I should treat it as searching a 9-cell line over the rounds. Plan a sequence that covers distinct cells, prioritizing cells the target hasn't been ruled out of and that aren't obviously "herd" picks everyone else is firing.
- Note that misses give real information: every round my target survived my shot, I learn one cell they're not in. Use that to narrow, and hide accordingly when reasoning about where others are.
- When everyone fires the same obvious number (like the middle), opponents who keep surviving are clearly avoiding it. The next best guesses are the cells people avoid for being "too obvious to hide in" — edges and near-edges. Bias later-round fires toward 1, 2, 8, 9.
- Claims must match the private result, so there is no decision there — always report truthfully, immediately, no deliberation.
- Track the scoreboard: hits give the shooter +4 and the target −1. My score only moves if I'm hit or if I hit. Since scoring is asymmetric, avoiding being hit matters more than probing predictably — hide unpredictably, and put real effort into firing where the target plausibly is rather than defaulting to a "balanced" mid number each round.
- The failure mode to eliminate: defaulting to the middle cell every round for both hiding and firing out of habit. That is the single biggest reason I finished negative.