"""PowerPoint engine: orchestrates Story JSON rendering into a .pptx file."""

from __future__ import annotations

from pathlib import Path

from .content_salary import OUTPUT_FILENAME
from .layout_engine import render_slide
from .schemas import validate_story
from .template_manager import TemplateManager
from .theme_engine import KNAUF_THEME
from .utils import OUTPUT_DIR, ensure_output_dir

OUTPUT_PATH = OUTPUT_DIR / OUTPUT_FILENAME


def _add_notes(slide, notes: str) -> None:
    if not notes:
        return
    # python-pptx has no stable public notes API; keep notes in metadata and a
    # hidden off-canvas text box so they stay packaged with the deck.
    slide.name = notes[:250]
    box = slide.shapes.add_textbox(-4572000, -4572000, 914400, 914400)
    box.name = "Speaker notes"
    box.text_frame.text = notes


def build_presentation_from_story(story: dict, output_path: Path | None = None) -> Path:
    """Render a validated Story JSON object to a PowerPoint file."""
    result = validate_story(story)
    if not result.valid:
        raise ValueError("Invalid Story JSON: " + "; ".join(result.errors))

    output_path = output_path or OUTPUT_PATH
    ensure_output_dir()
    manager = TemplateManager()
    prs = manager.load()
    safe_area = manager.get_safe_area()

    for idx, slide_json in enumerate(story["slides"], start=1):
        slide = prs.slides.add_slide(manager.best_layout(prs, slide_json["type"]))
        render_slide(slide, slide_json, KNAUF_THEME, safe_area, idx)
        if story["meta"].get("include_speaker_notes", True):
            _add_notes(slide, slide_json.get("speaker_notes", ""))

    prs.save(output_path)
    return output_path
