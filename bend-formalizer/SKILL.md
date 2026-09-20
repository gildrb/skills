---
name: bend-formalizer
description: Use this skill exclusively when the user explicitly asks to use Bend to mathematically prove a project or repository and requests the rewriting of logic in Bend, the declaration of properties in LAWS.bend, and the proof in PROOF.bend. Do not use it for general explanations, Bend generation without this formal objective, or generic validation.
metadata:
  activation-condition: explicit-bend-mathematical-proof-workflow
  source: active Bend installation and its matching documentation
---

# Bend Skill — mathematical formalization of projects

## Mandatory activation guard

Apply this skill only when the request explicitly aims to use Bend to mathematically prove a project or repository and includes the following workflow:

1. rewrite the project's relevant logic in Bend;
2. declare properties or invariants in `LAWS.bend`;
3. prove the laws in `PROOF.bend`.

If the request merely mentions "using Bend" but does not ask for a mathematical formalization of a project/repository involving `LAWS.bend` and `PROOF.bend`, **do not use this skill**. This includes:

- general questions or explanations about Bend;
- Bend code generation without the goal of mathematical proof;
- generic code validation without an explicit request to formalize the project in Bend;
- using Bend solely as a runtime, implementation language, or parallel backend;
- attempts to directly prove arbitrary code written in Python, TypeScript, Rust, C, or other languages.

This guard must be respected even if the skill is loaded manually. If any condition is missing, respond normally without applying this skill's workflow.

## Proof objective and scope

The goal is to construct a verifiable formalization of the project's relevant behavior:

```text
original project logic
        ↓ rewrite/modeling
Bend modules and functions
        ↓ specification
LAWS.bend
        ↓ checker-based proof
PROOF.bend
```

Bend does not automatically import external implementations, nor does it directly prove Python, TypeScript, Rust, or C code. If the original project is in another language:

- select the logic and behavior that need to be formalized;
- rewrite that behavior in Bend;
- declare the properties of the formal version in `LAWS.bend`;
- prove them in `PROOF.bend`;
- explicitly state that the proof covers the Bend model.

Equivalence between the original implementation and the Bend model requires an additional demonstration of refinement or equivalence. Do not claim that the original code has been proven simply because the Bend rewrite passed the checker.

## Sources of truth and version discovery

This skill does not pin a Bend version, installation directory, package manager, or operating system. Use the project's explicitly selected toolchain when one exists; otherwise resolve `bend` from the active `PATH`. Nix profiles and development shells are valid installations. Do not prefer an old `~/.bend/bin/bend` over the active toolchain.

Before writing Bend code:

1. Resolve the executable with `command -v bend` and inspect its help with `bend --help`. Use that same resolved executable for documentation, checking, and compilation throughout the task.
2. Query its version using the command advertised by its help. Current releases use `bend version`; do not assume `--version` is supported.
3. Read its language guide and relevant library definitions using the advertised commands. Current releases provide `bend guide` and `bend base`; inspect specific library names when supported.
4. Record the observed executable, version, and relevant capabilities. Never infer a version from this skill, an old transcript, or a different checkout.
5. If the CLI or documentation is unavailable, report the missing prerequisite. Do not invent syntax, silently switch installations, or substitute a legacy compiler that cannot check the required laws.

When the user requests the newest Bend, check the latest stable release from the official `bendlang/bend` project and compare it with the selected installation. Do not describe an installed or pinned version as "latest" without checking. If an update is needed, use the installation's owning package manager or declarative configuration with user authorization, then repeat discovery. For Nix-managed Bend, update the owning flake input and any explicit revision together; never run a self-updater against the Nix store. Preserve a project's explicit toolchain constraint unless the user authorizes changing it.

Do not install, update, publish, or fetch remote documentation silently. When remote documentation is needed, use official documentation matching the selected version. A checkout is authoritative only if it is the explicitly selected toolchain or matches the installed release; do not consult an unrelated stale copy.

The target repository supplies the behavior to formalize, its conventions, and the link between original code and the Bend model. The selected toolchain supplies language semantics, library APIs, proof rules, and backend capabilities.

## Version-adaptive implementation

Derive syntax and semantics from the selected installation rather than maintaining a frozen language reference in this skill. Confirm the actual type and ownership rules, numeric domains, pattern matching, recursion and termination restrictions, module syntax, effects, and proof syntax before relying on them.

Check parallel-call syntax and CPU/GPU backend support independently. Do not assume automatic parallelism, universal GPU availability, or identical execution behavior across interpreter, JavaScript, and native backends.

Do not mix examples from legacy Bend/HVM with a newer language generation. Conversely, do not reject a construct solely because an older release lacked it: the selected version's documentation and checker decide whether it is supported. Compatibility is capability-based, not a promise that every past or future compiler can express this proof workflow.

Keep proof guarantees explicit. Unsafe declarations, proof holes, unchecked assumptions, foreign code, and runtime measurements are not mathematical proofs of the modeled behavior. Do not weaken laws or domains to make a version's checker accept them.

## Mandatory Testing and Proof Structure

Before creating any Bend tests or proofs, understand how the repository organizes them. Examine directories, conventions, `AGENTS.md`, package manager configurations, and C documentation.
