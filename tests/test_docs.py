"""Public release documentation is complete and internally consistent."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_readme_has_real_install_and_compatibility_details() -> None:
    readme = _read("README.md")
    assert "pip install inkpaper" in readme
    assert "https://github.com/ronedgecomb/inkpaper.git@v0.1.0" in readme
    retired_url_marker = chr(60) + "public-repo-url" + chr(62)
    assert retired_url_marker not in readme
    assert 'python_version: "3.14"' in readme
    assert "Python 3.14 or newer" in readme
    assert "Gradio 6.20 through 6.x" in readme
    assert "uv run ruff check ." in readme
    assert "uv run ruff format --check ." in readme


def test_public_maintenance_files_exist_without_draft_markers() -> None:
    for name in ("CHANGELOG.md", "SECURITY.md", "RELEASING.md"):
        text = _read(name)
        assert text.strip()
        for marker in ("T" + "BD", "TO" + "DO"):
            assert marker not in text


def test_security_and_release_routes_are_exact() -> None:
    security = _read("SECURITY.md")
    releasing = _read("RELEASING.md")
    assert "https://github.com/ronedgecomb/inkpaper/security/advisories/new" in security
    assert ".github/workflows/release.yml" in releasing
    assert "environment named `pypi`" in releasing
    assert "scripts/check_release.py" in releasing
    assert "scripts/smoke_install.py" in releasing
    assert "Yank" in releasing


def test_local_credentials_are_ignored() -> None:
    ignore = _read(".gitignore").splitlines()
    assert ".env" in ignore
    assert ".env.*" in ignore
    assert "!.env.example" in ignore
    assert ".pypirc" in ignore
    assert "*.pem" in ignore
    assert "*.key" in ignore
