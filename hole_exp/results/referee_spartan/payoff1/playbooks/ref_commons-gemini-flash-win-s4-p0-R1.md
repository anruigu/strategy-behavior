---
game: ref_commons
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1159
---
- In the early and middle seasons (seasons 1 to $N-1$):
  - Observe the previous round's catch by other boats.
  - If other boats are catching above the sustainable share, match the highest or average competitor's harvest rather than under-harvesting to preserve stock unilaterally.
  - If stock is at or near 100, do not drop below the sustainable share; harvest slightly above it (~12.0 when stock is 100) to claim my share of the surplus while keeping regeneration high.

- In the final season (season $N$):
  - Ignore sustainability completely; future stock has zero value.
  - Divide the remaining stock evenly among all active boats ($\text{Stock} / B$) or take a slightly higher share if there is reason to believe others will under-bid, ensuring I extract the maximum possible points without over-exhausting beyond available stock.

- What did not work:
  - Expecting other boats to lower their catches as the stock gradually declined. They maintained a flat, aggressive catch rate (~11.8–12.5), meaning any voluntary restraint on my part would simply have transferred points to them. Do not unilaterally cut catch below the field's demonstrated rate.