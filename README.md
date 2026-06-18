# presentation-builder

A local Streamlit web app for generating professional, executive-style PowerPoint presentations from structured input.

The first supported use case is a **Role development / salary conversation** deck for **Morten Numan**, built on the uploaded Knauf PowerPoint template at `templates/Knauf.pptx`.

## What the app does

The Streamlit app lets a user:

- choose a presentation type
- enter a title
- enter a target audience
- enter a key message
- click **Generate PowerPoint**
- download the generated `.pptx`

The generated file is saved to:

```text
output/morten_salary_deck_v1.pptx
```

## Generated deck structure

The default deck includes eight slides:

1. Cover slide
2. Professional development timeline
3. Role 2024 vs. role today
4. Value creation for Knauf
5. Interdisciplinary profile / difficult to benchmark
6. Documented results
7. Future role potential
8. Conclusion / dialogue about role, title and salary

## Design approach

The builder uses `python-pptx` and starts from `templates/Knauf.pptx` as the base presentation. Generated slides apply a Knauf-inspired red, white and grey visual system with:

- large executive headlines
- concise slide copy
- cards and comparison panels
- timelines and simple diagrams
- strong visual hierarchy
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
app.py                    # Streamlit user interface
requirements.txt          # Python dependencies
src/content_salary.py     # Default storyline and text for the first use case
src/diagrams.py           # Timeline, Venn and arrow diagram helpers
src/layouts.py            # Reusable PowerPoint layout primitives
src/ppt_builder.py        # Main presentation generation service
src/theme.py              # Knauf-inspired colors, fonts and sizing
templates/Knauf.pptx      # Uploaded base PowerPoint template
output/                   # Generated presentations
```

## Notes

`python-pptx` does not expose a stable public speaker-notes API. The project therefore stores speaker guidance as slide metadata and hidden off-canvas text so the notes remain packaged with the generated deck without relying on fragile private PowerPoint XML internals.
