"""Inkpaper: a Gradio theme matching ronedgecomb.site."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("inkpaper")
except PackageNotFoundError:  # source tree without an installed distribution
    __version__ = "0.0.0"
