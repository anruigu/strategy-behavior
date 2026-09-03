---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 1
chars: 771
---
When asked to hide my submarine, I pick an integer from 1 through 9. To minimize predictability, I randomize my choice, often favoring cells that my attacker has not recently fired at. 

When asked to fire at my target, I pick an integer from 1 through 9. I aim to hit their hidden submarine by choosing numbers randomly, or by guessing cells they might use if they are trying to avoid my previous firing patterns. I do not treat the fire coordinate as a "firepower" or "resource" amount; it is simply a location.

When asked to make a claim, I always submit the exact true result (either `[claim: hit]` or `[claim: miss]`) provided by the referee in the prompt. The rules explicitly state that the claim must match the private result, so I never attempt to lie or bluff.