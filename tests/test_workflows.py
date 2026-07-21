"""GitHub automation stays lean, immutable, and least-privileged."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CI = ROOT / ".github" / "workflows" / "ci.yml"
RELEASE = ROOT / ".github" / "workflows" / "release.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
SHA = re.compile(r"[0-9a-f]{40}")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ci_triggers_and_quality_commands() -> None:
    ci = _read(CI)
    assert "pull_request:" in ci
    assert "branches: [main]" in ci
    assert "workflow_call:" in ci
    assert "pull_request_target" not in ci
    assert "uv run --locked ruff check ." in ci
    assert "uv run --locked ruff format --check ." in ci
    assert "uv run --locked pytest -q" in ci
    assert "gradio==6.20.0" in ci
    assert "gradio>=6.20,<7" in ci


def test_release_is_top_level_oidc_publish_only() -> None:
    release = _read(RELEASE)
    assert "types: [published]" in release
    assert "uses: ./.github/workflows/ci.yml" in release
    assert "environment:" in release and "name: pypi" in release
    assert release.count("id-token: write") == 1
    assert "password:" not in release
    assert "uv build" not in release
    assert "pypa/gh-action-pypi-publish" in release
    assert "packages-dir: release-artifacts/dist/" in release


def test_every_external_action_is_pinned_to_a_commit() -> None:
    for path in (CI, RELEASE):
        for line in _read(path).splitlines():
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            target = stripped.removeprefix("uses:").strip().split()[0]
            if target.startswith("./"):
                continue
            action, separator, ref = target.rpartition("@")
            assert action and separator == "@", target
            assert SHA.fullmatch(ref), target


def test_dependabot_covers_uv_and_actions_weekly() -> None:
    dependabot = _read(DEPENDABOT)
    assert 'package-ecosystem: "uv"' in dependabot
    assert 'package-ecosystem: "github-actions"' in dependabot
    assert dependabot.count('interval: "weekly"') == 2
