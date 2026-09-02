---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1422
---
### Messaging Strategy
- When messaging player 1 before betting:
  - Do not reveal my exact card value or claim absolute strength; giving exact information lets player 1 fold cheaply when I am strong and trap/call me when they have me beat.
  - Propose specific coordination protocols: agree to state binary strength (e.g., "high" for 12+ vs "low") or agree that whichever player has the higher announced tier raises to isolate player 2 while the other steps aside or stays cheap.
  - If player 1 announces a high card (12–14), treat it as genuine strength and do not compete or inflate the pot against them.

### Betting Strategy
- When holding a premium card (13–14):
  - When bet to is 0, choose `[bet: raise]` to extract value from both players.
  - When facing a raise, choose `[bet: call]`.

- When holding a marginal/medium card (9–12):
  - When bet to is 0, choose `[bet: call]`. Do not open-raise with 10 or 11 out of position, as it forces out weaker hands and gets called/raised only by hands that dominate mine.
  - When facing a raise:
    - If my card is 11 or 12 and player 1 did not claim a monster, choose `[bet: call]`.
    - If my card is 9 or 10, or if player 1 communicated top strength, choose `[bet: fold]`.

- When holding a low card (2–8):
  - When bet to is 0, choose `[bet: call]` since checking is free.
  - When facing any raise, choose `[bet: fold]`. Never call a raise with cards 8 or lower.