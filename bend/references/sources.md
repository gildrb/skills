# Design sources

These sources informed the workflow. They are provenance, not runtime
prerequisites. The active executable's `bend guide`, help, library definitions,
and observed checker behavior take precedence over changing web documents.

## Bend

- [Official guide](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md):
  language discovery, explicit proof terms, the laws/proofs separation,
  termination, affine ownership, and proof checking.
- [Official shader guide](https://github.com/bendlang/bend/blob/main/guide/SHADERS.md):
  workload balance, task granularity, ownership, generated-code inspection, and
  measurement. Its own notice identifies it as AI-written and awaiting human
  revision. Device-specific examples are not universal tuning constants.
- [Official limitations](https://github.com/bendlang/bend#limitations):
  proof and runtime trust boundaries. This skill does not promote the project's
  broad marketing claims into unconditional correctness guarantees.

## Giulio Rebuffo's Bend workflow

- [Objective](https://github.com/Giulio2002/bend-sha256/blob/main/OBJECTIVE.md):
  frozen public correctness requirements, editable implementation and supporting
  proofs, proof-gated experiments, a fresh baseline, and retained attempt history.
- [Read-only review policy](https://github.com/Giulio2002/bend-sha256/blob/main/ORCHESTRATOR.MD):
  inspect actual proof coverage, benchmark the same proved entry point, reject
  benchmark manipulation, and demand evidence rather than proposer narratives.
- [Project README](https://github.com/Giulio2002/bend-sha256/blob/main/README.md):
  explicitly distinguishes a packed-format theorem from the missing universal
  connection to another public input representation. This informed the skill's
  requirement to audit representation bridges instead of overstating coverage.

This skill adapts those mechanisms in original wording. It does not copy the
project's SHA-specific benchmark, dependencies, fixed thresholds, model choice,
or release pin. `autoImplement` and `autoResearch` name the requested portable
workflows here, not executable commands. No separate public `autoImplement`
implementation was verified; no claim of reproducing its source is made.

## Skill packaging

[Agent Skills specification](https://agentskills.io/specification): portable
`SKILL.md` metadata and relative, progressively loaded reference files.

The supplied [Doodlestein post](https://mdfromx.com/doodlestein/status/2101352970294096042)
could not be retrieved during authoring. It is not quoted or used as evidence;
the public format specification was used instead.
