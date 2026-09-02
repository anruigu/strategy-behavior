# 0902 variants -- what is in here

* `fidelity_v1.json` -- the byte-level fingerprint of all 38 cells BEFORE any
  of this work: scores, violations and a hash of every prompt, per cell x arm
  x policy x seed. Every engine refactor in this pass (payoff literals lifted
  to class attributes, rivalry terms added at an inert default) was gated
  against it, and it held for all 1216 episodes.
* `fidelity_v2.json` -- the same fingerprint after ONE deliberate change:
  `ref_sidebar`'s scripted colluding policy. It differs from v1 in exactly 16
  episodes, all of them `ref_sidebar` exploit episodes; honest play is
  identical, so the matched pair is intact and the game itself is untouched.
  See `test_referee_games.Scripted._bet`.
* `catalogue.json` -- every variant, measured. What `viz/variant_server.py`
  reads.
* `CATALOGUE.md` -- the same thing for a person.
