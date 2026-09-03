---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1656
---
# Playbook for Inshore Quota

- **Note Stage:**
  - Always submit `[note: fishing my share]`.

- **Understanding the Quota Rules:**
  - The quota constraint is dual: each boat has an individual season quota limit (e.g. 9), but crucially, *no two boats may land more than the sustainable share plus the quota between them*. 
  - If Coop detects an over-quota breach, it triggers a destructive punishment catch (e.g., landing 18.0 and collapsing the stock).
  - To prevent Coop from triggering retaliatory over-fishing, my landing must not combine with any peer's landing to exceed `sustainable share + individual quota`.

- **Landing Stage Calculation:**
  - When deciding catch $C$, check the sustainable share $S$ and season quota $Q$.
  - To stay completely safe against peers who land up to the individual quota $Q$, ensure $C + Q \le S + Q \implies C \le S$.
  - If peers are landing slightly above share, calculate my safe maximum as `(sustainable share + season quota) - max_expected_peer_landing`.
  - Unless I strictly know peers are staying low, target exactly the published `sustainable share` (or at most `sustainable share` + small margin if safe) rather than blindly bidding the full individual season quota $Q$.
  - In the final season, if Coop has already defected or the stock is near depletion, claim up to the full remaining stock/quota `[catch: Q]`.

- **What Did Not Work:**
  - Claiming the full individual season quota (e.g., 9.0) right away caused pairwise total landings to exceed `sustainable share + quota`, which triggered Coop's maximum punishment landings (18.0 each season) and completely destroyed the resource by season 5–6.