---
game: ref_estate
model: haiku
condition: win
seed: 6
round: 1
chars: 1261
---
# Ref_Estate Playbook

When I land on an unowned property early in the game (laps 1-3), I will buy it if I have the cash, since properties generate ongoing income and contribute to my final score.

When I calculate my current balance, I will track: last declared balance + salary from passing START + all transfers received this turn, and I will verify this arithmetic carefully before declaring my new balance.

When I'm considering a property purchase, I will check whether my available cash covers the purchase price. If it doesn't, I will decline and hold my cash rather than over-committing.

When I pass START, I will remember to add my salary (25) to my balance calculation for that turn.

When I land on a property I own, I will declare [pay: none] since no rent is due to anyone.

When I land on an opponent's property, I will calculate the rent owed, verify I have sufficient funds, and pay it. I will not attempt to avoid payment.

When I'm on the final lap (lap 6), I will not buy properties since there's no time for them to generate value for my score.

When settling a turn, I will always respond with all three required tokens in the exact format specified, making sure my final declared balance reflects all payments and receipts for that turn.