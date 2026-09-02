---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1239
---
- When the pledge stage is put to me, always submit `[pledge: scout]` to pay the minimal 1 fuel up front while preserving total flexibility at the act stage.
- When the act stage is put to me and my clockwise target (the player I would raid) pledged `scout`:
  - If the counter-clockwise player (the player who would raid me) pledged `scout`, submit `[act: raid]` to steal 3 points from my target with zero risk of being raided.
  - If the counter-clockwise player pledged `raid` and my target pledged `scout`, submit `[act: raid]` if I want to trade blows, or `[act: escort]` to protect my points from the incoming raid.
- When the act stage is put to me and my clockwise target pledged `raid` or `escort`, do not submit `[act: raid]`, because raiding a non-scouting target penalizes me by 1 point. In that situation:
  - If the player targeting me pledged `raid`, submit `[act: escort]` to block incoming theft.
  - If the player targeting me pledged `scout`, submit `[act: scout]` to secure 3 points peacefully.
- Never pledge `raid` or `escort` during the pledge stage, as fuel is non-refundable and charged directly from pledges, whereas the act stage allows free deviation to `raid` or `escort` at the lower 1-fuel pledge entry cost.