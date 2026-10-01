# External package distribution

This guide and its commerce skill/tool are outside the directory-candidate plugin.
They prepare storefront artifacts in the publisher's own workspace. They contain
no checkout for this lab. Use Python 3.10+; no account is needed for offline drafts.

# Agent ecosystems and package economics

Research snapshot: 2026-10-01. Recheck volatile rules before implementation or
release. These are public requirements and documented capabilities. They do not
establish a particular account's access or a lab's private commercial strategy.

## What each layer does

| Layer | Role | Evidence to collect |
| --- | --- | --- |
| Host | Runs work, manages tools and permissions | Exact product, version, plan and environment |
| Skill | Supplies task instructions and selective resources | Trigger accuracy, output contract and behavior tests |
| Plugin | Packages capabilities for installation | Manifest, file layout, version and compatibility |
| MCP | Connects data or actions when needed | Transport, auth, tool behavior and permission boundary |
| Plugin marketplace | Catalogs installable packages | Source revision, install/update/uninstall observations |
| Storefront | Collects payment and delivers purchased access | Eligibility, fee plan, entitlement and refund evidence |
| Blueprint | Explains a reproducible implementation | Complete worked example, prerequisites and known limits |

### OpenAI Dots, Work and Codex

Dots can delegate work to cloud and connected-computer tasks. Installed plugins
and connected accounts determine available tools. Local skills require a connected
computer. Do not infer Dots access from a working Codex installation.
[Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

Dots availability is a rollout and account question. The launch help page lists
plan and regional restrictions, including restrictions on Pro availability in
the EEA, Switzerland and UK. Check current account eligibility before selling a
Dots-specific promise.
[Getting started](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot).

Author new portable packages with root `plugin.json`, `skills/<name>/SKILL.md`
and optional root `mcp.json`. OpenAI metadata belongs under
`extensions.com.openai`; a legacy overlay is a fallback, not a merged authority.
Catalog source paths are relative to the marketplace root. A local install and
a public directory listing are separate operations.
[Packaging](https://developers.openai.com/plugins/build/plugins),
[portable schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).

ZIP upload creates a draft followed by scans and review. Skills-only submissions
do not require MCP demo/test cases. An initial MCP review currently requires five
positive and three negative cases; only one MCP server can be connected per plugin.
Adding MCP to an existing skills-only directory plugin is currently unsupported.
Plan a separate integration package when needed rather than assuming that upgrade.
[Submission](https://developers.openai.com/plugins/deploy/submission).

Directory plugins currently prohibit digital-product commerce and upgrade
promotion, including indirect freemium upsells. Existing paid-account features
may be used. Keep external digital sales outside the plugin experience. Do not
interpret an external checkout as permission to add a purchase CTA to the plugin.
[Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines).

### Anthropic and Google

Claude Code marketplace catalogs use `.claude-plugin/marketplace.json` and native
plugin metadata. Pin source revisions and verify installation in Claude. Portable
files alone do not prove every host interprets them identically.
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

Anthropic's engineering guidance starts with simple composable workflows and
adds autonomy where the task warrants it. Read its explanation of tool design,
evaluation and feedback before turning a deterministic pipeline into a swarm.
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

Google's Gemini function-calling interface uses structured function declarations.
A portable instruction pack is useful context, but it does not install functions
or create an authenticated connector. A Google adapter requires implementation
and host-specific tests.
[Function calling](https://ai.google.dev/gemini-api/docs/function-calling).

## What the labs want, and what buyers may reward

The first column below is grounded in the cited developer interfaces. The other
columns are business inferences to test, not private lab policy or proven demand.

| Documented direction | Inferred platform incentive | Customer-value hypothesis |
| --- | --- | --- |
| Portable skills and plugin packages | More useful workflows with less setup | A workflow that survives host changes |
| Tool auth, permissions and review | Reliable access with bounded authority | Fewer mistakes and a clear recovery path |
| Scans, metadata and submission checks | A directory users can trust | Inspectable source and tested behavior |
| Agent workflow and evaluation guidance | More dependable task execution | Measured improvements on the buyer's real task |
| Structured function calling | Software actions with explicit inputs | Integration with data the buyer already owns |

No source here establishes automatic payment to skill authors, a guaranteed
directory ranking or a general lab revenue share. Build a revenue model from
actual external purchases. Do not confuse installs, stars or token volume with
paying demand.

Free host tools make generic scaffolds inexpensive substitutes. Potential paid
value comes from domain-specific workflows, original examples and datasets,
repeatable tests, thoughtful failure recovery and maintained compatibility.
The product needs to prove those differences before pricing. Open-source code
can be sold legally under its license, but copied public instructions offer
little exclusivity. Record third-party attribution and sell original added value.

## External channels

| Channel | Suitable role | Boundary and primary source |
| --- | --- | --- |
| Polar | Managed file/repository delivery, one-time packs, optional update subscriptions | Confirm organization plan; use managed benefits before building billing infrastructure. [Downloads](https://polar.sh/docs/features/benefits/file-downloads), [GitHub access](https://polar.sh/docs/features/benefits/github-access) |
| Gumroad | Downloads, books and blueprints; optional Discover exposure | Direct and Discover fees differ. [Pricing](https://gumroad.com/pricing) |
| Whop | Digital packages and access; affiliates when useful | Optional billing, tax and orchestration fees add to base processing. [Fees](https://docs.whop.com/fees) |
| Stripe | Owned checkout where its responsibilities fit | Standard Payments and Merchant of Record arrangements differ; delivery, tax and entitlements need explicit design. [Payments](https://docs.stripe.com/payments), [Managed payments](https://docs.stripe.com/payments/managed-payments) |
| Etsy | Eligible original design downloads or workbooks | AI prompt bundles are excluded; AI-created work needs disclosure where required. [Creativity standards](https://www.etsy.com/legal/creativity/) |
| OpenAI / Claude catalogs | Workflow discovery and installation | Directory rules are host-specific. Catalog availability provides no automatic payment rail. |

### Polar delivery contract

Use a versioned ZIP and hash. Define the buyer's use rights and update period.
Attach file-download or GitHub-access benefits to the external product. GitHub
access normally requires an organization repository and a separate Polar app;
paid organization collaborator seats can add costs. Prefer file delivery when
repository access adds no buyer value. Verify
grant, duplicate purchase, partial/full refund, cancellation and portal access
in the sandbox. A successful checkout redirect is not an entitlement.

For additional software requiring validation, Polar provides customer-portal
license-key endpoints; the customer's key and organization ID are distinct from
a merchant admin token. Never distribute the latter. Customer-owned instruction
files remain copyable. Revocation can stop future access; it cannot delete a
previous download or revoke rights already granted by an open-source license.
[License keys](https://polar.sh/docs/features/benefits/license-keys),
[sandbox](https://polar.sh/docs/integrate/sandbox).

Avoid a per-run license check for plain skills: it adds friction and turns an
offline instruction pack into a network dependency. Managed delivery plus paid
access to future releases is often sufficient. Use enforcement only where the
customer value and license terms justify it.

### Model costs honestly

On the research date, Polar Starter lists 5% + $0.50 and a 1.5% international-card
addition; grandfathered plans and paid plans differ. Fees apply to the transaction
including tax, and original processing fees are retained after refunds. Check the
actual organization rather than assuming the old 4% rate.
[Current fees](https://polar.sh/docs/merchant-of-record/fees).

Gumroad lists 10% + $0.50 for direct sales and 30% through Discover. Whop lists
2.7% + $0.30 for domestic cards, with international, currency-conversion and
optional feature charges. These are base observations, not complete net-margin
estimates. Use the cited pages and actual account configuration above.

The offline calculator accepts explicit fees in one currency. Its formula is:

```text
fee = price excluding tax × (1 + tax rate) × fee rate + fixed fee
contribution/order = price × (1 - refund rate) - fee - affiliate commission
                     - variable cost - support reserve - expected dispute cost
monthly contribution = contribution/order × assumed orders
                       - maintenance allocation - acquisition spend
```

It conservatively assumes no affiliate refund clawback. FX, payout fees, income
tax and founder time need additional inputs or separate analysis. Customer-owned
keys or subscriptions reduce provider-compute costs for us; they still consume
the customer's money and quota. Measure total task cost and assistance burden.

## Evidence and maintenance

Keep a source record with URL, read date, applicable surface and affected decision.
Refresh on a provider release or before a submission. Re-run versioned task cases
when instructions, scripts, auth or host versions change. Promote a compatibility
claim only after its test passes. Preserve the failed result and the exact revision.
Automated monitoring should draft changes; it must not silently rewrite live
instructions, publish products or expand its own permissions.

## Run the external tools

From the repository root:

```text
python -B docs/builder-lab/scripts/distribution_lab.py economics SCENARIO.json
python -B docs/builder-lab/scripts/distribution_lab.py plan PRODUCT.json
python -B -m unittest discover -s docs/builder-lab/tests -v
```

A scenario uses one currency, required `fee_rate` and `fixed_fee`, a positive
`price_ex_tax` and integer `monthly_orders`. Optional fractional inputs include
`tax_rate`, `refund_rate`, `affiliate_rate` and `dispute_rate`. Optional monetary
inputs include `variable_cost`, `support_reserve`, `dispute_fee`,
`monthly_maintenance` and `monthly_acquisition`.

Example scenario:

```json
{"currency":"USD","fee_currency":"USD","price_ex_tax":"30","tax_rate":"0.25","fee_rate":"0.065","fixed_fee":"0.50","refund_rate":"0.1","monthly_orders":10,"monthly_maintenance":"20"}
```

This produces $2.94 transaction fees, $24.06 contribution per assumed order,
and $220.63 monthly contribution after the supplied allocation. It is an
illustration, not an account quote or an earnings forecast. Input the actual
account rates and cost assumptions.

Example requirements request:

```json
{"name":"Research brief package","channels":["openai","claude","polar","gumroad","whop"],"openai_commerce":"usage-only"}
```

`plan` returns a draft and required evidence; it never certifies readiness or
consumes release receipts. Use the product owner's real release gate for that.
Etsy's `original-design` flag is a declaration, not an eligibility check.
OpenAI plugin use and external sales retain separate policies and approvals.
