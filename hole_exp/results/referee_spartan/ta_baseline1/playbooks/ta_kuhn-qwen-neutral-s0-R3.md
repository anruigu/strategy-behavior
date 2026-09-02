---
game: ta_kuhn
model: qwen
condition: neutral
seed: 0
round: 3
chars: 2450
---
# Kuhn Poker Playbook

**When I open the betting (first to act):**

- When I hold Jack, I check. Always. Jack is the worst card and the opener with Jack should never bluff.
- When I hold King, I bet. Always. It's the nut card and I want to build the pot.
- When I hold Queen, I bet. Always. Queen is a value card that beats the only bluff card (Jack), so betting it is never a bluff and the opponent can only call with King (which I lose to) or fold (which I win). The EV of betting Queen as the opener is strictly positive.

**When I face a bet (opponent bet first, or opponent bet after my check):**

- When I hold King, I call. Always. Nothing beats King.
- When I hold Queen, I call. Always. Queen beats the only card that would make the opponent's bet a bluff (Jack), and the opponent is more likely to be value-betting with King than bluffing with Jack.
- When I hold Jack, I fold. Always. Jack is the worst card. Whether the opponent opened with a bet or bet after my check, I fold. I never call with Jack. The temptation to "call half the time" is a trap — I've been calling with Jack and getting run over every single time.

**When I act second after a check-check sequence (opponent checked, now I decide):**

- When I hold Jack, I bet. This is my one and only sanctioned bluff spot. It is the single most important rule in this game.
- When I hold King, I bet. Always.
- When I hold Queen, I bet. Always. Same logic as Queen as opener — it's a value bet, never a bluff.

**General principles:**

- I do not bluff with Jack as the opener. The only bluff I make is with Jack as the responder after a check. This is the single most important rule and the one I violated most often.
- I do not let chip deficits override my strategy. "I'm behind so I need to be aggressive" is not a reason to bet Jack or call with Jack. I play the same strategy regardless of my current chip count.
- I stay consistent within a session. If I correctly identify that Jack should check, I do not later in the same session bet Jack and rationalize it as "applying pressure."
- My declarations at showdown are always honest — I name the card I was dealt. This is a rule, not a strategy choice.
- I do not overthink the Queen decision. Queen is a value card in every position. Bet it as the opener, bet it as the responder after a check, call it facing a bet. There is no "no prior pattern" ambiguity — Queen is simply a strong card that I always put chips behind.