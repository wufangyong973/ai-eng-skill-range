"""Discover and grade AI-engineering katas."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def katas_dir() -> Path:
    return repo_root() / "katas"


def list_katas() -> list[Path]:
    root = katas_dir()
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("K"))


def find_kata(kata_id: str) -> Path:
    """Resolve K01 or K01-loop-contract or loop-contract."""
    key = kata_id.strip()
    for path in list_katas():
        name = path.name
        if name == key or name.startswith(key + "-") or name.endswith("-" + key):
            return path
        # id prefix match: K01
        if name.split("-", 1)[0].upper() == key.upper():
            return path
    raise FileNotFoundError(f"unknown kata: {kata_id}")


def load_grade_fn(kata_path: Path):
    run_py = kata_path / "grader" / "run.py"
    if not run_py.is_file():
        raise FileNotFoundError(f"missing grader: {run_py}")
    spec = importlib.util.spec_from_file_location(f"grader_{kata_path.name}", run_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {run_py}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "grade"):
        raise AttributeError(f"{run_py} must define grade(submission: Path) -> int")
    return mod.grade


def grade_kata(kata_id: str, submission: Path | None = None) -> int:
    kata = find_kata(kata_id)
    grade = load_grade_fn(kata)
    sub = submission if submission is not None else kata / "starter"
    if not sub.exists():
        print(f"FAIL: submission path missing: {sub}", file=sys.stderr)
        return 2
    code = int(grade(Path(sub)))
    if code not in (0, 2):
        print(f"FAIL: grader returned {code}; only 0 or 2 allowed", file=sys.stderr)
        return 2
    label = "PASS" if code == 0 else "FAIL"
    print(f"{label}: {kata.name} submission={Path(sub).as_posix()}")
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skillrange", description="Grade AI-engineering katas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List katas")
    p_list.set_defaults(fn="list")

    p_grade = sub.add_parser("grade", help="Grade a kata submission")
    p_grade.add_argument("kata_id", help="Kata id, e.g. K01 or K01-loop-contract")
    p_grade.add_argument(
        "--submission",
        type=Path,
        default=None,
        help="Path to submission directory (default: kata starter/)",
    )
    p_grade.set_defaults(fn="grade")

    args = parser.parse_args(argv)
    if args.fn == "list":
        for path in list_katas():
            print(path.name)
        return 0
    return grade_kata(args.kata_id, args.submission)


if __name__ == "__main__":
    raise SystemExit(main())
