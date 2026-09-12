# Install the Starlight Academy learning pack

The verified installation path is the [Academy learning pack](https://starlightintelligence.academy/academy/install).
The Git projection in `frankxai/starlight-academy-plugin` is a publication candidate;
clean installation from a public Git revision has not yet been verified. A
projection receipt alone does not establish a successful installation. Use the
archive commands below until this guide names a tested immutable Git revision.

The plugin offers five skills and eight local MCP tools for four missions across
agentic systems, human judgment and scientific inference. Start with an unaided
attempt, produce an artifact, preserve critique and revision, then transfer the
method to a changed context. No account, model key or cloud learner store is
required by the plugin. The host agent's own access and charges remain separate.

## Codex

Download and extract the complete learning pack. Use a current Codex CLI that
supports `plugin marketplace` and Node.js 22 or later. Review the source, open a
terminal in the extracted `starlight-academy` directory, then run:

```sh
node install.mjs codex
```

## Claude Code

In the same extracted learning-pack directory, with Claude Code installed, run:

```sh
node install.mjs claude
```

Both launchers register the extracted local marketplace and invoke the native
plugin manager. Append `--dry-run` to inspect the commands first. Keep native
trust prompts enabled and preserve the extracted directory for updates.

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

The [release receipt](release.json) lists the source ZIP hash and every projected file hash. These are
consistency checks, not signatures or independent publisher authentication. The
public mirror changes only source-repository URLs in the known native manifests,
then adds this guide, a plugin README and its Apache-2.0 license. Executable MCP
and skill bytes remain identical to the source archive.

Future Git installation will name a tested 40-character commit using Codex's
`--ref` or Claude's `@` suffix. This candidate guide provides no floating Git
installation command. Inspect updates before refreshing through your host's
marketplace manager. Disable or remove only
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
