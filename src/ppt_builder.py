"""Backward-compatible wrapper around the Story JSON presentation engine."""

from pathlib import Path

from .content_salary import DEFAULT_DECK_STYLE, DEFAULT_PROMPT, DEFAULT_SLIDE_COUNT
from .ppt_engine import build_presentation_from_story
from .story_builder import build_story


def build_presentation(
    prompt: str = DEFAULT_PROMPT,
    deck_style: str = DEFAULT_DECK_STYLE,
    slide_count: int = DEFAULT_SLIDE_COUNT,
    include_notes: bool = True,
    output_path: Path | None = None,
) -> Path:
    """Build a presentation via Story JSON, preserving the previous public API."""
    story = build_story(prompt, deck_style, slide_count, include_notes)
    return build_presentation_from_story(story, output_path)
