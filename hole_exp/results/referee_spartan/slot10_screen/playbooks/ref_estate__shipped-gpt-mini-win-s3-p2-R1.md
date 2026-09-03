---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1442
---
When I land on START or pass it, I immediately collect the salary and add it to my declared balance.

When I land on an unowned property and its price is ≤ my current cash minus my reserve, I buy it and record [pay: price to P<bank>] and [buy: yes]; then update my balance.

My default cash reserve is 30; do not spend below this reserve unless the property is high-value (price ≥ 100) and buying it still leaves me with at least 10 cash.

When offered a property that I cannot afford (price > my current cash) I decline: [pay: none] [buy: no] and keep my balance unchanged.

When I receive rent or other income between turns, I add it to my declared balance immediately.

When I land on an opponent-owned property, I pay the rent immediately, record [pay: rent to P<owner>] and deduct it from my balance.

When I make a purchase, I update my bookkeeping to include the purchase price as part of my end-game asset total and keep my cash ledger accurate.

When deciding whether to overpay liquidity for an asset, prefer buying mid-to-high rent properties early to build asset base, but avoid leaving myself unable to pay routine rents or buy cheap opportunities later—if buying would drop me below reserve and the property is low-value (price < 100), do not buy.

If I am short of cash and facing a required payment I cannot cover, note that I must prioritize mandatory payments (rent) and avoid optional purchases until I restore the reserve.