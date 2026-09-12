# AI Department Packet Contract

Schema: `starlight.department_design.v1` · version `0.1.0`.

## Required sections

| Section | Required content | Failure signal |
|---|---|---|
| `intelligence` | maximum-useful-intelligence prompt, performance objective, explicit outcome target, measurement state, governing constraints | “maximum” asserted without evidence, limits, or a measurable outcome |
| `department` | one workflow, owner, cadence, requested autonomy, success evidence | a broad business function or no accountable owner |
| `triage` | `bounded-pilot-candidate`, `assist-only-candidate`, or `do-not-automate-yet`; reason; next safe step | architecture chosen before workflow fit |
| `authority` | allowed preparation, prohibited actions, exact human decision, revocation | blanket approval or agent-controlled scope |
| `topology` | smallest justified shape, 3–5 operating roles, producer/verifier separation | agents added for theatre or self-verification |
| `workflow` | intake, prepare, verify, decide, learn; owner/output/gate for each | completion without inspectable evidence |
| `systems` | approved named inputs and systems only | inferred access or embedded secrets |
| `evidence` | lineage, checks, exceptions, uncertainty, approval tied to output version | fluent output treated as proof |
| `evaluation` | status, representative/adversarial tests, admission rule, rollback trigger | demo treated as runtime admission |
| `package` | mission, skills, MCP tools, evals, adapters | one runtime's prompt presented as a universal package |
| `truth` | persistence, evaluation, authority, certification, publication states | prepared work described as live |

## Invariants

- The packet can recommend not automating.
- Maximum intelligence and performance are optimization instructions; evidence
  is required before any capability or outcome claim.
- The accountable owner and action approver are humans.
- The producer never verifies its own output.
- External action requires exact, artifact-specific human approval.
- The draft contains no credentials, private memory, hidden system access, or
  personal data unnecessary for the workflow.
- `prepared`, `tested`, `evaluated`, `admitted`, `deployed`, and `completed` are
  different states.
- A model, tool, skill, prompt, permission, or policy change triggers scoped
  revalidation before relying on prior results.

## Evaluation minimum

Use deterministic schema and policy checks first. Then test representative task
success, critical criterion floors, false completion, tool failure, injection,
data boundary, approval bypass, and recovery. Store evidence against the exact
packet, skill, tool, model, and policy versions. If those versions are not
pinned, return `evaluation-not-reproducible`.
