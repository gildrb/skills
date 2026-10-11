"""Write an Anki .apkg file with the standard library only.

The package is a zip holding `collection.anki2` (an SQLite database in the
legacy schema 11, which every current Anki desktop, AnkiDroid and AnkiMobile
import) and a `media` JSON index. The table layout follows the format that
genanki writes (MIT, see THIRD_PARTY_NOTICES.md); no genanki code is needed
at run time.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE col (
    id integer primary key, crt integer not null, mod integer not null,
    scm integer not null, ver integer not null, dty integer not null,
    usn integer not null, ls integer not null, conf text not null,
    models text not null, decks text not null, dconf text not null,
    tags text not null
);
CREATE TABLE notes (
    id integer primary key, guid text not null, mid integer not null,
    mod integer not null, usn integer not null, tags text not null,
    flds text not null, sfld integer not null, csum integer not null,
    flags integer not null, data text not null
);
CREATE TABLE cards (
    id integer primary key, nid integer not null, did integer not null,
    ord integer not null, mod integer not null, usn integer not null,
    type integer not null, queue integer not null, due integer not null,
    ivl integer not null, factor integer not null, reps integer not null,
    lapses integer not null, left integer not null, odue integer not null,
    odid integer not null, flags integer not null, data text not null
);
CREATE TABLE revlog (
    id integer primary key, cid integer not null, usn integer not null,
    ease integer not null, ivl integer not null, lastIvl integer not null,
    factor integer not null, time integer not null, type integer not null
);
CREATE TABLE graves (
    usn integer not null, oid integer not null, type integer not null
);
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
"""

LATEX_PRE = (
    "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n"
    "\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n"
    "\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n"
)
LATEX_POST = "\\end{document}"


@dataclass
class NoteType:
    id: int
    name: str
    fields: list[str]
    qfmt: str
    afmt: str
    css: str = ""
    sort_field: int = 0


@dataclass
class Note:
    guid: str
    fields: list[str]
    tags: list[str] = field(default_factory=list)


def _strip(text: str) -> str:
    text = re.sub(r"<style.*?</style>|<script.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<img[^>]*src=[\"']?([^\"' >]+)[^>]*>", r" \1 ", text, flags=re.I)
    return re.sub(r"<[^>]+>", "", text).replace("&nbsp;", " ").strip()


def _checksum(text: str) -> int:
    return int(hashlib.sha1(_strip(text).encode("utf-8")).hexdigest()[:8], 16)


def _required(note_type: NoteType) -> list:
    used = [i for i, name in enumerate(note_type.fields) if "{{" + name + "}}" in note_type.qfmt]
    return [[0, "all", used or [0]]]


def write_apkg(
    out_path: str | Path,
    deck_id: int,
    deck_name: str,
    note_type: NoteType,
    notes: list[Note],
    media: list[str | Path] | None = None,
    timestamp: int | None = None,
    deck_description: str = "",
) -> None:
    ts = int(timestamp if timestamp is not None else __import__("time").time())
    ms = ts * 1000
    media = [Path(m) for m in (media or [])]

    model = {
        "css": note_type.css,
        "did": deck_id,
        "flds": [
            {"name": n, "ord": i, "font": "Arial", "media": [], "rtl": False, "size": 20, "sticky": False}
            for i, n in enumerate(note_type.fields)
        ],
        "id": str(note_type.id),
        "latexPost": LATEX_POST,
        "latexPre": LATEX_PRE,
        "latexsvg": False,
        "mod": ts,
        "name": note_type.name,
        "req": _required(note_type),
        "sortf": note_type.sort_field,
        "tags": [],
        "tmpls": [
            {
                "name": "Card 1",
                "ord": 0,
                "qfmt": note_type.qfmt,
                "afmt": note_type.afmt,
                "bqfmt": "",
                "bafmt": "",
                "bfont": "",
                "bsize": 0,
                "did": None,
            }
        ],
        "type": 0,
        "usn": -1,
        "vers": [],
    }

    def deck_json(did: int, name: str, desc: str = "") -> dict:
        return {
            "collapsed": False, "conf": 1, "desc": desc, "dyn": 0, "extendNew": 10,
            "extendRev": 50, "id": did, "lrnToday": [0, 0], "mod": ts, "name": name,
            "newToday": [0, 0], "revToday": [0, 0], "timeToday": [0, 0], "usn": -1,
        }

    decks = {"1": deck_json(1, "Default"), str(deck_id): deck_json(deck_id, deck_name, deck_description)}
    dconf = {
        "1": {
            "autoplay": True, "id": 1, "maxTaken": 60, "mod": 0, "name": "Default",
            "replayq": True, "timer": 0, "usn": 0,
            "lapse": {"delays": [10], "leechAction": 0, "leechFails": 8, "minInt": 1, "mult": 0},
            "new": {"bury": True, "delays": [1, 10], "initialFactor": 2500, "ints": [1, 4, 7],
                    "order": 1, "perDay": 20, "separate": True},
            "rev": {"bury": True, "ease4": 1.3, "fuzz": 0.05, "ivlFct": 1, "maxIvl": 36500,
                    "minSpace": 1, "perDay": 100},
        }
    }
    conf = {
        "activeDecks": [1], "addToCur": True, "collapseTime": 1200, "curDeck": 1,
        "curModel": str(note_type.id), "dueCounts": True, "estTimes": True, "newBury": True,
        "newSpread": 0, "nextPos": len(notes) + 1, "sortBackwards": False,
        "sortType": "noteFld", "timeLim": 0,
    }

    fd, db_path = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.executescript(SCHEMA_SQL)
        cur.execute(
            "INSERT INTO col VALUES(1,?,?,?,11,0,0,0,?,?,?,?,?)",
            (ts, ms, ms, json.dumps(conf), json.dumps({str(note_type.id): model}),
             json.dumps(decks), json.dumps(dconf), "{}"),
        )
        next_id = ms
        for pos, note in enumerate(notes):
            if len(note.fields) != len(note_type.fields):
                raise ValueError(f"note {note.guid} has {len(note.fields)} fields, expected {len(note_type.fields)}")
            nid, next_id = next_id, next_id + 1
            tags = " " + " ".join(note.tags) + " " if note.tags else ""
            cur.execute(
                "INSERT INTO notes VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (nid, note.guid, note_type.id, ts, -1, tags, "\x1f".join(note.fields),
                 _strip(note.fields[note_type.sort_field]), _checksum(note.fields[0]), 0, ""),
            )
            cid, next_id = next_id, next_id + 1
            cur.execute(
                "INSERT INTO cards VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (cid, nid, deck_id, 0, ts, -1, 0, 0, pos + 1, 0, 0, 0, 0, 0, 0, 0, 0, ""),
            )
        conn.commit()
        conn.close()

        out_path = Path(out_path)
        tmp_out = out_path.with_suffix(out_path.suffix + ".tmp")
        fixed = (1980, 1, 1, 0, 0, 0)
        with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zf:
            info = zipfile.ZipInfo("collection.anki2", fixed)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, Path(db_path).read_bytes())
            index = {str(i): p.name for i, p in enumerate(media)}
            info = zipfile.ZipInfo("media", fixed)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, json.dumps(index))
            for i, p in enumerate(media):
                info = zipfile.ZipInfo(str(i), fixed)
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, p.read_bytes())
        os.replace(tmp_out, out_path)
    finally:
        try:
            os.remove(db_path)
        except OSError:
            pass
