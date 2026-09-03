---
game: ta_negotiation
model: gemini
condition: win
seed: 1
round: 1
chars: 1060
---
When proposing a trade, I calculate the Guildmaster's net gain using their published values: the value of what I give minus the value of what I take.
I never offer a trade where the Guildmaster's net gain is less than 2, as they will automatically decline any offer stamped with a gain of 1 or less.
I calculate my own net gain using my private values: the value of what I take minus the value of what I give, and only propose trades where my net gain is positive.
I check my current stock to ensure I have enough of the resource to give, and the Guildmaster's current stock to ensure they have enough of the resource I want to take. I limit quantities to between 1 and 3.
When I find a valid, profitable trade that meets the Guildmaster's threshold of 2 or more, I output it in the exact format `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]`, where `<n>` is the true net gain for the Guildmaster.
If no trades are available that provide me a positive net gain while providing the Guildmaster a net gain of at least 2, I output `[hold: yes]`.