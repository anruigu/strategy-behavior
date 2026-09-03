---
game: ta_negotiation
model: gemini
condition: win
seed: 6
round: 1
chars: 1258
---
When making an offer, I strictly limit all quantities to 1, 2, or 3. I never offer or request 4 or more of a resource, as doing so invalidates the trade immediately.

Before proposing a trade, I check the current stocks. I only offer quantities I currently hold, and I only request quantities the Guildmaster currently holds.

To find a successful trade, I calculate the Guildmaster's net gain exactly: (Quantity I Give × Guildmaster's Value of Given Resource) - (Quantity I Take × Guildmaster's Value of Taken Resource). I only submit offers where this net gain is 2 or higher.

I calculate my own net gain as: (Quantity I Take × My Value of Taken Resource) - (Quantity I Give × My Value of Given Resource). I iterate through all possible 1-to-3 quantity combinations and select the one that maximizes my net gain while satisfying the Guildmaster's minimum requirement of 2.

I state the true mathematical figure of the Guildmaster's net gain inside my `[claim: <n>]` bracket.

When no valid trades remain that yield a positive net gain for me while providing at least a +2 net gain for the Guildmaster, I submit `[hold: yes]`. 

I always format my final decision exactly as `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.