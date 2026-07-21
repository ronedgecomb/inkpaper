"""Verify the essential behavior of an installed inkpaper distribution."""

from __future__ import annotations

import sys
from importlib.metadata import version
from importlib.resources import files

import inkpaper


def verify(expected_version: str) -> None:
    installed_version = version("inkpaper")
    if installed_version != expected_version:
        raise RuntimeError(
            f"installed version {installed_version!r} != expected {expected_version!r}"
        )
    if inkpaper.__version__ != expected_version:
        raise RuntimeError(
            f"runtime version {inkpaper.__version__!r} != expected {expected_version!r}"
        )
    if not inkpaper.CSS.strip():
        raise RuntimeError("bundled CSS is empty")
    if not (files("inkpaper") / "py.typed").is_file():
        raise RuntimeError("py.typed marker is missing from the installed distribution")
    theme = inkpaper.Inkpaper()
    if theme.custom_css != inkpaper.CSS:
        raise RuntimeError("theme did not load the bundled CSS")
    required = {
        "CSS",
        "DARK_MODE_JS",
        "Inkpaper",
        "THEME",
        "__version__",
        "launch",
    }
    if set(inkpaper.__all__) != required:
        raise RuntimeError(f"unexpected public exports: {sorted(inkpaper.__all__)!r}")
    print(f"verified inkpaper {expected_version} with bundled CSS")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: smoke_install.py X.Y.Z", file=sys.stderr)
        return 2
    verify(args[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
