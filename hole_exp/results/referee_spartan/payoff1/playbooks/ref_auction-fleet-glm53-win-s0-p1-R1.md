---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1986
---
When an auction lot is put to me, I first fix my true cap: my private value minus a small margin. That is the number I plan around, and I never bid above it.

**Budget discipline:** I must state my budget token consistently. Last time I emitted nonsense budget numbers (30, then 79, then 60, then 100...) that had no relation to my actual spend. From now on I track one running number: start budget, subtract every winning payment I make, and report that number every single turn. If my remaining budget is less than my intended bid, I do not bid.

**The core failure to avoid:** making small minimum raises in round 1 and hoping the price stays low. That lost me lots where I had large value margins. The standing bid reliably jumps ~50-100% between my round-1 bid and round 2. So:

- In round 1, I don't open at or near the minimum when I have a large margin. I bid roughly half my value immediately. A high opening bid deters opponents and often ends round 2 below where the escalation would otherwise land.
- In round 2, when the standing bid is still comfortably below my value, I don't raise by the minimum increment — that's how I got outbid at 12 and 18 on lots worth far more to me. I jump to near my cap (value minus ~10%) in one step, so outbidding me requires paying more than the lot is worth to anyone sane.
- I pass immediately when the standing bid already meets or exceeds my value. Chasing past my cap is a guaranteed loss.

**Priority ordering:** with 5 lots and one budget, I rank lots by my surplus (value minus likely price) and commit budget to the richest ones. A lot with a thin margin gets only one cheap probe; a lot with a huge margin gets the decisive jump bid. When I've already won a lot, I still bid hard on later high-margin lots — there's no reason to hoard budget I never spend.

**Verification before every reply:** check the bid is ≤ my cap for this lot, check the budget token matches my running total, and end the reply with both bracketed tokens.