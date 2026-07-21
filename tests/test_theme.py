"""Theme construction, token anchoring, and the always-dark invariant."""

from inkpaper.theme import MONO_STACK, NEUTRAL, SLATE, Inkpaper


def test_neutral_ramp_anchors_are_site_tokens() -> None:
    assert NEUTRAL.c950 == "#111111"  # ink
    assert NEUTRAL.c900 == "#1c1c1c"  # ink-2
    assert NEUTRAL.c700 == "#333333"  # hairline
    assert NEUTRAL.c500 == "#666666"  # paper-faint
    assert NEUTRAL.c300 == "#8a8a8a"  # paper-mut
    assert NEUTRAL.c50 == "#eeeeee"  # paper


def test_slate_ramp_anchor_is_site_token() -> None:
    assert SLATE.c500 == "#7288a7"  # slate


def test_theme_constructs_with_mono_fonts_and_no_radius() -> None:
    theme = Inkpaper()
    assert theme.name == "inkpaper"
    # Both font stacks are the same mono stack. In Gradio 6.20 the
    # theme's `font` attribute is the joined CSS font-family string.
    for face in MONO_STACK:
        assert face in theme.font
    assert theme.font == theme.font_mono
    assert theme.radius_lg == "0px"
    # Site type scale: 16px body, 14px meta, 12px label.
    assert theme.text_lg == "16px"
    assert theme.text_md == "14px"
    assert theme.text_sm == "12px"
