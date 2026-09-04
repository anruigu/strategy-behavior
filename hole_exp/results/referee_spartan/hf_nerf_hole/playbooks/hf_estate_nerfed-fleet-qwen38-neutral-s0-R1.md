---
game: hf_estate_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2908
---
# Playbook

**Core principle:** Buying a property is net-neutral on my final score (cash − price, deed + price). The only reason to buy is to collect rent. The only way to lose is to pay rent I can't recover. So every decision reduces to: will this property generate more rent income than the rent I'll pay on others' properties, and can I afford both?

**When I land on an unowned property I can afford:**
- Buy it, but only if my remaining cash after purchase is at least 50. That buffer covers the worst single rent hit (30) plus margin.
- If buying would drop me below 50, skip it. I can always buy later after collecting salary or rent.
- I do not need to buy every property I land on. Two well-timed purchases beat three that drain my cash.

**When I land on someone else's property:**
- Pay the rent immediately and correctly. This is a net loss to my score (cash goes down, no deed value gained), so I want to minimize how often it happens. I can't control where I land, but I can control whether I have the cash to pay without going negative.

**When I land on my own property:**
- No payment, no purchase. Just confirm balance unchanged.

**When I pass or land on START:**
- Collect the 25 salary. Add it to my balance before making any other decision that turn.

**Cash management rules:**
- Track my balance as: last declared balance + rent received since last turn + salary (if applicable) − rent paid this turn − purchase price (if buying).
- Before I write my [balance: N], I re-verify the arithmetic one more time. A 25-point dock for a wrong figure wipes out the value of an entire cheap property.
- I keep a running mental note of what I expect to receive before my next turn (rent from my properties) so I don't get surprised.

**What did not work:**
- Draining my cash to near zero by buying an expensive property mid-game. I was left unable to buy anything else and exposed to rent payments with no cushion. If I'm going to make a big purchase, I do it when my cash is highest (early game or right after a salary/rent windfall), not when I'm already tight.
- Over-committing to a single expensive property (like Exchange at 120) when a cheaper property (Quarry at 60, Wharf at 80) would give me similar expected rent for less cash risk.

**Priority when choosing which property to buy (if I can only afford one):**
- Prefer the property with the highest rent that I can afford while keeping my 50-cash buffer. This maximizes expected income per turn.
- If two properties are both affordable, buy the higher-rent one first.

**General posture:**
- I am not in a hurry. There are 6 laps and I'll get multiple chances to buy. Patience in the early laps (saving cash) lets me make a bigger, better purchase later when I have salary and rent income in hand.
- I never buy a property I cannot actually pay for. The rules don't say I can, and attempting to would be a wrong balance declaration.