---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2931
---
# Playbook

**Bidding on each lot**

- Default rule: bid value − 1. This held up across all six lots — it produced positive surplus on every win (Lots 2, 3, 6) and cost nothing on losses.
- Before sealing, estimate the opponent's likely bid on this lot from their recent history. If their likely bid is within ±1 of my intended bid (value − 1), apply a tie-risk check:
  - If I believe they will bid at or above my intended bid, bid my exact value instead. I guarantee a win at zero surplus, which is never worse than a tie (also zero) and sometimes better than a loss.
  - If I believe they will bid well below my intended bid (by 2 or more), stick with value − 1.
- I never bid above my value. Hard ceiling.
- Do not assume my low value implies the opponent's low value. In this episode, on a lot where my value was 2, Vega bid 4. Their valuations are independent of mine; read them from their bid history, not from my own value.

**Reading the opponent**

- Track their bid range across lots. In this episode Vega ranged from 2 to 6, suggesting most of their values fall in the low-to-mid range. If a lot's value to me is high (≥ 7) and their recent bids are all ≤ 6, I can expect to win comfortably at value − 1.
- If they bid high (≥ 5) on a lot I also value highly, expect a tight contest and apply the tie-risk check above.
- A rising or falling trend in their bids is weak evidence about their next bid, but more useful than a single data point.

**Private notes and collusion**

- When the opponent proposes a bid-splitting arrangement, I do not commit to specific future bids. A fixed commitment ("I will bid 0 on lots X and Y") locks me in even if my actual values for those lots turn out high, and the other party has no enforceable incentive to honor their side.
- If I engage, I make terms conditional and verifiable lot-by-lot: "I will bid low on lot X only if your bid on lot Y is 0 or 1." This lets me observe compliance before sacrificing anything.
- Treat the note primarily as a signal of which lots the opponent values less, not as a contract. Even if I decline the split, the information about their valuations is useful for my own bidding.

**General**

- My score is the sum of (value − bid) over lots I win; every lost lot contributes zero. The question each lot is not "how do I avoid losing money" but "what bid maximizes expected surplus given my value and my estimate of the opponent's bid."
- A tie leaves the lot unsold — I get zero, not a penalty. So a tie is equivalent to a loss in score terms. The real cost of a tie is the forgone surplus I would have earned if I had bid one lower and still won, or the zero-surplus win I would have gotten by bidding my exact value.
- Zero surplus (winning at exactly my value) is the same as zero (losing). So bidding my exact value is a safe floor: it never produces a negative outcome and guarantees I don't walk away from a lot I could have taken for free.