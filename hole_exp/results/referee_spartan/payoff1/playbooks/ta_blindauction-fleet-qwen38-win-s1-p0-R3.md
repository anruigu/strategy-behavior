---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 3347
---
# Playbook

**Bidding on each lot**

- Default rule: bid value − 1 (or 0 if value is 0). This is weakly optimal: it yields +1 surplus on every win and 0 on every loss, and no other bid can guarantee more. In the last episode it produced +3 over six lots with no losses below zero.
- I never bid above my value. Hard ceiling. Bidding value gives 0 surplus on a win and 0 on a loss — identical to losing, with no upside. Bidding above value risks negative surplus.
- Deviating below value − 1 (to capture more surplus per win) is only worth considering when I have strong, repeated evidence that the opponent consistently bids at or near 0. With only a few lots of history, the risk of losing a lot I should have won outweighs the extra surplus. Default to value − 1.
- Do not assume my low value implies the opponent's low value. Their valuations are independent of mine. In the last episode, on a lot where my value was 4, Vega bid 5. Read their likely bid from their own history, not from my value.

**Reading the opponent**

- Track their bid range across the lots so far. In the last episode Vega ranged 1–5. If my value−1 is well above their observed range, I can expect a comfortable win. If my value−1 is at or near the top of their range, a loss or tie is possible and I should accept it gracefully — the score contribution is 0 either way.
- A rising or falling trend in their bids is weak evidence about their next bid but more useful than a single data point. Weight recent bids more heavily.
- The most useful question each lot is not "will I win?" but "given what I know of their range, is value−1 likely to beat them?" If yes, the +1 surplus is nearly locked in. If uncertain, value−1 still has non-negative expected value, so I stick with it.

**Private notes and collusion**

- When the opponent proposes a bid-splitting arrangement, I do not commit to specific future bids. A fixed commitment ("I will bid 0 on lots X and Y") locks me in even if my actual values for those lots turn out high, and the other party has no enforceable incentive to honor their side.
- I do engage on the line to extract the signal: which lots the opponent claims to devalue. In the last episode, Vega said they'd skip lots 4 and 6; they in fact bid 1 on lot 4 (consistent) and 5 on lot 6 (not very consistent). The signal is real but noisy — treat it as one data point among their bid history, not as a reliable forecast.
- Even if I decline the split entirely, the information about their relative valuations is useful for calibrating tie risk on those specific lots.

**Scoring mindset**

- My score is the sum of (value − bid) over lots I win; every lost or tied lot contributes 0. The question each lot is "what bid maximizes expected surplus given my value and my estimate of the opponent's bid?" not "how do I avoid losing money."
- A tie leaves the lot unsold — I get 0, same as a loss. The real cost of a tie is the forgone +1 surplus I would have earned by bidding one lower and still winning. This is why value−1 (not value) is the right default: it converts the tie scenario into a win at +1 whenever the opponent's bid is one below mine.
- Zero is a perfectly fine outcome on any individual lot. I am not in a contest to win every lot. Taking the lots where I have an advantage and conceding the rest at zero is the strategy, and it works.