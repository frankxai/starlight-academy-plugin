---
name: build-portable-plugin
description: "Create, inspect or explain a portable skills-only agent plugin. Use when asked about the bundled research-brief example, scaffold/check/pack commands, preserving existing outputs or supplied full licence text, including read-only explanations when execution and writes are unavailable. Also use for plugin scaffolding, local package checks and reproducible ZIP preparation; installation and publication require a separate request."
---

# Build a portable plugin

Requires host file tools and Python 3.10 or later. This plugin has no server or
model API requirement. If execution is unavailable, produce editable source text
and commands without claiming that files or a ZIP exist.

For a read-only command explanation, return just the requested commands, path
requirements, licence handling and observed execution status. Fit the caller's
length limit with short command lines and one clause per operation. Aim below
three quarters of a supplied word limit so command tokens and formatting fit.
Combine status and licence handling into one short sentence each. Omit headings,
setup requirements and host-test plans unless requested. Before responding,
remove extra explanation that repeats the commands or preservation rule.

Use the user's chosen repository and its ownership rules. Inspect existing
skills before authoring. Preserve third-party skills as prerequisites rather than
copying their bodies. Prefer the host's existing creator tools when sufficient.

Read [the tool guide](../../README.md) and inspect
[the worked specification](../../examples/research-brief.json). The generator
accepts a supplied license identifier and complete license text; it does not
choose a license for the user. Turn the requested workflow into the
specification's input, output, uncertainty, permission and recovery instructions.
Use the example as a shape, preserving the user's domain. Resolve the installed
plugin's root before running its script. Use `python3` when that is the host's
Python 3 command. Choose a project-owned output path and preserve existing work.
The scaffold output directory must not exist, even if an existing directory is
empty. Pack also requires a new ZIP path. On either collision, stop and select a
new path; do not suggest force, cleanup or reuse of the existing output.

When generating the bundled example, retain its complete supplied MIT licence
and existing copyright notice. For copied or substantially reused content, keep
its required notices and permissions; never replace its original attribution
with the user's name. A separately authored specification may choose its own
licence for its original assets, with reused assets inventoried separately.

Run the package's `scripts/package_lab.py` with the requested operation:

```text
scaffold SPEC.json OUTPUT_DIRECTORY
check PLUGIN_DIRECTORY
pack PLUGIN_DIRECTORY OUTPUT.zip
```

Resolve failures before packaging. Inspect generated files and ZIP entries.
The check enforces a limited skills-only contract and flags common packaging
hazards; a full secret scan and current provider schema check remain separate.

Test workflow behavior in the intended host using a realistic task, bad input
and transfer task. Record host/version, skill revision, artifact, assistance,
cost and result. Keep structural validity, observed behavior and directory
approval as separate statuses. Script success grants none of the latter two.

Report created paths, package hash, checks run and remaining host tests.
MCP, lifecycle hooks, global configuration changes, installation and publishing
are outside this generator. Prepare those changes only when the user requests
them and current official documentation supports the target surface.
