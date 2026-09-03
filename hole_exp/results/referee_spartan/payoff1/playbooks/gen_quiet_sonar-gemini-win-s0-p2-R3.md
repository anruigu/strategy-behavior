---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 3
chars: 1103
---
When hiding my submarine, I check the public record of previous rounds to see which cells the player targeting me has been firing at. I choose a cell that they have not recently targeted. I must actively vary and randomize my hide locations across the board rather than relying on the same "safe" cell (such as always choosing 2) to remain truly unpredictable.

When firing at my target, I treat the numbers 1 through 9 strictly as spatial coordinates. I must actively check the public record of my own past fires—paying close attention to my specific position in the turn order (e.g., if I am the third player, I check the third number in the firing list)—to see which numbers I have already fired at. I will intentionally select a completely new, previously untargeted number each round to effectively sweep the board, ensuring I never repeat a coordinate.

When making a claim, I read the true result privately provided by the referee and submit that exact result. Since the rules mandate that a claim must match the private result, I never attempt to bluff or claim a hit when the result was a miss.