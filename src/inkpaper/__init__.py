"""Inkpaper: a Gradio theme matching ronedgecomb.site.

Usage::

    import gradio as gr
    import inkpaper

    with gr.Blocks() as demo:
        ...

    inkpaper.launch(demo)

``launch()`` is the recommended path; ``THEME`` and ``CSS`` remain
importable for apps that need to call ``Blocks.launch`` themselves.
Note that in Gradio 6, ``theme=`` and ``css=`` are ``launch()``
parameters, not ``gr.Blocks()`` parameters.
"""

from importlib.metadata import PackageNotFoundError, version

from inkpaper.theme import CSS, Inkpaper

try:
    __version__ = version("inkpaper")
except PackageNotFoundError:  # source tree without an installed distribution
    __version__ = "0.0.0"

THEME = Inkpaper()

# Pin the app to dark mode. Gradio reads the __theme URL parameter at
# startup; adding the body class covers the current load. The theme sets
# identical light and dark variables, so this only affects the handful
# of Gradio styles keyed off the mode class rather than theme variables.
DARK_MODE_JS = """
() => {
  const url = new URL(window.location.href);
  if (url.searchParams.get('__theme') !== 'dark') {
    url.searchParams.set('__theme', 'dark');
    window.location.replace(url.href);
  }
  document.body.classList.add('dark');
}
"""


def launch(blocks, **kwargs):
    """Launch ``blocks`` with the Inkpaper theme applied.

    Injects two defaults, each overridable by passing the kwarg
    yourself: ``theme=THEME`` and ``js=DARK_MODE_JS`` (forces dark
    mode). All other keyword arguments pass straight through to
    ``Blocks.launch``. A caller-supplied ``css`` loads after the
    theme's own CSS, so it wins the cascade.
    """
    kwargs.setdefault("theme", THEME)
    kwargs.setdefault("js", DARK_MODE_JS)
    return blocks.launch(**kwargs)


__all__ = [
    "CSS",
    "DARK_MODE_JS",
    "Inkpaper",
    "THEME",
    "__version__",
    "launch",
]
