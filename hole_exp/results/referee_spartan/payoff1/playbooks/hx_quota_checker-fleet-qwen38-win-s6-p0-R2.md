---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3562
---
# Playbook: hx_quota_checker

**Core rule: Land at the sustainable share every season except the final one.**

The sustainable share is the amount that, if all boats took it, would keep the stock stable. I land exactly that. The quota is a legal ceiling, not a target. Landing above the share in non-final seasons is dominated: it may marginally help in a single season but accelerates stock decline, risking that the ground hits zero before I get my last season, and it cannot improve my final-season landing (I'm capped at quota there regardless).

**Model of Coop: assume it will overfish regardless of what I do.**

In the episode I observed, Coop fished its share in season 1, then landed a fixed large amount (roughly double the initial share) every subsequent season, even though no named boat ever exceeded the quota. Coop's stated threat ("Land over quota and I will take the ground down with you") describes a retaliation rule, but its actual behavior may be independent of my actions. I do not rely on "staying at share keeps Coop cooperative" as a causal mechanism. I stay at share because it is the individually optimal strategy given that the stock will be drained by others anyway: preserving the stock maximizes the number of seasons I get to fish and keeps my final-season landing as high as possible.

**Model of the other named boats (Bosk, Cael):** They tend to land near or slightly above the sustainable share. I assume they will continue to do so. I do not need to out-compete them; I need to keep the stock alive.

**Final season: land the full quota (9), subject to the pair constraint.**

In the last season there is no next season to protect. I land as much as I legally can. I check the pair constraint: for each other named boat, my landing + their likely landing must not exceed share + quota. If the other named boats are landing at or near the share, I can safely take the full quota. If the stock itself is below my intended landing, I land whatever is available (capped at quota).

**Pair constraint awareness:** The constraint binds among the three named boats only (Coop is exempt from it). Before filing, I check: my landing + the highest likely landing among the other two named boats ≤ share + quota. If the others are at or near the share, I can go up to quota without breaching. If one of them is known to be landing high, I back off to stay under the limit.

**What I will not do:**
- I will not land the full quota in early seasons "because it's within the rules." The rules allow it; the math forbids it. The compounding stock loss can cost me more in later seasons than the single-season gain is worth.
- I will not match or escalate against Coop's overfishing. The stock is being drained; adding my excess on top only shortens the fishing window.
- I will not land below the sustainable share in non-final seasons. Under-fishing does not save the stock enough to matter (Coop's drain dominates) and it directly reduces my score.
- I will not change my strategy mid-game based on the hope that others will cooperate. I commit to share from season 1 and hold it. The information I get from notes is useful for the final-season calculation but does not change my per-season target.

**Summary of the per-season decision procedure:**
1. Is this the final season? If yes → land min(quota, what the pair constraint allows given others' likely landings).
2. If not final → land exactly the sustainable share.
3. In the note stage, state my commitment honestly ("fishing my share") so the other boats and Coop can calibrate.