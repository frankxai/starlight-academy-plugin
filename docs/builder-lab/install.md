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

The example-attribution concern was repaired and independently accepted in
merged PR12. Complete current-version host comparisons and prove runtime disable. Then
publish the reviewed payload through the existing catalogs with an immutable
Claude source pin. Preserve the current Academy entries and customer files.

The [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins)
distinguishes repository marketplaces from the universal directory. Local CLI
installation establishes no ChatGPT cloud, Dots account or directory approval.
Those statuses remain in [release.json](release.json).

## Version 0.1.1 reruns

The [versioned trial record](native-patch-trials.json) preserves the intermediate
failed response and the final eight-case batches at `1af40b2` in both hosts.
All twelve payload hashes matched the tested source. The native Codex install
was removed; owned cache and temporary profile are absent and previous global
configuration semantics were restored. Independent acceptance and merge completed
in PR12. These were assisted batches, with isolated triggers and comparisons
tracked separately in the next candidate.

## Version 0.1.2 candidate

The [native comparison record](native-comparison.json) includes fresh Claude
sessions with and without the plugin, actual replies and failed trigger/semantic
cases. The [method](native-evals.md) explains why a heuristic pass cannot certify
skill selection or safe verification guidance. Payload changes need independent
source review and native Codex 0.1.2 verification before catalog registration.
Runtime disable, actual Dots access and directory approval remain unproved.

## Version 0.1.3 scoped repository-skill trial

The [fresh record](native-0-1-3.json) observes all three Codex repository skills
in an enabled session and none in a disabled session. The owned profile was
removed and global metadata hashes stayed unchanged. This uses project skill
discovery, with relative reference layout preserved; it does not install or
remove a plugin from the global registry. Keep that lifecycle gate separate.
Claude loads the exact source with session-only `--plugin-dir`; partial response
acceptance and earlier failed candidates remain in the record.
