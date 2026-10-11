#!/usr/bin/env python3
"""Build Anki cards from a validated exam.json.

    python3 scripts/build.py path/to/exam.json [--out-dir DIR] [--timestamp SECONDS]

Writes, next to exam.json unless --out-dir is given:

  <id>.apkg          the deck, with its own note type and styling (preferred)
  <id>.txt           the same cards as a tab-separated file for File > Import
                     into the built-in "Basic" note type (fallback)
  <id>.preview.html  every card, front and back, rendered with MathJax, for
                     checking the cards by eye before importing

Card fronts are assembled here, from the shared context, the results of the
parts listed in `uses`, and the task. The model never retypes a carried-over
result, so it cannot drift from the part it came from.

Every note has a GUID derived from the exam id and part id, so importing a
rebuilt deck updates the existing cards instead of adding duplicates.
Standard library only.
"""

from __future__ import annotations

import argparse
import html
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apkg  # noqa: E402
import examlib  # noqa: E402
import validate  # noqa: E402

NOTE_TYPE_NAME = "Exam card (exam-to-anki v1)"

CSS = """
.card {
  font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 19px; line-height: 1.5; text-align: left;
  color: #1d1d1f; background: #fbfbfa; max-width: 760px; margin: 0 auto; padding: 4px 6px;
}
.card mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; padding: 2px 0; }
.e2a-src { font-size: 12px; letter-spacing: .02em; color: #77756f; margin-bottom: 10px; }
.e2a-ctx { margin: 0 0 10px; }
.e2a-lbl { font-weight: 600; margin-right: .25em; }
.e2a-pts { font-size: 13px; color: #77756f; }
.e2a-given {
  margin: 12px 0; padding: 8px 12px; border-left: 3px solid #3a7bd5;
  background: #eef3fb; border-radius: 0 6px 6px 0;
}
.e2a-given-h { font-size: 13px; font-weight: 600; color: #2c5fa8; margin-bottom: 2px; }
.e2a-given ul { margin: 0; padding-left: 1.1em; }
.e2a-task { margin-top: 12px; padding-top: 10px; border-top: 1px solid #e3e1db; }
.e2a-fig img { max-width: 100%; margin-top: 8px; }
.e2a-answer {
  font-weight: 700; font-size: 20px; padding: 8px 12px; margin-bottom: 8px;
  background: #edf7ef; border-left: 3px solid #2f8f4e; border-radius: 0 6px 6px 0;
}
.e2a-steps { margin: 8px 0; padding-left: 1.4em; }
.e2a-steps li { margin: 4px 0; }
.e2a-key { margin-top: 8px; font-size: 16px; color: #4a4843; }
.e2a-warn {
  font-size: 14px; font-weight: 600; color: #8a4b00; background: #fff3dc;
  padding: 4px 10px; border-radius: 6px; margin-bottom: 8px; display: inline-block;
}
hr#answer { border: 0; border-top: 2px dashed #d5d2ca; margin: 18px 0; }
.nightMode.card, .night_mode .card { color: #e8e6e1; background: #1f1f1e; }
.nightMode .e2a-src, .nightMode .e2a-pts, .night_mode .e2a-src, .night_mode .e2a-pts { color: #a09d96; }
.nightMode .e2a-given, .night_mode .e2a-given { background: #1d2a3d; border-color: #6c9de0; }
.nightMode .e2a-given-h, .night_mode .e2a-given-h { color: #9cc0f2; }
.nightMode .e2a-task, .night_mode .e2a-task { border-color: #3a3936; }
.nightMode .e2a-answer, .night_mode .e2a-answer { background: #1c3123; border-color: #5cbf7a; }
.nightMode .e2a-key, .night_mode .e2a-key { color: #c9c6bf; }
.nightMode .e2a-warn, .night_mode .e2a-warn { background: #3d2c10; color: #f3c178; }
""".strip()


def note_type() -> apkg.NoteType:
    return apkg.NoteType(
        id=examlib.stable_int("exam-to-anki/note-type/v1"),
        name=NOTE_TYPE_NAME,
        fields=["Front", "Back", "Ref"],
        qfmt="{{Front}}",
        afmt='{{FrontSide}}<hr id="answer">{{Back}}',
        css=CSS,
        sort_field=2,
    )


def cards(exam: examlib.Exam):
    title = exam.meta.get("short_title") or exam.meta.get("title", "")
    for leaf in exam.leaves:
        yield {
            "leaf": leaf,
            "guid": examlib.guid(exam, leaf),
            "front": examlib.render_front(exam, leaf),
            "back": examlib.render_back(exam, leaf),
            "ref": f"{title} · {leaf.full_label(exam.lang)}",
            "tags": examlib.tags_for(exam, leaf),
        }


def _one_line(text: str) -> str:
    return " ".join(text.replace("\t", " ").split())


def write_tsv(path: Path, exam: examlib.Exam, built: list[dict]) -> None:
    lines = [
        "#separator:tab",
        "#html:true",
        "#notetype:Basic",
        f"#deck:{exam.meta['deck']}",
        "#guid column:1",
        "#tags column:4",
    ]
    for c in built:
        lines.append("\t".join([c["guid"], _one_line(c["front"]), _one_line(c["back"]), " ".join(c["tags"])]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(path: Path, exam: examlib.Exam, built: list[dict]) -> None:
    title = html.escape(exam.meta.get("title", "Exam"))
    rows = []
    for c in built:
        leaf = c["leaf"]
        deps = ", ".join(leaf.uses)
        rows.append(
            f'<section class="pair" id="{html.escape(leaf.id)}">'
            f'<div class="meta">{html.escape(leaf.id)}'
            + (f" · uses {html.escape(deps)}" if deps else "")
            + f' · <code>{html.escape(" ".join(c["tags"]))}</code></div>'
            f'<div class="side"><div class="cap">Front</div><div class="card">{c["front"]}</div></div>'
            f'<div class="side"><div class="cap">Back</div><div class="card">{c["back"]}</div></div>'
            "</section>"
        )
    doc = f"""<!doctype html>
<html lang="{html.escape(exam.meta.get('language', 'en'))}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – card preview</title>
<script>window.MathJax = {{ tex: {{ inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }} }};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js" async></script>
<style>
body {{ margin: 0; padding: 24px 16px; background: #ecebe7; font-family: system-ui, sans-serif; }}
h1 {{ font-size: 20px; max-width: 1560px; margin: 0 auto 16px; }}
.pair {{ max-width: 1560px; margin: 0 auto 22px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.meta {{ grid-column: 1 / -1; font-size: 12px; color: #55534e; }}
.side {{ background: #fbfbfa; border: 1px solid #dad8d1; border-radius: 10px; padding: 14px; overflow-x: auto; }}
.cap {{ font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: #8b8880; margin-bottom: 6px; }}
@media (max-width: 900px) {{ .pair {{ grid-template-columns: 1fr; }} }}
{CSS}
</style></head><body>
<h1>{title} – {len(built)} cards</h1>
{''.join(rows)}
</body></html>
"""
    path.write_text(doc, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exam_json")
    ap.add_argument("--out-dir")
    ap.add_argument(
        "--timestamp",
        type=int,
        help="note modification time in seconds (default: $SOURCE_DATE_EPOCH or now); "
        "a newer timestamp makes Anki update cards that were imported before",
    )
    ap.add_argument("--no-apkg", action="store_true", help="only write the .txt and the preview")
    args = ap.parse_args(argv)

    exam, rep = validate.validate(args.exam_json)
    for line in rep.errors + rep.warnings:
        print(line)
    if exam is None or rep.errors:
        print("Not built: fix the errors above (python3 scripts/validate.py) first.")
        return 1

    out_dir = Path(args.out_dir) if args.out_dir else exam.path.resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = examlib.slug(exam.meta["id"])
    built = list(cards(exam))

    ts = args.timestamp
    if ts is None:
        ts = int(os.environ.get("SOURCE_DATE_EPOCH", time.time()))

    outputs = []
    if not args.no_apkg:
        media = []
        for leaf in exam.leaves:
            for fig in leaf.data.get("figures", []) or []:
                p = (exam.path.resolve().parent / fig).resolve()
                if p not in media:
                    media.append(p)
        nt = note_type()
        notes = [apkg.Note(guid=c["guid"], fields=[c["front"], c["back"], c["ref"]], tags=c["tags"]) for c in built]
        deck_name = exam.meta["deck"]
        apkg.write_apkg(
            out_dir / f"{stem}.apkg",
            deck_id=examlib.stable_int("exam-to-anki/deck/" + deck_name),
            deck_name=deck_name,
            note_type=nt,
            notes=notes,
            media=media,
            timestamp=ts,
            deck_description=html.escape(exam.meta.get("source", "")),
        )
        outputs.append(out_dir / f"{stem}.apkg")
    write_tsv(out_dir / f"{stem}.txt", exam, built)
    write_preview(out_dir / f"{stem}.preview.html", exam, built)
    outputs += [out_dir / f"{stem}.txt", out_dir / f"{stem}.preview.html"]

    deps = sum(1 for c in built if c["leaf"].uses)
    print(f"Built {len(built)} cards ({deps} with carried-over results) into deck '{exam.meta['deck']}':")
    for p in outputs:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
