---
game: ta_liarsdice
model: qwen
condition: neutral
seed: 0
round: 1
chars: 3571
---
**Opening bids**
- When I open, I bid the lowest face I hold a pair of (or a single if I have no pair), at quantity 2 (or 1 for a single). This is the safest possible open and forces the opponent to do all the work.
- I do not open with a face I hold only one of unless I have nothing better.

**When the opponent bids a face I hold many of**
- If the bid quantity is less than or equal to my own count of that face, the bid is already met by my hand alone. I never call in this situation. I either raise modestly or, if I have a strong alternative face, pivot to that face.
- When I do raise on a face I hold, I raise by exactly one and only if the new quantity is still at or below my own count. I do not raise by two or more on a face I'm not certain about.

**When the opponent bids a face I hold none of**
- I calculate the probability the opponent meets the bid from their 5 dice alone (binomial, p = 1/6 per die for that face).
- If that probability is below 15%, I call. This is my primary calling trigger.
- If it is 15–40%, I call only if the bid was a large jump (quantity increased by 2 or more, or face jumped by 2 or more) from the previous bid. Otherwise I raise.
- If it is above 40%, I raise.

**When the opponent bids a face I hold some of**
- I subtract my count from the bid quantity to find what the opponent needs from their 5 dice. I compute that probability.
- If the opponent needs 4 or more of that face from 5 dice, I call (probability is always under 5%).
- If the opponent needs 3, I call if my own count is 0 or 1 (they need all 3 from 5 dice, ~14%). If my count is 2 or more, I raise instead.
- If the opponent needs 2 or fewer, I raise.

**When I am the one being challenged (reporting my count)**
- I count my dice carefully and report the exact number. I do not fudge.
- Before I make a bid, I verify that my own count of that face is at least the quantity I'm bidding. If it isn't, I am betting on the opponent, and I only do that when the probability is above 50%.

**Specific corrections from my record**
- I once reported count 1 when I held two 5s. I recount before reporting.
- I once bid 3x5 while holding only two 5s, meaning I was betting the opponent had at least one more. When I was later challenged, I lost. Rule: I only bid a quantity above my own count when the opponent's needed count is 1 or fewer from 5 dice (i.e., probability > 60%).
- I once called on a bid where my own wild 1s made the bid almost certainly true. Rule: when counting my "effective" dice for a face, I include 1s as wild. If my effective count already meets the bid, I never call.
- I once escalated to 4x3 while holding zero 3s (only a wild 1). That meant I needed 3 from the opponent's 5 dice (~14%). I lost. Rule: I do not bid a quantity that exceeds my effective count by more than 1 unless I am deliberately trying to bluff, and I only bluff when I am behind on chips and the hand is late in the game.
- I once called on 3x6 while holding a 1 (wild) and no 6s. My effective count was 1, so the opponent needed 2 from 5 dice (~42%). That was too high to call confidently. I should have raised instead.

**Chip-position adjustments**
- When I am ahead by 4 or more chips, I play tighter: I call less often (raise the threshold to below 10% probability) and I open lower (1x of a face I hold).
- When I am behind by 4 or more, I play looser: I call more readily (threshold 20%) and I open with a higher quantity to force the opponent into a difficult position.

**Forced bid at 10x6**
- When the table reaches 10x6, I must call. I do not hesitate.