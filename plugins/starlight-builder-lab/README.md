# Starlight Builder Lab

Three portable skills and offline tooling for researching and building
agent workflow packages. Requires Python 3.10 or later for scripts. No API key,
server, dependency installation or billing account is needed to try the lab.

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
