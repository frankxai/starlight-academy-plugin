# Builder Lab release checks

Run `python -B scripts/verify_builder_release.py` from a checkout with Python
3.10 or later. It runs scaffold, check, pack, restore and repack, checks that
existing work survives rejected generation, exercises usage import and external
distribution commands, and checks local documentation references. It uses only
the standard library and removes its own temporary generated artifacts.

GitHub Actions runs the preservation, hostile-input, accounting and release
checks on Windows and Linux with Python 3.10 and 3.13. Action revisions are
immutable SHA pins. The workflow has read-only repository permission and does
not install packages, use provider credentials, activate plugins or publish.

## What must be proved separately

| Gate | Evidence required |
| --- | --- |
| Source integration | Green CI at the exact reviewed PR revision, secret checks, independent provider verdict, merge readback |
| Native host use | Loaded skill identity, actual case responses and artifacts, host/version, restrictions, source hashes and sanitized usage attribution |
| Catalog release | Both native manifests, the immutable Claude payload pin, Codex repo-backed source, install/disable/removal proof and release receipt |
| Dots | Actual account eligibility, supported local computer connection and one bounded responsibility trial, or documented ineligibility |
| Directory | Current rules, verified publisher identity, submission and actual approval state |
| Paid package | Buyer and price evidence, original rights inventory, approved seller/channel, supported entitlement, sandbox purchase/refund/update and release approval |

The [eight host cases](host-cases.json) cover constrained responses. A batch in
one session can show discovery and response behaviour; it cannot establish
isolated trigger precision, generated filesystem artifacts or an advantage over
the plain host. Those require separate executions and comparison evidence.

## Independent review and recovery

The October 2 review returned ITERATE, then PASS for the free source conditional
on CI. The follow-up added required notice inventory support, further portable
path checks, an observed sanitized native receipt fixture and invoice identity
deduplication. The final delta needs its own verdict before integration.

Review packets retain exact per-file SHA256 values privately. Public receipts
record the reviewed scope and source revision. A passed static review gives no
host, marketplace, legal or commerce approval.

Before catalog changes, verify the pinned Git revision contains byte-identical
plugin files after newline normalization. Preserve existing Academy plugin pins.
Rollback uses a normal revert PR and a new catalog revision; preserve older
immutable releases and customer work. Stop owned native test processes at
handoff. Hosted checks may finish independently in GitHub Actions.

The operating and commercial gates remain in the [programme issue](https://github.com/frankxai/starlight-academy-plugin/issues/5)
and [roadmap](ROADMAP.md). Cash revenue and ROI remain unknown until actual
seller receipts and disjoint costs are reconciled.
