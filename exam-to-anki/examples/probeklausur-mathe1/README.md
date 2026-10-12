# Example: Probeklausur Mathematik 1 für Informatiker

Source: practice exam (Probeklausur) of *Mathematik 1 für Informatiker*, Julius-Maximilians-Universität Würzburg, Institut für Mathematik, winter semester 2025/26, 26 January 2026 (J. Ratzkin, N. de Sena Maier). The exam text is transcribed verbatim into `exam.json`; the PDF itself is not included.

13 questions → 34 cards (one per leaf sub-question), in German.

| File | What it is |
|---|---|
| `exam.json` | Exam text, solutions, dependency map and verification code |
| `jmu-mathe1-probeklausur-ws2526.apkg` | The deck, ready to import |
| `jmu-mathe1-probeklausur-ws2526.txt` | Same cards for File → Import into the Basic note type |
| `jmu-mathe1-probeklausur-ws2526.preview.html` | All cards rendered with MathJax |

## Carried-over results

| Card | Front carries | From |
|---|---|---|
| 2 (b) | ggT(45, 24) = 3 | 2 (a) |
| 9 (b) | dim Bild(tr) = 1, dim ker(tr) = n² − 1 | 9 (a) |
| 9 (c) | same | 9 (a) |
| 10 (d) | det(3A) = 54 | 10 (a) |
| 11 (b) | the matrix of L | 11 (a) |
| 11 (c) | the matrix of L | 11 (a) |
| 11 (d) | the matrix of L; eigenvalues 4, 2, −2 (double) | 11 (a), 11 (c) |
| 12 (c) | ⟨u, v⟩ = −6, ‖u‖² = 5, ‖v‖² = 17 | 12 (a) |
| 13 (d) | det(UAU⁻¹) = det(A) | 13 (b) |

Deliberately **not** carried: 7 (b) looks like 7 (a) but its matrix is not diagonal; 8 (b) reuses only the method of 8 (a). 2 (b) gets only the gcd from 2 (a), not 2 (a)'s solution set.

## Verification

```
python3 scripts/check_math.py examples/probeklausur-mathe1/exam.json
```

29 parts have a sympy or brute-force check and all pass. 5 parts are argued only (1c.i, 1c.ii, 9c, 13c, 13d); they were reviewed step by step, and all 34 answers were re-solved independently by a second agent. One convention is assumed: ℝₙ[x] means polynomials of degree ≤ n (as in 1a.ii). The card for 1c.ii says so and gives the answer under the other convention too.

## Rebuild

```
python3 scripts/build.py examples/probeklausur-mathe1/exam.json --timestamp 1760227200
```

With the same timestamp the `.apkg` is byte-for-byte identical.
