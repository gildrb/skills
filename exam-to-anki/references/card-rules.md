# Card rules

One card per leaf sub-question. The build assembles each card the same way:

**Front**, top to bottom:

1. Header line: short exam title · `Aufgabe 11 (d)` / `Question 11 (d)`.
2. The question's `context`, with the question's points.
3. The `context` of each group the leaf sits in, with the group's label (`(a) Die folgenden Teilmengen sind Unterräume:`).
4. **From previous parts** (`Aus vorherigen Teilaufgaben`): the `result` of each part in `uses`, labelled `(a)`, `(c)`, or `Aufgabe 2 (b)` when it comes from another question.
5. The task, with its label and points.
6. Figures, if any.

**Back**: an "unverified" banner when needed, the answer (bold), the numbered steps, the key idea.

You control the content through exam.json; the layout is fixed so every card in every deck reads the same way.

## What to carry

Carrying results is the reason this skill exists, and getting it wrong in either direction ruins the card: carry too little and the card cannot be solved; carry too much and the card gives itself away.

**Carry a result when the part computes with it or cites it.**

| Later part | Earlier result | Carry? |
|---|---|---|
| (b) Compute `\det(L)` | (a) the matrix of `L` | Yes: the matrix. Without it the card cannot be solved. |
| (d) Find all eigenspaces | (a) the matrix, (c) the eigenvalues | Yes: both. Not (b), the determinant; (d) does not need it. |
| (b) Solve `45x+24y=5` | (a) solved `45x+24y=6` | Yes, but only the gcd, the one fact (b) needs. Not (a)'s solution set. |
| (d) Show `G'_U` is a group | (b) proved `\det(UAU^{-1})=\det A` | Yes: the proven statement, not the proof. |
| (c) `\operatorname{Proj}_u v` | (a) `\cos\theta`, computed via `\langle u,v\rangle=-6`, `\|u\|^2=5` | Yes: carry the inner products (a) computed, written as `result`, not the cosine. |
| (b) "Determine all `c` such that ... are independent" | (a) "Show ... are independent" | No. (b) reuses (a)'s *method*, not a result. Carrying (a) would hint the method. |
| (b) `M^k` for a non-diagonal `M` | (a) `A^k` for diagonal `A` | No. They look alike but (b) does not use (a). |

**Carry the statement in the form the exam expects you to use it.** If the exam works symbolically, carry `\dim\ker=n^2-1`, not "3 for `n=2`".

**Write `result` for the reader of the later card.** It is shown out of context, so it must be a complete statement: `\([L]_{\mathcal{B}} = \begin{pmatrix}...\end{pmatrix}\)`, not `the matrix above` or `= 54`.

**If the exam itself says "using (a)"** or "mit Teil (a)", the dependency is real; carry it. The validator warns when a task mentions a sibling label and `uses` is empty.

**A missing earlier result does not mean you should paraphrase it into `context`.** Use `uses` + `result`, so the value is written once and can be checked once.

## Wording

- Task and context verbatim, in the exam's language, notation and spelling, typos included. The user will meet this wording in the real exam.
- Answers, steps and key ideas in the exam's language too.
- `answer`: the result only, as short as the exam allows: `\(\det(3A)=54\)`, `Falsch: kein Unterraum (nicht abgeschlossen unter Addition).`, `76 Paare.` For proofs, the decisive line (the inductive step, the counterexample, the key equation).
- `steps`: what a student writes, nothing more. Two to five steps. No "First, we note that ..." filler.
- `key_idea`: one line a student could recall in the exam: the theorem, trick or pattern.

## Math

- MathJax only: `\( \)` and `\[ \]`. Anki does not render `$`.
- Keep the exam's symbols: if the exam writes `\operatorname{ggT}`, do not switch to `\gcd`; if it writes `\mathbb{R}_3[x]`, keep it.
- Matrices with `pmatrix`; determinants with `vmatrix`. Wide display formulas scroll horizontally on small screens, so they are fine, but avoid needless width.
- Write operators MathJax knows as commands (`\operatorname{tr}`, `\operatorname{span}`, `\ker`), so they render upright.

## Figures

If a part needs a figure (a circuit, a graph, a geometry sketch), crop it from the page image into a PNG next to exam.json and list it in that leaf's `figures`. Also describe what matters in text (labels, values, directions) in the `context` or `task`, so the card still works if an image fails. Figures shared by several parts: list the file on each leaf that needs it.

## Tags

Every card gets: the exam's `tags`, the exam id, `<exam id>::q<question id>`, `<exam id>::<part id>`, the question's and leaf's own `tags`, and `check` when unverified. Topic tags on questions (`eigenwerte`, `zahlentheorie`) let the user drill one topic across several exams.
