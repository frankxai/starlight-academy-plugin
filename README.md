# Install Starlight Academy from the public source

This directory describes the Academy plugin projection in
`frankxai/starlight-academy-plugin`. Check that the catalogs and plugin files are
present on the ref you select before installing. A projection receipt alone
does not establish publication or a successful installation.

The plugin offers five skills and eight local MCP tools for four missions across
agentic systems, human judgment and scientific inference. Start with an unaided
attempt, produce an artifact, preserve critique and revision, then transfer the
method to a changed context. No account, model key or cloud learner store is
required by the plugin. The host agent's own access and charges remain separate.

## Codex

Use a current Codex CLI that supports `plugin marketplace`. Install Node.js 22
or later first. Review the source, then run:

```sh
codex plugin marketplace add frankxai/starlight-academy-plugin
codex plugin add starlight-department-lab@starlight-academy
```

## Claude Code

```sh
claude plugin marketplace add frankxai/starlight-academy-plugin
claude plugin install starlight-department-lab@starlight-academy
```

In Claude Code's interactive interface, the same operations are `/plugin
marketplace add frankxai/starlight-academy-plugin` and `/plugin install
starlight-department-lab@starlight-academy`. Keep native trust prompts enabled.

If `starlight-academy` is already registered from an extracted local pack, inspect
that source in your host's marketplace manager before replacing it. Do not mix
local and Git projections under the same marketplace name. Keep your practice
files outside the plugin cache.

Open a new Codex task or restart Claude Code after installation. Ask:

> Use learn-starlight-mission. List the four missions using get_mission_studio,
> let me choose one, and preserve my first attempt before offering hints. Keep
> assistance, sources, critique and revision visible. Export the practice JSON
> to my workspace only when I ask. Treat it as practice, not a credential.

Confirm that `get_mission_studio` and `inspect_mission_practice` are available.
An installed listing is not proof that the MCP started. If tools are missing,
check that Node is visible to the app, restart, and inspect the host's MCP logs.

## Grok, Hermes and Antigravity

Use the versioned [Academy download and native installation guide](https://starlightintelligence.academy/academy/install).
It includes host-specific manifests and one launcher command per host. Hermes
starts disabled; Antigravity uses an anchored local server path. Full authenticated
host startup for these three adapters has not been verified. They are separate
projections, with different trust and update behavior.

## Reproducibility and updates

`release.json` lists the source ZIP hash and every projected file hash. These are
consistency checks, not signatures or independent publisher authentication. The
public mirror changes only source-repository URLs in the known native manifests,
then adds this guide, a plugin README and its Apache-2.0 license. Executable MCP
and skill bytes remain identical to the source archive.

To pin a reviewed revision, use the host's Git ref option when adding the
marketplace: Codex `--ref <reviewed-commit-or-tag>` or Claude's
`frankxai/starlight-academy-plugin@<reviewed-commit-or-tag>`. Replace the placeholder
with the actual reviewed ref; do not type the brackets. Inspect updates before
refreshing through your host's marketplace manager. Disable or remove only
`starlight-department-lab` to roll back an installation; saved practice files are
independent of the package.

Public Git installation does not mean admission to OpenAI's or Anthropic's public
directories. Workspace import, sharing and directory permissions remain owned by
the provider and workspace administrator. A browser link cannot bypass those
controls or silently install code on another person's machine.

## Source and learning boundaries

The Academy writes its own exercises and records source applications in the
bundled curriculum. Reference answers are public. The checks assess structure
and selected answers; they do not authenticate authorship, grade free-form
reasoning, prove learning gains or grant operational authority. The MCP has no
network or file-write capability. Host skills guide the learner's agent, whose
own tools require their normal permission controls.

Plugin and learning material: Apache-2.0, included at
`plugins/starlight-department-lab/LICENSE`. The public repository uses the same Apache-2.0 license.

Installation formats checked against [Claude's marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces)
and Codex CLI 0.154.0-alpha.6.2 on 2026-09-12. See also [OpenAI's workspace marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
