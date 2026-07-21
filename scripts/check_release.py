"""Fail unless a release tag exactly matches the static project version."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
TAG_PATTERN = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+")


def project_version(pyproject: Path = PYPROJECT) -> str:
    with pyproject.open("rb") as source:
        return tomllib.load(source)["project"]["version"]


def validate_release_tag(tag: str, pyproject: Path = PYPROJECT) -> str:
    if TAG_PATTERN.fullmatch(tag) is None:
        raise ValueError(f"release tag {tag!r} must have the form vX.Y.Z")
    version = project_version(pyproject)
    if tag != f"v{version}":
        raise ValueError(
            f"release tag {tag!r} does not match project version {version!r}"
        )
    return version


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: check_release.py vX.Y.Z", file=sys.stderr)
        return 2
    try:
        version = validate_release_tag(args[0])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"release tag and project version agree: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
