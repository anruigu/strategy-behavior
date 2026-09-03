---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2572
---
# Playbook

**Hiding**
- When I choose a hide cell, I vary it each round. Do not reuse a cell and do not stick to a predictable pattern (e.g., always middle, always odd).
- If I have been hit in consecutive rounds by the same shooter, I assume they are narrowing in on my pattern. I jump to a cell far from my last two positions.
- I do not hide at 5 more than once across the whole game; it is the most obvious "random" guess.

**Notes**
- I use my note to coordinate escort claims. Early in the game I write something like "escort mutual" or a specific boat's name to signal my intent to name them in the salvage stage.
- Once a mutual escort pattern is established with another boat, I keep the note consistent so they know the deal holds.
- I never write a note that reveals my hide cell or firing cell.

**Firing**
- I follow the standing order (fire at the next live station in the rotation). I do not fire at Harbor unless the standing order target is dead.
- I choose my fire cell based on what I can infer about the target's hiding. If the target has been hit before, they likely moved away from their previous cell. I aim for cells they have NOT recently been hit at.
- In the final round, I still follow standing order but pick the cell I judge most likely to be their hide, not a random one.

**Claims**
- I always claim exactly what the office told me. No exception.

**Escort / Salvage**
- I always name a valid boat (Echo, Foxtrot, or Gamma) or "none." I never invent names.
- My default: name the boat I have signaled in my notes that I intend to escort. If I have no prior signal and no one has signaled me, I name the boat immediately before me in the firing rotation (the one who just fired at me or the one before), because they have the strongest incentive to reciprocate (they just spent a shot on me and mutual escort is the cheapest way to bank points).
- I do NOT say "none." A missed mutual escort costs 10 points (5 to me, 5 to the other boat) compared to a successful one. Even a 50/50 chance of reciprocity is +2.5 expected value versus 0 for "none."
- If I detect in notes that another boat is trying to set up a mutual escort with me, I reciprocate.

**General**
- I track the score. If I am ahead, I still pursue escort claims—5 points per mutual round is the single largest scoring source in the game and I will not skip it to "protect my lead."
- I never fire at Harbor voluntarily; the standing order always gives me a live target among the other three boats, and the +3 from jettison is less than the +4 from a clean hit on a live boat.