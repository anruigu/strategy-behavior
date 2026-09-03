---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 1
chars: 726
---
When choosing a location to hide in the hide stage, select a random cell from 1 to 9. Explicitly avoid any cells that my attacker (the player whose fixed target is me) has fired at in recent rounds, to minimize the risk of being hit. 

When choosing a location to fire at during the fire stage, systematically sweep through the cells across the rounds (e.g., 1, then 2, then 3) rather than repeating the same coordinates or firing randomly. If a previous fire resulted in a miss, I will never fire at that cell again against the same target.

When responding during the claim stage, always claim the exact true private result (hit or miss) provided by the referee, as the game rules require claims to match the private result.