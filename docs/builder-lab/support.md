# Self-service support and maintenance

The candidate lab and reporting tool run offline on Python 3.10+ using the standard
library. They do not need API keys, billing access or a hosted inference service.
Start with the [portable plugin guide](../../plugins/starlight-builder-lab/README.md)
and [operations commands](operating-model.md). Customers use their own supported
host and runtime. Dots availability must be verified for the actual account.

| Symptom | Recovery | Evidence to include in a safe issue |
| --- | --- | --- |
| Package path already exists | Pick a new output path; preserve existing work | Command, tool version, short error |
| Download hash mismatch | Preserve the ZIP; obtain the release hash independently from the trusted publisher/channel | Version, expected/actual public hash, no account token |
| Restore rejected or interrupted | Use the [restore path](restore.md); preserve partial output and prior versions, retry into a fresh sibling | Version, short error and anonymous case ID |
| Junction/reparse or cloud-placeholder rejection | Use an ordinary fully local directory, then check again | Relative affected path, no personal home path |
| Licence missing | Supply the complete authorized licence and inventory; identifier alone is insufficient | Licence ID and public upstream revision |
| Unknown spend or ROI | Supply a scoped usage receipt or reconciled financial evidence; do not substitute zero | Receipt type/hash and missing field names |
| Duplicate usage receipt | Remove the duplicate attribution, preserve the original receipt | Run IDs and receipt digests |
| Python missing from host command lookup | Verify the installed Python 3.10+ interpreter in the intended native host; use its exact path where allowed | Host/runtime version and sanitized short error |
| Explicit Python path returns Windows access denied | Stop execution claims; retain the native diagnostic and follow the scoped recovery below | CLI/runtime version, exit code and short sanitized sandbox error |
| Host cannot load the skill | Verify provider packaging and host/version support; use a clean copy | Host/version, manifest, reproducible non-sensitive sample |
| Marketplace rejects product | Preserve rejection and category reason; review policy before altering scope | Public policy link, sanitized rejection |

The supplied tests cover source behavior only. Provider directories, host workflows,
consumer remedies and paid delivery need separate evidence. File checks are not
malware certification and cannot prove the semantics of third-party skills.

## Support contract for a future paid pack

Before listing, state included artifacts, supported host/version, installation and
upgrade/uninstall steps, update period, compatibility limits, licence rights, known
failure modes and remedy route. Promise only an operating process we can maintain.
Provide a complete sample and recovery guide. Buyer support must be self-service;
do not create founder calls or custom delivery as a hidden product dependency.

Use the owning issue for reproducible bugs; separate sensitive security reports
through the existing private repository reporting route. Never ask customers to
post keys, personal prompts, invoices or raw provider payloads publicly. Receipt
hashes and anonymous case IDs are enough for ordinary triage.

At each release, inspect the exact version archive, licence/notices, working links,
clean-host first run, positive/negative cases and update/rollback path. Preserve
the prior approved package, checksum and release receipt. Corrections and refunds
flow through the actual merchant/channel contract. Count unresolved defects,
time to recovery, return rate and maintenance cash per product; use those values
in continuation decisions. No always-on support bot or recurring job is installed
by this document.

Builder Lab 0.1.4 implements checksum-bound source restoration, with a copied-skill
guide and preservation tests. This makes downloaded packages inspectable without
manual raw extraction. It does not verify Polar or any other merchant's purchase,
refund, revocation or update entitlement. Existing 0.1.3 native host receipts remain
historical. The [current native restore evidence](native-restoration.md) verifies
one assisted Claude workflow; Codex execution, outside-user and commercial
lifecycle acceptance remain pending.

## Native runtime recovery

Verify Python 3.10+ in the same native host and permission context used for the
package command. A normal terminal's success is not evidence that the host's
sandbox can spawn that interpreter. If command lookup fails, use a verified
installed interpreter path only when the current task permissions allow it.

If that exact path still returns Windows error 5 / access denied, preserve the
short error and stop reporting generated artifacts. Consult the installed CLI
help and current official [Windows sandbox guide](https://learn.chatgpt.com/docs/windows/windows-sandbox).
Investigate host/runtime compatibility through its supported controls. Keep
security checks enabled; do not disable the sandbox, grant broad root permissions,
change global account settings or weaken ACLs as a package recovery step.

If execution remains unavailable, return the source draft and exact commands
marked not-run. An already available supported host may run a separately scoped
trial, with its own permission and artifact evidence. Preserve the earlier
failure. Re-test the original host after a supported correction before asserting
two-host compatibility. The lab remains an offline free candidate.

## Windows output access in version 0.1.5

Use an ordinary project parent whose ACL admits the maintaining account and only
intended collaborators. Fresh restored folders inherit that parent's permissions
on Windows; POSIX folders stay mode `0700`. Verify reading and editing with the
maintaining account before using the package. Preserve unreadable older folders
and retry into a fresh sibling using 0.1.5. Do not take ownership or rewrite old
ACLs as a restore step. Existing destinations remain refused.

[The current Codex observation](native-codex-runtime.md) records a timed-out 0.1.4
model attempt and a separate 0.1.5 model-free correction. Existing Python 3.11 ran
the corrected sandbox commands; ordinary-account source reading, editing and
repacking passed. Python 3.13 and two PowerShell launch probes remain denied.
Test the exact executable in the intended sandbox before claiming compatibility.
A normal terminal's success or version output alone does not close host acceptance.
No new runtime, account permission, global sandbox setting or native installation
was introduced. Outside-user and commercial acceptance remain pending.
