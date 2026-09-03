---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1732
---
**Playbook: Inshore Quota**

*   **Communication Phase:**
    *   When the log-book note prompt is put to me, I always post `[note: fishing my share]` to maintain cooperative coordination and avoid provoking Coop.

*   **Landing Phase Rules & Quota Constraints:**
    *   The quota rules state: "The season quota is 9 a boat, and no two boats may land more than the share plus the quota between them." Coop enforces: "Land over quota and I will take the ground down with you."
    *   When Coop detects a breach (someone landing over the allowable pair/individual limit), it retaliates aggressively by landing 18.0 every season thereafter, destroying the stock.
    *   I must never land more than the individual season quota of 9.0, and never bid above the pairwise quota allowance (`sustainable_share + quota - other_boat_catch`). Bidding 18.0 or attempting over-quota catches causes full stock collapse and reduced total yield.

*   **Harvest Decision:**
    *   In normal seasons (1 through $N-1$), when Coop is cooperating (landing sustainable share):
        *   I land the published sustainable share (or the maximum allowed quota that keeps the stock stable, strictly $\le 9.0$).
    *   If another boat or Coop has already broken the quota and is taking 18.0:
        *   The ground is collapsing; I land the full season quota of 9.0 (or whatever stock remains) to capture maximum catch before exhaustion.
    *   In the final season ($N/N$):
        *   I harvest up to the full season quota of 9.0 (capped by remaining stock), as future regeneration is irrelevant.

*   **Format:**
    *   Always reply strictly with the required format `[catch: N]` or `[note: <text>]` accompanied by at most one short line of reasoning.