# Shared evidence-driven controller

Adapted from Pi Workflows' autoimplement control loop. This protocol coordinates
both autoImplement and autoResearch; it is not an installed command or a daemon.

`observe -> choose one next stage -> execute -> record evidence -> observe`

Expected success, failure, and timeout return to the controller. Cancellation is
terminal. Never recursively start the same workflow from inside its active step.

## Scope and workspace

Derive authority from the user request and applicable repository instructions.
Record allowed repositories and separate edit, verify, commit, push, PR/comment,
merge, release, and deployment permissions. A path alone is not authority.
For a request to update an existing PR, use its actual head and base and keep all
work there. Publication authority is not direct-default-branch or merge authority.
Do not touch scratch repositories, credentials, remote policies, or other projects
merely because an upstream workflow mentions them.

Inspect the workspace before edits. Reuse a correct task branch. From a clean
default branch, create a task branch when authorized. On a dirty default branch,
use an isolated worktree/copy without discarding user edits. Carry needed uncommitted
task changes into the candidate explicitly and record their identity. Do not
pretend a clean HEAD copy contains those changes. Without Git, a separately owned
copy or a narrowly tracked reversible patch can preserve the same invariant.

An experiment runner that auto-stages, commits, or reverts may run only in a
reviewed, isolated, clean candidate workspace within the granted authority. Check
tracked AND untracked content. Preserve starting user work and session evidence
outside any rollback target. Do not change ignore rules or clear files to conceal
contamination. Use available protections without changing access policy.

## Durable run record

Use the canonical plan/progress document, or adapt the run-state template when
none exists. autoResearch also uses its `.auto/` session records. Before context
is lost, record:

- Task and selected plan identity; scope and exclusions; branch, base, PR, work path.
- Active toolchain/library identities, target, expected law files and theorem names,
  protected meanings, editable files, proof commands, required validation/review/CI.
- Current stage, attempts and failure fingerprints, exact source identity for each
  receipt, accepted baseline, incomplete candidate, next action, and stop reason.
- Applicable budget, remaining allowance, known blockers, and untested requirements.

After compaction or resumption, re-read canonical documents, the active guide when
its reading or identity is no longer established, current code/diff, relevant logs,
and current PR head. Reconcile recorded state with actual state before acting.
A summary, old success message, or remembered branch does not override reality.
Changed requirements require a documented authorized revision, not a silent edit.

## Choose stages from evidence

| Observed state | Next action |
| --- | --- |
| Cancellation | Stop owned work safely, record incomplete status, do not route again. |
| Guide or environment identity unknown | Read active documentation and establish capabilities. |
| Explicit autoImplement has no clear existing plan | Record the missing-plan blocker; do not invent the plan. |
| Selected plan is clear but its document is stale | Record the selected plan faithfully before implementation. |
| Evidence invalidates the plan | Revise only within authority; preserve the old plan and reason. |
| Implementation or proof obligation outstanding | Implement/prove or repair using actual diagnostics. |
| Candidate source changed after a pass | Invalidate affected proof, validation, review, and metric receipts. |
| Research baseline/candidate not measured comparably | Validate, then measure under the frozen metric policy. |
| Required review missing/invalid, or P0/P1 outstanding | Review current candidate or fix and reverify. |
| Valid low-severity findings remain | Apply proportionate scoped fixes and review their delta. |
| Authorized publication not current | Commit/push exact scoped files to the existing task PR. |
| Current PR comments not addressed | Inspect, respond, fix when valid, and resolve when permitted. |
| Required current-head CI unknown/pending | Inspect once, then bounded observation or useful local work. |
| All required evidence current and delivery complete | Report completion; merge only with separate authority. |
| Budget exhausted or a necessary capability is missing | Checkpoint and report blocked/incomplete, not successful. |

Dependency order matters: formal correctness precedes accepting speed results;
review must inspect current source; CI conclusions must refer to the current head.
Do not run an expensive stage again solely because a fixed checklist says so.

## Invalidation rules

A receipt records source contents, dependency/contract/toolchain fingerprints,
command, working directory, status, complete output location, and interpretation.
A commit alone is insufficient with uncommitted or generated inputs.

Implementation/proof/import changes invalidate affected proofs and all results
that depended on them. Toolchain/library changes require capability discovery and
fresh proof/build evidence. Workload, metric, numerical policy, or target changes
start a new research segment with a fresh baseline; never compare old scores as
though the question were unchanged. Review-policy or public-contract changes need
separate authority and invalidate earlier approval. New PR heads require fresh CI
inspection even when unchanged checks can reuse evidence under explicit policy.

Documentation-only edits need relevant local checks and delta review, not fictional
application proofs. A text file that generates code, controls builds, states laws,
or changes acceptance policy is not automatically an irrelevant documentation edit.

## Repair, replan, and bounded autonomy

An implementation bug returns to repair. Evidence that the selected architecture,
requirement, or verification plan is infeasible as stated returns to replanning.
Use an available planning/documentation workflow when suitable; otherwise perform
that role directly and record the same inputs and outputs. No planner dependency.

Honor explicit required approval for plan changes. Do not re-ask approval for the
already supplied plan. An implementation-only adjustment within granted authority
may proceed, with its reason recorded; changed intent, scope, public laws, acceptance
criteria, or permissions requires authorization. A runtime's plan-decision timeout
cannot approve those protected changes. Never answer an operator decision yourself.

Give each attempted route an evidence fingerprint and record what changed. On a
repeated failure, diagnose before retrying. Do not spend the budget repeating an
identical command against unchanged inputs or repeatedly proposing a rejected idea
without new evidence. Record finite per-command/review/CI limits and an overall
available budget before sustained work. Respect tighter user/host limits.

Continue productive in-scope stages without asking permission for every iteration.
Stop on explicit cancellation, exhausted budget, completion, or a concrete blocker.
Do not treat a false theorem as repairable by weakening it, or difficulty as proof
that a theorem is false. Preserve the exact remaining obligation and attempts.

## Concurrency and mutations

Batch independent read-only checks only when resources permit. Separate writable
checkouts, logs, and working directories; do not let a "read-only" check overwrite
shared build artifacts. Keep dependent checks, source changes, fixes, commits,
pushes, PR comment mutations, merges, and releases ordered. One repository has
one owner for each mutable candidate. Subagents receive the same scope, contract,
active guide identity, and evidence rules.

A reviewer must not alter the candidate it is judging. Review fixes return to the
implementation stage and invalidate affected evidence. Do not call sequential
self-review independent or assume a new agent supplies security isolation.
