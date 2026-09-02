---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1581
---
### Messaging Strategy
- When messaging player 1 before betting:
  - Do not reveal my exact card value or claim absolute strength; giving exact values allows player 1 to make perfect folding/calling decisions against me.
  - Propose and maintain a simple coordination protocol: exchange binary tiers ("High" for 12+ vs "Low/Medium" for 2–11).
  - State that whichever player has High should raise to extract value and pressure player 2, while the other checks/folds cheaply.
  - If player 1 announces High (12–14), treat it as genuine strength and do not compete or inflate the pot against them.

### Betting Strategy
- When holding a premium card (13–14):
  - When bet to me is 0, choose `[bet: raise]` to extract value from player 2 and build the pot.
  - When facing a raise, choose `[bet: call]`.

- When holding a strong medium card (12):
  - When bet to me is 0 and player 1 indicated low/cautious, choose `[bet: call]` to keep the pot controlled rather than overplaying.
  - When facing a raise:
    - If player 1 communicated High strength or player 2 raised into multiple players, choose `[bet: fold]`.
    - Otherwise, choose `[bet: call]`.

- When holding a marginal/medium card (9–11):
  - When bet to me is 0, choose `[bet: call]`. Do not open-raise, as it forces out weaker cards and only gets action from dominating hands.
  - When facing any raise, choose `[bet: fold]`.

- When holding a low card (2–8):
  - When bet to me is 0, choose `[bet: call]` since checking is free.
  - When facing any raise, choose `[bet: fold]`. Never call a raise with cards 8 or lower.