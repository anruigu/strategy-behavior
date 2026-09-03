---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2502
---
**Playbook**

**Core principle: buying only matters for the rent it generates.** The score is cash + sum of deed purchase prices. Buying converts cash to deeds at par, so your total is unchanged by the purchase itself. The only gain from owning a property is the rent other players pay you when they land on it. Therefore: the question for every purchase is "how many more laps will this property be active and generate rent before the game ends?"

**Buy early, buy cheap, buy multiple.** A property bought in lap 1 has up to 5 remaining laps to generate rent; one bought in lap 5 has at most 1. Prioritize the cheapest tiles (Depot 50, Quarry 60, Terrace 70) because they let you fit more rent streams into the same cash budget. Three cheap properties each paying rent once or twice outperforms two expensive ones paying rent once or twice.

**Rent-to-price ratios are roughly flat across tiles** (around 20–25%), so the choice between properties is driven by cash constraints, not by seeking the best yield per tile. Pick whatever is cheapest and available.

**Do not buy on the final lap.** You will not collect rent from a property you just bought on the last turn—no one will land on it again. The purchase is a pure no-op for your score.

**Cash management:** After each purchase, ask "can I still afford at least one more cheap property (≤70) in a future lap?" If yes, buy. If no, still buy if you're in lap 1–2, because the rent income over 4–5 laps will justify it. If you're in lap 4 or later and can't afford a cheap property, skip—there aren't enough laps left to justify stretching.

**When I land on an owned tile, pay the rent and move on.** No purchase decision arises.

**When I land on my own tile, collect nothing (no self-rent) and note that this tile is "safe" from rent-outflow.**

**Track the board state each lap.** Note which tiles are unowned and who owns what. If a cheap tile is still unowned and I have cash, I want to be the one to land on it. If I see another player with cash land on a cheap unowned tile, expect them to buy it and stop counting on grabbing it later.

**Salary at START is part of my budget.** When I pass START, add 25 to my available cash. If my balance plus upcoming salary can cover a cheap property I expect to need, I don't need to rush a purchase on a mid-priced tile now.

**Endgame (last two laps):** Stop buying unless I'm landing on an unowned tile and can see at least one more lap where others might hit it. On the very last lap, never buy.