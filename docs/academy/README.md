# Install the Starlight Academy learning pack

Install the learning pack from the [Academy installation page](https://starlightintelligence.academy/academy/install), or use the pinned public commands below.
Clean Codex and Claude profiles installed catalog revision
`60724543685f6a5db7cbed55fe4b4aa574913ff2` on 12 September 2026.
Both installed copies matched all 15 skill/MCP files, exposed eight tools, and
completed a mission request. This verifies installation and the local MCP;
it does not establish full authenticated host operation or provider directory admission.

The plugin offers five skills and eight local MCP tools for four missions across
agentic systems, human judgment and scientific inference. Start with an unaided
attempt, produce an artifact, preserve critique and revision, then transfer the
method to a changed context. No account, model key or cloud learner store is
required by the plugin. The host agent's own access and charges remain separate.

## Codex

Use Git, Node.js 22 or later, and a current Codex CLI with plugin commands.
Review the source, then run both commands in order:

```sh
codex plugin marketplace add frankxai/starlight-academy-plugin --ref 60724543685f6a5db7cbed55fe4b4aa574913ff2
codex plugin add starlight-department-lab@starlight-academy
```

## Claude Code

With Git, Node.js 22 or later and Claude Code installed, run:

```sh
claude plugin marketplace add https://raw.githubusercontent.com/frankxai/starlight-academy-plugin/60724543685f6a5db7cbed55fe4b4aa574913ff2/.claude-plugin/marketplace.json
claude plugin install starlight-department-lab@starlight-academy
```

The catalog pins Claude's HTTPS plugin payload to
`e06bbe8d4377ef7c439e83beacd6431072c89e58`. Native trust prompts stay enabled.
The checks used Codex 0.154.0-alpha.6.2 and Claude Code 2.1.268 on Windows;
other versions and operating systems may behave differently.

For an archive installation instead, download and extract the complete learning
pack, open a terminal in its `starlight-academy` directory, and run
`node install.mjs codex` or `node install.mjs claude`. Append `--dry-run` to inspect
the native steps. Preserve the extracted directory for local updates.

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
public mirror changes source-repository URLs in the known native manifests and
gives Claude an HTTPS `git-subdir` source pinned to an examined 40-character
payload commit. It adds this guide, a plugin README and the Apache-2.0 license.
Executable MCP and skill bytes remain identical to the source archive.

Both catalog commands above pin the tested 40-character catalog commit.
Codex uses `--ref`; Claude uses a commit-pinned HTTPS catalog whose plugin source
has its own exact payload SHA. Claude's marketplace URL suffix accepts branches
or tags, so it is not used as a commit pin. These pins remain fixed until you
explicitly choose an update. Inspect a new revision before changing your source.
Disable or remove only `starlight-department-lab` to roll back an installation;
saved practice files are independent of the package.

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
