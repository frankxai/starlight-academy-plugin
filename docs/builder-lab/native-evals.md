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
fragment hash. Tokens and invoice cash remain null. Canonical parent hashing
rejects duplicate imports with renamed prefixes, changed indentation or key
order. It does not identify separate aggregate/result files as one invocation.

For a retained actual Claude result, use `import-claude` with the same run ID.
Replace its cost-only row with the complete usage row; counting both would double
the expenditure. The same-ID combination is rejected. A different-ID actual
result still requires manual reconciliation with its aggregate provenance.
Keep separate failed attempts and missing-receipt gaps. Generate
the [goal report](reports/2026-10-02.md) after reconciliation. Thinking already
included in native output is counted once. Cash ROI requires reconciled cash
inputs; list-cost estimates cannot supply it.

## Version 0.1.3 direct CLI trials

[The new record](native-0-1-3.json) uses fresh `claude --print` sessions with
`--plugin-dir` for the with arm and no Builder Lab plugin for selected controls.
It preserves the original nine prompts, the Read/Skill restriction, plan mode,
strict empty MCP configuration and actual stream/result usage. Built-in Claude
plugins remain visible. This is a different harness from `claude plugin eval`;
it produces no native comparative scores and creates no kept evaluator sandbox.
Actual responses, tool selections, source hashes and the word proxy are retained.

Codex uses project `.agents/skills` with reference paths preserved, an owned
temporary skill-enable profile and the existing login launcher. Security hooks
and rules remain inherited; the actual sessions use read-only sandboxing and
disabled browsing/MCP configuration. Other skill descriptors remain, so pure
host isolation is not claimed. A separate D1 prompt checks the model-visible
catalog in fresh enabled and disabled sessions. Its pair proves catalog toggling,
without proving plugin registry removal or revoking access to readable files.
The no-command P3 prompt prevents reading the bundle through shell-based file
tools; its generic Codex reply remains limited rather than accepted.

Use a new source fixture and fresh receipt IDs for retries. Run one admitted
worker at a time, retain actual failures and reconcile complete results once.
The local debug renderer is a discovery diagnostic, excluded from model costs.

The 0.1.3 Codex export reads native response files as UTF-8 and retains raw native
usage plus the disjoint token-normalization arithmetic. One JSONL stream contains
trace events and final usage, so its receipt and trace hashes attest the same
object. The response-file hash is separate. Subsequent local catalog renders
confirm descriptor exclusion, but the 42-token D1 native-input difference remains
unexplained without exact raw requests. Trigger descriptions were tuned on these
prompts; use held-out phrasings and repeated cases before claiming general accuracy.
