---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 1815
---
When I land on an unowned property and I can buy it without my cash after the purchase falling below my reserve, I buy it immediately. If the purchase leaves my cash exactly equal to my reserve, that is allowed. I record the purchase to the bank and update my declared balance.

I set my reserve to at least the largest known rent on the board or 30 if the largest rent is unknown; I will not buy a property if buying it would leave my cash below this reserve.

When I land on an unowned property that costs more than my available cash (including any incoming transfers I have already received and declared since my last turn), I decline to buy and record [buy: no] and my current balance.

When I land on a property owned by another investor, I pay the exact rent immediately to that investor, record the payment, and update my cash balance and the bank ledger.

When I pass or land on START, I collect salary immediately and update my declared cash balance.

I always declare any incoming transfers I received since my last turn before deciding purchases or payments on my current turn.

I keep my bookkeeping current after every action: always output a [pay: N to P<k>] (or [pay: none]), a [buy: yes] or [buy: no], and my new [balance: N]. I note both purchases from the bank and payments to other investors.

I prefer to acquire multiple modest-priced properties early rather than spending nearly all cash on one expensive property that would leave me unable to pay likely rents; do not overcommit cash.

If I already own the property I land on, I do nothing (no purchase) and record no payment unless rent rules otherwise require payment.

When evaluating affordability, include declared incoming transfers and salary collected this turn before deciding whether a purchase is affordable relative to my reserve.