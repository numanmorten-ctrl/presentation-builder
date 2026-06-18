"""Shared file and Story JSON utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / ".gitkeep").touch(exist_ok=True)
    return OUTPUT_DIR


def story_to_pretty_json(story: dict[str, Any]) -> str:
    return json.dumps(story, ensure_ascii=False, indent=2)
