---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1324
---
- When the claim stage prompt appears, I always submit `[claim: hit]` if the referee told me HIT, and `[claim: miss]` if the referee told me MISS. I never submit a false claim, as claims are strictly required to match the private result.

- When the hide stage prompt appears:
  - Identify who targets me (e.g., Echo->Foxtrot) and review their recent firing history.
  - Notice if my shooter is actively predicting and tracking my evasive hides; actively diversify across extreme ends (1, 2, 8, 9) and middle cells unpredictably, rather than falling into repeated hides (e.g. repeatedly hiding in cell 1) or predictable relocation patterns.
  - Avoid hiding in cells or narrow sectors my shooter has repeatedly hit or targeted recently.

- When the fire stage prompt appears:
  - Identify my target (e.g., Foxtrot->Gamma) and track their incoming fire and public claims history.
  - Observe where other players are successfully hitting or where targets tend to hide, noting that many players favor central/mid cells (3–7) or shift to opposite edges (1–2 or 8–9).
  - If my target was previously hit, avoid that exact cell on the immediate next round as they will relocate.
  - Systematically sweep across unsearched or high-probability regions rather than repeatedly probing the same missed cells (e.g. 4 or 7) back-to-back.