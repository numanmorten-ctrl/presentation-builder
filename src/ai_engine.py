"""Future AI integration facade.

Currently delegates to the rule-based story builder. This module is intentionally
small so an OpenAI-backed implementation can later return the same Story JSON
contract without changing Streamlit or PowerPoint rendering code.
"""

from .story_builder import build_story

__all__ = ["build_story"]
