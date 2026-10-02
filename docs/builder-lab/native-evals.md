# Native comparisons and receipt import

The [comparison record](native-comparison.json) keeps actual Claude replies,
tool calls, tested payload hashes and failed cases. The first two 0.1.1 suites
produced 34 model runs, with known list-cost receipts but no retained token
traces. Later 0.1.2 trials retain each native result. These are small descriptive
pilots; they establish neither broad compatibility nor a measured commercial ROI.

Use identical natural prompts in fresh plugin and plain-host sessions. Record
skill selection separately from response quality. Our heuristic scores missed
an unverified payout-interface suggestion and a packaging trigger failure.
Read the actual reply before accepting a case. Generic plain-host responses
often meet the same contract; bundle-specific tasks require access to the bundle.

## Reproduce a bounded case

Consult the installed `claude plugin eval --help` and the current
[official evaluator reference](https://code.claude.com/docs/en/plugin-evals).
The trial used Claude Code 2.1.287 and `claude-sonnet-5-5`. Check machine admission,
account eligibility and usage before starting a worker. Run one worker at a time.

Create `evals/p3/prompt.md` inside a frozen plugin snapshot:

```markdown
---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Skill]
plugins: ["../.."]
---
Use the bundled research-brief example to explain scaffold/check/pack commands.
Execution and writes are unavailable. Preserve existing outputs and supplied
full licence text. Do not claim to have generated files or a ZIP.
```

Put a selection indicator in `evals/p3/graders/skill-fired.md`:

```yaml
---
type: tool_used
tool: Skill
arm: with-only
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?build-portable-plugin"'
---
```

Add response-contract graders and a lead review of the actual output. The native
selection indicator is excluded from the comparative response score. In our
pilot, P3 scored 1 even when the skill stayed idle.

```text
claude --setting-sources "" plugin eval PLUGIN_DIRECTORY --case p3 --runs 3 --concurrency 1 --ablation with-without --model claude-sonnet-5-5 --max-cost-usd 1.2 --keep-temp --no-publish --no-scaffold --mocks record --trust-plugin --json NATIVE.json
```

`--trust-plugin` applies to the exact reviewed snapshot. The cost ceiling is a
native list-price estimate; it does not establish invoice allocation. Inspect
partial/error records, snapshot hashes and terminal worker state. Archive actual
result receipts from `out/` before cleanup. On Windows the evaluator warned that
retained sandboxes could not be sealed. Read their outputs only; do not execute
code, run Git or load configuration inside them. Preserve an exact owned-folder
manifest when cleanup is rejected.

## Import actual costs and usage

```text
python -B docs/builder-lab/scripts/goal_report.py import-claude-eval NATIVE.json --goal BL-01 --id-prefix pilot-1 --source-url https://github.com/frankxai/starlight-academy-plugin/issues/3
```

The importer validates native schema and run/judge cost reconciliation without
reading supplied trace paths. Each run receives a parent hash, JSON pointer and
fragment hash. Tokens and invoice cash remain null. Renaming the same imported
receipt cannot evade report deduplication.

For a retained actual Claude result, use `import-claude` with the same run ID.
Replace its cost-only row with the complete usage row; counting both would double
the expenditure. Keep separate failed attempts and missing-receipt gaps. Generate
the [goal report](reports/2026-10-02.md) after reconciliation. Thinking already
included in native output is counted once. Cash ROI requires reconciled cash
inputs; list-cost estimates cannot supply it.
