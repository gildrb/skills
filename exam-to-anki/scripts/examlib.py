"""Shared model for exam-to-anki: load exam.json, walk its parts, render cards.

Standard library only. Every other script imports this module, so the card
text is produced in exactly one place.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA = "exam-to-anki/v1"

STATUSES = ("verified", "unverified")

LABELS = {
    "de": {
        "given": "Aus vorherigen Teilaufgaben",
        "question": "Aufgabe",
        "points": "P",
        "key_idea": "Idee",
        "unverified": "Nicht verifiziert – Lösung prüfen",
    },
    "en": {
        "given": "From previous parts",
        "question": "Question",
        "points": "pts",
        "key_idea": "Key idea",
        "unverified": "Unverified – check this solution",
    },
}


def labels(language: str) -> dict[str, str]:
    return LABELS.get((language or "en").split("-")[0].lower(), LABELS["en"])


@dataclass
class Leaf:
    """One sub-question that becomes exactly one card."""

    data: dict[str, Any]
    question: dict[str, Any]
    ancestors: list[dict[str, Any]]
    order: int

    @property
    def id(self) -> str:
        return str(self.data.get("id", ""))

    @property
    def uses(self) -> list[str]:
        return [str(u) for u in self.data.get("uses", []) or []]

    def label_path(self) -> str:
        """Labels below the question, e.g. "(a) i." for 1a.i."""
        parts = [a.get("label", "") for a in self.ancestors[1:]]
        if self.data is not self.question:
            parts.append(self.data.get("label", ""))
        return " ".join(p for p in parts if p).strip()

    def full_label(self, lang: dict[str, str]) -> str:
        q = self.question.get("label") or self.question.get("id", "")
        q = str(q).rstrip(".")
        rest = self.label_path()
        return f"{lang['question']} {q} {rest}".strip()


@dataclass
class Exam:
    path: Path
    data: dict[str, Any]
    leaves: list[Leaf] = field(default_factory=list)

    @property
    def meta(self) -> dict[str, Any]:
        return self.data.get("exam", {})

    @property
    def lang(self) -> dict[str, str]:
        return labels(self.meta.get("language", "en"))

    def by_id(self) -> dict[str, Leaf]:
        return {leaf.id: leaf for leaf in self.leaves}


def load(path: str | Path) -> Exam:
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    exam = Exam(path=path, data=data)
    order = 0
    for question in data.get("questions", []) or []:
        if not isinstance(question, dict):
            continue
        for leaf in _walk(question, question, []):
            leaf.order = order
            order += 1
            exam.leaves.append(leaf)
    return exam


def _walk(node: dict[str, Any], question: dict[str, Any], ancestors: list[dict[str, Any]]):
    """Yield leaves in exam order. `ancestors` runs from the question down to the leaf's parent."""
    parts = node.get("parts")
    if parts:
        for child in parts:
            if isinstance(child, dict):
                yield from _walk(child, question, ancestors + [node])
    else:
        yield Leaf(data=node, question=question, ancestors=ancestors, order=0)


def given_label(user: Leaf, used: Leaf, lang: dict[str, str]) -> str:
    """How a carried-over result is labelled on the front of `user`."""
    if used.question is user.question:
        return used.label_path() or used.full_label(lang)
    return used.full_label(lang)


def render_front(exam: Exam, leaf: Leaf) -> str:
    lang = exam.lang
    by_id = exam.by_id()
    out: list[str] = []
    title = exam.meta.get("short_title") or exam.meta.get("title", "")
    head = leaf.full_label(lang)
    out.append(f'<div class="e2a-src">{html.escape(title)} · {html.escape(head)}</div>')

    q = leaf.question
    q_points = q.get("points")
    q_head = ""
    if q_points and leaf.data is not q:
        q_head = f'<span class="e2a-pts">({html.escape(str(q_points))})</span> '
    if q.get("context"):
        out.append(f'<div class="e2a-ctx">{q_head}{q["context"]}</div>')
    elif q_head:
        out.append(f'<div class="e2a-ctx">{q_head}</div>')

    for anc in leaf.ancestors[1:]:
        if anc.get("context"):
            lbl = anc.get("label", "")
            out.append(f'<div class="e2a-ctx"><span class="e2a-lbl">{html.escape(lbl)}</span> {anc["context"]}</div>')

    if leaf.data.get("context") and leaf.data is not q:
        out.append(f'<div class="e2a-ctx">{leaf.data["context"]}</div>')

    if leaf.uses:
        items = []
        for uid in leaf.uses:
            used = by_id.get(uid)
            if used is None:
                continue
            items.append(
                f'<li><span class="e2a-lbl">{html.escape(given_label(leaf, used, lang))}</span> '
                f'{used.data.get("result", "")}</li>'
            )
        out.append(
            f'<div class="e2a-given"><div class="e2a-given-h">{html.escape(lang["given"])}:</div>'
            f'<ul>{"".join(items)}</ul></div>'
        )

    task_label = leaf.data.get("label", "") if leaf.data is not q else ""
    pts = leaf.data.get("points")
    pts_html = ""
    if pts not in (None, "") and leaf.data is not q:
        pts_html = f' <span class="e2a-pts">[{html.escape(str(pts))} {html.escape(lang["points"])}]</span>'
    elif pts not in (None, "") and leaf.data is q:
        pts_html = f'<span class="e2a-pts">({html.escape(str(pts))})</span> '
    lbl_html = f'<span class="e2a-lbl">{html.escape(task_label)}</span>' if task_label else ""
    if leaf.data is q:
        out.append(f'<div class="e2a-task">{pts_html}{leaf.data.get("task", "")}</div>')
    else:
        out.append(f'<div class="e2a-task">{lbl_html}{pts_html} {leaf.data.get("task", "")}</div>')

    for fig in leaf.data.get("figures", []) or []:
        out.append(f'<div class="e2a-fig"><img src="{html.escape(Path(fig).name)}"></div>')
    return "".join(out)


def render_back(exam: Exam, leaf: Leaf) -> str:
    lang = exam.lang
    d = leaf.data
    out: list[str] = []
    if d.get("status") == "unverified":
        out.append(f'<div class="e2a-warn">⚠ {html.escape(lang["unverified"])}</div>')
    out.append(f'<div class="e2a-answer">{d.get("answer", "")}</div>')
    steps = d.get("steps") or []
    if steps:
        out.append('<ol class="e2a-steps">' + "".join(f"<li>{s}</li>" for s in steps) + "</ol>")
    if d.get("key_idea"):
        out.append(
            f'<div class="e2a-key"><b>{html.escape(lang["key_idea"])}:</b> {d["key_idea"]}</div>'
        )
    return "".join(out)


def tags_for(exam: Exam, leaf: Leaf) -> list[str]:
    base = [_tag(t) for t in exam.meta.get("tags", []) or []]
    exam_tag = _tag(exam.meta.get("id", "exam"))
    q_id = _tag(str(leaf.question.get("id", "")))
    tags = base + [exam_tag, f"{exam_tag}::q{q_id}", f"{exam_tag}::{_tag(leaf.id)}"]
    tags += [_tag(t) for t in leaf.question.get("tags", []) or []]
    tags += [_tag(t) for t in leaf.data.get("tags", []) or []]
    if leaf.data.get("status") == "unverified":
        tags.append("check")
    seen: list[str] = []
    for t in tags:
        if t and t not in seen:
            seen.append(t)
    return seen


def _tag(text: str) -> str:
    text = re.sub(r"\s+", "_", str(text).strip())
    return re.sub(r"[^\w:.\-]", "", text)


def guid(exam: Exam, leaf: Leaf) -> str:
    """Stable per exam id + part id, so a rebuilt deck updates instead of duplicating."""
    return "e2a" + _base62(f"exam-to-anki::{exam.meta.get('id', '')}::{leaf.id}")


_B62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _base62(text: str) -> str:
    """Letters and digits only, so a GUID can never start a line with '#' in the import file."""
    n = int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:10], "big")
    out = []
    while n:
        n, r = divmod(n, len(_B62))
        out.append(_B62[r])
    return "".join(reversed(out)) or "0"


def stable_int(text: str) -> int:
    """An id in [2^30, 2^31) derived from text, the range Anki tools use for decks and note types."""
    n = int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")
    return (1 << 30) + n % (1 << 30)


def strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text or ""))


def slug(text: str) -> str:
    text = re.sub(r"[^\w\-]+", "-", str(text)).strip("-")
    return text or "exam"
