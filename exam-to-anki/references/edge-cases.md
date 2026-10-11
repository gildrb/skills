# Edge cases

## Sub-sub-parts (i., ii.)

If each sub-sub-part is a separate claim or task (prove-or-disprove lists, "compute for i. ... ii. ..."), each is a leaf and a card. If the roman numerals are steps of one task that only make sense together, make the group the leaf and put the steps in its `task`. Decide once while inventorying, and set `expected_cards` to match.

## Proof and "show that" parts

`answer` is the decisive line of the proof, `steps` the outline. Carry what was proven (the statement) to later parts, never the proof. Proofs usually get no `check`; a randomized or symbolic check of the claimed identity is still worth writing when possible (the example checks `(UAU^{-1})^k=UA^kU^{-1}` for concrete matrices).

## True/false, prove-or-disprove

`answer` starts with the verdict (`Wahr:` / `Falsch:`, `True:` / `False:`) and gives the reason in a few words. A counterexample belongs in `steps`, and the `check` should verify it.

## Ambiguous notation

If a symbol can mean two things (`\mathbb{R}_n[x]` as degree `\le n` or `< n`; `\mathbb{N}` with or without 0), use the course's convention when it is evident from the exam, and state the assumption in the first step. Ask the user only if the answers differ and nothing in the exam settles it.

## Answers that depend on a parameter

State the case split in `answer` (e.g. "injective only for `n=1`"). Do not silently assume the common case.

## Dependencies across questions

Allowed: `uses: ["2a"]` on a part of question 5. The front labels it `Aufgabe 2 (a)`. Use it only when the exam really chains questions.

## A part you cannot solve or verify

Still make the card: best answer, `status: "unverified"`, and say in `steps` what is uncertain. The card shows a warning and is tagged `check`. List it in your reply. Never mark a guess as verified.

## A later part that depends on an unverified result

Carry it anyway. The front shows the value as given, which is how the exam treats it too. The user still learns the method, and the unverified source card is flagged.

## Scans, photos, handwriting

Read each page as an image. If something is illegible, ask; if the user is not around, transcribe your best reading, mark the part `unverified`, and say what you could not read.

## Multiple-choice questions

Put the options in `task` (an HTML list is fine). `answer` is the correct option(s) with a one-line reason; `steps` say why each wrong option is wrong when that is instructive.

## Very long shared setups

Put the setup in `context` once. Every card that needs it repeats it; that is intended, because the card must stand alone. If the setup is a long table, render it as an HTML `<table>` in `context`.

## Re-running on the same exam

Keep `exam.id` and every part `id` unchanged. Rebuild and re-import: Anki updates the existing notes (same GUIDs, newer modification time) and keeps review history. Changing an id creates a new card, and the old one stays in the collection.

## Exams in other languages

Write `language` correctly. For `de` and `en` the card labels are translated; other languages get English labels until a translation is added to `LABELS` in `scripts/examlib.py`.
