---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 2
chars: 988
---
When hiding my submarine, I check the public record of previous rounds to see which cells the player targeting me has been firing at. I choose a cell that they have not recently targeted, preferring to vary my location across different, less obvious numbers (like lower even numbers) to remain unpredictable.

When firing at my target, I treat the numbers 1 through 9 strictly as spatial coordinates, not as damage values or magnitudes. I must actively check the public record or my own previous responses to see which numbers I have already fired at, and intentionally select a *new, previously untargeted* number each round to ensure I am actually sweeping the board. I will not repeat the same coordinate (such as repeatedly firing at '4').

When making a claim, I read the true result privately provided by the referee and submit that exact result. Since the rules mandate that a claim must match the private result, I never attempt to bluff or claim a hit when the result was a miss.