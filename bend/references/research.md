# autoResearch: proof-preserving optimization

Use this mode only when the task includes an optimization objective. It wraps
actual implementation and proving, not a separate unverified performance path.
The protocol is independent of any named runner or agent vendor.

## Establish the experiment

Read existing objectives, review policies, and prior attempts. Separate measured
facts from proposer narratives. A historical best score is not a fresh baseline.

Record the public entry point and frozen contract, editable implementation and
supporting-proof scope, installed toolchain, required execution target, workload,
metric and direction, correctness checks, acceptance criterion, and available
budget. Reuse an existing trusted benchmark instead of inventing a favorable one.

Use an isolated candidate workspace or a narrowly tracked reversible patch.
Preserve the user's work and the accepted baseline. Isolation need not use Git
or any additional package. Never reset or clean the user's working directory to
undo your experiment.

First prove and validate the baseline, then measure it. If the baseline fails,
repair within the authorized scope or report the failure. Do not compare
incompatible, unverified, or incomplete measurements as an improvement.

## Repeat one coherent hypothesis at a time

1. Identify the bottleneck and inspect prior failed ideas. Consider algorithmic
   work, representation, allocation, traversal, and data movement before only
   tuning syntax. Choose a concrete predicted mechanism, not a promised speedup.
2. Implement the candidate and its full proofs under the same public contract.
   Internal types and supporting lemmas may be replaced where authorized.
   Do not reject a potentially useful architecture solely because its proof is
   harder, or rewrite merely to make the diff larger.
3. Re-run the complete proof gate. Audit changed proof dependencies and discharge
   all revised lemma preconditions. Run required existing runtime validation.
   A proof failure, safety bypass, incorrect output, or incomplete gate rejects
   the candidate before performance scoring.
4. Measure the same proved entry point with unchanged workload and scoring rules.
   Store complete raw measurements and environment metadata, including failures.
5. Review the diff, proof chain, baseline compatibility, and measurements under
   the review protocol. Accept only when the proof and validation gates pass
   and the measured result satisfies the predeclared performance criterion.
6. Retain the best accepted candidate, not simply the most recent one. Record
   rejected hypotheses, evidence, and reasons before another grounded attempt.

A larger supporting-proof rewrite is permissible; weakening a public claim is
not. Benchmark-specific answers, result caching for known inputs, skipped work,
weakened precision, a disconnected fast path, changed timers, or toolchain
substitution are not optimizations under the unchanged contract.

## Apply the active Bend execution model

Read the installed parallelism guide and relevant library definitions. Confirm
whether the requested backend is actually executing, not falling back silently.

Examine balanced independent work, useful task granularity, flat leaf loops,
ownership, boxing, reference counting, specialization, and allocation according
to that release. Inspect emitted native code with the documented command when
it helps explain a measured bottleneck. Do not patch emitted code and transfer
the original source proof to that new program without justification.

Measure CPU versus GPU placement where relevant and available. Include transfer
and managed-memory migration costs for the actual device. Do not transplant
fork depths, lane counts, or performance figures from another GPU or a unified-
memory machine. Parallel execution is a hypothesis to measure, not a guarantee.

## Measure without changing the question

Keep inputs, required outputs, numerical policy, compiler configuration, and
machine conditions comparable. The frozen harness decides what lies inside the
timed region. Report exclusions explicitly and never move required work outside
that region to improve the score. Report end-to-end cost when it is the goal.

Use warm-up, repeated complete runs, and interleaved baseline/candidate order
when practical. Account for completed asynchronous/device work, not submission
latency. Inspect raw samples and noise. A trusted predeclared calibration may
increase batch size; it must retain comparable normalization and semantics.

Apply the agreed aggregate to complete runs. Do not cherry-pick samples or mix
per-workload winners into an execution mode that was never run. Do not change
thresholds after seeing results. When no meaningful improvement can be separated
from noise, report the result as inconclusive and retain the baseline.

A throughput target is an empirical acceptance condition unless a precise
machine/cost model and a checked connection to it have actually been provided.
Do not claim that writing a throughput target as a law makes it achievable.

## Review, stop, and hand off

Prefer a distinct read-only reviewer given the frozen contract, complete diff,
proof commands and outputs, raw samples, and earlier decisions. Without that
facility, perform and label a separate self-review. An independent-review
requirement cannot be fulfilled by renaming self-review.

A reviewer returns accept or reject with concrete evidence and unresolved risks.
Missing, malformed, or inconclusive review is not approval when approval is
required. A reviewer does not silently fix a candidate while judging it.

Follow the task's experiment or resource budget. Without one, do bounded work
within the current task, not an unattended unlimited loop. Stop when the goal is
met, the budget is exhausted, or further attempts need a specific unresolved
requirement or capability. Preserve useful failures and the best checked result.
Reverify the selected final snapshot after integrating any accepted change.
