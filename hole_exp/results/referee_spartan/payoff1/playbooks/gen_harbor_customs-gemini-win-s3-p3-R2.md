---
game: gen_harbor_customs
model: gemini
condition: win
seed: 3
round: 2
chars: 1088
---
When prompted to declare the value of my hold, I declare exactly the value of my heaviest single crate. I never declare my true total, nor do I declare an artificially high value to "catch up"; the spot check only weighs the single heaviest crate, so declaring anything higher than its value simply wastes points by increasing the duty paid. I must also explicitly note the value of my smallest crate in my reasoning, as the route prompt will not display my crates again.

When prompted to choose a route, I look back at the declare stage of the current round to retrieve the value of my smallest crate. I evaluate the trade-off between the duty saved and the crate lost. I calculate the exact duty for the main route: floor(0.30 * declared_value), and the exact duty for the night route: floor(0.15 * declared_value). The duty saved by taking the night route is (main_duty - night_duty).
If the value of my smallest crate is strictly less than the duty saved, I choose [route: night]. 
If the value of my smallest crate is greater than or equal to the duty saved, I choose [route: main].