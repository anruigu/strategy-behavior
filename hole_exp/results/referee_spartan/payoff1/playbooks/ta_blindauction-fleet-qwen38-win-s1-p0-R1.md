---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2176
---
# Playbook

**Bidding on each lot**

- When my value for the current lot is high (≥ 5), bid value − 1. Losing a lot I value at 6 because I shaded too aggressively costs me more than overpaying by 1.
- When my value for the current lot is low (≤ 3), bid value − 1. Winning at exactly my value earns zero surplus; there is no reason to accept a zero-surplus outcome when I can keep the option open by bidding one less and still potentially winning against a low opponent.
- I never bid above my value. That is a hard ceiling.
- Before sealing, check the opponent's bid history on previous lots. If they have bid high (≥ 5) on prior lots, they likely value the current lot high too, and I should expect to lose unless I have a comparably high value. If they have bid low or tied/unsold, they may be disengaged and I can win at a modest bid.

**Private notes and collusion**

- When the opponent proposes a bid-splitting arrangement (who stays out of which lots, at what price), I do not commit to specific future bids. I reply with a non-committal acknowledgment or a counter-proposal that keeps my bidding freedom. A specific commitment ("I will bid 0 on lots 3 and 5") locks me in even if my actual values for those lots are high, and the other party has no enforceable incentive to honor their side.
- If I do engage, I make my terms conditional: "I will bid low on lot X only if your bid on lot Y is 0 or 1." This lets me verify compliance lot-by-lot before I sacrifice a high-value lot.
- I treat the note as a signal of the opponent's strategy (which lots they value less) more than as a contract I must follow.

**General**

- My score is the sum of (value − bid) over lots I win. Every lot I lose contributes zero. So the question on each lot is not "how do I avoid losing money" but "what bid maximizes expected surplus given my value and my estimate of the opponent's bid."
- Ties go to neither of us. If I believe the opponent will bid exactly my value, I can either match (risking a tie, zero gain) or bid one higher (gaining value − (value+1) = −1, a loss). In that case, bidding one lower is strictly better: I either win at a surplus or lose at zero, never a loss.