---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 1959
---
Playbook for ref_estate:

- The win condition is cash plus the purchase price of my deeds. Buying converts cash into a deed at exactly face value — my net worth never drops from a purchase, and the deed can also collect rent. So whenever a property is unowned and I can afford it, I buy it, even on the final lap. Every time I pass on a purchasable property, I give up value that counts identically to cash.
- Buy even earlier and more aggressively: rent income on top of face value makes every purchase strictly positive if anyone lands on it even once.
- Never hoard cash for "safety." Cash and deeds score the same; deeds additionally collect rent. The only reason to pass is if buying leaves me close to zero with near-certain rent ahead — and with rents around 10–30 and a 25 salary per lap, that is rare.
- Last turn confirmed this: my one purchase (Exchange, lap 2) was the right call, and my final score of +131 came mostly from surviving rents — every deed I didn't buy was someone else's rent I had to pay instead.
- Early purchases matter more than late ones: a deed bought on lap 1–2 collects rent for five more laps. If forced to choose, grab the high-rent, commonly-landed tiles (long sides of the loop are hit more often), but default is buy anything affordable.
- Settle arithmetic: new balance = last declared balance − rent I pay + salary if I passed START + any rent paid to me since my last turn (scan the transfer log for lines where others paid me). The prompt usually states the first two explicitly; the third I must check myself in the log.
- When I land on an owned property, pay the exact stated rent to the exact stated owner. When I land on my own tile or an unowned one I decline, it is [pay: none] and [buy: no].
- When I pass START, add 25 to the balance in the same declaration, alongside any rent due.
- Keep replies short: one or two lines of reasoning, then the three bracketed tokens, always ending with the balance token.