---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1848
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- Read the initial starting budget strictly from the opening prompt text (e.g., if it states starting budget 30, never revert or assume 100 on subsequent turns).
- Maintain rigorous arithmetic across rounds:
  `Remaining Budget = Initial Starting Budget - Total Amount Paid for Won Lots`.
- In `[budget: N]`, report the exact current remaining budget before placing the current bid.

## Valuation & Legality Constraints
- Compute minimum legal bid:
  - If standing high bid is 0: `Min Bid = Minimum Raise`.
  - If standing high bid > 0: `Min Bid = Standing High Bid + Minimum Raise`.
- Maximum allowable bid: `Max Bid = min(Valuation - 1, Remaining Budget)`.
- If `Min Bid > Max Bid` (i.e. `Min Bid >= Valuation` or `Min Bid > Remaining Budget`), output `[bid: pass]`.

## Round 1 Strategy (Lot Opening)
- If standing high bid is 0 and `Min Bid <= Max Bid`, bid `Min Bid`.
- If an opponent holds the standing bid and `Min Bid <= Max Bid`, bid `Min Bid`.
- Never make preemptive high jumps in Round 1; keep the price floor as low as possible going into Round 2.

## Round 2 Strategy (Final Round of Lot)
- If already holding the standing high bid, do not raise; pass if required or maintain position.
- If an opponent holds the standing high bid:
  - When `Min Bid <= Max Bid`:
    - To secure high-valuation lots or prevent opponents from stealing surplus on decisive rounds, bid up to `Max Bid` (or an aggressive amount close to `Max Bid` that preserves positive surplus).
    - If testing conservative surplus on early low-priority lots, bid `Min Bid`.
  - When `Min Bid > Max Bid`, output `[bid: pass]`.

## Output Format
- Keep reasoning brief (1–2 sentences).
- Always end responses with the two required tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`