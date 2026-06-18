"""Theme constants for Knauf-inspired executive presentations."""

from pptx.dml.color import RGBColor
from pptx.util import Pt


# Knauf-inspired corporate palette. The template remains the true source of
# branding; these colors give generated shapes a consistent red/white/grey look.
KNAUF_RED = RGBColor(198, 12, 48)
DARK_GREY = RGBColor(54, 54, 54)
MID_GREY = RGBColor(115, 115, 115)
LIGHT_GREY = RGBColor(242, 242, 242)
BORDER_GREY = RGBColor(210, 210, 210)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(20, 20, 20)

FONT_HEADLINE = "Arial"
FONT_BODY = "Arial"

TITLE_SIZE = Pt(34)
SUBTITLE_SIZE = Pt(18)
SECTION_SIZE = Pt(24)
BODY_SIZE = Pt(13)
SMALL_SIZE = Pt(10)

SLIDE_WIDE_WIDTH = 13.333
SLIDE_WIDE_HEIGHT = 7.5
