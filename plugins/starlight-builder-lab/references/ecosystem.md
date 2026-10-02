# Agent ecosystems

Research snapshot: 2026-10-01. Recheck volatile rules before implementation or
release. These are public requirements and documented capabilities. They do not
establish a particular account's access or a lab's private commercial strategy.

## What each layer does

| Layer | Role | Evidence to collect |
| --- | --- | --- |
| Host | Runs work, manages tools and permissions | Exact product, version, plan and environment |
| Skill | Supplies task instructions and selective resources | Trigger accuracy, output contract and behavior tests |
| Plugin | Packages capabilities for installation | Manifest, file layout, version and compatibility |
| MCP | Connects data or actions when needed | Transport, auth, tool behavior and permission boundary |
| Plugin marketplace | Catalogs installable packages | Source revision, install/update/uninstall observations |
| Blueprint | Explains a reproducible implementation | Complete worked example, prerequisites and known limits |

### OpenAI Dots, Work and Codex

Dots can delegate work to cloud and connected-computer tasks. Installed plugins
and connected accounts determine available tools. Local skills require a connected
computer. Do not infer Dots access from a working Codex installation.
[Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

Dots availability is a rollout and account question. The launch help page lists
plan and regional restrictions, including restrictions on Pro availability in
the EEA, Switzerland and UK. Check current account eligibility before relying on a
Dots-specific workflow.
[Getting started](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot).

Author new portable packages with root `plugin.json`, `skills/<name>/SKILL.md`
and optional root `mcp.json`. OpenAI metadata belongs under
`extensions.com.openai`; a legacy overlay is a fallback, not a merged authority.
Catalog source paths are relative to the marketplace root. A local install and
a public directory listing are separate operations.
[Packaging](https://developers.openai.com/plugins/build/plugins),
[portable schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).

ZIP upload creates a draft followed by scans and review. Skills-only submissions
do not require MCP demo/test cases. An initial MCP review currently requires five
positive and three negative cases; only one MCP server can be connected per plugin.
Adding MCP to an existing skills-only directory plugin is currently unsupported.
Plan a separate integration package when needed rather than assuming that upgrade.
[Submission](https://developers.openai.com/plugins/deploy/submission).

Directory plugins currently prohibit digital-product commerce and upgrade
promotion, including indirect freemium upsells. Existing paid-account features
may be used. Keep external digital sales outside the plugin experience. Do not
interpret an external checkout as permission to add a purchase CTA to the plugin.
[Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines).

### Anthropic and Google

Claude Code marketplace catalogs use `.claude-plugin/marketplace.json` and native
plugin metadata. Pin source revisions and verify installation in Claude. Portable
files alone do not prove every host interprets them identically.
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

Anthropic's engineering guidance starts with simple composable workflows and
adds autonomy where the task warrants it. Read its explanation of tool design,
evaluation and feedback before turning a deterministic pipeline into a swarm.
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

Google's Gemini function-calling interface uses structured function declarations.
A portable instruction pack is useful context, but it does not install functions
or create an authenticated connector. A Google adapter requires implementation
and host-specific tests.
[Function calling](https://ai.google.dev/gemini-api/docs/function-calling).

## Evaluate an integration

Use public requirements to decide what to build: supported manifest layout,
selective skill loading, tool authentication, permission boundaries, behavior
cases and review evidence. Those interfaces do not establish a private roadmap.
Compare the same workflow with the host's baseline tools. Record output quality,
source coverage, assistance and total task cost. Retain failed cases and the
exact package revision before changing its instructions.
