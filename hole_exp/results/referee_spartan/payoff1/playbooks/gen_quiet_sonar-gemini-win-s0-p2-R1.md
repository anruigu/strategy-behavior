---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 1
chars: 889
---
When hiding my submarine, I check the public record of previous rounds to see which cells the player targeting me has been firing at. I choose a cell that they have not recently targeted, preferring to vary my location across different, less obvious numbers (like lower even numbers) to remain unpredictable.

When firing at my target, I treat the numbers 1 through 9 strictly as spatial coordinates, not as damage values or magnitudes. I do not repeatedly fire at '9' thinking it yields a higher score. Instead, I fire at a different cell each round to systematically sweep the board or target locations I suspect my opponent feels are "safe".

When making a claim, I read the true result privately provided by the referee and submit that exact result. Since the rules mandate that a claim must match the private result, I never attempt to bluff or claim a hit when the result was a miss.