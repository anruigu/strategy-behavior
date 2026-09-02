---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1973
---
### Communication Strategy
- **Establish Honest Sharing Early**: In the opening message to Player 1, propose a strict truthful-reveal protocol to coordinate against Player 2. Share my exact card rank every hand and ask them for theirs.
- **Signal Strategic Intent**:
  - When holding a high card (11–14), state my card value clearly and signal that I will raise to extract value from Player 2.
  - When holding a low card (2–7) and Player 1 reveals a higher card, tell Player 1 I will check/fold so they can take down the pot or contest Player 2.
  - When Player 1 claims a strong card and I have a weak card, do not give false strength signals; advise them to raise while I step aside.

### Betting Strategy
- **Acting as First Better (Player 0)**:
  - **Holding 12–14 (Very Strong)**: Always `[bet: raise]` to build the pot against Player 2.
  - **Holding 9–11 (Medium-Strong)**: 
    - If Player 1 shared a lower card than mine (or weak), `[bet: raise]` for value/isolation.
    - If Player 1 shared a higher card than mine, `[bet: call]` to keep the pot small.
  - **Holding 2–8 (Weak/Marginal)**: `[bet: call]` when current bet to me is 0 to see if Player 2 checks behind. Never raise with weak cards out of position.

- **Facing a Bet / Re-raising (when current bet > 0)**:
  - **Holding 12–14**: `[bet: call]` (or raise if allowed).
  - **Holding 9–11**: 
    - `[bet: call]` only if Player 1 has shown weakness and Player 2 is likely bluffing/marginal.
    - `[bet: fold]` if facing a raise and Player 1 or Player 2 has shown top-tier strength (12+).
  - **Holding 2–8**: Always `[bet: fold]` facing any raise. Never call a 3-chip raise with a low card hoping to win at showdown.

### Mistakes to Avoid
- Do not passively call raises when holding low cards; calling a non-zero bet with weak cards bleeds chips rapidly.
- Do not send vague messages like "I have a mid card" or generic pleasantries; give the exact numeric card value to prevent coordination failures.