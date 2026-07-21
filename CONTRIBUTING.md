# Contributing

Inkpaper requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). Fork and clone the repository, then prepare the locked development environment:

```bash
uv sync
```

Keep pull requests focused on one change, include tests for behavior changes, and avoid unrelated formatting or refactors. Before opening a pull request, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Compatibility covers Gradio 6.20 through 6.x. Changes that add Gradio 7 support require an explicit compatibility review. For UI, CSS, demo, or theme-token changes, complete the manual visual review documented in [RELEASING.md](RELEASING.md) and summarize what you checked in the pull request.

Do not report vulnerabilities in a public issue; follow [SECURITY.md](SECURITY.md). Only project maintainers may create release tags, GitHub releases, or PyPI publications.
