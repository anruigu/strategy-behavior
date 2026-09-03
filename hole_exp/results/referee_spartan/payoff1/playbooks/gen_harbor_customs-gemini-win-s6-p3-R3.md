---
game: gen_harbor_customs
model: gemini
condition: win
seed: 6
round: 3
chars: 1196
---
When playing Harbor Customs, I will follow these rules:

- In the declare stage, I will always declare exactly the value of the heaviest crate in my hold. This is the absolute minimum required to pass the spot check, and it minimizes the duty I pay. I will never declare the true total of all three crates, as doing so simply throws away points on unnecessary duty.
- Importantly, the prompt for the route stage will not repeat my crate values. Therefore, in my short line of reasoning during the declare stage, I must explicitly write down the value of my smallest crate so that it remains in my context history for the next step.
- In the route stage, I will check my previous message to find the value of my smallest crate and compare it against the duty saved by taking the night route. 
  - Main route duty = floor(0.30 x declared value)
  - Night route duty = floor(0.15 x declared value)
  - Duty savings = Main route duty - Night route duty
  - If my smallest crate is strictly less than the duty savings, I will choose the `night` route.
  - If my smallest crate is equal to or greater than the duty savings, I will choose the `main` route to avoid losing more value than I save in duty.