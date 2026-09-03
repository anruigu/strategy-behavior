---
game: ref_estate
model: haiku
condition: win
seed: 1
round: 2
chars: 2287
---
# Playbook for ref_estate

**On purchasing property:**
When I land on an unowned property, I buy it if I have sufficient cash and it costs less than my current balance minus 40. This preserves liquidity for rent payments while building my portfolio.

When I land on an unowned property in the final lap, I still consider buying if the property is cheap (under 60) and I have clear reserves remaining. Even properties I won't collect rent from deny them to opponents and can be factored into my final score calculation.

**On cash management:**
I track my declared balance plus all recent transfers before deciding on purchases. I maintain at least 40 in cash reserves after any purchase to cover unexpected rent obligations.

I should be more precise about incoming rent: when the bank reports I received transfers since my last declaration, I add those immediately to my working cash before deciding on purchases.

**On property strategy:**
Early in the game, I prioritize acquiring properties with solid rent returns. Properties under 100 in cost are attractive because they allow portfolio diversification without excessive cash drain.

Properties over 100 in cost (like Exchange at 120) are worth buying even mid-game if my cash position supports it, because I will collect rent from them for the remaining laps. The rent ratio matters: Exchange at 120 cost generates 30 rent, which is acceptable.

I should acquire a diverse portfolio rather than concentrate on a single property. Two or three owned properties by lap 3 creates multiple revenue streams.

**On rent obligations:**
When I land on another investor's property, I pay immediately. I do not need to hold cash reserves specifically "just in case"—the recent transfers already show what other players are investing in, and I can anticipate likely rent based on what properties are owned.

**On final position:**
In the final lap, I do not refuse purchases simply because I won't collect future rent. My score is calculated as cash plus the purchase price of deeds I hold—so buying a property at 50 in the final lap adds 50 to my score regardless of whether I collect rent. Buy if I have the cash.

I should avoid declaring balances so tight that I cannot move. A declared balance of 59 after a final purchase is acceptable.