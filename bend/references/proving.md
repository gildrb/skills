# Formal proving protocol

Use this process with the syntax and semantics read from the active `bend guide`.
Do not copy a proof from another release without checking it locally.

## State a meaningful theorem

Map each required behavior to an explicit proposition over the real entry point.
Record its quantified inputs, preconditions, output relation, and dependencies.
Cover arbitrary inputs or operation sequences when the requirement is general.

An independently specified result is useful only if the implementation is proved
to refine it. Trace any representation conversion through that relationship.
An unproved wrapper, serializer, packing step, or alternate fast path remains a
gap. Do not describe a representation-specific theorem as end-to-end correctness
when the connection to the public input/output format has not been proved.

Reject specifications that merely restate the implementation as its own oracle.
A genuinely independent specification may still be definitionally equal to a
simple implementation: reflexivity is legitimate when it proves the actual
contract. Proof size is not evidence of specification quality.

Look for missing obligations:

- Sorting: ascending output AND preservation of every input value and duplicate.
- Stateful updates: valid initialization AND preservation at every allowed step;
  connect this invariant to the requested observable behavior.
- Bounds: legality of each access, including caller-side preconditions; establish
  the installed library's actual indexing behavior rather than assuming traps.
- Conservation: define what is counted, signedness, external flows, and arithmetic
  semantics. A slogan about a sum is not automatically a security specification.
- Progress: required successful behavior must remain possible. Reject-all,
  constant-result, deleted-resource, or disabled-feature implementations must not
  satisfy the intended contract accidentally.

Check that preconditions are satisfiable. Every implementation-dependent
precondition needs evidence at its real caller, not an unsupported assumption.
Use concrete counterexamples to challenge the specification, without treating
failure to find one as proof of completeness.

## Construct proofs rather than placeholders

Inspect the installed guide's theorem example and relevant local library lemmas.
Learn how that executable represents propositions, evidence, case analysis,
induction, equality, rewriting, and erased versus runtime arguments. Names and
syntax in a previously read guide are not an API contract for another executable.

For each difficult goal:

1. Write its full statement and identify the changing quantity or state relation.
2. Select an induction measure accepted by the local termination rules. Prove
   the base case, then the step using the induction hypothesis on a smaller input.
3. For accumulators or a changed representation, strengthen an internal induction
   invariant as needed. Prove its premises at the public entry point. Do not add
   them as new assumptions to the public theorem.
4. Decompose algebraic, structural, and representation lemmas. Inspect the exact
   expected and observed terms after a failure. Use the local goal-inspection
   mechanism when documented, and discharge every temporary goal before delivery.
5. Check lemmas as they are completed; finish with the complete public contract.

Finite computation may establish a finite subclaim if the checker verifies the
exhaustive computation and its connection to the theorem. Testing finitely many
input sequences does not establish a theorem about all sequence lengths.

Respect the installed type, quantity/ownership, and termination rules. Do not
bypass them to close a proof. If an algorithm needs an explicit bound or fuel,
prove its relationship to the requested behavior instead of silently truncating
work. Logical termination does not establish a wall-clock or memory guarantee.

## Connect files, imports, and evidence

Use the project's proof structure when it covers the complete contract. Under
the LAWS/PROOF convention, public laws import the implementation and the proof
entry point imports those laws and supplies their corresponding definitions.
Derive qualification, imports, and syntax from the installed guide.

Trace the import closure and proof chain for each public theorem. Confirm the
law refers to the implementation used by the real caller. Supporting modules
with new obligations must be included in verification. Reject imported unsafe
proof code, arbitrary new assumptions, circular evidence, or shadowing of trusted
symbols. Existing axiomatic primitives are trust assumptions, not newly proved
mathematics; state them and do not expand that trust boundary silently.

Prefer a proof-only entry point without an application `main`. Use the installed
check-only mechanism if documented. Application output must not stand in for a
checker verdict. An empty file checking successfully proves none of the expected
public contract; the expected law inventory is a separate requirement.

## Establish a new or changed verification gate

Use disposable files outside the user's source. Adapt the local guide's smallest
complete theorem example and execute the discovered checker command.

Verify three cases with the same executable:

1. A complete, valid theorem checks.
2. A well-formed false claim paired with invalid evidence is rejected for a
   proof/type reason, not merely a syntax error or failed import.
3. An imported required claim with its proof omitted is not accepted as complete.

Read exit codes and full diagnostics. Do not infer soundness of the language from
these controls; they only check that the intended checking path is being used.
Unknown diagnostic semantics require investigation, not a guessed parser.

Audit every expected theorem independently of whether this version catches a
missing import automatically. In an isolated copy, omission of an expected law
must fail the overall acceptance gate even if the bare compiler accepts the
reduced program. Never weaken the real contract to conduct this check.

For an authorized verification audit, also apply meaningful, type-correct
implementation mutations in disposable copies. Confirm the unchanged relevant
law rejects an incorrect result. A parse error, timeout, unrelated failing law,
or failed build is not evidence that the intended theorem detected the bug.
Mutation checks supplement proofs and specification review; they do not prove
that the specification is complete. Respect project restrictions on new tests.

## Separate mathematical and operational claims

Identify boundaries around external IO, foreign code, precompiled dependencies,
backend lowering, runtime behavior, and hardware. A proof of pure logic does not
verify those components merely because the program calls them.

Determine the installed treatment of machine integers, overflow, floating-point
operations, NaNs, and conversions before stating numerical laws. Do not assume
real-number algebra applies to floating point. Unsupported numerical guarantees
remain unproved; no invented axioms or test-only claims of formal correctness.

For a timing goal, define the metric, workload, platform, synchronization, and
measurement procedure. A checked cost-model theorem is conditional on that
model; it is not automatically a bound on physical execution time.

A blocked proof report names the exact remaining proposition, diagnostics,
attempts, and any counterexample. Difficulty alone is not a counterexample and
not evidence that the theorem is false.
