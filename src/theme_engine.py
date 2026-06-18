"""Knauf presentation theme tokens used by layout renderers."""

from dataclasses import dataclass

from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


@dataclass(frozen=True)
class Theme:
    red: RGBColor = RGBColor(198, 12, 48)
    dark_grey: RGBColor = RGBColor(54, 54, 54)
    mid_grey: RGBColor = RGBColor(115, 115, 115)
    light_grey: RGBColor = RGBColor(242, 242, 242)
    border_grey: RGBColor = RGBColor(210, 210, 210)
    white: RGBColor = RGBColor(255, 255, 255)
    black: RGBColor = RGBColor(20, 20, 20)
    font_headline: str = "Arial"
    font_body: str = "Arial"
    title_size = Pt(34)
    subtitle_size = Pt(18)
    body_size = Pt(13)
    small_size = Pt(10)
    card_radius = None
    margin = Inches(0.85)
    gutter = Inches(0.25)


KNAUF_THEME = Theme()
