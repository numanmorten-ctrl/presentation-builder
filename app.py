"""Streamlit UI for the Story JSON based presentation engine."""

from pathlib import Path

import streamlit as st

from src.content_salary import DECK_STYLES, DEFAULT_DECK_STYLE, DEFAULT_PROMPT, DEFAULT_SLIDE_COUNT
from src.story_builder import build_story
from src.ppt_engine import build_presentation_from_story
from src.schemas import validate_story

st.set_page_config(page_title="Executive Deck Studio", page_icon="📊", layout="wide")

st.title("Executive Deck Studio")
st.caption("User input → Story JSON → Layout Engine → PowerPoint Engine → .pptx output")

with st.container(border=True):
    prompt = st.text_area(
        "Describe the presentation",
        value=DEFAULT_PROMPT,
        height=240,
        help="Describe the audience, purpose, context, must-have messages and any evidence to include.",
    )

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    deck_style = st.selectbox("Deck style", DECK_STYLES, index=DECK_STYLES.index(DEFAULT_DECK_STYLE))
with col2:
    slide_count = st.number_input("Number of slides", min_value=1, max_value=9, value=DEFAULT_SLIDE_COUNT, step=1)
with col3:
    include_notes = st.checkbox("Include speaker notes", value=True)

if "story" not in st.session_state:
    st.session_state.story = None
if "output_path" not in st.session_state:
    st.session_state.output_path = None

st.markdown("---")
st.subheader("Story JSON preview")
st.write("The storyline is generated and validated before PowerPoint rendering, so content can be debugged independently from layout.")

if st.button("Generate PowerPoint", type="primary", use_container_width=True):
    if not prompt.strip():
        st.error("Please describe the presentation before generating a deck.")
    else:
        story = build_story(prompt, deck_style, int(slide_count), include_notes)
        validation = validate_story(story)
        if not validation.valid:
            st.error("Story JSON validation failed: " + "; ".join(validation.errors))
        else:
            output_path = build_presentation_from_story(story)
            st.session_state.story = story
            st.session_state.output_path = output_path
            st.success(f"Generated {output_path.name}")

if st.session_state.story:
    st.json(st.session_state.story, expanded=False)
else:
    preview_story = build_story(prompt, deck_style, int(slide_count), include_notes) if prompt.strip() else None
    if preview_story:
        st.json(preview_story, expanded=False)

if st.session_state.output_path:
    path = Path(st.session_state.output_path)
    st.download_button(
        label="Download generated .pptx",
        data=path.read_bytes(),
        file_name=path.name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True,
    )
