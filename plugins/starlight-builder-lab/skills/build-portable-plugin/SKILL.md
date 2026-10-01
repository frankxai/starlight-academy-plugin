---
name: build-portable-plugin
description: "Create or inspect a portable skills-only agent plugin from an explicit workflow specification. Use for plugin scaffolding, local package checks or reproducible ZIP preparation, without installing or publishing automatically."
---

# Build a portable plugin

Requires host file tools and Python 3.10 or later. This plugin has no server or
model API requirement. If execution is unavailable, produce editable source text
and commands without claiming that files or a ZIP exist.

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
