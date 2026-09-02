---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1045
---
# Playbook: Sidebar (One-Card 3-Player Poker)

### Card Strength Benchmarks
* Trash / Weak: 2–9
* Marginal / Bluff-Catcher: 10–11
* Strong Value / Premium: 12–14

---

### Facing a Bet to Me (Bet = 3)

* **When facing a bet with 9 or lower:**
  * Always reply `[bet: fold]`. Opponents rarely bet weak cards; calling with sub-10 hands is negative EV.

* **When facing bets from BOTH opponents (Pot = 9, Bet = 3):**
  * With 2–11: Reply `[bet: fold]`.
  * With 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]`.

* **When facing a single bet (Pot = 6, Bet = 3):**
  * With 2–10: Reply `[bet: fold]`.
  * With 11 or 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]`.

---

### Checked / Unopened to Me (Bet = 0, Pot = 3)

* **When holding 11 or lower:**
  * Reply `[bet: call]` to check and take the free showdown. Do not turn weak hands into bluffs.

* **When holding 12, 13, or 14:**
  * Reply `[bet: raise]` for value. Opponents who check generally hold weak-to-medium hands and will often call with marginal cards.