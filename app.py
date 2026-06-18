"""Streamlit front end for local PowerPoint generation."""

from pathlib import Path

import streamlit as st

from src.content_salary import DEFAULT_AUDIENCE, DEFAULT_KEY_MESSAGE, DEFAULT_PRESENTATION_TYPE, DEFAULT_TITLE
from src.ppt_builder import build_presentation

st.set_page_config(page_title="Presentation Builder", page_icon="📊", layout="centered")

st.title("Presentation Builder")
st.caption("Generate executive-style PowerPoint decks from structured input.")

presentation_type = st.selectbox("Presentation type", [DEFAULT_PRESENTATION_TYPE])
title = st.text_input("Title", value=DEFAULT_TITLE)
audience = st.text_input("Target audience", value=DEFAULT_AUDIENCE)
key_message = st.text_area("Key message", value=DEFAULT_KEY_MESSAGE, height=120)

if st.button("Generate PowerPoint", type="primary"):
    if presentation_type != DEFAULT_PRESENTATION_TYPE:
        st.error("This presentation type is not implemented yet.")
    else:
        output_path = build_presentation(title=title, audience=audience, key_message=key_message)
        st.success(f"Generated {output_path.name}")
        st.download_button(
            label="Download generated .pptx",
            data=Path(output_path).read_bytes(),
            file_name=Path(output_path).name,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
