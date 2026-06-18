"""Typed Story JSON schemas and validation helpers for the presentation engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

SlideType = Literal[
    "cover",
    "executive_summary",
    "timeline",
    "comparison",
    "value_cards",
    "house_model",
    "case_list",
    "hub_and_spokes",
    "conclusion",
]


class StoryMeta(TypedDict):
    title: str
    subtitle: str
    audience: str
    style: str
    language: str
    include_speaker_notes: bool


class SlideStory(TypedDict, total=False):
    type: SlideType
    title: str
    subtitle: str
    speaker_notes: str
    cards: list[dict[str, str]]
    items: list[dict[str, str]]
    left_title: str
    right_title: str
    left_items: list[str]
    right_items: list[str]
    foundation: str
    core: str
    upper: str
    roof: str
    side_note: str
    cases: list[dict[str, str]]
    center: str
    statements: list[str]
    final_message: str


class DeckStory(TypedDict):
    meta: StoryMeta
    slides: list[SlideStory]


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


REQUIRED_BY_TYPE: dict[str, set[str]] = {
    "cover": {"type", "title", "subtitle"},
    "executive_summary": {"type", "title", "cards"},
    "timeline": {"type", "title", "items"},
    "comparison": {"type", "title", "left_title", "right_title", "left_items", "right_items"},
    "value_cards": {"type", "title", "cards"},
    "house_model": {"type", "title", "foundation", "core", "upper", "roof"},
    "case_list": {"type", "title", "cases"},
    "hub_and_spokes": {"type", "title", "center", "items"},
    "conclusion": {"type", "title", "statements", "final_message"},
}


def validate_story(story: dict[str, Any]) -> ValidationResult:
    """Validate the minimum shape required by the layout and PowerPoint engines."""
    errors: list[str] = []
    if not isinstance(story, dict):
        return ValidationResult(False, ["Story must be a dictionary."])
    meta = story.get("meta")
    slides = story.get("slides")
    if not isinstance(meta, dict):
        errors.append("Story must contain a meta object.")
    else:
        for key in ("title", "subtitle", "audience", "style", "language", "include_speaker_notes"):
            if key not in meta:
                errors.append(f"meta.{key} is required.")
    if not isinstance(slides, list) or not slides:
        errors.append("Story must contain a non-empty slides list.")
    elif isinstance(slides, list):
        for index, slide in enumerate(slides, start=1):
            if not isinstance(slide, dict):
                errors.append(f"slides[{index}] must be an object.")
                continue
            slide_type = slide.get("type")
            if slide_type not in REQUIRED_BY_TYPE:
                errors.append(f"slides[{index}].type is unsupported: {slide_type!r}.")
                continue
            for key in REQUIRED_BY_TYPE[slide_type] - slide.keys():
                errors.append(f"slides[{index}] ({slide_type}) missing required field: {key}.")
    return ValidationResult(not errors, errors)
