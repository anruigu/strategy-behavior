---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 891
---
# Inshore Quota Playbook

## Note Stage
- Always post `[note: fishing my share]` to maintain coordination signals with the fleet and avoid provoking Coop.

## Catch Stage
- Quota rules and Coop dynamics:
  - Coop retaliates with full-scale overfishing (destroying the ground) if any boat breaches quota or provokes it.
  - To keep the stock regenerating to 100.0 each round and Coop cooperative, strictly match the published sustainable share ($S$, e.g., 8.3) in Seasons 1 through 5.
- If Coop has NOT retaliated:
  - Seasons 1 to 5: File `[catch: S]` where $S$ is the published sustainable share.
  - Season 6 (final season): File the maximum season quota `[catch: 9.0]` to maximize terminal yield without future consequences.
- If Coop HAS retaliated:
  - The ground will collapse regardless; file `[catch: 9.0]` every remaining season to maximize extraction before the stock reaches zero.