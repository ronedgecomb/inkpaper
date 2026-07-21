"""Release tags must identify the exact version being built."""

from pathlib import Path

import pytest

from scripts.check_release import project_version, validate_release_tag


def _write_pyproject(path: Path, version: str) -> Path:
    path.write_text(f'[project]\nname = "inkpaper"\nversion = "{version}"\n')
    return path


def test_current_project_accepts_its_matching_tag() -> None:
    version = project_version()
    assert validate_release_tag(f"v{version}") == version


def test_release_tag_requires_v_prefix(tmp_path: Path) -> None:
    pyproject = _write_pyproject(tmp_path / "pyproject.toml", "1.2.3")
    with pytest.raises(ValueError, match="must have the form"):
        validate_release_tag("1.2.3", pyproject)


def test_release_tag_must_match_project_version(tmp_path: Path) -> None:
    pyproject = _write_pyproject(tmp_path / "pyproject.toml", "1.2.3")
    with pytest.raises(ValueError, match="does not match"):
        validate_release_tag("v1.2.4", pyproject)
