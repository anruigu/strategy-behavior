# Expanded model roster for the filtered 45-hole plot

User requested Kimi K3, DeepSeek V4-Pro, Google Gemma 4 (then specified 31B), Qwen 9B and GPT-OSS-20B. This extends the September 9 small-model engine audit with the same frozen source and the existing 45-hole analysis filter. Kimi and DeepSeek are comparison models, not claims of small parameter count.

Live report: `benchmark/results/small-engine49-20260909/plots/filtered-45-extended/REPORT.md`.
Exact routes and protocol: `benchmark/results/small-engine49-20260909/extension-plan.json`.

FLT now advertises `kimi-k3`, and its game canary succeeded. OpenRouter routes are `deepseek/deepseek-v4-pro-0813`, `google/gemma-4-31b-it`, `qwen/qwen3.5-9b`, and `openai/gpt-oss-20b`. The dated DeepSeek GA release supports low effort, unlike the older unversioned catalog entry. Full provider catalogs, canary responses, actual model IDs and billing are saved in `extension-preflight/`.

The model-only launcher lives outside the original source and verifies every original SHA-256 identity. It imports the frozen engines, client, game prompts, scoring and evaluation runner. All 49 original targets are evaluated; the current 45 eligible targets are plotted. Same three seeds, 57 blind episodes per model, fresh hinted diagnostics on valid misses, 16,384-token ceiling, omitted temperature and requested low reasoning. Gemma and Qwen expose reasoning but no discrete effort levels in their catalog entries; equal requests do not establish equal compute. The shared $500 ledger remains unchanged.

Run processes and a detached plot watcher are recorded in `*-process.json` and `extension-plot-process.json`. The watcher adds a model after its run ends, intersects valid completed blind episodes across all plotted models, and restricts hints to the same intersection. Missing episodes never become zeroes; an incomplete hinted subset is not drawn. Original five-model outputs are preserved. Expanded outputs use `plots/filtered-45-extended/`.

Validation: all original five-model rates and common episode IDs exactly match the existing filtered plot; pending models are absent from the data rather than counted as zero. Existing hinted subsets are complete. The expanded figure was rendered and visually inspected. Original rule disclosures remain documented; execution is not clean hidden-effect discovery.

A detached supervisor waits for the Qwen canary, launches it only on success, and permits one checkpoint-preserving recovery pass per added model after first-pass errors. Before recovery, status, coverage and hinted schedule are archived. The shared budget is never raised. The watcher waits for each model’s recovery to end before adding its curve. Lifecycle is tracked in `extension-lifecycle.json`. Ten-model aggregation and recovery exclusion were also checked using temporary synthetic fixtures, separate from all research results.
