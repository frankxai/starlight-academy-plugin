---
name: test-workflow-evidence
description: Build and revise deterministic acceptance checks for one synthetic agent workflow using public fixtures, false acceptances, false rejections and explicit unknown outcomes. Use after evaluation practice when a learner wants executable tests, an inspectable test suite or a regression case.
---

# Test workflow evidence

Help the learner turn an evidence judgment into a test that can expose failures.
Use only synthetic or explicitly public examples. This practice does not verify
the origin of supplied records, evaluate a live agent, certify a learner or
grant authority. The local tools do not send, write, call models or execute code.

## First attempt

1. Read `get_acceptance_lab` or `/academy/evaluation/fixtures.json`. It provides
   six check definitions and a starter suite with public expected labels.
2. Ask which failures a delivery-only check will miss. Preserve the learner's
   initial prediction and short explanation before running. Do not invent a
   response for them or request private internal reasoning.
3. Call `run_acceptance_suite` with `suiteJson` set to the serialized suite.
   Record the exact suite, checker version and returned results.

## Inspect and revise

- Inspect every mismatch. Distinguish false acceptance, false rejection and
  unknown outcomes. Unknown does not authorize a retry or consequential action.
- Add the check that would expose the failure and explain the observable fact
  it uses. Never average an authority or data-boundary failure into a score.
- Approval is a pre-admission snapshot. Delivery is a later observation.
  Matching supplied identifiers does not authenticate either record.
- Re-run after edits. Keep old results attached to the old input, not the new
  suite. A reference match only proves agreement on these public labels.

## Transfer and grader calibration

Change one fixture into a different workflow context. Set its expected verdict
before the run. Add a clean control so a reject-everything grader cannot appear
successful. Include at least one unresolved outcome. Explain why your new label
is appropriate; changing labels to match the checker is not improvement.

The JSON contract accepts 1–20 distinct cases and 1–6 distinct checks; no custom
code runs. When you need a real integration, first write a separate test against
mocked tools in the learner's authorized workspace. Capture the actual outcome
through a trustworthy observation adapter and obtain independent review before
using a result in an external action. The Academy comparator does not supply
that adapter or admission decision.

If the learner requests a file, save `ACCEPTANCE_SUITE.json` and a short
`ACCEPTANCE_REVIEW.md` containing prediction, mismatches, revision, transfer case,
known missing coverage and reviewer status. Label them unsigned self-study.
Do not upload or publish them without the learner's instruction.

## Method sources

- [Anthropic evaluation methodology](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): distinguish transcript and outcome; inspect grader disagreements.
- [LangChain Academy](https://github.com/langchain-ai/langchain-academy): executable learning artifacts.
- [Hugging Face hands-on assignment](https://huggingface.co/learn/agents-course/en/unit4/hands-on): transfer concepts into implementation. No benchmark or certification equivalence is claimed.

For an offline replay without a model, pass the suite or a browser run export on
stdin to `node mcp/check-acceptance.mjs` from the plugin root. Exit 0 means supplied
labels match, 1 means disagreement, and 2 means invalid input. Interpret the
fixture-level results; a zero exit code is not workflow admission.
