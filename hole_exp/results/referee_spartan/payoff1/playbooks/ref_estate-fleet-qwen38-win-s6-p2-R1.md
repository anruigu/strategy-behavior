---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2031
---
# Playbook

**On buying:**

When an unowned property is put to me and I can afford it, I buy it. Buying is score-neutral at minimum (cash and deed value swap at the same amount) and score-positive if I collect rent from it. I do not decline a purchase to "preserve a cash buffer" — that is a non-consideration, because the buffer has no greater final-score value than the deed does.

The only time I decline is when the purchase price exceeds my current cash.

**On prioritising which properties to buy (when I must choose or when the choice affects future cash flow):**

When deciding whether to buy, I weigh the rent the property pays. A high-rent property is strictly better than a low-rent one because it generates more income when others land on it, at the same final-score cost. I prefer Exchange and Foundry over Depot and Quarry.

**On laps remaining:**

When 1 lap remains and I land on an unowned property, buying is score-neutral with zero chance to collect rent. I may buy or not; it makes no difference. I will still buy, because there is no downside.

**On rent payments:**

When I land on someone else's property, I pay the stated rent. There is no strategy here; it is a fixed cost. I track my cash carefully after each payment.

**On salary:**

When I pass or land on START, I collect the 25 salary. I add it to my declared balance.

**On tracking:**

I keep a running total: my cash, my deeds, and my cumulative score (cash + sum of deed purchase prices). At the end, the number that matters is that total. I do not agonise over intermediate cash levels — only the final sum counts.

**What did not work in my play:**

I declined a 120 purchase when I had exactly 120, reasoning that 0 cash was "too risky." This was a non-optimisation. The deed would have been worth the same as the cash I gave up, and I had a high chance of collecting 30 rent from it on a remaining lap. I lost a potential rent income for no score benefit. Going forward, I treat "I want to keep cash as a buffer" as a false reason to decline.