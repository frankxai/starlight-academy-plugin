# Native restoration evidence, 2 October 2026

Builder Lab 0.1.4 restored an existing MIT quote package in one assisted Claude
Code 2.1.287 session. The skill was loaded through session-only `--plugin-dir`.
The actual trace has 12 generator commands: five succeeded and seven returned
the expected refusal. This is native workflow evidence for this version and
host; the current Codex execution and outside-user gates remain open.

| Native operation | Observed result |
| --- | --- |
| Restore, check and repack v1 | Ten source files restored; structural check passed; ZIP byte-identical to supplied download |
| Restore and check fresh v2 | Same ten file bytes; prior v1 preserved |
| Wrong expected checksum | Refused before requested output |
| Existing empty or edited destination | Both refused; existing work preserved |
| Check and pack a marked partial folder | Both refused; marker and original files preserved |
| Unsafe path and corrupted CRC fixtures | Both refused after checksum match |

The lead independently compared both restored folders with all input archive
bytes, checked the retained root and skill MIT licence hashes, and confirmed
the rejected output paths and partial ZIP did not exist. The model's final
response said 13 operations; its trace contains 12 generator calls. Five Read
errors include directory enumeration, binary-file inspection and three absent
files. The model disclosed filesystem uncertainty; the separate lead inspection
resolves that uncertainty without relabelling it as model-performed work.

The [source-bound JSON](native-restoration.json) retains the execution revision,
all 13 Builder Lab file hashes, relative commands and results, native usage,
trace/response fingerprints, correction and limitations. Runtime SHA-256 is
`03935e1c776218a8f00010acf213b31c48d14f1b6d89d4b60d24d849ba5a6cec`.
The execution revision is `1a1953264187f447d767dbd6d536f9f3f1d6c87b`.
These plugin bytes also match the nested `refinement_replay` in
[the prior source proof](restore-proof.json); that file's top-level replay is
historical and predates exact-byte/partial-marker refinements. Both are retained.

The supplied interpreter, paths, operation cases and expected producer hashes
are assistance. The quote manifest is a controlled trial adapter for the existing
accepted MIT source, not a published native quote plugin. The quote code was
not executed in this session. Its earlier deterministic save/reopen/export
remains separate evidence. Pre-marked partial-folder refusal is not a native
mid-write interruption test. No human cold trial or account installation occurred.

The one native workflow attempt reported 179,782 processed tokens across four
disjoint input/cache/output buckets and USD 0.1692548 in native list-price metadata.
The 296 thinking tokens are already within output. The 48.061 seconds include
client overhead. Root lead allocation, invoiced cash, revenue and cash ROI are
unknown. Deterministic Python/sandbox diagnostics are not model attempts.

## Codex on this machine

Codex CLI 0.159.3's deterministic sandbox probe could not spawn the installed
Python 3.13 executable. Two narrow per-invocation read profiles failed with
“elevated Windows sandbox requires effective :root read access.” The built-in
`:workspace` profile failed with `CreateProcessAsUserW failed: 5 (Access is denied.)`
even with the explicit interpreter path and `-B --version`. No new Codex model
attempt was made. Global settings and plugin configuration hashes were unchanged.
The root cause is unresolved beyond the observed child-spawn access denial.

Use the [support recovery guide](support.md) and current official
[Windows sandbox documentation](https://learn.chatgpt.com/docs/windows/windows-sandbox)
when diagnosing the same symptom. An ordinary terminal successfully running
Python does not prove the native sandbox can run it. These machine-specific
observations do not show that every Codex Windows installation fails.

## What remains

Manual extraction with independently supplied hashes and source inspection is
a capable alternative. This single assisted session has no control arm or measured
repair/time advantage. Existing comparison parity and old failures remain in the
record. Current Codex execution, isolated discovery, outside-user recovery, Dots
eligibility and directory acceptance remain pending in [BL-01](https://github.com/frankxai/starlight-academy-plugin/issues/3).
Actual seller, rights, terms and purchase/refund/revocation/update evidence remain
pending in [BL-05](https://github.com/frankxai/starlight-academy-plugin/issues/9).
No paid readiness or marketplace approval follows from this trial.

## Later Codex observation and Windows fix

The [2 October Codex record](native-codex-runtime.md) adds an actual assisted
restore-to-quote attempt using existing Python 3.11 and the same 0.1.4 Builder
source. Its 19 target operations were observed before timeout; complete session
and usage evidence is absent. It revealed unreadable source folders for the
maintaining account. Version 0.1.5 corrects fresh Windows folder ACL inheritance.
The separate model-free replay proves ordinary-account source reading/editing,
repack parity, preserved edits and fresh-sibling recovery. Original denied folders,
Python 3.13 errors and earlier native receipts remain unchanged. These later
observations supersede the earlier "no new Codex model attempt" statement only
for their dated scope. BL-01 two-host/cold-use/Dots acceptance stays pending.
