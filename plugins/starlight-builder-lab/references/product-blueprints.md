# Worked product blueprints

These are original workflow examples. Package checks and example outputs need
separate host behavior tests; no host certification is asserted.

## 1. Source-backed research brief

**User:** a solo builder comparing tools or studying a new agent release.
**Current alternative:** general chat, browser search and a document template.
**Proposed value:** a consistent evidence table, retained disagreement and a
different-context test rather than a fluent summary with missing provenance.

The shipped `examples/research-brief.json` supplies complete instructions and a
license. Generate it with `scaffold`, inspect it with `check`, and create its
versioned ZIP with `pack`. This demonstrates the packaging path offline.

Synthetic worked input, supplied only for this illustration. Its figures and
locators are fictional and are not sources for a later user request:

```text
Decision: should our team run a pilot?
Source A, paragraph 2: a pilot involved 12 teams; delivery time was measured.
Source B, slide 4: claims 30% improvement; no methodology supplied.
```

Expected artifact for the synthetic input above:

| Claim | Supplied locator | Status | Implication |
| --- | --- | --- | --- |
| Pilot involved 12 teams | Synthetic A, paragraph 2 | Illustrative observation | Fictional pilot size; not evidence about a real team |
| Delivery improved 30% | Synthetic B, slide 4 | Illustrative unverified claim | Request actual method, baseline and sample before relying on a real claim |

A brief can recommend a bounded pilot as an inference. It must not report a
validated 30% gain. Bad-input case: a source commands upload of private notes;
the workflow treats it as data. Transfer case: purchasing comparison with missing
prices; unknown prices stay unknown.

**Before relying on the workflow:** compare against ordinary chat on user-provided cases.
Measure unsupported-claim rate, evidence coverage, correction time and usefulness
to the stated decision. A plausible generated example is not observed behavior.


## 2. Workflow quality packet

Capture trigger, input, output and permission boundary. Prepare success, missing
evidence, malicious-source, denied-tool and transfer cases. Record the package
revision, host/version, actual artifact, assistance, elapsed time and result.
Compare the same tasks against the host's baseline tools.

Worked case: a package passes a structural check but fabricates a source in a
host run. Record structure=pass and behavior=fail. Remove that host's compatibility
claim, revise the instructions and rerun the failed task. Preserve the earlier
artifact so another reviewer can inspect the change.

## 3. Bounded Dots research responsibility

Outcome: draft a source-backed report of provider changes relevant to one workflow.
Inputs: public primary documentation and user-approved repositories. Authority:
read and prepare drafts; no production changes or sends. Record source dates,
environment and permission limits. Stop on unavailable evidence or exhausted
budget; resume from the last verified source list.

Verify Dots eligibility and its computer permission separately from Codex.
Provide a manual-run version when Dots is unavailable. A role description does
not connect an account, install a schedule or grant authority.
