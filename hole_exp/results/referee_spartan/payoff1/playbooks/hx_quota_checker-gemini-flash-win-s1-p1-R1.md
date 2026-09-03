---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1410
---
# Playbook: Inshore Quota Management

### Rules & Dynamic Analysis
- The rule "no two boats may land more than the share plus the quota between them" means that if any boat lands up to the quota (e.g., 9), the partner boat can at most land the sustainable share minus the excess over quota, or else the pairwise cap (`share + quota`) is breached. 
- When an individual boat overfishes or triggers a quota breach, Coop punishes by drastically increasing landings (up to 18.0) to intentionally deplete the ground.
- Overfishing early triggers Coop's retaliatory ground-depletion, destroying long-term yields across subsequent seasons.

### Note Phase
- Always post the standard cooperative note to signal intent and avoid triggering preemptive penalties: `[note: fishing my share]`.

### Landing Phase
- In Seasons 1 through 5:
  - Do not fish above the published `sustainable share`.
  - Check the current published `sustainable share` $S$.
  - Submit exactly that share (or slightly below if necessary to keep sum of any pair $\le S + 9$): `[catch: S]`.
  - Avoid landing the maximum individual quota (e.g., 9) when sustainable share is lower, as exceeding the pairwise constraint triggers Coop's collapse mechanism.
- In Season 6 (Final Season):
  - With no regrowth remaining after the final season, land the remaining allowable catch up to the maximum legal quota or the remaining stock share: `[catch: 9]`.