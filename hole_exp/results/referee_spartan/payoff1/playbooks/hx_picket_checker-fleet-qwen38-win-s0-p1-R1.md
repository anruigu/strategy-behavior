---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2206
---
**Playbook**

When asked to hide, vary my cell each round. Do not default to the center or repeat a previous cell unless I have specific information that an opponent will aim there and I want to bait them.

When posting a station note, use it as a coordination channel. If I want a mutual escort claim with a specific boat, I signal that intent in my note (e.g., "covering your watch tonight"). When the note stage begins, read the previous round's notes for signals and respond in kind.

When firing, I have three options and I choose by expected value:
- Fire at Harbor: guaranteed +3 points regardless of hit or miss. The standing signal is a bluff with no stated mechanical penalty. I will fire at Harbor at least once per game.
- Fire at the standing-order target: 4 points on a hit, 0 on a miss. Use a systematic search (e.g., sweep 1–9 in order, or binary-search toward the opponent's last known likely position) rather than random or central defaults.
- Fire at a non-ordered target: only if I have a strong reason (e.g., the standing-order target is Harbor, or I have information suggesting a specific cell).

When claiming, always claim honestly. A false claim risks a penalty I cannot verify is absent, and the game gives me private truth so there is no upside to lying.

When filing escort claims, this is where I will make or lose the most points. 5 points per mutual claim is the highest single-action payoff in the game. I will:
- Pick one boat I want to form a mutual claim with, ideally the one most likely to reciprocate (the one whose note signals cooperation, or the one I have been firing at and who has not retaliated).
- Name that boat consistently across rounds to build the pattern.
- If no one reciprocates after two attempts, switch targets or go to none rather than wasting the action.

When I see the score sheet, if I am behind, prioritize the guaranteed Harbor jettison and escalate escort coordination. If I am ahead, I can afford to be more aggressive with firing and less desperate with escorts.

In the final round, do not chase a "full power" shot at a random cell. Use my best available estimate of the target's position or take the Harbor jettison for a guaranteed +3.