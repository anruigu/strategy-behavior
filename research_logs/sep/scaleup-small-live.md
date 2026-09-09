# Small-model cross-play and self-play — September 7

User correction: the requested small-model tests are **cross-play and self-play**, not the focal-player/scripted-rival experiment.

The mistaken scripted-rival launch (`benchmark/results/scaleup-small-20260907`) was stopped immediately. It saved 13 actions, no full benchmark result. Its status explicitly records the correction; those traces must not be pooled into the requested experiment.

Target small tier: Claude Haiku 4.5, GPT-5 mini, Gemini 3.7 Flash. Cross-play means different families at the same table. Self-play means independent conversations for copies of the same model, with no shared hidden state or conversation. No reflection or persistent playbook. Use matched environment seeds and rotate competitive seat assignments; cooperative Hanabi reports team performance rather than individual win rates.

Current status: model tests paused while Allie plays and reviews the games. The interface now has a plain-language guide and contextual action help. Resolve live-seat scope after that review:

- The new ten-game, 60-hole suite currently invokes only focal seat 0 and uses scripted rival actions. Changing the model client does not turn it into true cross-play.
- Existing live-seat adapters support native Exchange, native Hanabi and live IPD. These differ from the new profiles and have their own mechanism specifications; they cannot be reported as testing all 60 holes.
- Extending the new suite needs explicit live decision phases, private seat observations, engine event attribution per seat and freshly validated holes. NPC-response mechanisms (delayed retaliation, encoded withdrawal, trust responses, automatic Hanabi slot choice) need particular care: model behavior cannot be counted as a guaranteed planted engine hole.
- Win as Much currently has four seats; distinct-family cross-play needs a fourth small family or a separately versioned three-seat profile. Do not silently duplicate a family to fill the fourth cross-play seat.

No replacement API batch should be launched until its actual game suite and seat semantics match the user's choice. The previous mixed small/large cross-family pilot remains stopped.
