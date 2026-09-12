# Starlight Academy

Public teaching material for your AI conversation: choose a challenge, make your
own first attempt, practice with a guide, critique, revise and test transfer.

The plugin provides one guiding skill and connects four public MCP tools:
`get_academy`, `get_teacher`, `get_challenge`, `get_feedback_guide`.
The server is `https://starlightintelligence.academy/mcp` (Streamable HTTP).
It accepts catalog IDs only. No drafts, accounts, private data, model calls,
student database, automatic training, credentials or external actions.

Your chosen host provides the AI conversation under its own data policy.
Teachers are fictional teaching methods, not separately running models or human
instructors. Switching teacher roles is not independent review.

## Connect and practice

Use https://starlightintelligence.academy/academy/connect for the current
connection instructions and a matching browser challenge. The root `plugin.json`
and `mcp.json` use Agent Plugins 1.0.0. Codex and Claude compatibility manifests
are included. Host support varies; a standard manifest is not proof of execution
in every host.

For Codex CLI, connect the remote tools directly:

```sh
codex mcp add starlight-academy --url https://starlightintelligence.academy/mcp
```

For Claude Code:

```sh
claude mcp add --transport http starlight-academy https://starlightintelligence.academy/mcp
```

The commands connect MCP tools. To install the bundled teaching skill as well,
use a compatible plugin host with this complete folder or the public directory
after it is published. A direct MCP connection is not a plugin-directory install.

Start a fresh conversation: “Use Starlight Academy. Help me choose a challenge
and ask for my own first attempt before showing a solution.”

## Publication status

This package is independently developed by Starlight Intelligence Systems.
OpenAI directory submission is being prepared. It has not been submitted,
approved or publicly listed; there is no OpenAI Verified claim. The existing
offline `starlight-department-lab` package remains a separate five-skill toolkit.

## Privacy and feedback

Read https://starlightintelligence.academy/academy/connect and
https://starlightintelligence.academy/privacy. The server returns public material
and processes selected catalog IDs. Hosting may process technical request data.
The plugin does not collect feedback text or opt you into model training.
You choose what to preserve or share through your host's tools.
