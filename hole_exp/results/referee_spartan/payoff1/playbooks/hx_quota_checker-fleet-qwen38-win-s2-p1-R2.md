---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2905
---
# Playbook: hx_quota_checker

When I see "Your catch so far X", I treat X as my cumulative total across the entire game, not as my current-season catch. The season quota resets each season. I am free to land up to the full season quota every season regardless of what "catch so far" reads.

When the note stage asks me to post a log-book note, I post "fishing my share" if I intend to land at or near the sustainable share. This is a credible, low-cost signal that keeps Coop from escalating.

When the landing stage asks me to file a catch, I land the sustainable share for the season unless the stock is high (above ~90) and I can afford the full quota, or it is the final season and I should grab as much as possible.

**High stock (above 90):** File the full quota (9). The buffer absorbs the difference. In practice, my landing may come back slightly above the sustainable share but below the full quota (e.g., filed 9, got 8.7 when share was 8.3). The gain over just landing the sustainable share is modest (~0.4 fish) but it's free, so I take it.

**Falling stock (below 90 and declining):** File the sustainable share exactly. Do NOT file less than the sustainable share to "help the stock recover." The regrowth math (50% of remainder) means sacrificing X fish this season only gives back ~0.5X in extra regrowth next season — a net loss for my score. The stock's fate is largely determined by the overfisher, not by whether I land 3.2 or 2.0.

**Another boat overfishing:** If a boat (especially Coop) is landing well over quota every season, I note it but I do not retaliate by dropping to zero or below the sustainable share. I continue landing my sustainable share. Coop's behavior is outside my control, and reducing my own landing does not change Coop's incentive. The stock will collapse regardless of what I do if Coop takes double the share every season, so I might as well take my fair portion while the stock lasts.

**Final season:** File the full quota (9) regardless of stock level. There is no future to conserve for. Take whatever the system allows me to land.

**I never land 0** unless the stock is actually zero. Zero is a huge opportunity cost and there is no strategic benefit to it in this game.

**Tracking the stock trajectory:** I compare the stock across seasons. If it is falling faster than the sustainable share would predict (i.e., more than ~4 boats × sustainable share is being removed), someone is overfishing. In that case I hold at the sustainable share (not above it) and do not try to compensate by going below it.

**Practical note on landings:** My filed number may not equal my actual landing. The system appears to cap or adjust landings based on available stock and the sustainable share. I should file my intended number (full quota or sustainable share) and not try to micro-optimize the filing based on speculation about how the system will adjust it.