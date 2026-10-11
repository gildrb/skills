"""Tests for the exam-to-anki scripts. Standard library only.

    python3 -m unittest discover -s tests -v

check_math tests that need sympy are skipped when it is not installed.
"""

from __future__ import annotations

import copy
import io
import json
import re
import sqlite3
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import check_math  # noqa: E402
import examlib  # noqa: E402
import validate  # noqa: E402

EXAMPLE = ROOT / "examples" / "probeklausur-mathe1" / "exam.json"

try:
    import sympy  # noqa: F401

    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False


def leaf(id, label, **kw):
    d = {
        "id": id,
        "label": label,
        "task": kw.pop("task", f"Task {id} \\(x^2\\)"),
        "answer": kw.pop("answer", f"Answer for {id}"),
        "steps": kw.pop("steps", ["one step"]),
        "key_idea": kw.pop("key_idea", "an idea"),
        "status": kw.pop("status", "verified"),
    }
    d.update(kw)
    return d


def tiny_exam():
    return {
        "schema": "exam-to-anki/v1",
        "exam": {"id": "tiny", "title": "Tiny exam", "deck": "Test::Tiny", "language": "en", "expected_cards": 3},
        "questions": [
            {
                "id": "1",
                "label": "1.",
                "context": "Let \\(f(x)=x^2\\).",
                "parts": [
                    leaf("1a", "(a)", task="Compute \\(f(3)\\).", answer="\\(f(3)=9\\)", result="\\(f(3)=9\\)",
                         check="assert 3**2 == 9"),
                    leaf("1b", "(b)", task="Compute \\(f(3)+1\\).", answer="\\(10\\)", uses=["1a"]),
                ],
            },
            {"id": "2", "label": "2.", "task": "Prove it.", "answer": "Done.", "steps": ["s"],
             "key_idea": "k", "status": "unverified"},
        ],
    }


class TempExam:
    def __init__(self, data):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "exam.json"
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def __enter__(self):
        return self.path

    def __exit__(self, *exc):
        self.dir.cleanup()


def errors_for(data):
    with TempExam(data) as p:
        _, rep = validate.validate(p)
    return rep


class ValidateTests(unittest.TestCase):
    def test_tiny_exam_is_valid(self):
        rep = errors_for(tiny_exam())
        self.assertEqual(rep.errors, [])

    def test_example_is_valid(self):
        _, rep = validate.validate(EXAMPLE)
        self.assertEqual(rep.errors, [])

    def assertError(self, data, pattern):
        rep = errors_for(data)
        self.assertTrue(any(re.search(pattern, e) for e in rep.errors), rep.errors)

    def test_uses_later_part(self):
        d = tiny_exam()
        d["questions"][0]["parts"][0]["uses"] = ["1b"]
        d["questions"][0]["parts"][1]["result"] = "x"
        self.assertError(d, "comes later")

    def test_uses_unknown_part(self):
        d = tiny_exam()
        d["questions"][0]["parts"][1]["uses"] = ["9z"]
        self.assertError(d, "unknown part 9z")

    def test_uses_part_without_result(self):
        d = tiny_exam()
        del d["questions"][0]["parts"][0]["result"]
        self.assertError(d, "no result to carry over")

    def test_dollar_math(self):
        d = tiny_exam()
        d["questions"][0]["parts"][0]["task"] = "Compute $f(3)$."
        self.assertError(d, r"uses \$")

    def test_unbalanced_delimiters_and_braces(self):
        d = tiny_exam()
        d["questions"][0]["parts"][0]["answer"] = "\\(\\frac{1}{2\\)"
        self.assertError(d, "unbalanced braces")
        d = tiny_exam()
        d["questions"][0]["parts"][0]["answer"] = "\\(x"
        self.assertError(d, "never closed")
        d = tiny_exam()
        d["questions"][0]["parts"][0]["steps"] = ["\\(\\begin{pmatrix}1\\end{bmatrix}\\)"]
        self.assertError(d, "does not match")

    def test_answer_leak(self):
        d = tiny_exam()
        d["questions"][0]["context"] = "Let \\(f(x)=x^2\\), so \\(f(3)=9\\)."
        self.assertError(d, "answer leak")

    def test_expected_cards_mismatch(self):
        d = tiny_exam()
        d["exam"]["expected_cards"] = 4
        self.assertError(d, "expected_cards")

    def test_duplicate_id(self):
        d = tiny_exam()
        d["questions"][1]["id"] = "1a"
        self.assertError(d, "duplicate id")

    def test_missing_fields(self):
        d = tiny_exam()
        del d["questions"][0]["parts"][1]["key_idea"]
        d["questions"][0]["parts"][1]["status"] = "maybe"
        rep = errors_for(d)
        self.assertTrue(any("missing key_idea" in e for e in rep.errors))
        self.assertTrue(any("status must be" in e for e in rep.errors))

    def test_sibling_reference_without_uses_warns(self):
        d = tiny_exam()
        d["questions"][0]["parts"][1]["uses"] = []
        d["questions"][0]["parts"][1]["task"] = "Using (a), compute \\(f(3)+1\\)."
        rep = errors_for(d)
        self.assertTrue(any("mentions (a)" in w for w in rep.warnings), rep.warnings)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TempExam(tiny_exam())
        self.exam = examlib.load(self.tmp.__enter__())

    def tearDown(self):
        self.tmp.__exit__()

    def test_front_carries_result_not_reasoning(self):
        b = self.exam.by_id()["1b"]
        front = examlib.render_front(self.exam, b)
        self.assertIn("From previous parts", front)
        self.assertIn("\\(f(3)=9\\)", front)
        self.assertIn("Let \\(f(x)=x^2\\).", front)
        self.assertNotIn("Answer for", front)

    def test_front_without_uses_has_no_given_block(self):
        a = self.exam.by_id()["1a"]
        self.assertNotIn("e2a-given", examlib.render_front(self.exam, a))

    def test_unverified_is_tagged_and_flagged(self):
        q2 = self.exam.by_id()["2"]
        self.assertIn("check", examlib.tags_for(self.exam, q2))
        self.assertIn("e2a-warn", examlib.render_back(self.exam, q2))

    def test_guid_stable_and_safe(self):
        g1 = [examlib.guid(self.exam, l) for l in self.exam.leaves]
        g2 = [examlib.guid(examlib.load(self.exam.path), l) for l in examlib.load(self.exam.path).leaves]
        self.assertEqual(g1, g2)
        self.assertEqual(len(set(g1)), len(g1))
        self.assertTrue(all(re.fullmatch(r"e2a[0-9A-Za-z]+", g) for g in g1))

    def test_german_labels(self):
        d = tiny_exam()
        d["exam"]["language"] = "de"
        with TempExam(d) as p:
            ex = examlib.load(p)
            self.assertIn("Aus vorherigen Teilaufgaben", examlib.render_front(ex, ex.by_id()["1b"]))


class BuildTests(unittest.TestCase):
    def build(self, data, *extra):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "exam.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        with redirect_stdout(io.StringIO()) as out:
            code = build.main([str(p), "--timestamp", "1700000000", *extra])
        return code, Path(tmp.name), out.getvalue()

    def test_build_outputs(self):
        code, d, _ = self.build(tiny_exam())
        self.assertEqual(code, 0)
        apkg_path = d / "tiny.apkg"
        with zipfile.ZipFile(apkg_path) as zf:
            self.assertEqual(sorted(zf.namelist()), ["collection.anki2", "media"])
            db = Path(tempfile.mkdtemp()) / "c.anki2"
            db.write_bytes(zf.read("collection.anki2"))
        con = sqlite3.connect(db)
        self.assertEqual(con.execute("pragma integrity_check").fetchone()[0], "ok")
        self.assertEqual(con.execute("select count(*) from notes").fetchone()[0], 3)
        self.assertEqual(con.execute("select count(*) from cards").fetchone()[0], 3)
        dues = [r[0] for r in con.execute("select due from cards order by due")]
        self.assertEqual(dues, [1, 2, 3])
        decks = json.loads(con.execute("select decks from col").fetchone()[0])
        self.assertIn("Test::Tiny", [v["name"] for v in decks.values()])
        flds = con.execute("select flds from notes order by id").fetchall()
        self.assertTrue(all(f[0].count("\x1f") == 2 for f in flds))
        con.close()

        lines = (d / "tiny.txt").read_text(encoding="utf-8").splitlines()
        headers = [l for l in lines if l.startswith("#")]
        rows = [l for l in lines if not l.startswith("#")]
        self.assertIn("#guid column:1", headers)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(len(r.split("\t")) == 4 for r in rows))
        self.assertTrue((d / "tiny.preview.html").is_file())

    def test_build_is_deterministic(self):
        _, d1, _ = self.build(tiny_exam())
        _, d2, _ = self.build(tiny_exam())
        self.assertEqual((d1 / "tiny.apkg").read_bytes(), (d2 / "tiny.apkg").read_bytes())

    def test_build_refuses_invalid(self):
        d = tiny_exam()
        d["questions"][0]["parts"][1]["uses"] = ["nope"]
        code, folder, out = self.build(d)
        self.assertEqual(code, 1)
        self.assertIn("Not built", out)
        self.assertFalse((folder / "tiny.apkg").exists())

    def test_figures_go_into_media(self):
        data = tiny_exam()
        data["questions"][1]["figures"] = ["fig.png"]
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "exam.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        (Path(tmp.name) / "fig.png").write_bytes(b"\x89PNG fake")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build.main([str(p), "--timestamp", "1"]), 0)
        with zipfile.ZipFile(Path(tmp.name) / "tiny.apkg") as zf:
            self.assertEqual(json.loads(zf.read("media")), {"0": "fig.png"})
            self.assertEqual(zf.read("0"), b"\x89PNG fake")


class CheckMathTests(unittest.TestCase):
    def run_checks(self, data):
        with TempExam(data) as p, redirect_stdout(io.StringIO()) as out:
            code = check_math.main([str(p)])
        return code, out.getvalue()

    def test_passing_and_failing_checks(self):
        d = tiny_exam()
        code, out = self.run_checks(d)
        self.assertEqual(code, 0, out)
        self.assertIn("PASS  1a", out)
        self.assertIn("no check", out)
        d["questions"][0]["parts"][0]["check"] = ["x = 3", "assert x ** 2 == 10"]
        code, out = self.run_checks(d)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  1a", out)
        self.assertIn("assert x ** 2 == 10", out)

    @unittest.skipUnless(HAVE_SYMPY, "sympy not installed")
    def test_example_checks_pass(self):
        with redirect_stdout(io.StringIO()) as out:
            code = check_math.main([str(EXAMPLE)])
        self.assertEqual(code, 0, out.getvalue())

    @unittest.skipUnless(HAVE_SYMPY, "sympy not installed")
    def test_wrong_example_answer_is_caught(self):
        data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        q11 = next(q for q in bad["questions"] if q["id"] == "11")
        part = next(p for p in q11["parts"] if p["id"] == "11b")
        part["check"][-1] = "assert M.det() == -32"
        with TempExam(bad) as p, redirect_stdout(io.StringIO()) as out:
            code = check_math.main([str(p), "--only", "11b"])
        self.assertEqual(code, 1, out.getvalue())


if __name__ == "__main__":
    unittest.main()
