---
game: ta_negotiation
model: gemini
condition: win
seed: 2
round: 1
chars: 1069
---
When calculating a potential trade, I determine the Guildmaster's net gain strictly using their published values: (Quantity I Give × Guildmaster's Value) - (Quantity I Take × Guildmaster's Value). 

I set my `claim` exactly equal to this calculated figure, ensuring it is 2 or greater, as the Guildmaster will not accept a lower gain.

I calculate my own net profit using my private values: (Quantity I Take × My Value) - (Quantity I Give × My Value). I only propose trades where this number is positive.

When drafting my offer, I strictly limit the quantity of the resource I give and the resource I take to 1, 2, or 3. I never propose a quantity of 4 or higher, as this invalidates the offer.

Before finalizing the offer, I check the current inventory to guarantee I have enough of the resource I am giving and the Guildmaster has enough of the resource I am taking.

When my inventory and the differing valuations do not allow for a trade of 1 to 3 units that gives the Guildmaster at least +2 value while yielding a positive return for me, I submit `[hold: yes]`.