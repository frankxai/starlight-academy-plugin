# Current release checkpoint

Builder Lab 0.1.2 source and reporting corrections were independently accepted and merged in [PR13](https://github.com/frankxai/starlight-academy-plugin/pull/13#issuecomment-5948724619). [PR14](https://github.com/frankxai/starlight-academy-plugin/pull/14) prepares 0.1.3 with shorter response guidance and an explicit requirement that scaffold and ZIP targets be new paths. Source acceptance for the new revision awaits its own review and CI.

The [0.1.3 native record](native-0-1-3.json) retains 17 fresh model runs and both tested source payloads. At 5a1624c, Claude selected the intended skill in all five positive cases once. The role table and packaging reply meet the 180-word proxy; research, meeting and rights replies exceed it. The collision reply still gives ambiguous empty-directory advice. The generator independently rejected an existing empty target and preserved it. These are descriptive observations with selected plain-host controls; they establish no general advantage.

Two fresh Codex sessions report all three repository skills when enabled and none when disabled. Global metadata stayed unchanged and the temporary profile was removed. This proves the scoped catalog toggle. Codex's P3 reply stayed generic because the unchanged prompt forbids commands and it did not read the bundle. Plugin registry installation, removal and broader host behavior remain open.

The [dated usage report](reports/2026-10-02.md) includes 116 attributed receipts through the first PR14 review: 81 complete token receipts and 35 incomplete ones. The final correction review will postdate this snapshot. Dots eligibility, catalog release, buyers, seller/rights evidence and sandbox delivery remain open. Native list-price costs, allocated invoices, cash revenue and ROI have separate evidence requirements.

## Historical snapshots

The dated sections below retain their original source and receipt scopes. Their pending states are historical; the current machine-readable checkpoint is [release.json](release.json).

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
deduplication. The final delta returned PASS at `afdde34`; CI passed and PR #4 merged the identical source tree as `0d77f5c`. Post-merge CI passed. The later native-host receipts still need their scoped independent acceptance.

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

## Observed native host scope

Claude Code 2.1.287 invoked all three skills and returned eight constrained
responses accepted by the lead. A separate restricted trial executed the exact
scaffold, check and pack commands. The lead inspected the generated ZIP and
confirmed its expected hash and retained MIT example licence text.

Codex CLI 0.159.3 loaded and read all three installed skills. It returned eight
responses; the lead accepted seven and flagged P2's unlabelled synthetic example
as falsely described supplied evidence. Three earlier discovery failures and
their usage remain in the record. Independent acceptance is pending.

[Host verification](host-verification.json), [actual responses](host-responses.json)
and [artifact evidence](host-artifact.json) retain the exact source revision,
hashes, assistance and limitations. [Native test notes](install.md) describe the
validated methods and remaining recovery gates. The temporary Codex installation
was removed through its native CLI; previous configuration semantics were restored.
Runtime disable, isolated triggering, plain-host comparison, final catalog and
Dots account access remain unfinished.

The eleven BL-01 receipts account for 619,260 processed tokens: ordinary input
129,454, cache writes 211,542, cache reads 183,559 and output 94,705. The known
Claude list-price subtotal is USD 1.763351; four Codex native costs are unknown.
One separate BL-02 reporting review adds 43,365 processed tokens and USD 0.214148,
bringing the twelve-receipt known subtotal to USD 1.977499. It returned ITERATE;
the corrected reporting packet awaits re-review. It is a checker receipt, not a
BL-02 maker run.

Native Codex input is partitioned into ordinary input, cache reads and observed
cache writes using the [OpenAI token accounting definition](https://developers.openai.com/api/docs/guides/prompt-caching).
The four displayed buckets are disjoint and sum to processed tokens. The v1 JSON
compatibility aggregates `fresh_input_tokens` and `fresh_io_tokens` already
include cache writes and must not be added again. Reasoning remains within
output. Whole-goal lead and source-maker usage, one timed-out review expenditure,
allocated invoices and cash ROI remain unknown.

## Version 0.1.1 patch evidence

The original 0.1.0 trials above remain dated evidence. The 0.1.1 patch separates
bundled synthetic examples from current user evidence and preserves existing
copyright when reusing the MIT demo. An intermediate Claude response contradicted
licence preservation; it remains failed in the [versioned trial record](native-patch-trials.json).
Final batches at `1af40b2` returned eight lead-accepted cases in each host. The
Codex temporary install was removed and prior configuration semantics restored.
These are prompted batches with assistance, not baseline or isolated-trigger proof.

A separate Claude model used the merged reporting tool to produce its actual
JSON and Markdown outputs. Codex compared both to the frozen generator, with
exact matches. The [adoption receipt](report-adoption.json) records the artifact
hashes, commands, assistance and scope. It covers one report-maker use; whole-goal
source-maker telemetry and cash remain unknown. Final patch publication review
is pending.

The updated snapshot contains 18 attributed receipts, 1,071,459 processed tokens and USD 2.499784 known list-price API-equivalent cost. Six Codex costs and all allocated invoices remain unknown. One subsequent patch review was stopped for a RAM reserve shortfall without final usage/cost or verdict. Its incomplete attempt is retained separately and excluded from complete-subset token totals.
