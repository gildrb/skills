# exam.json format (`exam-to-anki/v1`)

One file per exam. It holds the exam's text, your solutions, the dependency map and the verification code. Every card is built from it; nothing else is needed.

## Skeleton

```json
{
  "schema": "exam-to-anki/v1",
  "exam": {
    "id": "uni-course-exam-2026",
    "title": "Full exam title as printed",
    "short_title": "Short title for the card header",
    "source": "University, course, semester, date, authors",
    "language": "de",
    "deck": "Course::Exam name",
    "tags": ["course"],
    "expected_cards": 34
  },
  "questions": [ ... ]
}
```

| Field | Required | Meaning |
|---|---|---|
| `schema` | yes | Always `"exam-to-anki/v1"`. |
| `exam.id` | yes | Stable, unique slug. Card GUIDs come from it, so **never change it** once a deck was imported; changing it makes Anki treat every card as new. It also names the output files and the tag. |
| `exam.title` | yes | Exam title as printed. |
| `exam.short_title` | no | Shown in each card's header line; defaults to `title`. |
| `exam.source` | no | Where the exam is from. Stored as the deck description. |
| `exam.language` | yes | BCP-47 code of the exam's language. `de` and `en` have built-in label text ("Aus vorherigen Teilaufgaben" / "From previous parts"); other languages fall back to English labels. |
| `exam.deck` | yes | Anki deck name; `::` makes subdecks. |
| `exam.tags` | no | Tags on every card. |
| `exam.expected_cards` | strongly recommended | The number of leaf sub-questions you counted when you first read the exam. The validator fails when it differs from the number of leaves in the file. |

## Questions and parts

A question is a node. A node either has `parts` (a list of child nodes) or is a **leaf** (it has a `task`). Nest as deep as the exam does: question 1 → part (a) → sub-part i.

```json
{
  "id": "11", "label": "11.", "points": "20 Punkte", "tags": ["eigenwerte"],
  "context": "Sei \\[L(A)=3\\,\\operatorname{tr}(A)\\,\\mathbb{1}_2-2A^T.\\]",
  "parts": [
    { "id": "11a", "label": "(a)", "points": 4,
      "task": "Berechnen Sie die Darstellungsmatrix ...",
      "answer": "\\([L]_{\\mathcal{B}}=\\begin{pmatrix}...\\end{pmatrix}\\)",
      "result": "\\([L]_{\\mathcal{B}}=\\begin{pmatrix}...\\end{pmatrix}\\)",
      "steps": ["...", "..."],
      "key_idea": "...",
      "status": "verified",
      "check": ["M = ...", "assert M == sp.Matrix(...)"] },
    { "id": "11b", "label": "(b)", "points": 4, "uses": ["11a"],
      "task": "Berechnen Sie \\(\\det(L)\\).", "answer": "\\(\\det(L)=32\\)", ... }
  ]
}
```

### Fields on any node

| Field | Meaning |
|---|---|
| `id` | Unique across the whole file. Use the exam's numbering: `1`, `1a`, `1a.i`, `11c`. Leaf ids end up in tags and GUIDs, so keep them stable. |
| `label` | The label exactly as printed: `1.`, `(a)`, `i.`. Required on every leaf below a question. |
| `context` | Setup text shared by everything below this node, verbatim. Shown on every card under it, in order from the question down. |
| `points` | Shown on the card. A number on a leaf (`4` → `[4 P]`), or free text on a question (`"4 Punkte pro Teilaufgabe"`). |
| `tags` | Extra tags for cards under this node (topic tags work well). |

### Fields on a leaf

| Field | Required | Meaning |
|---|---|---|
| `task` | yes | What this part asks, verbatim, without its label. A question without parts puts its whole text here. |
| `answer` | yes | The final answer, shown bold first on the back. One line where possible. Do not repeat the label. |
| `steps` | yes | List of short solution steps (strings). Key equations, not prose. |
| `key_idea` | yes | One line naming the concept or trick. |
| `status` | yes | `verified` or `unverified`. |
| `uses` | no | Ids of earlier leaves whose `result` this part needs. Order them as they should appear. |
| `result` | when used | The statement later parts receive, written so it reads well on another card: `"\\(\\operatorname{ggT}(45,24)=3\\)"`. It may differ from `answer`: (a) may *answer* with a full solution set but *pass on* only the gcd its successor needs. |
| `check` | for computable answers | Python (a string, or a list of lines) that recomputes the answer independently and asserts it. `sp` (sympy), `Fraction`, `gcd`, `math`, `itertools` and a seeded `random` are pre-imported. |
| `figures` | no | Image files (paths relative to exam.json) shown under the task and packed into the .apkg. |

### Rules the validator enforces

- `uses` may only point to leaves that come **earlier** in the file, and each must have a `result`.
- A leaf's own `answer` or `result` must not appear on its own front (a leak, usually through `context`).
- Math only in `\( \)` and `\[ \]`, balanced, with balanced `{}` and matching `\begin`/`\end`; no `$`.
- A node has either `parts` or `task`/`answer`/`steps`, not both.
- Leaf count equals `expected_cards` when that is set.

## JSON and LaTeX

Every LaTeX backslash is doubled in JSON: `\frac{a}{b}` is written `"\\frac{a}{b}"`, and a matrix row break `\\` is written `"\\\\"`. Literal braces in sets are `\{` and `\}`, so `"\\{1,2\\}"`. When a file gets long, writing it from a short Python script (raw strings, `json.dump(..., ensure_ascii=False, indent=2)`) avoids escaping mistakes; the example's file was made that way.

Text can contain light HTML (`<b>`, `<i>`, `<br>`). Do not put line breaks or tabs inside strings; the build turns all whitespace into single spaces in the .txt file.
