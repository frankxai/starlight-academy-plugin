# Current release checkpoint

Builder Lab 0.1.1 was independently accepted and merged in [PR12](https://github.com/frankxai/starlight-academy-plugin/pull/12). Scoped BL-02 reporting adoption is complete. The current 0.1.2 candidate repairs implicit triggers and unsupported earnings-interface guidance. Its [native comparison record](native-comparison.json) retains actual responses, baseline results and failures. See the [evaluation method](native-evals.md) and [current usage report](reports/2026-10-02.md).

The 17bf5ad Claude pilot selected four of five intended skills; the packaging case missed while still scoring 1 under heuristic graders. The intended skill fired 3/3 after the ba1162a description change. The unchanged earlier description fired 1/2 across dfe34dd and17bf5ad, so run variance is not excluded. One reply still gave incorrect empty-directory advice; two met the core command/licence contract. Output length misses are separately recorded. The earlier earnings case failed lead review despite its heuristic pass; the revised map skill gave evidence-based verification steps in its observed rerun. Generic baseline replies often meet the same contract. No general performance advantage is inferred.

The output-length proxy exceeded 180 in 26 of 38 limit-bearing replies: 15/19 with the plugin and11/19 without. The proxy counts whitespace-delimited tokens, including Markdown pipes and separators; it can overcount words in tables. This is a descriptive small pilot, with no causal arm comparison. Under this conservative proxy, no with-arm full-fixture acceptance is recorded for any of P1 through P5.

Current source review, native Codex 0.1.2, runtime disable, catalog registration and actual Dots eligibility remain open. Paid release also requires a selected buyer workflow, seller/rights evidence and a verified sandbox delivery lifecycle. The known USD figures are native list-price estimates. Cash, invoice allocation and ROI remain unknown.

## Historical snapshots

The dated sections below preserve earlier source and receipt scopes. Their pending states are historical; the current machine-readable state is [release.json](release.json).

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
