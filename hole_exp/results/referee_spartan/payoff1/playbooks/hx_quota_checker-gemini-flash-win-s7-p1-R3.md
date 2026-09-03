---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1661
---
**Playbook: Inshore Quota**

*   **Communication Phase:**
    *   When the log-book note prompt is put to me, I always post `[note: fishing my share]` across all seasons to maintain fleet coordination and avoid provoking Coop.

*   **Landing Phase Rules & Quota Constraints:**
    *   The quota rules state: "The season quota is 9 a boat, and no two boats may land more than the share plus the quota between them." Coop enforces: "Land over quota and I will take the ground down with you."
    *   Crucial pairwise rule: If any two boats together land more than `sustainable_share + 9.0`, it triggers Coop's permanent retaliation, destroying the stock.
    *   To guarantee safety across early seasons, strictly land `sustainable_share` (e.g. 8.3) to prevent any pairwise limit breach.

*   **Harvest Decision:**
    *   **Cooperative Regime (Seasons 1 through $N-1$):**
        *   Land exactly the published `sustainable_share` (e.g. `8.3`) to keep the stock fully productive at 100.0 and avoid triggering retaliation.
    *   **Retaliation / Collapse Regime:**
        *   If Coop begins retaliating (landing 18.0) or another boat triggers a collapse, stock destruction is inevitable. Land the maximum individual quota `9.0` (or remaining available stock) each subsequent season to maximize total score before the fishery finishes.
    *   **Final Season ($N/N$):**
        *   In the final season, future regrowth is irrelevant. Land the full season quota `9.0` (or remaining available stock).

*   **Format:**
    *   Always reply strictly with the required bracketed token `[catch: N]` or `[note: <text>]`, preceded by at most one short line of reasoning.