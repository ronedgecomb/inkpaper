# AGENTS.md

Guidance for coding agents working in this repository.

## Workflow

- Package management uses [uv](https://docs.astral.sh/uv/) with a locked environment on Python 3.14. Prepare it with `uv sync` and run everything through `uv run`.
- Before opening a pull request, all three gates must pass:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

- Keep pull requests focused on one change, and record user-visible changes under `## [Unreleased]` in CHANGELOG.md.

## Constraints

- Compatibility covers Python 3.10 or newer and Gradio 6.20 through 6.x. Do not raise the `gradio<7` cap without an explicit review of the theme tokens and the DOM-level CSS workarounds against the new major version.
- The theme is always-dark: any theme-variable change must preserve the invariant that every `*_dark` variable mirrors its light twin (see `_mirror_light_to_dark` in `src/inkpaper/theme.py`).
- UI, CSS, demo, or theme-token changes require the manual visual review documented in RELEASING.md; summarize what was checked in the pull request.
- Releases (tags, GitHub Releases, PyPI publications) are maintainer-only; see RELEASING.md.
- `docs/` is intentionally untracked internal design material (see `.gitignore`); never commit or publish it.
