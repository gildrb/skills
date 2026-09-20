---
name: bend
description: Implement, repair, refactor, and optimize Bend programs with machine-checked formal proofs. Use for Bend or .bend code, LAWS.bend, PROOF.bend, law-driven development, proof failures, or proof-preserving CPU/GPU optimization. Read the installed bend guide, construct and check proofs, and use resumable implementation, experiment, review, and delivery loops. Explicit autoImplement executes an existing plan; autoResearch runs a proof-gated optimization session.
---

# Bend: implement, prove, verify

Execute the requested work. A plan, suggested command, compiling program, finite
test suite, or proof narrative is not a completed implementation and proof.

`complete => contract proved AND required validation passed AND delivery checked`

`tests passed != universal proof`

`source proof != verified compiler, external effects, or hardware`

## 1. Read the active language before editing

Resolve the project's active `bend` in its existing execution environment. Use
that same executable and environment for documentation, proofs, and builds.
Execute and read the actual output:

```sh
bend guide
bend --help
bend --version
```

Read the complete guide, retrieving any truncated output. Invocation alone is
not reading. Do not substitute a web copy or remembered syntax. Discover an
auxiliary command's equivalent from local help if it differs. Record executable
identity, reported version, and relevant capabilities, not a required release.

The local guide and library definitions govern syntax, proof construction,
targets, and checker behavior. Inspect unfamiliar APIs with the documented
library command, such as `bend base`. Read locally documented parallelism or
effects guides when relevant. Treat external examples as leads to check locally.

If documentation or a necessary proof capability cannot be obtained, report the
exact failure. Do not silently switch toolchains or provers. A changed executable,
library, or execution environment invalidates earlier capability and proof
receipts: read the active guide and revalidate before continuing.

## 2. Recover the task, authority, and contract

Read repository instructions, relevant callers and implementation, laws/proofs,
canonical plans, objective/review policies, and existing session records. Preserve
unrelated user edits. Identify the public entry points, target, task branch, and
existing PR. Continue that PR, not a replacement branch or a second PR.

Use the [controller](references/controller.md) for scope, workspace isolation,
resumption, evidence invalidation, retries, and cancellation. It applies to both
workflows. Read the relevant workflow before taking its first action:

- **Ordinary Bend task:** execute the implementation/proof cycle below. Do not
  activate an autonomous research session or invent publication authority.
- **Explicit autoImplement:** read [autoImplement](references/autoimplement.md).
  Execute the selected existing plan end to end. Do not invent an initial plan;
  an absent or materially ambiguous plan blocks this mode, not ordinary proving.
- **Optimization / autoResearch:** read [autoResearch](references/research.md).
  Establish or resume an objective, verified baseline, measurement policy, and
  durable experiment history. Do not require a prewritten implementation plan.

Existing compatible Pi tools may execute these stages. Read the [Pi adapters](references/pi-adapters.md)
before delegating. Otherwise perform the stages directly with available tools.
Never assume a workflow name is a CLI command or silently start two controllers.
No agent vendor, model, or research runner is a dependency of this skill.

Map requirements to laws. When asked to formalize them, write faithful laws and
their proofs rather than merely recommending formalization. Distinguish explicit
requirements from inferred assumptions. A material ambiguity is an unresolved
specification issue, not permission to choose an easier contract.

Separate protected public claims and specification meanings from editable
implementation and supporting proofs. Protect valid-input conditions, independent
reference semantics, observable results, expected theorem inventory, and acceptance
controls. Do not freeze every imported implementation detail. Internal algorithms,
representations, lemma statements, and proof bodies may change within scope if
the unchanged public contract is proved. Project restrictions still prevail.

Never weaken a public law, strengthen its premises, shrink its domain, redefine a
protected predicate, omit a required law, or redirect verification to easier code
without explicit authorization. Plan approval, a review verdict, a timeout, and
an improved metric do not independently authorize specification changes.

Run the existing proof gate before editing. Record pre-existing failures rather
than bypassing them. Establish a new gate using [proving](references/proving.md).

## 3. Implement and prove, not merely type-check

Read [proving](references/proving.md) before changing laws or proofs.

1. Select the next requirement and its exact proof obligation. State the relation
   between the implementation and specification, including representation changes.
2. Implement a coherent change and construct its proof. Decompose difficult goals
   into reusable lemmas and check incrementally. A coherent change may replace an
   algorithm and its proof architecture; diff size is not a correctness criterion.
3. Run the installed checker on completed lemmas, then every required public law.
   Under the locally documented LAWS/PROOF convention, run `bend PROOF.bend` in
   the correct directory. Otherwise use the documented equivalent and all project
   proof entry points. Audit the import closure and expected theorem inventory.
4. Read complete diagnostics. Distinguish a false claim, missing lemma, type or
   ownership error, termination issue, resource limit, and toolchain defect.
   Repair the code or proof. Re-read actual definitions instead of guessing syntax.
   Evidence that invalidates the plan returns to the controller's replan stage;
   an ordinary implementation bug stays in the repair loop.
5. Run required local/backend validation and [review](references/review.md).
   Recheck after repairs. Continue until the obligations are discharged or a
   concrete goal, counterexample, resource limit, or capability remains unresolved.

Do the formal proving yourself. No arbitrary new axioms, unsafe escape hatches,
circular evidence, trusted-definition overrides, or final holes. Audit transitive
proof dependencies and disclose existing trusted primitives. Open laws and finite
examples cannot substitute for a general theorem.

## 4. Retention and delivery are separate gates

`keep experiment => contract intact AND proof checked AND validation passed`

`keep optimization => keep experiment AND predeclared metric policy satisfied`

A locally retained experiment is not yet a reviewed, delivered PR. Both workflows
use the controller's final review, comment, and CI stages before completion.
Preserve unsuccessful attempts and learning, not failed code in the accepted path.

Use a distinct read-only reviewer when available. Otherwise label a separate
self-review honestly. If a particular reviewer or independent approval is required,
its absence blocks acceptance. No fabricated reviewer receipts or fallback to a
different reviewer when the required configuration is unavailable.

Check process status AND full checker diagnostics using the active version's
semantics. Do not hardcode a success banner or trust exit zero alone. Missing
laws, unsafe qualifications, incomplete/truncated evidence, timeouts, stale logs,
or application output resembling a checker verdict cannot establish verification.

Do not change the checker, dependencies, specification, benchmark, or acceptance
controls to obtain a pass. Commit, push, comment, merge, release, and deployment
are distinct scoped actions. A PR request permits its normal scoped updates;
it does not authorize merging, deploying, unrelated repositories, or policy changes.

## 5. Finish with current evidence

Read [review](references/review.md) on the delivered snapshot. Complete authorized
publication in the same PR; inspect current-head reviews/comments and required CI.
For documentation-only work, relevant local checks suffice unless repository
policy requires more. Never invent green CI when no checks exist or failures remain.

Report the active Bend identity, changed implementation/proofs, theorem coverage,
exact executed commands and outcomes, final source identity, review mode and
remaining findings, performance evidence when applicable, and any blockers.
For a PR task, include its link and post the same evidence summary there when
commenting is authorized. State untested backend, staging, or production behavior.

Work autonomously within the authorized execution budget. Stop on cancellation;
do not restart automatically or manufacture approval from silence. Checkpoint
unfinished work so another invocation can resume, without claiming background work.

Useful templates: [run state](assets/run-state.md) and [research session](assets/research-session.md).
Use existing canonical documents instead of creating competing sources of truth.
[Sources](references/sources.md) and [third-party notices](THIRD_PARTY_NOTICES.md)
record provenance. Editable instructions do not enforce compliance; only a
suitably protected external gate can independently enforce acceptance.
