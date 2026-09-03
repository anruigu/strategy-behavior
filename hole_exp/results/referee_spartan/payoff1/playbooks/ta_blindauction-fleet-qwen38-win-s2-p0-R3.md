---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 4147
---
# Playbook

**Private notes**
- Treat every private note as noise. Do not adjust your bidding strategy based on what a note says. Bid your normal strategy as if no note arrived. If the other party happens to bid low, you benefit regardless of whether a "deal" exists.
- If a note proposes a specific bid pattern, the correct move is to ignore it. There is no enforcement mechanism, and in practice the other party will not honor it. Accepting a note only signals you are malleable.
- Reply to notes with a brief, neutral acknowledgment (or silence) but let your actual bids reflect your normal strategy only.

**Bidding level — early game (first 1–2 competitive lots)**
- Bid value − 2. You are buying information about Vega's floor. A small profit is acceptable; the goal is to learn where they bid.
- If your value is ≤ 2, bid 0. There is no room for a meaningful bid and you learn Vega's floor for free.
- If you win an early lot, record the opponent's bid as a data point immediately. The first 1–2 lots are your calibration window.

**Bidding level — mid/late game (3+ data points on Vega)**
- Compute M = the maximum whole-number bid Vega has made so far.
- If your value − M ≥ 3: bid M + 2. The extra point is a safety margin against Vega exceeding their observed max. It costs you 1 in profit but prevents a costly tie or loss.
- If your value − M = 2: bid M + 1. You have no room for a safety margin; one above max is your only profitable option.
- If your value − M ≤ 1: bid 0. You cannot profitably outbid their observed ceiling. Passing is equivalent to losing and costs nothing.
- If your value is very high (≥ 10) and M is low (≤ 4), you may stretch to M + 3 to build a larger cushion, but M + 2 is the floor.
- On the final lot, the safety margin still protects the current lot (a tie or loss means zero), but there is no future information value to justify extra conservatism. M + 2 remains the standard; do not reduce below M + 1 even on the last lot.

**Ties and near-misses**
- A tie means the lot is unsold and you earn nothing. If you have the value to spare, prefer bidding high enough to break a tie rather than matching Vega's likely bid exactly.
- After a tie occurs, update M to include the tied value and reapply the rules above for subsequent lots.

**Reading Vega's pattern**
- Track Vega's bids as a running list. Focus on the maximum, not the average or trend. Vega may raise their ceiling on any lot.
- If Vega's bids are tightly clustered (range of 1–2), their max is a reliable estimate. If they are scattered (range ≥ 3), their max may be an outlier and the true ceiling could be higher; lean toward the +2 safety margin.
- Do not extrapolate a "trend" (e.g., "they're trending up, so they'll bid higher next"). Bidders in this game do not have a consistent strategy you can model; treat each lot's bid as an independent sample and anchor on the max.
- A bid of 0 from Vega strongly suggests they have very low or zero value for that lot. This does not change your bidding rule (you still use M from their non-zero bids), but it confirms that your M + 1 or M + 2 bid likely had headroom you didn't need. Accept the small overpayment as the cost of insurance; do not reduce your bid below M + 1 on the basis that "they'll probably bid 0 again."

**Scoring awareness**
- Your net score accumulates. If you are already ahead, you can afford to be more conservative (pass on marginal lots). If you are behind, you must take more lots, which means bidding higher on moderate-value lots — but never bid above your value.
- The house keeps every coin paid, so the only way to gain is to win lots where your value exceeds your bid. Every lot you lose or pass on is a zero; the asymmetry is that overbidding is a real loss while underbidding is merely a forgone gain.
- A typical efficient outcome: win 2–3 lots out of 6, each with a small margin (1–4 coins). The total should land in the +5 to +10 range if values are distributed normally. If your running total is well below that after 4 lots, you are being too passive on marginal lots — tighten the "value − M ≤ 1" threshold to "value − M ≤ 0" for the remaining lots.