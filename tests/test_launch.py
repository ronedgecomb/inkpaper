"""launch() injects Inkpaper defaults and forwards everything else."""

import inkpaper


class FakeBlocks:
    """Records launch kwargs instead of starting a server."""

    def __init__(self) -> None:
        self.kwargs: dict | None = None

    def launch(self, **kwargs):
        self.kwargs = kwargs
        return "launched"


def test_launch_injects_theme_and_dark_js() -> None:
    fake = FakeBlocks()
    result = inkpaper.launch(fake)
    assert result == "launched"
    assert fake.kwargs["theme"] is inkpaper.THEME
    assert fake.kwargs["js"] == inkpaper.DARK_MODE_JS
    assert "footer_links" not in fake.kwargs
    assert "css" not in fake.kwargs  # the theme itself carries the CSS


def test_launch_forwards_caller_kwargs() -> None:
    fake = FakeBlocks()
    inkpaper.launch(fake, server_port=7861, css="h1 { color: red; }")
    assert fake.kwargs["server_port"] == 7861
    assert fake.kwargs["css"] == "h1 { color: red; }"


def test_caller_overrides_win() -> None:
    fake = FakeBlocks()
    other_theme = object()
    inkpaper.launch(fake, theme=other_theme, js="() => {}", footer_links=[])
    assert fake.kwargs["theme"] is other_theme
    assert fake.kwargs["js"] == "() => {}"
    assert fake.kwargs["footer_links"] == []
