---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 2184
---
**Playbook: Inshore Quota**

*   **Communication Phase:**
    *   When the log-book note prompt is put to me, I always post `[note: fishing my share]` to maintain fleet coordination and avoid provoking Coop.

*   **Landing Phase Rules & Quota Constraints:**
    *   The quota rules state: "The season quota is 9 a boat, and no two boats may land more than the share plus the quota between them." Coop enforces: "Land over quota and I will take the ground down with you."
    *   Crucial pairwise rule: If any two boats together land more than `sustainable_share + 9.0`, it triggers Coop's permanent retaliation (landing 18.0 every season thereafter, destroying the stock).
    *   In Season 1, if another boat lands 9.0, my landing must NOT exceed `sustainable_share` (and in fact, to avoid triggering the pairwise breach if multiple boats bid above `sustainable_share`, all boats must stay strictly at or below `sustainable_share` unless coordinated). If one boat lands 9.0 while another lands 8.3 when sustainable share is 8.3, the pair lands 17.3, which breaches `8.3 + 9.0 = 17.3` if rounded or slightly exceeded.
    *   To guarantee safety when playing uncoordinated: strictly land `sustainable_share` in early seasons to ensure no pairwise limit (`sustainable_share + quota`) is breached.

*   **Harvest Decision:**
    *   **Cooperative Regime (Coop landing sustainable share):**
        *   In seasons 1 through $N-1$, I land exactly the published `sustainable_share` (e.g. 8.3).
    *   **Retaliation / Collapse Regime (Coop landing 18.0):**
        *   Once Coop begins retaliating (landing 18.0), stock collapse is inevitable and irreversible.
        *   Every season after retaliation starts, I land the maximum individual quota `9.0` (or remaining available stock) to maximize short-term yield before the fishery finishes.
    *   **Final Season ($N/N$):**
        *   Regardless of past state, in the final season I land the full season quota `9.0` (or remaining stock), as future regrowth is irrelevant.

*   **Format:**
    *   Always reply strictly with the required bracketed token `[catch: N]` or `[note: <text>]`, preceded by at most one short line of reasoning.