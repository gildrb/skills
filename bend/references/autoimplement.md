# autoImplement: selected plan to verified delivery

Adapted from `osolmaz/pi-workflows/skills/autoimplement/SKILL.md`. Use when the
user explicitly requests autoImplement. Preserve its selected-plan, implementation,
verification, review, PR-comment, CI, and authorized-delivery stages. Add Bend's
formal-proof gate; neither a generic reviewer nor CI replaces it.

## 0. Recover the selected plan

Find the clear existing plan in the request, conversation, or named canonical
document. Do not invent a new initial plan. If missing or materially ambiguous,
record the exact blocker. Ordinary Bend implementation/proving can still be a
separate task; do not claim it executed an unspecified autoImplement plan.

If the selected plan's documentation is missing or stale, record that same plan
before implementation. Reuse an available documentation workflow or write the
canonical document directly. Include the end state, protected contract, implementation
scope, proof obligations, validation, and action authority. Do not silently change
the plan while documenting it. Resume by re-reading it after context compaction.

Use the shared controller. Where a compatible native workflow is available,
apply the Pi adapter once; otherwise execute these stages directly. Do not run
a native controller and a duplicate manual loop for the same work.

## 1. Implement the plan and construct formal proofs

Implement the requested end state, not just the easiest subtask. Use Bend's
implementation/proof cycle for every affected requirement. Check lemmas during
construction, then the complete public contract. Inspect actual definitions,
callers, representations, and dependencies, not names alone.

Plan-invalidating evidence from implementation, verification, review, or CI
returns to replanning with the old plan and new evidence. Local coding/proof
errors stay in the repair loop. Preserve the public meaning and allowed actions;
record authorized plan revisions and refresh stale canonical documentation.

Continue in the existing PR. If PR delivery is requested and none exists, create
one within scope. Keep canonical documents, proof files, and implementation in
that same delivery. Do not create changes in an unrelated scratch repository.

## 2. Verify locally

Run the active-version proof gate and required project checks. Exercise relevant
entry points and supported backends with existing smoke/integration checks when
applicable. Never relabel finite tests as universal proof. Declare staging,
production, hardware, or remote checks that could not run.

Retain full diagnostic evidence. A truncated display requires retrieving the
underlying output before interpretation. Command failure must propagate; no
`|| true`, success-only grepping, or wrapper that hides checker failures.
Run independent checks in bounded batches only where the controller permits.

Mutation testing is not an automatic per-change prerequisite. Keep existing
mutation tooling available and run it when repository policy or the requested
audit requires it. New verification-gate controls from the proving protocol are
separate from an expensive application-wide mutation campaign.

## 3. Publish the candidate and review it

When authorized, commit and push the scoped candidate before PR-based review.
Review the actual pushed head and relevant dependency fingerprint against the
actual base branch. Without publication authority, review the local snapshot
and mark publication incomplete rather than pushing anyway.

Use `pi-reviewer --base <actual-base>` with its configured defaults when available
and selected by the task. Discover its local interface before relying on it.
Do not hardcode a model or thinking level. If this reviewer is explicitly required
but unavailable, report a blocker; do not silently substitute another reviewer.
Otherwise use an available independent read-only reviewer, or label self-review.

Record each review round with separate P0, P1, P2, and lower findings and its
source identity. Use a bounded tool-native timeout, normally at most ten minutes
per item and always within the remaining budget. Timeout, truncation, malformed
output, and missing review are not clean verdicts.

Repair valid P0/P1 findings, re-prove, revalidate, push when authorized, and rerun
review until none remain. Treat missing/unsafe proofs, disconnected fast paths,
vacuous public laws, and acceptance-policy bypasses as blockers regardless of a
reviewer's severity label. Legacy compatibility is required only by the contract.

When only P2/lower findings remain, fix valid proportionate issues and verify the
fix. Avoid a full external review solely for a harmless P2 documentation change:
record a delta review tied to the new snapshot. Changes affecting public semantics,
proof chains, runtime behavior, or acceptance controls invalidate full review.
If policy requires independent review of every head, obtain it for the new head.
Unchanged repositories/dependencies do not need gratuitous repeat reviews.

## 4. Address existing PR discussion

Inspect inline reviews and PR conversation separately from local reviewer output.
Local pi-reviewer output is not a posted PR review. Tie comments to current code;
recheck older findings that still apply. Fix valid comments through the normal
proof/validation loop. Explain inapplicable findings with evidence, not dismissal.
Reply and resolve threads only within granted permissions; never impersonate a
reviewer or claim their approval. If resolution tools are unavailable, report
which threads remain unresolved. Do not wait unless a required review is pending.

## 5. Inspect CI for the current head

After a valid review with no blocking findings, inspect required checks once
before waiting. For a pending check, record the exact repository/PR/head and
tracking command or connector operation. Bound each observation, normally at
most five minutes and always within the remaining budget. Do useful local
verification between observations rather than repeatedly sleeping. No invented ETA.

Classify failures from evidence. An identical failure on the unchanged base or
other concrete isolation may establish that it predates this task; intuition does
not. Report unrelated failures explicitly and obey required-check policy. Do not
call CI green when failures remain, or treat "no checks" as passed checks.

Documentation-only changes need the relevant local checks and delta review,
without waiting for irrelevant CI unless repository policy says otherwise.
Proofs, executable examples, build inputs, or control files are not exempt merely
because their container is Markdown. State what has and has not been executed.

## 6. Deliver or report the precise remaining stage

Ensure authorized code, proofs, plans, and specification changes are committed
and pushed in the same PR. Reverify the actual final snapshot after relevant
fixes. Merge only with separate explicit or applicable standing authority and
satisfied policy. Otherwise leave the PR ready, pending, or blocked as evidence
warrants. Never auto-release, deploy, or split into new PRs.

Return the PR link, exact validation commands/outcomes, source/proof coverage,
review findings, CI status, and untested boundaries. Add the same final report to
the PR when commenting is authorized. If interrupted or blocked, record the next
stage and remaining evidence instead of claiming completion.

Repeated activation while active does not start duplicate work. After completion,
a duplicate request is a no-op unless the user supplies a new task or new evidence
invalidates completion. After cancellation, only a new explicit instruction resumes.
