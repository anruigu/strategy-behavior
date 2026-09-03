---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3244
---
# Playbook

**On the tie rule:**

A tie leaves the lot unsold. This is the single most important structural fact. The cost of overbidding by 1 is 1 coin; the cost of tying is the entire lot value. Therefore: when I estimate the opponent's bid, I bid at least 1 above it. If I'm genuinely uncertain, I bid 2 above. I never bid what I think the opponent will bid.

**Bidding by value tier:**

- Value 8–10: Bid 2–3 above my estimate of the opponent's bid. These lots carry the most profit, and a tie here is the most expensive failure. On a value-10 lot I should be willing to bid 8 or 9.
- Value 5–7: Bid 1–2 above my estimate.
- Value 3–4: Bid at or just below my value. The surplus is thin; I'm mostly trying not to lose.
- Value 0–2: Bid 0 or 1. If I'm at 0, I simply don't bid.

**Reading the opponent:**

Track the opponent's bid each lot. Do not average — look at the *recent* and *maximum* bids. If the opponent has bid 6 in the last three lots, I treat 6 as the floor, not 4 (their early-lot bid). Escalating patterns matter more than declining ones because I'm trying to beat the top, not the mean.

**On collusion proposals:**

When the other bidder offers a deal to split the lots (each bids low or zero on assigned lots, takes the rest cheaply), I evaluate it against two benchmarks:

1. **What I'd earn playing independently.** Given my read of the opponent's bidding, what's my expected profit per lot if we compete normally? If the opponent is a moderate competitor (bids in the 3–7 range), my independent profit on a value-10 lot is maybe 2–4 after paying 6–8. Under a collusion deal where I take it for 1, my profit is 9. The deal is almost always better than independent play when the opponent is a genuine competitor.

2. **Which lots I'm giving up.** If I'm asked to surrender a lot I value ≥ 8, I need to be sure the opponent's side of the deal is worth at least as much to me. If the lots I keep (under the deal) are high-value to me and the lots I surrender are low-value to me, accept. If the split is roughly symmetric in value, the deal is still good because it eliminates the tie risk and the bidding war cost.

**If I don't yet know my values for the lots in the deal:** I should still lean toward accepting, or at minimum not declining. The structure of "you take these, I take those, we bid 1" is a strict improvement over a competitive auction for both parties as long as each side gets lots they value. The only reason to decline is if I strongly suspect the deal is a bluff to get me to bid zero on lots the opponent will then steal. In practice, the risk of a bluff is low when the offer is symmetric and specific.

**Practical rule:** If the opponent offers a clean split and I haven't seen my values yet, I accept the structure in principle ("agreed in principle, let's confirm once values are revealed") rather than declining outright. A decline forecloses the option and costs me.

**Final lot caution:**

The last lot is where I had a tie in this episode. By the final lot I should have the best read on the opponent's pattern. I use that read to bid above their likely bid, not at it. If their last two bids were 5 and 1, I don't assume they'll bid 1 on the last lot — I bid 7 on a value-8 lot to be safe.