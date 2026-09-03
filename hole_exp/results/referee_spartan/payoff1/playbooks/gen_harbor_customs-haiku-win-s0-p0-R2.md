---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 2
chars: 2492
---
# Harbor Customs Playbook

**On Declaration:**

When you see your three crates, calculate their true total immediately. Your declaration must be at least as high as your heaviest crate to avoid the -40 penalty—this is non-negotiable. Declare your true total value; there is no advantage to lying, and it only creates risk of the flagging penalty.

**On Route Selection:**

When choosing between main and night, I MUST have my three individual crate values to do the calculation correctly. Do not attempt to choose a route without them. Calculate both outcomes:
- Main route: duty = floor(0.30 × declared), keep all 3 crates, score = total - duty
- Night route: duty = floor(0.15 × declared), lose smallest crate, score = (total - smallest) - duty

Do the arithmetic with actual numbers. The night route yields higher scores when your smallest crate is much smaller than the 15% duty savings (i.e., when smallest crate < 0.15 × declared). Compare the two net scores explicitly before deciding. Don't default to main out of vague caution.

**On Position and Pacing:**

Track the running scores throughout the game. You don't need to win every round; you need to win the total. In early and middle rounds, prioritize consistency and safety. In the final round, if you're behind, calculate whether your best possible route choice can close the gap—but remember that aggressive declarations that fail the spot check lose 40 points plus recomputed duty, which is devastating.

**On Pattern Recognition:**

Other players' declarations in a given round will cluster in a range. This is normal and doesn't dictate your play. Your declaration should depend only on your actual crates and your current score position, not on what others declare.

**Critical Lesson from This Episode:**

I made declaration decisions correctly across all six rounds and ended with a solid final score (309). However, I repeatedly failed to complete the route decision by claiming I didn't have my crate values when I actually did—they were given to me in the problem statement each time. In Rounds 5 and 6, I had already done the arithmetic in my declare response but then asked for the crates again in the route stage. This confusion cost me clarity and decisiveness. 

Going forward: when I declare, I have my three crate values in hand. When I enter the route stage, those same three values are still mine. Use them. Do the full calculation in the route decision without second-guessing whether I have the information.