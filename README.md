# inkpaper

A Gradio theme matching [ronedgecomb.site](https://ronedgecomb.site):
ink surfaces, paper text, slate accents, mono type. Always dark.

## Usage

```python
import gradio as gr
import inkpaper

with gr.Blocks() as demo:
    ...

inkpaper.launch(demo)
```

`inkpaper.launch(demo, **kwargs)` forwards every keyword argument to
`Blocks.launch` and injects two overridable defaults: the theme and a
dark-mode pin.

For full manual control, the pieces are importable — note that in
Gradio 6 `theme=` belongs to `launch()`, not `gr.Blocks()`:

```python
demo.launch(theme=inkpaper.THEME)  # the theme carries its CSS with it
```

## Install

In a Space's `requirements.txt` (or any project):

```
inkpaper @ git+<public-repo-url>@v0.1.0
```

Requires Python >= 3.14 — configure your Space's runtime accordingly.

Once published to PyPI: `inkpaper==0.1.0`.

## Tokens

| Token       | Value     | Role                                  |
| ----------- | --------- | ------------------------------------- |
| ink         | `#111111` | background                            |
| ink-2       | `#1c1c1c` | raised surfaces (inputs, code)        |
| hairline    | `#333333` | borders, dividers                     |
| paper-faint | `#666666` | metadata, placeholders                |
| paper-mut   | `#8a8a8a` | chrome, secondary text                |
| paper       | `#eeeeee` | primary text                          |
| slate       | `#7288a7` | interactive accent — hover/focus only |

Type is mono-only: 16px body, 14px meta, 12px labels. Motion eases in
at 200ms and back out at 300ms.

## Development

```
uv sync          # install with dev dependencies
uv run pytest    # test suite
uv run python demo/app.py   # kitchen-sink demo
```

## License

MIT
