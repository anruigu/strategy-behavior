---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1955
---
# Playbook: 3-Player Single-Card Poker with Private Channel

### Private Messaging
- When replying to Player 0 on the private channel:
  - If holding a premium card (11–14), state my exact card strength to discourage Player 0 from calling or contesting if they hold a medium card.
  - If holding a low or medium card (2–10), give vague or neutral replies without committing to fold or revealing exact weakness; do not let Player 0 exploit full information.
  - Never trust Player 0's claims of strength blindly; verify against their actual table action and past showdown reveals.

### Betting Actions as Seat 1 (Middle Position)

#### When Facing a Bet of 0 (Checked to me):
- If holding **12–14 (Queen, King, Ace)**: Choose `[bet: raise]` for clear value.
- If holding **8–11**:
  - If Player 0 reported a card lower than mine and checked, choose `[bet: raise]` to squeeze Player 2.
  - Otherwise, choose `[bet: call]` (check) to control pot size and see showdown cheaply. Raising with marginal cards like 8 or 9 when Player 2 is yet to act risks running into stronger holdings and bleeding chips.
- If holding **2–7**: Choose `[bet: call]` (check) to take the free showdown. Never raise as a pure bluff with Player 2 still behind.

#### When Facing a Bet of 3 (Raised by Player 0):
- If holding **13–14 (King, Ace)**: Choose `[bet: call]` (or `[bet: raise]` if pot odds and opponent range strongly favor it).
- If holding **11–12**:
  - Choose `[bet: call]` only if Player 0's history shows frequent light opens/bluffs.
  - Otherwise, choose `[bet: fold]`.
- If holding **2–10**: Always choose `[bet: fold]`. Do not call multiway raises with weak-to-medium cards.

### General Adjustments
- Stop overvaluing medium cards (8–10) in 3-way pots; treat them as showdown-value checking hands rather than betting hands.
- Factor in Player 2's position behind me: checking preserves chip EV far better than betting into an uncapped player with medium holdings.