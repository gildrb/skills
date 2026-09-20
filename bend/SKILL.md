---
name: bend
description: Implement, repair, refactor, and optimize Bend programs with machine-checked formal proofs. Use for Bend or .bend code, LAWS.bend, PROOF.bend, law-driven development, proof failures, or proof-preserving CPU/GPU optimization. Reads the installed bend guide before coding and runs implementation/proof and research/review loops until the requested contract is checked or a concrete blocker is reported.
---

# Bend: implement, prove, verify

Execute the task. Do not substitute a plan, suggested commands, pseudocode, tests,
or a proof narrative for the requested implementation and checked proof.

`complete => requested contract proved AND required validation passed`

`tests passed != universal proof`

`source proof != verified compiler, external effects, or hardware`

## 1. Read the installed language before editing

Resolve the project's active `bend` in its existing execution environment. Use
that same executable and environment for documentation, proofs, and builds.
Run these commands and read their actual output:

```sh
bend guide
bend --help
bend --version
```

Read the complete guide, including output omitted by tool truncation. Do not
merely invoke it, skim a search excerpt, or substitute remembered syntax or a
web copy. If an auxiliary command differs, discover its equivalent from the
installed help. Record the executable identity, reported version, and relevant
capabilities. Do not require a particular release number.

The local guide and local library definitions govern language syntax, proof
construction, supported targets, and CLI behavior. Use the documented library
inspection command, such as `bend base`, before relying on unfamiliar APIs.
Read locally documented parallelism or effects guides when relevant. Online
examples are leads to check against this executable, not its specification.

If the guide or a needed proof capability cannot be obtained, report the exact
failure. Never silently change the toolchain, substitute another prover, or
claim an unsupported proof capability. A toolchain change invalidates earlier
capability checks and requires re-reading the guide and rechecking the work.

## 2. Establish the contract and baseline

Read project instructions, the requested behavior, relevant implementation and
callers, existing laws and proofs, and any objective/review policy. Preserve
unrelated user changes. Identify the actual public entry points and target.

Record which requirements already have laws and which need formalization.
When asked to formalize requirements, write their faithful laws and proofs;
do not stop at proposing that somebody else should write them. Distinguish
explicit requirements from additional assumptions. A material ambiguity is an
unresolved specification issue, not permission to choose an easier contract.

Separate protected public claims and specification meanings from editable code
and supporting proofs. Protect valid-input conditions, independent reference
semantics, observable results, and acceptance controls. Do not freeze the entire
implementation merely because the laws import it. Supporting lemma statements,
proof bodies, internal representations, and algorithms may change when the
unchanged public contract is still proved. Existing project restrictions prevail.

Do not weaken a public law, add assumptions to it, shrink its domain, change a
protected predicate, omit a required law, or redirect verification to easier
code without explicit authorization. Keep a record of the expected law files,
public theorem names, and their intended implementation targets.

Run the existing proof gate before changes. Record a pre-existing failure
rather than treating it as permission to bypass verification. For a new proof
setup, establish the gate using [proving](references/proving.md).

## 3. autoImplement: implement and prove

This is the default workflow, not an external command. Read
[proving](references/proving.md) before writing or changing laws or proofs.

1. Identify the next unsatisfied requirement and its exact proof obligation.
   State the intended implementation-to-specification relationship. For an
   optimization, identify the unchanged theorem the fast path must satisfy.
2. Make one coherent implementation change and construct its actual proof.
   Split a difficult theorem into reusable lemmas; check those incrementally.
   A coherent change may replace an algorithm and its proof architecture.
3. Run the installed checker on the changed proof and then the complete public
   contract. In a project using the documented LAWS/PROOF convention, run
   `bend PROOF.bend` from the correct project directory. Otherwise use the
   installed guide's equivalent and the project's required proof entry points.
4. Read diagnostics. Distinguish a false claim, missing lemma, scope/ownership
   error, termination issue, resource limit, or toolchain defect. Repair the
   implementation or proof without changing the required meaning. Revisit the
   guide and actual definitions instead of repeatedly guessing syntax.
5. Review the exact candidate using [review](references/review.md). Recheck
   after any repair. Continue until every requested obligation is discharged,
   or report a concrete remaining goal, counterexample, or execution blocker.

Do the proving yourself. A compiling program, an open law, a local smoke proof,
a bounded collection of examples, or a natural-language argument does not
complete a general correctness task. No new arbitrary axioms, unsafe escape
hatches, circular evidence, trusted-definition overrides, or final proof holes.
Audit transitive proof dependencies and declare existing trusted primitives.

Use available read-only reviewer/subagent facilities for a separate review.
Otherwise perform a separate self-review and label it honestly. Do not fabricate
an independent review. If independent approval is required by the project, its
absence blocks acceptance. Subagents must use the same recorded toolchain,
contract, and evidence requirements; concurrency must not race source edits.

## 4. autoResearch: only for an optimization objective

Read [research](references/research.md). Run the same implementation/proof loop
for each candidate, then measure and review it. Keep a fresh verified baseline,
an explicit performance hypothesis, unchanged scoring rules, raw observations,
and a record of rejected attempts. Preserve only accepted candidates.

`retain => contract intact AND proof checked AND required validation passed`

`retain optimization => retain AND measured gain meets the agreed criterion`

These are workflow labels, not dependencies on a particular agent, runner,
model, package manager, or orchestration service. Follow an existing compatible
research harness when supplied; do not assume its commands or install one.

## 5. Final acceptance and evidence

Read [review](references/review.md) and check the final source snapshot, not an
earlier candidate. Verification must cover every required theorem and the
implementation actually delivered or measured. Inspect exit status AND the
installed checker's complete diagnostics. Do not hardcode a success banner or
accept exit zero alone. Missing output, timeouts, unsafe qualifications,
unresolved obligations, stale evidence, or an incomplete law inventory cannot
establish successful verification.

Do not modify the checker, library, dependencies, protected specification,
benchmark, or verification controls to obtain acceptance. Do not commit, push,
merge, deploy, delete user work, or change access controls unless the task
separately authorizes it. Work within the task's available execution budget;
do not start an unbounded or unattended research loop.

Return a short evidence report containing the actual version/executable,
changed implementation and proof files, public theorems checked, exact commands
and outcomes, reviewed source identity, and remaining assumptions or blockers.
Identify self-review versus independent review. Separate source-level proof,
backend execution checks, and performance measurements. If only one was
established, say so. Never report an unfinished proof as complete.

This skill directs agent behavior. A protected external verifier can enforce
acceptance; editable instructions alone cannot enforce an agent's compliance.
See [sources](references/sources.md) for provenance, not runtime instructions.
