"""Simple executive diagrams used by the deck builder."""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from .layouts import add_card
from .theme import BODY_SIZE, DARK_GREY, FONT_BODY, FONT_HEADLINE, KNAUF_RED, LIGHT_GREY, MID_GREY, WHITE


def add_timeline(slide, items):
    y = Inches(3.25)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.25), y, Inches(10.85), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = KNAUF_RED
    line.line.fill.background()
    gap = 10.3 / (len(items) - 1)
    for idx, (year, heading, body) in enumerate(items):
        x = Inches(1.1 + idx * gap)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y - Inches(0.16), Inches(0.36), Inches(0.36))
        dot.fill.solid(); dot.fill.fore_color.rgb = KNAUF_RED; dot.line.color.rgb = WHITE
        box_y = Inches(2.0 if idx % 2 == 0 else 3.75)
        add_card(slide, x - Inches(0.55), box_y, Inches(2.05), Inches(1.08), year, f"{heading}\n{body}", fill=WHITE)


def add_venn(slide, labels, center):
    positions = [(3.0, 2.6), (5.0, 2.6), (4.0, 3.75)]
    colors = [KNAUF_RED, MID_GREY, DARK_GREY]
    for (x, y), label, color in zip(positions, labels, colors):
        c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(3.0), Inches(2.0))
        c.fill.solid(); c.fill.fore_color.rgb = color; c.fill.transparency = 28
        c.line.color.rgb = WHITE
        tf = c.text_frame; tf.clear()
        p = tf.paragraphs[0]; p.text = label; p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_BODY; p.font.size = BODY_SIZE; p.font.bold = True; p.font.color.rgb = WHITE
    mid = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.05), Inches(3.55), Inches(2.2), Inches(0.72))
    mid.fill.solid(); mid.fill.fore_color.rgb = WHITE; mid.line.color.rgb = KNAUF_RED
    p = mid.text_frame.paragraphs[0]; p.text = center; p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_HEADLINE; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = KNAUF_RED


def add_step_arrow(slide, steps):
    for i, step in enumerate(steps):
        x = Inches(1.0 + i * 3.9)
        shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, Inches(3.1), Inches(3.25), Inches(1.05))
        shp.fill.solid(); shp.fill.fore_color.rgb = KNAUF_RED if i == 0 else LIGHT_GREY
        shp.line.color.rgb = WHITE
        p = shp.text_frame.paragraphs[0]; p.text = step; p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_HEADLINE; p.font.size = Pt(16); p.font.bold = True
        p.font.color.rgb = WHITE if i == 0 else DARK_GREY
