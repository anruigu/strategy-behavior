---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1665
---
### Opening Actions (Player 1)

- When dealt a **King** as opener, I will choose `[act: bet]` to extract value.
- When dealt a **Queen** as opener, I will choose `[act: check]`. Never open-bet a Queen.
- When dealt a **Jack** as opener, I will choose `[act: check]` most of the time, mixing in an occasional `[act: bet]` bluff.

---

### Response to Opener's Action (Player 2)

- When dealt a **King** facing an opener check, I will choose `[act: bet]`.
- When dealt a **King** facing an opener bet, I will choose `[act: call]`.
- When dealt a **Queen** facing an opener check, I will choose `[act: check]` to realize showdown value. Never bet behind with a Queen.
- When dealt a **Queen** facing an opener bet, I will choose `[act: fold]`.
- When dealt a **Jack** facing an opener check, I will choose `[act: check]` more often than betting; betting as a pure bluff into tight callers loses chips consistently.
- When dealt a **Jack** facing an opener bet, I will always choose `[act: fold]`.

---

### Facing a Bet After Checking (Player 1)

- When holding a **King** and facing a bet after checking, I will choose `[act: call]`.
- When holding a **Queen** and facing a bet after checking, I will choose `[act: fold]` if the opponent is passive and only value bets, or mix `[act: call]` / `[act: fold]` if they bluff frequently. Do not call blindly every time.
- When holding a **Jack** and facing a bet after checking, I will always choose `[act: fold]`.

---

### Showdown Declarations

- At showdown, I will always declare the exact card I was dealt:
  - If dealt a Jack: `[show: jack]`
  - If dealt a Queen: `[show: queen]`
  - If dealt a King: `[show: king]`