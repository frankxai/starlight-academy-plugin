# Completed current Codex workflow

Builder Lab 0.1.5 completed a controlled restore-to-quote workflow under Codex
CLI 0.159.3 on Windows. It restored inspectable source, authored and saved buyer
wording, reopened revision 2, exported four buyer files and verified a receipt
hash retained outside that folder. The lead read both ten-file source folders
and independently compared the ZIP, source, snapshot, buyer files and hashes.

The [JSON record](native-codex-completion.json) records source revisions,
disjoint usage and verification. This completed attempt is separate from the
[earlier timeout and access defect](native-codex-runtime.md); both remain in the
evidence history. Public fingerprints identify retained private traces. They do
not give a reviewer access to those traces.

## What ran

Builder source: `6392b1cc5b129d521752d6c47ec7b1f6b6aba35e`; Quote Desk source:
`8fbd3ae606f256d25a59aeea6a52ac063654ff5c`. Thirteen Builder files matched immutable Git blobs.
The ten-file Quote ZIP uses private adapter metadata and preserves both MIT
notices. Local `.agents` skill discovery was observed; no native plugin
installation, cache or marketplace listing was performed.

The native worker completed in 201.407 seconds, exit 0, within
a 240-second bound. Twenty command items contain seven package calls and six
Quote Desk calls: ten target successes and three specified refusals. The seven
other inspection commands succeeded. The final response met the requested
140-word limit: 117 whitespace-separated words.

Package checks covered fresh v1 restoration, check, exact-byte repack, fresh v2,
existing edited-output refusal, wrong-hash refusal and a marked-partial check.
The edited note and partial marker remain unchanged; wrong-hash output is absent.
This is refusal/recovery evidence, with no native mid-write interruption claim.

Quote Desk ran init, intake, edit, separate show, selected-revision export-buyer
and separate verify-buyer. The retained receipt hash is
`503a40fba34b6dde35485ca8661469cf0db4bd1f3d208575a7d8016ff40e3425`. The lead checked every receipt payload and the reopened
snapshot `e701345dde2379c9b92fa9288b35aab7596e96c58f9637076fa8bd99e15d838c`. Owner notes stay outside the buyer folder.
Receipt integrity does not approve the quote or identify a seller.

## Actual authored draft

The native model wrote this synthetic wording and saved it through the restored
Quote Desk skill. Scope, tax, price, timing, prose and rights approval remain
pending; outbound actions are disabled.

```text
Thank you for asking about an inspection of one unit at your workshop next week.

The draft amount for one equipment inspection visit is EUR 120.00. The scope, tax treatment, final price and timing remain subject to the owner's approval; the final amount payable has not been confirmed.

Please share the equipment type and model, any fault or concern you would like inspected, the workshop address and access details, and your preferred days next week. These details will help the owner confirm the inspection scope and whether the requested timing is available.

No appointment is booked or availability promised. This draft is not a binding quote or booking commitment. Please wait for the owner's confirmation of the scope, tax, price and appointment before making arrangements.
```

Quote SHA-256: `351af4a88ec4b6405e6be3299c016b87fa02af490f4d53a4ae7dd5eafef3cb1b`.

## Reusable usage import

The offline reporter now accepts a bounded, single-turn `codex exec --json`
JSONL stream:

```powershell
python -B docs/builder-lab/scripts/goal_report.py import-codex native.jsonl --goal BL-01 --id unique-native-attempt --source-url https://github.com/frankxai/starlight-academy-plugin/issues/3
```

It requires a thread start, turn start and final completed usage event. Failed,
truncated, duplicate-key, oversized and multiple-turn streams are refused.
Prompts, commands, reasoning text, paths, thread identifiers and results are
excluded. A canonical thread/usage fingerprint detects replays across renamed
imports, whitespace and ignored content changes; a separate hash identifies the
actual input bytes. Fingerprints provide deduplication, not provider authenticity.

This attempt reported 1,102,987 inclusive input tokens: 72,587 ordinary input,
1,030,400 cache reads and explicitly zero cache writes. Generated output was
4,117, including 404 reasoning tokens. Total processed was 1,107,104. Cash and
API-equivalent cost remain unknown. Missing fields stay unknown; a CLI schema
default never supplies a missing zero. Reasoning is never added to output again.

The [official JSONL guide](https://learn.chatgpt.com/docs/non-interactive-mode)
documents completion events. OpenAI's [usage guidance](https://developers.openai.com/api/docs/guides/agents-api/observability)
explains inclusive cached input and reasoning output, and warns that usage is
not final billing. The separate cache-write field was explicitly present in
this CLI's actual receipt; it is absent from that guide's sample. The installed
0.159.3 schema also exposes cacheWriteInputTokens with a default. API telemetry
and every CLI version should not be assumed to have the same fields.

The lead imported the real trace through both Python and the CLI and compared
the results. This is deterministic adoption by the lead; the native maker did
not use the reporting command. One receipt belongs only to BL-01.

## Remaining product gates

The run used supplied interpreters, paths, hashes, cases, adapter metadata and
fictional service facts. Manual extraction, source inspection and copying the
same wording remain capable alternatives. No paid or time advantage was measured.
The existing Python executable's sandbox-user modify ACL was neither changed nor
certified; Python 3.13 sandbox launch remains unresolved. Workspace sandbox and
network-disabled settings remained, without a network-denial probe. The user
config and checked runtime bytes were unchanged at run close; the temporary
profile was removed and the native worker stopped.

[BL-01](https://github.com/frankxai/starlight-academy-plugin/issues/3) remains
In review, two of four accepted criteria, due 8 October. This is one completed
assisted current-host workflow. Full two-host native use, isolated plugin
lifecycle, outside-user recovery and Dots evidence remain pending. Seller,
rights, purchase/refund/revocation/update and revenue evidence remain under
[BL-05](https://github.com/frankxai/starlight-academy-plugin/issues/9) and the
existing commercial goals. Policy loading is distinct from universal runtime
enforcement.
