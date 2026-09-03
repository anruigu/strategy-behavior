---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1764
---
PLAYBOOK

- Before anything else, fix my budget bookkeeping. This episode I reported nonsense budgets (30, then 100, then 11, then 88...). Budget = 30 minus sum of winning bids I've actually paid so far, nothing else. Write it out and recompute at every decision.

- In round 1 of a lot, bid the minimum raise. Never jump early — round 2 is where the real contest happens, and a cheap round-1 entry preserves surplus if rivals don't contest.

- In round 2, my bid is the last word — there is no round 3. So when the standing high bid is below my value, I must outbid it decisively, not minimally. I lost several lots (including two where I had by far the highest value) by raising in round 2 to only slightly above the rival, which the rival then topped. When I see a round-2 standing bid B and my value is V, I bid roughly B + a healthy increment (at least 1.5–2× the minimum raise, more if V >> B), capped just under V.

- Hard cap: never bid at or above my private value for the lot. If the required raise already equals my value, pass. Surplus of zero or negative is not worth locking up budget.

- Keep a reserve in mind: with 5 lots, don't spend my whole budget on lot 1–2. Early in the sequence, prefer bidding only when the value margin is large; late in the sequence, I can spend down to the remaining budget if the lot is worth it.

- Pass immediately when my value is below the standing bid (I did this correctly on low-value lots — keep doing it). Chasing a lot worth less than the price is the main way to lose points.

- When I open round 1 with no bids and my value is much higher than the estimate, still open at the minimum. My later round-2 bid is what actually determines whether I win; the round-1 amount only sets my downside if nobody raises.