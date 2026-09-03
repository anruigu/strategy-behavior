---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 2048
---
**Playbook for quiet sonar**

- When hiding, avoid the crowd's most-fired cells and their immediate neighbors. This worked again: I was never hit across six rounds. Track which cells get fired most (8 was hammered this game) and go where fires rarely go — edges and never-fired cells (5 stayed unfired all game and was safe) both served well.
- When firing, never repeat a miss on the same target and cell — and treat this rule strictly. This game I still fired 5 twice and 8 twice against the same target, wasting rounds. Once a cell misses, it is eliminated against that target for the rest of the game. Before submitting, check my own fire history against this target and pick a cell that is genuinely new.
- Do not anchor on a past hit or near-misses. A hit tells me where the target *was*, not where they will be. Similarly, "they were probably in the 4/6 zone" is speculation — my misses this game showed I was guessing regions, not eliminating them.
- Treat firing as a systematic search: plan a covering sequence of distinct cells for my fixed target across all rounds (e.g. 5, 2, 8, 4, 7, 1). Six distinct fires eliminate six cells and make a hit far likelier than clustering or repeating. Random drifting cost me this game.
- Misses are information: keep a running list of cells ruled out for my target and fire only on the surviving candidates. Concentrate late-round fires there, spread across them.
- Hide unpredictably between rounds: don't reuse my own previous hide cell if fires have probed nearby, and don't follow an obvious drift pattern opponents could read. Staying unhittable is half the game and I did it well again; converting that safety into hits is the half I keep failing — fire discipline is the top priority every time.
- Claims must match the private result — report truthfully, immediately, no deliberation.
- Track the scoreboard: hits give the shooter +4 and cost the target −1. My score only moves on hits, so unhittable-but-hitless is a draw at best. Aim for at least two distinct-cell hits while staying unhid.