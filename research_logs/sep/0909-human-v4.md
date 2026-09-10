# Human focal-agent V4

Requested: archive symmetric play-against-Qwen as V0; use actual AI-eval games
and opponent interventions in V4, with the human replacing focal seat 0.

Published application revision: `144b0f9f`.
Sources: `benchmark/results/v3-ma-four-model-20260909/plan.json` and its frozen
engine snapshot. Ten recipient-dependent scenarios; ordinary/open referee;
ordinary/nerfed conditions from the run plus defensive from its specifications.
Four Commons scenarios excluded from this menu because they have no nerf arm.

V0 preserves all nineteen prior symmetric games. V3 remains available. Existing
shared-workspace v3-SA/v3-MA integrations were preserved while merging the V4
changes; those unpublished integrations were not bundled into this deployment.

Validation: 42 unit/integration tests; all public-deployment gates; ten full
browser playthroughs, mobile view, final outcomes, and saved traces. Actual saved
AI traces replay exactly for all twenty scenario × ordinary/nerfed combinations.
All four real model routes accepted eval actions in a live protocol check.

Deployment adds `OPENROUTER_API_KEY` to the app through Secret
`plays-eval-openrouter`, enabling the same Haiku/mini routes as the eval. Existing
FLT credentials serve Qwen and GLM. No credentials are stored in this repository.

Logs and inspection artifacts for this implementation are under `/tmp/v4-human-*`
and `/tmp/check-v4-human-browser.py`; these are verification, not study samples.
The full release checkout inherits unrelated pre-existing V3 research-guide
validation drift; the complete sparse public deployment gate passed. Shared
research changes remain in the original workspace.

Live verification completed after deployment: all four models finished Clues ·
The note through the public player, with four human submissions and eight
referee stages each. GLM used ordinary policy (the linked episode's setup);
Qwen, Haiku, and mini used nerfed policy. Runs: `d0603a7854ec`, `d0edda46c83e`,
`d9a2017d9929`, `5fed1085c0cf`, respectively. The human test policy sent the marked
slot, so these are informed functionality checks, not discovery observations.
Server-side JSONL records were checked for source/condition/model/seed, exact
focal observations, private prompt bytes, final outcomes, and complete stages.
The public browser and all shared-workspace gates passed; the new pod is 5/5
ready. The model-credential restart encountered a stuck terminating old pod;
that obsolete pod was removed to allow the replacement to start.
