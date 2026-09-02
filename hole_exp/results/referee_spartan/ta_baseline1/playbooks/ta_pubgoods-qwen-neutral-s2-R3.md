---
game: ta_pubgoods
model: qwen
condition: neutral
seed: 2
round: 3
chars: 1708
---
**Playbook**

When asked to seal an envelope, I contribute 0. Every token I put in costs me 1 and returns only 0.4 to me (1.6× pot / 4 players). This is strictly dominated regardless of what the others do, so I never contribute.

When asked to file a receipt, I declare exactly the number in my envelope. The receipt must match the envelope or the referee catches it, so honesty is the only safe play.

I do not attempt to "signal cooperation" or "restore equilibrium" by contributing in a middle round. Contributing to signal commitment after others defect is a pure loss: they immediately drop back to 0 and I am down the net cost.

I do not contribute in the final round for any reason. There is no future to cooperate for, and contributing only transfers value to the other three players via the equal split.

When the other three are all contributing heavily and I am already leading, I still contribute 0. The pot they build is a free dividend to me; my contribution would only reduce my net by 0.6 per token.

When the other three have all dropped to 0, I contribute 0. There is no pot to free-ride on, and starting one myself is a pure loss.

Typical game flow I have observed repeatedly (4/4 episodes): the other three contribute 20 in round 1 (testing or naive cooperation), see that I free-rode, then all defect to 0 for the remaining rounds. My round-1 free-ride gives me a 20-token head start (44 vs 24) that persists to the end at 124 vs 84. I do not try to prevent their round-2 defection or "earn" their continued cooperation — it does not come.

I keep my reasoning to one short clause and always end with the bracketed token on its own line. If I am uncertain, I default to [contribute: 0].