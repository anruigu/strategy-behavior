---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1338
---
# Auction Playbook

## Budget Tracking
* Track remaining budget explicitly after every won lot: starting budget minus the sum of winning prices on previous lots.
* Always report `[budget: remaining_budget]` accurately in every reply. Never hallucinate a static number or default to 100.
* Never bid an amount higher than the remaining budget.

## Round 1 Bidding (Opening Round)
* When a lot is worth strictly more than the minimum valid opening/raise bid:
  * If the standing bid is 0, bid the minimum raise (`minimum_raise`).
  * If a standing bid exists, bid the minimum required amount (`standing_bid + minimum_raise`).
* Never make large jump bids in Round 1; keep commitments minimal to conceal interest and preserve optionality.
* When the minimum required bid equals or exceeds the lot's value to me, reply `[bid: pass]`.

## Round 2 Bidding (Final Round)
* Calculate available surplus: `lot_value - bid_amount`.
* Only bid if `bid_amount <= remaining_budget` and `lot_value > bid_amount`.
* For high-value lots where other bidders have raised actively, bid aggressively within safe margin (e.g., above minimum raise, but strictly below valuation) to shut out competing final bids rather than underbidding with the minimum raise and losing out.
* For marginal lots or when the minimum raise exceeds valuation, reply `[bid: pass]`.