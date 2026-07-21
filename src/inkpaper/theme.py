"""The Inkpaper theme: ronedgecomb.site's identity as a Gradio theme.

Anchor values are the site's design tokens. Gradio requires full
c50-c950 ramps, so stops between anchors are interpolated; every
interpolated stop is marked as such and is not a site token.
"""

from __future__ import annotations

import gradio.themes as themes
from gradio.themes.utils import colors, sizes

NEUTRAL = colors.Color(
    name="ink_neutral",
    c50="#eeeeee",  # paper
    c100="#d0d0d0",  # interpolated
    c200="#adadad",  # interpolated
    c300="#8a8a8a",  # paper-mut
    c400="#787878",  # interpolated
    c500="#666666",  # paper-faint
    c600="#4d4d4d",  # interpolated
    c700="#333333",  # hairline
    c800="#272727",  # interpolated
    c900="#1c1c1c",  # ink-2
    c950="#111111",  # ink
)

SLATE = colors.Color(
    name="ink_slate",
    c50="#eef1f6",  # interpolated
    c100="#dde4ec",  # interpolated
    c200="#c2cdda",  # interpolated
    c300="#a7b6c9",  # interpolated
    c400="#8c9fb8",  # interpolated
    c500="#7288a7",  # slate
    c600="#5f7492",  # interpolated
    c700="#4e6079",  # interpolated
    c800="#3e4c60",  # interpolated
    c900="#2e3947",  # interpolated
    c950="#1f262f",  # interpolated
)

MONO_STACK = (
    "ui-monospace",
    "SF Mono",
    "Cascadia Mono",
    "JetBrains Mono",
    "Menlo",
    "Consolas",
    "monospace",
)

TEXT_SIZES = sizes.Size(
    name="text_inkpaper",
    xxs="9px",
    xs="10px",
    sm="12px",  # label size
    md="14px",  # meta size
    lg="16px",  # body size
    xl="18px",
    xxl="22px",
)


class Inkpaper(themes.Base):
    """Always-dark Gradio theme: ink surfaces, paper text, slate accents."""

    def __init__(self) -> None:
        super().__init__(
            primary_hue=SLATE,
            secondary_hue=SLATE,
            neutral_hue=NEUTRAL,
            text_size=TEXT_SIZES,
            radius_size=sizes.radius_none,
            font=MONO_STACK,
            font_mono=MONO_STACK,
        )
        self.name = "inkpaper"
