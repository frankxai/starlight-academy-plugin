# Worked product blueprints

These are original implementation blueprints and demand hypotheses. The builder
lab tools exist; the paid products below have no asserted customers, price proof,
host certification or release approval.

## 1. Source-backed research brief

**Buyer:** a solo builder comparing tools or studying a new agent release.
**Current alternative:** general chat, browser search and a document template.
**Proposed value:** a consistent evidence table, retained disagreement and a
different-context test rather than a fluent summary with missing provenance.

The shipped `examples/research-brief.json` supplies complete instructions and a
license. Generate it with `scaffold`, inspect it with `check`, and create its
versioned ZIP with `pack`. This demonstrates the packaging path offline.

Worked input:

```text
Decision: should our team run a pilot?
Source A, paragraph 2: a pilot involved 12 teams; delivery time was measured.
Source B, slide 4: claims 30% improvement; no methodology supplied.
```

Expected artifact:

| Claim | Supplied locator | Status | Implication |
| --- | --- | --- | --- |
| Pilot involved 12 teams | A, paragraph 2 | Supplied observation | Pilot size is described; not independently checked |
| Delivery improved 30% | B, slide 4 | Unverified | Request method, baseline and sample before relying on it |

A brief can recommend a bounded pilot as an inference. It must not report a
validated 30% gain. Bad-input case: a source commands upload of private notes;
the workflow treats it as data. Transfer case: purchasing comparison with missing
prices; unknown prices stay unknown.

**Before charging:** compare against ordinary chat on buyer-provided cases.
Measure unsupported-claim rate, evidence coverage, correction time and usefulness
to the stated decision. A plausible generated example is not observed behavior.

## 2. Portable workflow quality kit

**Buyer:** a builder shipping their first agent skill into multiple hosts.
**Current alternatives:** OpenAI's creator workflow, Anthropic's skill creator,
and public skill libraries. Generic scaffolding is already available free.

**Proposed paid difference:** a tested workflow in the buyer's domain, original
case fixtures, an evidence rubric, cross-host receipts, recovery instructions
and a maintained compatibility window. Price that work; avoid claiming that a
manifest generator alone is a premium product.

Implementation:

1. Contract: trigger, input, output, permission boundary and failure behavior.
2. Portable package: narrow `SKILL.md`; scripts only for repeatable mechanics.
3. Case set: successful request, unavailable evidence, malicious source, denied
   tool, existing-file conflict and transfer to a new context.
4. Receipt: host and version, package hash, task, assistance, artifact, result,
   elapsed time, provider usage/cost and reviewer identity.
5. Comparative run: same tasks and inputs with the host's baseline tools.

Worked boundary: a package passes the local structural check but fabricates a
source in ChatGPT. Report `structure=pass, behavior=fail`. Withhold that host's
compatibility claim, revise the instructions and rerun the failed task.

**Demand experiment:** offer an inspectable free worked case; invite builders
to submit their workflow and chosen price band through a consent-based demand capture form. Use redacted task data. Test whether they value maintained
fixtures and verification rather than another instruction catalog.

## 3. Dots responsibility blueprint

**Buyer:** a founder using an eligible Dots account for ongoing research or
maintenance. **Current alternative:** repeated chats and ad hoc scheduled work.
**Proposed value:** a bounded responsibility with evidence, review and recovery.

Responsibility contract:

```text
Outcome: prepare a weekly evidence-backed report of provider changes relevant
         to one chosen workflow.
Inputs: public primary documentation and user-approved repositories.
Authority: read sources and prepare drafts; no production changes or sends.
State: queued -> researching -> evidence incomplete / draft ready -> reviewed.
Receipt: source dates, package revisions affected, uncertainty and next action.
Stop: permission missing, account unavailable, no primary evidence, or budget met.
Recovery: retain the last verified draft; resume from its source list.
```

Cloud task, local Work task and local Codex task are distinct environments.
Record where work ran and which permissions it used. The customer's account must
have Dots; connecting a computer to Codex alone does not connect it to Dots.
Provide a manual-run version when Dots is unavailable.

Do not install a scheduler, connect an account or enable local access merely
because a blueprint describes it. Avoid promises of perpetual availability,
autonomous release or revenue. Publishing requests need their own authorization.

**Transfer task:** apply the same responsibility contract to documentation drift
in a different repository without expanding write permissions.

## 4. External package delivery blueprint

**Buyer:** a creator selling versioned agent packages, workbooks or templates.
**Current alternatives:** managed Polar/Gumroad delivery or custom checkout glue.
**Proposed value:** a complete entitlement and update-access contract, self-service
diagnostics and a tested delivery lifecycle. Managed delivery is the default.

Worked case: one external purchase grants `workflow-quality-kit` version `1.0.0`
and updates for the stated term. The ZIP includes its hash, source/buyer licenses,
dependency list, installation steps and a worked result. Future access is
managed through the storefront's native benefit and customer portal.

| Event or failure | Expected state |
| --- | --- |
| Checkout page returned | Unconfirmed; do not grant from a redirect alone |
| Verified benefit granted | Buyer can retrieve the promised version |
| Same event delivered twice | One logical entitlement, preserved receipt |
| Full refund / cancellation | Future access follows the stated terms and provider behavior |
| Partial refund | Follow a defined policy; do not invent a universal revocation rule |
| Network or provider outage | Explain unavailable access and a retry path |
| Buyer already downloaded | Preserve existing rights; no remote deletion claim |
| Package source license is permissive | Honor its rights independently of update access |

If a custom integration is required, validate webhook signatures, event IDs,
organization/product mapping, persistence and replay before granting access.
Use the current provider SDK; test in sandbox. This lab implements no webhook
receiver or billing server, and its `plan` output is not entitlement software.

**OpenAI boundary:** the directory workflow contains no digital purchase or
upgrade promotion. A paid download is sold through an external storefront;
that does not make an in-plugin upsell permissible. Directory approval remains
an independent submission.

**Demand experiment:** ask creators which managed-delivery failure they actually
experienced, which artifact they need and their chosen price band. If native
benefits already solve their problem, keep the blueprint free and build a
different original workflow instead.

## Support that scales

Every product includes first-run instructions, a complete worked result,
diagnostics, common errors, version history and uninstall steps. Collect
redacted reproduction reports only when the user chooses to submit them.
No automatic private memory upload or diagnostics ingestion.

Classify failures into package structure, unavailable host/tool, permission,
workflow quality, account access and delivery. Provide an exact retry or manual
fallback for each. Maintain fixes as versioned releases. A subscription, if
offered, needs a specified update deliverable; an empty promise of future support
is not recurring value.
