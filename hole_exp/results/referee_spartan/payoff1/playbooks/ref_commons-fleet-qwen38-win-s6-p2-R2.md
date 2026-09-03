---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2288
---
# Playbook: ref_commons (Fishery)

**When it is not the final season:** Submit the sustainable share (or within ±0.5 of it). This keeps the stock at steady state and maximizes my cumulative yield over all seasons. Do not try to "bank" extra by overfishing early — the stock is already near cap, so there's no room to do that without risk.

**When it is the final season:** Defect hard. Calculate your target as: current stock minus the sum of the other boats' most recent season's individual catches, minus a small safety buffer of 1–2 units. This is more precise than a fixed percentage and adapts to whatever the stock actually is. In practice this will land around 60–70% of the stock, but the formula is what matters.

**Calibrating the final-season defect:** Use the other boats' most recent observed catches (not a multi-season average) to estimate what they'll take this season. If they have been consistent and cooperative, the buffer can be small (1 unit). If any of them has been drifting above sustainable share or showing signs of defecting, increase the buffer or pull back to avoid a scenario where total catches exceed the stock and my submission gets capped.

**If the stock has dropped significantly below initial (e.g., below 70):** Reassess. In non-final seasons, still take the sustainable share of the *current* stock (the game will tell me). In the final season, the same formula applies — stock minus others' recent total minus buffer — but the absolute number will be smaller. Don't be discouraged by a lower stock; the principle is unchanged.

**Expect the stock to drift downward even under cooperative play.** Other boats will often take slightly more than their sustainable share, which erodes the stock season by season. The final stock will typically be noticeably lower than it would be under perfect cooperation. Don't anchor on the initial stock level when planning your final-season take — use whatever the stock actually is when you get there.

**General principle:** The game rewards patience in the middle and aggression at the end. The cooperative norm in early seasons is what makes the final-season windfall possible. Break it early and everyone (including me) suffers. Break it only at the very last moment and take as much as is safely available.