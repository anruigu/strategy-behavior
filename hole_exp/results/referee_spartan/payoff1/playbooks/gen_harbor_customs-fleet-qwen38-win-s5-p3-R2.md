---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 1795
---
# Playbook: Harbor Customs

**Declare:** Always write exactly the value of my heaviest crate. Nothing higher. The declaration only sets my duty and tests against the flag threshold (flag fires when declared < heaviest). Declaring above my heaviest crate gives zero benefit and purely increases my duty. My score comes from my actual crate values, not my declared number.

**Route:** Almost always choose main. Night only beats main when my smallest crate is very small (≤5) AND my heaviest crate is very large (≥34), because the 15% duty saving must outweigh losing the smallest crate. Concretely: night saves floor(0.30×heaviest) − floor(0.15×heaviest) in duty but costs me my smallest crate. That net is positive only when smallest < ~5 and heaviest is large enough that the duty gap exceeds it. In every other case, main is equal or better. When in doubt, take main.

**Never do:**
- Do not declare a number higher than my heaviest crate to "compensate" for being behind in points. I have lost significant points across games by doing exactly this. Being behind changes nothing about the math of the current round.
- Do not switch to night on a "nothing to lose" final-round gamble. The expected value of night is lower than main in nearly all distributions.
- Do not declare my true total (sum of all three crates). That is far above my heaviest crate and inflates my duty with no upside.

**Quick check before committing:**
1. What is my heaviest crate? → That is my declaration.
2. Is my smallest crate ≤5 AND my heaviest ≥34? If yes, night is at least a tie and often a small win — take it. Otherwise, main.
3. My expected score for this round = (sum of all three crates) − floor(0.30 × heaviest). If that number feels low, it is because my crates are small, not because I declared wrong.