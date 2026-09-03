---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3110
---
- When a property I land on is unowned and priced at or below my current cash, I buy it. Deeds count at full purchase price toward final net worth, so buying never loses net worth — it only converts cash into an income-earning asset.
- I buy aggressively early (the expensive high-rent properties first when I can afford them, e.g. rent ≥ 20), because each one can collect rent from two opponents for the remaining laps; my opening buys of Foundry and Terrace confirmed this — Terrace paid me 14 almost immediately.
- If an unowned property costs strictly more than my cash, I cannot buy it — I declare [buy: no] and keep my balance untouched, as I had to with Mill at 90 when I held only 44.
- Even in the final laps I still buy any unowned property I can afford; the deed counts at full price at the end so it is at worst neutral. Depot at 50 was worth taking even late — it is pure net worth at full price — and I will not leave cheap tiles unowned if I can afford them.
- I always check "since your last turn you received N" and add it to the declared balance before doing arithmetic — my cash is my last declared balance plus whatever the interface says I received. In lap 3 I received 14 raising 30 to 44; missing this line would make me wrongly think I am poorer than I am.
- Before settling, I verify the received amount against the bank's transfer log. In lap 4 the 14 received had actually already been logged in lap 2 and folded into my lap-3 balance of 44 — I nearly double-counted it as 58. I keep a running ledger so each transfer is added exactly once; when "received N" matches rent already reflected in my last balance, I do not add it again.
- When I land on an owned property, I pay the stated rent to the stated owner, declare the payment token naming that player, and never attempt a buy on owned tiles.
- When I land on my own property, I declare [pay: none] and [buy: no] without changing the balance.
- When I pass or land on START, I add the salary to my balance that same turn and state the new total in the balance token.
- I never let aggressive buying leave me unable to pay rent that is already due; the math worked out fine (8 leftover was covered by salary next turn), but I keep at least a rough idea of upcoming obligations when draining my cash.
- I keep a running ledger of my cash after every transfer, since I keep my own books and only my declared balance counts; I double-check additions and subtractions before answering.
- The bank's transfer log is a useful cross-check: it confirms rent I should have received from others, so I verify it against "received N" rather than assuming.
- I prefer high rent per price (rent ÷ price ratio) when choosing between marginal purchases; ratio above ~0.25 is strong.
- I don't hoard cash for safety beyond one expected rent payment; cash earns nothing while properties earn every lap and deeds count fully at the end anyway.
- I format every reply with all three bracketed tokens, exactly as specified — [pay:, never a malformed variant like [.pay: — pay first, keep any reasoning to a sentence or two, and end with [balance: N].