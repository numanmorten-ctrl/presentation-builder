"""Rule-based content for Executive Deck Studio's default salary/development deck."""

DEFAULT_DECK_STYLE = "Executive / McKinsey-style"
DEFAULT_SLIDE_COUNT = 9
DEFAULT_PROMPT = """Morten Numan salary/development conversation.

Create an executive deck for a constructive dialogue about how Morten's role has developed, how his interdisciplinary profile creates value for Knauf, and why role, title and salary should be reviewed."""
OUTPUT_FILENAME = "morten_salary_deck_v2.pptx"

DECK_STYLES = [
    "Executive / McKinsey-style",
    "Technical",
    "Sales / customer-facing",
    "Internal management",
]


def build_salary_story(
    prompt: str,
    deck_style: str = DEFAULT_DECK_STYLE,
    slide_count: int = DEFAULT_SLIDE_COUNT,
    include_notes: bool = True,
) -> list[dict]:
    """Return the slide-by-slide storyline used by the PowerPoint builder.

    The generator is intentionally rule based for now. It recognizes the default
    Morten Numan salary/development use case and shapes it into a concise
    executive narrative while preserving the user's prompt as context.
    """
    style_lens = {
        "Executive / McKinsey-style": "crisp executive storyline, quantified where possible, with clear asks",
        "Technical": "more emphasis on BIM, data, systems, automation, software and AI depth",
        "Sales / customer-facing": "more emphasis on customer value, credibility and business outcomes",
        "Internal management": "more emphasis on role clarity, mandate, governance and retention",
    }.get(deck_style, "crisp executive storyline")

    story = [
        {
            "kind": "cover",
            "title": "Role development and salary dialogue",
            "subtitle": "Morten Numan | Executive discussion document",
            "kicker": "KNAUF | EXECUTIVE DECK STUDIO",
            "key_message": "Expanded scope. Hybrid value profile. Time to align role, title and salary.",
            "context": prompt.strip(),
            "notes": "Open by positioning the meeting as a constructive development dialogue, not a transactional salary request.",
        },
        {
            "kind": "summary",
            "title": "Executive summary",
            "subtitle": "The role has outgrown a narrow benchmark.",
            "points": [
                ("Role scope", "Responsibilities have expanded beyond the original 2024 baseline."),
                ("Value creation", "Morten connects building expertise with BIM, data, systems and automation."),
                ("Decision ask", "Agree how role, title and salary should reflect the contribution today."),
            ],
            "notes": "Keep this slide short. It should give the manager the whole argument in under one minute.",
        },
        {
            "kind": "timeline",
            "title": "Professional journey timeline",
            "subtitle": "A steady move from execution to broader digital value creation.",
            "items": [
                ("2024", "Role baseline", "Defined responsibilities and expected delivery."),
                ("H1 2025", "Broader coordination", "More cross-functional collaboration and ownership."),
                ("H2 2025", "Digital leverage", "BIM, data and systems work became more central."),
                ("Today", "Hybrid impact", "Automation, software and AI potential extend the mandate."),
            ],
            "notes": "Use the timeline to show development as a fact pattern over time.",
        },
        {
            "kind": "comparison",
            "title": "Role 2024 vs. role today",
            "subtitle": "The actual role has materially increased in complexity.",
            "left_title": "2024 baseline",
            "right_title": "Today",
            "left": ["Defined task execution", "Mainly functional scope", "Limited benchmark complexity"],
            "right": ["End-to-end ownership", "Cross-functional digital mandate", "Difficult-to-benchmark hybrid profile"],
            "notes": "Emphasize the delta between formal role description and lived contribution.",
        },
        {
            "kind": "cards",
            "title": "Value creation for Knauf",
            "subtitle": "Impact sits at the intersection of productivity, quality and business translation.",
            "cards": [
                ("Productivity", "Automates and simplifies repeatable work."),
                ("Quality", "Improves structure, data discipline and consistency."),
                ("Speed", "Turns ambiguity into usable systems and decisions."),
                ("Leverage", "Helps teams work across technical and commercial boundaries."),
            ],
            "notes": "Translate skills into business outcomes: less friction, better decisions, faster delivery.",
        },
        {
            "kind": "house",
            "title": "Interdisciplinary profile — difficult to benchmark",
            "subtitle": "The profile is a stacked capability model, not a single-function role.",
            "foundation": "Building background and practical experience",
            "core": "BIM + data + systems",
            "levels": ["Automation", "Software", "AI"],
            "roof": "Digital products and business value",
            "notes": "Explain that market benchmarks often price these layers separately, while this role combines them.",
        },
        {
            "kind": "results",
            "title": "Documented results",
            "subtitle": "Evidence should be anchored in concrete examples before the meeting.",
            "metrics": [
                ("Broader", "scope"),
                ("Higher", "ownership"),
                ("Faster", "execution"),
                ("Stronger", "alignment"),
            ],
            "evidence": ["Projects delivered", "Processes improved", "Stakeholders supported"],
            "notes": "Replace placeholders with named projects, feedback and delivery outcomes if available.",
        },
        {
            "kind": "potential",
            "title": "Future potential",
            "subtitle": "Formalizing the role creates more value for Knauf and a clearer development path.",
            "steps": ["Recognize current scope", "Define future mandate", "Scale digital products", "Align title and salary"],
            "notes": "Position recognition as a business enabler: clarity helps both retention and value creation.",
        },
        {
            "kind": "conclusion",
            "title": "Conclusion / dialogue about role, title and salary",
            "message": "The contribution has changed materially; the role framework should now catch up.",
            "asks": ["Confirm role scope", "Discuss fitting title", "Review salary alignment"],
            "notes": "Close by asking for agreement on next steps, timeline and decision owners.",
        },
    ]

    for slide in story:
        slide["style_lens"] = style_lens
        if not include_notes:
            slide["notes"] = ""
    return story[: max(1, min(slide_count, len(story)))]
