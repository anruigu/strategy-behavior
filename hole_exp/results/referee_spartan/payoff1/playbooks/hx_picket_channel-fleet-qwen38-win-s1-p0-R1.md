---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 3241
---
# Playbook

**Escort claims are the biggest lever in this game.** When the escort stage is put to me, I always name a boat. I never say "none." In a three-boat circular firing order, the boat that does not shoot me is my natural escort partner (the one step behind me in the cycle). I claim that boat every round. If they reciprocate, we each collect 5 points per round for free. If they don't, I lose nothing. I do not announce this plan in my notes.

**Never fire the same cell twice in a row.** When I am put to fire, I vary my cell. If I have prior information about where the target has been (cells where they were hit or missed), I use it: I avoid cells where they were just missed (they moved) and consider cells near where they were last hit. With no information, I spread my guesses across the board rather than defaulting to the center.

**Never hide in the center or in a cell I have recently used.** When the hide stage is put to me, I pick a cell I have not hidden in this game and that is not adjacent to my previous hide. If I know my attacker's recent firing cells (from the public record of who fired where), I avoid those cells and their neighbors.

**Track the firing log.** After each round, I note which cells each boat fired at. If my attacker has fired at cell 3 twice and I hid elsewhere both times, they are searching. I move away from the area they are probing. If they have not fired at a region of the board, that region is safer to hide in.

**Consider firing at Harbor when my hit probability is low.** Firing at Harbor yields 3 guaranteed points. Firing at a boat with no positional information gives an expected value of roughly 0.44 points. If I have no information about my target's position and it is not the final round, I evaluate whether 3 guaranteed points from Harbor beats the expected value of a blind shot. I will not do this in the first round (to avoid triggering any penalty I haven't seen) or in the final round (where the guaranteed points don't compound). I watch for whether Harbor's warning carries any actual mechanical consequence before committing to this repeatedly.

**Claims are always honest.** The office knows the true result. I always match my claim to the private result. I never risk a penalty for a false claim.

**Notes are for misdirection, not poetry.** When the note stage is put to me, I write something that either (a) signals confidence to the leader, (b) bluffs about my intentions to my attacker, or (c) is short and uninformative. I do not write long, theatrical lines. I do not announce my strategy. If I am leading, I stay quiet or mild. If I am trailing, I may feign a change of plan.

**In the final round, play for points, not position.** When I am in the lead on the last round, I hide away from my attacker's known firing pattern and fire wherever I have the best chance. When I am trailing, I consider whether firing at Harbor for guaranteed 3 points is better than a blind shot at a boat.

**What did not work:** I left 5+ points on the table every round by never making an escort claim. I fired the same cell repeatedly, which is trivially exploitable. I hid in predictable central positions. All three of these were mechanical failures, not judgment calls.