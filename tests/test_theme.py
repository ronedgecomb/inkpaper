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


def test_role_mapping_follows_site_rules() -> None:
    theme = Inkpaper()
    # Surfaces are flat ink; chrome is hairline.
    assert theme.body_background_fill == "*neutral_950"
    assert theme.body_text_color == "*neutral_50"
    assert theme.block_background_fill == "*neutral_950"
    assert theme.block_border_color == "*neutral_700"
    assert theme.block_shadow == "none"
    # Slate marks interactive elements.
    assert theme.slider_color == "*primary_500"
    assert theme.loader_color == "*primary_500"
    assert theme.input_border_color_focus == "*primary_500"
    # Stop/cancel: neutral paper-mut border fading to slate, no invented red.
    assert theme.button_cancel_border_color == "*neutral_300"
    assert theme.button_cancel_border_color_hover == "*primary_500"
    assert theme.button_cancel_text_color == "*neutral_300"


def test_every_dark_variable_mirrors_its_light_twin() -> None:
    theme = Inkpaper()
    pairs = [
        (name, name.removesuffix("_dark"))
        for name in vars(theme)
        if name.endswith("_dark")
    ]
    assert len(pairs) > 50, "expected Gradio to expose many dark variables"
    mismatched = [
        dark
        for dark, light in pairs
        if hasattr(theme, light) and getattr(theme, dark) != getattr(theme, light)
    ]
    assert mismatched == []
