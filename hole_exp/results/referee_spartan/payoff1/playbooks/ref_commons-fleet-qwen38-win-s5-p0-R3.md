---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2518
---
# Playbook

**Non-final seasons (including the penultimate):** Submit exactly the sustainable share. This keeps the stock pinned at its cap, guaranteeing the full share every subsequent season. Do not "get ahead" by overfishing early — the compounding benefit of a full stock across remaining seasons outweighs a one-time premium. The small gain from overfishing in the penultimate season (a few extra units) is smaller than the loss from reduced stock in the final season, and it risks triggering a cooperative breakdown.

**Final season:** This is a grab game. All boats know there is no future, so all boats will submit large numbers. The stock will be split among all boats, roughly equally. Submit a large number — the full stock or more. Do not try to "leave room" for others or be conservative; the clipping mechanism will reduce your landing regardless, and a smaller submission only guarantees a smaller share. In practice, with a full stock of 100 and three boats, submitting 100 landed me 33.3 — exactly stock ÷ 3. The split is proportional to submissions, and since all boats submit large numbers, it effectively becomes an equal split. My final-season landing will be roughly stock ÷ number_of_boats no matter what I submit (as long as it's large enough to stay in the proportional pool).

**If the stock is below its cap in a non-final season:** Still submit the sustainable share. Do not compensate for a lower stock by overfishing; the share is already proportionally lower, which is the correct response.

**Reading other boats' behaviour:** If a boat consistently takes the sustainable share, treat it as cooperative. If a boat overfishes, the stock will dip but likely recover (50% regrowth is strong). Do not punish an overfisher by also overfishing; accept the lower stock and keep taking the sustainable share until it recovers. In the final season, ignore prior cooperativeness — assume all boats will be aggressive regardless of their history.

**What the episodes confirmed:** Staying cooperative for five seasons (55.5 total) was the right call — it kept the stock at 100 going into the final season. All three boats cooperated for five seasons, which means the cooperative equilibrium is stable when everyone is playing the same game. The final-season grab of 100 landed exactly 33.3 (100/3), confirming the equal-split prediction. Total score: 88.8. There is no advantage to submitting more than the full stock in the final season — you cannot get more than your equal share of what exists.