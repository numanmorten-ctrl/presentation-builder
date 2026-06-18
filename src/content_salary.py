"""Default copy, options and trigger terms for the salary/development use case."""

DEFAULT_DECK_STYLE = "Executive / McKinsey-style"
DEFAULT_SLIDE_COUNT = 9
DEFAULT_PROMPT = """Morten Numan salary/development conversation.

Create an executive deck for a constructive dialogue about how Morten's role has developed, how his interdisciplinary profile creates value for Knauf, and why role, title and salary should be reviewed."""
OUTPUT_FILENAME = "morten_salary_deck_engine_v1.pptx"

DECK_STYLES = [
    "Executive / McKinsey-style",
    "Technical",
    "Sales / customer-facing",
    "Internal management",
]

MORTEN_TRIGGER_WORDS = ("løn", "rolle", "bim", "software", "automation", "ai", "knauf")


def is_morten_salary_prompt(description: str) -> bool:
    """Return true when the prompt matches the supported Morten salary storyline."""
    lowered = description.casefold()
    return any(word in lowered for word in MORTEN_TRIGGER_WORDS)
