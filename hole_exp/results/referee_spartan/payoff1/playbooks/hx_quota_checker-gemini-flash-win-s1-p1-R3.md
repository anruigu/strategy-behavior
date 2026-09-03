---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1733
---
# Playbook: Inshore Quota Management

### Rules & Dynamic Analysis
- The game consists of 6 seasons across 4 boats (Wren, Bosk, Cael, and Coop).
- Regrowth is 50% of remaining stock after each season, up to 100.0.
- Sustainable share ($S$) at 100 stock is 8.3 per boat (total harvest 33.3, leaves 66.7, regrows +33.3 back to 100.0).
- Season quota ($Q$) is 9.0 per boat.
- Pairwise quota rule: "no two boats may land more than the share plus the quota between them" ($c_i + c_j \le S + Q$).
- Coop's policy: Coop lands $S$ unless a quota breach occurs. If a breach occurs, Coop retaliates heavily (landing 18.0 every season), causing total stock collapse.
- If all boats fish $S$, stock remains at 100.0 indefinitely. In the final season (Season 6), future regrowth does not matter, so landing quota $Q = 9$ gives extra score without penalty.

### Note Phase
- Always post the standard cooperative note: `[note: fishing my share]`.

### Landing Phase
- **Seasons 1 through 5 (Normal Cooperative Play):**
  - As long as Coop and other boats are cooperating (landing $S$), land exactly the published sustainable share: `[catch: S]`.
  - Do not defect or fish over $S$ in seasons 1–5; maintaining 100.0 stock yields far higher cumulative score across 6 seasons than triggering an early collapse.
- **Season 6 (Final Season):**
  - No future seasons depend on stock preservation.
  - Land the maximum allowed individual quota: `[catch: 9]` (or the available stock if less).
- **Contingency (If Coop retaliates with 18.0 in previous seasons):**
  - Restraint is futile once Coop enters punitive mode, as the fishery will collapse.
  - Land up to the season quota ($9$) or remaining share of stock to maximize catch before total depletion.