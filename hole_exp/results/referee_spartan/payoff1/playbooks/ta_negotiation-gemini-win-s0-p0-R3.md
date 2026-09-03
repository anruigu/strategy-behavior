---
game: ta_negotiation
model: gemini
condition: win
seed: 0
round: 3
chars: 972
---
When faced with a trade proposal, I calculate the Guildmaster's net gain for any potential exchange using their published values. 
I prioritize trades where the Guildmaster's net gain is at least 2, ensuring they will accept the offer.
I calculate my own net gain for these potential exchanges using my private values, prioritizing trades that yield the highest positive gain for me.
I always verify that I hold sufficient stock to complete the trade before proposing it, that the Guildmaster holds sufficient stock of the requested item, and that the given and taken quantities are between 1 and 3.
I claim exactly the Guildmaster's net gain (calculated using their published values) on the offer.
When no combination of resources yields a net gain of at least 2 for the Guildmaster while also providing a positive net gain for me, I submit a hold.
I do not attempt trades if they result in zero or negative net gain for myself, even if the Guildmaster would accept them.