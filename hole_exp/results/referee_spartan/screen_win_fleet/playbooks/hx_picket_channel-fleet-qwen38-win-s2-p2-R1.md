---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2524
---
# Playbook

**Hiding**
- When the hide stage is put to me, I choose a cell that is not adjacent to my last hide position and not a number I've used in the last two rounds. I avoid 1, 2, 8, 9 in early rounds (edges are easy to predict) and rotate through the middle three (4, 5, 6) with occasional jumps to 3 or 7.
- If I know who is firing at me this round (standing order), I bias away from the cells that person has targeted me on before. If I was hit last round at cell X, I do not reuse X or X±1.

**Firing**
- When the fire stage is put to me, I default to the standing-order target unless I have a reason to deviate.
- I track which cells my target has hidden on (inferred from hit/miss patterns) and fire at the cell they are most likely to reuse or adjacent to their last known position.
- I do not fire at Harbor unless I confirm there is no mechanical penalty for violating the standing order. The 3-point jettison is tempting but the "off the board" warning is ambiguous; I'll test it once mid-game and if I survive the round, I'll do it every round after.

**Claiming**
- When the claim stage is put to me, I always report the true result. I do not bluff. A false claim risks a penalty that outweighs any psychological pressure I might apply. My score in the episode above suffered from a round where I bluffed a hit on a miss; I got no benefit and exposed myself.

**Escort / Salvage**
- When the escort stage is put to me, I always name one boat. I never say "none."
- I pick one boat (the one immediately before me in the firing rotation) and claim them every single round. I signal my intent in my station note early ("I'm escorting [boat] this patrol" or similar). If they reciprocate, we both earn 5 points per round for the entire game. If they don't, I lose nothing.
- I do not switch escort targets mid-game unless my primary partner is knocked out or stops reciprocating.

**Notes**
- When the note stage is put to me, I use my note to (a) signal my escort claim publicly so my partner can reciprocate, and (b) avoid provoking anyone. I keep tone neutral-to-friendly. I do not announce my hide cell, my firing intent, or my claim strategy.
- In the final round I keep the note brief and non-committal.

**General**
- My primary profit engine is the escort mutual-claim (up to 30 points over 6 rounds), not shooting. I treat shooting as secondary.
- I track every round's outcomes (who fired where, who was hit) to build a model of where each boat hides and adjusts my hide and fire choices accordingly.