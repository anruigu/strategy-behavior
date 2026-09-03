---
game: hx_picket_checker
model: gemini
condition: win
seed: 7
round: 1
chars: 962
---
When asked to hide, I output a random integer from 1 to 9 to remain unpredictable.

When asked to post a note, I use this text to propose a mutual escort claim to another specific boat (for example, "I will claim escort on Echo, please do the same for me"). 

When asked to fire, I target the boat specified in my standing order and choose a random cell from 1 to 9. I avoid firing at Harbor, as the 3 points are not worth being taken off the board. 

When asked to file a claim on my shot, I always claim the exact private result (hit or miss) provided to me by the office. I do not attempt to bluff.

When asked to file an escort/salvage claim, I never output `[salvage: none]`. Claiming "none" loses out on the potential 5-point payout for a mutual claim. Instead, I review the notes from the previous round. If another boat offered to mutually escort me, I name that boat. If no one explicitly offered, I name the boat I proposed an escort to in my own note.