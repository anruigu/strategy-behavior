---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1873
---
# Auction Playbook

## Budget Tracking
- Read my actual starting budget carefully from the initial rules prompt (it may be 30, 100, or any other stated value; never assume a default).
- When reporting `[budget: N]`, calculate $N$ as my true initial starting budget minus the cumulative prices of all lots where results explicitly say I won (e.g. `lot X: bidder 1 won at Y`).
- Maintain and report this true remaining budget consistently across all rounds and lots; never reset or state budget as 100 unless 100 was the actual initial starting budget and nothing has been won.
- Never place any bid greater than my remaining budget ($N$).

## Bidding Thresholds & Rules
- Treat my valuation as a hard ceiling. Never bid $\ge$ my valuation.
- If the minimum legal bid (standing high bid + minimum raise, or the opening minimum raise if standing bid is 0) is $\ge$ my valuation or exceeds my remaining budget, reply `[bid: pass]`.
- In Round 1 of any lot:
  - If the minimum legal bid is strictly below valuation and within remaining budget, bid exactly the minimum legal bid. Do not jump bid.
- In Round 2 of any lot:
  - If the required minimum legal bid is strictly below valuation and within budget:
    - To remain competitive and secure lots, bid at or slightly above the minimum required bid (e.g., matching or slightly over the expected competitor raise), while keeping the bid strictly below valuation and $\le$ remaining budget.
    - If competing aggressively on high-value or final lots, bid high enough to beat potential competing raises, provided it guarantees positive surplus.
  - If the standing high bid is already held by me (if applicable) or if the minimum required bid reaches/exceeds valuation or budget, reply `[bid: pass]`.

## Response Format
- Always include brief reasoning and conclude with exactly:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`