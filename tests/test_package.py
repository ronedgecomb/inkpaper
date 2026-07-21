"""Package-level surface tests."""

from importlib.metadata import version
from typing import Any, get_type_hints

import gradio as gr

import inkpaper
from inkpaper.theme import Inkpaper


def test_version_matches_installed_distribution() -> None:
    assert inkpaper.__version__ == version("inkpaper")


def test_public_surface() -> None:
    assert isinstance(inkpaper.THEME, Inkpaper)
    assert inkpaper.Inkpaper is Inkpaper
    assert isinstance(inkpaper.CSS, str) and inkpaper.CSS.strip()
    assert isinstance(inkpaper.DARK_MODE_JS, str)
    assert callable(inkpaper.launch)


def test_launch_has_practical_public_annotations() -> None:
    hints = get_type_hints(inkpaper.launch)
    assert hints == {
        "blocks": gr.Blocks,
        "kwargs": Any,
        "return": tuple[Any, str, str],
    }


def test_independent_theme_instances_do_not_alias_singleton() -> None:
    assert Inkpaper() is not inkpaper.THEME
