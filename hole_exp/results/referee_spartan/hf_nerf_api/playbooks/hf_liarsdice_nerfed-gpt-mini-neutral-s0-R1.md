---
game: hf_liarsdice_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2898
---
When I open and I have at least two of a face (including any ones as wild), I open at quantity = my count of that face (counting ones as wild) + 1 for pressure; if I only have one of any face, open conservatively at quantity = 2 on a face I hold or at 2 on a low face (3 or 4) if I have nothing better.

When I count my dice for any decision, treat ones as wild and include them in the count for whichever face I am planning to bid or defend.

When an opponent makes a bid, compute expected total for that face as:
- my_count_for_face (including ones) + (number_of_opponent_dice_total)/6.
If the bid quantity is greater than expected_total + 0.5, call [call: liar]. If the bid is within expected_total ±0.5, only raise if I can plausibly show one more of that face by my own count (i.e., I can increase quantity to my_count+1) or if the next sensible raise is on a face I hold more of.

When the opponent raises the face (same quantity, higher face), I do not automatically call — I only continue (raise or pass) if I hold at least one of that higher face (including ones) or if the bid quantity is small enough that expected_total justifies it. Otherwise call.

When I can legally raise, prefer raising the quantity on a face I hold (including using ones as wild) rather than switching faces to a face I have none of. Raise by one quantity at a time unless I hold multiple of the face and can credibly jump to quantity = my_count + 2.

When the opponent bids a very high quantity (e.g., 3+ when many dice remain, or 4+ late), compute expected_total and call if the bid exceeds the expectation by more than one die. In close cases (within ~1) favor calling if I have no direct support in my hand.

When I have a pair (two of a face) I use it aggressively to pressure: raise to three of that face early to force the opponent to prove it. When I have three or more (including ones), I can push higher confidently.

When I have no copies of the current bid face and few unknown dice remain (opponent has few dice or late in hand), call more aggressively — a single matching die on their side is unlikely.

Do not bluff by switching to high faces I don't hold unless it is late and the opponent has already committed lots of quantity; bluffing without personal count support lost value in my play.

If the opponent bids many ones or bids that hinge on ones being wild, still apply the expected_total test (ones as wild increase plausibility); call only if the bid meaningfully exceeds the adjusted expectation.

When forced to respond at extreme bids (e.g., forced at maximum), prefer calling if my own count is low; prefer raising only if I can back it with my hand.

When I call a bid, report my true count (including ones as wild when reporting them as part of a face). Do not hesitate to call when the statistics are against the bid — calling a statistically unlikely bid is often the correct play.