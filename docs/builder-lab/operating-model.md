# Builder Lab operating model

This programme turns the existing lab into reusable, measured workflow products.
Its [SMART goals](GOALS.md) are a dated projection of owning GitHub issues.
[Project 8](https://github.com/users/frankxai/projects/8) remains the portfolio
interface. No additional command centre or global task queue is created.

## Where to manage work

| Surface | Purpose | Authority and update rule |
| --- | --- | --- |
| Owning repository issue | Buyer outcome, acceptance, target date, budget proposal, dependencies, work acknowledgement | Execution truth; update on material evidence or handoff |
| GitHub Project 8 | Portfolio status, target date, known spend, next gate and links | Dated projection; candidate dates do not admit workers |
| PR and versioned Markdown | Inspectable implementation, research, rights, tests, release and rollback | Exact commit and checks prove source, deployment receipts prove live behaviour |
| Existing private objective ledger | Cross-brand priority and original intent | Preserve existing objectives; at most three admitted objectives |
| Slack `#starlight-systems` | Issue-linked exceptions, blockers and coordination | Conversation context; decisions return to the issue |
| Slack `#brand-starlight` | Reviewed buyer-language drafts and brand decisions | Publishing and outreach require the applicable owner gate |
| Existing revenue/accounting systems | Paid receipts, refunds, tax and cost reconciliation | Private source records; publish sanitized totals with coverage |

Slack workspace/channel discovery passed on 1 October 2026. No message, channel,
app or recurring job was created. Existing digest delivery remains tracked in
[config issue 50](https://github.com/frankxai/starlight-agent-config/issues/50).
Queen/Slack work and the token-tracker pulse bridge already have separate owners;
consume their reviewed contracts rather than replacing their lanes.

## R&D to revenue

| Stage | Required artifact | Exit evidence | Why fund this technology |
| --- | --- | --- | --- |
| Research | Buyer job, current official host rules, competitive/free baseline, dated uncertainty | A falsifiable problem and a transferable test | Avoid paying to rebuild free generic scaffolding |
| Engineering | Original domain workflow, complete examples, adversarial fixtures, rights inventory | Cold use succeeds; unsafe and missing-evidence cases stop correctly | Reliability and maintenance are customer value |
| Marketing | One truthful offer, inspected sample, role/reason/price demand fields | Qualified consented signals tied to a product | Select an offer from evidence before buying reach |
| Sales | Eligible seller, terms, actual channel fees, supported entitlement | Sandbox purchase/access/refund/update proofs and release approval | Native delivery reduces integration and operating cost |
| Support | First-run guide, known limits, recovery, version/support period | A buyer completes the task without private founder assistance | Self-service protects contribution and founder capacity |
| Evolution | Defects, refunds, comparative task success and attributable receipts | Continue, repair or park decision with evidence | Spend follows observed outcomes rather than activity counts |

The free Apache-licensed lab teaches portable skills. A paid offer must supply
original domain value, maintained fixtures or eligible services outside the
directory candidate. [OpenAI directory policy](https://developers.openai.com/plugins/plugin-guidelines)
currently forbids digital selling and indirect upgrade promotion inside plugins.
Neither directory inclusion nor lab alignment establishes creator revenue share.

## Bounded work packet

Before execution, the owning issue records: goal ID, buyer result, exact repo and
branch, explicit paths, acknowledged maker, independent checker or review hold,
acceptance fixtures, source revision, machine admission, proposed API-equivalent
cost ceiling, actual billing basis, stop rule, receipt destination and next check.
An assignee or persona name is not a live agent. Clear active claims on handoff.

Admit one local implementation lane now. A future parallel lane requires explicit
dispatch, independent files, machine admission and owner acknowledgement. Proposed
budgets in `goals.json` authorize no payment or unattended runs. Limit a scoped
fix/review loop to three attempts; stop on a repeated fault, missing rights,
capacity hold or cost ceiling and retain the usable artifact.

Monday reviews buyer evidence and admits bounded work. Thursday reconciles source,
board and blockers. Sunday records accepted/slipped/held outcomes. These are manual
cadence contracts, not installed schedules. W40 is not silently admitted from W39.

## Measure without inventing returns

Run from the repository root:

```sh
python docs/builder-lab/scripts/goal_report.py report docs/builder-lab/goals.json docs/builder-lab/evidence.json
python docs/builder-lab/scripts/goal_report.py report docs/builder-lab/goals.json docs/builder-lab/evidence.json --format json
python docs/builder-lab/scripts/goal_report.py import-claude RECEIPT.json --goal BL-01 --id review-unique --source-url https://github.com/frankxai/starlight-academy-plugin/pull/4
```

The importer retains usage, receipt hash and attribution, never model responses,
prompts or credentials. Keep raw receipts and invoices private. Multiple copies
of one receipt must fail rather than double-count. A caller supplies audited,
sanitized evidence; this CLI does not inspect actual agents, invoices or GitHub.

The report displays four disjoint buckets: ordinary input, cache writes, cache
reads and generated output. Their sum is processed tokens. Thinking is included
in output. In the v1 JSON output, the compatibility key `fresh_input_tokens`
aggregates ordinary input and cache writes; `fresh_io_tokens` also adds output.
These aggregate keys must not be added to the four buckets again.
Partial token receipts are counted and excluded from the complete subtotal.
Cost subtotals remain separated by the supplied `cost_basis`; mixed bases have
no combined total. Invoice totals are labelled as a known subset, with the count
of runs missing invoice evidence. Claude CLI list-price costs are API-equivalent values; subscription invoices
and actual cash remain separate. A telemetry gap is never a free run.

Cash contribution = receipts excluding tax and refunds minus variable cash cost.
Cash ROI = (contribution minus allocated investment) / allocated investment.
It requires one period, currency, `reconciled_by` and a timezone-bearing
`reconciled_at` at or before the evidence observation, on or after the period's
end date in the declared reconciliation offset.
The reconciliation remains a caller attestation. The calculated ROI does not
certify cash or invoices. Unknown inputs stay unknown;
zero investment gives undefined ROI. Founder time, subscription allocation and
FX must be explicitly included in an investment record if used. Revenue targets
are objectives, not forecasts. No useful-life savings or customer success is
inferred from passing source tests.

Variable cash cost and allocated investment must be disjoint, with the allocation
basis recorded privately. Refund-dominated periods may have negative net receipts.
This source projection checks data shape and arithmetic; the accountable human
must reconcile invoices, bank/merchant records and whether costs were included
once. It cannot certify a submitted financial record.

Known invoice cash requires an anonymized `invoice_id` and evidence link. The
same invoice cannot be attributed to two runs here. Shared subscription invoices
need the existing accounting owner's external allocation before inclusion.

Shared dependencies retain their existing owners:
[usage capture 93](https://github.com/frankxai/agentic-ops/issues/93),
[cost baseline 85](https://github.com/frankxai/agentic-ops/issues/85),
[legal entities 77](https://github.com/frankxai/agentic-ops/issues/77),
[demand doors 62](https://github.com/frankxai/agentic-ops/issues/62) and
[agent accountability 51](https://github.com/frankxai/agentic-ops/issues/51).
