---
name: design-ai-department
description: Triage and design one accountable AI department from a recurring workflow, including when not to automate, the smallest viable topology, human authority, evidence, evaluations, recovery, and portable package projections. Use when asked to design an AI team, agent department, governed workflow, multi-agent operating model, or installable department packet.
---

# Design AI Department

Design from work and authority, not from an agent roster. Produce one
`starlight.department_design.v1` draft for human review. This skill prepares a
design; it never deploys a department or grants runtime authority.

## Lead with maximum useful intelligence

Prompt the system to apply the maximum useful intelligence available: reason
deeply, generate and compare stronger approaches, challenge assumptions, use
approved tools and evidence well, and optimize for the highest-quality outcome
the current constraints can support.

Define performance through the named outcome and its evidence. Never optimize
for fluency, token volume, agent count, activity, or speed in isolation. Record
the intelligence mode as `maximum-useful-intelligence` and measurement status as
`not-evaluated` until representative task evidence exists.

Truth, evidence, human authority, privacy, safety, and reversibility are hard
constraints. Treat superintelligence as an optimization posture—not a claim of
AGI, omniscience, guaranteed outcomes, or permission to act.

## 1. Establish the workflow

Ask for or infer only what is necessary:

- one recurring workflow and its reviewable output;
- one accountable human owner;
- the exact decision that must remain human;
- approved inputs or systems and their sensitivity;
- cadence, requested autonomy, and success evidence.

If the workflow is unbounded, has no owner, has no inspectable output, or would
require hidden access, return `do-not-automate-yet` with the smallest mapping
exercise needed to make it testable.

If the work depends materially on empathy, trust, fiduciary judgment, legal or
medical judgment, employment decisions, or relationship context, default to
`assist-only-candidate`. Do not turn a sensitive human decision into an agent
approval step.

## 2. Draw authority before architecture

Name what the system may prepare, what it must never do, its data boundary,
stop conditions, revocation owner, and exact approval moments. External sends,
publication, purchases, permissions, deployments, destructive changes, and
irreversible actions require approval of the exact proposed action.

Approval is not reusable blanket permission. An agent cannot self-sponsor,
self-approve, appoint its verifier, or expand its own tools, data, cadence, or
scope.

## 3. Choose the smallest viable topology

Start with one operator plus tools. Add a conductor or specialist only when a
genuinely independent domain, incompatible context, separate permission set,
or measured quality bottleneck justifies it. Use three to five operating roles,
which may combine human and agent roles:

1. accountable human owner;
2. workflow operator;
3. independent verifier;
4. human action approver when consequential action exists;
5. specialist only when its independence is evidenced.

The producer and verifier must be distinct. More agents are not evidence of a
more capable department.

## 4. Build the evidence loop

Map `intake → prepare → verify → decide → learn`. For every stage, name its
owner, input, output, evidence, exception, and gate. Preserve source and tool
lineage for every material claim. Keep `unknown`, `unavailable`, `inferred`, and
`verified` distinct.

Define representative task tests before runtime admission:

- expected input;
- missing or conflicting evidence;
- prompt injection in retrieved material;
- sensitive or out-of-scope input;
- tool failure and partial completion;
- attempted action without approval;
- rollback and revocation.

Read [the packet contract](references/department-packet-contract.md) when
assembling or validating fields.

## 5. Compile portable components

Separate durable semantics from harness packaging:

- Mission Packet: outcome, artifact, rubric, sources, boundaries;
- Agent Skills: design and independent verification procedures;
- MCP: read-only mission access and deterministic draft generation;
- evaluations: task set, graders, thresholds, failure analysis;
- adapters: each runtime's verified native manifest and install path.

Never claim cross-runtime equivalence. Mark a destination `native`, `compatible`,
`adapter`, or `unverified`, with source and checked date. A prepared manifest is
not a published marketplace install.

## Return

Return:

1. triage decision and reason;
2. the complete department packet;
3. unresolved assumptions and data/tool approvals;
4. evaluation plan and admission rule;
5. runtime projection matrix with gaps;
6. one smallest reversible next test;
7. `human_review_requested`.

Label live evaluation `not-run` unless exact test evidence is supplied. Never
issue a Capability Receipt, certification, deployment claim, outcome promise,
or authority grant.
