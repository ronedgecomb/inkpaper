"""Package-level surface tests."""

import inkpaper
from inkpaper.theme import Inkpaper


def test_version() -> None:
    assert inkpaper.__version__ == "0.1.0"


def test_public_surface() -> None:
    assert isinstance(inkpaper.THEME, Inkpaper)
    assert inkpaper.Inkpaper is Inkpaper
    assert isinstance(inkpaper.CSS, str) and inkpaper.CSS.strip()
    assert isinstance(inkpaper.DARK_MODE_JS, str)
    assert callable(inkpaper.launch)
