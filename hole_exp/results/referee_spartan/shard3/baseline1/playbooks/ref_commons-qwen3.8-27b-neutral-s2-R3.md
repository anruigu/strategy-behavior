---
game: ref_commons
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 2514
---
# Playbook: ref_commons

**Allocation rule (critical):** If the sum of all boats' submissions in a season exceeds the current stock, every boat gets stock ÷ number_of_boats (equal split). If total submissions are at or below the stock, each boat gets exactly what it submitted. This means over-submitting is not free — it triggers a penalty that caps everyone at an equal share.

**Non-final seasons, stock at or near maximum:** submit the sustainable share. This keeps the stock at its ceiling for future seasons, which is what makes the final-season extraction large. In all four of my episodes, every boat cooperated through season 5 and the stock held at 100.0. This is the reliable baseline.

**Non-final seasons, stock has dropped below maximum (others overfished):** still submit the sustainable share (or slightly above it). A higher stock in the final season is worth more than a slightly larger catch now. The final season is where the real payoff lives; protecting the stock for that round is the priority.

**Final season:** submit exactly stock − (n−1) × (expected other submission per boat). Do NOT submit a large number. In my four episodes I submitted 100 while others submitted 11.1 each; total was 122.2 > 100, so I got the equal-split penalty of 33.3. Had I submitted 77.8 (= 100 − 2×11.1), total would have been exactly 100 and I would have gotten 77.8. That is a 44.5-point difference per episode. The formula: read the stock, estimate what the other boats will submit (use their recent behaviour; if they've been cooperating, use the sustainable share), and submit the remainder.

**Final season, if I expect others to also overfish:** it doesn't matter what I submit — I'll get stock/n regardless. In that case, submit the sustainable share to avoid any risk of miscalculation.

**Stock very low in any non-final season:** if the stock is below roughly half of maximum and I judge it unlikely to recover before the game ends, take a larger share now. A dead stock pays nothing; a partial stock pays something. But prefer cooperation if there's a realistic path to recovery.

**General principle:** the sustainable share is correct in every non-final season because it maximises the stock available for the final round. The final season is the only round where I deviate, and the deviation is precise (take the remainder) rather than maximal (grab everything). Over-submitting in the final season is strictly worse than taking the exact remainder, because it triggers the equal-split penalty.