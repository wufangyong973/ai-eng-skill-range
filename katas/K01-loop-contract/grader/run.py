import re
from pathlib import Path

REQUIRED = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]


def _section_bodies(text):
    # Map each required heading to its body: text up to the next required
    # heading (or EOF), which is enough because strict only runs when every
    # heading is already present.
    ordered = sorted((text.find(h), h) for h in REQUIRED if text.find(h) != -1)
    bodies = {}
    for i, (_, heading) in enumerate(ordered):
        start = ordered[i][0] + len(heading)
        end = ordered[i + 1][0] if i + 1 < len(ordered) else len(text)
        bodies[heading] = text[start:end]
    return bodies


def _body_is_empty(body):
    # HTML comments and markdown headings carry no decision content.
    stripped = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    stripped = re.sub(r"(?m)^\s*#.*$", "", stripped)
    return not stripped.strip()


def grade(submission: Path) -> int:
    path = submission / "LOOP_CONTRACT.md"
    if not path.is_file():
        print("FAIL: missing LOOP_CONTRACT.md")
        return 2
    text = path.read_text(encoding="utf-8")
    missing = [h for h in REQUIRED if h not in text]
    if missing:
        print("FAIL: missing headings:")
        for heading in missing:
            print(f"  - {heading}")
        return 2
    return 0


def grade_strict(submission: Path) -> int:
    # Second, stricter mode: every required heading must also have
    # non-comment text under it. Default grade() stays heading-only so the
    # pass/fail golden fixtures keep their exit codes.
    if grade(submission) != 0:
        return 2
    text = (submission / "LOOP_CONTRACT.md").read_text(encoding="utf-8")
    empty = [h for h, body in _section_bodies(text).items() if _body_is_empty(body)]
    if empty:
        print("FAIL: empty sections under strict:")
        for heading in empty:
            print(f"  - {heading}")
        return 2
    return 0
