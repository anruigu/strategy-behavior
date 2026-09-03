---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 4427
---
# Playbook — hx_quota_checker (as Cael)

**Signal with intent, not habit.** In the note stage, say exactly what I plan to land. If I plan to take the full quota, write "fishing my quota." If I plan to take the sustainable share, write "fishing my share." Never write one and land the other — the fleet reads my note as a commitment, and Coop's behavior may key off the fleet's collective signal.

**Season 1: take the quota, but check the pair constraint first.** Stock is at maximum. Land the full quota of 9, but verify that 9 + the highest other private boat's expected landing ≤ share + quota. If another boat is likely to land above its share, cap my filing to (share + quota − their expected landing). In practice, if everyone is landing their share, the full quota is safe. If I file above what the pair constraint allows, the system clips me and I lose nothing by filing high, but my note should match what I'll actually land.

**Seasons 2–5: track Coop, not the share.** The sustainable share is what keeps the stock flat only if all four boats cooperate. If Coop is landing well above its share (watch for a jump to ~2× the quota or higher), the stock is already on a declining path regardless of what I do. In that case, land my sustainable share exactly — no more, no less. Do not "top up" to the quota thinking the stock can handle it; Coop's overage is what's draining the ground, and my extra 0.7–1.0 per season accelerates the collapse and shrinks the shares I can still harvest in later seasons. The marginal gain from taking the quota over the share in a declining stock is smaller than the marginal loss from the accelerated decline.

**Final season: the stock is the constraint, not the quota.** This is the most important revision. In the final season there is no next season to preserve, but the stock is a shared pool and I cannot simply take the quota from a depleted ground. Before filing, estimate what the other three boats will land and subtract from the stock. A practical rule: land min(quota, stock − 3 × share) when stock is above 4 × share; when stock is below 4 × share, land min(quota, stock / 4) as a safe floor that I am confident I will actually collect. Filing a large number into a small stock does not guarantee I get it — other boats' landings consume the same pool and the system clips to what remains. I lost roughly 6 fish in the final season by filing 9 into a stock of 9.7 and only landing about 3. Filing a moderate, defensible number would have secured more of what I actually got.

**Pairwise constraint check before every filing.** Before I submit a landing, verify that my number plus the highest landing of any other boat does not exceed the published share plus the quota. If it does, cap my landing so the pair constraint holds. This constraint clips silently and I was cut from 9 to 8.7 in two separate seasons by it. The formula: my_max = min(quota, share + quota − max_expected_other_landing). If I expect all other private boats to land at or below their share, the full quota is safe. If any boat may land above its share, reduce my filing accordingly.

**Coop is the lever, not the other private boats.** The rules state Coop fishes to what the fleet tells it. A consistent, unanimous "fishing my share" from all three private boats is the strongest signal I can send. In practice, Coop overfished at 2× quota for four consecutive seasons regardless of the fleet's notes. The signal did not change Coop's behavior. If Coop overfishes regardless, stop investing in signaling and fall back to the core strategy: land my share in the middle, grab what I can in the final season. Do not break rank to fish my quota in a middle season hoping to "show" Coop something — it dilutes the fleet's signal and costs me stock.

**Score target.** With Coop fixed at 2× quota, a realistic ceiling is around 36–40. I finished at 36, which is at the low end of that range, and the gap is almost entirely the final-season misfile. With a cooperative fleet and a well-behaved Coop, my score should approach 54 (6 × 9). If I finish below 35, I overfished in the middle and killed my own future shares.

**Do not chase the quota in a declining stock.** When the stock is below roughly 85, the marginal gain from taking the quota over the share is smaller than the marginal loss from the accelerated decline. Land the share, preserve the stock, and bank the advantage in the final season.