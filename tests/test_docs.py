"""Public release documentation is complete and internally consistent."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def _version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        return tomllib.load(pyproject)["project"]["version"]


def test_readme_has_real_install_and_compatibility_details() -> None:
    readme = _read("README.md")
    assert "pip install inkpaper" in readme
    tag_url = f"https://github.com/ronedgecomb/inkpaper.git@v{_version()}"
    assert tag_url in readme
    retired_url_marker = chr(60) + "public-" + "repo-url" + chr(62)
    assert retired_url_marker not in readme
    assert "python_version" not in readme
    assert "Python 3.10 or newer" in readme
    assert "Gradio 6.20 through 6.x" in readme
    assert "uv run ruff check ." in readme
    assert "uv run ruff format --check ." in readme


def test_public_maintenance_files_exist_without_draft_markers() -> None:
    for name in ("CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "RELEASING.md"):
        text = _read(name)
        assert text.strip()
        for marker in ("T" + "BD", "TO" + "DO"):
            assert marker not in text


def test_contributing_documents_the_public_change_process() -> None:
    readme = _read("README.md")
    contributing = _read("CONTRIBUTING.md")
    assert "[CONTRIBUTING.md](CONTRIBUTING.md)" in readme
    for requirement in (
        "Python 3.14",
        "uv sync",
        "uv run ruff check .",
        "uv run ruff format --check .",
        "uv run pytest",
        "Gradio 6.20",
        "Gradio 7",
        "SECURITY.md",
        "manual visual",
        "maintainers",
    ):
        assert requirement in contributing


def test_security_and_release_routes_are_exact() -> None:
    security = _read("SECURITY.md")
    releasing = _read("RELEASING.md")
    assert "https://github.com/ronedgecomb/inkpaper/security/advisories/new" in security
    assert ".github/workflows/release.yml" in releasing
    assert "environment named `pypi`" in releasing
    assert "scripts/check_release.py" in releasing
    assert "scripts/smoke_install.py" in releasing
    assert "Yank" in releasing


def test_solo_release_approval_cannot_deadlock() -> None:
    releasing = _read("RELEASING.md")
    assert "leave self-review allowed" in releasing
    assert "genuinely independent reviewer" in releasing
    assert "prevent self-bypass where the account settings support it" not in releasing


def test_release_command_requires_a_manual_gate_summary() -> None:
    releasing = _read("RELEASING.md")
    prompt = (
        '$visualGateSummary = Read-Host "Summarize the completed manual visual gate"'
    )
    assert prompt in releasing
    guard = """if ([string]::IsNullOrWhiteSpace($visualGateSummary)) {
    throw "A manual visual-gate summary is required."
}"""
    assert guard in releasing
    assert "--notes $visualGateSummary --generate-notes" in releasing


def test_yank_guidance_matches_pypi_and_preserves_versions() -> None:
    releasing = _read("RELEASING.md")
    assert "select **Yank**" in releasing
    assert "select **Yank release**" not in releasing
    assert "Uploaded files and filenames cannot be overwritten or reused" in releasing
    assert "never reuse a published version" in releasing


def test_local_credentials_are_ignored() -> None:
    ignore = _read(".gitignore").splitlines()
    assert ".env" in ignore
    assert ".env.*" in ignore
    assert "!.env.example" in ignore
    assert ".pypirc" in ignore
    assert "*.pem" in ignore
    assert "*.key" in ignore


def test_release_guide_covers_both_shells() -> None:
    releasing = _read("RELEASING.md")
    assert "```powershell" in releasing
    assert "```bash" in releasing
