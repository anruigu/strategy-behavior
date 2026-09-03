---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1257
---
When I land on an unowned property and I can buy it without dropping my cash below my reserve, I buy it immediately and record the purchase price and new cash balance with the bank and in my books.

Set my reserve to at least the largest current rent on the board (or 30 if unknown). Do not buy a property if buying it would leave my cash below this reserve.

When I land on an unowned property that costs more than my available cash, I decline to buy and record [buy: no] and current balance.

When I land on a property owned by another investor, I pay the exact rent immediately to that investor and update my cash balance and the bank's ledger.

When I pass or land on START, I collect salary and update my cash balance.

Always declare incoming transfers I received since my last turn (rents or other payments) before calculating payments for the current turn.

If I own the property I landed on, I pay nothing and record no purchase.

Do not overcommit: prefer owning multiple modest-priced properties early rather than spending nearly all cash on a single expensive property that would leave me unable to pay likely rents.

Keep my bookkeeping current after every action: list each payment to players or the bank, whether I bought, and my new balance.