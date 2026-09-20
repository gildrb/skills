# Design sources and adaptations

Provenance only, not runtime dependencies. The active executable's complete
`bend guide`, help, library definitions, and observed checking behavior determine
how to write and prove code. Upstream revisions below identify research inputs,
not required Bend, agent, or runner versions.

## Pi Workflows: actual autoimplement behavior

[autoimplement/SKILL.md](https://github.com/osolmaz/pi-workflows/blob/63a8b740b6b6ce1819b06aeaa4e9fdeabb002839/skills/autoimplement/SKILL.md),
inspected for this integration. File blob: `a35b5d20d60cac4071a3e85b7cf8ba8df312e4e5`.

Adopted: selected existing plan rather than invented initial plan; concrete action
scope; prepared workspace and existing-PR continuity; evidence-driven repair versus
replanning; canonical-document recovery after compaction; local verification;
current-head review with P0/P1 repair loops and proportionate P2 handling; separate
PR-comment handling; bounded CI observation; authorized merge only; final PR report;
bounded concurrency and terminal cancellation; native-controller delegation once.

Adaptations: proof checking and public-law inventory are additional mandatory gates.
A public-contract change is not approved by silence or a planner. Pi-specific
review/planning/documentation facilities are optional unless explicitly required.
No unrelated scratch-repository publication, fabricated async execution, or implicit
merge/release authority. Full review is renewed for changes that invalidate its
proof/runtime assumptions even if an earlier finding was labeled P2.

## pi-autoresearch: actual experiment loop

[Creation skill](https://github.com/davebcn87/pi-autoresearch/blob/939ede8220daad440eac6bb7b6e315cc283e0a64/skills/autoresearch-create/SKILL.md),
[README](https://github.com/davebcn87/pi-autoresearch/blob/939ede8220daad440eac6bb7b6e315cc283e0a64/README.md),
and [runtime tool schemas](https://github.com/davebcn87/pi-autoresearch/blob/939ede8220daad440eac6bb7b6e315cc283e0a64/extensions/pi-autoresearch/index.ts).
Creation-skill blob: `8272f0173050523b7744ad8514677eaf5ae51d63`.
Runtime blob: `9e62aac705a3d9a120ed3006432484986cab35d2`.

Adopted: `.auto/` session layout; objective/measurement/scope discovery; validated
baseline; initialization, experiment, and result-logging stages; `METRIC` output;
secondary metrics; actionable side information; keep/discard/crash/checks_failed;
append-only history; learned-failure and idea-backlog recovery; backpressure outside
the measured metric; runner-owned automatic commit/revert when authorized.

Adaptations: Bend proof/validation is mandatory before acceptance, not optional;
proof is established before measurement and checked for freshness afterward;
hard correctness/secondary constraints outrank speed; complete logs outrank tool
tails; frozen measurement policy and new segments preserve comparability; advisory
confidence is not a statistical guarantee. No copied failure-masking shell example,
unlimited unattended work, delayed explicit cancellation, uncontrolled rollback,
automatic installation, hooks, dashboard configuration, or branch splitting.
Both workflows finish through the same review/comment/CI and same-PR delivery stages.
Portable log formats are explicitly distinguished from native tool-owned schemas.

Full MIT texts and attribution travel with the skill in
[third-party notices](../THIRD_PARTY_NOTICES.md). No upstream extension source,
website, or third-party bundled library is vendored.

## Bend and Giulio Rebuffo

[Official guide](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md):
local language discovery, explicit proof terms, claims/proofs separation, affine
ownership, termination, and checking. Read the installed guide at runtime instead
of copying a frozen web syntax reference.

[Official shader guide](https://github.com/bendlang/bend/blob/main/guide/SHADERS.md):
workload balance, ownership, granularity, generated-code inspection, and measurement.
Its AI-authorship notice and device-specific examples prevent treating its numbers
as universal tuning constants.

[Official limitations](https://github.com/bendlang/bend#limitations): trust and
implementation boundaries. Broad marketing claims are not unconditional guarantees.

Giulio2002's [objective](https://github.com/Giulio2002/bend-sha256/blob/main/OBJECTIVE.md),
[review policy](https://github.com/Giulio2002/bend-sha256/blob/main/ORCHESTRATOR.MD),
and [README](https://github.com/Giulio2002/bend-sha256/blob/main/README.md) informed
the original proof-preserving core: frozen public meaning, editable supporting
proofs, actual benchmark/theorem entry-point correspondence, raw evidence, and
explicit representation-bridge gaps. SHA-specific thresholds, dependencies,
model selections, and release pins are not reused.

## Packaging and validation limits

[Agent Skills specification](https://agentskills.io/specification): portable YAML
metadata and progressively loaded references. The initial author's inaccessible
[Doodlestein link](https://mdfromx.com/doodlestein/status/2101352970294096042) remains
unused as evidence. Actual workflow sources above replace the initial placeholder
interpretation of the autoImplement/autoResearch names.

Static metadata/link/content checks do not establish agent compliance. Evaluation
scenarios describe live checks to run; they are not fabricated results. A checked
application theorem still depends on specification adequacy and the declared trust
boundary. Native integration follows discovered capabilities rather than promising
compatibility with all future tools.
