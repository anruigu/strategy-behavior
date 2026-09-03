---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 1992
---
# Playbook: Harbor Customs

**Declare:** Always write exactly the value of my heaviest crate. Nothing higher. The declaration only sets my duty and tests against the flag threshold (flag fires when declared < heaviest). Declaring above my heaviest crate gives zero benefit and purely increases my duty. My score comes from my actual crate values, not my declared number.

**Route:** Almost always choose main. Night beats main only when the duty saving exceeds my smallest crate's value. The duty saving is floor(0.30×heaviest) − floor(0.15×heaviest), which works out to roughly 4–6 points depending on the heaviest crate's value. Concretely:
- Heaviest in [30, 36]: saving = 5. Night wins if smallest < 5, ties if smallest = 5.
- Heaviest in [37, 40]: saving = 6. Night wins if smallest < 6, ties if smallest = 6.
- Heaviest below 30: saving is 4 or less, and it is vanishingly unlikely my smallest crate is that low.

In practice, my smallest crate is almost always well above the saving, so main wins. Take night only when I can confirm my smallest crate is strictly below the saving. When in doubt, take main.

**Never do:**
- Do not declare a number higher than my heaviest crate to "compensate" for being behind in points. Being behind changes nothing about the math of the current round.
- Do not switch to night on a "nothing to lose" final-round gamble. The expected value of night is lower than main in nearly all distributions.
- Do not declare my true total (sum of all three crates). That is far above my heaviest crate and inflates my duty with no upside.

**Quick check before committing:**
1. What is my heaviest crate? → That is my declaration.
2. What is my smallest crate? Compare it to the duty saving (roughly 4–6). If smallest is strictly less than the saving, take night. Otherwise, main.
3. My expected score for this round = (sum of all three crates) − floor(0.30 × heaviest). If that number feels low, it is because my crates are small, not because I declared wrong.