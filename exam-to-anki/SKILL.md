---
name: exam-to-anki
description: Turn a past exam (PDF, scan, photo or pasted text) into verified Anki cards. Solve every part, check the math with code, and build one self-contained card per sub-question, where later parts like (b) and (c) carry the results of earlier parts on their front so they can be solved inline. Outputs an importable .apkg deck. Use whenever someone shares an old exam, Probeklausur, Altklausur, practice test or problem sheet and wants flashcards, Anki cards or a deck from it, even if they only say "make cards from this".
license: MIT
metadata:
  tags: "Anki, Flashcards, Spaced Repetition, Exams, Study"
  category: "learning"
---

# Exam to Anki

This skill turns an exam into a deck where **every sub-question is one card that can be solved cold**: the front holds the shared setup, the results of the earlier parts that this part builds on, and the task in the exam's own words; the back holds the verified answer, short steps and the key idea.

Models are good at solving exams and bad at the bookkeeping around them: a value from (a) retyped wrongly on the card for (c), a part silently skipped, a hint leaked onto a front, `$...$` math that Anki does not render. This skill moves that bookkeeping into scripts. You write one structured `exam.json`; the scripts check it, run your verification code, and assemble every card. **You never write a card front by hand, and you never retype a carried-over result.**

A complete worked example ships with the skill: `examples/probeklausur-mathe1/` (a German first-semester maths exam, 13 questions, 34 cards, 9 cards with carried-over results). Open its `exam.json` before you write your first one.

## The rule every card must pass

> Could someone solve this card from its front alone, with nothing else open, and not be handed the answer?

Everything below serves that rule.

## Workflow

Scripts live in `scripts/` next to this file. They need Python 3.9+ and nothing else; `sympy` makes the math checks far more useful (`pip install sympy`). Run them from the skill folder or pass full paths.

### 1. Read the whole exam and inventory it

Read every page **as an image** when the exam is a PDF or scan. Text extraction mangles formulas (sums, fractions, matrices, exponents come out scrambled), so use it only to copy plain wording, and take every formula from the page image.

Then list every leaf sub-question: `1a.i, 1a.ii, 1b.i, ..., 2a, 2b, 3, ...`. A leaf is the smallest thing the exam asks you to do and grades on its own. Count them; that count goes into `exam.expected_cards`, and the validator refuses the deck if a part was later skipped, merged or split.

Ask the user only if something is unreadable or the exam is ambiguous in a way that changes answers. Otherwise go on.

### 2. Solve every part, in order, and map the dependencies

Solve fully, as a strong student would in the exam. For each leaf note:

- the **answer**: the final result, stated the way the exam wants it (a value, a set, a matrix, true/false with the reason in one line, or the key line of a proof);
- the **steps**: the short path a student writes down, key equations only;
- the **key idea**: the one concept or trick that unlocks it;
- **uses**: which earlier parts this part genuinely needs a *result* from;
- **result**: for any part that a later part uses, the statement to carry over.

Deciding what to carry is the judgement call this skill exists for. Read `references/card-rules.md` § "What to carry" before you decide; the short version:

- Carry a result when the later part *computes with it* or *cites it* (the matrix from (a) when (b) asks for its determinant; the gcd from (a) when (b) asks whether another equation is solvable).
- Carry the *statement*, never the working. For a proof part, carry what was proven.
- Carry nothing when the later part only reuses the *method* of an earlier part, or when the parts merely look alike. Carrying then is a hint, and hints ruin a card.
- Carry only what that part needs. (d) using (a) and (c) does not get (b).

### 3. Write exam.json

Format: `references/exam-json.md`. The essentials:

- Copy context and task wording **verbatim**, in the exam's language and notation. Do not paraphrase, simplify or fix the exam's wording.
- Put the shared setup on the question (or group) as `context`, once. The build copies it onto every card that needs it.
- Math is MathJax: `\( ... \)` inline, `\[ ... \]` display. Never `$`. In JSON every backslash is doubled: `"\\(x^2\\)"`.
- Every leaf: `id`, `label`, `task`, `answer`, `steps`, `key_idea`, `status`, and `uses`/`result`/`check` where they apply.
- `status` is `verified` only after step 4. Anything you could not verify stays `unverified`; the card gets a warning banner and the tag `check`.

### 4. Verify with code

For every part with a computable answer, write a `check`: Python that **recomputes the answer independently** and asserts it. Do not just restate the answer; compute it another way (sympy, brute force over a range, substitution back into the equation, a random test of an identity).

```
python3 scripts/check_math.py path/to/exam.json
```

Every check must pass. A failing check means the solution or the check is wrong: find out which, fix it, and run again. Proof parts usually get no check; reread those proofs step by step instead, and set `status: unverified` if any step is shaky.

### 5. Validate

```
python3 scripts/validate.py path/to/exam.json
```

Fix every error. It catches: dependencies on unknown or later parts, dependencies on parts without a `result`, an answer or result that appears on its own front, `$` math, unbalanced `\( \)`, braces or `\begin`/`\end`, missing fields, duplicate ids, and a card count that does not match `expected_cards`. Read every warning; a warning that a task mentions "(a)" while `uses` is empty is often a missed dependency.

### 6. Build and look at the cards

```
python3 scripts/build.py path/to/exam.json
```

This writes, next to `exam.json`:

- `<exam id>.apkg`: the deck, with its own note type and styling (light and dark). This is what the user imports.
- `<exam id>.txt`: the same cards as a tab-separated file for File → Import into the built-in Basic note type, a fallback for when an .apkg cannot be used.
- `<exam id>.preview.html`: every card, front and back, rendered with MathJax.

Open the preview and look at it: every card with a "From previous parts" block, every card with a matrix or long display formula, and a handful of others. If a browser is available (Playwright, Chrome), screenshot those cards and read the images. Check that formulas render (no red MathJax errors, no raw `\(`), that each front passes the rule above, and that no back contradicts its front.

### 7. Deliver

Give the user the `.apkg` (and the `.txt` only if they asked or cannot use .apkg). In your reply:

- one line on what was built (cards, questions, how many carry results);
- the final answers in a compact list, so the user can spot-check;
- every part left `unverified`, and why;
- import: open the .apkg with Anki (double-click, or File → Import). Re-importing a rebuilt deck updates the same cards instead of duplicating them, because every card has a stable ID derived from the exam id and part id.

## Commands

| Command | What it does |
|---|---|
| `python3 scripts/validate.py exam.json` | Structural and content checks; exit 1 on errors |
| `python3 scripts/check_math.py exam.json [--only 2a,11c]` | Runs each part's `check` in its own process; exit 1 on any failure or skip |
| `python3 scripts/build.py exam.json [--out-dir DIR] [--timestamp S]` | Validates, then writes .apkg, .txt and preview.html |
| `python3 -m unittest discover -s tests` | The skill's own tests |

`build.py` refuses to build an exam.json with validation errors.

## Files

- `scripts/examlib.py`: the one place where card fronts, backs, tags and GUIDs are made.
- `scripts/validate.py`, `scripts/check_math.py`, `scripts/build.py`: the commands above.
- `scripts/apkg.py`: writes .apkg with the standard library only.
- `references/exam-json.md`: the exam.json format, field by field.
- `references/card-rules.md`: what goes on a card, what to carry, wording, math, figures, tags.
- `references/edge-cases.md`: proofs, true/false parts, figures, multi-question dependencies, scans, ambiguous exams, parts you cannot solve.
- `examples/probeklausur-mathe1/`: a full worked example with its built deck.
- `evals/evals.json`: test prompts and what a good result contains.
