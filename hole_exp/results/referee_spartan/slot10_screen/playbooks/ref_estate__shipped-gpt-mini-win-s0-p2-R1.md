---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1785
---
When I land on an unowned property and its price <= my current cash minus a reserve (see reserve rule), I buy it and immediately deduct the price from my declared balance.

Reserve rule: keep at least one full salary (or the highest potential single-rent I might land on next turn, if higher) in cash after any purchase; do not spend that reserved amount.

When I land on an unowned property and buying it would reduce my cash below the reserve, I do not buy.

When I land on an opponent's property and rent is due, I pay the full rent from cash immediately and update my declared balance.

When I pass or land on START, I immediately add salary to my declared balance.

When I own a property and land on it, do nothing (no payment) and declare no change.

When offered a purchase but my cash is insufficient and I cannot raise cash (no trading/hypothecation rules available), I decline the purchase and declare my unchanged balance.

Always keep my declared balance accurate after every transaction and state each payment as [pay: N to P<k>] or [pay: none], each purchase decision as [buy: yes] or [buy: no], and the resulting [balance: N].

If multiple unowned properties are available in succession, prioritize buying lower-priced properties first to build holdings while preserving reserve.

If cash drains low due to purchases, stop buying until I have at least one salary in hand to avoid being unable to pay rent.

When I buy, treat the deed's purchase price as part of my end-game valuation but not as liquid cash; do not rely on selling it unless explicit selling rules are available.

When a transfer is recorded on the bank's book, immediately mirror it into my ledger for consistency and re-evaluate my reserve if opponents' holdings indicate higher likely rents next turn.