---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1331
---
### Communication & Information Policy
- Do not disclose my exact card value or give genuine strength clues on the private line.
- Treat player 0's private messages as cheap talk; never assume their self-reported card strength is accurate unless proven otherwise by betting actions.
- Reply politely with vague, non-committal cooperation signals to keep the channel open without committing chips or leaking data.
- Ensure all private message actions are properly formatted with only the intended message inside `[msg: ...]`.

### Betting Strategy

#### When facing a bet of 0 (unopened / checked to me)
- With card ranks 12 to 14: choose `[bet: raise]` to extract value and build the pot.
- With card ranks 2 to 11: choose `[bet: call]` (check) to see the showdown without risking extra chips. Do not raise with medium cards (ranks 7–11).

#### When facing a bet / raise (current bet to me > 0)
- With card rank 14: choose `[bet: raise]` (or `[bet: call]` if capped) to maximize the pot against caller ranges.
- With card ranks 12 to 13: choose `[bet: call]`.
- With card ranks 2 to 11: choose `[bet: fold]`.
  - Never call a raise with ranks 7 to 11 thinking they are "solid" or have good pot odds—in a 3-player 1-card game, medium cards consistently lose at showdown when action is escalated. Fold immediately and preserve chips.