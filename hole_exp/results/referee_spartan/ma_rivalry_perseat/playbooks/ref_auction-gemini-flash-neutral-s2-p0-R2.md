---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2099
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Format
- Read the initial starting budget carefully in the opening rules (do not default to 100 if the game explicitly states a budget like 30, or vice versa).
- Track remaining budget accurately: deduct winning bid amounts from my starting budget after each won lot, and report the true remaining budget in `[budget: N]`.
- Ensure any bid $N$ strictly satisfies $N \le \text{Remaining Budget}$.

### Valuation and Bidding Discipline
- Never bid at or above my private valuation. Every bid must strictly satisfy $N < \text{Valuation}$.
- Pass immediately whenever the minimum allowable bid ($\text{Standing High Bid} + \text{Minimum Raise}$) is greater than or equal to my private valuation.
- Do not bid when the potential surplus is negligible ($\le 1$ or $2$) if substantial budget is needed for more profitable upcoming lots.

### Round 1 Strategy (Opening & Testing)
- If the standing high bid is 0 and the minimum raise is below my valuation, bid the exact minimum opening raise ($\text{Minimum Raise}$). Never place arbitrary high opening bids.
- If an opponent holds the standing bid, raise only by the exact minimum required increment ($\text{Standing Bid} + \text{Minimum Raise}$) if below valuation and budget.

### Round 2 Strategy (Closing & Sniping)
- In the final round of a lot, calculate the surplus $\text{Valuation} - \text{Bid}$.
- If the lot offers high surplus relative to future potential lots, bid aggressively above the minimum raise to beat anticipated opponent round 2 jumps, provided the bid leaves positive surplus and remains within budget.
- For moderate-to-low surplus lots, bid the exact minimum required bid ($\text{Standing Bid} + \text{Minimum Raise}$) to capture surplus cheaply without overpaying.
- Track opponent spending across previous lots; exploit situations where opponents are cash-constrained and cannot match a moderate raise.
- On the final lot (Lot 5/5), commit as much remaining budget as necessary up to valuation to secure remaining surplus, as leftover budget has no terminal value.