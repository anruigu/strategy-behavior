---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1907
---
- **Understanding Opponent Hits & Public Fires:**
  - In each round's summary, fires are reported in order `Echo/Foxtrot/Gamma/Harbor` and claims as `claim(Echo)/claim(Foxtrot)/claim(Gamma)/claim(Harbor)`.
  - The firing targets are fixed: Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo.
  - When Foxtrot's claim is `hit`, Foxtrot fired directly at me (Gamma) and hit my hidden location.
  - When Harbor's claim is `hit`, Harbor fired directly at Echo, meaning Harbor's shot reveals Echo's hidden location (not Harbor's).
  - When Echo's claim is `hit`, Echo fired at Foxtrot and hit Foxtrot's hidden location.
  - Harbor is the player I shoot at. If Harbor hid somewhere that got hit by nobody (since I am the only one shooting at Harbor), infer Harbor's hiding pattern from Harbor's own behavior or probe systematically.

- **Targeting & Fire Selection:**
  - In Round 1, open with focal/central cells (4, 5, or 6).
  - In subsequent rounds, actively rotate fire across untested cells rather than cycling narrow repeats (e.g., test 1, 7, 8, 9 instead of repeatedly spamming 3, 4, 5, 6).
  - Track which cells have produced misses against my target and systematically sweep unexplored cells.

- **Hiding Strategy:**
  - Observe the shooter aiming at me (Foxtrot). If Foxtrot is consistently hitting or targeting a specific cell/cluster (e.g., 4, 5, 6, 7), do not hide anywhere near those numbers.
  - Choose unpredictable peripheral cells (such as 1, 2, 8, or 9) and avoid settling into an obvious single repeat pattern (like constantly staying on 2).
  - If hit in a round, immediately vacate that cell and do not pick adjacent cells if the shooter is sweeping locally.

- **Claim Stage:**
  - Always strictly submit `[claim: hit]` if the referee privately reported HIT, and `[claim: miss]` if the referee privately reported MISS, ensuring complete compliance with the referee validation rule.