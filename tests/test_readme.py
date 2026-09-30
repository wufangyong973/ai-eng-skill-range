from pathlib import Path

from skillrange.cli import main

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8-sig")
FAIL = ROOT / "katas" / "K01-loop-contract" / "fixtures" / "fail"


def test_readme_spoken_h1_is_skill_range():
    assert README.lstrip().startswith("# skill-range\n")
    assert "ai-eng-skill-range" in README


def test_readme_first_screen_matches_top100_craft():
    pip_at = README.find("pip install")
    interview_at = README.find("Interview pack")
    assert 0 <= pip_at < interview_at
    head = "\n".join(README.splitlines()[:28])
    assert "# skill-range" in head
    assert "git clone https://github.com/homayoun-safarpour/ai-eng-skill-range" in head
    assert "pip install -e" in head
    assert "fixtures/fail" in head
    assert "FAIL: missing headings:" in head
    assert "## 5. Irreversible" in head
    assert "Interview pack" not in head
    assert "\u2014" not in head


def test_readme_stranger_grade_exits_2():
    code = main(
        [
            "grade",
            "K01",
            "--submission",
            str(FAIL),
        ]
    )
    assert code == 2
