# inkpaper

[![CI](https://github.com/ronedgecomb/inkpaper/actions/workflows/ci.yml/badge.svg)](https://github.com/ronedgecomb/inkpaper/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/inkpaper)](https://pypi.org/project/inkpaper/)
[![Python](https://img.shields.io/badge/python-3.10%2B-7288a7)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-7288a7)](LICENSE)

An always-dark Gradio theme with monospace type, ink-black surfaces, paper-white text, and slate accents.

![The Inkpaper demo app: the Inputs tab of a dark Gradio page with monospace text and slate accents](https://raw.githubusercontent.com/ronedgecomb/inkpaper/main/.github/demo.png)

## Install

```bash
pip install inkpaper
```

Or pin a GitHub release tag:

```text
inkpaper @ git+https://github.com/ronedgecomb/inkpaper.git@v0.1.1
```

For local development, clone this repository and run `uv sync`.

## Compatibility

Inkpaper supports Python 3.10 or newer and Gradio 6.20 through 6.x. The dependency is capped below the next major version: when Gradio 7 arrives, the theme tokens and DOM-level CSS workarounds must be reviewed against it before the cap is lifted.

## Usage

```python
import gradio as gr
import inkpaper

with gr.Blocks() as demo:
    gr.Markdown("# Inkpaper")

inkpaper.launch(demo)
```

`inkpaper.launch(demo, **kwargs)` forwards keyword arguments to `Blocks.launch` and supplies two overridable defaults: `theme=inkpaper.THEME` and the dark-mode JavaScript.

```python
inkpaper.launch(
    demo,
    server_port=7861,
    footer_links=[],
    css=".gradio-container { max-width: 72rem; }",
)
```

For direct control, pass the ready-made theme to Gradio:

```python
demo.launch(theme=inkpaper.THEME)
```

`THEME` is shared. Create an independent instance before applying app-specific changes; set both normal and dark values to preserve the always-dark invariant:

```python
theme = inkpaper.Inkpaper()
theme.set(
    button_primary_border_color="#eeeeee",
    button_primary_border_color_dark="#eeeeee",
)
demo.launch(theme=theme)
```

The public API is `Inkpaper`, `THEME`, `CSS`, `DARK_MODE_JS`, `launch`, and `__version__`.

## Tokens

| Token | Value | Role |
| --- | --- | --- |
| ink | `#111111` | background |
| ink-2 | `#1c1c1c` | raised surfaces |
| hairline | `#333333` | borders and dividers |
| paper-faint | `#666666` | metadata and empty-field hints |
| paper-mut | `#8a8a8a` | chrome and secondary text |
| paper | `#eeeeee` | primary text |
| slate | `#7288a7` | hover, focus, and interaction |

Type is mono-only: 16px body, 14px metadata, and 12px labels. Color transitions enter in 200ms and leave in 300ms.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run ruff check --fix .
uv run ruff format .
uv run python demo/app.py
```

Contribution setup and review expectations are in [CONTRIBUTING.md](CONTRIBUTING.md). Release preparation, including the manual visual gate and external Trusted Publishing setup, is documented in [RELEASING.md](RELEASING.md). Changes are recorded in [CHANGELOG.md](CHANGELOG.md), and security reports follow [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
