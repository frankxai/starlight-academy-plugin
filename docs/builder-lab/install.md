# Native host validation and recovery

Builder Lab is source on main. It is still absent from the repository's Codex
and Claude catalogs. The receipts below describe bounded local tests, with
production distribution gates remaining open.

## Claude Code 2.1.287

The response trial used `--plugin-dir` with the committed plugin snapshot,
`--restricted`, Read/Skill tools, plan mode and a strict empty MCP configuration.
All three native skills were invoked. A separate trial used `dontAsk` and three
exact Bash allow rules for scaffold, check and pack in new test paths. The lead
checked the actual generated ZIP, entries and example licence.

These are session-only plugin loads. Ending the trial releases the session's
plugin; no persistent Claude marketplace installation was performed. The checked
Claude settings and installed-plugin metadata stayed unchanged. See
[responses](host-responses.json) and [artifact proof](host-artifact.json).

## Codex CLI 0.159.3

The test used a Git-blob snapshot of the merged source, a temporary local
marketplace and the native `codex plugin add` command. All twelve installed files
matched that source. A read-only, ephemeral session loaded and read the three
skills, with browsing disabled and a scoped profile disabling other plugins and
MCP connections.

The first three attempts stopped at discovery failure. This installed version
required per-skill scope entries pointing to `SKILL.md` files rather than folders;
the final session also selected `skills.max_context_tokens=10000`. This is an
observed compatibility workaround, not a change to the shared configuration.
The current [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
describes per-skill overrides and the context limit. Recheck the actual client
before reusing the workaround in another installation.

The successful session returned eight cases. P2's unlabelled invented example
remains a quality concern. The private machine profile and its personal paths
are excluded from the package.

After testing, `codex plugin remove` removed only the temporary test plugin and
its owned cache. Existing configuration semantics were restored. A debug
listing still showed skill descriptors with
`enabled=false`, so that listing does not prove runtime disable behavior.

## Before catalog release

The Builder Lab source is licensed Apache-2.0. The separately generated
research-brief example retains its own MIT licence.

Resolve the example-attribution concern, obtain independent acceptance of the
host receipts, run the plain-host comparison and prove runtime disable. Then
publish the reviewed payload through the existing catalogs with an immutable
Claude source pin. Preserve the current Academy entries and customer files.

The [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins)
distinguishes repository marketplaces from the universal directory. Local CLI
installation establishes no ChatGPT cloud, Dots account or directory approval.
Those statuses remain in [release.json](release.json).
