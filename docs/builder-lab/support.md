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
historical; new host/cold-user and commercial lifecycle acceptance is pending.
