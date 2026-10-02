# Installed Codex interruption and artifact recovery

Observed 3 October 2026 (Amsterdam). The [JSON record](native-codex-installed-workflow.json) distinguishes the incomplete installed-agent attempt from the lead's successful artifact recovery. This extends the earlier [completed local-skill workflow](native-codex-completion.md) and [native version-update check](native-codex-upgrade.md).

## Installed workflow outcome

Codex CLI 0.159.3 used gpt-6.1-sol/high with workspace-write sandbox and tool network disabled. Its task-owned local marketplace installed Builder 0.1.5 from main `e2d9032a21184ddeda70ed46dca83555d20c3266`. All thirteen cached files matched Git blobs; the debug renderer showed three plugin skills, and the model read the installed build-portable-plugin skill and ran its cached tool.

The model restored two fresh ten-file Quote Desk folders, inspected source and notices, checked and repacked the first byte-identically, initialized the supplied fictional service workflow, authored buyer wording and saved revision 2. The maintaining account independently read both restored folders and matched every file to the retained archive.

The 240-second run timed out after 242.391 seconds. Nine completed shell-command items returned 0, but two inspection commands contained errors: inline Python quoting failed, and Get-FileHash was unavailable. The model repaired those inspections. Four package operations and three Quote operations completed; the full requested native reopen/export/verification and three adverse cases were not reached. No `turn.completed` event, final response or complete token/cost receipt exists. The owned worker is stopped. This attempt remains incomplete.

## Recovery after the stopped agent

A new ordinary Node process reopened the exact saved revision 2 and snapshot hash. The lead exported its 387-byte authored wording without editing it, retained the returned receipt hash outside the new buyer folder and verified the four-file packet against that value. All 48 original working files remained byte-identical. The buyer text is:

```text
Thank you for requesting an inspection of one unit at your workshop. The draft amount for one equipment inspection visit is EUR 120.00. Please confirm the equipment type and the inspection you need. The scope, tax treatment, final price and proposed timing next week all remain pending the owner's approval. No appointment or booking is confirmed, and this draft is not a binding quote.
```

Saved wording SHA-256: `4ec518754393e038688cea44b353f41d8c28a0a0671350257949db9143aff74f`. Retained buyer receipt SHA-256: `8e6910d6e36587f9017a1cc8933c388b82fe53f91f5fd6d2b032733d4473280a`. These identify the retained synthetic artifact; source, price, rights and delivery approval remain pending.

The lead separately exercised existing-output, wrong-hash and partial-marker refusals, preserving the previous edit/marker and leaving wrong-hash output absent. Those three adverse cases are lead-executed, separate from the incomplete native case set. The first lead export used unsupported guessed flags and was refused; its streams remain, then the documented skill flags succeeded in a fresh output. Six corrected deterministic calls produced three successes and three expected refusals, adding no model calls.

## Cleanup and next execution

The initial cleanup helper reused the workload-start memory reserve and blocked removal. Targeted ordinary cleanup then removed only the owned native selector/cache and temporary profile. Global configuration bytes and semantics matched the pre-install snapshot. Native fixture/runtime/cached-source bytes were preserved during the model run. Free RAM at cleanup was 3217 MiB, below the 4 GiB floor; further model runs were held.

Resume from the saved revision and inspect the documented command flags. Preserve existing outputs, choose fresh export paths and retain the returned receipt hash separately. Keep incomplete usage unknown and distinguish an agent continuation from ordinary process recovery. Admission for new model work remains separate from mandatory ordinary cleanup.

## Dots and remaining acceptance

OpenAI currently lists Pro 100, Pro 200 and Pro 500 access outside the EEA, UK and Switzerland for users over 18. Business Premium rolls out worldwide, and Enterprise requires workspace admin enablement. Eligible accounts may still lack the gradual rollout. Actual account/workspace access was not observed; the plan/workspace question remains pending. [Official Dots access guidance](https://learn.chatgpt.com/docs/dots).

This assisted synthetic trial supplied paths, a producer-known hash, fictional service/amount and explicit cases. Actual interruption occurred after a saved edit, without a mid-write interruption test. Manual unpacking, source inspection, editing and copying remain a capable alternative; comparative repair/time/cost and paid advantage are unmeasured. Full current native Codex/Claude behavior, outside-user use, Dots, directory, seller/rights and native commercial delivery remain open. [BL01](https://github.com/frankxai/starlight-academy-plugin/issues/3) retains 2/4 full accepted criteria.
