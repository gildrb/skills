# Skills

Reusable agent skills in the [Agent Skills format](https://agentskills.io/specification).

## Bend

[Read the skill](bend/SKILL.md).

The agent reads the active `bend guide`, derives syntax and verification behavior
from that executable, implements the requested behavior, writes formal proofs,
and runs the checker before reporting completion. It does not pin a Bend release.

`autoImplement`: implement, prove, inspect diagnostics, repair, and review.

`autoResearch`: keep the public contract fixed while proposing, proving,
measuring, and reviewing optimization candidates.

Keep the `bend` directory and its references together when loading it into an
agent. The workflows do not require a particular agent vendor or research runner.
They are instructions, not a substitute for an independently protected verifier.

[Sources](bend/references/sources.md) document the design's provenance.
[Evaluation scenarios](evals/bend.md) describe how to check agent behavior.
