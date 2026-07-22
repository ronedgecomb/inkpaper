"""The companion CSS: sentinel rules and theme carriage."""

from inkpaper.theme import CSS, Inkpaper


def test_css_contains_sentinel_rules() -> None:
    assert "::selection" in CSS
    assert "#7288a7" in CSS  # slate
    assert "#111111" in CSS  # ink
    assert "300ms" in CSS  # exit timing
    assert "200ms" in CSS  # entrance timing
    assert ":focus-visible" in CSS


def test_theme_carries_the_css() -> None:
    assert Inkpaper().custom_css == CSS
    assert CSS.strip(), "CSS must not be empty"


def test_css_overrides_footer_link_hover() -> None:
    assert "footer :is(.show-api, .built-with, .settings, .record):hover:hover" in CSS
