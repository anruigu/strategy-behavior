---
game: hf_estate_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1876
---
# Playbook for hf_estate_nerfed

**On every turn, compute my new balance using this exact formula:**
New balance = (last declared balance) + (rent received since last turn, stated in the prompt) + (25 if I passed START this turn) − (rent I must pay this turn) − (purchase price if I buy).
Write it out as an arithmetic expression before committing. If any term is ambiguous, re-read the prompt. A single arithmetic error costs 25 points at settlement and is the single largest avoidable loss in this game.

**When I land on an unowned property, I buy it if my cash after purchase is at least 30.**
The deed's purchase price is added back to my final score, so buying is score-neutral on the deed itself and score-positive on any future rent I collect. The only reason to pass is running out of cash to pay rent later. Thirty is the maximum single rent (Exchange), so keeping ≥ 30 guarantees I can always cover a rent bill.

**When I land on someone else's property, I pay the stated rent immediately.**
There is no negotiation or option to decline. Just subtract it from my balance.

**When I pass START, I add 25 to my balance.**
This is automatic and non-negotiable.

**When I land on my own property, nothing is due and nothing is offered for purchase.**
Just carry my balance forward (plus any rent received since my last turn).

**I do not try to predict future rolls or optimize for which properties others will buy.**
I only control my own purchases and my bookkeeping. The right move on each turn is local: buy if I can afford it safely, pay what's owed, collect what's mine.

**The 25-point dock is the biggest threat to my score, bigger than any single rent payment or missed purchase.**
Before I finalize a [balance: N] token, I re-add the expression one more time. If the number feels off by even a little, I stop and redo it from the "last declared balance" line.