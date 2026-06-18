# Executive Deck Studio

A local Streamlit web app for generating executive-style PowerPoint presentations. The app now uses an **AI-style presentation workflow** while remaining fully local and rule based; OpenAI API integration is intentionally not included yet.

The first supported use case is a **Morten Numan salary/development conversation** deck, built on the uploaded Knauf PowerPoint template at `templates/Knauf.pptx`.

## What the app does

The Streamlit app lets a user:

1. Describe the presentation in one large text area.
2. Choose a deck style:
   - Executive / McKinsey-style
   - Technical
   - Sales / customer-facing
   - Internal management
3. Choose the number of slides.
4. Choose whether to include speaker notes.
5. Click **Generate PowerPoint**.
6. Download the generated `.pptx`.

The generated file is saved to:

```text
output/morten_salary_deck_v2.pptx
```

## Generated deck structure

The default nine-slide deck includes:

1. Cover
2. Executive summary
3. Professional journey timeline
4. Role 2024 vs. role today
5. Value creation for Knauf
6. Interdisciplinary profile — difficult to benchmark
7. Documented results
8. Future potential
9. Conclusion / dialogue about role, title and salary

## Design approach

The builder uses `python-pptx` and starts from `templates/Knauf.pptx` as the base presentation. Generated slides apply a Knauf-inspired red, white and grey executive visual system with:

- large headlines
- concise slide copy with fewer words per slide
- strong whitespace
- cards and comparison panels
- timelines and arrows
- simple consulting-style diagrams
- a house model for the interdisciplinary profile slide:
  - foundation = building background and practical experience
  - core = BIM + data + systems
  - upper levels = automation + software + AI
  - roof = digital products and business value
- best-effort speaker-note metadata for each slide

## Setup

Create and activate a virtual environment if desired, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the local app:

```bash
streamlit run app.py
```

## Project structure

```text
app.py                    # Streamlit Executive Deck Studio interface
requirements.txt          # Python dependencies
src/content_salary.py     # Rule-based default storyline and workflow options
src/diagrams.py           # Timeline, house model and arrow diagram helpers
src/layouts.py            # Reusable PowerPoint layout primitives
src/ppt_builder.py        # Main presentation generation service
templates/Knauf.pptx      # Uploaded base PowerPoint template
output/                   # Generated presentations
```

## Notes

`python-pptx` does not expose a stable public speaker-notes API. The project therefore stores speaker guidance as slide metadata and hidden off-canvas text so the notes remain packaged with the generated deck without relying on fragile private PowerPoint XML internals.
