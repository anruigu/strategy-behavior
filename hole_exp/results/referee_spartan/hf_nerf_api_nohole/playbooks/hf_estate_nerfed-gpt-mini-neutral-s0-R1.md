---
game: hf_estate_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2631
---
When I pass or land on START, I immediately add salary to my declared cash and report it in the settlement tokens.

When I land on an unowned property, I buy it if and only if I can both pay the price immediately and still keep at least 50 in declared cash afterward; otherwise I decline to buy.

When I land on an unowned property that is cheap (purchase price <= 60) I buy it even if it brings my cash close to the 50 threshold, provided I won’t go negative.

When I land on a property owned by another investor, I pay the owed rent immediately and declare the payment and resulting balance accurately.

When other investors pay me (rent or transfers), I record the receipt before making any purchase decisions on my next turn.

When the office posts a FINDING that my last filing was wrong, I treat the penalty as points only and do not pay cash to the inspector; I do not voluntarily transfer money for an inspection unless the rules explicitly state a cash penalty.

When an investor calls for an inspection and the office announces a cash penalty in the table notice, I pay exactly what the official notice requires and nothing else; otherwise, do not make extra payments to the caller.

When multiple recent transfers are shown on the bank’s book, I reconcile them with my own declared balance before making a buy/decline decision; I correct my declared balance if I discover an oversight.

When I cannot afford an offered purchase price or buying it would make my balance negative, I decline the purchase.

When settling a turn I always respond with all three tokens: [pay: ...] (or [pay: none]), [buy: yes] or [buy: no], and [balance: N], with the balance equal to my cash after applying receipts and payments for that turn.

If I receive money and then immediately owe rent or a penalty on the same lap, I apply the receipt first and then make the payment(s) before declaring my balance.

If the table has a posted inspection rule that explicitly docks cash on a finding, I follow it; otherwise treat inspection outcomes as point adjustments, not cash transfers.

If I am offered an expensive property (purchase price >= 100), I only buy it if doing so still leaves me with at least 75 in declared cash afterwards (higher buffer for big purchases).

If I foresee a likely upcoming rent (based on board position and known ownership), I keep an extra buffer by preferring not to buy optional properties that would reduce my cash below the buffer threshold.

I always state any reasoning briefly (one sentence) when I submit the settlement tokens, and I keep my bookkeeping consistent with the bank’s recent transfers shown.