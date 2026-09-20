# Optional Pi adapters

The portable workflow does not depend on Pi. When compatible Pi facilities are
already available, discover their installed contracts and delegate instead of
manually duplicating their controller. Source-level interface examples below are
leads, not hardcoded promises about a future extension. Never install a package,
change agent settings, bind a shortcut, or select a model merely to use this skill.

## Pi Workflows autoimplement

Read the active workflow schema and upstream autoimplement instructions. At top
level, list workflows, build the complete input, and start `autoimplement` once.
If already inside a workflow step, complete that step's contract; do not start
another workflow. After a successful start, return control as required by the
host. Do not claim a background run exists unless the host actually started it.

Build input from established facts:

- `task`, selected `plan`, absolute `repository`, concrete `scope`, `constraints`,
  actual `baseBranch`, canonical `documents`, and explicit `merge` authority.
  Scope names allowed edit/verify/commit/push/PR actions and excluded operations.
- `workspaceMode`: reuse the correct task branch. Use the workflow's `auto` behavior
  only if it preserves that branch and any existing PR. Direct default-branch work
  needs explicit authority. Include `preparedWorkspace` only with a real matching
  preparation receipt, not a fabricated object.
- `documentation`: include only a trusted receipt matching the selected plan and
  canonical documents. Otherwise let the workflow inspect/document them.
- `approval`: honor required plan-change approval. Delegate implementation-plan
  decisions only within already granted scope. Never use timeout-based approval
  for new public laws, acceptance rules, permissions, or user intent. Do not answer
  the operator's protected decision through a model/tool call.
- `concurrency`: obey explicit user limits and host/resource constraints. No
  overlapping mutations of the same candidate.

Supply `verificationChecks` only when the final absolute working path and every
safe command record are known. Otherwise omit it and use the workflow planner.
For the current upstream contract each record has `id`, `command`, string `args`,
exact `cwd`, positive `timeoutMs`/`maxOutputChars`, boolean `readOnly`, `baseEligible`,
`changedFileScope`, and `findingFormat` (`text` or `json`). Derive all values from
actual tools. `baseEligible` requires a genuinely read-only command that works
unchanged in an isolated base checkout. Do not include Git, GitHub CLI, shell
wrappers, mutation, publication, merge, release, or deployment commands in that
field. Provide `verificationUntested` only with supplied checks, using actual
untested requirements. Never label commands read-only just to fit the schema.

Pass the Bend proof protocol, expected law inventory, active-toolchain discovery,
full-diagnostic requirement, and forbidden proof bypasses in the plan/constraints.
A direct check command alone is insufficient on a release that exits zero with
unsafe or incomplete evidence. Ensure the delegated steps audit that evidence
and protected law coverage. If the host cannot express the required acceptance
contract, use the portable controller and report the limitation. Do not weaken
the proof gate to fit a native field or patch the upstream engine in this task.

Use the workflow's reviewer configuration rather than hardcoding model choices.
If `pi-reviewer` is required and unavailable, stop that review stage; no silent
`codex review` substitution. If no particular reviewer is required, the portable
review policy allows another available independent reviewer or labeled self-review.

## pi-autoresearch

Inspect actual mode, tool schemas, working directory, session files, and Git
side effects. Merely loading `autoresearch-create` does not activate the upstream
mode in a fresh session. Do not claim tools are available until the host exposes
them. Use a supported activation mechanism only with research authority; otherwise
perform the portable stages. Do not print a slash command and claim it executed.

The upstream sequence is `init_experiment -> run_experiment -> log_experiment`.
Initialization describes name, `metric_name`, unit, and `direction` (`lower` or
`higher`). Initialize a new comparable segment once; recover an existing session
without erasing its baseline or budget. Configuration fields such as `workingDir`
and `maxIterations` must match the installed schema and authorized path/budget.
No "unlimited" default overrides the current task's finite execution allowance.

`run_experiment` takes the actual measurement command and bounded benchmark/check
timeouts. It executes `.auto/checks.sh` after a passing benchmark. Make that file
mandatory for Bend and preserve its full logs; proof checks are not timed as the
performance metric. Establish a fresh candidate proof before measurement as well.
Confirm source/evidence identity after benchmark and hooks before retention.

`log_experiment` records the result and may auto-commit a `keep` or auto-revert
`discard`, `crash`, or `checks_failed`. Before any call, confirm those effects are
authorized and confined to the clean owned candidate workspace. Never use it in
a checkout containing unrelated tracked/untracked user changes. Otherwise record
the attempt portably and perform only narrowly authorized retention/rollback.
Do not add a duplicate manual commit/revert around a tool that already owns it.

Supply actual commit identity as the schema requires, finite metric, status,
description, secondary `metrics`, and useful `asi`. Include proof receipt, source
fingerprint, failure details, and learned lesson in `asi` or referenced evidence.
If the API requires a crash placeholder, flag its absence of measurement and do
not use it as a score. Inspect complete logs despite abbreviated tool output.
Validate the retention path with disposable controls for invalid evidence, an
omitted required law, an unsafe qualification, and a stale source receipt. These
are integration controls, not a proof of checker soundness. Only call `keep` after
all Bend proof/validation and candidate-review conditions hold. The native tool refusing `checks_failed` is not the whole acceptance gate.

Preserve native `.auto/log.jsonl` records and let native tools write their own
schema. Do not splice a portable record format into the extension's file. Never
call `/autoresearch clear` or reset counters to erase bad outcomes. On explicit
stop, stop owned work and disable native auto-resume using a supported control;
do not start another iteration. A later explicit resume must reread durable state.

Dashboard shortcuts, exported reports, hooks, and independent-branch finalization
are optional upstream features, not required or automatically enabled here.
No fixed shortcut is assumed. A hook's output cannot grant new scope or weaken
laws. Branch finalization cannot replace the user's existing PR without permission.

## Intentional Bend-specific differences

The upstream execution order and durable state are reused. The following are
not copied: optional correctness, metric-only retention, swallowed check failures,
unlimited unattended looping, delaying explicit cancellation, implicit law approval,
automatic runner installation, destructive rollback of user work, or mandatory
Pi/model dependencies. These would contradict this skill's correctness, portability,
or authority contract. Report unavailable native facilities rather than simulating
successful calls. Native integration is capability-adaptive, not a guarantee that
every future Pi release accepts these illustrative field names.
