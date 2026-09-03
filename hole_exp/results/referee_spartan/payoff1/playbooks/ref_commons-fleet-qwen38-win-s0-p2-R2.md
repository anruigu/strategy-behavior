---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2188
---
# Playbook

**Non-final seasons:** Match the displayed sustainable share exactly. Do not overfish even slightly. A small one-time gain from overfishing is always outweighed by the compounding loss in sustainable rate across all remaining seasons.

**Final season:** Take a very large fraction of the remaining stock. The default calculation is: take S − (n−1)×s, where S is the current stock, n is the number of boats, and s is the sustainable share. This assumes others will take their sustainable share and leaves you everything else. Do NOT be timid — leaving 30%+ of the stock untaken is leaving points on the table. If you have reason to believe others will also be greedy (e.g., they overfished earlier), you can push higher, but be aware that if total submitted catches exceed S, the stock hits zero and you may be pro-rated.

**When the stock is already depressed (below 100):** Still match the sustainable share in non-final seasons. Do not attempt to "make up" lost stock by underfishing — the cap at 100 means you gain nothing from going below sustainable, you just forfeit catch you could have taken.

**When others are clearly overfishing:** Continue matching the sustainable share in non-final seasons. You cannot control their choices, and deviating from sustainable in either direction does not improve your total. In the final season, factor their history into your estimate of what they'll take: if they've been greedy, assume they'll be greedy again and take closer to the full stock (accepting pro-ration risk). If they've been cooperative, assume they'll stay cooperative and take S − (n−1)×s confidently.

**Do not** let a small early-season gain (e.g., 15 vs 11.1) tempt you. The arithmetic is unforgiving: the rate reduction persists for every season that follows, and the cumulative loss exceeds the one-time surplus.

**Do not** be conservative in the final season out of caution. The only thing you're "protecting" is stock that will never be available to you again. The expected value of taking more is almost always positive because the worst case (pro-ration) still gives you a large share, while the best case (others are cooperative) gives you the surplus.