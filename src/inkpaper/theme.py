"""The Inkpaper theme. Always-dark surfaces, monospace type, slate accents.

Anchor values are the theme's core palette. Gradio requires full
c50-c950 ramps, so stops between anchors are interpolated; every
interpolated stop is marked as such and is not an anchor value.
"""

from __future__ import annotations

from importlib.resources import files

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

CSS = (files("inkpaper") / "inkpaper.css").read_text(encoding="utf-8")


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
        self.set(
            # Body and surfaces: flat ink, paper text.
            body_background_fill="*neutral_950",
            body_text_color="*neutral_50",
            body_text_color_subdued="*neutral_300",
            background_fill_primary="*neutral_950",
            background_fill_secondary="*neutral_900",
            border_color_primary="*neutral_700",
            border_color_accent="*primary_500",
            border_color_accent_subdued="*primary_700",
            color_accent="*primary_500",
            color_accent_soft="*primary_950",
            # Blocks and panels: flat, hairline-bordered, unshadowed.
            block_background_fill="*neutral_950",
            block_border_color="*neutral_700",
            block_label_background_fill="*neutral_950",
            block_label_text_color="*neutral_300",
            block_title_text_color="*neutral_50",
            block_info_text_color="*neutral_500",
            block_shadow="none",
            panel_background_fill="*neutral_950",
            panel_border_color="*neutral_700",
            shadow_drop="none",
            shadow_drop_lg="none",
            shadow_inset="none",
            accordion_text_color="*neutral_50",
            # Buttons: outlined and flat. Primary announces itself in
            # slate; secondary rests as chrome; cancel rests as paper-mut.
            # All converge on slate at hover, because slate means interactive.
            button_border_width="1px",
            button_primary_background_fill="transparent",
            button_primary_background_fill_hover="*primary_500",
            button_primary_border_color="*primary_500",
            button_primary_text_color="*primary_500",
            button_primary_text_color_hover="*neutral_950",
            button_secondary_background_fill="transparent",
            button_secondary_background_fill_hover="transparent",
            button_secondary_border_color="*neutral_700",
            button_secondary_border_color_hover="*primary_500",
            button_secondary_text_color="*neutral_300",
            button_secondary_text_color_hover="*primary_500",
            button_cancel_background_fill="transparent",
            button_cancel_background_fill_hover="transparent",
            button_cancel_border_color="*neutral_300",
            button_cancel_border_color_hover="*primary_500",
            button_cancel_text_color="*neutral_300",
            button_cancel_text_color_hover="*primary_500",
            # Inputs: raised ink-2 wells, slate only on interaction.
            input_background_fill="*neutral_900",
            input_background_fill_focus="*neutral_900",
            input_background_fill_hover="*neutral_900",
            input_border_color="*neutral_700",
            input_border_color_hover="*primary_500",
            input_border_color_focus="*primary_500",
            input_placeholder_color="*neutral_500",
            input_shadow="none",
            input_shadow_focus="none",
            # Checkboxes and radios.
            checkbox_background_color="*neutral_900",
            checkbox_background_color_hover="*neutral_900",
            checkbox_background_color_focus="*neutral_900",
            checkbox_background_color_selected="*primary_500",
            checkbox_border_color="*neutral_700",
            checkbox_border_color_hover="*primary_500",
            checkbox_border_color_focus="*primary_500",
            checkbox_border_color_selected="*primary_500",
            checkbox_label_background_fill="transparent",
            checkbox_label_background_fill_hover="transparent",
            checkbox_label_background_fill_selected="transparent",
            checkbox_label_border_color="*neutral_700",
            checkbox_label_border_color_hover="*primary_500",
            checkbox_label_border_color_selected="*primary_500",
            checkbox_label_text_color="*neutral_300",
            checkbox_label_text_color_selected="*neutral_50",
            # Sliders, loaders, links, misc accents.
            slider_color="*primary_500",
            loader_color="*primary_500",
            link_text_color="*neutral_50",
            link_text_color_hover="*primary_500",
            link_text_color_active="*primary_500",
            link_text_color_visited="*neutral_50",
            stat_background_fill="*primary_500",
            # Tables and code.
            table_border_color="*neutral_700",
            table_even_background_fill="*neutral_950",
            table_odd_background_fill="*neutral_900",
            table_row_focus="*primary_950",
            table_text_color="*neutral_50",
            code_background_fill="*neutral_900",
            # Errors: the palette has no red; errors speak through
            # contrast (paper text, paper-mut border on ink-2).
            error_background_fill="*neutral_900",
            error_border_color="*neutral_300",
            error_text_color="*neutral_50",
            error_icon_color="*neutral_300",
            # Type roles: 16px body, 14px meta, 12px labels, mono weights.
            body_text_size="*text_lg",
            block_title_text_size="*text_md",
            block_label_text_size="*text_sm",
            block_info_text_size="*text_sm",
            section_header_text_size="*text_md",
            block_title_text_weight="400",
            prose_header_text_weight="600",
        )
        _mirror_light_to_dark(self)
        self.custom_css = CSS


def _mirror_light_to_dark(theme: themes.Base) -> None:
    """Give every ``*_dark`` variable its light counterpart's value.

    The site has exactly one look, so the theme must render identically
    whichever mode Gradio believes it is in.
    """
    for name in list(vars(theme)):
        if name.endswith("_dark"):
            light = name.removesuffix("_dark")
            if hasattr(theme, light):
                setattr(theme, name, getattr(theme, light))
