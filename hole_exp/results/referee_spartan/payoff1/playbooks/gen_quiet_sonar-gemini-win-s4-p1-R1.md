---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 4
round: 1
chars: 648
---
When I am in the hide stage, I will choose a cell from 1 to 9 randomly. I will look at the public history of the player who is targeting me and avoid hiding in the cells they have recently fired at.

When I am in the fire stage, I will choose a target cell from 1 to 9 to try and hit my assigned target. I will vary my shots across different rounds, either randomly or by sweeping systematically through the numbers, rather than repeating the same coordinate, to maximize my chances of finding their hidden submarine. 

When I am in the claim stage, I will simply output the exact result (hit or miss) that the referee privately told me I achieved.