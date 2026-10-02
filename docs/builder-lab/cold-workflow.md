# Native package build and recovery

At accepted source `1e9b159330d87e754f9265f17564432d3638a2cb`, Claude Code
2.1.287 created three editable MIT demonstration packages and six ZIPs. Each
build refused existing source directories, including an empty directory,
refused an existing export and rejected the malformed specification. The lead
confirmed all protected bytes, the complete MIT notice and the archive contents.
The first Claude baseline denial, Codex interpreter failure and timeout are also
retained. Every new ZIP has SHA-256
`fdc40d65c85efb69e827b25dbf0914b9fd246a4d07b8102b79564a0078a12825`.

The [native record](cold-workflow.json) retains six attempts, five complete usage
receipts, the unknown timeout, commands, responses, denials and separate lead
inspection. Public responses replace private fixture/interpreter paths with
placeholders; their public hashes and private native hashes have separate labels.
The plugin payload remains version 0.1.3; the generated example remains 0.1.1.

| Condition | Arm | Result | Processed tokens | Native list USD | Elapsed seconds |
| --- | --- | --- | ---: | ---: | ---: |
| Original cold task | Codex with | Interpreter unreachable in native sandbox; cause unknown; no package | 414,884 | Unknown | 150.907 |
| Original cold task | Codex without | Timed out; no complete native usage | Unknown | Unknown | 180 limit |
| Verified interpreter | Claude without | Wrapped command denied; no package | 73,265 | 0.1186426 | 27.157 |
| Verified interpreter | Claude with | Core build/recovery accepted; ZIP inspection completed by lead | 165,138 | 0.1402778 | 37.596 |
| Interpreter and direct commands | Claude without | Core build/recovery accepted; ZIP inspection completed by lead | 109,083 | 0.1258618 | 38.940 |
| Interpreter and direct commands | Claude with | Core build/recovery accepted; ZIP inspection completed by lead | 139,620 | 0.1075118 | 31.703 |

Both direct-command arms produced the same package. Both first-condition arms
initially issued denied wrappers. The baseline stopped and reported the denial;
the plugin arm retried an already permitted direct helper prefix. One run per arm
cannot attribute this retry difference to the skill. Both baselines read the same
SKILL.md, README and helper from their fixtures: the contrast is native plugin
auto-loading versus source-guide reads. This small assisted pilot establishes no
general quality, cost or speed advantage. Fixed within-host order, caching,
different tool turns and supplied interpreter/command guidance limit comparison.
Wall time includes client overhead; processed tokens include repeated context.
Native prices are list/API-equivalent receipts, with invoice allocation unknown.

The output is deterministic arrangement of the supplied original example,
with editable instructions. It is a free supporting tool. The earlier
[research-brief outcome comparison](outcome-comparison.md) remains the evidence
for actual source-derived writing; those six drafts also showed no clear paid
advantage. Human cold use and buyer value are unmeasured.

## First-run dependency and permission checks

Before asking a model to run the multi-step build, verify Python 3.10 or later
inside the same execution boundary. A successful interpreter in the lead shell
does not establish access inside another native host. Resolve the actual
installed executable; a missing alias is not permission evidence.

Codex CLI 0.159.3 provides `codex sandbox --permission-profile NAME --cd DIR --
COMMAND...`. Its built-in read-only profile is `:read-only`; `:workspace` permits
workspace writes. These names differ from the older `--sandbox workspace-write`
flag. Use the installed CLI help and the current
[permission profiles](https://learn.chatgpt.com/docs/permissions). A dependency
diagnostic must retain the existing boundary and record its exact grants.

All three retained non-model diagnostics used a CLI-only profile extending
`:read-only` with an exact Python-directory read grant and network disabled.
Both direct-process diagnostics returned Windows access denied; the executable
path separator varied. System PowerShell started,
but could not resolve that executable. Its process exit was zero because no
native child set an exit code; the stderr still proves the interpreter failed.
The original Codex model session itself reported command-not-found, a distinct
observed failure from these separately configured direct-process diagnostics.
No full-access/unelevated switch or broad global grant was made. Codex package
execution remains unresolved on this machine. The
[Windows sandbox guide](https://learn.chatgpt.com/docs/windows/windows-sandbox)
describes supported diagnosis and read-access controls; it does not establish
the cause of this local failure.

In the Claude trials, restricted mode explicitly exposed Bash, Read and Skill.
`dontAsk` denied unapproved commands. The generator prefix was permitted; shell
variables, `cd` wrappers and appended commands could fall outside that prefix.
Both recovery arms received identical guidance to issue one direct command:

```text
PYTHON -B source-plugin/scripts/package_lab.py scaffold source-plugin/examples/research-brief.json scratch/<new-directory>
PYTHON -B source-plugin/scripts/package_lab.py check scratch/<new-directory>
PYTHON -B source-plugin/scripts/package_lab.py pack scratch/<new-directory> scratch/<new-export>.zip
```

Replace `PYTHON` with the verified executable, and use absent output paths.
Do not expand permissions to accommodate arbitrary generated code. Follow the
current [Claude permission rules](https://code.claude.com/docs/en/permissions).
Both Claude arms used or attempted read-only Bash inspections beyond the helper
prefix, despite the assistance prompt requiring Read for ordinary inspection
and prohibiting other commands. Some were classified safe and ran; others were
denied. This remains a prompt-instruction compliance gap. Lead acceptance of
core build/recovery does not close it. These tool rules are not an operating-system
sandbox or universal filesystem boundary.

## Preservation, interruption and inspection

The supplied helper returns actual errors for occupied outputs and invalid
specifications. Keep those outputs intact and choose a fresh sibling path.
The complete MIT example notice remains distinct from the Apache-2.0 tooling
licence. Generation retains supplied text; it does not provide legal approval.

Retain stdout/stderr while a native process runs. The first Codex runner lost
partial stdout on timeout, so its commands and token expenditure are unknown.
The later runner streamed both traces to owned files before starting the process.
The timed-out process tree was stopped only after its owned marker/PID was
revalidated. A later lead readback confirmed source/protected bytes and no new
scratch artifacts; it cannot recover the missing model trace.

Native model ZIP-entry inspection was not completed in the successful Claude
sessions. The lead separately read each ZIP, checked entries/CRC, compared
licence bytes and checked generated sources through the supplied helper. Preserve
that distinction in support records; the native response alone does not prove
archive contents. Expected source contains five files, with no customer work or
new account connection included.

The owned temporary Codex plugin was removed through the native CLI. Its cache
and profile are absent and parsed global configuration semantics are restored.
Claude used session-only `--plugin-dir` paths. All six attempts are terminal;
private fixtures and traces remain for review. No watcher or server was installed.
The unblinded source maker performed the lead inspection. Its timestamp in the
public record is the publication snapshot stamp; inspection duration was not
separately measured. Claude trial result-JSON hashes link directly to the
accounting receipts, while JSONL trace and response hashes retain separate scopes.

This evidence awaits its own exact-revision publication review and CI. BL-01
remains 2/4. Original response-suite length/advice failures, native Codex execution,
human cold use, actual Dots account eligibility, catalog/directory release and
commerce remain open.
