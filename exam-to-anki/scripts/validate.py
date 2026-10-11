#!/usr/bin/env python3
"""Check an exam.json before any card is built.

    python3 scripts/validate.py path/to/exam.json

Exit status 0 means no errors (warnings may still be printed), 1 means errors.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import examlib  # noqa: E402

TEXT_FIELDS = ("context", "task", "answer", "result", "key_idea")
LEAF_REQUIRED = ("id", "task", "answer", "steps", "key_idea", "status")
SIBLING_REF = re.compile(
    r"(?:(?<![\w\\])\(([a-z])\)|\b(?:Teil(?:aufgabe)?|part|Aufgabe)\s*\(?([a-z])\)?(?![a-z]))",
    re.IGNORECASE,
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"WARNING {where}: {msg}")


def check_math(text: str, where: str, rep: Report) -> None:
    """MathJax delimiters must be \\( \\) or \\[ \\], balanced, with balanced braces inside."""
    if not isinstance(text, str):
        return
    if re.search(r"(?<!\\)\$", text):
        rep.error(where, "uses $ for math; Anki's MathJax needs \\( ... \\) or \\[ ... \\]")
    tokens = re.finditer(r"\\\(|\\\)|\\\[|\\\]", text)
    open_tok = None
    start = 0
    for m in tokens:
        tok = m.group(0)
        if tok in ("\\(", "\\["):
            if open_tok is not None:
                rep.error(where, f"math opened with {open_tok} is not closed before {tok}")
                return
            open_tok, start = tok, m.end()
        else:
            want = "\\)" if open_tok == "\\(" else "\\]"
            if open_tok is None or tok != want:
                rep.error(where, f"unmatched {tok}")
                return
            _check_braces(text[start:m.start()], where, rep)
            open_tok = None
    if open_tok is not None:
        rep.error(where, f"math opened with {open_tok} is never closed")


def _check_braces(math: str, where: str, rep: Report) -> None:
    depth = 0
    cleaned = re.sub(r"\\[{}]", "", math)
    for ch in cleaned:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                break
    if depth != 0:
        snippet = math if len(math) < 60 else math[:57] + "..."
        rep.error(where, f"unbalanced braces in math: {snippet}")
    envs = re.findall(r"\\(begin|end)\{(\w+\*?)\}", math)
    stack: list[str] = []
    for kind, name in envs:
        if kind == "begin":
            stack.append(name)
        elif not stack or stack.pop() != name:
            rep.error(where, f"\\end{{{name}}} does not match its \\begin")
            return
    if stack:
        rep.error(where, f"\\begin{{{stack[-1]}}} is never ended")


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", examlib.strip_html(text))


def validate(path: str | Path) -> tuple[examlib.Exam | None, Report]:
    rep = Report()
    try:
        exam = examlib.load(path)
    except FileNotFoundError:
        rep.error(str(path), "file not found")
        return None, rep
    except ValueError as exc:
        rep.error(str(path), f"not valid JSON: {exc}")
        return None, rep

    data = exam.data
    if data.get("schema") != examlib.SCHEMA:
        rep.error("schema", f'must be "{examlib.SCHEMA}"')
    meta = data.get("exam")
    if not isinstance(meta, dict):
        rep.error("exam", "missing exam object")
        meta = {}
    for key in ("id", "title", "deck", "language"):
        if not meta.get(key):
            rep.error(f"exam.{key}", "missing")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        rep.error("questions", "must be a non-empty list")
        return exam, rep

    seen_ids: dict[str, str] = {}

    def visit(node, where: str) -> None:
        if not isinstance(node, dict):
            rep.error(where, "must be an object")
            return
        nid = str(node.get("id", ""))
        here = f"{where}[{nid or '?'}]"
        if not nid:
            rep.error(here, "missing id")
        elif nid in seen_ids:
            rep.error(here, f"duplicate id (also at {seen_ids[nid]})")
        else:
            seen_ids[nid] = here
        for key in TEXT_FIELDS:
            if key in node:
                check_math(node[key], f"{here}.{key}", rep)
        parts = node.get("parts")
        if parts is not None and (not isinstance(parts, list) or not parts):
            rep.error(here, "parts must be a non-empty list")
            return
        if parts:
            for key in ("task", "answer", "steps"):
                if key in node:
                    rep.error(here, f"has both parts and {key}; put {key} on a leaf part")
            for child in parts:
                visit(child, here)

    for i, q in enumerate(questions):
        visit(q, f"questions[{i}]")

    by_id = exam.by_id()
    exam_dir = Path(path).resolve().parent
    for leaf in exam.leaves:
        d = leaf.data
        here = f"part {leaf.id or '?'}"
        for key in LEAF_REQUIRED:
            if d.get(key) in (None, "", []):
                rep.error(here, f"missing {key}")
        if d.get("status") and d["status"] not in examlib.STATUSES:
            rep.error(here, f"status must be one of {', '.join(examlib.STATUSES)}")
        if leaf.data is not leaf.question and not d.get("label"):
            rep.error(here, "missing label, e.g. (a)")
        steps = d.get("steps")
        if steps is not None and not isinstance(steps, list):
            rep.error(here, "steps must be a list of strings")
        else:
            for j, step in enumerate(steps or []):
                check_math(step, f"{here}.steps[{j}]", rep)
        chk = d.get("check")
        if chk is not None and not (
            isinstance(chk, str) or (isinstance(chk, list) and all(isinstance(x, str) for x in chk))
        ):
            rep.error(here, "check must be a string or a list of lines")
        for fig in d.get("figures", []) or []:
            if not (exam_dir / fig).is_file():
                rep.error(here, f"figure not found: {fig}")

        uses = d.get("uses", []) or []
        if not isinstance(uses, list):
            rep.error(here, "uses must be a list of part ids")
            uses = []
        for uid in uses:
            used = by_id.get(str(uid))
            if used is None:
                rep.error(here, f"uses unknown part {uid}")
            elif used is leaf:
                rep.error(here, "uses itself")
            elif used.order > leaf.order:
                rep.error(here, f"uses {uid}, which comes later in the exam")
            elif not used.data.get("result"):
                rep.error(here, f"uses {uid}, but {uid} has no result to carry over")
        if len(set(map(str, uses))) != len(uses):
            rep.error(here, "lists the same part twice in uses")

        front = _norm(examlib.render_front(exam, leaf))
        own_result = _norm(d.get("result", ""))
        own_answer = _norm(d.get("answer", ""))
        if own_result and len(own_result) >= 4 and own_result in front:
            rep.error(here, "its own result appears on its front (answer leak)")
        if own_answer and len(own_answer) >= 6 and own_answer in front:
            rep.error(here, "its own answer appears on its front (answer leak)")

        if not uses:
            sibling_labels = {
                s.data.get("label", "").strip("() .").lower(): s
                for s in exam.leaves
                if s.question is leaf.question and s.order < leaf.order
            }
            text = examlib.strip_html(d.get("task", ""))
            for m in SIBLING_REF.finditer(text):
                ref = (m.group(1) or m.group(2) or "").lower()
                if ref in sibling_labels:
                    rep.warn(here, f"task mentions ({ref}) but uses is empty; carry its result if needed")
                    break

    expected = meta.get("expected_cards")
    if expected is not None and expected != len(exam.leaves):
        rep.error(
            "exam.expected_cards",
            f"says {expected} sub-questions, but exam.json has {len(exam.leaves)} leaf parts; "
            "a part was skipped, merged or split",
        )
    unverified = [leaf.id for leaf in exam.leaves if leaf.data.get("status") == "unverified"]
    if unverified:
        rep.warn("status", f"unverified parts (will be tagged 'check'): {', '.join(unverified)}")
    return exam, rep


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exam_json")
    args = ap.parse_args(argv)
    exam, rep = validate(args.exam_json)
    for line in rep.errors + rep.warnings:
        print(line)
    if exam is not None and not rep.errors:
        deps = sum(1 for leaf in exam.leaves if leaf.uses)
        print(
            f"OK      {len(exam.leaves)} cards from {len(exam.data.get('questions', []))} questions, "
            f"{deps} with carried-over results"
        )
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
