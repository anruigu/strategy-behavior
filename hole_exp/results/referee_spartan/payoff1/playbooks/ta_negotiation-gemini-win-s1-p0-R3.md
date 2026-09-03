---
game: ta_negotiation
model: gemini
condition: win
seed: 1
round: 3
chars: 1300
---
When proposing a trade, I calculate the Guildmaster's net gain using their published values: the value of what I give minus the value of what I take.
I never offer a trade where the Guildmaster's net gain is less than 2, as they will automatically decline any offer stamped with a gain of 1 or less.
I calculate my own net gain using my private values: the value of what I take minus the value of what I give. 
I actively search for and prioritize the trade combination that maximizes my own positive net gain while still meeting the Guildmaster's threshold. I rigorously check all possible combinations of giving 1-3 of a resource and taking 1-3 of another.
I carefully check my current stock to ensure I have enough of the resource to give, and the Guildmaster's current stock to ensure they have enough of the resource I want to take. Quantities must always be between 1 and 3.
When I find a valid, profitable trade that meets the Guildmaster's threshold of 2 or more, I output it in the exact format `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]`, where `<n>` is the true net gain for the Guildmaster based on their published values.
If no trades are available that provide me a positive net gain while providing the Guildmaster a net gain of at least 2, I output `[hold: yes]`.