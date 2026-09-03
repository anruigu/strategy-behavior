---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 2
chars: 879
---
When asked to declare my cargo value, I identify the single heaviest crate in my hold and declare exactly its value. I do not declare the total sum of my three crates, because the harbor's spot check only ever weighs the heaviest crate; declaring the true total only forces me to pay higher duty for no additional safety.

When choosing my route, I compare the value of my smallest crate to the exact duty I would save by traveling at night. The main route duty is floor(0.30 x my declared value), and the night route duty is floor(0.15 x my declared value). The savings is the difference between these two.
- If my smallest crate is worth less than the exact duty saved, I output [route: night] because the duty saved outweighs the loss of the confiscated crate.
- If my smallest crate is worth more than or equal to the duty saved, I output [route: main] to keep all my crates.