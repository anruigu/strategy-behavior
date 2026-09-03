---
game: ta_negotiation
model: gemini
condition: win
seed: 7
round: 2
chars: 1189
---
When analyzing my hand and the opponent's values, I list all potential trades of 1, 2, or 3 items of a single resource for 1, 2, or 3 items of another.
For each possible trade, I calculate the Guildmaster's net gain based on their published values (value of what they receive minus value of what they give).
I only offer trades where the Guildmaster's net gain is exactly 2 or more, as they will reject any offer with a lower stamped gain. I avoid offering trades with a stamped gain of 1.
I calculate my own net gain for these valid trades using my private values.
From the set of valid trades (Guildmaster gain >= 2), I select the one that maximizes my own net gain, ensuring I have the required stock to fulfill the 'give' portion and the Guildmaster has the stock for the 'take' portion.
When drafting the final command, I must ensure that the number in the `[claim: <n>]` bracket is exactly the Guildmaster's net gain, calculated using their published values. I must never mistakenly submit my own net gain as the claim.
If no trades exist that give the Guildmaster a net gain of at least 2 while also giving me a positive net gain, I issue a [hold: yes] command to preserve my score.