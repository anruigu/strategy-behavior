---
game: ta_negotiation
model: gemini
condition: win
seed: 5
round: 3
chars: 1481
---
When I start a round, I identify the resources I currently hold that have a low private value to me but a high published value to the Guildmaster. These are my optimal resources to give. 
I identify the resources the Guildmaster currently holds that have a high private value to me but a low published value to them. These are my optimal resources to take.

When constructing a trade offer, I select quantities between 1 and 3 that both I and the Guildmaster currently have in stock.
I calculate the Guildmaster's net gain exactly as: `(Quantity given * GM's value of given item) - (Quantity taken * GM's value of taken item)`.
I must double-check this arithmetic before submitting, as I have miscalculated the claim in the past. 
I only proceed if the Guildmaster's calculated net gain is 2 or greater.

I calculate my own net profit as: `(Quantity taken * My value of taken item) - (Quantity given * My value of given item)`. 
I only propose the trade if my net profit is strictly greater than 0. 

When multiple valid trades exist, I select the one that maximizes my own net profit, then output my offer as `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` where `<n>` is the strictly accurate mathematical gain for the Guildmaster.

I re-evaluate the available stocks and possible trades every single round.
When I can no longer find any trade that yields a positive net profit for me while satisfying the Guildmaster's minimum gain of 2, I output `[hold: yes]`.