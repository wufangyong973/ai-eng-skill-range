from pathlib import Path

REQUIRED = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]

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
