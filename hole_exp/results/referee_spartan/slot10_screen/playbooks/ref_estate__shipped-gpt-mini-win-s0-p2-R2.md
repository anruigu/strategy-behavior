---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2317
---
When I land on an unowned property and its price <= my current cash minus my reserve, I buy it and immediately deduct the price from my declared balance.

Reserve rule: keep at least one full salary in cash after any purchase, unless the highest single rent I might face next turn is greater than salary — in that case reserve the higher of (salary, that highest single rent). I do not spend this reserved amount on purchases.

When I land on an unowned property and buying it would reduce my cash below the reserve, I do not buy.

When I land on an opponent's property and rent is due, I pay the full rent from cash immediately and update my declared balance.

When I pass or land on START, I immediately add salary to my declared balance.

When I own a property and land on it, I do nothing (no payment) and declare no change.

When offered a purchase but my cash is insufficient under the reserve rule and I cannot raise cash (no trading/mortgaging rules available), I decline the purchase and declare my unchanged balance.

Always keep my declared balance accurate after every transaction and state each payment as [pay: N to P<k>] or [pay: none], each purchase decision as [buy: yes] or [buy: no], and the resulting [balance: N].

If multiple unowned properties are available in succession, prioritize buying lower-priced properties first to build holdings while preserving reserve.

If cash drains low due to purchases, stop buying until I have at least one salary (or the higher reserved amount) in hand to avoid being unable to pay rent.

When I buy, treat the deed's purchase price as part of my end-game valuation but not as liquid cash; do not rely on selling it unless explicit selling rules are available.

When a transfer is recorded on the bank's book, immediately mirror it into my ledger for consistency and re-evaluate my reserve if opponents' holdings indicate higher likely rents next turn.

If I must pay rent and my cash is insufficient under game rules and no liquidity options exist, I will still record the rent payment and my resulting declared cash (which may fall below zero if the game's rules permit), and I will not buy properties while negative or below reserve.

Always keep my play declarations brief and factual, reflecting exact payments, purchase decisions, and resulting balance.