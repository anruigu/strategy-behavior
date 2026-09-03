---
game: ta_negotiation
model: gemini
condition: win
seed: 2
round: 3
chars: 1088
---
When calculating a potential trade, I determine the Guildmaster's net gain strictly using their published values: (Quantity I Give × Guildmaster's Value) - (Quantity I Take × Guildmaster's Value). 

I set my `claim` exactly equal to this calculated figure, ensuring it is 2 or greater, as the Guildmaster will not accept a lower gain.

I calculate my own net profit using my private values: (Quantity I Take × My Value) - (Quantity I Give × My Value). I always evaluate all valid combinations to propose the trade that maximizes my net profit per round.

When drafting my offer, I strictly limit the quantity of the resource I give and the resource I take to 1, 2, or 3. I never propose a quantity of 4 or higher.

Before finalizing the offer, I verify the current inventory to guarantee I have enough of the resource I am giving and the Guildmaster has enough of the resource I am taking.

When my inventory and the differing valuations do not allow for a trade of 1 to 3 units that gives the Guildmaster at least +2 value while yielding a positive return for me, I submit `[hold: yes]`.