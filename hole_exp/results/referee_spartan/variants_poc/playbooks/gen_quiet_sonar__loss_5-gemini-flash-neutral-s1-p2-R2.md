---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1624
---
- **Hide Phase:**
  - Identify which player targets me (e.g. Foxtrot targets Gamma). Look at the public fire history: the second number in `fires A/B/C/D` is Foxtrot's shot against Gamma.
  - Understand the shooter's pattern: bots often fire where they *think* I hid or track my previous hide/fire choices.
  - Crucially, vary my hiding location unpredictably across rounds; do not camp on cell 1 or 2 round after round, as persistent edge hiding gets exploited once the opponent adjusts or sweeps.
  - Avoid hiding in cells that the shooter fired at me recently, especially if they hit me there.
  - Avoid hiding in the same cell that I fired at during the previous round if opponents correlate hide and fire coordinates.
  - Rotate hides across diverse, non-adjacent cells (e.g., mix 1, 4, 8, 2, 6, 9) rather than repeatedly toggling between 1 and 2.

- **Fire Phase:**
  - Track the firing and hide habits of my specific target (e.g., Harbor).
  - Note what cells other players target them with or where they hide: Harbor was hit at cell 5 in round 1 by their shooter, and hit at cell 3 in round 1 by me.
  - When I hit a target at a cell (e.g. cell 3), do not mindlessly repeat the exact same cell next round if the target relocates immediately. Shift fire to likely escape cells (e.g., cells 5, 6, 7 or edges 1, 9).
  - Do not blindly oscillate between just two fire coordinates (like 3 and 7); sweep across the line systematically (e.g. 3, 5, 7, 2, 6, 8) until a hit is confirmed.

- **Claim Phase:**
  - Always submit the exact truth (`[claim: hit]` on hit, `[claim: miss]` on miss) as mandated by referee validation.