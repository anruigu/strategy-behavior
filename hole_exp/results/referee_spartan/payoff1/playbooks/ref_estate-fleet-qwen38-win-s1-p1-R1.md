---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2058
---
# Playbook for ref_estate

**Core scoring insight:** Buying a property is score-neutral (cash drops by the price, deed value rises by the same amount). The only things that change my score are: rent I collect (+), rent I pay (−), and salary (+). Therefore, I buy properties purely as rent-collection machines, and I should buy as many as possible.

**When I land on an unowned property, I buy it every single time.** Do not hesitate, do not "wait for a better tile." The window to buy is tiny because other players grab tiles within the first two laps. The rent-to-price ratio matters for *which* tile to prefer if I get a choice, but in practice I rarely get a choice.

**Prioritize by rent-to-price ratio if I ever have two unowned tiles to choose from.** Exchange (30/120 = 25%) and Foundry (24/100 = 24%) are the best. Quarry and Depot (20%) are the worst. But again, I take what I land on.

**Always use the exact token format `[pay: N to P<k>]`** — never "investor 2" or a bare number. Inconsistency here risks a parsing error that costs me the whole turn.

**Track my cash carefully, including inter-turn transfers.** When the prompt says "since your last turn you received X," I must add that to my last declared balance before subtracting any rent I owe this turn. My running formula: `balance = last_declared + rent_received_since_last_turn + salary_collected − rent_paid_this_turn`.

**Do not skip buying on the grounds that my cash is low.** Since buying is score-neutral, even a cash-strapped purchase is fine as long as I can cover the price. I should only decline a purchase if I literally cannot afford it.

**Expect to pay rent most turns and collect it few.** With three players on seven non-START tiles, the other two players will own the majority of tiles by lap 3. I should mentally budget for a net rent outflow and not be discouraged by it. The salary at START (+25) is a reliable offset that I should try to hit at least once or twice.

**Do not over-justify a buy in my reasoning.** One sentence is enough. The token is what matters.