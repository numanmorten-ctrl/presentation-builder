"""Streamlit UI for the Story JSON based presentation engine."""

from pathlib import Path

import streamlit as st

from src.apv_geometry import APV_GEOMETRY_TYPES, calculate_apv_from_geometry, calculate_exposed_perimeter_mm
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
if "custom_profile_apv" not in st.session_state:
    st.session_state.custom_profile_apv = None

st.markdown("---")
st.subheader("Andre profiler")
st.caption("Indtast Ap/V direkte, eller beregn Ap/V ud fra en simpel profilgeometri.")

with st.container(border=True):
    apv_method = st.radio(
        "Metode",
        ["Indtast Ap/V direkte", "Beregn Ap/V ud fra geometri"],
        horizontal=True,
        key="custom_profile_apv_method",
    )

    if apv_method == "Indtast Ap/V direkte":
        direct_apv = st.number_input(
            "Ap/V (m⁻¹)",
            min_value=0.0,
            value=float(st.session_state.custom_profile_apv or 0.0),
            step=1.0,
            key="custom_profile_direct_apv_input",
        )
        st.session_state.custom_profile_apv = direct_apv if direct_apv > 0 else None
    else:
        st.info(
            "Denne beregning finder kun Ap/V for den valgte geometri. "
            "Den faktiske Fireboard-beklædning og antal beskyttede sider vælges i de næste trin."
        )
        geometry_labels = [geometry.label for geometry in APV_GEOMETRY_TYPES]
        geometry_by_label = {geometry.label: geometry for geometry in APV_GEOMETRY_TYPES}
        selected_label = st.selectbox("Geometri/eksponering", geometry_labels, key="custom_profile_geometry_type")
        selected_geometry = geometry_by_label[selected_label]
        st.caption(selected_geometry.description)

        dim_col1, dim_col2, dim_col3 = st.columns(3)
        with dim_col1:
            a_mm = st.number_input("a (mm)", min_value=0.0, step=1.0, key="custom_profile_a_mm")
        with dim_col2:
            b_mm = st.number_input("b (mm)", min_value=0.0, step=1.0, key="custom_profile_b_mm")
        with dim_col3:
            steel_area_mm2 = st.number_input("A (mm²)", min_value=0.0, step=10.0, key="custom_profile_area_mm2")

        if a_mm > 0 and b_mm > 0 and steel_area_mm2 > 0:
            exposed_perimeter_mm = calculate_exposed_perimeter_mm(selected_geometry.key, a_mm, b_mm)
            calculated_apv = calculate_apv_from_geometry(selected_geometry.key, a_mm, b_mm, steel_area_mm2)
            st.session_state.custom_profile_apv = calculated_apv
            st.success(f"F = {exposed_perimeter_mm:.1f} mm · Ap/V = {calculated_apv:.1f} m⁻¹")
        else:
            st.session_state.custom_profile_apv = None
            st.warning("Udfyld a, b og A for at beregne Ap/V.")

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
