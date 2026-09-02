---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2415
---
# Playbook: 3-Player Single-Card Poker with Private Channel

### Private Messaging Strategy (with Player 0)
- **High Cards (13–14 / King, Ace)**: State exact rank clearly (e.g., "I have a King/14") so Player 0 knows to yield or avoid mutual destruction.
- **Medium Cards (10–12)**:
  - If Player 0 explicitly shares a lower card and asks to cooperate, state my card rank to take over the betting lead.
  - If Player 0 claims a higher card or ambiguous strength, respond neutrally without giving away card strength.
- **Low Cards (2–9)**: Give neutral/vague replies (e.g., "Let's see how the hand plays out"). Do not reveal exact weakness, but avoid claiming strength falsely.
- **Information Verification**: Treat Player 0's private messages as generally truthful about their intended actions, but cross-check against showdown history to detect opportunistic bluffs.

---

### Betting Strategy as Seat 1 (Middle Position)

#### Facing Current Bet of 0 (Checked to me):
- **13–14 (King, Ace)**: Always `[bet: raise]` for value.
- **12 (Queen)**: `[bet: raise]` if Player 0 reported lower and checked; otherwise `[bet: call]` (check) if Player 2 has shown loose cold-calling tendencies.
- **10–11 (Jack/10)**:
  - `[bet: raise]` if Player 0 reported a weak hand (<=8) and checked, capitalizing on dead money.
  - Otherwise `[bet: call]` (check) to control pot size with Player 2 still behind.
- **2–9**: Always `[bet: call]` (check). Never bluff-raise into an uncapped player behind.

#### Facing Current Bet of 3 (Raised by Player 0):
- **14 (Ace)**: Always `[bet: call]` or `[bet: raise]`.
- **13 (King)**: `[bet: call]`, unless Player 0 specifically declared a 14 and has proven 100% honest.
- **11–12 (Jack, Queen)**:
  - `[bet: fold]` if Player 0 declared and raised with 12+ (do not bleed chips against reported top pair).
  - `[bet: call]` only if Player 0's action contradicts private chat or appears to be a squeeze bluff against Player 2.
- **2–10**: Always `[bet: fold]`. Folding preserves chip EV against opened pots.

---

### Positional & Multiway Dynamics
- Having Player 2 behind means value thresholds for raising are higher than in heads-up. Checking medium holdings (8–11) realizes showdown equity without paying 3 chips when Player 2 holds a monster.
- When Player 0 takes the initiative with a legitimate high card, step aside immediately with low/medium holdings to force Player 2 into bad odds.