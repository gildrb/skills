#!/usr/bin/env python3
"""Run every part's `check` code and report which solutions it confirms.

    python3 scripts/check_math.py path/to/exam.json [--only 11c,11d]

A check is Python that recomputes the answer independently and asserts it,
for example:

    "check": [
      "M = sp.Matrix([[1,0,0,3],[0,0,-2,0],[0,-2,0,0],[3,0,0,1]])",
      "assert M.det() == 32"
    ]

Each check runs in its own Python process with a timeout. The names `sp`
(sympy, when installed), `Fraction`, `gcd`, `math`, `itertools` and `random`
(seeded) are already imported. Parts without a check are listed so you can
see what still rests on reasoning alone.

Exit status: 0 if every check passed, 1 if any failed or could not run.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import examlib  # noqa: E402

PRELUDE = textwrap.dedent(
    """
    import math, itertools, random
    from fractions import Fraction
    from math import gcd
    random.seed(0)
    try:
        import sympy as sp
    except ImportError:
        sp = None
    """
)

NEEDS_SYMPY = "__E2A_NEEDS_SYMPY__"


def run_check(code: str, timeout: float) -> tuple[str, str]:
    guard = f"\nif sp is None and 'sp.' in {code!r}:\n    print({NEEDS_SYMPY!r}); raise SystemExit(3)\n"
    program = PRELUDE + guard + code + "\n"
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(p for p in sys.path if p)
    try:
        proc = subprocess.run(
            [sys.executable, "-c", program],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return "FAIL", f"timed out after {timeout:.0f}s"
    if proc.returncode == 0:
        return "PASS", ""
    if NEEDS_SYMPY in proc.stdout:
        return "SKIP", "needs sympy (pip install sympy)"
    err = (proc.stderr or proc.stdout).strip().splitlines()
    tail = err[-1] if err else f"exit {proc.returncode}"
    if tail == "AssertionError":
        for line in reversed(err):
            if line.strip().startswith("assert"):
                tail = f"assertion failed: {line.strip()}"
                break
    return "FAIL", tail


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exam_json")
    ap.add_argument("--only", help="comma-separated part ids to run")
    ap.add_argument("--timeout", type=float, default=60.0)
    args = ap.parse_args(argv)

    exam = examlib.load(args.exam_json)
    only = {s.strip() for s in args.only.split(",")} if args.only else None
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    without: list[str] = []
    for leaf in exam.leaves:
        if only and leaf.id not in only:
            continue
        chk = leaf.data.get("check")
        if not chk:
            without.append(leaf.id)
            continue
        code = "\n".join(chk) if isinstance(chk, list) else chk
        status, detail = run_check(code, args.timeout)
        counts[status] += 1
        print(f"{status:4}  {leaf.id}" + (f"  {detail}" if detail else ""))
    if without:
        print(f"NONE  no check (reasoning only): {', '.join(without)}")
    print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, {counts['SKIP']} skipped")
    return 1 if counts["FAIL"] or counts["SKIP"] else 0


if __name__ == "__main__":
    sys.exit(main())
