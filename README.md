# Skills

Reusable agent skills in the [Agent Skills format](https://agentskills.io/specification).

## Bend

[Read the skill](bend/SKILL.md).

The agent reads the complete active `bend guide`, learns that executable's syntax
and verification behavior, implements the requested behavior, constructs formal
proofs, and runs the checker. No Bend release is hardcoded.

**autoImplement:** recover the selected plan, implement and prove, validate,
review/repair, address PR comments, inspect CI, and finish in the same PR.

**autoResearch:** establish a verified baseline and persistent `.auto/` session,
try a coherent change, prove and measure it, review, log learning, keep/discard,
and repeat within the authorized budget. Finish through the same delivery stages.

The workflows adapt Pi Workflows and pi-autoresearch. Compatible native facilities
are used when available; other agents execute the stages directly. No particular
agent, model, runner, or package manager is required. Research cannot retain an
unproved speedup. PR publication does not grant merge or deployment permission.

Keep the entire `bend` directory together, including references, templates, and
[third-party MIT notices](bend/THIRD_PARTY_NOTICES.md). These are agent instructions,
not an executable workflow engine or an independently protected verifier.

[Sources and adaptation details](bend/references/sources.md).
[Evaluation scenarios](evals/bend.md), not claimed live test results.
