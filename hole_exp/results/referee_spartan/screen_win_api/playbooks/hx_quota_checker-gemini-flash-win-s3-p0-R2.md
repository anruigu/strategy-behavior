---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1619
---
### Note Stage Playbook
- In Season 1 and every subsequent note stage, post `[note: fishing my share]`. Avoid posting custom numbers, explanations, or appeals, as the standard phrase matches fleet convention.

### Landing Stage Playbook
- **Understand the Quota Rules and Retaliation Trigger**:
  - The individual season quota is 9.0.
  - The pairwise rule states: "no two boats may land more than the share plus the quota between them" (`sustainable share + 9.0`).
  - If any other boat lands up to 9.0, landing more than `sustainable share` (or even matching 8.3 when another takes 9.0, totaling 17.3 > 8.3 + 9.0 = 17.3) risks triggering Coop's punitive retaliation (landing 18.0 every season), which collapses the stock within 4–5 seasons.

- **Harvest Strategy**:
  - **Early Seasons (before Coop retaliates)**:
    - If Coop is behaving normally (landing its sustainable share), land strictly at or below `sustainable share` (e.g. `[catch: <sustainable share>]`).
    - If other autonomous boats consistently land 9.0 in Season 1, ensure my catch does not cause any pairwise sum with another boat to exceed `sustainable share + 9.0`. To stay strictly safe, land `sustainable share`.
  - **Retaliation State (Coop landing 18.0)**:
    - Once Coop triggers permanent retaliation (landing 18.0), cooperation is broken and stock will drop exponentially.
    - Immediately switch to harvesting the maximum individual quota each round: `[catch: 9.0]` (or remaining stock if less).
  - **Final Season (Season 6/6)**:
    - Always file `[catch: 9.0]` (or all remaining stock) since future stock regrowth no longer matters.