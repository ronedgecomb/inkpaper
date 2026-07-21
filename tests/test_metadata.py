"""Release-facing project metadata and compatibility policy."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _project() -> dict:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        return tomllib.load(pyproject)["project"]


def test_declared_runtime_compatibility() -> None:
    project = _project()
    assert project["requires-python"] == ">=3.14"
    assert project["dependencies"] == ["gradio>=6.20,<7"]


def test_pypi_identity_and_discovery_metadata() -> None:
    project = _project()
    assert project["authors"] == [{"name": "Ron Edgecomb"}]
    assert project["keywords"] == ["gradio", "theme", "dark-theme", "monospace"]
    assert project["license"] == "MIT"
    assert not any(value.startswith("License ::") for value in project["classifiers"])
    assert {
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    } <= set(project["classifiers"])


def test_canonical_project_urls() -> None:
    assert _project()["urls"] == {
        "Homepage": "https://github.com/ronedgecomb/inkpaper",
        "Repository": "https://github.com/ronedgecomb/inkpaper",
        "Issues": "https://github.com/ronedgecomb/inkpaper/issues",
        "Changelog": "https://github.com/ronedgecomb/inkpaper/blob/main/CHANGELOG.md",
    }


def test_distribution_validation_tools_are_locked_dev_dependencies() -> None:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        dev = tomllib.load(pyproject)["dependency-groups"]["dev"]
    assert "twine>=6,<7" in dev
    assert "check-wheel-contents>=0.6,<1" in dev
