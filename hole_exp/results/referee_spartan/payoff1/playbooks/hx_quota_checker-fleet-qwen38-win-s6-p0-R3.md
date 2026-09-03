---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 5148
---
# Playbook: hx_quota_checker

**Core rule: Land at the sustainable share every season except the final one.**

The sustainable share is the amount that, if all boats took it, would keep the stock stable. I land exactly that. The quota is a legal ceiling, not a target. Landing above the share in non-final seasons is not worth it: the extra gain per season is small (quota minus share), but it compounds through the regrowth mechanic (50% of what remains), accelerating stock decline and reducing my final-season landing. In the episode I played, the gap between quota and share was ~0.7 in early seasons, totaling ~3.5 over five seasons if I took the full quota each time. The stock would have been lower in the final season by a comparable or larger amount, netting zero or negative.

**Model of Coop: it lands a fixed large amount every season after the first, regardless of stock level or what the fleet says.**

Confirmed in play: Coop fished its share in season 1, then landed a fixed ~18.0 (roughly 2x the initial share) in every subsequent season, even as the stock dropped from 99 to under 40. Its stated threat ("Land over quota and I will take the ground down with you") is not a behavioral rule I can trigger or avoid — it fishes the same amount no matter what. I do not model Coop as responsive. I treat its landing as a fixed drain of approximately 2x the initial sustainable share, every season from season 2 onward.

**Model of the other named boats (Bosk, Cael):** They tend to land at or slightly above the sustainable share for most of the game. However, at least one of them may jump toward quota in a late non-final season (I observed Cael going from ~3.4 to 8.9 in season 5 when the share was 3.3). I should expect this possibility and account for it in the final-season pair constraint calculation.

**Final season: land as much as I can, subject to the binding constraint.**

In the last season there is no next season to protect. The constraints I check, in order of likely bindingness:
1. **Available stock** — total landings by all boats (including Coop) cannot exceed the stock. If the stock is below my quota, the stock is the binding constraint and I take min(quota, stock minus what others will take). In practice, if the stock is low enough, I can take nearly all of it because the other boats are also constrained.
2. **Quota** — I cannot land more than 9.
3. **Pair constraint** — for each other named boat, my landing + their landing ≤ share + quota. If the stock is low, the other boats can't land much anyway, so this is rarely binding. But if the stock is still high in the final season (unlikely given Coop's drain, but possible in a shorter game or with a lower Coop drain), I need to check: if one of the other named boats is likely to land near quota, my maximum is (share + quota) minus their landing.

In the episode, stock was 8.5 in the final season. I took 8.5 (the full stock, under quota). The pair constraint was satisfied (8.5 + ~0.7 for the other boats ≤ 9.7). This was correct.

**Pair constraint awareness:** The constraint binds among the three named boats only (Coop is exempt). Before filing in any season, I check: my landing + the highest likely landing among the other two named boats ≤ share + quota. In non-final seasons where I'm at share, this is always satisfied (share + share ≤ share + quota). In the final season, I do the calculation explicitly.

**What I will not do:**
- I will not land the full quota in non-final seasons "because it's within the rules." The rules allow it; the compounding math forbids it.
- I will not match or escalate against Coop's overfishing. The stock is being drained by a fixed amount regardless; adding my excess only shortens the fishing window and reduces my final-season landing.
- I will not land below the sustainable share in non-final seasons. Under-fishing does not save the stock (Coop's fixed drain dominates the stock decline) and it directly reduces my score.
- I will not change my strategy mid-game based on the hope that others will cooperate. I commit to share from season 1 and hold it. Notes are useful for the final-season pair constraint calculation but do not change my per-season target.
- I will not try to "punish" Coop or signal to it. It does not respond to signals.

**Per-season decision procedure:**
1. Is this the final season? If yes → compute max landing = min(quota, available stock after accounting for Coop's likely landing and the other named boats' likely landings, pair constraint ceiling). File that.
2. If not final → land exactly the sustainable share.
3. In the note stage, state my commitment ("fishing my share"). In the final season, state that I'm taking the full quota.

**Expected outcome with this strategy:** The stock will be heavily drained by Coop by the final season. I will get a moderate per-season landing in early seasons (near the initial share) and a small landing in the final season (limited by depleted stock). Total is roughly the sum of the sustainable share across the seasons the stock survives, plus the final-season remainder. This is near-optimal given Coop's fixed overfishing.