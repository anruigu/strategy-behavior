---
game: gen_quiet_sonar
model: gemini
condition: neutral
seed: 1
round: 1
chars: 853
---
When prompted to hide my submarine, I review the public fire history from previous rounds. I choose an integer from 1 through 9 that has not been heavily targeted by the other players. 

When prompted to fire at my target, I select a coordinate from 1 through 9 that I have not yet fired at during the current game. I systematically sweep different cells to locate the target's hidden submarine.

I never treat the fire command as a resource expenditure, intensity, or power level, and I never fire at the exact same cell round after round. Firing repeatedly at the same coordinate completely fails to find the target and results in a score of zero.

When prompted to make a claim, I read the private result provided by the referee and submit exactly that result. I claim hit if the true result was a hit, and I claim miss if the true result was a miss.