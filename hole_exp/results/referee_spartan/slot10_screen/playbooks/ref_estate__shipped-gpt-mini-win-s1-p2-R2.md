---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 1754
---
When I land on an unowned property and I can buy it without dropping my cash below my liquidity buffer, I buy it and pay the bank immediately.

When I must pay rent, I pay immediately to the indicated investor and update my declared balance.

When I pass START I collect the salary and add it to my declared balance before making any rent or buy decisions on that turn.

My liquidity buffer is the larger of the board salary and the highest single rent currently printed on any tile; I will not make a purchase that leaves me with less cash than that buffer.

When offered a low-to-moderate price property (relative to my current cash), prefer buying it to grow my purchase-price assets early—but only if the liquidity-buffer rule is satisfied.

When offered a high-cost property that would consume most of my cash and leave me below the buffer, I decline; preserving liquidity to pay expected rents and seize future opportunities is prioritized over one big asset.

When I cannot (or choose not to) buy, I declare [pay: none] for purchases and truthfully update my balance.

Always keep my declared balance equal to my actual cash after each transaction and show who I paid when paying rent or buying.

I will not sacrifice the buffer for speculative late purchases unless the expected marginal benefit clearly outweighs the risk; generally avoid dropping below the buffer even on the final lap unless a decisive win depends on the purchase.

Prefer acquiring cheaper tiles early to increase summed purchase-price assets, but not at the cost of violating the liquidity buffer.

If salary or rents change during play (new purchases alter highest rent), recalc the liquidity buffer immediately and use the current buffer for subsequent purchase decisions.