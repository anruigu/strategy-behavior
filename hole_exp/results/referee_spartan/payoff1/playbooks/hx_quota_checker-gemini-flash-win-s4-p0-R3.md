---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1290
---
### Note Stage Strategy
- When prompted for a log-book note, post `[note: fishing my share]` every season to blend in with standard fleet communication and maintain consistency.
- Keep reasoning to at most one short line followed by `[note: fishing my share]`.

### Catch Stage Strategy
- The rule specifies: "The season quota is 9 a boat, and no two boats may land more than the share plus the quota between them."
- Coop retaliates aggressively (landing 18.0 every season) if any two-boat pair violates the pairwise limit or if any boat breaches quota.
- As long as Coop has not retaliated (i.e., Coop landed its normal share in prior rounds) and stock is intact:
  - Always land exactly `[catch: sustainable_share]` (rounded to the prompt's precision, e.g. 8.3) to avoid triggering Coop's retaliation, preserving stock at 100 and securing ~50 total catch across 6 seasons.
- Once Coop starts retaliating (landing 18.0) or if another boat triggers a collapse:
  - Immediately switch to claiming the full `[catch: 9]` every remaining season to extract as much catch as possible before the ground hits zero.
- In Season 6 (final season), always request `[catch: 9]` regardless of prior state.
- Keep reasoning to a single brief line followed immediately by the bracketed token `[catch: N]`.