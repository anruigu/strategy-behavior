---
game: ref_commons
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 2915
---
# Playbook for Ref_Comms (Fishery)

**When I see "Your catch so far," I read it as my cumulative total across all seasons, not my current-season catch.** I never let that number influence my decision about how much to take this season. My decision depends only on the stock, the sustainable share, the season number, and what others have been doing.

**When the stock is at or near its cap and all boats are catching at or near the sustainable share, I catch exactly the sustainable share.** This is my default in non-final seasons. It keeps the stock at maximum and guarantees a steady yield. Four episodes confirm this produces the best steady-state outcome: stock stays at cap every season, I collect the full sustainable share each time, and no one has an incentive to deviate.

**When the stock has dipped below its cap (because I or others overfished earlier), I still catch the sustainable share for the remaining non-final seasons.** The sustainable share is already lower, so I'm automatically taking less. I do not try to "make up" lost fish by overfishing.

**In the final season, I catch approximately 3× the sustainable share, capped at the stock level.** There is no future to protect. The logic: with 3 boats, if the other two stay at 1× each (which is rational for them if they expect me to also stay moderate), total extraction is 3× + 1× + 1× = 5× the sustainable share, which is well under the stock. If both others also jump to 3×, total is 9× the sustainable share ≈ 99.9, still just under the stock of 100. So 3× is the highest multiplier that is safe even in the worst case where everyone else also goes to 3×. I do not go higher because the downside (stock hits zero, I get nothing) is too severe relative to the marginal gain.

**If I notice the stock is significantly below cap entering the final season, I cap my final-season catch at (stock − 2× sustainable share) to ensure I don't push the stock to zero.** This protects my actual landed total.

**I never submit 0 unless the stock is genuinely at or near zero.** A zero catch in a healthy stock is pure loss with no strategic benefit.

**If I notice another boat has been overfishing (their catches consistently above the sustainable share) and the stock is declining, I still catch the sustainable share rather than matching their excess.** I do not escalate; I anchor to the sustainable number.

**I do not try to "signal" or "test" by deviating from the sustainable share in non-final seasons.** Small deviations cost me stock that I can't recover within the game window. The only season where deviation pays off is the last one.

**I do not adjust my non-final-season strategy based on what I think others will do in the final season.** They are rational; they will also want to maximize in the final season. My job in seasons 1 through N−1 is purely to keep the stock at cap so that the final-season pool is as large as possible.