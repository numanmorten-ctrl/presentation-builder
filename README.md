# Executive Deck Studio

A local Streamlit app that generates executive PowerPoint decks from a structured **Story JSON** contract. The project now follows a presentation-engine architecture instead of hardcoding slides directly in the UI.

## Architecture

```text
User input → Story JSON → Layout Engine → PowerPoint Engine → .pptx output
```

Project structure:

```text
app.py                    # Streamlit UI only
src/ai_engine.py          # Future AI integration facade
src/story_builder.py      # Rule-based Story JSON generator
src/layout_engine.py      # Slide-type renderers
src/template_manager.py   # Knauf template loading, cleanup and safe areas
src/ppt_engine.py         # Orchestrates rendering and saving
src/theme_engine.py       # Knauf theme tokens
src/content_salary.py     # Defaults and trigger words for the Morten use case
src/schemas.py            # Story JSON types and validation
src/utils.py              # Shared output and JSON helpers
templates/Knauf.pptx      # Base Knauf template
output/.gitkeep           # Output folder placeholder; generated pptx files are ignored
assets/                   # Optional assets
```

## Story JSON concept

The app first converts the user description into a structured story object:

```json
{
  "meta": {
    "title": "...",
    "subtitle": "...",
    "audience": "...",
    "style": "...",
    "language": "da",
    "include_speaker_notes": true
  },
  "slides": [
    { "type": "cover", "title": "...", "subtitle": "...", "speaker_notes": "..." }
  ]
}
```

This separation makes it possible to debug narrative quality before rendering PowerPoint. `src/schemas.py` validates the required fields for each supported slide type.

Supported slide types:

- `cover`
- `executive_summary`
- `timeline`
- `comparison`
- `value_cards`
- `house_model`
- `case_list`
- `hub_and_spokes`
- `conclusion`

## Current generator behavior

`src/story_builder.py` is rule based today and is ready for later OpenAI integration through `src/ai_engine.py`. If the prompt contains words such as `løn`, `rolle`, `BIM`, `software`, `automation`, `AI` or `Knauf`, it generates a Danish Morten salary/development storyline. Other prompts receive a generic executive storyline.

The default generated file is:

```text
output/morten_salary_deck_engine_v1.pptx
```

Generated `.pptx` files in `output/` are ignored by Git; `output/.gitkeep` keeps the directory present.

## Run the app

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Streamlit:

```bash
streamlit run app.py
```

The UI provides:

- presentation description text area
- deck style selector
- slide count input
- include speaker notes checkbox
- Story JSON preview
- PowerPoint generation and download

## Add a new slide type

1. Add the new `type` and required fields in `src/schemas.py`.
2. Teach `src/story_builder.py` to emit that slide JSON.
3. Add a renderer function in `src/layout_engine.py` with the signature `renderer(slide, slide_json, theme, safe_area)`.
4. Register it in `RENDERERS` in `src/layout_engine.py`.
5. If needed, update `src/template_manager.py` to map the new type to a different template layout.
6. Run validation and deck-generation checks.

## Verification

Useful checks:

```bash
python -m compileall app.py src
python - <<'PY'
from pptx import Presentation
from src.content_salary import DEFAULT_PROMPT
from src.story_builder import build_story
from src.ppt_engine import build_presentation_from_story

story = build_story(DEFAULT_PROMPT, slide_count=9)
path = build_presentation_from_story(story)
prs = Presentation(path)
assert len(prs.slides) == 9
print(path)
PY
```
