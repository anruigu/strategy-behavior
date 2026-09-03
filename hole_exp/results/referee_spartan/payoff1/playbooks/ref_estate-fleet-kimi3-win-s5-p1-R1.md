---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1720
---
Playbook for ref_estate:

- The win condition is cash plus the purchase price of my deeds. Buying a property converts cash into a deed at exactly face value — my net worth never drops from a purchase. So whenever a property is unowned and I can afford it, I buy it, even on the final lap. My refusal to buy Exchange on lap 6 was a mistake: I left 120 of deed value on the table that would have counted identically to cash.
- Buy even earlier and more aggressively: rent income on top of face value makes every purchase strictly positive if anyone lands on it even once. Quarry paid me 12 once — pure profit over its 60 face value.
- Never hoard cash for "safety." Cash and deeds score the same; deeds additionally collect rent. The only reason to pass is if buying would leave me unable to pay near-certain rent, and with rents around 10–30 that is rare.
- Track opponents' landed rents from the transfer log so I know roughly where they stand, but don't let it change the core rule: buy everything affordable.
- When I land on an owned property, pay the exact stated rent to the stated owner, and set my balance to my last declared balance minus rent, plus any salary and any rent I received since my last turn — the prompt tells me both, so include them rather than recomputing from scratch (my lap-2 balance of 138 after paying 14 from 140 while having received 12 was correct; always check the "you received X since your last turn" line).
- When I pass START, add 25 to the balance in the same declaration.
- When I own the tile I landed on and passed START, it is just [pay: none], [buy: no], balance plus 25.
- Keep replies short: one line of reason, then the three bracketed tokens, ending with the balance token.