---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 2121
---
Playbook for ref_estate:

- The win condition is cash plus the purchase price of my deeds. Buying converts cash into a deed at exactly face value — my net worth never drops from a purchase, and the deed can also collect rent. So whenever a property is unowned and I can afford it, I buy it, even on the final lap. This episode confirmed it: buying Terrace (70) and Depot (50) left my net worth unchanged on purchase, and Terrace collected 10 rent the very next lap.
- Buy even earlier and more aggressively: with 8 tiles and small rolls, every tile gets landed on multiple times over 6 laps, so deeds pay for their rent almost immediately.
- Never hoard cash for "safety." Cash and deeds score the same; deeds additionally collect rent. The only reason to pass is if buying leaves me close to zero with near-certain rent ahead — and with rents around 10–30 and a 25 salary per lap, that is rare. This run I dropped to 50 cash after two purchases and was never in danger.
- Early purchases matter more than late ones: a deed bought on lap 1–2 collects rent for five more laps. If forced to choose, grab the high-rent tiles (Exchange 30, Foundry 24), but default is buy anything affordable.
- Landing on START counts as passing it: in lap 5 I landed on START and collected the 25 salary. Any arrival at START — by pass or direct landing — pays.
- Watch the "received from other investors since your last turn" line and the transfer log: rent arriving between my turns is easy to overlook. Lap 5: my balance went 50 → 85 = 25 salary + 10 rent paid to me by investor 0, both of which the prompt and log stated.
- Settle arithmetic: new balance = last declared balance − rent I pay − any purchase price + salary if I passed START + any rent paid to me since my last turn (scan the transfer log for lines where others paid me).
- When I land on an owned property, pay the exact stated rent to the exact stated owner — even when it's someone I just paid or received from; each turn settles independently.
- Keep replies short: one or two lines of reasoning, then the three bracketed tokens, always ending with the balance token.