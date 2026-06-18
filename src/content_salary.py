"""Structured default content for Morten Numan's salary/development deck."""

DEFAULT_PRESENTATION_TYPE = "Role development / salary conversation"
DEFAULT_TITLE = "Role development and salary dialogue"
DEFAULT_AUDIENCE = "Manager / HR business partner"
DEFAULT_KEY_MESSAGE = (
    "Morten's role has expanded materially in scope, impact and complexity, "
    "creating a strong basis for a dialogue about role, title and salary."
)
OUTPUT_FILENAME = "morten_salary_deck_v1.pptx"


def build_salary_story(title: str, audience: str, key_message: str) -> list[dict]:
    """Return the slide-by-slide storyline used by the PowerPoint builder."""
    return [
        {
            "kind": "cover",
            "title": title,
            "subtitle": "Salary and development conversation | Morten Numan",
            "audience": audience,
            "key_message": key_message,
            "notes": "Open with the purpose: a constructive dialogue about how the role has evolved and how compensation/title should reflect that evolution.",
        },
        {
            "kind": "timeline",
            "title": "Professional development timeline",
            "subtitle": "A role that has grown step-by-step in scope and accountability.",
            "items": [
                ("2024", "Defined role baseline", "Core responsibilities and expected delivery."),
                ("H1 2025", "Broader coordination", "More cross-functional involvement and stakeholder management."),
                ("H2 2025", "Higher complexity", "More independent problem solving across disciplines."),
                ("Today", "Expanded impact", "Visible contribution to business outcomes and team effectiveness."),
            ],
            "notes": "Use this slide to anchor the conversation in development over time, not a single isolated salary request.",
        },
        {
            "kind": "comparison",
            "title": "Role 2024 vs. role today",
            "left_title": "Role in 2024",
            "right_title": "Role today",
            "left": ["Defined task ownership", "Primarily within own function", "Operational execution focus"],
            "right": ["Broader role ownership", "Cross-functional coordination", "Advisory and execution focus"],
            "notes": "Emphasize the delta between formal role expectations and the role Morten is actually performing today.",
        },
        {
            "kind": "cards",
            "title": "Value creation for Knauf",
            "subtitle": "Contribution is visible across quality, speed and collaboration.",
            "cards": [
                ("Business continuity", "Keeps complex work moving with limited friction."),
                ("Better decisions", "Connects technical, commercial and operational perspectives."),
                ("Execution quality", "Turns ambiguity into structured plans and deliverables."),
                ("Team leverage", "Helps colleagues align, prioritize and progress."),
            ],
            "notes": "Translate role growth into business value. Keep the language factual and outcome-oriented.",
        },
        {
            "kind": "venn",
            "title": "Interdisciplinary profile — difficult to benchmark",
            "subtitle": "The role combines capabilities that are often benchmarked separately.",
            "circles": ["Technical insight", "Business understanding", "Stakeholder leadership"],
            "center": "Hybrid value profile",
            "notes": "Explain why simple salary benchmarking may understate the value of this hybrid role profile.",
        },
        {
            "kind": "results",
            "title": "Documented results",
            "subtitle": "Examples to support an evidence-based dialogue.",
            "metrics": [
                ("Higher", "ownership"),
                ("Broader", "scope"),
                ("Stronger", "alignment"),
                ("Faster", "execution"),
            ],
            "notes": "Replace placeholders with specific documented examples before the final conversation if available.",
        },
        {
            "kind": "potential",
            "title": "Future role potential",
            "subtitle": "A natural next step is to formalize the role that is already emerging.",
            "steps": ["Recognize current scope", "Clarify future mandate", "Align title and compensation"],
            "notes": "Position the ask as forward-looking: formalizing responsibilities helps both Morten and Knauf.",
        },
        {
            "kind": "conclusion",
            "title": "Conclusion: dialogue about role, title and salary",
            "message": "The role has expanded. The value profile has changed. The compensation framework should be reviewed accordingly.",
            "asks": ["Confirm role scope", "Discuss appropriate title", "Align salary with contribution and market difficulty"],
            "notes": "Close with a clear invitation to dialogue and agreement on next steps.",
        },
    ]
