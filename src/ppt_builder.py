"""PowerPoint generation service for the Streamlit app."""

from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from .content_salary import OUTPUT_FILENAME, build_salary_story
from .diagrams import add_step_arrow, add_timeline, add_venn
from .layouts import add_bullets, add_card, add_footer, add_section_label, add_title, blank_layout, set_wide
from .theme import BLACK, BODY_SIZE, DARK_GREY, FONT_BODY, FONT_HEADLINE, KNAUF_RED, LIGHT_GREY, MID_GREY, WHITE

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "Knauf.pptx"
OUTPUT_DIR = ROOT / "output"
OUTPUT_PATH = OUTPUT_DIR / OUTPUT_FILENAME


def _new_slide(prs, index: int, title: str | None = None, subtitle: str | None = None):
    """Create a blank slide from the uploaded template and apply common chrome."""
    slide = prs.slides.add_slide(blank_layout(prs))
    if title:
        add_title(slide, title, subtitle)
    add_footer(slide, index)
    return slide


def _add_notes(slide, notes: str):
    """Best-effort speaker note support.

    python-pptx does not expose a stable public API for notes slides. To keep the
    content available without relying on fragile private XML, notes are stored in
    the slide name metadata and as alternative text on a hidden off-canvas shape.
    """
    slide.name = notes[:250]
    box = slide.shapes.add_textbox(Inches(-5), Inches(-5), Inches(1), Inches(1))
    box.name = "Speaker notes"
    box.text_frame.text = notes


def _cover(prs, slide_no, data):
    slide = _new_slide(prs, slide_no)
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
    band.fill.solid(); band.fill.fore_color.rgb = KNAUF_RED; band.line.fill.background()
    label = slide.shapes.add_textbox(Inches(0.75), Inches(0.35), Inches(2.6), Inches(0.3))
    p = label.text_frame.paragraphs[0]; p.text = "KNAUF | EXECUTIVE DIALOGUE"; p.font.name = FONT_BODY; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = WHITE
    title = slide.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(9.8), Inches(1.0))
    p = title.text_frame.paragraphs[0]; p.text = data["title"]; p.font.name = FONT_HEADLINE; p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = BLACK
    sub = slide.shapes.add_textbox(Inches(0.9), Inches(3.02), Inches(8.6), Inches(0.42))
    p = sub.text_frame.paragraphs[0]; p.text = data["subtitle"]; p.font.name = FONT_BODY; p.font.size = Pt(20); p.font.color.rgb = MID_GREY
    add_card(slide, Inches(0.95), Inches(4.25), Inches(5.4), Inches(1.25), "Key message", data["key_message"], fill=LIGHT_GREY)
    add_card(slide, Inches(7.15), Inches(4.25), Inches(3.8), Inches(1.25), "Audience", data["audience"], fill=WHITE)
    return slide


def _comparison(prs, slide_no, data):
    slide = _new_slide(prs, slide_no, data["title"])
    add_card(slide, Inches(1.0), Inches(2.05), Inches(5.15), Inches(3.35), data["left_title"], "", fill=LIGHT_GREY)
    add_bullets(slide, data["left"], Inches(1.35), Inches(2.9), Inches(4.3), Inches(1.8))
    add_card(slide, Inches(7.2), Inches(2.05), Inches(5.15), Inches(3.35), data["right_title"], "", fill=WHITE)
    add_bullets(slide, data["right"], Inches(7.55), Inches(2.9), Inches(4.3), Inches(1.8))
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.25), Inches(3.25), Inches(0.82), Inches(0.55))
    arrow.fill.solid(); arrow.fill.fore_color.rgb = KNAUF_RED; arrow.line.fill.background()
    return slide


def _cards(prs, slide_no, data):
    slide = _new_slide(prs, slide_no, data["title"], data.get("subtitle"))
    for i, (heading, body) in enumerate(data["cards"]):
        x = Inches(0.95 + (i % 2) * 5.9)
        y = Inches(2.15 + (i // 2) * 1.72)
        add_card(slide, x, y, Inches(5.1), Inches(1.25), heading, body, fill=WHITE if i % 2 else LIGHT_GREY)
    return slide


def _results(prs, slide_no, data):
    slide = _new_slide(prs, slide_no, data["title"], data.get("subtitle"))
    for i, (big, label) in enumerate(data["metrics"]):
        x = Inches(0.95 + i * 3.05)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.55), Inches(2.45), Inches(2.05))
        card.fill.solid(); card.fill.fore_color.rgb = KNAUF_RED if i == 0 else WHITE
        card.line.color.rgb = KNAUF_RED
        tf = card.text_frame; tf.clear()
        p = tf.paragraphs[0]; p.text = big; p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_HEADLINE; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = WHITE if i == 0 else KNAUF_RED
        p2 = tf.add_paragraph(); p2.text = label; p2.alignment = PP_ALIGN.CENTER
        p2.font.name = FONT_BODY; p2.font.size = Pt(16); p2.font.color.rgb = WHITE if i == 0 else DARK_GREY
    add_section_label(slide, "Evidence examples to add before the meeting", Inches(1.0), Inches(5.25), Inches(5.0))
    add_bullets(slide, ["Specific projects", "Stakeholder feedback", "Delivery outcomes"], Inches(1.0), Inches(5.6), Inches(10.5), Inches(0.55))
    return slide


def _conclusion(prs, slide_no, data):
    slide = _new_slide(prs, slide_no, data["title"])
    msg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(11.1), Inches(1.35))
    msg.fill.solid(); msg.fill.fore_color.rgb = KNAUF_RED; msg.line.fill.background()
    p = msg.text_frame.paragraphs[0]; p.text = data["message"]; p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_HEADLINE; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = WHITE
    for i, ask in enumerate(data["asks"]):
        add_card(slide, Inches(1.0 + i * 3.75), Inches(4.25), Inches(3.25), Inches(1.15), f"0{i+1}", ask, fill=WHITE)
    return slide


def build_presentation(title: str, audience: str, key_message: str, output_path: Path | None = None) -> Path:
    """Build the salary/development deck and return the generated file path."""
    output_path = output_path or OUTPUT_PATH
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prs = Presentation(str(TEMPLATE_PATH)) if TEMPLATE_PATH.exists() else Presentation()
    set_wide(prs)
    story = build_salary_story(title, audience, key_message)
    builders = {
        "cover": _cover,
        "comparison": _comparison,
        "cards": _cards,
        "results": _results,
        "conclusion": _conclusion,
    }
    for idx, data in enumerate(story, start=1):
        if data["kind"] == "timeline":
            slide = _new_slide(prs, idx, data["title"], data.get("subtitle")); add_timeline(slide, data["items"])
        elif data["kind"] == "venn":
            slide = _new_slide(prs, idx, data["title"], data.get("subtitle")); add_venn(slide, data["circles"], data["center"])
        elif data["kind"] == "potential":
            slide = _new_slide(prs, idx, data["title"], data.get("subtitle")); add_step_arrow(slide, data["steps"])
        else:
            slide = builders[data["kind"]](prs, idx, data)
        _add_notes(slide, data.get("notes", ""))
    prs.save(output_path)
    return output_path
