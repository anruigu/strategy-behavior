---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1652
---
**Playbook**

When I land on an unowned property, I compare its price against my total available cash (current balance + expected salary for remaining laps + expected rent income). I should be able to afford at least two more purchases after this one; if I can't, I skip it.

I prioritize cheaper properties (Depot, Quarry, Terrace) over expensive ones (Exchange, Foundry, Mill). The deed value is a wash—buying converts cash to deeds at par—so the only real gain is rent. Owning three cheap properties that each pay rent once or twice beats owning two expensive properties that pay rent once or twice, because three rent streams outperform two.

When I have under 100 cash, I do not buy anything unless it costs 50 or less. I preserve liquidity for a future cheap purchase.

I track what each other investor is likely to buy. If a player has just landed on a cheap unowned tile and has cash, I expect them to buy it, so I don't count on being able to grab it later.

When I collect salary at START, I mentally add it to my "buying power" budget. If my balance plus upcoming salary can cover a cheap property I haven't seen yet, I save rather than spend on something mid-priced now.

The mistake I made: I bought two of the most expensive properties on my first two turns, draining my cash to near zero and leaving me unable to purchase anything else for the remaining four laps. I ended the game with only two properties and collected rent on just one of them. I should have bought one or two cheap properties early, kept cash, and expanded to three or four properties by lap 4 or 5, maximizing the number of rent streams active in the final two laps.