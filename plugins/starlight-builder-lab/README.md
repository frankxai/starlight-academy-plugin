# Starlight Builder Lab

Three portable skills and offline tooling for researching, building and restoring
agent workflow packages. Requires Python 3.10 or later for scripts. No API key,
server, dependency installation or billing account is needed to try the lab.
Source checks cover Windows and Linux on Python 3.10 and 3.13. Other operating
systems remain unverified; restore rejects symlinked output ancestors, including
system aliases such as macOS `/var`. Choose a canonical ordinary local parent.

This is source for a candidate plugin. It is not registered in the Academy
marketplaces or approved for an OpenAI directory. Host behavior tests and
independent review must be completed before promoting compatibility claims.

| Skill | Use it to |
| --- | --- |
| `map-agent-ecosystem` | Verify host capabilities and interpret public lab requirements |
| `design-agent-product` | Define one self-service workflow and its behavior tests |
| `build-portable-plugin` | Generate, inspect and package supplied skill instructions |

Read [the ecosystem reference](references/ecosystem.md) when deciding
where a package runs. Use [worked blueprints](references/product-blueprints.md)
when choosing an artifact to build. The public lab has no checkout or upgrade path.

## First working package

From this plugin directory, choose a new directory and ZIP path outside the
plugin. The example below writes under an existing project-owned `scratch`
directory. Substitute your own authorized paths. Generation refuses existing
directories and packaging refuses existing files.

```text
python -B scripts/package_lab.py scaffold examples/research-brief.json ../../scratch/research-brief-demo
python -B scripts/package_lab.py check ../../scratch/research-brief-demo
python -B scripts/package_lab.py pack ../../scratch/research-brief-demo ../../scratch/research-brief-demo.zip
python -B -m unittest discover -s tests -v
```

Inspect the output and run the skill on the supplied worked, adverse and transfer
tasks in the intended host. A reproducible ZIP and structural pass do not prove
the skill's answers are correct. The checker accepts one-line name/description fields, quoted or unquoted;
multiline YAML needs a full validator. It is not a general Agent Skills validator.

`scaffold` accepts a JSON object with `name`, `version`, `description`, `author`,
`license`, `license_text` and `skills[]`. Each skill supplies `name`,
`description` and complete `instructions`. The bundled example is MIT-licensed;
retain its complete licence and existing copyright notice when reusing its
content. For a separately authored specification, choose a licence for its
original assets and retain the required notices of reused assets. See the
[MIT licence text](https://spdx.org/licenses/MIT.html).
Generation retains the supplied text; it does not assess its legal sufficiency.

## Troubleshooting and removal

| Result | Action |
| --- | --- |
| Output already exists | Inspect it or choose a new versioned output; do not overwrite existing work |
| Forbidden path or private-pattern match | Remove the sensitive material from the package source; run a full secret scanner |
| Nested skill or invalid frontmatter | Use `skills/<name>/SKILL.md` and the supplied scaffold layout |
| Native manifest drift | Reconcile name/version before packaging |
| No Python or host file tools | Use the skills as a drafting guide; do not report generated artifacts |
| Symlink test skipped | Record the host limitation; rerun on a symlink-capable runner |
| Reparse point / OneDrive placeholder | Work with ordinary local files; this checker rejects all reparse-point content |

No service or watcher is installed. Remove generated source/ZIP files only through
your project's normal ownership process. If you later install the plugin, disable
or uninstall it through that host's plugin controls. Account connections, if added
later, need their own revocation. Existing Academy plugins are unaffected.

The source uses Apache-2.0. No third-party skill bodies are vendored. Primary
references support the dated research; future provider behavior needs fresh tests.

## Restore a downloaded package or inspect an update

Version 0.1.5 retains the download-to-source path and fixes Windows output access.
Obtain the expected SHA-256 from a trusted publisher release or channel record
independently of the downloaded ZIP.
Choose a new folder under an ordinary fully local project directory:

```text
python -B scripts/package_lab.py restore DOWNLOAD.zip NEW_DIRECTORY --sha256 PUBLISHER_SHA256
python -B scripts/package_lab.py check NEW_DIRECTORY
```

On Windows, restored folders inherit the chosen parent's permissions, so the
workspace owner can inspect and edit source created by a separate agent account.
Choose a parent whose access rules allow only the intended collaborators; restore
does not make a shared parent private. POSIX output folders use mode `0700`.
Check access in the account that will maintain the package before using it.
If an older restore is unreadable, preserve it and retry with version 0.1.5 into a
fresh sibling under an accessible parent. Restore never changes an existing ACL.

Restore reads and hashes the same bounded archive bytes. It checks the complete
skills-only package and supplied licence before creating the requested folder.
The result reports the archive and per-file hashes. Restore and pack preserve UTF-8 file bytes,
including CRLF and CR line endings,
and accepts inspected Python or JavaScript/Node text source; no code is executed.
The checks remain structural and the secret scan heuristic-only. A checksum
matches a supplied artifact; it does not authenticate its publisher, prove rights,
verify purchase/access or certify that executable source is safe.

Supported ZIPs use stored or DEFLATE compression, at most 32 MiB archive size,
512 entries, 16 MiB total expanded content and 1 MiB per file. Paths use at most
12 components and 240 characters. Links, reparse/special files, encryption,
ambiguous paths, duplicates, case collisions, invalid UTF-8 and bad CRCs are
refused. The package contract also refuses private-key patterns and personal paths.
Unicode normalization equivalence across filesystems is not certified. This is a
bounded text-package tool, not a general ZIP extractor.

Prior versions and customer edits are preserved. An existing destination, even
an empty folder, stops the command. Wrong hashes or invalid archives/packages
stop before output creation. A write failure can leave a partial new folder;
keep it for inspection and retry into a fresh sibling. A `.restore-incomplete`
marker remains until all files are written; check and pack refuse a marked folder.
Keep the marker and partial files together. No complete restore is
claimed without a successful command result. Review the source and returned
hashes before using it. The code assumes a trusted local filesystem and cooperating
writers, without adversarial path replacement or a power-loss guarantee.

For an update, restore to a new versioned folder, inspect differences and manually
reconcile your edits. Choose the version through your host's normal controls only
when installation is requested. Rollback selects the preserved prior version.
Restore never installs a plugin, migrates secrets, connects accounts or changes an
entitlement. Historic host receipts verify only their recorded version and scope.
