"""Streamlit front end for Executive Deck Studio."""

from pathlib import Path

import streamlit as st

from src.content_salary import DECK_STYLES, DEFAULT_DECK_STYLE, DEFAULT_PROMPT, DEFAULT_SLIDE_COUNT
from src.ppt_builder import build_presentation

st.set_page_config(page_title="Executive Deck Studio", page_icon="📊", layout="wide")

st.title("Executive Deck Studio")
st.caption("AI-style presentation workflow with a rule-based generator. OpenAI integration can be added later.")

with st.container(border=True):
    prompt = st.text_area(
        "Describe the presentation",
        value=DEFAULT_PROMPT,
        height=260,
        help="Describe the audience, purpose, context, must-have messages and any evidence to include.",
    )

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    deck_style = st.selectbox("Deck style", DECK_STYLES, index=DECK_STYLES.index(DEFAULT_DECK_STYLE))
with col2:
    slide_count = st.number_input("Number of slides", min_value=1, max_value=9, value=DEFAULT_SLIDE_COUNT, step=1)
with col3:
    include_notes = st.toggle("Include speaker notes", value=True)

st.markdown("---")
st.subheader("Default rule-based storyline")
st.write(
    "For now, the generator is optimized for the **Morten Numan salary/development conversation** and produces an executive Knauf-style deck."
)

if st.button("Generate PowerPoint", type="primary", use_container_width=True):
    if not prompt.strip():
        st.error("Please describe the presentation before generating a deck.")
    else:
        output_path = build_presentation(
            prompt=prompt,
            deck_style=deck_style,
            slide_count=int(slide_count),
            include_notes=include_notes,
        )
        st.success(f"Generated {output_path.name}")
        st.download_button(
            label="Download generated .pptx",
            data=Path(output_path).read_bytes(),
            file_name=Path(output_path).name,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )
