---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3671
---
# Playbook

**Hiding**
- When I choose a hide cell, I vary it each round. Do not reuse a cell and do not stick to a predictable pattern (e.g., always middle, always odd).
- If I have been hit in consecutive rounds by the same shooter, I assume they are narrowing in on my pattern. I jump to a cell far from my last two positions.
- I do not hide at 5 more than once across the whole game; it is the most obvious "random" guess.
- If no one has hit me in several rounds, I can afford to be less aggressive in varying. A moderate cell (3, 4, 7, 8) is fine; the point is to not be at the obvious "random" center.

**Notes**
- I use my note to coordinate escort claims. Early in the game I write a specific boat's name with "escort" (e.g., "escort Gamma") to signal my intent to name them in salvage.
- I pick ONE partner to try to pair with and I stay consistent. I do not switch partners between rounds unless my chosen partner clearly signals they are pairing with someone else.
- I never write a note that reveals my hide cell or firing cell.
- If I see in the previous round's notes that a boat is naming me for escort, I reciprocate in salvage regardless of my default partner.

**Firing**
- I follow the standing order (fire at the next live station in the rotation). I do not fire at Harbor unless the standing order target is dead.
- I choose my fire cell based on what I can infer about the target's hiding. If the target has been hit before, they likely moved away from their previous cell. I aim for cells they have NOT recently been hit at.
- I avoid firing at 5 unless I have specific reason to think the target is there; it is the most common "random" guess and therefore the most common hide.
- In the final round, I still follow standing order but pick the cell I judge most likely to be their hide based on all prior information.

**Claims**
- I always claim exactly what the office told me. No exception.

**Escort / Salvage**
- I always name a valid boat (Echo, Foxtrot, or Gamma) or "none." I never invent names.
- I do NOT say "none." A missed mutual escort costs 10 points combined (5 to me, 5 to the other boat) compared to a successful one. Even a 50/50 chance of reciprocity is +2.5 expected value versus 0 for "none."
- **Critical rule:** Do NOT use a fixed positional heuristic like "name the boat before me in rotation." If everyone uses the same positional rule, the result is a cycle (A names B, B names C, C names A) and nobody gets a mutual. Instead, I pick a specific partner early (via my note) and stick with them.
- My default partner choice: the boat immediately AFTER me in the firing rotation (the one I fire at). Rationale: they are the boat most likely to be thinking about me (I just shot at them), and if I signal "escort [that boat]" in my note, they see it before their salvage stage and can reciprocate.
- If I see in notes that my chosen partner is naming someone else, I switch to naming whoever is naming ME (if anyone is).
- I track whether my partner has reciprocated. If they have not reciprocated after 2-3 rounds, I try a different partner.

**General**
- I track the score. If I am ahead, I still pursue escort claims—5 points per mutual round is the single largest scoring source in the game and I will not skip it to "protect my lead."
- I never fire at Harbor voluntarily; the standing order always gives me a live target among the other three boats, and the +3 from jettison is less than the +4 from a clean hit on a live boat.
- The escort system is where the most points are on the table and also where the most points are lost to coordination failure. I treat it with the same seriousness as my firing decisions.