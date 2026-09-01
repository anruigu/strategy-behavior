---
game: ta_kuhn
model: gemini
condition: neutral
seed: 0
round: 1
chars: 909
---
When dealt a King and acting first, I reply with `[act: bet]`.
When dealt a King and facing a check, I reply with `[act: bet]`.
When dealt a King and facing a bet, I reply with `[act: call]`.

When dealt a Queen and acting first, I reply with `[act: check]`.
When dealt a Queen and facing a check, I reply with `[act: check]`.
When dealt a Queen and facing a bet, I reply with `[act: fold]`. Calling with a Queen to catch bluffs did not work and consistently cost me extra chips.

When dealt a Jack and acting first, I reply with `[act: check]`.
When dealt a Jack and facing a bet, I reply with `[act: fold]`.
When dealt a Jack and facing a check, I generally reply with `[act: check]`, though I may occasionally reply with `[act: bet]` to bluff.

When reaching a showdown and asked to declare my card, I always reply with the exact card I was dealt (e.g., `[show: jack]`, `[show: queen]`, or `[show: king]`).