import streamlit as st
from app.components.cards import section_heading
from app.components.theme import apply_theme

apply_theme()

section_heading("WELCOME", "A clearer view of property value", "Real Estate AI combines a validated valuation model with market exploration tools.")
left, right = st.columns([1.35, 1])
with left:
    st.markdown("### Everything needed for an informed first pass")
    st.write("Use a consistent set of property details to create an estimate, compare similar listings, and inspect local pricing patterns.")
    if st.button("Estimate a property price", type="primary", use_container_width=True):
        st.switch_page("pages/2_Predict.py")
with right:
    st.markdown("<div class='insight-card'><span>HOW IT WORKS</span><h3>Inputs in. Context out.</h3><p>Area, layout, age, neighbourhood, and amenity score are evaluated together by the trained pipeline.</p></div>", unsafe_allow_html=True)
st.markdown("### Explore the workspace")
cards = st.columns(3)
for column, title, text in zip(cards, ["Estimate", "Understand", "Compare"], ["Generate a transparent price estimate.", "Explore pricing and supply patterns.", "Find properties that fit your needs."]):
    with column:
        st.markdown(f"<div class='feature-card'><h3>{title}</h3><p>{text}</p></div>", unsafe_allow_html=True)
