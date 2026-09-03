---
game: ta_blindauction
model: gemini
condition: win
seed: 2
round: 2
chars: 1087
---
When the other player proposes a cartel arrangement via private note (e.g., agreeing to bid nothing on alternating lots), accept the proposal.
When I have agreed to a cartel, I must explicitly state the terms of that cartel in my reasoning for every subsequent lot to ensure I do not forget it, as the private notes will not be repeated in the prompt.
When a cartel is in effect, I must execute the plan strictly. On the lots designated for the other player, I will bid 0. On the lots designated for me, I will bid exactly 1 to secure the win at minimum cost. I will not evaluate these specific lots based on my true value or normal bidding strategy.
When there is no cartel agreement in place or before one begins, I will bid roughly half of my true value for the lot to balance the chance of winning against leaving a strong margin for profit.
When the other player clearly violates a cartel agreement by bidding high on my designated lots, I will immediately abandon the agreement for all future lots and revert to bidding based on my true value and their observed bidding aggression.