---
name: design-agent-product
description: "Turn a user workflow into a portable agent package or technical blueprint, with worked examples, evidence tests and licensing boundaries. Use before implementing an agent workflow."
---

# Design an agent workflow

Read [the worked blueprints](../../references/product-blueprints.md). Start with
the user's workflow and available technology. Select an existing package to
improve when it fits. Define an observable output before writing instructions.

Write one workflow contract with:

- User, trigger, present workaround and the change they need.
- Input, artifact, acceptance test, failed-input behavior and recovery.
- Required host capabilities, data locations and user-owned keys or accounts.
- Original assets, third-party prerequisites and license obligations.
- One worked example, one adverse case and one different-context transfer task.
- A comparison with the host's baseline behavior on the same task.

Use a portable skill for repeatable judgment; use a script for deterministic
mechanics; add MCP only when the task requires connected data or actions. Keep
instructions and reference resources small enough for selective loading.

Record host requirements, user data locations and relevant usage limits. Package
self-service setup, diagnostics, uninstall and a known-issues guide. Measure
task cost and assistance rather than promising autonomous or error-free work.

Return the contract and one improved artifact when implementation is authorized.
Retain license and attribution requirements for reused code and resources.
Distinguish source generation, tested host behavior and provider approval.
