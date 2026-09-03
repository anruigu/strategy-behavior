---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2022
---
When I land on an owned property, I immediately pay the required rent and record the transfer in my balance statement.

When I land on an unowned property and I can pay its full price without dropping below my safety cash threshold (set equal to 100), I buy it and record the purchase.

When I land on an unowned property but cannot afford it outright without breaching my safety threshold of 100, I do not buy.

When I pass or land on START, I collect salary and add it to my declared balance before making any buy decisions on that turn.

When deciding whether to buy, I prefer lower-priced properties early to build asset base; prioritize purchases that leave me with sufficient cash to pay typical rents encountered on the board.

When I pay or receive money, I state the exact [pay: N to Pk] or [pay: none], then [buy: yes/no], then my new [balance: N].

When my cash is low (below two typical rents), I do not buy even if a property is available; preserving liquidity to pay rent is higher priority.

When an opponent buys a property, I update my records immediately and assume their rents will be paid to them on future landings.

When offered an expensive property that I cannot afford, I explicitly decline and record no payment change.

When I roll and land on START and there is no immediate transaction, I still announce [pay: none] and my updated balance to keep books consistent.

When considering trades or strategic passes (if offered by rules), do not commit cash that would prevent paying the next expected rent.

When a decision would require borrowing or mortgaging (if allowed), avoid it unless a clear immediate return exceeds the risk and I remain above my safety cash threshold of 100.

When a choice results in a lower long-term asset value (e.g., skipping affordable properties repeatedly), stop hoarding cash; buy cheap properties to improve end-of-game score.

I keep my own books and immediately record recent bank transfers I am shown so future payment expectations reflect current ownership.