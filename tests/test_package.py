"""Package-level surface tests."""

from importlib.metadata import version

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
