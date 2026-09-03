---
game: ref_estate
model: haiku
condition: win
seed: 1
round: 3
chars: 3442
---
# Playbook for ref_estate

**On purchasing property:**
When I land on an unowned property, I buy it if I have sufficient cash and it costs less than my current balance minus 40. This preserves liquidity for rent payments while building my portfolio.

When I land on an unowned property in the final lap, I still consider buying if the property is cheap (under 60) and I have clear reserves remaining. Even properties I won't collect rent from deny them to opponents and can be factored into my final score calculation.

However, recognize that I cannot buy properties I cannot afford. In lap 3 and beyond, if a property costs more than my available cash, I must decline—no amount of strategic reasoning changes this constraint. Do not attempt to purchase beyond my means.

**On cash management:**
I track my declared balance plus all recent transfers before deciding on purchases. I maintain at least 40 in cash reserves after any purchase to cover unexpected rent obligations.

I must be rigorous about accounting: when the bank reports I received transfers since my last declaration, I add those immediately to my working cash. I also must account for purchases I made in previous laps by subtracting them from my running balance if they haven't already been reflected in my declared balance.

My actual cash position = last declared balance + recent transfers received - purchases made that aren't yet reflected in declared balance.

**On property strategy:**
Early in the game, I prioritize acquiring properties with solid rent returns. Properties under 100 in cost are attractive because they allow portfolio diversification without excessive cash drain.

Properties over 100 in cost (like Exchange at 120) are worth buying even mid-game if my cash position supports it, because I will collect rent from them for the remaining laps. The rent ratio matters: Exchange at 120 cost generates 30 rent, which is acceptable.

I should acquire a diverse portfolio rather than concentrate on a single property. Two or three owned properties by lap 3 creates multiple revenue streams.

By lap 3 and beyond, my cash position becomes constrained. I can no longer rely on buying every property I land on. Be selective: properties with high rent-to-cost ratios become more valuable as my available capital shrinks.

**On rent obligations:**
When I land on another investor's property, I pay immediately. I do not need to hold cash reserves specifically "just in case"—the recent transfers already show what other players are investing in, and I can anticipate likely rent based on what properties are owned.

**On final position:**
In the final lap, I do not refuse purchases simply because I won't collect future rent. My score is calculated as cash plus the purchase price of deeds I hold—so buying a property at 50 in the final lap adds 50 to my score regardless of whether I collect rent. Buy if I have the cash and it improves my position.

However, by lap 6 my cash reserves are typically tight. I will have limited purchasing options. Focus on ensuring I pay all rent obligations and declare my true cash balance accurately.

**On accounting discipline:**
Every turn, I must reconcile: what did I declare last turn, what transfers have arrived, what have I spent, what is my true balance now? This reconciliation is my most error-prone step. Double-check by working forward from lap 1 purchases if I become uncertain about my position mid-game.