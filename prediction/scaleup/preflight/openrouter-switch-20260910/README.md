# FLT access failure and OpenRouter continuation

On September 10, 2026, the FLT gateway began returning HTTP 403 around
19:47:32 UTC for both Qwen 3.8 27B and GLM 5.3. Its model catalog also returned
403. A fresh SDK client reproduced the denial around 19:50:20. The returned
error was generic and did not disclose a cause. These observations identify a
provider access failure, but do not establish whether it came from a key policy,
gateway configuration, or another upstream condition.

At 19:54:45 the catalog returned HTTP 200; a subsequent SDK catalog check also
succeeded. No credential rotation was performed. This recovery suggests a
transient failure, but is not a diagnosis of the underlying cause.

The user requested switching to OpenRouter. The OpenRouter catalog and key
checks succeeded, followed by live generation preflight for these exact routes:

- `qwen/qwen3.8-27b`
- `z-ai/glm-5.3`

New dataset plans now default to OpenRouter. The 77 complete FLT episodes are
retained; the 67 unfinished episodes have a separate OpenRouter manifest and
restart from their original opening states. No episode combines providers. The
game specification, logical model identity, prompt condition, environment seed,
seat assignment, temperature, reasoning request, and token cap are preserved.
Provider assignment followed original completion and is not randomized.

Evidence is in `diagnosis.json`, `flt-sdk-recheck.json`,
`openrouter-model-catalog.json`, and `generation-preflight.json`. Historical
failure counts remain in `../../runs/pilot-20260910/collection-blocker.json`.
Current coverage, source attribution, and verified exports are in
`../../runs/pilot-20260910/export/`; the viewer follows the continuation pointer.
