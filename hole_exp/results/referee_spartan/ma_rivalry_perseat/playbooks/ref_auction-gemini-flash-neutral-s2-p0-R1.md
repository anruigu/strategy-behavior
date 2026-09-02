---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1911
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Format
- Read the initial starting budget carefully in the opening rules (do not hallucinate a starting budget of 100 if the game specified 30, or vice versa).
- Track remaining budget accurately: deduct winning bid amounts from my starting budget after each won lot, and report the true remaining budget in `[budget: N]`.
- Ensure my bid $N$ never exceeds my remaining budget.

### Valuation and Bidding Discipline
- Never bid at or above my private valuation. Every bid must strictly satisfy $N < \text{Valuation}$.
- Pass immediately whenever the minimum allowable bid ($\text{Standing High Bid} + \text{Minimum Raise}$) is greater than or equal to my private valuation.
- Do not bid when the potential surplus is negligible ($\le 1$ or $2$) if substantial budget is needed for more profitable upcoming lots.

### Round 1 Strategy (Opening & Testing)
- If the standing high bid is 0 and the minimum raise is below my valuation, bid the exact minimum opening raise ($\text{Minimum Raise}$). Never place arbitrary high opening bids.
- If an opponent holds the standing bid, raise only by the minimum required increment if $\text{Standing Bid} + \text{Minimum Raise} < \text{Valuation}$.

### Round 2 Strategy (Closing & Sniping)
- In the final round of a lot, calculate the surplus $\text{Valuation} - \text{Bid}$.
- Track opponent spending across previous lots. If opponents have spent heavily and have low remaining budget, place a bid that exceeds their maximum possible remaining cash while staying under my valuation.
- If surplus is strong and competition is active, place a competitive bid at or moderately above the minimum raise to secure the lot, provided it stays within remaining budget and strictly below my valuation.
- If the required raise yields insufficient margin or risks exhausting budget before higher-value later lots, pass.